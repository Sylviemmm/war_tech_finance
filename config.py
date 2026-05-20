"""
配置文件
Configuration Settings
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """应用配置类"""
    
    # 基础配置
    app_name: str = "战争技术金融可视化分析平台"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # 数据库配置
    database_url: str = "sqlite:///./war_tech_finance.db"
    database_echo: bool = False  # 是否输出SQL日志
    
    # 服务器配置
    host: str = "0.0.0.0"
    port: int = 8000
    
    # 分页配置
    default_page_size: int = 50
    max_page_size: int = 1000
    
    # 文件上传配置
    max_file_size: int = 100 * 1024 * 1024  # 100MB
    upload_dir: str = "uploads"
    
    # 数据验证配置
    strict_validation: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# 创建全局配置实例
settings = Settings()

# 确保上传目录存在
os.makedirs(settings.upload_dir, exist_ok=True)