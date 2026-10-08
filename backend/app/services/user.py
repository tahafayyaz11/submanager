import uuid
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate


class UserService:
    @staticmethod
    def get_by_id(db: Session, user_id: str) -> Optional[User]:
        """Fetch user by primary key ID."""
        statement = select(User).where(User.id == user_id)
        return db.scalars(statement).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        """Fetch user by lowercase email."""
        clean_email = email.strip().lower()
        statement = select(User).where(User.email == clean_email)
        return db.scalars(statement).first()

    @staticmethod
    def create(db: Session, obj_in: UserCreate) -> User:
        """
        Create a new user with bcrypt password hashing.
        Validates email uniqueness.
        """
        clean_email = obj_in.email.strip().lower()
        existing = UserService.get_by_email(db, clean_email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An account with this email already exists.",
            )

        hashed = hash_password(obj_in.password)
        db_user = User(
            id=str(uuid.uuid4()),
            email=clean_email,
            hashed_password=hashed,
            full_name=obj_in.full_name,
            is_active=True,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def authenticate(db: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user by email and password.
        Returns the User instance if valid, or None.
        """
        clean_email = email.strip().lower()
        user = UserService.get_by_email(db, clean_email)
        if not user:
            return None
        if not user.hashed_password:
            # User might be registered through OAuth/Clerk without a local password
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def get_or_create_external_user(
        db: Session,
        user_id: str,
        email: str,
        full_name: Optional[str] = None,
    ) -> User:
        """
        Ensure an external user (e.g., Clerk OAuth or SSO) is represented in Postgres.
        """
        user = UserService.get_by_id(db, user_id)
        if user:
            return user

        clean_email = email.strip().lower()
        user_by_email = UserService.get_by_email(db, clean_email)
        if user_by_email:
            return user_by_email

        new_user = User(
            id=user_id,
            email=clean_email,
            hashed_password=None,
            full_name=full_name,
            is_active=True,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user


user_service = UserService()
