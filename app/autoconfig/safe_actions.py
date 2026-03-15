from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


class ActionType(str, Enum):
    """High-level safe actions the agent can perform."""

    UPDATE_QOS = "update_qos"
    LIMIT_BANDWIDTH = "limit_bandwidth"
    ENABLE_MONITORING = "enable_monitoring"


@dataclass(frozen=True, slots=True)
class SafeAction:
    """Declarative, side-effect-free description of an auto-config action."""

    action_type: ActionType
    target_id: str
    parameters: Mapping[str, Any]

    def to_audit_dict(self) -> dict[str, Any]:
        return {
            "action_type": self.action_type.value,
            "target_id": self.target_id,
            "parameters": dict(self.parameters),
        }


def build_limit_bandwidth_action(customer_id: str, kbps: int) -> SafeAction:
    if kbps <= 0:
        raise ValueError("kbps must be positive")
    return SafeAction(
        action_type=ActionType.LIMIT_BANDWIDTH,
        target_id=customer_id,
        parameters={"kbps": kbps},
    )


def build_enable_monitoring_action(device_id: str) -> SafeAction:
    return SafeAction(
        action_type=ActionType.ENABLE_MONITORING,
        target_id=device_id,
        parameters={},
    )
