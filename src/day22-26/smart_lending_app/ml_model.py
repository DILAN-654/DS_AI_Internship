from __future__ import annotations

import csv
import json
import math
import os
import random
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "model"
MODEL_PATH = MODEL_DIR / "credit_model.joblib"
DEFAULT_DATASET_PATH = BASE_DIR / "datasets" / "Credit scoring Dataset.csv"


RISK_LABEL_MAP = {
    "Low Risk": "Low",
    "Medium Risk": "Medium",
    "High Risk": "High",
    "Low": "Low",
    "Medium": "Medium",
    "High": "High",
}

NUM_FEATURES = [
    "age",
    "monthly_income",
    "loan_amount",
    "transaction_count",
    "avg_monthly_spend",
    "savings_ratio",
    "mobile_recharge_freq",
    "missed_payments",
    "credit_score",
    "income_to_loan_ratio",
    "spend_to_income_ratio",
]
CAT_FEATURES = ["gender", "employment_type"]

ALL_FEATURES = [*NUM_FEATURES, *CAT_FEATURES]
TARGET_COL = "risk_category"

UNKNOWN_CATEGORY = "Unknown"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _get_n_jobs() -> int:
    try:
        n_jobs = int(str(os.environ.get("SKLEARN_N_JOBS", "1")).strip())
    except Exception:
        return 1
    if n_jobs == 0:
        return 1
    if n_jobs < -1:
        return -1
    return n_jobs


def _normalize_risk_label(label: str) -> str:
    if label is None:
        return "Medium"
    normalized = label.strip()
    return RISK_LABEL_MAP.get(normalized, normalized)


def _safe_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (float, int)):
        return float(value)
    s = str(value).strip()
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _safe_int(value: Any) -> Optional[int]:
    f = _safe_float(value)
    if f is None:
        return None
    try:
        return int(round(f))
    except Exception:
        return None


def enrich_features(raw: Dict[str, Any]) -> Dict[str, Any]:
    features = dict(raw)

    monthly_income = _safe_float(features.get("monthly_income"))
    loan_amount = _safe_float(features.get("loan_amount"))
    avg_monthly_spend = _safe_float(features.get("avg_monthly_spend"))

    if features.get("income_to_loan_ratio") is None:
        if monthly_income is None or loan_amount in (None, 0):
            features["income_to_loan_ratio"] = None
        else:
            features["income_to_loan_ratio"] = float(monthly_income / loan_amount)

    if features.get("spend_to_income_ratio") is None:
        if monthly_income in (None, 0) or avg_monthly_spend is None:
            features["spend_to_income_ratio"] = None
        else:
            features["spend_to_income_ratio"] = float(avg_monthly_spend / monthly_income)

    return features


def _prepare_features_for_model(enriched: Dict[str, Any]) -> Dict[str, Any]:
    prepared: Dict[str, Any] = {}

    for name in NUM_FEATURES:
        value = _safe_float(enriched.get(name))
        prepared[name] = float(value) if value is not None else math.nan

    for name in CAT_FEATURES:
        raw_value = enriched.get(name)
        text = str(raw_value).strip() if raw_value is not None else ""
        prepared[name] = text or UNKNOWN_CATEGORY

    return prepared


def load_credit_dataset(dataset_path: Path) -> Tuple[list[dict], list[str]]:
    X: list[dict] = []
    y: list[str] = []

    with dataset_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                features = {
                    "age": _safe_int(row.get("age")),
                    "gender": (row.get("gender") or "").strip() or None,
                    "employment_type": (row.get("employment_type") or "").strip() or None,
                    "monthly_income": _safe_float(row.get("monthly_income")),
                    "loan_amount": _safe_float(row.get("loan_amount")),
                    "transaction_count": _safe_int(row.get("transaction_count")),
                    "avg_monthly_spend": _safe_float(row.get("avg_monthly_spend")),
                    "savings_ratio": _safe_float(row.get("savings_ratio")),
                    "mobile_recharge_freq": _safe_int(row.get("mobile_recharge_freq")),
                    "missed_payments": _safe_int(row.get("missed_payments")),
                    "credit_score": _safe_int(row.get("credit_score")),
                    "income_to_loan_ratio": None,
                    "spend_to_income_ratio": None,
                }
                features = enrich_features(features)
                features = _prepare_features_for_model(features)

                label = _normalize_risk_label(row.get(TARGET_COL, "Medium"))
                if label not in ("Low", "Medium", "High"):
                    continue
                X.append(features)
                y.append(label)
            except Exception:
                continue

    if not X:
        raise ValueError(f"No usable rows found in dataset: {dataset_path}")

    return X, y


