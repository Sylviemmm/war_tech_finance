"""
国家CRUD操作
Country CRUD Operations
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from models.country import Country
from schemas.country import CountryCreate, CountryUpdate, CountryFilter
from crud.base import CRUDBase

class CRUDCountry(CRUDBase[Country, CountryCreate, CountryUpdate]):
    """国家CRUD操作"""
    
    def get_by_iso_code(self, db: Session, iso_code: str) -> Optional[Country]:
        """根据ISO代码获取国家"""
        return db.query(Country).filter(Country.iso_code == iso_code).first()
    
    def get_by_name(self, db: Session, name: str) -> Optional[Country]:
        """根据名称获取国家"""
        return db.query(Country).filter(Country.name == name).first()
    
    def search_countries(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        search: Optional[str] = None,
        continent: Optional[str] = None,
        region: Optional[str] = None,
        min_population: Optional[int] = None,
        max_population: Optional[int] = None,
        min_gdp: Optional[float] = None,
        max_gdp: Optional[float] = None,
        order_by: str = "name",
        order_desc: bool = False
    ) -> List[Country]:
        """搜索国家"""
        query = db.query(Country)
        
        # 搜索条件
        if search:
            query = query.filter(
                or_(
                    Country.name.ilike(f"%{search}%"),
                    Country.iso_code.ilike(f"%{search}%"),
                    Country.iso3_code.ilike(f"%{search}%")
                )
            )
        
        # 过滤条件
        if continent:
            query = query.filter(Country.continent == continent)
        
        if region:
            query = query.filter(Country.region == region)
        
        if min_population is not None:
            query = query.filter(Country.population >= min_population)
        
        if max_population is not None:
            query = query.filter(Country.population <= max_population)
        
        if min_gdp is not None:
            query = query.filter(Country.gdp >= min_gdp)
        
        if max_gdp is not None:
            query = query.filter(Country.gdp <= max_gdp)
        
        # 排序
        order_field = getattr(Country, order_by)
        if order_desc:
            query = query.order_by(order_field.desc())
        else:
            query = query.order_by(order_field)
        
        # 分页
        return query.offset(skip).limit(limit).all()
    
    def get_countries_by_continent(self, db: Session, continent: str) -> List[Country]:
        """根据大洲获取国家"""
        return db.query(Country).filter(Country.continent == continent).all()
    
    def get_countries_by_region(self, db: Session, region: str) -> List[Country]:
        """根据地区获取国家"""
        return db.query(Country).filter(Country.region == region).all()
    
    def get_top_countries_by_population(
        self, 
        db: Session, 
        limit: int = 10
    ) -> List[Country]:
        """获取人口最多的国家"""
        return db.query(Country).filter(
            Country.population.isnot(None)
        ).order_by(Country.population.desc()).limit(limit).all()
    
    def get_top_countries_by_gdp(
        self, 
        db: Session, 
        limit: int = 10
    ) -> List[Country]:
        """获取GDP最高的国家"""
        return db.query(Country).filter(
            Country.gdp.isnot(None)
        ).order_by(Country.gdp.desc()).limit(limit).all()

# 创建国家CRUD实例
country = CRUDCountry(Country)