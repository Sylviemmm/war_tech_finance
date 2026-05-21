"""
数据导入工具
Data Import Utilities
"""

import csv
import json
import pandas as pd
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

class DataImportError(Exception):
    """数据导入错误"""
    pass

class DataImporter:
    """数据导入器"""
    
    def __init__(self, db: Session):
        self.db = db
        self.errors = []
        self.success_count = 0
        self.error_count = 0
    
    def import_from_csv(self, file_path: str, model_class, batch_size: int = 1000) -> Dict[str, Any]:
        """从CSV文件导入数据"""
        try:
            # 读取CSV文件
            df = pd.read_csv(file_path)
            
            # 数据验证和清洗
            cleaned_data = self._clean_data(df, model_class)
            
            # 批量插入
            results = self._batch_insert(cleaned_data, model_class, batch_size)
            
            return {
                "success": True,
                "total_records": len(cleaned_data),
                "success_count": results["success_count"],
                "error_count": results["error_count"],
                "errors": results["errors"][:10],  # 只返回前10个错误
                "message": f"成功导入 {results['success_count']} 条记录，失败 {results['error_count']} 条记录"
            }
            
        except Exception as e:
            logger.error(f"CSV导入失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"CSV导入失败: {e}"
            }
    
    def import_from_json(self, file_path: str, model_class) -> Dict[str, Any]:
        """从JSON文件导入数据"""
        try:
            # 读取JSON文件
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 确保数据是列表格式
            if isinstance(data, dict):
                data = [data]
            
            # 数据验证和清洗
            cleaned_data = []
            for item in data:
                try:
                    cleaned_item = self._clean_json_data(item, model_class)
                    cleaned_data.append(cleaned_item)
                except Exception as e:
                    self.error_count += 1
                    self.errors.append(f"数据项清洗失败: {e}")
                    logger.warning(f"数据项清洗失败: {e}")
            
            # 批量插入
            results = self._batch_insert(cleaned_data, model_class)
            
            return {
                "success": True,
                "total_records": len(data),
                "cleaned_records": len(cleaned_data),
                "success_count": results["success_count"],
                "error_count": results["error_count"],
                "errors": results["errors"][:10],
                "message": f"成功导入 {results['success_count']} 条记录，失败 {results['error_count']} 条记录"
            }
            
        except Exception as e:
            logger.error(f"JSON导入失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"JSON导入失败: {e}"
            }
    
    def _clean_data(self, df: pd.DataFrame, model_class) -> List[Dict[str, Any]]:
        """清洗数据"""
        cleaned_data = []
        
        for index, row in df.iterrows():
            try:
                # 转换为字典
                item = row.to_dict()
                
                # 清洗数据
                cleaned_item = self._clean_json_data(item, model_class)
                cleaned_data.append(cleaned_item)
                
            except Exception as e:
                self.error_count += 1
                self.errors.append(f"第 {index + 1} 行数据清洗失败: {e}")
                logger.warning(f"第 {index + 1} 行数据清洗失败: {e}")
        
        return cleaned_data
    
    def _clean_json_data(self, data: Dict[str, Any], model_class) -> Dict[str, Any]:
        """清洗JSON数据"""
        cleaned = {}
        
        # 获取模型字段
        from pydantic import BaseModel
        if hasattr(model_class, 'schema'):
            model_fields = model_class.schema()['properties']
        else:
            # 如果没有schema，使用SQLAlchemy模型字段
            model_fields = {column.name: column.type for column in model_class.__table__.columns}
        
        for field, value in data.items():
            if field in model_fields:
                # 处理空值
                if pd.isna(value) or value is None or value == '':
                    continue
                
                # 类型转换
                try:
                    if isinstance(value, str):
                        # 尝试转换为日期
                        try:
                            value = datetime.fromisoformat(value.replace('Z', '+00:00'))
                        except:
                            # 保持字符串
                            pass
                    
                    cleaned[field] = value
                    
                except Exception as e:
                    logger.warning(f"字段 {field} 类型转换失败: {e}")
                    continue
        
        return cleaned
    
    def _batch_insert(self, data: List[Dict[str, Any]], model_class, batch_size: int = 1000) -> Dict[str, Any]:
        """批量插入数据"""
        success_count = 0
        error_count = 0
        batch_errors = []
        
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            
            try:
                # 创建模型实例
                instances = []
                for item in batch:
                    try:
                        instance = model_class(**item)
                        instances.append(instance)
                    except Exception as e:
                        error_count += 1
                        batch_errors.append(f"数据创建失败: {e}")
                        logger.warning(f"数据创建失败: {e}")
                
                # 批量保存
                if instances:
                    self.db.bulk_save_objects(instances)
                    self.db.commit()
                    success_count += len(instances)
                
            except Exception as e:
                self.db.rollback()
                error_count += len(batch)
                batch_errors.append(f"批量插入失败: {e}")
                logger.error(f"批量插入失败: {e}")
        
        return {
            "success_count": success_count,
            "error_count": error_count,
            "errors": batch_errors
        }
    
    def get_import_report(self) -> Dict[str, Any]:
        """获取导入报告"""
        return {
            "success_count": self.success_count,
            "error_count": self.error_count,
            "total_errors": len(self.errors),
            "errors": self.errors[:20]  # 返回前20个错误
        }

