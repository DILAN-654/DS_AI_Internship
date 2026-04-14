from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import warnings

import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split


FEATURE_NAMES = ("length", "diameter", "height", "whole_weight")

FEATURE_SPECS = {
    "length": {"label": "Shell length", "min": 0.1, "max": 1.0, "step": 0.01},
    "diameter": {"label": "Shell diameter", "min": 0.05, "max": 0.8, "step": 0.01},
    "height": {"label": "Shell height", "min": 0.01, "max": 0.4, "step": 0.01},
    "whole_weight": {"label": "Whole weight", "min": 0.05, "max": 3.0, "step": 0.01},
}

DEFAULT_INPUT = {
    "length": 0.55,
    "diameter": 0.42,
    "height": 0.14,
    "whole_weight": 0.85,
}


@dataclass(frozen=True)
class ModelBundle:
    model: Any
    metrics: dict[str, float]
    trained_at: str
    feature_names: tuple[str, ...]


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _generate_synthetic_abalone_data(n_samples: int = 3000) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(42)

    length = rng.uniform(0.15, 0.82, n_samples)
    diameter = np.clip(length * rng.normal(0.78, 0.06, n_samples), 0.08, 0.70)
    height = np.clip(diameter * rng.normal(0.28, 0.05, n_samples), 0.02, 0.30)
    density = rng.normal(23.0, 4.0, n_samples)
    whole_weight = np.clip(length * diameter * height * density + rng.normal(0.15, 0.08, n_samples), 0.05, 2.80)

    age = (
        1.5
        + 18.0 * length
        + 10.0 * diameter
        + 25.0 * height
        + 3.2 * whole_weight
        + rng.normal(0.0, 1.1, n_samples)
    )
    age = np.clip(age, 1.0, 30.0)

    X = np.column_stack([length, diameter, height, whole_weight])
    y = age.astype(float)
    return X, y


def train_and_save_model(model_path: str | Path, force: bool = False) -> ModelBundle:
    model_path = Path(model_path)
    if model_path.exists() and not force:
        return load_or_train_model(model_path)

    model_path.parent.mkdir(parents=True, exist_ok=True)

    X, y = _generate_synthetic_abalone_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    model = RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        min_samples_leaf=2,
        n_jobs=1,
    )
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    bundle = ModelBundle(
        model=model,
        metrics={
            "mae": float(mean_absolute_error(y_test, predictions)),
            "r2": float(r2_score(y_test, predictions)),
        },
        trained_at=_utc_now_iso(),
        feature_names=FEATURE_NAMES,
    )
    joblib.dump(bundle, model_path)
    return bundle


def load_or_train_model(model_path: str | Path) -> ModelBundle:
    model_path = Path(model_path)

    if model_path.exists():
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                loaded = joblib.load(model_path)
            if isinstance(loaded, ModelBundle):
                return loaded
            if hasattr(loaded, "predict"):
                return ModelBundle(
                    model=loaded,
                    metrics={},
                    trained_at="unknown",
                    feature_names=FEATURE_NAMES,
                )
        except Exception:
            pass

    return train_and_save_model(model_path, force=True)


def coerce_features(source: dict[str, Any]) -> dict[str, float]:
    features: dict[str, float] = {}

    for name in FEATURE_NAMES:
        raw_value = source.get(name)
        spec = FEATURE_SPECS[name]

        if raw_value is None or str(raw_value).strip() == "":
            raise ValueError(f"Please enter {spec['label'].lower()}.")

        try:
            value = float(str(raw_value).strip())
        except ValueError as exc:
            raise ValueError(f"{spec['label']} must be a numeric value.") from exc

        if value < float(spec["min"]) or value > float(spec["max"]):
            raise ValueError(
                f"{spec['label']} must be between {spec['min']} and {spec['max']}."
            )

        features[name] = value

    return features


def predict_age(bundle: ModelBundle, features: dict[str, float]) -> float:
    ordered = np.array([[features[name] for name in FEATURE_NAMES]], dtype=float)
    prediction = float(bundle.model.predict(ordered)[0])
    return round(prediction, 1)


def get_model_overview(bundle: ModelBundle, model_path: str | Path) -> dict[str, Any]:
    return {
        "algorithm": type(bundle.model).__name__,
        "metrics": bundle.metrics,
        "trained_at": bundle.trained_at,
        "model_path": str(Path(model_path)),
        "features": list(FEATURE_NAMES),
    }
