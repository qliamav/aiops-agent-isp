from __future__ import annotations

import polars as pl

from app.features.engineer import FeatureEngineer
from app.features.preprocessor import Preprocessor


def test_preprocessor_and_engineer_pipeline() -> None:
    raw_events = [
        {"rx_bytes": 1000, "tx_bytes": 500, "latency_ms": 10.0, "timestamp": "2024-01-01T00:00:00"},
        {"rx_bytes": 2000, "tx_bytes": 1000, "latency_ms": 20.0, "timestamp": "2024-01-01T00:01:00"},
    ]

    pre = Preprocessor()
    frame = pre.to_frame(raw_events)
    assert isinstance(frame, pl.DataFrame)
    assert frame.height == 2

    engineer = FeatureEngineer()
    enriched = engineer.build_features(frame)

    for col in [
        "traffic_bytes_total",
        "traffic_bytes_delta",
        "traffic_bytes_total_z",
        "traffic_bytes_delta_z",
        "latency_ms_z",
    ]:
        assert col in enriched.columns
