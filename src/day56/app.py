from __future__ import annotations

import json
import os
from typing import Any

from flask import Flask, jsonify, render_template, request

from random_forest_model import (
    DEFAULT_SAMPLE,
    FEATURE_SPECS,
    get_model_overview,
    predict_species,
    train_and_save_model,
)


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "day56-random-forest-demo")

# Create the model artifact once so the app is deployable on a fresh server.
train_and_save_model()


def _coerce_features(source: dict[str, Any]) -> dict[str, float]:
    features: dict[str, float] = {}

    for name, spec in FEATURE_SPECS.items():
        raw_value = source.get(name)
        if raw_value is None or str(raw_value).strip() == "":
            raise ValueError(f"Please enter {spec['label'].lower()}.")

        try:
            value = float(str(raw_value).strip())
        except ValueError as exc:
            raise ValueError(f"{spec['label']} must be a number.") from exc

        if value < float(spec["min"]) or value > float(spec["max"]):
            raise ValueError(
                f"{spec['label']} should be between {spec['min']} and {spec['max']} {spec['unit']}."
            )

        features[name] = value

    return features


def _format_form_data(source: dict[str, Any]) -> dict[str, str]:
    return {
        name: str(source.get(name, DEFAULT_SAMPLE[name]))
        for name in FEATURE_SPECS
    }


@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    error = None
    form_data = _format_form_data(DEFAULT_SAMPLE)

    if request.method == "POST":
        form_data = _format_form_data(request.form)
        try:
            features = _coerce_features(request.form)
            prediction = predict_species(features)
        except ValueError as exc:
            error = str(exc)

    return render_template(
        "index.html",
        field_specs=FEATURE_SPECS,
        form_data=form_data,
        prediction=prediction,
        error=error,
        overview=get_model_overview(),
        default_payload=json.dumps(DEFAULT_SAMPLE, indent=2),
    )


@app.post("/api/predict")
def api_predict():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "Send a JSON object with the four flower measurements."}), 400

    try:
        features = _coerce_features(payload)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    result = predict_species(features)
    result["model"] = get_model_overview()
    return jsonify(result)


@app.get("/health")
def health():
    overview = get_model_overview()
    return jsonify(
        {
            "status": "ok",
            "service": "day56-random-forest-web-app",
            "model": overview["algorithm"],
            "accuracy": overview["accuracy"],
            "trained_at": overview["trained_at"],
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=True)
