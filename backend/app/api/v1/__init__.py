from fastapi import APIRouter
from app.api.v1.analytics import router as analytics_router
from app.api.v1.auth import router as auth_router
from app.api.v1.health import router as health_router
from app.api.v1.subscriptions import router as subscriptions_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(health_router, prefix="/health", tags=["Health"])
api_router.include_router(subscriptions_router, prefix="/subscriptions", tags=["Subscriptions"])
api_router.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])

__all__ = ["api_router"]

