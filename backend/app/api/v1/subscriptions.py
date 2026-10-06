import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user_id
from app.db.session import get_db
from app.schemas.subscription import (
    SubscriptionCreate,
    SubscriptionResponse,
    SubscriptionUpdate,
)
from app.services.subscription import subscription_service

router = APIRouter()


@router.post(
    "",
    response_model=SubscriptionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create subscription",
)
def create_subscription(
    subscription_in: SubscriptionCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
) -> SubscriptionResponse:
    """
    Create a new subscription for the authenticated/development user.
    """
    return subscription_service.create(db=db, obj_in=subscription_in, user_id=user_id)


@router.get(
    "",
    response_model=List[SubscriptionResponse],
    status_code=status.HTTP_200_OK,
    summary="List subscriptions",
)
def list_subscriptions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status_filter: Optional[str] = Query(None, alias="status"),
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
) -> List[SubscriptionResponse]:
    """
    List subscriptions scoped to current user.
    """
    return subscription_service.get_multi(
        db=db,
        user_id=user_id,
        skip=skip,
        limit=limit,
        status=status_filter,
    )


@router.get(
    "/{subscription_id}",
    response_model=SubscriptionResponse,
    status_code=status.HTTP_200_OK,
    summary="Get subscription by ID",
)
def get_subscription(
    subscription_id: uuid.UUID,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
) -> SubscriptionResponse:
    """
    Retrieve single subscription by ID, scoped to user.
    """
    sub = subscription_service.get_by_id(db=db, subscription_id=subscription_id, user_id=user_id)
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subscription '{subscription_id}' not found.",
        )
    return sub


@router.put(
    "/{subscription_id}",
    response_model=SubscriptionResponse,
    status_code=status.HTTP_200_OK,
    summary="Update subscription (PUT)",
)
@router.patch(
    "/{subscription_id}",
    response_model=SubscriptionResponse,
    status_code=status.HTTP_200_OK,
    summary="Update subscription (PATCH)",
)
def update_subscription(
    subscription_id: uuid.UUID,
    subscription_in: SubscriptionUpdate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
) -> SubscriptionResponse:
    """
    Update subscription fields.
    """
    sub = subscription_service.get_by_id(db=db, subscription_id=subscription_id, user_id=user_id)
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subscription '{subscription_id}' not found.",
        )
    return subscription_service.update(db=db, db_obj=sub, obj_in=subscription_in)


@router.delete(
    "/{subscription_id}",
    response_model=SubscriptionResponse,
    status_code=status.HTTP_200_OK,
    summary="Archive subscription",
)
def archive_subscription(
    subscription_id: uuid.UUID,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
) -> SubscriptionResponse:
    """
    Soft-archive subscription by setting status='archived' (Phase 2 rule).
    """
    sub = subscription_service.get_by_id(db=db, subscription_id=subscription_id, user_id=user_id)
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subscription '{subscription_id}' not found.",
        )
    return subscription_service.archive(db=db, db_obj=sub)
