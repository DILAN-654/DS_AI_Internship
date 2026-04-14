from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np
from joblib import dump, load
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split


BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "model"
MODEL_PATH = MODEL_DIR / "iris_random_forest.joblib"

FEATURE_NAMES = (
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width",
)

FEATURE_SPECS = {
    "sepal_length": {"label": "Sepal length", "unit": "cm", "min": 4.0, "max": 8.0, "step": 0.1},
    "sepal_width": {"label": "Sepal width", "unit": "cm", "min": 2.0, "max": 4.5, "step": 0.1},
    "petal_length": {"label": "Petal length", "unit": "cm", "min": 1.0, "max": 7.0, "step": 0.1},
    "petal_width": {"label": "Petal width", "unit": "cm", "min": 0.1, "max": 2.6, "step": 0.1},
}

DEFAULT_SAMPLE = {
    "sepal_length": 5.9,
    "sepal_width": 3.0,
    "petal_length": 5.1,
    "petal_width": 1.8,
}


@dataclass(frozen=True)
class ModelBundle:
    model: Any
    accuracy: float
    report: dict[str, Any]
    feature_importances: dict[str, float]
    feature_names: tuple[str, ...]
    class_names: tuple[str, ...]
    trained_at: str


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def train_and_save_model(force: bool = False) -> ModelBundle:
    if MODEL_PATH.exists() and not force:
        return load_model_bundle()

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    iris = load_iris()
    X = iris.data
    y = iris.target
    class_names = tuple(str(name) for name in iris.target_names)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=8,
        min_samples_split=2,
        random_state=42,
    )
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = float(accuracy_score(y_test, predictions))
    report = classification_report(
        y_test,
        predictions,
        target_names=class_names,
        output_dict=True,
        zero_division=0,
    )
    feature_importances = {
        name: float(score)
        for name, score in zip(FEATURE_NAMES, model.feature_importances_)
    }

    bundle = ModelBundle(
        model=model,
        accuracy=accuracy,
        report=report,
        feature_importances=feature_importances,
        feature_names=FEATURE_NAMES,
        class_names=class_names,
        trained_at=_utc_now_iso(),
    )
    dump(bundle, MODEL_PATH)
    get_model_bundle.cache_clear()
    return bundle


def load_model_bundle() -> ModelBundle:
    if not MODEL_PATH.exists():
        return train_and_save_model(force=True)
    bundle = load(MODEL_PATH)
    if not isinstance(bundle, ModelBundle):
        raise TypeError("Saved model file does not contain a valid ModelBundle.")
    return bundle


@lru_cache(maxsize=1)
def get_model_bundle() -> ModelBundle:
    return load_model_bundle()


def _ordered_vector(features: dict[str, float]) -> np.ndarray:
    return np.array([[float(features[name]) for name in FEATURE_NAMES]], dtype=float)


def predict_species(features: dict[str, float], model_bundle: ModelBundle | None = None) -> dict[str, Any]:
    bundle = model_bundle or get_model_bundle()
    vector = _ordered_vector(features)

    probabilities = bundle.model.predict_proba(vector)[0]
    best_index = int(np.argmax(probabilities))

    probability_map = {
        class_name: float(probability)
        for class_name, probability in zip(bundle.class_names, probabilities)
    }

    return {
        "predicted_class": bundle.class_names[best_index],
        "confidence": float(probabilities[best_index]),
        "probabilities": probability_map,
        "features": {name: float(features[name]) for name in FEATURE_NAMES},
    }


def get_model_overview() -> dict[str, Any]:
    bundle = get_model_bundle()
    ranked_features = sorted(
        bundle.feature_importances.items(),
        key=lambda item: item[1],
        reverse=True,
    )
    return {
        "algorithm": "RandomForestClassifier",
        "accuracy": bundle.accuracy,
        "trained_at": bundle.trained_at,
        "classes": list(bundle.class_names),
        "feature_importances": ranked_features,
        "model_path": str(MODEL_PATH),
    }


if __name__ == "__main__":
    bundle = train_and_save_model(force=True)
    print(f"Model trained successfully at {MODEL_PATH}")
    print(f"Accuracy: {bundle.accuracy:.2%}")
