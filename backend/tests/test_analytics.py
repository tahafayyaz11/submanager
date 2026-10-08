import uuid
from datetime import date, timedelta
from decimal import Decimal
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.analytics import (
    normalize_monthly_cost,
    normalize_annual_cost,
    analytics_service,
)

client = TestClient(app)


# ---------------- Normalization Unit Tests ----------------

def test_normalization_monthly():
    price = Decimal("100.00")
    assert normalize_monthly_cost(price, "monthly") == Decimal("100.00")
    assert normalize_annual_cost(price, "monthly") == Decimal("1200.00")


def test_normalization_yearly():
    price = Decimal("120.00")
    # 120 / 12 = 10.00
    assert normalize_monthly_cost(price, "yearly") == Decimal("10.00")
    assert normalize_annual_cost(price, "yearly") == Decimal("120.00")


def test_normalization_quarterly():
    price = Decimal("30.00")
    # 30 / 3 = 10.00
    assert normalize_monthly_cost(price, "quarterly") == Decimal("10.00")
    assert normalize_annual_cost(price, "quarterly") == Decimal("120.00")


def test_normalization_weekly():
    price = Decimal("10.00")
    # (10 * 52) / 12 = 43.3333... -> 43.33
    assert normalize_monthly_cost(price, "weekly") == Decimal("43.33")
    assert normalize_annual_cost(price, "weekly") == Decimal("520.00")


# ---------------- Integration & API Tests ----------------

@pytest.fixture
def test_users():
    user_a = f"test-analyst-a-{uuid.uuid4().hex[:8]}"
    user_b = f"test-analyst-b-{uuid.uuid4().hex[:8]}"
    return user_a, user_b


