from __future__ import annotations

from fastapi.testclient import TestClient

from app.api import app
from app.monitoring import router as monitoring_router


client = TestClient(app)


def test_metrics_endpoint_responds() -> None:
    # Ensure /metrics endpoint exists when router is included.
    app.include_router(monitoring_router)
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
