from __future__ import annotations

from typing import Iterable

import polars as pl


class Preprocessor:
    """Prepares raw ISP events into a tabular Polars DataFrame."""

    def __init__(self, *, tz: str = "UTC") -> None:
        self._tz = tz

    def to_frame(self, events: Iterable[dict[str, object]]) -> pl.DataFrame:
        frame = pl.DataFrame(events)
        if "timestamp" in frame.columns:
            frame = frame.with_columns(
                pl.col("timestamp").str.strptime(pl.Datetime).dt.convert_time_zone(self._tz)
            )
        return frame
