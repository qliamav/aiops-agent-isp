"""Anomaly detection for ISP telemetry using Isolation Forest."""

from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.ensemble import IsolationForest


class AnomalyDetector:
    """Fits and predicts anomalies on numerical feature arrays."""

    def __init__(
        self,
        *,
        n_estimators: int = 100,
        contamination: float = 0.1,
        random_state: int | None = 42,
    ) -> None:
        self._model = IsolationForest(
            n_estimators=n_estimators,
            contamination=contamination,
            random_state=random_state,
        )
        self._feature_names: list[str] | None = None

    def fit(self, X: np.ndarray, feature_names: list[str] | None = None) -> AnomalyDetector:
        """Fit the detector on training data. X shape (n_samples, n_features)."""
        self._model.fit(X)
        self._feature_names = feature_names
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Return +1 for inlier, -1 for outlier per sample."""
        return self._model.predict(X)

    def score_samples(self, X: np.ndarray) -> np.ndarray:
        """Return anomaly score (negative = more anomalous)."""
        return self._model.score_samples(X)

    @property
    def feature_names(self) -> list[str] | None:
        return self._feature_names

    def get_params(self) -> dict[str, Any]:
        """Serializable params for persistence."""
        return {
            "n_estimators": self._model.n_estimators,
            "contamination": self._model.contamination,
            "random_state": self._model.random_state,
            "feature_names": self._feature_names,
        }
