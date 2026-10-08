import uuid
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_signup_success():
    unique_email = f"user_{uuid.uuid4().hex[:8]}@example.com"
    payload = {
        "email": unique_email,
        "password": "SecretPassword123!",
        "full_name": "Test User",
    }
    response = client.post("/api/v1/auth/signup", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == unique_email
    assert data["user"]["full_name"] == "Test User"
    assert "id" in data["user"]


def test_signup_duplicate_email():
    unique_email = f"duplicate_{uuid.uuid4().hex[:8]}@example.com"
    payload = {
        "email": unique_email,
        "password": "Password123!",
        "full_name": "Original User",
    }
    res1 = client.post("/api/v1/auth/signup", json=payload)
    assert res1.status_code == 201

    # Attempt to signup with same email
    res2 = client.post("/api/v1/auth/signup", json=payload)
    assert res2.status_code == 400
    assert "already exists" in res2.json()["detail"].lower()


def test_login_success():
    unique_email = f"login_{uuid.uuid4().hex[:8]}@example.com"
    password = "CorrectPassword123"
    # Create user
    client.post(
        "/api/v1/auth/signup",
        json={"email": unique_email, "password": password, "full_name": "Login User"},
    )

    # Login
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": unique_email, "password": password},
    )
    assert login_res.status_code == 200
    data = login_res.json()
    assert "access_token" in data
    assert data["user"]["email"] == unique_email


def test_login_invalid_password():
    unique_email = f"wrongpwd_{uuid.uuid4().hex[:8]}@example.com"
    client.post(
        "/api/v1/auth/signup",
        json={"email": unique_email, "password": "RealPassword123"},
    )

    # Login with bad password
    bad_res = client.post(
        "/api/v1/auth/login",
        json={"email": unique_email, "password": "WrongPassword"},
    )
    assert bad_res.status_code == 401
    assert "invalid email or password" in bad_res.json()["detail"].lower()


def test_get_me_protected():
    unique_email = f"me_{uuid.uuid4().hex[:8]}@example.com"
    signup_res = client.post(
        "/api/v1/auth/signup",
        json={"email": unique_email, "password": "Password123!", "full_name": "Me User"},
    )
    token = signup_res.json()["access_token"]

    # Call /me with Bearer token
    me_res = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me_res.status_code == 200
    me_data = me_res.json()
    assert me_data["email"] == unique_email
    assert me_data["full_name"] == "Me User"


def test_user_ownership_and_isolation():
    """
    CRITICAL PHASE 3 TEST:
    Verify that User A and User B have complete data isolation.
    User A cannot view, update, or archive User B's subscriptions.
    """
    user_a_email = f"user_a_{uuid.uuid4().hex[:8]}@example.com"
    user_b_email = f"user_b_{uuid.uuid4().hex[:8]}@example.com"

    # 1. Signup User A
    res_a = client.post(
        "/api/v1/auth/signup",
        json={"email": user_a_email, "password": "PasswordA123!", "full_name": "Alice"},
    )
    token_a = res_a.json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # 2. Signup User B
    res_b = client.post(
        "/api/v1/auth/signup",
        json={"email": user_b_email, "password": "PasswordB123!", "full_name": "Bob"},
    )
    token_b = res_b.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # 3. User A creates a subscription
    sub_a_payload = {
        "service_name": "Alice Netflix",
        "price": 19.99,
        "currency": "USD",
        "billing_cycle": "monthly",
        "renewal_date": "2026-11-01",
        "category": "Entertainment",
    }
    create_a_res = client.post("/api/v1/subscriptions", json=sub_a_payload, headers=headers_a)
    assert create_a_res.status_code == 201
    sub_a_id = create_a_res.json()["id"]

    # 4. User B creates a subscription
    sub_b_payload = {
        "service_name": "Bob Spotify",
        "price": 10.99,
        "currency": "USD",
        "billing_cycle": "monthly",
        "renewal_date": "2026-11-05",
        "category": "Entertainment",
    }
    create_b_res = client.post("/api/v1/subscriptions", json=sub_b_payload, headers=headers_b)
    assert create_b_res.status_code == 201
    sub_b_id = create_b_res.json()["id"]

    # 5. User A lists subscriptions: should only contain Alice's, NOT Bob's
    list_a_res = client.get("/api/v1/subscriptions", headers=headers_a)
    assert list_a_res.status_code == 200
    a_items = list_a_res.json()
    a_names = [item["service_name"] for item in a_items]
    assert "Alice Netflix" in a_names
    assert "Bob Spotify" not in a_names

    # 6. User B lists subscriptions: should only contain Bob's, NOT Alice's
    list_b_res = client.get("/api/v1/subscriptions", headers=headers_b)
    assert list_b_res.status_code == 200
    b_items = list_b_res.json()
    b_names = [item["service_name"] for item in b_items]
    assert "Bob Spotify" in b_names
    assert "Alice Netflix" not in b_names

    # 7. User B tries to read User A's subscription directly by ID -> 404 (strictly isolated)
    get_leak_res = client.get(f"/api/v1/subscriptions/{sub_a_id}", headers=headers_b)
    assert get_leak_res.status_code == 404

    # 8. User B tries to update User A's subscription -> 404
    update_leak_res = client.put(
        f"/api/v1/subscriptions/{sub_a_id}",
        json={"service_name": "Hacked Netflix"},
        headers=headers_b,
    )
    assert update_leak_res.status_code == 404

    # 9. User B tries to archive User A's subscription -> 404
    archive_leak_res = client.delete(
        f"/api/v1/subscriptions/{sub_a_id}",
        headers=headers_b,
    )
    assert archive_leak_res.status_code == 404
