"""
金融数据模型
Finance Data Models
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from database import Base
import json

class Finance(Base):
    """金融数据表"""
    __tablename__ = "finance_data"
    
    id = Column(Integer, primary_key=True, index=True)
    indicator_name = Column(String(100), nullable=False, index=True, comment="指标名称")
    value = Column(Float, nullable=False, comment="数值")
    date = Column(DateTime, nullable=False, index=True, comment="日期")
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=True, index=True, comment="国家ID")
    data_type = Column(String(50), nullable=True, index=True, comment="数据类型: stock_price, exchange_rate, interest_rate, bond_yield")
    source = Column(String(100), nullable=True, comment="数据来源")
    impact_level = Column(Integer, nullable=True, comment="影响程度 (1-10)")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    
    def __repr__(self):
        return f"<Finance(id={self.id}, indicator_name='{self.indicator_name}', date='{self.date}')>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "indicator_name": self.indicator_name,
            "value": self.value,
            "date": self.date.isoformat() if self.date else None,
            "country_id": self.country_id,
            "data_type": self.data_type,
            "source": self.source,
            "impact_level": self.impact_level,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """从字典创建对象"""
        return cls(
            indicator_name=data.get("indicator_name"),
            value=data.get("value"),
            date=data.get("date"),
            country_id=data.get("country_id"),
            data_type=data.get("data_type"),
            source=data.get("source"),
            impact_level=data.get("impact_level")
        )