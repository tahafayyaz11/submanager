from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_health_endpoint():
    """Verify Phase 1 GET /health specification"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data == {"status": "ok"}


def test_api_v1_health_endpoint():
    """Verify versioned /api/v1/health endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root_index_endpoint():
    """Verify application root metadata endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["app"] == "Subsfolio"
    assert data["health_check"] == "/health"
    assert "version" in data


def test_detailed_health_endpoint():
    """Verify detailed health endpoint structure"""
    response = client.get("/api/v1/health/detailed")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "database_connected" in data
    assert "database" in data
    assert "environment" in data
