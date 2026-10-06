from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import __version__
from app.core.config import settings
from app.db.session import get_db
from app.schemas.health import DetailedHealthResponse, HealthResponse
from app.services.health import check_database_health

router = APIRouter()


@router.get("", response_model=HealthResponse, summary="Basic health check")
def health_check() -> HealthResponse:
    """
    Returns simple status ok response.
    """
    return HealthResponse(status="ok")


@router.get("/detailed", response_model=DetailedHealthResponse, summary="Detailed health check")
def detailed_health_check(db: Session = Depends(get_db)) -> DetailedHealthResponse:
    """
    Returns detailed health check including PostgreSQL connectivity.
    """
    is_connected, msg = check_database_health(db)
    return DetailedHealthResponse(
        status="ok",
        app_name=settings.APP_NAME,
        environment=settings.APP_ENV,
        database=msg,
        database_connected=is_connected,
        version=__version__,
    )
