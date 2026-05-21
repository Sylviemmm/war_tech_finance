"""
关系数据模型
Relation Data Models
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from database import Base
import json

class Relation(Base):
    """关系表"""
    __tablename__ = "relations"
    
    id = Column(Integer, primary_key=True, index=True)
    source_type = Column(String(50), nullable=False, index=True, comment="源实体类型: war, technology, finance, country")
    source_id = Column(Integer, nullable=False, index=True, comment="源实体ID")
    target_type = Column(String(50), nullable=False, index=True, comment="目标实体类型: war, technology, finance, country")
    target_id = Column(Integer, nullable=False, index=True, comment="目标实体ID")
    relation_type = Column(String(50), nullable=False, index=True, comment="关系类型: catalyze, apply_to, finance, impact, invest, commercialize, participate, develop")
    strength = Column(Integer, nullable=True, comment="关系强度 (1-10)")
    start_date = Column(DateTime, nullable=True, index=True, comment="开始日期")
    end_date = Column(DateTime, nullable=True, comment="结束日期")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    
    def __repr__(self):
        return f"<Relation(id={self.id}, source_type='{self.source_type}', target_type='{self.target_type}')>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "source_type": self.source_type,
            "source_id": self.source_id,
            "target_type": self.target_type,
            "target_id": self.target_id,
            "relation_type": self.relation_type,
            "strength": self.strength,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """从字典创建对象"""
        return cls(
            source_type=data.get("source_type"),
            source_id=data.get("source_id"),
            target_type=data.get("target_type"),
            target_id=data.get("target_id"),
            relation_type=data.get("relation_type"),
            strength=data.get("strength"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date")
        )