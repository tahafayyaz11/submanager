import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import (
    ARRAY,
    CheckConstraint,
    Date,
    DateTime,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Subscription(Base):
    __tablename__ = "subscriptions"
    __table_args__ = (
        CheckConstraint("price >= 0", name="ck_subscription_positive_price"),
        CheckConstraint(
            "billing_cycle IN ('monthly', 'yearly', 'quarterly', 'weekly')",
            name="ck_subscription_billing_cycle",
        ),
        CheckConstraint(
            "status IN ('active', 'cancelled', 'archived', 'paused')",
            name="ck_subscription_status",
        ),
        Index("ix_subscriptions_user_id", "user_id"),
        Index("ix_subscriptions_renewal_date", "renewal_date"),
        Index("ix_subscriptions_status", "status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )
    service_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    plan_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="USD",
    )
    billing_cycle: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="monthly",
    )
    purchase_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )
    renewal_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="Other",
    )
    payment_method: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )
    reminder_days_before: Mapped[List[int]] = mapped_column(
        ARRAY(Integer),
        nullable=False,
        default=list,
    )
    notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="active",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
