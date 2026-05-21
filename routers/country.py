"""
国家API路由
Country API Routes
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from models.country import Country
from schemas.country import CountryCreate, CountryUpdate, Country, CountryList, CountryFilter
from crud.country import country

router = APIRouter(prefix="/api/v1/countries", tags=["countries"])

@router.get("/", response_model=CountryList)
async def get_countries(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(50, ge=1, le=1000, description="返回的记录数"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    continent: Optional[str] = Query(None, description="大洲"),
    region: Optional[str] = Query(None, description="地区"),
    min_population: Optional[int] = Query(None, ge=0, description="最小人口"),
    max_population: Optional[int] = Query(None, ge=0, description="最大人口"),
    min_gdp: Optional[float] = Query(None, ge=0, description="最小GDP"),
    max_gdp: Optional[float] = Query(None, ge=0, description="最大GDP"),
    order_by: str = Query("name", description="排序字段"),
    order_desc: bool = Query(False, description="是否降序")
):
    """获取国家列表"""
    countries = country.search_countries(
        db=db,
        skip=skip,
        limit=limit,
        search=search,
        continent=continent,
        region=region,
        min_population=min_population,
        max_population=max_population,
        min_gdp=min_gdp,
        max_gdp=max_gdp,
        order_by=order_by,
        order_desc=order_desc
    )
    
    total = country.count(db, filters={
        "continent": continent,
        "region": region
    })
    
    return CountryList(
        countries=countries,
        total=total,
        page=skip // limit + 1,
        page_size=limit
    )

@router.get("/{country_id}", response_model=Country)
async def get_country(country_id: int, db: Session = Depends(get_db)):
    """获取国家详情"""
    db_country = country.get(db, country_id=country_id)
    if not db_country:
        raise HTTPException(status_code=404, detail="国家未找到")
    return db_country

@router.post("/", response_model=Country)
async def create_country(country_data: CountryCreate, db: Session = Depends(get_db)):
    """创建国家"""
    # 检查ISO代码是否已存在
    if country.get_by_iso_code(db, country_data.iso_code):
        raise HTTPException(status_code=400, detail="ISO代码已存在")
    
    return country.create(db=db, obj_in=country_data)

@router.put("/{country_id}", response_model=Country)
async def update_country(
    country_id: int, 
    country_data: CountryUpdate, 
    db: Session = Depends(get_db)
):
    """更新国家"""
    db_country = country.get(db, country_id=country_id)
    if not db_country:
        raise HTTPException(status_code=404, detail="国家未找到")
    
    # 检查ISO代码是否与其他国家冲突
    if country_data.iso_code and country_data.iso_code != db_country.iso_code:
        if country.get_by_iso_code(db, country_data.iso_code):
            raise HTTPException(status_code=400, detail="ISO代码已存在")
    
    return country.update(db=db, db_obj=db_country, obj_in=country_data)

@router.delete("/{country_id}")
async def delete_country(country_id: int, db: Session = Depends(get_db)):
    """删除国家"""
    db_country = country.get(db, country_id=country_id)
    if not db_country:
        raise HTTPException(status_code=404, detail="国家未找到")
    
    country.remove(db=db, id=country_id)
    return {"message": "国家删除成功"}

@router.get("/search/{search_term}", response_model=List[Country])
async def search_countries_by_term(
    search_term: str,
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100, description="返回的记录数")
):
    """搜索国家"""
    countries = country.search_countries(
        db=db,
        skip=0,
        limit=limit,
        search=search_term
    )
    return countries

@router.get("/continent/{continent}", response_model=List[Country])
async def get_countries_by_continent(
    continent: str,
    db: Session = Depends(get_db),
    limit: int = Query(100, ge=1, le=1000, description="返回的记录数")
):
    """根据大洲获取国家"""
    countries = country.get_countries_by_continent(db, continent)
    return countries[:limit]

@router.get("/region/{region}", response_model=List[Country])
async def get_countries_by_region(
    region: str,
    db: Session = Depends(get_db),
    limit: int = Query(100, ge=1, le=1000, description="返回的记录数")
):
    """根据地区获取国家"""
    countries = country.get_countries_by_region(db, region)
    return countries[:limit]

@router.get("/top/population", response_model=List[Country])
async def get_top_countries_by_population(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100, description="返回的记录数")
):
    """获取人口最多的国家"""
    countries = country.get_top_countries_by_population(db, limit)
    return countries

@router.get("/top/gdp", response_model=List[Country])
async def get_top_countries_by_gdp(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100, description="返回的记录数")
):
    """获取GDP最高的国家"""
    countries = country.get_top_countries_by_gdp(db, limit)
    return countries