def generate_synthetic_dataset(n: int = 2500) -> Tuple[list[dict], list[str]]:
    rng = random.Random(42)
    X: list[dict] = []
    y: list[str] = []

    for _ in range(max(50, int(n))):
        age = rng.randint(21, 70)
        gender = rng.choice(["Male", "Female"])
        employment_type = rng.choices(
            ["Salaried", "Self-Employed", "Student", "Unemployed"],
            weights=[0.60, 0.27, 0.08, 0.05],
            k=1,
        )[0]

        monthly_income = max(3000.0, min(250000.0, rng.gauss(65000.0, 28000.0)))
        loan_amount = max(2000.0, min(900000.0, rng.gauss(250000.0, 160000.0)))
        transaction_count = rng.randint(10, 300)

        spend_ratio = min(0.95, max(0.15, rng.gauss(0.55, 0.18)))
        avg_monthly_spend = monthly_income * spend_ratio

        savings_ratio = min(0.60, max(0.01, rng.gauss(0.22, 0.12)))
        mobile_recharge_freq = rng.randint(0, 20)
        missed_payments = rng.choices([0, 1, 2, 3, 4, 5, 6], weights=[0.45, 0.20, 0.13, 0.09, 0.07, 0.04, 0.02], k=1)[0]
        credit_score = rng.randint(300, 850)

        features = enrich_features(
            {
                "age": age,
                "gender": gender,
                "employment_type": employment_type,
                "monthly_income": monthly_income,
                "loan_amount": loan_amount,
                "transaction_count": transaction_count,
                "avg_monthly_spend": avg_monthly_spend,
                "savings_ratio": savings_ratio,
                "mobile_recharge_freq": mobile_recharge_freq,
                "missed_payments": missed_payments,
                "credit_score": credit_score,
                "income_to_loan_ratio": None,
                "spend_to_income_ratio": None,
            }
        )
        features = _prepare_features_for_model(features)

        income_to_loan_ratio = _safe_float(features.get("income_to_loan_ratio"))
        if income_to_loan_ratio is None or math.isnan(income_to_loan_ratio):
            income_to_loan_ratio = 0.0
        spend_to_income_ratio = _safe_float(features.get("spend_to_income_ratio"))
        if spend_to_income_ratio is None or math.isnan(spend_to_income_ratio):
            spend_to_income_ratio = 0.0

        score = 0.0
        score += (credit_score - 600) / 80.0
        score += (monthly_income / 25000.0) * 1.5
        score += savings_ratio * 4.0
        score -= missed_payments * 1.7
        score -= max(0.0, spend_to_income_ratio - 0.6) * 6.0
        score += max(-2.5, min(2.5, (income_to_loan_ratio - 0.25) * 10.0))
        if employment_type == "Self-Employed":
            score -= 0.2
        if employment_type == "Unemployed":
            score -= 1.2
        if employment_type == "Student":
            score -= 0.7

        if score >= 3.0:
            label = "Low"
        elif score >= 0.5:
            label = "Medium"
        else:
            label = "High"

        X.append(features)
        y.append(label)

    return X, y


@dataclass(frozen=True)
class ModelBundle:
    pipeline: Any
    version: str
    trained_at: str
    metrics: Dict[str, Any]
    features: list[str]


def _import_sklearn():
    from joblib import dump, load  # type: ignore

    from sklearn.ensemble import RandomForestClassifier  # type: ignore
    from sklearn.feature_extraction import DictVectorizer  # type: ignore
    from sklearn.impute import SimpleImputer  # type: ignore
    from sklearn.metrics import classification_report  # type: ignore
    from sklearn.model_selection import train_test_split  # type: ignore
    from sklearn.pipeline import Pipeline  # type: ignore

    return {
        "dump": dump,
        "load": load,
        "RandomForestClassifier": RandomForestClassifier,
        "DictVectorizer": DictVectorizer,
        "SimpleImputer": SimpleImputer,
        "classification_report": classification_report,
        "train_test_split": train_test_split,
        "Pipeline": Pipeline,
    }


