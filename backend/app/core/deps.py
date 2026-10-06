from typing import Optional
from fastapi import Header, HTTPException, status
from app.core.config import settings


def get_current_user_id(x_user_id: Optional[str] = Header(None, alias="X-User-Id")) -> str:
    """
    Temporary development-only user identity resolver.

    Rules:
    1. If an explicit X-User-Id header is provided, use it.
    2. If missing, ONLY in development environment (APP_ENV == 'development'),
       use settings.DEV_USER_ID if configured.
    3. Outside development (or when DEV_USER_ID is unset in development),
       never fall back to a shared user: raise 401 Unauthorized.

    This dependency is isolated here and will be replaced in Phase 3 with JWT token validation
    without changing SubscriptionService or database query logic.
    """
    if x_user_id and x_user_id.strip():
        return x_user_id.strip()

    if settings.APP_ENV == "development" and settings.DEV_USER_ID:
        return settings.DEV_USER_ID.strip()

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required. Provide an 'X-User-Id' header for development.",
    )
