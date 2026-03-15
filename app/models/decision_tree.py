"""Decision tree classifier for ISP telemetry (e.g. incident type, fault class)."""

from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.tree import DecisionTreeClassifier


class DecisionTreePredictor:
    """Thin wrapper around sklearn DecisionTreeClassifier with type hints."""

    def __init__(
        self,
        *,
        max_depth: int | None = 10,
        min_samples_leaf: int = 5,
        random_state: int | None = 42,
    ) -> None:
        self._tree = DecisionTreeClassifier(
            max_depth=max_depth,
            min_samples_leaf=min_samples_leaf,
            random_state=random_state,
        )
        self._feature_names: list[str] | None = None

    def fit(
        self,
        X: np.ndarray,
        y: np.ndarray,
        *,
        feature_names: list[str] | None = None,
    ) -> DecisionTreePredictor:
        """Fit the decision tree. y: class labels (int)."""
        self._tree.fit(X, y)
        self._feature_names = feature_names
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict class label per sample."""
        return self._tree.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predict class probabilities."""
        return self._tree.predict_proba(X)

    @property
    def feature_names(self) -> list[str] | None:
        return self._feature_names

    def get_params(self) -> dict[str, Any]:
        """Serializable params."""
        return {
            "max_depth": self._tree.max_depth,
            "min_samples_leaf": self._tree.min_samples_leaf,
            "random_state": self._tree.random_state,
            "feature_names": self._feature_names,
        }
