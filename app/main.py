import json
import logging
from collections import defaultdict
from time import time
from typing import Any, Callable

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .core.config import settings


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:  # type: ignore[override]
        payload: dict[str, Any] = {
            "timestamp": self.formatTime(record, datefmt="%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO))
for handler in logging.getLogger().handlers:
    handler.setFormatter(JsonFormatter())

logger = logging.getLogger("aiops-isp-lite")


_RATE_BUCKET: dict[str, list[float]] = defaultdict(list)


def rate_limiter(request: Request) -> None:
    client_host = request.client.host if request.client else "anonymous"
    window_seconds = settings.rate_limit_window_seconds
    max_requests = settings.rate_limit_requests

    now = time()
    window_start = now - window_seconds

    bucket = _RATE_BUCKET[client_host]
    _RATE_BUCKET[client_host] = [ts for ts in bucket if ts >= window_start]

    if len(_RATE_BUCKET[client_host]) >= max_requests:
        raise_429()

    _RATE_BUCKET[client_host].append(now)


def raise_429() -> None:
    raise HTTPException(status_code=429, detail="Rate limit exceeded")


app = FastAPI(title="AIOPS ISP LITE", version="0.1.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next: Callable[[Request], Any]):  # type: ignore[type-arg]
    start_time = time()
    response = await call_next(request)
    process_time = time() - start_time
    logger.info(
        "request_completed",
        extra={
            "path": request.url.path,
            "method": request.method,
            "status_code": getattr(response, "status_code", 0),
            "process_time_ms": round(process_time * 1000, 2),
        },
    )
    return response


@app.get("/health", dependencies=[Depends(rate_limiter)])
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/info", dependencies=[Depends(rate_limiter)])
async def info() -> dict[str, str]:
    return {"service": "aiops-isp-lite", "env": settings.app_env}


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("unhandled_exception", extra={"path": request.url.path})
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
