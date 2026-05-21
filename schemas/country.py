"""
国家数据模式
Country Data Schemas
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class CountryBase(BaseModel):
    """国家基础模式"""
    name: str = Field(..., min_length=1, max_length=100, description="国家名称")
    iso_code: str = Field(..., min_length=2, max_length=10, description="ISO国家代码")
    iso3_code: Optional[str] = Field(None, max_length=3, description="ISO3国家代码")
    continent: Optional[str] = Field(None, max_length=50, description="大洲")
    region: Optional[str] = Field(None, max_length=50, description="地区")
    political_system: Optional[str] = Field(None, max_length=100, description="政治体制")
    gdp: Optional[float] = Field(None, description="GDP")
    military_spending: Optional[float] = Field(None, description="军费开支")
    population: Optional[int] = Field(None, ge=0, description="人口数量")
    latitude: Optional[float] = Field(None, ge=-90, le=90, description="纬度")
    longitude: Optional[float] = Field(None, ge=-180, le=180, description="经度")

    @validator('iso_code')
    def validate_iso_code(cls, v):
        """验证ISO代码格式"""
        if not v.isupper():
            raise ValueError('ISO代码必须为大写字母')
        return v

class CountryCreate(CountryBase):
    """创建国家模式"""
    pass

class CountryUpdate(CountryBase):
    """更新国家模式"""
    name: Optional[str] = None
    iso_code: Optional[str] = None

class Country(CountryBase):
    """国家完整模式"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CountryList(BaseModel):
    """国家列表模式"""
    countries: List[Country]
    total: int
    page: int
    page_size: int

class CountryFilter(BaseModel):
    """国家过滤模式"""
    continent: Optional[str] = None
    region: Optional[str] = None
    min_population: Optional[int] = None
    max_population: Optional[int] = None
    min_gdp: Optional[float] = None
    max_gdp: Optional[float] = None
    search: Optional[str] = None