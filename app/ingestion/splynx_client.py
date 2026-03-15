from __future__ import annotations

from typing import Any

import httpx
from pydantic import BaseModel, Field


class SplynxCustomer(BaseModel):
    id: str = Field(..., description="Splynx customer identifier")
    name: str
    status: str


class SplynxClient:
    def __init__(self, base_url: str, api_key: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._client = httpx.AsyncClient(base_url=self._base_url, headers={"Authorization": f"Bearer {api_key}"})

    async def list_customers(self) -> list[SplynxCustomer]:
        response = await self._client.get("/customers")
        response.raise_for_status()
        raw_items: list[dict[str, Any]] = response.json()
        return [SplynxCustomer.model_validate(item) for item in raw_items]

    async def aclose(self) -> None:
        await self._client.aclose()
