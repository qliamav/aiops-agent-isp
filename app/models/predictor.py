"""Generic predictor interface for ISP telemetry (classification/regression)."""

from __future__ import annotations

from typing import Any, Protocol

import numpy as np


class PredictorProtocol(Protocol):
    """Protocol for fit/predict models used by the predictor facade."""

    def fit(self, X: np.ndarray, y: np.ndarray) -> Any: ...
    def predict(self, X: np.ndarray) -> np.ndarray: ...


class Predictor:
    """Facade that wraps a decision tree (or other model) for inference."""

    def __init__(self, model: PredictorProtocol) -> None:
        self._model = model
        self._feature_names: list[str] | None = None
        self._n_classes_: int = 0

    def fit(
        self,
        X: np.ndarray,
        y: np.ndarray,
        *,
        feature_names: list[str] | None = None,
    ) -> Predictor:
        """Fit the underlying model and store metadata."""
        self._model.fit(X, y)
        self._feature_names = feature_names
        self._n_classes_ = len(np.unique(y))
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Return predicted class or value per sample."""
        return self._model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Return class probabilities if the model supports it."""
        if hasattr(self._model, "predict_proba"):
            return self._model.predict_proba(X)
        raise AttributeError("Underlying model has no predict_proba")

    @property
    def feature_names(self) -> list[str] | None:
        return self._feature_names

    @property
    def n_classes(self) -> int:
        return self._n_classes_
