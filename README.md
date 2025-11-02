# ML Pipeline Versioning (Windows-ready)

This repository demonstrates a minimal reproducible ML pipeline with model versioning, CI (GitHub Actions), and model serving API (FastAPI). It is designed to work on Windows (PowerShell) and deploys freely to Render.com.

What is included
- `src/train.py` - simple pipeline that trains a RandomForest on Iris and saves model + metrics with a semantic version.
- `src/versioning.py` - read/bump semantic version in `version.txt`.
- `src/api.py` - FastAPI web service to serve model predictions (deployed on Render).
- `tests/test_pipeline.py` - pytest that runs the pipeline and checks artifacts are created.
- `.github/workflows/ci.yml` - CI pipeline to run tests and a sample pipeline run on push/PR.
- `render.yaml` - Render.com deployment configuration.

Quick start (PowerShell)

1. Create a virtual environment and activate it (PowerShell):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run tests:

```powershell
pytest -q
```

4. Run training locally (does not bump version by default):

```powershell
python .\src\train.py --output-dir artifacts
```

5. Bump patch version and save artifacts:

```powershell
python .\src\train.py --bump patch --output-dir artifacts
# then commit & push the updated version.txt and artifacts as desired
```

Deploy to Render.com (Free Tier)

1. Create a Render account and connect your GitHub repository.
2. Add a "New Web Service" in Render's dashboard:
   - Connect to your GitHub repo
   - Service name: `ml-pipeline-api` (or your choice)
   - Start Command: `uvicorn src.api:app --host 0.0.0.0 --port $PORT`
   - Environment: `Python 3`
   - Environment Variables: 
     - `PYTHONPATH`: `.`
   - Click "Create Web Service"

The service will deploy automatically. Once deployed:
- API docs: `https://<your-service>.onrender.com/docs`
- Health check: `https://<your-service>.onrender.com/`
- Make predictions:
```bash
# Example prediction request
curl -X POST https://<your-service>.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

Notes
- For production-grade model/data versioning, integrate `dvc` or `mlflow`. This example uses a simple semantic-version file to keep the process minimal and CI-friendly.
- The GitHub Actions workflow runs tests and a sample training run. It uses a matrix with `windows-latest` and `ubuntu-latest`.
- First deploy may take a few minutes as Render builds the environment and installs dependencies.
- Free tier may sleep after inactivity; first request after sleep will take longer.

License: MIT
