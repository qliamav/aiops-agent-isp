"""Train anomaly detector from preprocessed feature matrix."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .anomaly_detector import AnomalyDetector


def train_anomaly(
    X: np.ndarray,
    *,
    feature_names: list[str] | None = None,
    n_estimators: int = 100,
    contamination: float = 0.1,
    random_state: int | None = 42,
) -> AnomalyDetector:
    """Train and return a fitted AnomalyDetector."""
    detector = AnomalyDetector(
        n_estimators=n_estimators,
        contamination=contamination,
        random_state=random_state,
    )
    detector.fit(X, feature_names=feature_names)
    return detector


def save_detector(detector: AnomalyDetector, path: Path | str) -> None:
    """Persist detector state (params + sklearn model) for later load."""
    import joblib

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "model": detector._model,
            "feature_names": detector._feature_names,
        },
        path,
    )


def load_detector(path: Path | str) -> AnomalyDetector:
    """Load a previously saved detector."""
    import joblib

    data = joblib.load(path)
    det = AnomalyDetector()
    det._model = data["model"]
    det._feature_names = data.get("feature_names")
    return det
