from __future__ import annotations

from typing import Any

import pytest

from app.ingestion.ingestor import Ingestor


class DummySplynxClient:
    async def list_customers(self) -> list[dict[str, Any]]:  # pragma: no cover - trivial
        return [{"id": "c1"}, {"id": "c2"}]


class DummyGenieAcsClient:
    async def list_devices(self) -> list[dict[str, Any]]:  # pragma: no cover - trivial
        return [{"id": "d1"}]


@pytest.mark.asyncio
async def test_ingestor_returns_customers_and_devices() -> None:
    ingestor = Ingestor(splynx_client=DummySplynxClient(), genieacs_client=DummyGenieAcsClient())
    result = await ingestor.ingest()
    assert "customers" in result and "devices" in result
    assert len(result["customers"]) == 2
    assert len(result["devices"]) == 1
