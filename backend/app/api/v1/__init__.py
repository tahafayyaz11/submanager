from fastapi import APIRouter
from app.api.v1.health import router as health_router
from app.api.v1.subscriptions import router as subscriptions_router

api_router = APIRouter()
api_router.include_router(health_router, prefix="/health", tags=["Health"])
api_router.include_router(subscriptions_router, prefix="/subscriptions", tags=["Subscriptions"])

__all__ = ["api_router"]
