"""
技术数据模式
Technology Data Schemas
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class TechnologyBase(BaseModel):
    """技术基础模式"""
    name: str = Field(..., min_length=1, max_length=200, description="技术名称")
    invention_date: Optional[datetime] = Field(None, description="发明日期")
    inventor: Optional[str] = Field(None, max_length=100, description="发明者")
    application_domain: Optional[str] = Field(None, max_length=100, description="应用领域")
    military_civilian: Optional[str] = Field(None, description="军事/民用属性: military, civilian, dual_use")
    patent_number: Optional[str] = Field(None, max_length=50, description="专利号")
    description: Optional[str] = Field(None, description="描述")
    significance_level: Optional[int] = Field(None, ge=1, le=10, description="重要性级别 (1-10)")

    @validator('military_civilian')
    def validate_military_civilian(cls, v):
        """验证军事/民用属性"""
        if v is not None and v not in ['military', 'civilian', 'dual_use']:
            raise ValueError('军事/民用属性必须是: military, civilian, dual_use')
        return v

    @validator('significance_level')
    def validate_significance_level(cls, v):
        """验证重要性级别"""
        if v is not None and (v < 1 or v > 10):
            raise ValueError('重要性级别必须在1-10之间')
        return v

    @validator('patent_number')
    def validate_patent_number(cls, v):
        """验证专利号格式"""
        if v is not None:
            # 简单的专利号格式验证
            if not v.replace('-', '').replace('/', '').isdigit():
                raise ValueError('专利号格式不正确')
        return v

class TechnologyCreate(TechnologyBase):
    """创建技术模式"""
    pass

class TechnologyUpdate(TechnologyBase):
    """更新技术模式"""
    name: Optional[str] = None

class Technology(TechnologyBase):
    """技术完整模式"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TechnologyList(BaseModel):
    """技术列表模式"""
    technologies: List[Technology]
    total: int
    page: int
    page_size: int

class TechnologyFilter(BaseModel):
    """技术过滤模式"""
    invention_date_from: Optional[datetime] = None
    invention_date_to: Optional[datetime] = None
    application_domain: Optional[str] = None
    military_civilian: Optional[str] = None
    min_significance_level: Optional[int] = None
    max_significance_level: Optional[int] = None
    search: Optional[str] = None

class TechnologyStats(BaseModel):
    """技术统计模式"""
    total_technologies: int
    technologies_by_domain: Dict[str, int]
    technologies_by_military_civilian: Dict[str, int]
    average_significance_level: float
    technologies_by_century: Dict[str, int]