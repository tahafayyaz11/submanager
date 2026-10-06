import uuid
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.subscription import Subscription
from app.schemas.subscription import SubscriptionCreate, SubscriptionUpdate


class SubscriptionService:
    @staticmethod
    def create(db: Session, obj_in: SubscriptionCreate, user_id: str) -> Subscription:
        """Create a new subscription record scoped to the user"""
        db_obj = Subscription(
            user_id=user_id,
            service_name=obj_in.service_name,
            plan_name=obj_in.plan_name,
            price=obj_in.price,
            currency=obj_in.currency,
            billing_cycle=obj_in.billing_cycle,
            purchase_date=obj_in.purchase_date,
            renewal_date=obj_in.renewal_date,
            category=obj_in.category,
            payment_method=obj_in.payment_method,
            reminder_days_before=obj_in.reminder_days_before,
            notes=obj_in.notes,
            status=obj_in.status,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def get_by_id(db: Session, subscription_id: uuid.UUID, user_id: str) -> Optional[Subscription]:
        """Retrieve a single subscription strictly scoped to the user"""
        statement = select(Subscription).where(
            Subscription.id == subscription_id,
            Subscription.user_id == user_id,
        )
        return db.scalars(statement).first()

    @staticmethod
    def get_multi(
        db: Session,
        user_id: str,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
    ) -> List[Subscription]:
        """List subscriptions strictly scoped to the user with optional status filter"""
        statement = select(Subscription).where(Subscription.user_id == user_id)
        if status:
            statement = statement.where(Subscription.status == status)
        statement = statement.order_by(Subscription.renewal_date.asc()).offset(skip).limit(limit)
        return list(db.scalars(statement).all())

    @staticmethod
    def update(
        db: Session,
        db_obj: Subscription,
        obj_in: SubscriptionUpdate,
    ) -> Subscription:
        """Update an existing subscription"""
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def archive(db: Session, db_obj: Subscription) -> Subscription:
        """
        Soft-archive a subscription by setting status='archived'
        (Phase 2 specification rule).
        """
        db_obj.status = "archived"
        db.commit()
        db.refresh(db_obj)
        return db_obj


subscription_service = SubscriptionService()
