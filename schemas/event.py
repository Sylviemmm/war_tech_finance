"""
事件数据模式
Event Data Schemas
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class EventBase(BaseModel):
    """事件基础模式"""
    name: str = Field(..., min_length=1, max_length=200, description="事件名称")
    event_date: datetime = Field(..., description="事件日期")
    event_type: Optional[str] = Field(None, description="事件类型: war_event, tech_breakthrough, financial_crisis")
    description: Optional[str] = Field(None, description="描述")
    related_entities: Optional[Dict[str, Any]] = Field(None, description="关联实体")
    impact_score: Optional[int] = Field(None, ge=1, le=10, description="影响分数 (1-10)")

    @validator('event_type')
    def validate_event_type(cls, v):
        """验证事件类型"""
        if v is not None and v not in ['war_event', 'tech_breakthrough', 'financial_crisis']:
            raise ValueError('事件类型必须是: war_event, tech_breakthrough, financial_crisis')
        return v

    @validator('impact_score')
    def validate_impact_score(cls, v):
        """验证影响分数"""
        if v is not None and (v < 1 or v > 10):
            raise ValueError('影响分数必须在1-10之间')
        return v

class EventCreate(EventBase):
    """创建事件模式"""
    pass

class EventUpdate(EventBase):
    """更新事件模式"""
    name: Optional[str] = None
    event_date: Optional[datetime] = None

class Event(EventBase):
    """事件完整模式"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EventList(BaseModel):
    """事件列表模式"""
    events: List[Event]
    total: int
    page: int
    page_size: int

class EventFilter(BaseModel):
    """事件过滤模式"""
    event_date_from: Optional[datetime] = None
    event_date_to: Optional[datetime] = None
    event_type: Optional[str] = None
    min_impact_score: Optional[int] = None
    max_impact_score: Optional[int] = None
    search: Optional[str] = None