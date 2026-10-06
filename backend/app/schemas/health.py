from pydantic import BaseModel
from typing import Optional


class HealthResponse(BaseModel):
    """Simple health response model"""
    status: str = "ok"


class DetailedHealthResponse(BaseModel):
    """Detailed health check response with database status"""
    status: str = "ok"
    app_name: str
    environment: str
    database: str
    database_connected: bool
    version: str
