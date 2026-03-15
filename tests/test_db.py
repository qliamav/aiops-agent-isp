from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app
from app.db.models import Alert, Device


client = TestClient(app)


def test_device_and_alert_models_have_tablenames() -> None:
    assert Device.__tablename__ == "devices"
    assert Alert.__tablename__ == "alerts"


def test_models_have_expected_columns() -> None:
    device_columns = {c.name for c in Device.__table__.columns}  # type: ignore[attr-defined]
    alert_columns = {c.name for c in Alert.__table__.columns}  # type: ignore[attr-defined]
    assert {"id", "external_id", "customer_name", "ip_address", "extra_metadata", "created_at"}.issubset(
        device_columns
    )
    assert {"id", "device_id", "severity", "message", "payload", "created_at"}.issubset(alert_columns)


def test_health_endpoint_uses_models_module_importable() -> None:
    response = client.get("/health")
    assert response.status_code == 200
