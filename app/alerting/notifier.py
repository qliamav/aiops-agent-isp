"""Alert notifier: dispatch alerts (log, optional webhook/email stub)."""

from __future__ import annotations

import logging
from typing import Any

from .rules import Severity

logger = logging.getLogger("aiops-isp-lite.alerting")


class Notifier:
    """Sends alert payloads to configured channels (e.g. JSON log, future webhook)."""

    def __init__(self, *, log_only: bool = True) -> None:
        self._log_only = log_only

    def notify(
        self,
        severity: str | Severity,
        message: str,
        *,
        device_id: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> None:
        """Emit an alert (logged as JSON; no file/DB delete)."""
        sev = severity.value if isinstance(severity, Severity) else severity
        record: dict[str, Any] = {
            "severity": sev,
            "alert_message": message,
            "device_id": device_id,
        }
        if payload:
            record["payload"] = payload
        logger.warning("alert", extra=record)
