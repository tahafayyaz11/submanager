import uuid
from decimal import Decimal
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.config import settings

client = TestClient(app)

DEV_HEADERS = {"X-User-Id": "test-user-alpha"}


def test_create_subscription():
    payload = {
        "service_name": "Spotify Premium",
        "plan_name": "Individual",
        "price": "10.99",
        "currency": "USD",
        "billing_cycle": "monthly",
        "renewal_date": "2026-11-20",
        "category": "Entertainment",
        "payment_method": "Credit Card",
        "reminder_days_before": [7, 3, 1],
        "notes": "Student discount ends next year",
        "status": "active",
    }
    response = client.post("/api/v1/subscriptions", json=payload, headers=DEV_HEADERS)
    assert response.status_code == 201
    data = response.json()
    assert data["service_name"] == "Spotify Premium"
    assert data["price"] == "10.99"
    assert data["currency"] == "USD"
    assert data["billing_cycle"] == "monthly"
    assert data["user_id"] == "test-user-alpha"
    assert data["status"] == "active"
    assert "id" in data
    assert "created_at" in data


def test_get_subscriptions_list():
    # Fetch list for user
    response = client.get("/api/v1/subscriptions", headers=DEV_HEADERS)
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    assert len(items) >= 1
    assert any(sub["service_name"] == "Spotify Premium" for sub in items)


def test_get_subscription_by_id():
    # First create
    create_res = client.post(
        "/api/v1/subscriptions",
        json={
            "service_name": "GitHub Copilot",
            "price": "10.00",
            "currency": "USD",
            "billing_cycle": "monthly",
            "renewal_date": "2026-12-01",
        },
        headers=DEV_HEADERS,
    )
    assert create_res.status_code == 201
    sub_id = create_res.json()["id"]

    # Fetch by ID
    get_res = client.get(f"/api/v1/subscriptions/{sub_id}", headers=DEV_HEADERS)
    assert get_res.status_code == 200
    assert get_res.json()["id"] == sub_id
    assert get_res.json()["service_name"] == "GitHub Copilot"


def test_update_subscription():
    # Create
    create_res = client.post(
        "/api/v1/subscriptions",
        json={
            "service_name": "Canva Pro",
            "price": "12.99",
            "currency": "USD",
            "billing_cycle": "monthly",
            "renewal_date": "2026-11-10",
        },
        headers=DEV_HEADERS,
    )
    assert create_res.status_code == 201
    sub_id = create_res.json()["id"]

    # Update price and plan_name
    update_res = client.put(
        f"/api/v1/subscriptions/{sub_id}",
        json={
            "price": "14.99",
            "plan_name": "Teams",
            "category": "Design",
        },
        headers=DEV_HEADERS,
    )
    assert update_res.status_code == 200
    data = update_res.json()
    assert data["price"] == "14.99"
    assert data["plan_name"] == "Teams"
    assert data["category"] == "Design"
    assert data["service_name"] == "Canva Pro"


def test_archive_subscription():
    # Create
    create_res = client.post(
        "/api/v1/subscriptions",
        json={
            "service_name": "Duolingo Plus",
            "price": "6.99",
            "currency": "USD",
            "billing_cycle": "monthly",
            "renewal_date": "2026-11-05",
        },
        headers=DEV_HEADERS,
    )
    assert create_res.status_code == 201
    sub_id = create_res.json()["id"]

    # Delete / Archive
    del_res = client.delete(f"/api/v1/subscriptions/{sub_id}", headers=DEV_HEADERS)
    assert del_res.status_code == 200
    data = del_res.json()
    assert data["id"] == sub_id
    assert data["status"] == "archived"


def test_validation_errors():
    # 1. Negative price
    res1 = client.post(
        "/api/v1/subscriptions",
        json={
            "service_name": "Invalid Sub",
            "price": "-10.00",
            "renewal_date": "2026-11-01",
        },
        headers=DEV_HEADERS,
    )
    assert res1.status_code == 422

    # 2. Empty service name
    res2 = client.post(
        "/api/v1/subscriptions",
        json={
            "service_name": "   ",
            "price": "10.00",
            "renewal_date": "2026-11-01",
        },
        headers=DEV_HEADERS,
    )
    assert res2.status_code == 422

    # 3. Invalid currency length
    res3 = client.post(
        "/api/v1/subscriptions",
        json={
            "service_name": "Valid Name",
            "price": "10.00",
            "currency": "US",
            "renewal_date": "2026-11-01",
        },
        headers=DEV_HEADERS,
    )
    assert res3.status_code == 422

    # 4. Invalid billing cycle
    res4 = client.post(
        "/api/v1/subscriptions",
        json={
            "service_name": "Valid Name",
            "price": "10.00",
            "billing_cycle": "biweekly",
            "renewal_date": "2026-11-01",
        },
        headers=DEV_HEADERS,
    )
    assert res4.status_code == 422


def test_not_found_handling():
    fake_id = uuid.uuid4()
    assert client.get(f"/api/v1/subscriptions/{fake_id}", headers=DEV_HEADERS).status_code == 404
    assert client.put(f"/api/v1/subscriptions/{fake_id}", json={"price": "20.00"}, headers=DEV_HEADERS).status_code == 404
    assert client.delete(f"/api/v1/subscriptions/{fake_id}", headers=DEV_HEADERS).status_code == 404


def test_user_isolation():
    """Verify user A cannot read, update, or archive user B's subscriptions"""
    user_a = {"X-User-Id": "user-alice-01"}
    user_b = {"X-User-Id": "user-bob-02"}

    # User A creates a subscription
    res_a = client.post(
        "/api/v1/subscriptions",
        json={
            "service_name": "Alice Secret SaaS",
            "price": "99.00",
            "currency": "USD",
            "billing_cycle": "monthly",
            "renewal_date": "2026-12-15",
        },
        headers=user_a,
    )
    assert res_a.status_code == 201
    sub_id = res_a.json()["id"]

    # User B lists subscriptions -> Alice's subscription MUST NOT appear
    b_list = client.get("/api/v1/subscriptions", headers=user_b)
    assert b_list.status_code == 200
    assert not any(s["id"] == sub_id for s in b_list.json())

    # User B attempts to access Alice's subscription directly -> 404 Not Found
    assert client.get(f"/api/v1/subscriptions/{sub_id}", headers=user_b).status_code == 404

    # User B attempts to update Alice's subscription -> 404 Not Found
    assert client.put(f"/api/v1/subscriptions/{sub_id}", json={"price": "1.00"}, headers=user_b).status_code == 404

    # User B attempts to archive Alice's subscription -> 404 Not Found
    assert client.delete(f"/api/v1/subscriptions/{sub_id}", headers=user_b).status_code == 404

    # User A can still retrieve and update it successfully
    a_get = client.get(f"/api/v1/subscriptions/{sub_id}", headers=user_a)
    assert a_get.status_code == 200
    assert a_get.json()["service_name"] == "Alice Secret SaaS"


def test_production_guardrail_unauthorized(monkeypatch):
    """Verify that outside development, lack of identity returns 401 Unauthorized"""
    monkeypatch.setattr(settings, "APP_ENV", "production")
    # Request without X-User-Id in production environment must return 401
    res = client.get("/api/v1/subscriptions")
    assert res.status_code == 401
