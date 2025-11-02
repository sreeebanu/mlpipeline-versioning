# ML Pipeline Versioning (Windows-ready)

This repository demonstrates a minimal reproducible ML pipeline with model versioning and CI (GitHub Actions). It is designed to work on Windows (PowerShell) and on GitHub Actions (including `windows-latest`).

What is included
- `src/train.py` - simple pipeline that trains a RandomForest on Iris and saves model + metrics with a semantic version.
- `src/versioning.py` - read/bump semantic version in `version.txt`.
- `tests/test_pipeline.py` - pytest that runs the pipeline and checks artifacts are created.
- `.github/workflows/ci.yml` - CI pipeline to run tests and a sample pipeline run on push/PR.

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

Notes
- For production-grade model/data versioning, integrate `dvc` or `mlflow`. This example uses a simple semantic-version file to keep the process minimal and CI-friendly.
- The GitHub Actions workflow runs tests and a sample training run. It uses a matrix with `windows-latest` and `ubuntu-latest`.

License: MIT
