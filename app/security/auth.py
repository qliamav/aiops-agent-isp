"""API key auth for AIOPS ISP LITE (optional; no secrets hardcoded)."""

from __future__ import annotations

import os
from typing import Annotated

from fastapi import Header, HTTPException, status


def get_api_key(x_api_key: Annotated[str | None, Header(alias="X-Api-Key")] = None) -> str | None:
    """Extract API key from X-Api-Key header. Returns None if not configured."""
    return x_api_key


def require_api_key(
    x_api_key: Annotated[str | None, Header(alias="X-Api-Key")] = None,
) -> str:
    """Dependency: require valid API key from header or env. No delete/remove."""
    expected = os.environ.get("API_KEY")
    if not expected:
        return x_api_key or ""
    if not x_api_key or x_api_key != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
    return x_api_key
