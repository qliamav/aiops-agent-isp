from __future__ import annotations

from fastapi import APIRouter, Response
from prometheus_client import CONTENT_TYPE_LATEST, CollectorRegistry, generate_latest

from .metrics import REQUEST_COUNT, REQUEST_LATENCY


router = APIRouter(prefix="/metrics", tags=["monitoring"])


@router.get("", include_in_schema=False)
async def metrics() -> Response:
    registry = CollectorRegistry()
    # Register example metrics so that export works without errors.
    REQUEST_COUNT.labels(method="GET", path="/health", status="200").inc(0)
    REQUEST_LATENCY.labels(path="/health").observe(0.0)
    data = generate_latest(registry)
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
