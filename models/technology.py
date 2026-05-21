"""
技术数据模型
Technology Data Models
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from database import Base
import json

class Technology(Base):
    """技术表"""
    __tablename__ = "technologies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True, comment="技术名称")
    invention_date = Column(DateTime, nullable=True, index=True, comment="发明日期")
    inventor = Column(String(100), nullable=True, comment="发明者")
    application_domain = Column(String(100), nullable=True, comment="应用领域")
    military_civilian = Column(String(20), nullable=True, comment="军事/民用属性: military, civilian, dual_use")
    patent_number = Column(String(50), nullable=True, comment="专利号")
    description = Column(Text, nullable=True, comment="描述")
    significance_level = Column(Integer, nullable=True, comment="重要性级别 (1-10)")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<Technology(id={self.id}, name='{self.name}', invention_date='{self.invention_date}')>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "invention_date": self.invention_date.isoformat() if self.invention_date else None,
            "inventor": self.inventor,
            "application_domain": self.application_domain,
            "military_civilian": self.military_civilian,
            "patent_number": self.patent_number,
            "description": self.description,
            "significance_level": self.significance_level,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """从字典创建对象"""
        return cls(
            name=data.get("name"),
            invention_date=data.get("invention_date"),
            inventor=data.get("inventor"),
            application_domain=data.get("application_domain"),
            military_civilian=data.get("military_civilian"),
            patent_number=data.get("patent_number"),
            description=data.get("description"),
            significance_level=data.get("significance_level")
        )