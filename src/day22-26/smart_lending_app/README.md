# Smart Lending Optimization System

Full-stack Flask app that predicts borrower credit risk (Low/Medium/High), recommends a loan plan, and provides Admin review tools.

## Features

- User registration/login
- Loan application form (borrower + alternative data)
- Optional document upload (PDF/JPG/PNG)
- ML credit-risk prediction with confidence + basic explanations
- Loan recommendation (amount + EMI plan)
- Admin dashboard (applications, approve/reject, charts)
- Admin model training (upload CSV or use built-in dataset)
- Real-time prediction API (`POST /api/predict`)

## Quick Start (SQLite)

```bash
cd smart_lending_app
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python app.py
```

Then open `http://127.0.0.1:5000`.

### Default Admin Login

- Email: `admin@smartlending.com`
- Password: `Admin@123`

Change via environment variables:

- `ADMIN_EMAIL`
- `ADMIN_PASSWORD`

## Database

By default, the app uses SQLite: `smart_lending_app/smart_lending.db`.

To use MySQL, set `DATABASE_URL`:

```bash
set DATABASE_URL=mysql+pymysql://user:password@localhost:3306/smart_lending
```

## Model Training

- Built-in dataset: `smart_lending_app/datasets/Credit scoring Dataset.csv`
- Admin page: `/admin/train`
- Optional: set `SKLEARN_N_JOBS=-1` to speed up training (default is `1`).

If no dataset is available, training falls back to synthetic data. If ML deps are missing, prediction falls back to a rule-based heuristic.

## Real-time Prediction API

`POST /api/predict` with JSON:

```json
{
  "age": 35,
  "gender": "Male",
  "employment_type": "Salaried",
  "monthly_income": 80000,
  "loan_amount": 250000,
  "transaction_count": 120,
  "avg_monthly_spend": 42000,
  "savings_ratio": 0.25,
  "mobile_recharge_freq": 10,
  "missed_payments": 0,
  "credit_score": 740
}
```

## Notes

- Uploads are stored in `smart_lending_app/uploads/` and are only downloadable by the owner or an admin.
- If you previously created a DB with an older schema, delete the old `smart_lending.db` and restart.
