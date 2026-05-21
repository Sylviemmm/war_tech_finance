"""
所有数据模型的导入文件
All Models Import File
"""

# 导入所有模型，确保它们被注册到Base.metadata中
from .country import Country
from .war import War
from .technology import Technology
from .finance import Finance
from .event import Event
from .relation import Relation

# 导出所有模型
__all__ = [
    'Country',
    'War', 
    'Technology',
    'Finance',
    'Event',
    'Relation'
]