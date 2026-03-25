import os
import json
from datetime import datetime
from functools import wraps
from pathlib import Path

from flask import Flask, abort, flash, jsonify, redirect, render_template, request, send_from_directory, url_for
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from ml_model import (
    build_explanation,
    calculate_emi,
    load_model,
    predict_risk,
    recommend_loan_amount,
    suggest_repayment_plan,
    to_json,
    train_and_save_model,
)

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
DATASETS_DIR = BASE_DIR / "datasets"


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "smart-lending-dev-secret")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    f"sqlite:///{(BASE_DIR / 'smart_lending.db').as_posix()}",
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAX_CONTENT_LENGTH"] = int(os.environ.get("MAX_UPLOAD_BYTES", str(5 * 1024 * 1024)))

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    applications = db.relationship("LoanApplication", backref="user", lazy=True)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class LoanApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)

    # Borrower & alternative data (aligned with dataset)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    employment_type = db.Column(db.String(50), nullable=False)

    monthly_income = db.Column(db.Float, nullable=False)
    requested_loan_amount = db.Column(db.Float, nullable=False)

    transaction_count = db.Column(db.Integer, nullable=False)
    avg_monthly_spend = db.Column(db.Float, nullable=False)
    savings_ratio = db.Column(db.Float, nullable=False)
    mobile_recharge_freq = db.Column(db.Integer, nullable=False)
    missed_payments = db.Column(db.Integer, nullable=False)
    credit_score = db.Column(db.Integer, nullable=False)

    document_filename = db.Column(db.String(255))

    # System outputs
    system_recommendation = db.Column(db.String(30), nullable=False, default="Review")
    recommended_loan_amount = db.Column(db.Integer)
    term_months = db.Column(db.Integer)
    annual_interest_rate = db.Column(db.Float)
    estimated_emi = db.Column(db.Integer)

    # Admin decision
    status = db.Column(db.String(20), nullable=False, default="Pending")  # Pending/Approved/Rejected

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    prediction = db.relationship("Prediction", backref="application", uselist=False, lazy=True)


class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey("loan_application.id"), nullable=False, unique=True, index=True)

    risk_level = db.Column(db.String(10), nullable=False)  # Low/Medium/High
    confidence_score = db.Column(db.Float, nullable=False)
    probabilities_json = db.Column(db.Text)
    explanation_json = db.Column(db.Text)
    model_version = db.Column(db.String(40), nullable=False, default="unknown")

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


@login_manager.user_loader
def load_user(user_id: str):
    try:
        return db.session.get(User, int(user_id))
    except Exception:
        return None


@app.context_processor
def inject_globals():
    return {
        "user": current_user if getattr(current_user, "is_authenticated", False) else None,
        "datetime": datetime,
    }


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return login_manager.unauthorized()
        if not getattr(current_user, "is_admin", False):
            abort(403)
        return fn(*args, **kwargs)

    return wrapper


def init_db():
    db.create_all()

    admin_email = os.environ.get("ADMIN_EMAIL", "admin@smartlending.com").strip().lower()
    admin_password = os.environ.get("ADMIN_PASSWORD", "Admin@123")

    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        admin_user = User(
            name="Admin",
            email=admin_email,
            password_hash=generate_password_hash(admin_password),
            is_admin=True,
        )
        db.session.add(admin_user)
        db.session.commit()


def ensure_directories():
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    DATASETS_DIR.mkdir(parents=True, exist_ok=True)


def allowed_file(filename: str) -> bool:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in {"pdf", "png", "jpg", "jpeg"}


def setup_app_once():
    if getattr(app, "_did_setup", False):
        return

    ensure_directories()
    init_db()
    try:
        train_and_save_model(force=False)
    except Exception:
        # Model training can be triggered later from the Admin panel.
        pass

    app._did_setup = True


