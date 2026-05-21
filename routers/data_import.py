"""
数据导入API路由
Data Import API Routes
"""

from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from models.country import Country
from models.war import War
from models.technology import Technology
from models.finance import Finance
from models.event import Event
from models.relation import Relation
from schemas.country import CountryCreate
from schemas.war import WarCreate
from schemas.technology import TechnologyCreate
from schemas.finance import FinanceCreate
from schemas.event import EventCreate
from schemas.relation import RelationCreate
from utils.data_import import DataImporter, validate_country_data, validate_war_data, DataImportError

router = APIRouter(prefix="/api/v1/import", tags=["import"])

@router.post("/countries")
async def import_countries(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """导入国家数据"""
    if not file.filename.endswith(('.csv', '.json')):
        raise HTTPException(status_code=400, detail="只支持CSV和JSON文件格式")
    
    try:
        # 保存上传的文件
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # 创建导入器
        importer = DataImporter(db)
        
        # 根据文件类型导入
        if file.filename.endswith('.csv'):
            result = importer.import_from_csv(file_path, Country)
        else:
            result = importer.import_from_json(file_path, Country)
        
        # 清理临时文件
        import os
        os.remove(file_path)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
        
        return {
            "success": True,
            "message": result["message"],
            "details": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导入失败: {str(e)}")

@router.post("/wars")
async def import_wars(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """导入战争数据"""
    if not file.filename.endswith(('.csv', '.json')):
        raise HTTPException(status_code=400, detail="只支持CSV和JSON文件格式")
    
    try:
        # 保存上传的文件
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # 创建导入器
        importer = DataImporter(db)
        
        # 根据文件类型导入
        if file.filename.endswith('.csv'):
            result = importer.import_from_csv(file_path, War)
        else:
            result = importer.import_from_json(file_path, War)
        
        # 清理临时文件
        import os
        os.remove(file_path)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
        
        return {
            "success": True,
            "message": result["message"],
            "details": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导入失败: {str(e)}")

@router.post("/technologies")
async def import_technologies(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """导入技术数据"""
    if not file.filename.endswith(('.csv', '.json')):
        raise HTTPException(status_code=400, detail="只支持CSV和JSON文件格式")
    
    try:
        # 保存上传的文件
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # 创建导入器
        importer = DataImporter(db)
        
        # 根据文件类型导入
        if file.filename.endswith('.csv'):
            result = importer.import_from_csv(file_path, Technology)
        else:
            result = importer.import_from_json(file_path, Technology)
        
        # 清理临时文件
        import os
        os.remove(file_path)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
        
        return {
            "success": True,
            "message": result["message"],
            "details": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导入失败: {str(e)}")

@router.post("/finance")
async def import_finance(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """导入金融数据"""
    if not file.filename.endswith(('.csv', '.json')):
        raise HTTPException(status_code=400, detail="只支持CSV和JSON文件格式")
    
    try:
        # 保存上传的文件
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # 创建导入器
        importer = DataImporter(db)
        
        # 根据文件类型导入
        if file.filename.endswith('.csv'):
            result = importer.import_from_csv(file_path, Finance)
        else:
            result = importer.import_from_json(file_path, Finance)
        
        # 清理临时文件
        import os
        os.remove(file_path)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
        
        return {
            "success": True,
            "message": result["message"],
            "details": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导入失败: {str(e)}")

@router.post("/events")
async def import_events(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """导入事件数据"""
    if not file.filename.endswith(('.csv', '.json')):
        raise HTTPException(status_code=400, detail="只支持CSV和JSON文件格式")
    
    try:
        # 保存上传的文件
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # 创建导入器
        importer = DataImporter(db)
        
        # 根据文件类型导入
        if file.filename.endswith('.csv'):
            result = importer.import_from_csv(file_path, Event)
        else:
            result = importer.import_from_json(file_path, Event)
        
        # 清理临时文件
        import os
        os.remove(file_path)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
        
        return {
            "success": True,
            "message": result["message"],
            "details": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导入失败: {str(e)}")

@router.post("/relations")
async def import_relations(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """导入关系数据"""
    if not file.filename.endswith(('.csv', '.json')):
        raise HTTPException(status_code=400, detail="只支持CSV和JSON文件格式")
    
    try:
        # 保存上传的文件
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # 创建导入器
        importer = DataImporter(db)
        
        # 根据文件类型导入
        if file.filename.endswith('.csv'):
            result = importer.import_from_csv(file_path, Relation)
        else:
            result = importer.import_from_json(file_path, Relation)
        
        # 清理临时文件
        import os
        os.remove(file_path)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
        
        return {
            "success": True,
            "message": result["message"],
            "details": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导入失败: {str(e)}")

@router.get("/template/{entity_type}")
async def get_import_template(entity_type: str):
    """获取数据导入模板"""
    templates = {
        "country": {
            "name": "国家",
            "fields": [
                {"name": "name", "type": "string", "required": True, "description": "国家名称"},
                {"name": "iso_code", "type": "string", "required": True, "description": "ISO国家代码"},
                {"name": "iso3_code", "type": "string", "required": False, "description": "ISO3国家代码"},
                {"name": "continent", "type": "string", "required": False, "description": "大洲"},
                {"name": "region", "type": "string", "required": False, "description": "地区"},
                {"name": "political_system", "type": "string", "required": False, "description": "政治体制"},
                {"name": "gdp", "type": "number", "required": False, "description": "GDP"},
                {"name": "military_spending", "type": "number", "required": False, "description": "军费开支"},
                {"name": "population", "type": "integer", "required": False, "description": "人口数量"},
                {"name": "latitude", "type": "number", "required": False, "description": "纬度"},
                {"name": "longitude", "type": "number", "required": False, "description": "经度"}
            ],
            "sample_data": [
                {
                    "name": "中国",
                    "iso_code": "CN",
                    "iso3_code": "CHN",
                    "continent": "亚洲",
                    "region": "东亚",
                    "political_system": "社会主义",
                    "gdp": 17734130000000.0,
                    "military_spending": 209200000000.0,
                    "population": 1412000000,
                    "latitude": 35.8617,
                    "longitude": 104.1954
                }
            ]
        },
        "war": {
            "name": "战争",
            "fields": [
                {"name": "name", "type": "string", "required": True, "description": "战争名称"},
                {"name": "start_date", "type": "date", "required": True, "description": "开始日期"},
                {"name": "end_date", "type": "date", "required": False, "description": "结束日期"},
                {"name": "belligerents", "type": "json", "required": False, "description": "参战方"},
                {"name": "casualties", "type": "integer", "required": False, "description": "伤亡人数"},
                {"name": "geographic_scope", "type": "json", "required": False, "description": "地理范围"},
                {"name": "war_type", "type": "string", "required": False, "description": "战争类型"},
                {"name": "casus_belli", "type": "string", "required": False, "description": "战争原因"},
                {"name": "impact_level", "type": "integer", "required": False, "description": "影响程度"}
            ],
            "sample_data": [
                {
                    "name": "第一次世界大战",
                    "start_date": "1914-07-28",
                    "end_date": "1918-11-11",
                    "belligerents": {"allies": ["英国", "法国", "俄国"], "central_powers": ["德国", "奥匈帝国"]},
                    "casualties": 17000000,
                    "geographic_scope": {"continents": ["欧洲", "亚洲", "非洲", "美洲"], "countries": ["英国", "法国", "德国", "奥匈帝国"]},
                    "war_type": "international",
                    "casus_belli": "萨拉热窝事件",
                    "impact_level": 10
                }
            ]
        }
    }
    
    if entity_type not in templates:
        raise HTTPException(status_code=404, detail="不支持的实体类型")
    
    return templates[entity_type]