from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.api.v1 import api_router
from app.core.config import settings
from app.schemas.health import HealthResponse


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager for application startup and shutdown"""
    # Startup actions (if any)
    yield
    # Shutdown actions (if any)


app = FastAPI(
    title=settings.APP_NAME,
    version=__version__,
    description="Subsfolio API — AI-Powered Subscription Intelligence Platform",
    lifespan=lifespan,
)

# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else [settings.CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root Health Check required by Phase 1 specification
@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_endpoint() -> HealthResponse:
    """
    Root health check endpoint.
    Returns: {"status": "ok"}
    """
    return HealthResponse(status="ok")


# Include API v1 Router
app.include_router(api_router, prefix="/api/v1")

# Also mount /subscriptions, /auth, and /analytics at root for convenient API access
from app.api.v1.subscriptions import router as subscriptions_router
from app.api.v1.auth import router as auth_router
from app.api.v1.analytics import router as analytics_router

app.include_router(subscriptions_router, prefix="/subscriptions", tags=["Subscriptions (Root Alias)"])
app.include_router(auth_router, prefix="/auth", tags=["Auth (Root Alias)"])
app.include_router(analytics_router, prefix="/analytics", tags=["Analytics (Root Alias)"])



@app.get("/", tags=["Root"])
def root_info() -> dict:
    """
    Root discovery endpoint.
    """
    return {
        "app": settings.APP_NAME,
        "version": __version__,
        "environment": settings.APP_ENV,
        "health_check": "/health",
        "docs_url": "/docs",
    }
