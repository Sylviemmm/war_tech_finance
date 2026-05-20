from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# ==================== 国家相关Schema ====================

class CountryBase(BaseModel):
    name: str
    iso_code: Optional[str] = None
    iso3_code: Optional[str] = None
    continent: Optional[str] = None
    region: Optional[str] = None
    political_system: Optional[str] = None
    gdp: Optional[float] = None
    military_spending: Optional[float] = None
    population: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class CountryCreate(CountryBase):
    pass

class CountryUpdate(CountryBase):
    name: Optional[str] = None

class Country(CountryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ==================== 战争相关Schema (COW数据适配) ====================

class WarBase(BaseModel):
    war_name: str
    war_type: Optional[str] = None
    war_type_code: Optional[int] = Field(None, ge=1, le=8, description="COW战争类型代码: 1-8")
    
    # 时间信息
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    
    # 参与方信息
    belligerents_side1: Optional[str] = None  # 发起方/第一方
    belligerents_side2: Optional[str] = None  # 被发起方/第二方
    initiator: Optional[str] = None  # 战争发起者
    
    # 伤亡与规模
    total_deaths: Optional[int] = Field(0, ge=0)
    side1_deaths: Optional[int] = Field(0, ge=0)
    side2_deaths: Optional[int] = Field(0, ge=0)
    non_state_deaths: Optional[int] = Field(0, ge=0)
    
    # 战争结果
    outcome: Optional[str] = None
    outcome_code: Optional[int] = Field(None, ge=1, le=8)
    
    # 地理信息
    where_fought: Optional[str] = None
    where_fought_code: Optional[int] = Field(None, ge=1, le=9)
    
    # 数据源
    source_file: Optional[str] = None
    data_source: Optional[str] = "COW"
    
    # 扩展字段
    description: Optional[str] = None
    impact_level: Optional[int] = Field(None, ge=1, le=10)

class WarCreate(WarBase):
    war_id: Optional[str] = None  # COW战争编号，如 IS1, ES300

class WarUpdate(BaseModel):
    war_name: Optional[str] = None
    war_type: Optional[str] = None
    war_type_code: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    belligerents_side1: Optional[str] = None
    belligerents_side2: Optional[str] = None
    initiator: Optional[str] = None
    total_deaths: Optional[int] = None
    outcome: Optional[str] = None
    where_fought: Optional[str] = None
    description: Optional[str] = None
    impact_level: Optional[int] = None

class War(WarBase):
    id: int
    war_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # 计算字段
    duration_days: Optional[int] = None
    belligerents_list: Optional[Dict[str, List[str]]] = None

    class Config:
        from_attributes = True

class WarDetail(War):
    """战争详情Schema，包含关联数据"""
    participants: List[Dict[str, Any]] = []
    related_technologies: List[Dict[str, Any]] = []
    related_finance: List[Dict[str, Any]] = []
    related_events: List[Dict[str, Any]] = []

# ==================== 战争统计Schema ====================

class WarStatistics(BaseModel):
    total_wars: int
    wars_by_type: Dict[str, int]
    wars_by_region: Dict[str, int]
    total_deaths: int
    avg_duration_days: Optional[float]
    wars_by_period: Dict[str, int]

class WarFilter(BaseModel):
    """战争筛选条件"""
    war_type_code: Optional[int] = None
    where_fought_code: Optional[int] = None
    start_year_from: Optional[int] = None
    start_year_to: Optional[int] = None
    min_deaths: Optional[int] = None
    max_deaths: Optional[int] = None
    initiator: Optional[str] = None
    outcome_code: Optional[int] = None

# ==================== 战争参与方Schema ====================

class WarParticipantBase(BaseModel):
    participant_name: str
    side: int = Field(..., ge=1, le=2)
    is_initiator: int = Field(0, ge=0, le=1)
    entry_date: Optional[datetime] = None
    exit_date: Optional[datetime] = None
    deaths: Optional[int] = Field(0, ge=0)
    outcome: Optional[str] = None

class WarParticipantCreate(WarParticipantBase):
    war_id: int
    country_id: Optional[int] = None

class WarParticipant(WarParticipantBase):
    id: int
    war_id: int
    country_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

# ==================== 技术相关Schema ====================

class TechnologyBase(BaseModel):
    name: str
    invention_date: Optional[datetime] = None
    inventor: Optional[str] = None
    application_domain: Optional[str] = None
    military_civilian: Optional[str] = None
    patent_number: Optional[str] = None
    description: Optional[str] = None
    significance_level: Optional[int] = Field(None, ge=1, le=10)
    impact_on_warfare: Optional[str] = None

class TechnologyCreate(TechnologyBase):
    related_war_id: Optional[int] = None

class TechnologyUpdate(TechnologyBase):
    name: Optional[str] = None

class Technology(TechnologyBase):
    id: int
    related_war_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ==================== 金融数据相关Schema ====================

class FinanceBase(BaseModel):
    indicator_name: str
    value: float
    date: datetime
    data_type: Optional[str] = None
    source: Optional[str] = None
    impact_level: Optional[int] = Field(None, ge=1, le=10)
    war_finance_type: Optional[str] = None  # 战争融资类型

class FinanceCreate(FinanceBase):
    country_id: Optional[int] = None
    related_war_id: Optional[int] = None

class FinanceUpdate(FinanceBase):
    indicator_name: Optional[str] = None
    value: Optional[float] = None
    date: Optional[datetime] = None

class Finance(FinanceBase):
    id: int
    country_id: Optional[int] = None
    related_war_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

# ==================== 事件相关Schema ====================

class EventBase(BaseModel):
    name: str
    event_date: datetime
    event_type: Optional[str] = None
    description: Optional[str] = None
    related_entities: Optional[str] = None
    impact_score: Optional[int] = Field(None, ge=1, le=10)
    event_role: Optional[str] = None  # 事件角色: 导火索、转折点等

class EventCreate(EventBase):
    related_war_id: Optional[int] = None

class EventUpdate(EventBase):
    name: Optional[str] = None
    event_date: Optional[datetime] = None

class Event(EventBase):
    id: int
    related_war_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ==================== 关系相关Schema ====================

class RelationBase(BaseModel):
    source_type: str
    source_id: int
    target_type: str
    target_id: int
    relation_type: str
    strength: Optional[int] = Field(None, ge=1, le=10)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class RelationCreate(RelationBase):
    pass

class RelationUpdate(RelationBase):
    relation_type: Optional[str] = None
    strength: Optional[int] = None

class Relation(RelationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# ==================== 数据导入Schema ====================

class DataImportResponse(BaseModel):
    success: bool
    message: str
    imported_count: int
    errors: List[str] = []

class COWDataImport(BaseModel):
    """COW数据导入配置"""
    file_path: str
    war_type_mapping: Optional[Dict[int, str]] = None
    skip_existing: bool = True

# ==================== API响应Schema ====================

class PaginatedResponse(BaseModel):
    total: int
    page: int
    page_size: int
    pages: int
    items: List[Any]

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
