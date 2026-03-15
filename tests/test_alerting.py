"""Tests for app.alerting.rules and app.alerting.notifier."""

from __future__ import annotations

import logging

from app.alerting.notifier import Notifier
from app.alerting.rules import AlertRule, Severity, severity_rank, should_fire


def test_severity_rank_order() -> None:
    assert severity_rank("low") < severity_rank("medium")
    assert severity_rank("medium") < severity_rank("high")
    assert severity_rank("high") < severity_rank("critical")
    assert severity_rank("unknown") == -1


def test_alert_rule_severity_rank() -> None:
    rule = AlertRule(min_severity=Severity.HIGH, device_id=None)
    assert rule.severity_rank() == 2


def test_should_fire_by_severity() -> None:
    rule = AlertRule(min_severity=Severity.MEDIUM, device_id=None)
    assert should_fire(rule, "high", device_id="dev-1") is True
    assert should_fire(rule, "critical", device_id=None) is True
    assert should_fire(rule, "low", device_id="dev-1") is False


def test_should_fire_by_device_id() -> None:
    rule = AlertRule(min_severity=Severity.LOW, device_id="dev-99")
    assert should_fire(rule, "high", device_id="dev-99") is True
    assert should_fire(rule, "high", device_id="dev-other") is False


def test_notifier_notify_logs(caplog: logging.LogCaptureFixture) -> None:
    caplog.set_level(logging.WARNING, logger="aiops-isp-lite.alerting")
    notifier = Notifier(log_only=True)
    notifier.notify(Severity.HIGH, "Test alert", device_id="dev-1", payload={"k": "v"})
    assert len(caplog.records) >= 1
    assert caplog.records[0].levelno == logging.WARNING
