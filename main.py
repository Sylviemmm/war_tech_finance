"""
战争技术金融可视化分析平台 - API服务
War-Tech-Fin Visualization Analysis Platform - API Service
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from datetime import datetime

# 导入路由
from routers import country, war
from routers import data_import as data_import_router

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="战争技术金融可视化分析平台 API",
    description="基于产品文档的战争-技术-金融同构逻辑研究API接口",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含路由
app.include_router(country.router)
app.include_router(war.router)
app.include_router(data_import_router.router)

@app.get("/")
async def root():
    """API根路径"""
    return {
        "message": "战争技术金融可视化分析平台 API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "docs": "/docs",
        "endpoints": {
            "countries": "/api/v1/countries",
            "wars": "/api/v1/wars"
        }
    }

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "war-tech-fin-api"
    }

@app.get("/api/v1/info")
async def api_info():
    """API信息接口"""
    return {
        "name": "战争技术金融可视化分析平台 API",
        "version": "1.0.0",
        "description": "基于产品文档的战争-技术-金融同构逻辑研究API接口",
        "endpoints": {
            "countries": {
                "base": "/api/v1/countries",
                "operations": ["GET", "POST", "PUT", "DELETE"],
                "features": ["search", "filter", "pagination", "sorting"]
            },
            "wars": {
                "base": "/api/v1/wars", 
                "operations": ["GET", "POST", "PUT", "DELETE"],
                "features": ["search", "filter", "pagination", "sorting", "statistics"]
            }
        },
        "docs": {
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )