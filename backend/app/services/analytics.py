from collections import defaultdict
from datetime import date, datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.subscription import Subscription
from app.schemas.analytics import (
    CategorySpendItem,
    CurrencySpendSummary,
    DashboardSummaryResponse,
    FullDashboardResponse,
    NearestRenewal,
    ServiceSpendItem,
    SpendingByCategoryResponse,
    SpendingByServiceResponse,
    UpcomingRenewalItem,
    UpcomingRenewalsResponse,
)

# Constant decimal multipliers for high-precision financial arithmetic
TWELVE = Decimal("12")
THREE = Decimal("3")
FIFTY_TWO = Decimal("52")
FOUR = Decimal("4")
HUNDRED = Decimal("100")
CENT = Decimal("0.01")
TENTH = Decimal("0.1")


def normalize_monthly_cost(price: Decimal, billing_cycle: str) -> Decimal:
    """
    Normalize active subscription cost to monthly equivalent using Decimal arithmetic.

    Rules:
    - monthly:   monthly_cost = price
    - yearly:    monthly_cost = price / 12
    - quarterly: monthly_cost = price / 3
    - weekly:    monthly_cost = (price * 52) / 12
    """
    cycle = billing_cycle.lower().strip() if billing_cycle else "monthly"
    if cycle == "monthly":
        val = price
    elif cycle == "yearly":
        val = price / TWELVE
    elif cycle == "quarterly":
        val = price / THREE
    elif cycle == "weekly":
        val = (price * FIFTY_TWO) / TWELVE
    else:
        val = price

    return val.quantize(CENT, rounding=ROUND_HALF_UP)


def normalize_annual_cost(price: Decimal, billing_cycle: str) -> Decimal:
    """
    Normalize estimated annual recurring spending using Decimal arithmetic.

    Rules:
    - monthly:   annual_cost = price * 12
    - yearly:    annual_cost = price
    - quarterly: annual_cost = price * 4
    - weekly:    annual_cost = price * 52
    """
    cycle = billing_cycle.lower().strip() if billing_cycle else "monthly"
    if cycle == "monthly":
        val = price * TWELVE
    elif cycle == "yearly":
        val = price
    elif cycle == "quarterly":
        val = price * FOUR
    elif cycle == "weekly":
        val = price * FIFTY_TWO
    else:
        val = price * TWELVE

    return val.quantize(CENT, rounding=ROUND_HALF_UP)


