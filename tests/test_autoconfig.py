from __future__ import annotations

from fastapi.testclient import TestClient

from app.api import app


client = TestClient(app)


def test_autoconfig_dry_run_returns_payload() -> None:
    body = {
        "action_type": "limit_bandwidth",
        "target_id": "cust-1",
        "parameters": {"kbps": 1024},
    }
    response = client.post("/autoconfig/dry-run", json=body)
    assert response.status_code == 200
    data = response.json()
    assert data["dry_run"] is True
    assert data["action"]["target_id"] == "cust-1"
    assert data["action"]["parameters"]["kbps"] == 1024


def test_autoconfig_limit_bandwidth_accepts_request() -> None:
    response = client.post("/autoconfig/limit-bandwidth", params={"customer_id": "cust-2", "kbps": 2048})
    assert response.status_code == 200
    assert response.json()["accepted"] is True


def test_autoconfig_enable_monitoring_accepts_request() -> None:
    response = client.post("/autoconfig/enable-monitoring", params={"device_id": "dev-1"})
    assert response.status_code == 200
    assert response.json()["accepted"] is True
