import logging
from sqlalchemy import text
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def check_database_health(db: Session) -> tuple[bool, str]:
    """
    Checks PostgreSQL connectivity with a ping query.
    Returns (is_connected: bool, message: str).
    """
    try:
        # Simple test query
        db.execute(text("SELECT 1"))
        return True, "connected"
    except Exception as exc:
        logger.warning(f"Database health check failed: {exc}")
        return False, f"disconnected: {str(exc)}"
