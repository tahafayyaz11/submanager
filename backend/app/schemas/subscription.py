import re
import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator

BillingCycle = Literal["monthly", "yearly", "quarterly", "weekly"]
SubscriptionStatus = Literal["active", "cancelled", "archived", "paused"]


class SubscriptionBase(BaseModel):
    service_name: str = Field(..., min_length=1, max_length=100, description="Service name")
    plan_name: Optional[str] = Field(None, max_length=100, description="Plan or tier name")
    price: Decimal = Field(..., ge=Decimal("0.00"), decimal_places=2, description="Subscription price")
    currency: str = Field(default="USD", description="3-letter uppercase ISO 4217 currency code")
    billing_cycle: BillingCycle = Field(default="monthly", description="Billing cycle frequency")
    purchase_date: Optional[date] = Field(None, description="Original purchase date")
    renewal_date: date = Field(..., description="Next renewal charge date")
    category: str = Field(default="Other", max_length=50, description="Subscription category")
    payment_method: Optional[str] = Field(None, max_length=50, description="Payment method used")
    reminder_days_before: List[int] = Field(default=[7, 3, 1], description="Days before renewal to alert")
    notes: Optional[str] = Field(None, description="User notes or cancellation guidelines")
    status: SubscriptionStatus = Field(default="active", description="Subscription status")

    @field_validator("service_name")
    @classmethod
    def validate_service_name(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Service name cannot be empty or whitespace only")
        return stripped

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, v: str) -> str:
        upper = v.strip().upper()
        if not re.match(r"^[A-Z]{3}$", upper):
            raise ValueError("Currency must be exactly three uppercase letters (e.g., USD, PKR, EUR)")
        return upper

    @field_validator("reminder_days_before")
    @classmethod
    def validate_reminder_days(cls, v: List[int]) -> List[int]:
        for day in v:
            if day < 0:
                raise ValueError("Reminder days must be non-negative integers")
        return sorted(list(set(v)), reverse=True)


class SubscriptionCreate(SubscriptionBase):
    """Schema for creating a subscription"""
    pass


class SubscriptionUpdate(BaseModel):
    """Schema for updating a subscription (all fields optional)"""
    service_name: Optional[str] = Field(None, min_length=1, max_length=100)
    plan_name: Optional[str] = Field(None, max_length=100)
    price: Optional[Decimal] = Field(None, ge=Decimal("0.00"), decimal_places=2)
    currency: Optional[str] = None
    billing_cycle: Optional[BillingCycle] = None
    purchase_date: Optional[date] = None
    renewal_date: Optional[date] = None
    category: Optional[str] = Field(None, max_length=50)
    payment_method: Optional[str] = Field(None, max_length=50)
    reminder_days_before: Optional[List[int]] = None
    notes: Optional[str] = None
    status: Optional[SubscriptionStatus] = None

    @field_validator("service_name")
    @classmethod
    def validate_service_name(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            stripped = v.strip()
            if not stripped:
                raise ValueError("Service name cannot be empty")
            return stripped
        return v

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            upper = v.strip().upper()
            if not re.match(r"^[A-Z]{3}$", upper):
                raise ValueError("Currency must be exactly three uppercase letters")
            return upper
        return v


class SubscriptionResponse(SubscriptionBase):
    """Schema for subscription API responses"""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: str
    created_at: datetime
    updated_at: datetime
