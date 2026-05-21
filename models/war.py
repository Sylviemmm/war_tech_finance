"""
战争数据模型 - COW数据适配
War Data Models - COW Data Adaptation
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from database import Base
import json

class War(Base):
    """战争表 - 基于COW (Correlates of War) 数据集结构"""
    __tablename__ = "wars"
    
    # 主键
    id = Column(Integer, primary_key=True, index=True, comment="内部ID")
    
    # COW数据源相关字段
    war_id = Column(String(20), unique=True, nullable=True, index=True, comment="COW战争编号，如 IS1, ES300")
    war_name = Column(String(200), nullable=False, index=True, comment="战争名称")
    
    # 战争类型 (基于COW分类)
    war_type = Column(String(100), nullable=True, comment="战争类型中文描述")
    war_type_code = Column(Integer, nullable=True, index=True, comment="COW类型代码: 1-8")
    
    # 时间信息
    start_date = Column(DateTime, nullable=True, index=True, comment="开始日期")
    end_date = Column(DateTime, nullable=True, comment="结束日期")
    start_year = Column(Integer, nullable=True, index=True, comment="开始年份")
    end_year = Column(Integer, nullable=True, comment="结束年份")
    
    # 参与方信息
    belligerents_side1 = Column(Text, nullable=True, comment="发起方/第一方 (分号分隔)")
    belligerents_side2 = Column(Text, nullable=True, comment="被发起方/第二方 (分号分隔)")
    initiator = Column(String(200), nullable=True, comment="战争发起者")
    
    # 伤亡与规模
    total_deaths = Column(Integer, nullable=True, default=0, comment="总战斗死亡人数")
    side1_deaths = Column(Integer, nullable=True, default=0, comment="第一方死亡人数")
    side2_deaths = Column(Integer, nullable=True, default=0, comment="第二方死亡人数")
    non_state_deaths = Column(Integer, nullable=True, default=0, comment="非国家方死亡人数")
    
    # 战争结果与影响
    outcome = Column(String(100), nullable=True, comment="战争结果")
    outcome_code = Column(Integer, nullable=True, comment="结果代码: 1-8")
    
    # 地理信息
    where_fought = Column(String(100), nullable=True, comment="战争发生地区")
    where_fought_code = Column(Integer, nullable=True, index=True, comment="地区代码: 1-9")
    
    # 数据源信息
    source_file = Column(String(100), nullable=True, comment="原始数据文件名")
    data_source = Column(String(50), nullable=True, default="COW", comment="数据来源标识")
    
    # 额外字段（用于扩展）
    description = Column(Text, nullable=True, comment="战争描述")
    impact_level = Column(Integer, nullable=True, comment="影响等级 1-10")
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<War(id={self.id}, war_id='{self.war_id}', name='{self.war_name}')>"
    
    def get_duration_days(self):
        """计算战争持续天数"""
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return None
    
    def get_belligerents_list(self):
        """获取参与方列表"""
        side1 = self.belligerents_side1.split('; ') if self.belligerents_side1 else []
        side2 = self.belligerents_side2.split('; ') if self.belligerents_side2 else []
        return {
            'side1': [s.strip() for s in side1 if s.strip()],
            'side2': [s.strip() for s in side2 if s.strip()]
        }
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "war_id": self.war_id,
            "war_name": self.war_name,
            "war_type": self.war_type,
            "war_type_code": self.war_type_code,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "start_year": self.start_year,
            "end_year": self.end_year,
            "belligerents_side1": self.belligerents_side1,
            "belligerents_side2": self.belligerents_side2,
            "initiator": self.initiator,
            "total_deaths": self.total_deaths,
            "side1_deaths": self.side1_deaths,
            "side2_deaths": self.side2_deaths,
            "non_state_deaths": self.non_state_deaths,
            "outcome": self.outcome,
            "outcome_code": self.outcome_code,
            "where_fought": self.where_fought,
            "where_fought_code": self.where_fought_code,
            "duration_days": self.get_duration_days(),
            "belligerents_list": self.get_belligerents_list(),
            "source_file": self.source_file,
            "data_source": self.data_source,
            "description": self.description,
            "impact_level": self.impact_level,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """从字典创建对象"""
        return cls(
            war_id=data.get("war_id"),
            war_name=data.get("war_name"),
            war_type=data.get("war_type"),
            war_type_code=data.get("war_type_code"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            start_year=data.get("start_year"),
            end_year=data.get("end_year"),
            belligerents_side1=data.get("belligerents_side1"),
            belligerents_side2=data.get("belligerents_side2"),
            initiator=data.get("initiator"),
            total_deaths=data.get("total_deaths", 0),
            side1_deaths=data.get("side1_deaths", 0),
            side2_deaths=data.get("side2_deaths", 0),
            non_state_deaths=data.get("non_state_deaths", 0),
            outcome=data.get("outcome"),
            outcome_code=data.get("outcome_code"),
            where_fought=data.get("where_fought"),
            where_fought_code=data.get("where_fought_code"),
            source_file=data.get("source_file"),
            data_source=data.get("data_source", "COW"),
            description=data.get("description"),
            impact_level=data.get("impact_level")
        )


class WarParticipant(Base):
    """战争参与方详细表（用于多对多关系）"""
    __tablename__ = "war_participants"
    
    id = Column(Integer, primary_key=True, index=True)
    war_id = Column(Integer, ForeignKey("wars.id"), nullable=False, comment="战争ID")
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=True, comment="国家ID")
    participant_name = Column(String(100), nullable=False, comment="参与方名称（用于非国家实体）")
    side = Column(Integer, nullable=False, comment="1=第一方, 2=第二方")
    is_initiator = Column(Integer, default=0, comment="0=否, 1=是")
    entry_date = Column(DateTime, nullable=True, comment="参战日期")
    exit_date = Column(DateTime, nullable=True, comment="退出日期")
    deaths = Column(Integer, nullable=True, default=0, comment="该方死亡人数")
    outcome = Column(String(50), nullable=True, comment="该方结果")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    
    def __repr__(self):
        return f"<WarParticipant(id={self.id}, war_id={self.war_id}, name='{self.participant_name}')>"


# COW数据字典（用于参考）
WAR_TYPE_DESCRIPTIONS = {
    1: "Inter-State War (国家间战争) - 两个或多个国际体系成员之间的战争",
    2: "Extra-State War (国家对外战争) - 国际体系成员与非成员之间的战争",
    3: "Extra-State War (国家对外战争) - 殖民战争",
    4: "Intra-State War (国内战争) - 中央政府 vs 内部对立集团",
    5: "Intra-State War (国内战争) - 地方政府 vs 内部对立集团",
    6: "Intra-State War (国内战争) - 非政府团体间的战争",
    7: "Intra-State War (国内战争) - 非政府团体间的战争（不同地区）",
    8: "Non-State War (非国家战争) - 非国际体系成员间的战争"
}

OUTCOME_DESCRIPTIONS = {
    1: "胜利 (Victory) - 一方实现主要战争目标",
    2: "失败 (Defeat) - 一方未能实现主要战争目标",
    3: "妥协 (Compromise) - 双方达成妥协",
    4: "转型 (Transformed) - 战争转型为其他类型",
    5: "继续 (Ongoing) - 战争仍在继续",
    6: "僵局 (Stalemate) - 战争陷入僵局",
    7: "释放 (Released) - 被占领土释放",
    8: "未知 (Unknown) - 结果未知"
}

WHERE_FOUGHT_DESCRIPTIONS = {
    1: "北美 (North America)",
    2: "西欧 (Western Europe)",
    3: "东欧 (Eastern Europe)",
    4: "拉美 (Latin America)",
    5: "撒哈拉以南非洲 (Sub-Saharan Africa)",
    6: "中东/北非 (Middle East/North Africa)",
    7: "亚洲 (Asia)",
    8: "大洋洲 (Oceania)",
    9: "跨地区 (Multi-regional)"
}
