from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from app.main import logger

from .safe_actions import SafeAction, build_enable_monitoring_action, build_limit_bandwidth_action


router = APIRouter(prefix="/autoconfig", tags=["autoconfig"])


@router.post("/dry-run", response_model=dict[str, Any])
async def dry_run(action: SafeAction) -> dict[str, Any]:
    """Return the action that *would* be applied without touching external systems."""
    payload = action.to_audit_dict()
    logger.info("autoconfig_dry_run", extra={"action": payload})
    return {"dry_run": True, "action": payload}


@router.post("/limit-bandwidth", response_model=dict[str, Any])
async def limit_bandwidth(customer_id: str, kbps: int) -> dict[str, Any]:
    action = build_limit_bandwidth_action(customer_id=customer_id, kbps=kbps)
    logger.info("autoconfig_limit_bandwidth", extra={"action": action.to_audit_dict()})
    return {"accepted": True}


@router.post("/enable-monitoring", response_model=dict[str, Any])
async def enable_monitoring(device_id: str) -> dict[str, Any]:
    action = build_enable_monitoring_action(device_id=device_id)
    logger.info("autoconfig_enable_monitoring", extra={"action": action.to_audit_dict()})
    return {"accepted": True}
