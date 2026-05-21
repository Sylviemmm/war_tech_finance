"""
关系数据模式
Relation Data Schemas
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class RelationBase(BaseModel):
    """关系基础模式"""
    source_type: str = Field(..., description="源实体类型: war, technology, finance, country")
    source_id: int = Field(..., ge=1, description="源实体ID")
    target_type: str = Field(..., description="目标实体类型: war, technology, finance, country")
    target_id: int = Field(..., ge=1, description="目标实体ID")
    relation_type: str = Field(..., description="关系类型: catalyze, apply_to, finance, impact, invest, commercialize, participate, develop")
    strength: Optional[int] = Field(None, ge=1, le=10, description="关系强度 (1-10)")
    start_date: Optional[datetime] = Field(None, description="开始日期")
    end_date: Optional[datetime] = Field(None, description="结束日期")

    @validator('source_type')
    def validate_source_type(cls, v):
        """验证源实体类型"""
        if v not in ['war', 'technology', 'finance', 'country']:
            raise ValueError('源实体类型必须是: war, technology, finance, country')
        return v

    @validator('target_type')
    def validate_target_type(cls, v):
        """验证目标实体类型"""
        if v not in ['war', 'technology', 'finance', 'country']:
            raise ValueError('目标实体类型必须是: war, technology, finance, country')
        return v

    @validator('relation_type')
    def validate_relation_type(cls, v):
        """验证关系类型"""
        if v not in ['catalyze', 'apply_to', 'finance', 'impact', 'invest', 'commercialize', 'participate', 'develop']:
            raise ValueError('关系类型必须是: catalyze, apply_to, finance, impact, invest, commercialize, participate, develop')
        return v

    @validator('strength')
    def validate_strength(cls, v):
        """验证关系强度"""
        if v is not None and (v < 1 or v > 10):
            raise ValueError('关系强度必须在1-10之间')
        return v

class RelationCreate(RelationBase):
    """创建关系模式"""
    pass

class RelationUpdate(RelationBase):
    """更新关系模式"""
    source_type: Optional[str] = None
    source_id: Optional[int] = None
    target_type: Optional[str] = None
    target_id: Optional[int] = None

class Relation(RelationBase):
    """关系完整模式"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class RelationList(BaseModel):
    """关系列表模式"""
    relations: List[Relation]
    total: int
    page: int
    page_size: int

class RelationFilter(BaseModel):
    """关系过滤模式"""
    source_type: Optional[str] = None
    target_type: Optional[str] = None
    relation_type: Optional[str] = None
    min_strength: Optional[int] = None
    max_strength: Optional[int] = None
    start_date_from: Optional[datetime] = None
    start_date_to: Optional[datetime] = None
    end_date_from: Optional[datetime] = None
    end_date_to: Optional[datetime] = None

class RelationNetwork(BaseModel):
    """关系网络模式"""
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    total_nodes: int
    total_edges: int