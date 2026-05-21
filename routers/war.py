"""
战争API路由
War API Routes
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from models.war import War
from schemas.war import WarCreate, WarUpdate, War, WarList, WarFilter, WarStats
from crud.war import war

router = APIRouter(prefix="/api/v1/wars", tags=["wars"])

@router.get("/", response_model=WarList)
async def get_wars(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(50, ge=1, le=1000, description="返回的记录数"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    start_date_from: Optional[datetime] = Query(None, description="开始日期从"),
    start_date_to: Optional[datetime] = Query(None, description="开始日期到"),
    end_date_from: Optional[datetime] = Query(None, description="结束日期从"),
    end_date_to: Optional[datetime] = Query(None, description="结束日期到"),
    war_type: Optional[str] = Query(None, description="战争类型"),
    min_casualties: Optional[int] = Query(None, ge=0, description="最小伤亡人数"),
    max_casualties: Optional[int] = Query(None, ge=0, description="最大伤亡人数"),
    min_impact_level: Optional[int] = Query(None, ge=1, le=10, description="最小影响程度"),
    max_impact_level: Optional[int] = Query(None, ge=1, le=10, description="最大影响程度"),
    order_by: str = Query("start_date", description="排序字段"),
    order_desc: bool = Query(False, description="是否降序")
):
    """获取战争列表"""
    wars = war.search_wars(
        db=db,
        skip=skip,
        limit=limit,
        search=search,
        start_date_from=start_date_from,
        start_date_to=start_date_to,
        end_date_from=end_date_from,
        end_date_to=end_date_to,
        war_type=war_type,
        min_casualties=min_casualties,
        max_casualties=max_casualties,
        min_impact_level=min_impact_level,
        max_impact_level=max_impact_level,
        order_by=order_by,
        order_desc=order_desc
    )
    
    total = war.count(db)
    
    return WarList(
        wars=wars,
        total=total,
        page=skip // limit + 1,
        page_size=limit
    )

@router.get("/{war_id}", response_model=War)
async def get_war(war_id: int, db: Session = Depends(get_db)):
    """获取战争详情"""
    db_war = war.get(db, war_id=war_id)
    if not db_war:
        raise HTTPException(status_code=404, detail="战争未找到")
    return db_war

@router.post("/", response_model=War)
async def create_war(war_data: WarCreate, db: Session = Depends(get_db)):
    """创建战争"""
    # 计算持续时间
    if war_data.end_date and war_data.start_date:
        duration = (war_data.end_date - war_data.start_date).days
        war_data_dict = war_data.dict()
        war_data_dict["duration_days"] = duration
    else:
        war_data_dict = war_data.dict()
    
    return war.create(db=db, obj_in=war_data_dict)

@router.put("/{war_id}", response_model=War)
async def update_war(
    war_id: int, 
    war_data: WarUpdate, 
    db: Session = Depends(get_db)
):
    """更新战争"""
    db_war = war.get(db, war_id=war_id)
    if not db_war:
        raise HTTPException(status_code=404, detail="战争未找到")
    
    # 重新计算持续时间
    if war_data.end_date and war_data.start_date:
        duration = (war_data.end_date - war_data.start_date).days
        war_data_dict = war_data.dict()
        war_data_dict["duration_days"] = duration
    else:
        war_data_dict = war_data.dict()
    
    return war.update(db=db, db_obj=db_war, obj_in=war_data_dict)

@router.delete("/{war_id}")
async def delete_war(war_id: int, db: Session = Depends(get_db)):
    """删除战争"""
    db_war = war.get(db, war_id=war_id)
    if not db_war:
        raise HTTPException(status_code=404, detail="战争未找到")
    
    war.remove(db=db, id=war_id)
    return {"message": "战争删除成功"}

@router.get("/stats/summary", response_model=WarStats)
async def get_war_stats(db: Session = Depends(get_db)):
    """获取战争统计信息"""
    return war.get_wars_stats(db)

@router.get("/type/{war_type}", response_model=List[War])
async def get_wars_by_type(
    war_type: str,
    db: Session = Depends(get_db),
    limit: int = Query(100, ge=1, le=1000, description="返回的记录数")
):
    """根据类型获取战争"""
    wars = war.get_wars_by_type(db, war_type)
    return wars[:limit]

@router.get("/date-range/{start_date}/{end_date}", response_model=List[War])
async def get_wars_by_date_range(
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db),
    limit: int = Query(100, ge=1, le=1000, description="返回的记录数")
):
    """根据日期范围获取战争"""
    try:
        start_date_obj = datetime.fromisoformat(start_date)
        end_date_obj = datetime.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="日期格式不正确")
    
    wars = war.get_wars_by_date_range(db, start_date_obj, end_date_obj)
    return wars[:limit]

@router.get("/longest", response_model=List[War])
async def get_longest_wars(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100, description="返回的记录数")
):
    """获取持续时间最长的战争"""
    wars = war.get_longest_wars(db, limit)
    return wars

@router.get("/deadliest", response_model=List[War])
async def get_deadliest_wars(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100, description="返回的记录数")
):
    """获取伤亡人数最多的战争"""
    wars = war.get_deadliest_wars(db, limit)
    return wars

@router.get("/century/{century}", response_model=List[War])
async def get_wars_by_century(
    century: int,
    db: Session = Depends(get_db),
    limit: int = Query(100, ge=1, le=1000, description="返回的记录数")
):
    """根据世纪获取战争"""
    wars = war.get_wars_by_century(db, century)
    return wars[:limit]

@router.get("/detailed", response_model=List[dict])
async def get_detailed_war_data(
    db: Session = Depends(get_db),
    war_type: Optional[str] = Query(None, description="战争类型筛选"),
    min_deaths: Optional[int] = Query(0, ge=0, description="最小伤亡数"),
    min_year: Optional[int] = Query(1800, ge=1800, le=2023, description="最小年份"),
    limit: int = Query(1000, ge=1, le=5000, description="返回的记录数")
):
    """获取详细的战争数据用于可视化"""
    wars = war.get_detailed_war_data(
        db=db,
        war_type=war_type,
        min_deaths=min_deaths,
        min_year=min_year,
        limit=limit
    )
    return wars