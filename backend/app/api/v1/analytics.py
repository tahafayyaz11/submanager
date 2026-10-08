from typing import Dict, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user_id
from app.db.session import get_db
from app.schemas.analytics import (
    DashboardSummaryResponse,
    FullDashboardResponse,
    SpendingByCategoryResponse,
    SpendingByServiceResponse,
    UpcomingRenewalsResponse,
)
from app.services.analytics import analytics_service

router = APIRouter()


@router.get(
    "/summary",
    response_model=DashboardSummaryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get dashboard summary metrics",
)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
) -> DashboardSummaryResponse:
    """
    Retrieve top-level summary cards:
    - Monthly recurring spend grouped by currency
    - Estimated annual spend grouped by currency
    - Total active subscriptions count
    - Immediate next renewal
    """
    return analytics_service.get_dashboard_summary(db=db, user_id=user_id)


@router.get(
    "/spending-by-service",
    response_model=Dict[str, SpendingByServiceResponse],
    status_code=status.HTTP_200_OK,
    summary="Get normalized spending grouped by service",
)
def get_spending_by_service(
    currency: Optional[str] = Query(None, description="Optional 3-letter currency code filter"),
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
) -> Dict[str, SpendingByServiceResponse]:
    """
    Retrieve service spending breakdown and percentage share.
    Normalized into monthly equivalent amounts.
    """
    return analytics_service.get_spending_by_service(db=db, user_id=user_id, currency=currency)


@router.get(
    "/spending-by-category",
    response_model=Dict[str, SpendingByCategoryResponse],
    status_code=status.HTTP_200_OK,
    summary="Get normalized spending grouped by category",
)
def get_spending_by_category(
    currency: Optional[str] = Query(None, description="Optional 3-letter currency code filter"),
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
) -> Dict[str, SpendingByCategoryResponse]:
    """
    Retrieve category analytics including subscription count, normalized monthly spend,
    and proportion of monthly budget.
    """
    return analytics_service.get_spending_by_category(db=db, user_id=user_id, currency=currency)


@router.get(
    "/upcoming-renewals",
    response_model=UpcomingRenewalsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get upcoming renewals ordered chronologically",
)
def get_upcoming_renewals(
    days: Optional[int] = Query(None, ge=1, description="Filter renewals within the next N days"),
    limit: int = Query(20, ge=1, le=100, description="Max renewals to return"),
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
) -> UpcomingRenewalsResponse:
    """
    Retrieve active upcoming renewals sorted by renewal date ascending.
    """
    return analytics_service.get_upcoming_renewals(db=db, user_id=user_id, days=days, limit=limit)


@router.get(
    "/dashboard",
    response_model=FullDashboardResponse,
    status_code=status.HTTP_200_OK,
    summary="Get aggregate dashboard analytics in a single call",
)
def get_full_dashboard(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
) -> FullDashboardResponse:
    """
    Single round-trip aggregated dashboard endpoint returning summary, services,
    categories, and upcoming renewals.
    """
    return analytics_service.get_full_dashboard(db=db, user_id=user_id)
