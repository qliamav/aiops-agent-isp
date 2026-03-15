"""Tests for app.models.predictor and app.models.decision_tree."""

from __future__ import annotations

import numpy as np

from app.models.decision_tree import DecisionTreePredictor
from app.models.predictor import Predictor


def test_decision_tree_fit_predict() -> None:
    rng = np.random.RandomState(42)
    X = rng.randn(100, 4)
    y = (X[:, 0] + X[:, 1] > 0).astype(int)
    dt = DecisionTreePredictor(max_depth=5, min_samples_leaf=2, random_state=42)
    dt.fit(X, y, feature_names=["a", "b", "c", "d"])
    pred = dt.predict(X[:5])
    assert pred.shape == (5,)
    assert set(pred).issubset({0, 1})
    assert dt.feature_names == ["a", "b", "c", "d"]


def test_decision_tree_predict_proba() -> None:
    X = np.random.RandomState(0).randn(50, 3)
    y = np.random.RandomState(0).randint(0, 2, size=50)
    dt = DecisionTreePredictor(random_state=0).fit(X, y)
    proba = dt.predict_proba(X[:3])
    assert proba.shape == (3, 2)
    np.testing.assert_allclose(proba.sum(axis=1), 1.0)


def test_decision_tree_get_params() -> None:
    dt = DecisionTreePredictor(max_depth=8, min_samples_leaf=10, random_state=1)
    params = dt.get_params()
    assert params["max_depth"] == 8
    assert params["min_samples_leaf"] == 10
    assert params["random_state"] == 1


def test_predictor_facade_fit_predict() -> None:
    X = np.random.RandomState(7).randn(60, 3)
    y = np.random.RandomState(7).randint(0, 2, size=60)
    tree = DecisionTreePredictor(random_state=7)
    predictor = Predictor(tree)
    predictor.fit(X, y, feature_names=["f1", "f2", "f3"])
    pred = predictor.predict(X[:4])
    assert pred.shape == (4,)
    assert predictor.feature_names == ["f1", "f2", "f3"]
    assert predictor.n_classes >= 1


def test_predictor_predict_proba() -> None:
    X = np.random.RandomState(11).randn(40, 2)
    y = np.random.RandomState(11).randint(0, 2, size=40)
    tree = DecisionTreePredictor(random_state=11).fit(X, y)
    predictor = Predictor(tree)
    predictor.fit(X, y)
    proba = predictor.predict_proba(X[:2])
    assert proba.shape == (2, 2)
    np.testing.assert_allclose(proba.sum(axis=1), 1.0)