def train_and_save_model(force: bool = False, dataset_path: Optional[os.PathLike | str] = None) -> Dict[str, Any]:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    if MODEL_PATH.exists() and not force:
        bundle = load_model()
        return {
            "status": "skipped",
            "model_path": str(MODEL_PATH),
            "version": bundle.version,
            "trained_at": bundle.trained_at,
        }

    ds_path = Path(dataset_path) if dataset_path else DEFAULT_DATASET_PATH

    sklearn = _import_sklearn()
    if ds_path.exists():
        X, y = load_credit_dataset(ds_path)
        data_source = str(ds_path)
    else:
        X, y = generate_synthetic_dataset()
        data_source = "synthetic"

    (
        train_test_split,
        DictVectorizer,
        RandomForestClassifier,
        SimpleImputer,
        classification_report,
        Pipeline,
        dump,
    ) = (
        sklearn["train_test_split"],
        sklearn["DictVectorizer"],
        sklearn["RandomForestClassifier"],
        sklearn["SimpleImputer"],
        sklearn["classification_report"],
        sklearn["Pipeline"],
        sklearn["dump"],
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    clf = RandomForestClassifier(
        n_estimators=250,
        max_depth=14,
        random_state=42,
        class_weight="balanced",
        n_jobs=_get_n_jobs(),
    )
    pipeline = Pipeline(
        steps=[
            ("vec", DictVectorizer(sparse=False)),
            ("impute", SimpleImputer(strategy="median")),
            ("clf", clf),
        ]
    )
    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_test)
    metrics = classification_report(y_test, preds, output_dict=True, zero_division=0)

    version = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    bundle = ModelBundle(
        pipeline=pipeline,
        version=version,
        trained_at=_utc_now_iso(),
        metrics=metrics,
        features=ALL_FEATURES,
    )
    dump(bundle, MODEL_PATH)

    return {
        "status": "trained",
        "model_path": str(MODEL_PATH),
        "version": version,
        "trained_at": bundle.trained_at,
        "metrics": metrics,
        "rows": len(X),
        "data_source": data_source,
    }


def load_model() -> ModelBundle:
    if not MODEL_PATH.exists():
        train_and_save_model()

    sklearn = _import_sklearn()
    load = sklearn["load"]
    bundle = load(MODEL_PATH)

    if isinstance(bundle, ModelBundle):
        return bundle
    # Backwards compatibility: previous versions saved only the pipeline.
    return ModelBundle(
        pipeline=bundle,
        version="legacy",
        trained_at="unknown",
        metrics={},
        features=ALL_FEATURES,
    )


def predict_risk(features: Dict[str, Any], model_bundle: Optional[ModelBundle] = None) -> Tuple[str, float, Dict[str, float]]:
    features = enrich_features(features)

    if model_bundle is None:
        try:
            model_bundle = load_model()
        except Exception:
            return heuristic_predict_risk(features)

    pipeline = model_bundle.pipeline

    try:
        model_features = _prepare_features_for_model(features)
        pred = pipeline.predict([model_features])[0]
        probs = pipeline.predict_proba([model_features])[0]
        classes = pipeline.classes_
        prob_map = {str(k): float(v) for k, v in zip(classes, probs)}
        conf = float(max(prob_map.values()) if prob_map else 0.0)
        pred_norm = _normalize_risk_label(str(pred))
        return pred_norm, conf, prob_map
    except Exception:
        return heuristic_predict_risk(features)


def heuristic_predict_risk(features: Dict[str, Any]) -> Tuple[str, float, Dict[str, float]]:
    credit_score = _safe_int(features.get("credit_score")) or 650
    missed_payments = _safe_int(features.get("missed_payments")) or 0
    savings_ratio = _safe_float(features.get("savings_ratio"))
    spend_to_income_ratio = _safe_float(features.get("spend_to_income_ratio"))
    income_to_loan_ratio = _safe_float(features.get("income_to_loan_ratio"))

    score = 0.0
    score += (credit_score - 650) / 30.0
    score -= missed_payments * 1.5
    if savings_ratio is not None:
        score += (savings_ratio - 0.2) * 6.0
    if spend_to_income_ratio is not None:
        score -= max(0.0, spend_to_income_ratio - 0.55) * 8.0
    if income_to_loan_ratio is not None:
        score += max(-2.0, min(2.0, (income_to_loan_ratio - 0.25) * 10.0))

    if score >= 2.0:
        risk = "Low"
    elif score >= -1.0:
        risk = "Medium"
    else:
        risk = "High"

    # Soft probabilities from score.
    p_low = 1.0 / (1.0 + math.exp(-score))
    p_high = 1.0 - p_low
    p_med = 0.35
    probs = {
        "Low": float(max(0.0, min(1.0, p_low * 0.8))),
        "Medium": float(max(0.0, min(1.0, p_med))),
        "High": float(max(0.0, min(1.0, p_high * 0.8))),
    }
    total = sum(probs.values()) or 1.0
    probs = {k: v / total for k, v in probs.items()}
    conf = float(probs.get(risk, max(probs.values())))
    return risk, conf, probs


