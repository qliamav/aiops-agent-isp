"""Structured JSON logger for AIOPS (no file/stream delete)."""

from __future__ import annotations

import json
import logging
from typing import Any


class StructuredFormatter(logging.Formatter):
    """Format log records as single-line JSON."""

    def format(self, record: logging.LogRecord) -> str:  # type: ignore[override]
        payload: dict[str, Any] = {
            "timestamp": self.formatTime(record, datefmt="%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        for key, value in record.__dict__.items():
            if key not in (
                "name", "msg", "args", "created", "filename", "funcName",
                "levelname", "levelno", "lineno", "module", "msecs",
                "pathname", "process", "processName", "relativeCreated",
                "stack_info", "exc_info", "exc_text", "thread", "threadName",
                "message", "taskName",
            ) and value is not None and not callable(value):
                payload[key] = value
        return json.dumps(payload, ensure_ascii=False, default=str)


def get_structured_logger(name: str) -> logging.Logger:
    """Return a logger with structured JSON formatting (adds handler if missing)."""
    log = logging.getLogger(name)
    if not log.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(StructuredFormatter())
        log.addHandler(handler)
        log.setLevel(logging.INFO)
    return log
