"""
基础CRUD操作
Base CRUD Operations
"""

from typing import Type, TypeVar, Generic, List, Optional, Dict, Any, Union
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime

# 泛型类型变量
ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """基础CRUD操作类"""
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def get(self, db: Session, id: int) -> Optional[ModelType]:
        """根据ID获取单个记录"""
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_multi(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        order_desc: bool = False
    ) -> List[ModelType]:
        """获取多个记录"""
        query = db.query(self.model)
        
        # 应用过滤条件
        if filters:
            for key, value in filters.items():
                if value is not None:
                    if key.endswith("__gt"):
                        field = key[:-4]
                        query = query.filter(getattr(self.model, field) > value)
                    elif key.endswith("__lt"):
                        field = key[:-4]
                        query = query.filter(getattr(self.model, field) < value)
                    elif key.endswith("__gte"):
                        field = key[:-5]
                        query = query.filter(getattr(self.model, field) >= value)
                    elif key.endswith("__lte"):
                        field = key[:-5]
                        query = query.filter(getattr(self.model, field) <= value)
                    elif key.endswith("__in"):
                        field = key[:-4]
                        query = query.filter(getattr(self.model, field).in_(value))
                    elif key.endswith("__like"):
                        field = key[:-6]
                        query = query.filter(getattr(self.model, field).like(f"%{value}%"))
                    else:
                        query = query.filter(getattr(self.model, key) == value)
        
        # 应用排序
        if order_by:
            order_field = getattr(self.model, order_by)
            if order_desc:
                query = query.order_by(order_field.desc())
            else:
                query = query.order_by(order_field)
        
        # 应用分页
        return query.offset(skip).limit(limit).all()
    
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """创建记录"""
        obj_data = obj_in.dict()
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self, 
        db: Session, 
        *, 
        db_obj: ModelType, 
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """更新记录"""
        obj_data = obj_in if isinstance(obj_in, dict) else obj_in.dict()
        
        for field, value in obj_data.items():
            if value is not None:
                setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def remove(self, db: Session, *, id: int) -> ModelType:
        """删除记录"""
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
    
    def count(self, db: Session, filters: Optional[Dict[str, Any]] = None) -> int:
        """计算记录数量"""
        query = db.query(self.model)
        if filters:
            for key, value in filters.items():
                if value is not None:
                    query = query.filter(getattr(self.model, key) == value)
        return query.count()
    
    def exists(self, db: Session, id: int) -> bool:
        """检查记录是否存在"""
        return db.query(self.model).filter(self.model.id == id).first() is not None