# Day 56 Random Forest Deployment

This project is a simple ML deployment demo built in the `src/day56` folder.

It trains a `RandomForestClassifier` on the Iris dataset, saves the trained model with `joblib`, and serves predictions through:

- a Flask web app at `/`
- a JSON API at `/api/predict`
- a health check at `/health`

## Project files

- `app.py` - Flask web application
- `random_forest_model.py` - training, saving, loading, and prediction logic
- `templates/index.html` - web UI
- `static/style.css` - app styling
- `requirements.txt` - deployment dependencies
- `Procfile` - process command for platforms like Render

## Run locally

From the repo root:

```powershell
.venv\Scripts\python.exe src/day56/app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Test the API

```powershell
Invoke-RestMethod `
  -Uri http://127.0.0.1:5000/api/predict `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"sepal_length":5.9,"sepal_width":3.0,"petal_length":5.1,"petal_width":1.8}'
```

## Deploy publicly on Render

1. Push this repository to GitHub.
2. Create a new Render Web Service.
3. Point Render to this repo.
4. Set the Root Directory to `src/day56`.
5. Use:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
6. After deploy, Render will give you a public link.

## Temporary public link from your laptop

If you need a fast temporary demo link before hosting:

1. Run:

```powershell
.\src\day56\start_public_link.ps1
```

2. Copy the generated `https://...lhr.life` URL.

This tunnel is temporary, but it works well for quick submissions and demos.
