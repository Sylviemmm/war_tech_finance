"""
战争数据模式
War Data Schemas
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class WarBase(BaseModel):
    """战争基础模式"""
    name: str = Field(..., min_length=1, max_length=200, description="战争名称")
    start_date: datetime = Field(..., description="开始日期")
    end_date: Optional[datetime] = Field(None, description="结束日期")
    belligerents: Optional[Dict[str, Any]] = Field(None, description="参战方")
    casualties: Optional[int] = Field(None, ge=0, description="伤亡人数")
    geographic_scope: Optional[Dict[str, Any]] = Field(None, description="地理范围")
    war_type: Optional[str] = Field(None, description="战争类型: international, civil, colonial, proxy, hybrid")
    casus_belli: Optional[str] = Field(None, max_length=100, description="战争原因")
    impact_level: Optional[int] = Field(None, ge=1, le=10, description="影响程度 (1-10)")

    @validator('war_type')
    def validate_war_type(cls, v):
        """验证战争类型"""
        if v is not None and v not in ['international', 'civil', 'colonial', 'proxy', 'hybrid']:
            raise ValueError('战争类型必须是: international, civil, colonial, proxy, hybrid')
        return v

    @validator('impact_level')
    def validate_impact_level(cls, v):
        """验证影响程度"""
        if v is not None and (v < 1 or v > 10):
            raise ValueError('影响程度必须在1-10之间')
        return v

class WarCreate(WarBase):
    """创建战争模式"""
    pass

class WarUpdate(WarBase):
    """更新战争模式"""
    name: Optional[str] = None
    start_date: Optional[datetime] = None

class War(WarBase):
    """战争完整模式"""
    id: int
    duration_days: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class WarList(BaseModel):
    """战争列表模式"""
    wars: List[War]
    total: int
    page: int
    page_size: int

class WarFilter(BaseModel):
    """战争过滤模式"""
    start_date_from: Optional[datetime] = None
    start_date_to: Optional[datetime] = None
    end_date_from: Optional[datetime] = None
    end_date_to: Optional[datetime] = None
    war_type: Optional[str] = None
    min_casualties: Optional[int] = None
    max_casualties: Optional[int] = None
    min_impact_level: Optional[int] = None
    max_impact_level: Optional[int] = None
    search: Optional[str] = None

class WarStats(BaseModel):
    """战争统计模式"""
    total_wars: int
    wars_by_type: Dict[str, int]
    total_casualties: Optional[int]
    average_duration: Optional[float]
    wars_by_century: Dict[str, int]