def validate_war_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """验证战争数据"""
    validated = {}
    
    # 必填字段
    required_fields = ['name', 'start_date']
    for field in required_fields:
        if field not in data or not data[field]:
            raise DataImportError(f"必填字段 {field} 不能为空")
    
    # 日期格式验证
    if 'start_date' in data:
        try:
            if isinstance(data['start_date'], str):
                validated['start_date'] = datetime.fromisoformat(data['start_date'])
            else:
                validated['start_date'] = data['start_date']
        except Exception as e:
            raise DataImportError(f"开始日期格式错误: {e}")
    
    if 'end_date' in data and data['end_date']:
        try:
            if isinstance(data['end_date'], str):
                validated['end_date'] = datetime.fromisoformat(data['end_date'])
            else:
                validated['end_date'] = data['end_date']
        except Exception as e:
            raise DataImportError(f"结束日期格式错误: {e}")
    
    # 计算持续时间
    if 'start_date' in validated and 'end_date' in validated:
        duration = (validated['end_date'] - validated['start_date']).days
        validated['duration_days'] = duration
    
    # 数值字段验证
    numeric_fields = ['casualties', 'impact_level']
    for field in numeric_fields:
        if field in data and data[field]:
            try:
                validated[field] = int(data[field])
                if field == 'impact_level' and (validated[field] < 1 or validated[field] > 10):
                    raise DataImportError(f"影响程度必须在1-10之间")
            except ValueError:
                raise DataImportError(f"字段 {field} 必须是整数")
    
    # JSON字段处理
    json_fields = ['belligerents', 'geographic_scope']
    for field in json_fields:
        if field in data and data[field]:
            if isinstance(data[field], str):
                try:
                    validated[field] = json.loads(data[field])
                except json.JSONDecodeError:
                    validated[field] = data[field]
            else:
                validated[field] = data[field]
    
    return validated

def validate_country_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """验证国家数据"""
    validated = {}
    
    # 必填字段
    required_fields = ['name', 'iso_code']
    for field in required_fields:
        if field not in data or not data[field]:
            raise DataImportError(f"必填字段 {field} 不能为空")
    
    # ISO代码格式验证
    if 'iso_code' in data:
        validated['iso_code'] = data['iso_code'].upper()
    
    # 数值字段验证
    numeric_fields = ['gdp', 'military_spending', 'population', 'latitude', 'longitude']
    for field in numeric_fields:
        if field in data and data[field]:
            try:
                validated[field] = float(data[field])
                
                # 经纬度范围验证
                if field == 'latitude' and (validated[field] < -90 or validated[field] > 90):
                    raise DataImportError(f"纬度必须在-90到90之间")
                if field == 'longitude' and (validated[field] < -180 or validated[field] > 180):
                    raise DataImportError(f"经度必须在-180到180之间")
                    
            except ValueError:
                raise DataImportError(f"字段 {field} 必须是数字")
    
    return validated