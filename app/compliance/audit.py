"""Audit log for compliance (append-only; no delete/remove)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.logging.structured_logger import get_structured_logger

logger = get_structured_logger("aiops-isp-lite.audit")


@dataclass(slots=True)
class AuditEntry:
    """Single audit record: actor, action, resource, optional payload."""

    actor: str
    action: str
    resource: str
    payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "actor": self.actor,
            "action": self.action,
            "resource": self.resource,
            "payload": self.payload,
        }


def audit_log(entry: AuditEntry) -> None:
    """Append an audit entry to the structured log. No file or record deletion."""
    logger.info("audit", extra=entry.to_dict())
