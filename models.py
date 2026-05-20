from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Enum
from sqlalchemy.sql import func
from database import Base
import json

class Country(Base):
    __tablename__ = "countries"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    iso_code = Column(String(10), unique=True, nullable=True)
    iso3_code = Column(String(3), unique=True, nullable=True)
    continent = Column(String(50), nullable=True)
    region = Column(String(50), nullable=True)
    political_system = Column(String(100), nullable=True)
    gdp = Column(Float, nullable=True)
    military_spending = Column(Float, nullable=True)
    population = Column(Integer, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class War(Base):
    __tablename__ = "wars"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # COW数据源相关字段
    war_id = Column(String(20), unique=True, nullable=True, index=True)  # COW战争编号，如 IS1, ES300
    war_name = Column(String(200), nullable=False)
    
    # 战争类型 (基于COW分类)
    war_type = Column(String(100), nullable=True)  # 中文描述
    war_type_code = Column(Integer, nullable=True)  # COW类型代码: 1-8
    
    # 时间信息
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    start_year = Column(Integer, nullable=True)
    end_year = Column(Integer, nullable=True)
    
    # 参与方信息
    belligerents_side1 = Column(Text, nullable=True)  # 发起方/第一方
    belligerents_side2 = Column(Text, nullable=True)  # 被发起方/第二方
    initiator = Column(String(200), nullable=True)  # 战争发起者
    
    # 伤亡与规模
    total_deaths = Column(Integer, nullable=True, default=0)  # 总战斗死亡人数
    side1_deaths = Column(Integer, nullable=True, default=0)  # 第一方死亡人数
    side2_deaths = Column(Integer, nullable=True, default=0)  # 第二方死亡人数
    non_state_deaths = Column(Integer, nullable=True, default=0)  # 非国家方死亡人数
    
    # 战争结果与影响
    outcome = Column(String(100), nullable=True)  # 战争结果
    outcome_code = Column(Integer, nullable=True)  # 结果代码: 1-8
    
    # 地理信息
    where_fought = Column(String(100), nullable=True)  # 战争发生地区
    where_fought_code = Column(Integer, nullable=True)  # 地区代码: 1-9
    
    # 数据源信息
    source_file = Column(String(100), nullable=True)  # 原始数据文件名
    data_source = Column(String(50), nullable=True, default="COW")  # 数据来源标识
    
    # 额外字段（用于扩展）
    description = Column(Text, nullable=True)  # 战争描述
    impact_level = Column(Integer, nullable=True)  # 影响等级 1-10
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def get_duration_days(self):
        """计算战争持续天数"""
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return None
    
    def get_belligerents_list(self):
        """获取参与方列表"""
        side1 = self.belligerents_side1.split('; ') if self.belligerents_side1 else []
        side2 = self.belligerents_side2.split('; ') if self.belligerents_side2 else []
        return {
            'side1': [s.strip() for s in side1 if s.strip()],
            'side2': [s.strip() for s in side2 if s.strip()]
        }

class Technology(Base):
    __tablename__ = "technologies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    invention_date = Column(DateTime, nullable=True)
    inventor = Column(String(100), nullable=True)
    application_domain = Column(String(100), nullable=True)
    military_civilian = Column(String(20), nullable=True)
    patent_number = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    significance_level = Column(Integer, nullable=True)
    
    # 与战争的关联
    related_war_id = Column(Integer, ForeignKey("wars.id"), nullable=True)
    impact_on_warfare = Column(Text, nullable=True)  # 对战争方式的影响
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Finance(Base):
    __tablename__ = "finance_data"
    
    id = Column(Integer, primary_key=True, index=True)
    indicator_name = Column(String(100), nullable=False)
    value = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=True)
    data_type = Column(String(50), nullable=True)
    source = Column(String(100), nullable=True)
    impact_level = Column(Integer, nullable=True)
    
    # 与战争的关联
    related_war_id = Column(Integer, ForeignKey("wars.id"), nullable=True)
    war_finance_type = Column(String(50), nullable=True)  # 战争融资类型: 军费、赔款、贷款等
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    event_date = Column(DateTime, nullable=False)
    event_type = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    related_entities = Column(Text, nullable=True)
    impact_score = Column(Integer, nullable=True)
    
    # 与战争的关联
    related_war_id = Column(Integer, ForeignKey("wars.id"), nullable=True)
    event_role = Column(String(50), nullable=True)  # 事件角色: 导火索、转折点、结束标志等
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class WarParticipant(Base):
    """战争参与方详细表（用于多对多关系）"""
    __tablename__ = "war_participants"
    
    id = Column(Integer, primary_key=True, index=True)
    war_id = Column(Integer, ForeignKey("wars.id"), nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=True)
    participant_name = Column(String(100), nullable=False)  # 参与方名称（用于非国家实体）
    side = Column(Integer, nullable=False)  # 1=第一方, 2=第二方
    is_initiator = Column(Integer, default=0)  # 0=否, 1=是
    entry_date = Column(DateTime, nullable=True)  # 参战日期
    exit_date = Column(DateTime, nullable=True)  # 退出日期
    deaths = Column(Integer, nullable=True, default=0)  # 该方死亡人数
    outcome = Column(String(50), nullable=True)  # 该方结果
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Relation(Base):
    __tablename__ = "relations"
    
    id = Column(Integer, primary_key=True, index=True)
    source_type = Column(String(50), nullable=False)
    source_id = Column(Integer, nullable=False)
    target_type = Column(String(50), nullable=False)
    target_id = Column(Integer, nullable=False)
    relation_type = Column(String(50), nullable=False)
    strength = Column(Integer, nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# COW数据字典（用于参考）
WAR_TYPE_DESCRIPTIONS = {
    1: "Inter-State War (国家间战争) - 两个或多个国际体系成员之间的战争",
    2: "Extra-State War (国家对外战争) - 国际体系成员与非成员之间的战争",
    3: "Extra-State War (国家对外战争) - 殖民战争",
    4: "Intra-State War (国内战争) - 中央政府 vs 内部对立集团",
    5: "Intra-State War (国内战争) - 地方政府 vs 内部对立集团",
    6: "Intra-State War (国内战争) - 非政府团体间的战争",
    7: "Intra-State War (国内战争) - 非政府团体间的战争（不同地区）",
    8: "Non-State War (非国家战争) - 非国际体系成员间的战争"
}

OUTCOME_DESCRIPTIONS = {
    1: "胜利 (Victory) - 一方实现主要战争目标",
    2: "失败 (Defeat) - 一方未能实现主要战争目标",
    3: "妥协 (Compromise) - 双方达成妥协",
    4: "转型 (Transformed) - 战争转型为其他类型",
    5: "继续 (Ongoing) - 战争仍在继续",
    6: "僵局 (Stalemate) - 战争陷入僵局",
    7: "释放 (Released) - 被占领土释放",
    8: "未知 (Unknown) - 结果未知"
}

WHERE_FOUGHT_DESCRIPTIONS = {
    1: "北美 (North America)",
    2: "西欧 (Western Europe)",
    3: "东欧 (Eastern Europe)",
    4: "拉美 (Latin America)",
    5: "撒哈拉以南非洲 (Sub-Saharan Africa)",
    6: "中东/北非 (Middle East/North Africa)",
    7: "亚洲 (Asia)",
    8: "大洋洲 (Oceania)",
    9: "跨地区 (Multi-regional)"
}
