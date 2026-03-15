from __future__ import annotations

from typing import Sequence

from .genieacs_client import GenieAcsClient, GenieAcsDevice
from .splynx_client import SplynxClient, SplynxCustomer


class Ingestor:
    def __init__(self, splynx_client: SplynxClient, genieacs_client: GenieAcsClient) -> None:
        self._splynx_client = splynx_client
        self._genieacs_client = genieacs_client

    async def ingest(self) -> dict[str, Sequence[object]]:
        customers: list[SplynxCustomer] = await self._splynx_client.list_customers()
        devices: list[GenieAcsDevice] = await self._genieacs_client.list_devices()
        return {"customers": customers, "devices": devices}
