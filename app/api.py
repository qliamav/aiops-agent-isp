from __future__ import annotations

from fastapi import FastAPI

from .main import app as base_app
from .autoconfig.controller import router as autoconfig_router


# Re-export FastAPI app with additional routers if needed.
app: FastAPI = base_app
app.include_router(autoconfig_router)
