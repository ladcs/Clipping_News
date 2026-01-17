from fastapi import APIRouter

from api.v1.routers.news_router import router as news_router
from api.v1.routers.news_source_router import router as news_source_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(news_router, prefix="/news", tags=["news"])
api_router.include_router(news_source_router, prefix="/sources", tags=["news sources"])