def test_empty_account_analytics(test_users):
    user_a, _ = test_users
    headers = {"X-User-Id": user_a}

    res = client.get("/api/v1/analytics/summary", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["total_active_subscriptions"] == 0
    assert data["currencies"] == {}
    assert data["primary_currency"] is None
    assert data["nearest_renewal"] is None

    # Test full dashboard on empty account
    res_full = client.get("/api/v1/analytics/dashboard", headers=headers)
    assert res_full.status_code == 200
    full_data = res_full.json()
    assert full_data["summary"]["total_active_subscriptions"] == 0
    assert full_data["upcoming_renewals"]["total_upcoming"] == 0


def test_multi_cycle_and_multi_currency_summary(test_users):
    user_a, _ = test_users
    headers = {"X-User-Id": user_a}
    today = date.today()

    # 1. Netflix: PKR 1,100 / monthly
    client.post(
        "/api/v1/subscriptions",
        headers=headers,
        json={
            "service_name": "Netflix",
            "price": "1100.00",
            "currency": "PKR",
            "billing_cycle": "monthly",
            "renewal_date": (today + timedelta(days=10)).isoformat(),
            "category": "Entertainment",
            "status": "active",
        },
    )

    # 2. Spotify: PKR 4,788 / yearly -> 399/mo
    client.post(
        "/api/v1/subscriptions",
        headers=headers,
        json={
            "service_name": "Spotify",
            "price": "4788.00",
            "currency": "PKR",
            "billing_cycle": "yearly",
            "renewal_date": (today + timedelta(days=20)).isoformat(),
            "category": "Entertainment",
            "status": "active",
        },
    )

    # 3. ChatGPT: USD 20.00 / monthly
    client.post(
        "/api/v1/subscriptions",
        headers=headers,
        json={
            "service_name": "ChatGPT Plus",
            "price": "20.00",
            "currency": "USD",
            "billing_cycle": "monthly",
            "renewal_date": (today + timedelta(days=5)).isoformat(),
            "category": "AI Tools",
            "status": "active",
        },
    )

    # 4. Archived subscription (must NOT contribute to spend)
    client.post(
        "/api/v1/subscriptions",
        headers=headers,
        json={
            "service_name": "Old Expired VPN",
            "price": "50.00",
            "currency": "USD",
            "billing_cycle": "monthly",
            "renewal_date": (today + timedelta(days=1)).isoformat(),
            "category": "Security",
            "status": "archived",
        },
    )

    # Query summary
    res = client.get("/api/v1/analytics/summary", headers=headers)
    assert res.status_code == 200
    data = res.json()

    # Active count must be 3 (excluding archived)
    assert data["total_active_subscriptions"] == 3

    # Primary currency is PKR (2 subscriptions vs 1 in USD)
    assert data["primary_currency"] == "PKR"

    # PKR calculations: 1100 + (4788/12 = 399) = 1499.00
    pkr_summary = data["currencies"]["PKR"]
    assert Decimal(pkr_summary["monthly_spend"]) == Decimal("1499.00")
    # Annual: (1100 * 12 = 13200) + 4788 = 17988.00
    assert Decimal(pkr_summary["annual_spend"]) == Decimal("17988.00")
    assert pkr_summary["active_subscriptions_count"] == 2

    # USD calculations: only 20.00 (archived 50.00 excluded)
    usd_summary = data["currencies"]["USD"]
    assert Decimal(usd_summary["monthly_spend"]) == Decimal("20.00")
    assert Decimal(usd_summary["annual_spend"]) == Decimal("240.00")
    assert usd_summary["active_subscriptions_count"] == 1

    # Nearest renewal: ChatGPT Plus is in 5 days (earliest among active)
    assert data["nearest_renewal"] is not None
    assert data["nearest_renewal"]["service_name"] == "ChatGPT Plus"
    assert data["nearest_renewal"]["days_until"] == 5


def test_spending_by_service_endpoint(test_users):
    user_a, _ = test_users
    headers = {"X-User-Id": user_a}
    today = date.today()

    # Add 2 services in USD
    client.post(
        "/api/v1/subscriptions",
        headers=headers,
        json={
            "service_name": "Figma",
            "price": "12.00",
            "currency": "USD",
            "billing_cycle": "monthly",
            "renewal_date": (today + timedelta(days=15)).isoformat(),
            "category": "Design",
            "status": "active",
        },
    )
    client.post(
        "/api/v1/subscriptions",
        headers=headers,
        json={
            "service_name": "Claude Pro",
            "price": "20.00",
            "currency": "USD",
            "billing_cycle": "monthly",
            "renewal_date": (today + timedelta(days=25)).isoformat(),
            "category": "AI Tools",
            "status": "active",
        },
    )

    res = client.get("/api/v1/analytics/spending-by-service?currency=USD", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "USD" in data
    usd_services = data["USD"]
    assert Decimal(usd_services["total_monthly_spend"]) == Decimal("32.00")

    services = usd_services["services"]
    assert len(services) == 2
    # Highest spend first: Claude Pro (20.00) then Figma (12.00)
    assert services[0]["service_name"] == "Claude Pro"
    # 20 / 32 = 62.5%
    assert Decimal(str(services[0]["percentage"])) == Decimal("62.5")
    assert services[1]["service_name"] == "Figma"
    # 12 / 32 = 37.5%
    assert Decimal(str(services[1]["percentage"])) == Decimal("37.5")


def test_spending_by_category_endpoint(test_users):
    user_a, _ = test_users
    headers = {"X-User-Id": user_a}
    today = date.today()

    client.post(
        "/api/v1/subscriptions",
        headers=headers,
        json={
            "service_name": "Notion",
            "price": "10.00",
            "currency": "USD",
            "billing_cycle": "monthly",
            "renewal_date": (today + timedelta(days=12)).isoformat(),
            "category": "Productivity",
            "status": "active",
        },
    )
    client.post(
        "/api/v1/subscriptions",
        headers=headers,
        json={
            "service_name": "Todoist",
            "price": "5.00",
            "currency": "USD",
            "billing_cycle": "monthly",
            "renewal_date": (today + timedelta(days=18)).isoformat(),
            "category": "Productivity",
            "status": "active",
        },
    )

    res = client.get("/api/v1/analytics/spending-by-category?currency=USD", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "USD" in data
    categories = data["USD"]["categories"]
    prod_cat = next((c for c in categories if c["category"] == "Productivity"), None)
    assert prod_cat is not None
    assert prod_cat["subscription_count"] == 2
    assert Decimal(prod_cat["monthly_spend"]) == Decimal("15.00")


def test_upcoming_renewals_ordering(test_users):
    user_a, _ = test_users
    headers = {"X-User-Id": user_a}
    today = date.today()

    # Create 3 subscriptions with distinct dates
    client.post(
        "/api/v1/subscriptions",
        headers=headers,
        json={
            "service_name": "Service Far",
            "price": "15.00",
            "currency": "USD",
            "billing_cycle": "monthly",
            "renewal_date": (today + timedelta(days=30)).isoformat(),
            "category": "Cloud",
            "status": "active",
        },
    )
    client.post(
        "/api/v1/subscriptions",
        headers=headers,
        json={
            "service_name": "Service Near",
            "price": "5.00",
            "currency": "USD",
            "billing_cycle": "monthly",
            "renewal_date": (today + timedelta(days=2)).isoformat(),
            "category": "Cloud",
            "status": "active",
        },
    )

    res = client.get("/api/v1/analytics/upcoming-renewals", headers=headers)
    assert res.status_code == 200
    data = res.json()
    renewals = data["renewals"]
    assert len(renewals) >= 2
    # First must be Service Near
    assert renewals[0]["service_name"] == "Service Near"
    assert renewals[0]["days_until"] == 2


def test_cross_user_isolation(test_users):
    user_a, user_b = test_users
    headers_a = {"X-User-Id": user_a}
    headers_b = {"X-User-Id": user_b}
    today = date.today()

    # User A creates a subscription
    client.post(
        "/api/v1/subscriptions",
        headers=headers_a,
        json={
            "service_name": "Private Server",
            "price": "99.00",
            "currency": "USD",
            "billing_cycle": "monthly",
            "renewal_date": (today + timedelta(days=7)).isoformat(),
            "category": "Developer Tools",
            "status": "active",
        },
    )

    # User B checks their summary - must NOT see User A's subscription
    res_b = client.get("/api/v1/analytics/summary", headers=headers_b)
    assert res_b.status_code == 200
    data_b = res_b.json()
    assert data_b["total_active_subscriptions"] == 0
    assert "USD" not in data_b["currencies"]
    assert data_b["nearest_renewal"] is None


def test_analytics_invalid_bearer_token():
    headers = {"Authorization": "Bearer invalid.malformed.token"}
    res = client.get("/api/v1/analytics/summary", headers=headers)
    assert res.status_code == 401
    assert "Invalid or expired authentication token" in res.json()["detail"]


def test_analytics_missing_auth_in_production(monkeypatch):
    from app.core.config import settings

    monkeypatch.setattr(settings, "APP_ENV", "production")
    monkeypatch.setattr(settings, "DEV_USER_ID", None)
    # Request without Authorization header
    res = client.get("/api/v1/analytics/summary")
    assert res.status_code == 401

