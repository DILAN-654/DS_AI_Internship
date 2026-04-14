from __future__ import annotations

import sys
from pathlib import Path

from flask import Flask, jsonify, request

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from model_utils import DEFAULT_INPUT, coerce_features, get_model_overview, load_or_train_model, predict_age

app = Flask(__name__)
MODEL_PATH = BASE_DIR / "abalone_predictor.joblib"
MODEL_BUNDLE = load_or_train_model(MODEL_PATH)

@app.route("/")
def index():
    overview = get_model_overview(MODEL_BUNDLE, MODEL_PATH)
    return f"""
    <h1>Welcome to our abalone prediction service</h1>
    <p>This API predicts abalone age from four shell measurements.</p>
    <p><strong>Model:</strong> {overview["algorithm"]}</p>
    <p><strong>Last trained:</strong> {overview["trained_at"]}</p>
    <p>Send a JSON POST request to <code>/predict</code> with:</p>
    <ul>
    <li>length</li>
    <li>diameter</li>
    <li>height</li>
    <li>whole_weight</li>
    </ul>
    <p>Example payload:</p>
    <pre>{DEFAULT_INPUT}</pre>
    """

@app.route('/predict', methods=['POST'])
def abalone_prediction():
    content = request.get_json(silent=True)
    if not isinstance(content, dict):
        return jsonify({"error": "Send a JSON object with length, diameter, height, and whole_weight."}), 400

    try:
        features = coerce_features(content)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    result = predict_age(MODEL_BUNDLE, features)
    return jsonify(
        {
            "predicted_age_years": result,
            "inputs": features,
            "model": get_model_overview(MODEL_BUNDLE, MODEL_PATH),
        }
    )


@app.route('/health', methods=['GET'])
def health():
    overview = get_model_overview(MODEL_BUNDLE, MODEL_PATH)
    return jsonify(
        {
            "status": "ok",
            "service": "abalone-web-api",
            "algorithm": overview["algorithm"],
            "trained_at": overview["trained_at"],
            "metrics": overview["metrics"],
        }
    )

if __name__ == '__main__':
    app.run(debug=True)
