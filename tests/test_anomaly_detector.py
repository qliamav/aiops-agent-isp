"""Tests for app.models.anomaly_detector and train_anomaly."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from app.models.anomaly_detector import AnomalyDetector
from app.models.train_anomaly import load_detector, save_detector, train_anomaly


def test_anomaly_detector_fit_predict() -> None:
    rng = np.random.default_rng(42)
    X = rng.standard_normal((100, 5))
    detector = AnomalyDetector(n_estimators=10, contamination=0.1, random_state=42)
    detector.fit(X, feature_names=["a", "b", "c", "d", "e"])
    pred = detector.predict(X)
    assert pred.shape == (100,)
    assert set(np.unique(pred)).issubset({-1, 1})
    assert detector.feature_names == ["a", "b", "c", "d", "e"]


def test_anomaly_detector_score_samples() -> None:
    X = np.random.RandomState(0).randn(50, 3)
    detector = AnomalyDetector(n_estimators=10, random_state=0).fit(X)
    scores = detector.score_samples(X)
    assert scores.shape == (50,)
    assert np.all(np.isfinite(scores))


def test_anomaly_detector_get_params() -> None:
    detector = AnomalyDetector(n_estimators=20, contamination=0.05, random_state=1)
    params = detector.get_params()
    assert params["n_estimators"] == 20
    assert params["contamination"] == 0.05
    assert params["random_state"] == 1


def test_train_anomaly_returns_fitted_detector() -> None:
    X = np.random.RandomState(7).randn(80, 4)
    detector = train_anomaly(
        X,
        feature_names=["f1", "f2", "f3", "f4"],
        n_estimators=15,
        contamination=0.1,
        random_state=7,
    )
    assert detector.feature_names == ["f1", "f2", "f3", "f4"]
    pred = detector.predict(X[:5])
    assert pred.shape == (5,)


def test_save_and_load_detector(tmp_path: Path) -> None:
    X = np.random.RandomState(11).randn(60, 2)
    detector = train_anomaly(X, feature_names=["x", "y"], random_state=11)
    path = tmp_path / "detector.joblib"
    save_detector(detector, path)
    assert path.exists()
    loaded = load_detector(path)
    np.testing.assert_array_equal(detector.predict(X), loaded.predict(X))
    assert loaded.feature_names == detector.feature_names
