from __future__ import annotations

from dataclasses import dataclass

import polars as pl
from sklearn.preprocessing import StandardScaler


@dataclass(slots=True)
class FeatureSpec:
    name: str
    description: str


class FeatureEngineer:
    """Simple feature engineering pipeline for ISP telemetry.

    This class expects a Polars DataFrame and creates a few numerical features
    ready for ML models, with type-safe signatures.
    """

    def __init__(self) -> None:
        self._scaler = StandardScaler()

    def build_features(self, frame: pl.DataFrame) -> pl.DataFrame:
        # Example: assume columns ["rx_bytes", "tx_bytes", "latency_ms"] exist.
        required = {"rx_bytes", "tx_bytes", "latency_ms"}
        missing = required.difference(set(frame.columns))
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")

        df = frame.with_columns(
            (pl.col("rx_bytes") + pl.col("tx_bytes")).alias("traffic_bytes_total"),
            (pl.col("rx_bytes") - pl.col("tx_bytes")).alias("traffic_bytes_delta"),
        )

        numeric = df.select(["traffic_bytes_total", "traffic_bytes_delta", "latency_ms"]).to_pandas()
        scaled = self._scaler.fit_transform(numeric)
        scaled_df = pl.DataFrame(
            scaled,
            schema=["traffic_bytes_total_z", "traffic_bytes_delta_z", "latency_ms_z"],
        )

        return df.hstack(scaled_df)

    def specs(self) -> list[FeatureSpec]:
        return [
            FeatureSpec(name="traffic_bytes_total", description="RX+TX bytes"),
            FeatureSpec(name="traffic_bytes_delta", description="RX-TX bytes"),
            FeatureSpec(name="latency_ms", description="Measured latency"),
        ]
