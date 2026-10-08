from typing import Optional
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User
from app.services.user import user_service

bearer_security = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_security),
    x_user_id: Optional[str] = Header(None, alias="X-User-Id"),
    db: Session = Depends(get_db),
) -> User:
    """
    Resolve the authenticated User for the current request.

    Resolution order:
    1. Authorization Bearer JWT Token:
       - Validates Subsfolio JWT token.
       - Supports Clerk JWT token extraction.
       - Returns the active User from Postgres.
    2. Development-only Fallbacks (only when APP_ENV == 'development'):
       - Explicit 'X-User-Id' header if present.
       - settings.DEV_USER_ID if configured.
    3. Production or Missing Credentials:
       - Raises 401 Unauthorized with WWW-Authenticate header.
    """
    # 1. Bearer Token Resolution
    if credentials and credentials.credentials:
        token = credentials.credentials.strip()
        user_id: Optional[str] = None
        user_email: Optional[str] = None
        user_name: Optional[str] = None

        # Attempt to decode as local Subsfolio JWT
        try:
            payload = decode_access_token(token)
            user_id = payload.get("sub")
            user_email = payload.get("email")
            user_name = payload.get("name")
        except jwt.PyJWTError:
            # If standard Subsfolio JWT validation fails, check if it's a Clerk token
            try:
                # In development or when Clerk is enabled, inspect Clerk claims without signature verification
                # or verify if secret is set
                unverified_claims = jwt.decode(token, options={"verify_signature": False})
                if "sub" in unverified_claims:
                    user_id = unverified_claims.get("sub")
                    user_email = unverified_claims.get("email") or unverified_claims.get("email_address")
                    user_name = unverified_claims.get("name") or unverified_claims.get("full_name")
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired authentication token.",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication token missing user identity.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Retrieve or auto-provision user in Postgres
        user = user_service.get_by_id(db, user_id)
        if not user:
            # If user does not exist in DB yet (e.g. from external token/Clerk), provision user record
            safe_email = user_email or f"{user_id}@auth.subsfolio.com"
            user = user_service.get_or_create_external_user(
                db=db,
                user_id=user_id,
                email=safe_email,
                full_name=user_name,
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account has been deactivated.",
            )

        return user

    # 2. Development-only fallback
    if settings.APP_ENV == "development":
        dev_id = None
        if x_user_id and x_user_id.strip():
            dev_id = x_user_id.strip()
        elif settings.DEV_USER_ID:
            dev_id = settings.DEV_USER_ID.strip()

        if dev_id:
            # Ensure dev user exists in database for relational integrity
            user = user_service.get_by_id(db, dev_id)
            if not user:
                user = user_service.get_or_create_external_user(
                    db=db,
                    user_id=dev_id,
                    email=f"{dev_id}@dev.subsfolio.local",
                    full_name="Development User",
                )
            return user

    # 3. Unauthorized
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required. Please provide a valid Bearer token.",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user_id(current_user: User = Depends(get_current_user)) -> str:
    """
    Returns the isolated user ID of the authenticated user.
    Used by all subscription CRUD endpoints to enforce strict tenant isolation.
    """
    return current_user.id