@app.before_request
def _run_setup_once():
    setup_app_once()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        if not (name and email and password):
            flash("Please fill all fields.", "danger")
            return redirect(url_for("register"))

        if User.query.filter_by(email=email).first():
            flash("Email already exists.", "warning")
            return redirect(url_for("register"))

        user = User(name=name, email=email, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect(url_for("admin_dashboard") if user.is_admin else url_for("dashboard"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for("home"))


@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.is_admin:
        return redirect(url_for("admin_dashboard"))

    apps = (
        LoanApplication.query.filter_by(user_id=current_user.id)
        .order_by(LoanApplication.created_at.desc())
        .all()
    )
    return render_template("dashboard.html", apps=apps)


@app.route("/apply", methods=["GET", "POST"])
@login_required
def apply_loan():
    if current_user.is_admin:
        flash("Admin accounts cannot submit loan applications.", "warning")
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        form = request.form

        def bad(msg: str):
            flash(msg, "danger")
            return redirect(url_for("apply_loan"))

        try:
            age = int(form.get("age") or 0)
            gender = (form.get("gender") or "").strip()
            employment_type = (form.get("employment_type") or "").strip()

            monthly_income = float(form.get("monthly_income") or 0)
            requested_loan_amount = float(form.get("requested_loan_amount") or 0)

            transaction_count = int(form.get("transaction_count") or 0)
            avg_monthly_spend = float(form.get("avg_monthly_spend") or 0)
            savings_ratio = float(form.get("savings_ratio") or 0)
            mobile_recharge_freq = int(form.get("mobile_recharge_freq") or 0)
            missed_payments = int(form.get("missed_payments") or 0)
            credit_score = int(form.get("credit_score") or 0)
        except Exception:
            return bad("Please enter valid values in all fields.")

        if not (18 <= age <= 90):
            return bad("Age must be between 18 and 90.")
        if gender not in {"Male", "Female", "Other"}:
            return bad("Please select a valid gender.")
        if employment_type not in {"Salaried", "Self-Employed", "Student", "Unemployed"}:
            return bad("Please select a valid employment type.")
        if monthly_income <= 0 or requested_loan_amount <= 0:
            return bad("Income and requested loan amount must be greater than 0.")
        if not (0 <= savings_ratio <= 1):
            return bad("Savings ratio must be between 0 and 1.")
        if not (300 <= credit_score <= 850):
            return bad("Credit score must be between 300 and 850.")
        if transaction_count < 0 or mobile_recharge_freq < 0 or missed_payments < 0:
            return bad("Counts and missed payments cannot be negative.")

        document = request.files.get("document")
        saved_filename = None
        if document and document.filename:
            if not allowed_file(document.filename):
                return bad("Invalid document type. Upload PDF/JPG/PNG only.")
            safe_name = secure_filename(document.filename)
            stamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
            saved_filename = f"u{current_user.id}_{stamp}_{safe_name}"
            document.save(UPLOAD_DIR / saved_filename)

        features = {
            "age": age,
            "gender": gender,
            "employment_type": employment_type,
            "monthly_income": monthly_income,
            "loan_amount": requested_loan_amount,
            "transaction_count": transaction_count,
            "avg_monthly_spend": avg_monthly_spend,
            "savings_ratio": savings_ratio,
            "mobile_recharge_freq": mobile_recharge_freq,
            "missed_payments": missed_payments,
            "credit_score": credit_score,
        }

        model_bundle = None
        model_version = "heuristic"
        try:
            model_bundle = load_model()
            model_version = model_bundle.version
        except Exception:
            model_bundle = None

        risk_level, confidence, probabilities = predict_risk(features, model_bundle=model_bundle)
        explanation = build_explanation(features, risk_level)

        if risk_level == "Low":
            system_rec = "Approve"
        elif risk_level == "Medium":
            system_rec = "Review"
        else:
            system_rec = "Reject"

        term_months, annual_rate = suggest_repayment_plan(risk_level)
        recommended_amount = recommend_loan_amount(
            monthly_income=monthly_income,
            credit_score=credit_score,
            risk_level=risk_level,
            requested_loan_amount=requested_loan_amount,
        )
        emi = calculate_emi(recommended_amount, months=term_months, annual_rate=annual_rate)

        application = LoanApplication(
            user_id=current_user.id,
            age=age,
            gender=gender,
            employment_type=employment_type,
            monthly_income=monthly_income,
            requested_loan_amount=requested_loan_amount,
            transaction_count=transaction_count,
            avg_monthly_spend=avg_monthly_spend,
            savings_ratio=savings_ratio,
            mobile_recharge_freq=mobile_recharge_freq,
            missed_payments=missed_payments,
            credit_score=credit_score,
            document_filename=saved_filename,
            system_recommendation=system_rec,
            recommended_loan_amount=recommended_amount,
            term_months=term_months,
            annual_interest_rate=annual_rate,
            estimated_emi=emi,
            status="Pending",
        )
        db.session.add(application)
        db.session.flush()  # get ID before creating Prediction

        prediction = Prediction(
            application_id=application.id,
            risk_level=risk_level,
            confidence_score=float(round(confidence, 4)),
            probabilities_json=to_json(probabilities),
            explanation_json=to_json(explanation),
            model_version=model_version,
        )
        db.session.add(prediction)
        db.session.commit()

        return redirect(url_for("application_detail", application_id=application.id))

    return render_template("apply.html")


@app.route("/applications/<int:application_id>")
@login_required
def application_detail(application_id: int):
    application = LoanApplication.query.get_or_404(application_id)
    if (not current_user.is_admin) and application.user_id != current_user.id:
        abort(403)

    prediction = application.prediction
    probabilities = {}
    explanation = {}
    if prediction:
        try:
            probabilities = json.loads(prediction.probabilities_json or "{}")
        except Exception:
            probabilities = {}
        try:
            explanation = json.loads(prediction.explanation_json or "{}")
        except Exception:
            explanation = {}

    return render_template(
        "application_detail.html",
        application=application,
        prediction=prediction,
        probabilities=probabilities,
        explanation=explanation,
    )


@app.route("/uploads/<path:filename>")
@login_required
def download_upload(filename: str):
    application = LoanApplication.query.filter_by(document_filename=filename).first()
    if not application:
        abort(404)
    if (not current_user.is_admin) and application.user_id != current_user.id:
        abort(403)
    return send_from_directory(UPLOAD_DIR, filename, as_attachment=True)


@app.route("/admin")
@admin_required
def admin_dashboard():
    apps = LoanApplication.query.order_by(LoanApplication.created_at.desc()).all()

    total = len(apps)
    approved = sum(1 for a in apps if a.status == "Approved")
    rejected = sum(1 for a in apps if a.status == "Rejected")
    pending = sum(1 for a in apps if a.status == "Pending")

    risk_counts = {"Low": 0, "Medium": 0, "High": 0}
    for a in apps:
        if a.prediction and a.prediction.risk_level in risk_counts:
            risk_counts[a.prediction.risk_level] += 1

    return render_template(
        "admin.html",
        apps=apps,
        stats={
            "total": total,
            "approved": approved,
            "rejected": rejected,
            "pending": pending,
            "low": risk_counts["Low"],
            "medium": risk_counts["Medium"],
            "high": risk_counts["High"],
        },
    )


@app.route("/admin/applications/<int:application_id>")
@admin_required
def admin_application_detail(application_id: int):
    application = LoanApplication.query.get_or_404(application_id)

    prediction = application.prediction
    probabilities = {}
    explanation = {}
    if prediction:
        try:
            probabilities = json.loads(prediction.probabilities_json or "{}")
        except Exception:
            probabilities = {}
        try:
            explanation = json.loads(prediction.explanation_json or "{}")
        except Exception:
            explanation = {}

    return render_template(
        "application_detail.html",
        application=application,
        prediction=prediction,
        probabilities=probabilities,
        explanation=explanation,
        admin_view=True,
    )


@app.route("/admin/action/<int:application_id>/<action>", methods=["POST"])
@admin_required
def admin_action(application_id: int, action: str):
    application = LoanApplication.query.get_or_404(application_id)
    action = action.lower()

    if action == "approve":
        application.status = "Approved"
    elif action == "reject":
        application.status = "Rejected"
    else:
        flash("Invalid action.", "danger")
        return redirect(url_for("admin_dashboard"))

    db.session.commit()
    flash(f"Application marked as {application.status}.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/train", methods=["GET", "POST"])
@admin_required
def admin_train():
    info = {}
    error = None

    if request.method == "POST":
        dataset_file = request.files.get("dataset")
        dataset_path = None

        if dataset_file and dataset_file.filename:
            safe_name = secure_filename(dataset_file.filename)
            if not safe_name.lower().endswith(".csv"):
                flash("Please upload a CSV file.", "danger")
                return redirect(url_for("admin_train"))
            stamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
            dataset_path = DATASETS_DIR / f"dataset_{stamp}_{safe_name}"
            dataset_file.save(dataset_path)

        try:
            info = train_and_save_model(force=True, dataset_path=str(dataset_path) if dataset_path else None)
            flash("Model trained successfully.", "success")
        except Exception as e:
            error = str(e)
            flash("Model training failed. Check server logs.", "danger")

    try:
        bundle = load_model()
        current = {
            "version": bundle.version,
            "trained_at": bundle.trained_at,
            "metrics": bundle.metrics,
        }
    except Exception:
        current = None

    return render_template("admin_train.html", info=info, error=error, current=current)


@app.route("/api/predict", methods=["POST"])
def api_predict():
    payload = request.get_json(silent=True) or {}
    try:
        features = {
            "age": int(payload.get("age")),
            "gender": str(payload.get("gender")),
            "employment_type": str(payload.get("employment_type")),
            "monthly_income": float(payload.get("monthly_income")),
            "loan_amount": float(payload.get("loan_amount")),
            "transaction_count": int(payload.get("transaction_count", 0)),
            "avg_monthly_spend": float(payload.get("avg_monthly_spend", 0)),
            "savings_ratio": float(payload.get("savings_ratio", 0)),
            "mobile_recharge_freq": int(payload.get("mobile_recharge_freq", 0)),
            "missed_payments": int(payload.get("missed_payments", 0)),
            "credit_score": int(payload.get("credit_score")),
        }
    except Exception:
        return jsonify({"error": "Invalid payload"}), 400

    model_bundle = None
    model_version = "heuristic"
    try:
        model_bundle = load_model()
        model_version = model_bundle.version
    except Exception:
        model_bundle = None

    risk_level, confidence, probabilities = predict_risk(features, model_bundle=model_bundle)
    explanation = build_explanation(features, risk_level)

    term_months, annual_rate = suggest_repayment_plan(risk_level)
    recommended_amount = recommend_loan_amount(
        monthly_income=features["monthly_income"],
        credit_score=features["credit_score"],
        risk_level=risk_level,
        requested_loan_amount=features["loan_amount"],
    )
    emi = calculate_emi(recommended_amount, months=term_months, annual_rate=annual_rate)

    decision = "Approve" if risk_level == "Low" else "Review" if risk_level == "Medium" else "Reject"

    return jsonify(
        {
            "risk_level": risk_level,
            "confidence_score": confidence,
            "probabilities": probabilities,
            "system_recommendation": decision,
            "recommended_loan_amount": recommended_amount,
            "term_months": term_months,
            "annual_interest_rate": annual_rate,
            "estimated_emi": emi,
            "explanation": explanation,
            "model_version": model_version,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
