"""Alert rules: severity and condition evaluation for ISP alerts."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

try:
    from enum import StrEnum
except ImportError:
    class StrEnum(str, Enum):  # type: ignore[misc]
        """Backport of StrEnum for Python 3.10."""

        pass


class Severity(StrEnum):
    """Alert severity levels (low to critical)."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


_SEVERITY_ORDER: tuple[str, ...] = ("low", "medium", "high", "critical")


@dataclass(frozen=True, slots=True)
class AlertRule:
    """Rule that fires when alert severity is at or above threshold."""

    min_severity: Severity
    device_id: str | None = None  # None = any device

    def severity_rank(self) -> int:
        try:
            return _SEVERITY_ORDER.index(self.min_severity.value)
        except ValueError:
            return -1


def severity_rank(severity: str) -> int:
    """Return numeric rank for comparison (higher = more severe)."""
    try:
        return _SEVERITY_ORDER.index(severity.lower())
    except ValueError:
        return -1


def should_fire(rule: AlertRule, severity: str, device_id: str | None = None) -> bool:
    """Return True if the rule should fire for this alert."""
    if rule.device_id is not None and device_id is not None and rule.device_id != device_id:
        return False
    return severity_rank(severity) >= rule.severity_rank()
