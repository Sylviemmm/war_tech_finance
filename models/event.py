"""
事件数据模型
Event Data Models
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from database import Base
import json

class Event(Base):
    """事件表"""
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True, comment="事件名称")
    event_date = Column(DateTime, nullable=False, index=True, comment="事件日期")
    event_type = Column(String(50), nullable=True, index=True, comment="事件类型: war_event, tech_breakthrough, financial_crisis")
    description = Column(Text, nullable=True, comment="描述")
    related_entities = Column(Text, nullable=True, comment="关联实体 (JSON)")
    impact_score = Column(Integer, nullable=True, comment="影响分数 (1-10)")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<Event(id={self.id}, name='{self.name}', event_date='{self.event_date}')>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "event_date": self.event_date.isoformat() if self.event_date else None,
            "event_type": self.event_type,
            "description": self.description,
            "related_entities": json.loads(self.related_entities) if self.related_entities else None,
            "impact_score": self.impact_score,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """从字典创建对象"""
        return cls(
            name=data.get("name"),
            event_date=data.get("event_date"),
            event_type=data.get("event_type"),
            description=data.get("description"),
            related_entities=json.dumps(data.get("related_entities")) if data.get("related_entities") else None,
            impact_score=data.get("impact_score")
        )