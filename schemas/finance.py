"""
金融数据模式
Finance Data Schemas
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class FinanceBase(BaseModel):
    """金融数据基础模式"""
    indicator_name: str = Field(..., min_length=1, max_length=100, description="指标名称")
    value: float = Field(..., description="数值")
    date: datetime = Field(..., description="日期")
    country_id: Optional[int] = Field(None, description="国家ID")
    data_type: Optional[str] = Field(None, description="数据类型: stock_price, exchange_rate, interest_rate, bond_yield")
    source: Optional[str] = Field(None, max_length=100, description="数据来源")
    impact_level: Optional[int] = Field(None, ge=1, le=10, description="影响程度 (1-10)")

    @validator('data_type')
    def validate_data_type(cls, v):
        """验证数据类型"""
        if v is not None and v not in ['stock_price', 'exchange_rate', 'interest_rate', 'bond_yield']:
            raise ValueError('数据类型必须是: stock_price, exchange_rate, interest_rate, bond_yield')
        return v

    @validator('impact_level')
    def validate_impact_level(cls, v):
        """验证影响程度"""
        if v is not None and (v < 1 or v > 10):
            raise ValueError('影响程度必须在1-10之间')
        return v

class FinanceCreate(FinanceBase):
    """创建金融数据模式"""
    pass

class FinanceUpdate(FinanceBase):
    """更新金融数据模式"""
    indicator_name: Optional[str] = None
    date: Optional[datetime] = None

class Finance(FinanceBase):
    """金融数据完整模式"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class FinanceList(BaseModel):
    """金融数据列表模式"""
    finance_data: List[Finance]
    total: int
    page: int
    page_size: int

class FinanceFilter(BaseModel):
    """金融数据过滤模式"""
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    country_id: Optional[int] = None
    data_type: Optional[str] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    min_impact_level: Optional[int] = None
    max_impact_level: Optional[int] = None
    search: Optional[str] = None

class FinanceStats(BaseModel):
    """金融数据统计模式"""
    total_records: int
    records_by_type: Dict[str, int]
    average_value: float
    min_value: float
    max_value: float
    records_by_country: Dict[str, int]