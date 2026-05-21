"""
国家数据模型
Country Data Models
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from database import Base
import json

class Country(Base):
    """国家表"""
    __tablename__ = "countries"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True, comment="国家名称")
    iso_code = Column(String(10), unique=True, nullable=False, index=True, comment="ISO国家代码")
    iso3_code = Column(String(3), unique=True, nullable=True, comment="ISO3国家代码")
    continent = Column(String(50), nullable=True, comment="大洲")
    region = Column(String(50), nullable=True, comment="地区")
    political_system = Column(String(100), nullable=True, comment="政治体制")
    gdp = Column(Float, nullable=True, comment="GDP")
    military_spending = Column(Float, nullable=True, comment="军费开支")
    population = Column(Integer, nullable=True, comment="人口数量")
    latitude = Column(Float, nullable=True, comment="纬度")
    longitude = Column(Float, nullable=True, comment="经度")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<Country(id={self.id}, name='{self.name}', iso_code='{self.iso_code}')>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "iso_code": self.iso_code,
            "iso3_code": self.iso3_code,
            "continent": self.continent,
            "region": self.region,
            "political_system": self.political_system,
            "gdp": self.gdp,
            "military_spending": self.military_spending,
            "population": self.population,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """从字典创建对象"""
        return cls(
            name=data.get("name"),
            iso_code=data.get("iso_code"),
            iso3_code=data.get("iso3_code"),
            continent=data.get("continent"),
            region=data.get("region"),
            political_system=data.get("political_system"),
            gdp=data.get("gdp"),
            military_spending=data.get("military_spending"),
            population=data.get("population"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude")
        )