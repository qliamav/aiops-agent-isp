from __future__ import annotations

from typing import Any

import httpx
from pydantic import BaseModel, Field


class GenieAcsDevice(BaseModel):
    id: str = Field(..., description="GenieACS device identifier")
    serial_number: str | None = None
    ip_address: str | None = None


class GenieAcsClient:
    def __init__(self, base_url: str, username: str, password: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient(base_url=self._base_url, auth=(username, password))

    async def list_devices(self) -> list[GenieAcsDevice]:
        response = await self._client.get("/devices")
        response.raise_for_status()
        data: list[dict[str, Any]] = response.json()
        return [GenieAcsDevice.model_validate(item) for item in data]

    async def aclose(self) -> None:
        await self._client.aclose()