def build_explanation(features: Dict[str, Any], risk_level: str) -> Dict[str, Any]:
    features = enrich_features(features)

    credit_score = _safe_int(features.get("credit_score"))
    missed_payments = _safe_int(features.get("missed_payments"))
    savings_ratio = _safe_float(features.get("savings_ratio"))
    spend_to_income_ratio = _safe_float(features.get("spend_to_income_ratio"))
    income_to_loan_ratio = _safe_float(features.get("income_to_loan_ratio"))

    positives: list[str] = []
    risks: list[str] = []

    if credit_score is not None:
        if credit_score >= 750:
            positives.append(f"Strong credit score ({credit_score})")
        elif credit_score >= 650:
            positives.append(f"Fair credit score ({credit_score})")
        else:
            risks.append(f"Low credit score ({credit_score})")

    if missed_payments is not None:
        if missed_payments == 0:
            positives.append("No missed payments")
        elif missed_payments <= 2:
            risks.append(f"Some missed payments ({missed_payments})")
        else:
            risks.append(f"Frequent missed payments ({missed_payments})")

    if savings_ratio is not None:
        if savings_ratio >= 0.25:
            positives.append(f"Healthy savings ratio ({savings_ratio:.2f})")
        elif savings_ratio >= 0.10:
            positives.append(f"Moderate savings ratio ({savings_ratio:.2f})")
        else:
            risks.append(f"Low savings ratio ({savings_ratio:.2f})")

    if spend_to_income_ratio is not None:
        if spend_to_income_ratio <= 0.50:
            positives.append(f"Controlled spending ({spend_to_income_ratio:.2f} spend/income)")
        elif spend_to_income_ratio <= 0.80:
            risks.append(f"High spending ({spend_to_income_ratio:.2f} spend/income)")
        else:
            risks.append(f"Very high spending ({spend_to_income_ratio:.2f} spend/income)")

    if income_to_loan_ratio is not None:
        if income_to_loan_ratio >= 0.30:
            positives.append(f"Comfortable income-to-loan ratio ({income_to_loan_ratio:.2f})")
        elif income_to_loan_ratio >= 0.20:
            risks.append(f"Tight income-to-loan ratio ({income_to_loan_ratio:.2f})")
        else:
            risks.append(f"Very tight income-to-loan ratio ({income_to_loan_ratio:.2f})")

    return {
        "risk_level": _normalize_risk_label(risk_level),
        "positives": positives[:5],
        "risk_factors": risks[:5],
        "note": "Explanation is rule-based for transparency (basic XAI).",
    }


def recommend_loan_amount(
    monthly_income: float,
    credit_score: int,
    risk_level: str,
    requested_loan_amount: Optional[float] = None,
) -> int:
    annual_income = max(0.0, float(monthly_income)) * 12.0
    risk_level = _normalize_risk_label(risk_level)

    if risk_level == "Low":
        max_ratio = 0.55
    elif risk_level == "Medium":
        max_ratio = 0.35
    else:
        max_ratio = 0.18

    score_factor = max(0.6, min(1.15, (float(credit_score) - 500.0) / 350.0))
    max_allowed = annual_income * max_ratio * score_factor

    if requested_loan_amount is not None:
        recommended = min(float(requested_loan_amount), max_allowed)
    else:
        recommended = max_allowed

    return int(max(2000, min(recommended, 750000)))


def suggest_repayment_plan(risk_level: str) -> Tuple[int, float]:
    risk_level = _normalize_risk_label(risk_level)
    if risk_level == "Low":
        return 60, 0.11
    if risk_level == "Medium":
        return 48, 0.14
    return 36, 0.18


def calculate_emi(loan_amount: float, months: int = 60, annual_rate: float = 0.12) -> int:
    principal = max(0.0, float(loan_amount))
    n = max(1, int(months))
    r = float(annual_rate) / 12.0

    if r <= 0:
        return int(math.ceil(principal / n))

    factor = (1 + r) ** n
    emi = principal * r * factor / (factor - 1)
    return int(math.ceil(emi))


def to_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))
