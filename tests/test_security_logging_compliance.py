"""Tests for app.security.auth, app.logging.structured_logger, app.compliance.audit."""

from __future__ import annotations

import logging

from app.compliance.audit import AuditEntry, audit_log
from app.logging.structured_logger import StructuredFormatter, get_structured_logger
from app.security.auth import get_api_key, require_api_key


def test_get_api_key_returns_header_value() -> None:
    assert get_api_key("key-123") == "key-123"
    assert get_api_key(None) is None


def test_require_api_key_accepts_when_env_unset(monkeypatch: object) -> None:
    import os
    monkeypatch.delitem(os.environ, "API_KEY", raising=False)
    result = require_api_key("any-key")
    assert result in ("any-key", "")


def test_require_api_key_rejects_invalid_when_env_set(monkeypatch: object) -> None:
    from fastapi import HTTPException
    monkeypatch.setenv("API_KEY", "secret")
    try:
        require_api_key("wrong")
        assert False, "expected HTTPException"
    except HTTPException as e:
        assert e.status_code == 401


def test_structured_formatter_produces_json() -> None:
    formatter = StructuredFormatter()
    record = logging.LogRecord(
        name="test", level=logging.INFO, pathname="", lineno=0,
        msg="hello", args=(), exc_info=None,
    )
    record.getMessage = lambda: "hello"  # type: ignore[method-assign]
    out = formatter.format(record)
    assert "message" in out and "hello" in out


def test_get_structured_logger_returns_logger() -> None:
    log = get_structured_logger("test.module")
    assert log.name == "test.module"
    assert isinstance(log, logging.Logger)


def test_audit_entry_to_dict() -> None:
    entry = AuditEntry(actor="user1", action="update", resource="device/1", payload={"key": "v"})
    d = entry.to_dict()
    assert d["actor"] == "user1"
    assert d["action"] == "update"
    assert d["resource"] == "device/1"
    assert d["payload"] == {"key": "v"}


def test_audit_log_invokes_logger(caplog: logging.LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO, logger="aiops-isp-lite.audit")
    entry = AuditEntry(actor="sys", action="read", resource="config")
    audit_log(entry)
    assert len(caplog.records) >= 1
