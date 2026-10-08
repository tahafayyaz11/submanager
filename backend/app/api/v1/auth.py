from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.core.security import create_access_token
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import TokenResponse, UserCreate, UserLogin, UserResponse
from app.services.user import user_service

router = APIRouter()


@router.post(
    "/signup",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account",
)
def signup(
    user_in: UserCreate,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """
    Register a new user account with email and password.
    Returns access token and user profile.
    """
    user = user_service.create(db=db, obj_in=user_in)
    access_token = create_access_token(
        subject=user.id,
        extra_claims={
            "email": user.email,
            "name": user.full_name,
        },
    )
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate existing user",
)
def login(
    user_in: UserLogin,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """
    Authenticate an existing user with email and password.
    Returns access token and user profile.
    """
    user = user_service.authenticate(
        db=db,
        email=user_in.email,
        password=user_in.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        subject=user.id,
        extra_claims={
            "email": user.email,
            "name": user.full_name,
        },
    )
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
    )


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current user profile",
)
def get_me(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """
    Retrieve profile details for the currently authenticated user.
    """
    return UserResponse.model_validate(current_user)
