from __future__ import annotations

import sys
from pathlib import Path

from flask import Flask, render_template, request

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from model_utils import (
    DEFAULT_INPUT,
    FEATURE_NAMES,
    FEATURE_SPECS,
    coerce_features,
    get_model_overview,
    load_or_train_model,
    predict_age,
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asecretkey'
MODEL_PATH = BASE_DIR / "abalone_predictor.joblib"
MODEL_BUNDLE = load_or_train_model(MODEL_PATH)

@app.route("/", methods=["GET", "POST"])
def index():
    form_data = {name: str(DEFAULT_INPUT[name]) for name in FEATURE_NAMES}
    error = None

    if request.method == "POST":
        form_data = {name: request.form.get(name, "").strip() for name in FEATURE_NAMES}
        try:
            features = coerce_features(request.form)
            result = predict_age(MODEL_BUNDLE, features)
            return render_template(
                'prediction.html',
                result=result,
                features=features,
                overview=get_model_overview(MODEL_BUNDLE, MODEL_PATH),
                field_specs=FEATURE_SPECS,
            )
        except ValueError as exc:
            error = str(exc)

    return render_template(
        'home.html',
        field_specs=FEATURE_SPECS,
        form_data=form_data,
        error=error,
        overview=get_model_overview(MODEL_BUNDLE, MODEL_PATH),
    )


if __name__ == '__main__':
    app.run(debug=True)
