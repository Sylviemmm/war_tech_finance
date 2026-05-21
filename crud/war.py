"""
战争CRUD操作
War CRUD Operations
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from models.war import War
from schemas.war import WarCreate, WarUpdate, WarFilter
from crud.base import CRUDBase

class CRUDWar(CRUDBase[War, WarCreate, WarUpdate]):
    """战争CRUD操作"""
    
    def get_by_name(self, db: Session, name: str) -> Optional[War]:
        """根据名称获取战争"""
        return db.query(War).filter(War.name == name).first()
    
    def search_wars(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        search: Optional[str] = None,
        start_date_from: Optional[Any] = None,
        start_date_to: Optional[Any] = None,
        end_date_from: Optional[Any] = None,
        end_date_to: Optional[Any] = None,
        war_type: Optional[str] = None,
        min_casualties: Optional[int] = None,
        max_casualties: Optional[int] = None,
        min_impact_level: Optional[int] = None,
        max_impact_level: Optional[int] = None,
        order_by: str = "start_date",
        order_desc: bool = False
    ) -> List[War]:
        """搜索战争"""
        query = db.query(War)
        
        # 搜索条件
        if search:
            query = query.filter(
                or_(
                    War.name.ilike(f"%{search}%"),
                    War.casus_belli.ilike(f"%{search}%")
                )
            )
        
        # 时间范围过滤
        if start_date_from:
            query = query.filter(War.start_date >= start_date_from)
        
        if start_date_to:
            query = query.filter(War.start_date <= start_date_to)
        
        if end_date_from:
            query = query.filter(War.end_date >= end_date_from)
        
        if end_date_to:
            query = query.filter(War.end_date <= end_date_to)
        
        # 其他过滤条件
        if war_type:
            query = query.filter(War.war_type == war_type)
        
        if min_casualties is not None:
            query = query.filter(War.casualties >= min_casualties)
        
        if max_casualties is not None:
            query = query.filter(War.casualties <= max_casualties)
        
        if min_impact_level is not None:
            query = query.filter(War.impact_level >= min_impact_level)
        
        if max_impact_level is not None:
            query = query.filter(War.impact_level <= max_impact_level)
        
        # 排序
        order_field = getattr(War, order_by)
        if order_desc:
            query = query.order_by(order_field.desc())
        else:
            query = query.order_by(order_field)
        
        # 分页
        return query.offset(skip).limit(limit).all()
    
    def get_wars_by_type(self, db: Session, war_type: str) -> List[War]:
        """根据类型获取战争"""
        return db.query(War).filter(War.war_type == war_type).all()
    
    def get_wars_by_date_range(
        self, 
        db: Session, 
        start_date: Any, 
        end_date: Any
    ) -> List[War]:
        """根据日期范围获取战争"""
        return db.query(War).filter(
            and_(
                War.start_date >= start_date,
                War.start_date <= end_date
            )
        ).all()
    
    def get_longest_wars(self, db: Session, limit: int = 10) -> List[War]:
        """获取持续时间最长的战争"""
        return db.query(War).filter(
            War.duration_days.isnot(None)
        ).order_by(War.duration_days.desc()).limit(limit).all()
    
    def get_deadliest_wars(self, db: Session, limit: int = 10) -> List[War]:
        """获取伤亡人数最多的战争"""
        return db.query(War).filter(
            War.casualties.isnot(None)
        ).order_by(War.casualties.desc()).limit(limit).all()
    
    def get_wars_by_century(self, db: Session, century: int) -> List[War]:
        """根据世纪获取战争"""
        start_year = (century - 1) * 100
        end_year = century * 100 - 1
        
        return db.query(War).filter(
            func.extract('year', War.start_date).between(start_year, end_year)
        ).all()
    
    def get_wars_stats(self, db: Session) -> Dict[str, Any]:
        """获取战争统计信息"""
        total_wars = db.query(War).count()
        
        # 按类型统计
        wars_by_type = {}
        war_types = db.query(War.war_type).distinct().all()
        for wt in war_types:
            if wt[0]:
                wars_by_type[wt[0]] = db.query(War).filter(War.war_type == wt[0]).count()
        
        # 总伤亡人数
        total_casualties = db.query(func.sum(War.casualties)).scalar() or 0
        
        # 平均持续时间
        avg_duration = db.query(func.avg(War.duration_days)).scalar() or 0
        
        # 按世纪统计
        wars_by_century = {}
        for century in range(18, 22):  # 18-21世纪
            wars_by_century[f"{century}世纪"] = len(self.get_wars_by_century(db, century))
        
        return {
            "total_wars": total_wars,
            "wars_by_type": wars_by_type,
            "total_casualties": total_casualties,
            "average_duration": avg_duration,
            "wars_by_century": wars_by_century
        }

    def get_detailed_war_data(
        self, 
        db: Session, 
        war_type: Optional[str] = None,
        min_deaths: int = 0,
        min_year: int = 1800,
        limit: int = 1000
    ) -> List[Dict[str, Any]]:
        """获取详细的战争数据用于可视化"""
        query = db.query(War)
        
        # 过滤条件
        if war_type:
            query = query.filter(War.war_type_code == int(war_type))
        
        query = query.filter(
            and_(
                War.start_year >= min_year,
                War.total_deaths >= min_deaths
            )
        )
        
        # 按开始日期排序
        query = query.order_by(War.start_date)
        
        # 限制数量
        wars = query.limit(limit).all()
        
        # 转换为可视化格式
        result = []
        for war_obj in wars:
            # 计算地理坐标（基于地区）
            lat, lon = self._get_coordinates_by_region(war_obj.where_fought)
            
            # 计算颜色深度
            color = self._get_death_color(war_obj.total_deaths, war_obj.war_type_code)
            
            # 计算点大小
            size = self._get_point_size(war_obj.total_deaths)
            
            war_data = {
                'war_id': war_obj.war_id,
                'war_name': war_obj.war_name,
                'war_type_code': war_obj.war_type_code,
                'war_type': war_obj.war_type or 'Unknown',
                'start_date': war_obj.start_date.isoformat() if war_obj.start_date else '',
                'end_date': war_obj.end_date.isoformat() if war_obj.end_date else '',
                'start_year': war_obj.start_year,
                'total_deaths': war_obj.total_deaths or 0,
                'belligerents_side1': war_obj.belligerents_side1,
                'belligerents_side2': war_obj.belligerents_side2,
                'initiator': war_obj.initiator,
                'outcome': war_obj.outcome,
                'where_fought': war_obj.where_fought,
                'lat': lat,
                'lon': lon,
                'color': color,
                'size': size
            }
            result.append(war_data)
        
        return result
    
    def _get_coordinates_by_region(self, region: Optional[str]) -> tuple:
        """根据地区获取地理坐标"""
        region_coords = {
            '北美 (North America)': {'lat': 40, 'lon': -100},
            '西欧 (Western Europe)': {'lat': 50, 'lon': 10},
            '东欧 (Eastern Europe)': {'lat': 55, 'lon': 30},
            '拉美 (Latin America)': {'lat': -15, 'lon': -60},
            '撒哈拉以南非洲 (Sub-Saharan Africa)': {'lat': -5, 'lon': 20},
            '中东/北非 (Middle East/North Africa)': {'lat': 30, 'lon': 35},
            '亚洲 (Asia)': {'lat': 35, 'lon': 100},
            '大洋洲 (Oceania)': {'lat': -25, 'lon': 135},
            '跨地区 (Multi-regional)': {'lat': 20, 'lon': 0}
        }
        
        if region in region_coords:
            coords = region_coords[region]
            # 添加随机偏移，避免重叠
            import random
            lat = coords['lat'] + random.uniform(-5, 5)
            lon = coords['lon'] + random.uniform(-10, 10)
            return lat, lon
        else:
            return 20, 0  # 默认世界中心
    
    def _get_death_color(self, deaths: int, war_type_code: int) -> str:
        """根据伤亡数和战争类型计算颜色"""
        WAR_TYPE_COLORS = {
            1: '#ff6b6b',  # 国家间战争 - 红色系
            2: '#4ecdc4',  # 国家对外战争 - 青色系
            3: '#45b7d1',  # 国家对外战争 - 蓝色系
            4: '#96ceb4',  # 国内战争-中央政府 - 绿色系
            5: '#feca57',  # 国内战争-地方政府 - 黄色系
            6: '#ff9ff3',  # 国内战争-非政府 - 粉色系
            7: '#54a0ff',  # 国内战争-非政府 - 深蓝色
            8: '#5f27cd',  # 非国家战争 - 紫色
            9: '#ff6b6b'   # 未知类型 - 使用红色系
        }
        
        if deaths == 0:
            return WAR_TYPE_COLORS.get(war_type_code, '#ff6b6b') + '40'  # 透明
        
        # 计算颜色深度
        max_deaths = 1000000  # 假设最大伤亡数
        min_deaths = 1
        
        if deaths <= min_deaths:
            depth = 0.3
        elif deaths >= max_deaths:
            depth = 1.0
        else:
            depth = 0.3 + 0.7 * (deaths - min_deaths) / (max_deaths - min_deaths)
        
        # 将深度转换为透明度
        alpha = int(40 + depth * 215)  # 40-255
        
        # 获取基础颜色
        base_color = WAR_TYPE_COLORS.get(war_type_code, '#ff6b6b')
        
        # 转换为RGBA
        if base_color.startswith('#'):
            r = int(base_color[1:3], 16)
            g = int(base_color[3:5], 16)
            b = int(base_color[5:7], 16)
            return f'rgba({r}, {g}, {b}, {alpha/255})'
        
        return base_color
    
    def _get_point_size(self, deaths: int) -> int:
        """根据伤亡数计算点大小"""
        if deaths == 0:
            return 5
        
        max_deaths = 1000000  # 假设最大伤亡数
        min_deaths = 1
        
        if deaths <= min_deaths:
            size = 8
        elif deaths >= max_deaths:
            size = 25
        else:
            size = 8 + 17 * (deaths - min_deaths) / (max_deaths - min_deaths)
        
        return int(size)

# 创建战争CRUD实例
war = CRUDWar(War)