from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_info_endpoint_returns_service_and_env() -> None:
    response = client.get("/info")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "aiops-isp-lite"
    assert "env" in data


def test_rate_limiter_allows_initial_requests() -> None:
    # With default settings, a few rapid requests should be accepted.
    for _ in range(5):
        response = client.get("/health")
        assert response.status_code == 200
