from datetime import date
from decimal import Decimal
from typing import Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class CurrencySpendSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    currency: str = Field(..., description="3-letter currency code (e.g., USD, PKR)")
    monthly_spend: Decimal = Field(..., description="Normalized current monthly recurring spend")
    annual_spend: Decimal = Field(..., description="Normalized estimated annual recurring spend")
    active_subscriptions_count: int = Field(..., description="Count of active subscriptions in this currency")


class NearestRenewal(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    service_name: str
    renewal_date: date
    days_until: int
    price: Decimal
    currency: str
    billing_cycle: str
    category: str


class DashboardSummaryResponse(BaseModel):
    currencies: Dict[str, CurrencySpendSummary] = Field(
        default_factory=dict, description="Spending summary grouped by currency"
    )
    primary_currency: Optional[str] = Field(
        None, description="Primary currency with most subscriptions or highest spend"
    )
    total_active_subscriptions: int = Field(0, description="Total active subscriptions across all currencies")
    nearest_renewal: Optional[NearestRenewal] = Field(None, description="Immediate next renewal")


class ServiceSpendItem(BaseModel):
    service_name: str
    currency: str
    monthly_spend: Decimal
    annual_spend: Decimal
    percentage: Decimal = Field(..., description="Percentage of total monthly spend in this currency")
    billing_cycle: str
    category: str


class SpendingByServiceResponse(BaseModel):
    currency: str
    total_monthly_spend: Decimal
    services: List[ServiceSpendItem]
    other_spend: Optional[Decimal] = Field(None, description="Summed spend for grouped minor slices (<3%)")
    other_percentage: Optional[Decimal] = Field(None, description="Percentage for grouped minor slices")


class CategorySpendItem(BaseModel):
    category: str
    currency: str
    subscription_count: int
    monthly_spend: Decimal
    percentage: Decimal = Field(..., description="Percentage of total monthly spend in this currency")


class SpendingByCategoryResponse(BaseModel):
    currency: str
    total_monthly_spend: Decimal
    categories: List[CategorySpendItem]


class UpcomingRenewalItem(BaseModel):
    id: str
    service_name: str
    renewal_date: date
    days_until: int
    price: Decimal
    currency: str
    billing_cycle: str
    category: str
    status: str


class UpcomingRenewalsResponse(BaseModel):
    total_upcoming: int
    renewals: List[UpcomingRenewalItem]


class FullDashboardResponse(BaseModel):
    summary: DashboardSummaryResponse
    spending_by_service: Dict[str, SpendingByServiceResponse]
    spending_by_category: Dict[str, SpendingByCategoryResponse]
    upcoming_renewals: UpcomingRenewalsResponse