class AnalyticsService:
    @staticmethod
    def _get_active_subscriptions(db: Session, user_id: str) -> List[Subscription]:
        """Query active subscriptions strictly scoped to the authenticated user"""
        statement = (
            select(Subscription)
            .where(
                Subscription.user_id == user_id,
                Subscription.status == "active",
            )
            .order_by(Subscription.renewal_date.asc())
        )
        return list(db.scalars(statement).all())

    def get_dashboard_summary(self, db: Session, user_id: str) -> DashboardSummaryResponse:
        """
        Compute top-level summary metrics:
        - Monthly recurring spend grouped by currency
        - Annual recurring spend grouped by currency
        - Active subscriptions count per currency and total
        - Next immediate renewal
        """
        active_subs = self._get_active_subscriptions(db, user_id)

        currency_groups: Dict[str, List[Subscription]] = defaultdict(list)
        for sub in active_subs:
            currency_groups[sub.currency.upper()].append(sub)

        currencies_summary: Dict[str, CurrencySpendSummary] = {}
        for curr, subs in currency_groups.items():
            total_monthly = sum(
                (normalize_monthly_cost(s.price, s.billing_cycle) for s in subs),
                Decimal("0.00"),
            ).quantize(CENT, rounding=ROUND_HALF_UP)

            total_annual = sum(
                (normalize_annual_cost(s.price, s.billing_cycle) for s in subs),
                Decimal("0.00"),
            ).quantize(CENT, rounding=ROUND_HALF_UP)

            currencies_summary[curr] = CurrencySpendSummary(
                currency=curr,
                monthly_spend=total_monthly,
                annual_spend=total_annual,
                active_subscriptions_count=len(subs),
            )

        # Determine primary currency: most active subscriptions, then highest spend
        primary_currency: Optional[str] = None
        if currencies_summary:
            primary_currency = max(
                currencies_summary.keys(),
                key=lambda c: (
                    currencies_summary[c].active_subscriptions_count,
                    currencies_summary[c].monthly_spend,
                ),
            )

        # Nearest renewal calculation
        nearest_renewal: Optional[NearestRenewal] = None
        today = date.today()
        if active_subs:
            nearest_sub = active_subs[0]
            days_until = (nearest_sub.renewal_date - today).days
            nearest_renewal = NearestRenewal(
                service_name=nearest_sub.service_name,
                renewal_date=nearest_sub.renewal_date,
                days_until=days_until,
                price=nearest_sub.price,
                currency=nearest_sub.currency.upper(),
                billing_cycle=nearest_sub.billing_cycle,
                category=nearest_sub.category,
            )

        return DashboardSummaryResponse(
            currencies=currencies_summary,
            primary_currency=primary_currency,
            total_active_subscriptions=len(active_subs),
            nearest_renewal=nearest_renewal,
        )

    def get_monthly_spending(self, db: Session, user_id: str) -> Dict[str, Decimal]:
        """Get normalized monthly spending grouped by currency"""
        summary = self.get_dashboard_summary(db, user_id)
        return {curr: item.monthly_spend for curr, item in summary.currencies.items()}

    def get_annual_spending(self, db: Session, user_id: str) -> Dict[str, Decimal]:
        """Get normalized annual spending grouped by currency"""
        summary = self.get_dashboard_summary(db, user_id)
        return {curr: item.annual_spend for curr, item in summary.currencies.items()}

    def get_spending_by_service(
        self, db: Session, user_id: str, currency: Optional[str] = None
    ) -> Dict[str, SpendingByServiceResponse]:
        """
        Calculate spending proportion per service for each currency (or a specific currency).
        Includes percentage calculation and optional grouped 'Other' slice for minor shares.
        """
        active_subs = self._get_active_subscriptions(db, user_id)
        if currency:
            active_subs = [s for s in active_subs if s.currency.upper() == currency.upper()]

        currency_groups: Dict[str, List[Subscription]] = defaultdict(list)
        for sub in active_subs:
            currency_groups[sub.currency.upper()].append(sub)

        results: Dict[str, SpendingByServiceResponse] = {}

        for curr, subs in currency_groups.items():
            # Sum normalized monthly spend per service
            service_map: Dict[str, Dict] = {}
            total_monthly = Decimal("0.00")

            for s in subs:
                m_cost = normalize_monthly_cost(s.price, s.billing_cycle)
                a_cost = normalize_annual_cost(s.price, s.billing_cycle)
                total_monthly += m_cost

                if s.service_name in service_map:
                    service_map[s.service_name]["monthly_spend"] += m_cost
                    service_map[s.service_name]["annual_spend"] += a_cost
                else:
                    service_map[s.service_name] = {
                        "service_name": s.service_name,
                        "currency": curr,
                        "monthly_spend": m_cost,
                        "annual_spend": a_cost,
                        "billing_cycle": s.billing_cycle,
                        "category": s.category,
                    }

            total_monthly = total_monthly.quantize(CENT, rounding=ROUND_HALF_UP)

            items: List[ServiceSpendItem] = []
            for item in service_map.values():
                m_spend = item["monthly_spend"].quantize(CENT, rounding=ROUND_HALF_UP)
                a_spend = item["annual_spend"].quantize(CENT, rounding=ROUND_HALF_UP)
                if total_monthly > Decimal("0.00"):
                    pct = ((m_spend / total_monthly) * HUNDRED).quantize(TENTH, rounding=ROUND_HALF_UP)
                else:
                    pct = Decimal("0.0")

                items.append(
                    ServiceSpendItem(
                        service_name=item["service_name"],
                        currency=curr,
                        monthly_spend=m_spend,
                        annual_spend=a_spend,
                        percentage=pct,
                        billing_cycle=item["billing_cycle"],
                        category=item["category"],
                    )
                )

            # Sort items descending by monthly spend
            items.sort(key=lambda x: x.monthly_spend, reverse=True)

            # Group long tail into Other if there are more than 6 services
            other_spend: Optional[Decimal] = None
            other_percentage: Optional[Decimal] = None
            if len(items) > 6:
                minor_items = items[5:]
                other_spend = sum((i.monthly_spend for i in minor_items), Decimal("0.00")).quantize(
                    CENT, rounding=ROUND_HALF_UP
                )
                if total_monthly > Decimal("0.00"):
                    other_percentage = ((other_spend / total_monthly) * HUNDRED).quantize(
                        TENTH, rounding=ROUND_HALF_UP
                    )
                else:
                    other_percentage = Decimal("0.0")

            results[curr] = SpendingByServiceResponse(
                currency=curr,
                total_monthly_spend=total_monthly,
                services=items,
                other_spend=other_spend,
                other_percentage=other_percentage,
            )

        return results

    def get_spending_by_category(
        self, db: Session, user_id: str, currency: Optional[str] = None
    ) -> Dict[str, SpendingByCategoryResponse]:
        """
        Calculate category analytics:
        - category
        - subscription count
        - normalized monthly spend
        - percentage of monthly spending
        """
        active_subs = self._get_active_subscriptions(db, user_id)
        if currency:
            active_subs = [s for s in active_subs if s.currency.upper() == currency.upper()]

        currency_groups: Dict[str, List[Subscription]] = defaultdict(list)
        for sub in active_subs:
            currency_groups[sub.currency.upper()].append(sub)

        results: Dict[str, SpendingByCategoryResponse] = {}

        for curr, subs in currency_groups.items():
            category_map: Dict[str, Dict] = {}
            total_monthly = Decimal("0.00")

            for s in subs:
                m_cost = normalize_monthly_cost(s.price, s.billing_cycle)
                total_monthly += m_cost
                cat = s.category or "Other"

                if cat in category_map:
                    category_map[cat]["count"] += 1
                    category_map[cat]["monthly_spend"] += m_cost
                else:
                    category_map[cat] = {
                        "category": cat,
                        "currency": curr,
                        "count": 1,
                        "monthly_spend": m_cost,
                    }

            total_monthly = total_monthly.quantize(CENT, rounding=ROUND_HALF_UP)

            cat_items: List[CategorySpendItem] = []
            for item in category_map.values():
                m_spend = item["monthly_spend"].quantize(CENT, rounding=ROUND_HALF_UP)
                if total_monthly > Decimal("0.00"):
                    pct = ((m_spend / total_monthly) * HUNDRED).quantize(TENTH, rounding=ROUND_HALF_UP)
                else:
                    pct = Decimal("0.0")

                cat_items.append(
                    CategorySpendItem(
                        category=item["category"],
                        currency=curr,
                        subscription_count=item["count"],
                        monthly_spend=m_spend,
                        percentage=pct,
                    )
                )

            # Sort descending by monthly spend
            cat_items.sort(key=lambda x: x.monthly_spend, reverse=True)

            results[curr] = SpendingByCategoryResponse(
                currency=curr,
                total_monthly_spend=total_monthly,
                categories=cat_items,
            )

        return results

    def get_upcoming_renewals(
        self, db: Session, user_id: str, days: Optional[int] = None, limit: int = 20
    ) -> UpcomingRenewalsResponse:
        """
        Query upcoming renewals sorted chronologically by renewal_date ascending.
        Optionally filter within the next `days` days.
        """
        statement = (
            select(Subscription)
            .where(
                Subscription.user_id == user_id,
                Subscription.status == "active",
            )
            .order_by(Subscription.renewal_date.asc())
        )
        subs = list(db.scalars(statement).all())
        today = date.today()

        renewal_items: List[UpcomingRenewalItem] = []
        for s in subs:
            days_until = (s.renewal_date - today).days
            if days is not None and days_until > days:
                continue

            renewal_items.append(
                UpcomingRenewalItem(
                    id=str(s.id),
                    service_name=s.service_name,
                    renewal_date=s.renewal_date,
                    days_until=days_until,
                    price=s.price,
                    currency=s.currency.upper(),
                    billing_cycle=s.billing_cycle,
                    category=s.category,
                    status=s.status,
                )
            )

        # Apply limit after ordering
        if limit:
            renewal_items = renewal_items[:limit]

        return UpcomingRenewalsResponse(
            total_upcoming=len(renewal_items),
            renewals=renewal_items,
        )

    def get_full_dashboard(self, db: Session, user_id: str) -> FullDashboardResponse:
        """
        Aggregate full dashboard payload into a single network call.
        Includes summary, spending by service, spending by category, and upcoming renewals.
        """
        summary = self.get_dashboard_summary(db, user_id)
        services = self.get_spending_by_service(db, user_id)
        categories = self.get_spending_by_category(db, user_id)
        renewals = self.get_upcoming_renewals(db, user_id, limit=20)

        return FullDashboardResponse(
            summary=summary,
            spending_by_service=services,
            spending_by_category=categories,
            upcoming_renewals=renewals,
        )


analytics_service = AnalyticsService()
