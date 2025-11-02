"""Simple ML pipeline: trains RandomForest on Iris, saves model + metrics with versioning.

Usage examples:
    python src/train.py --output-dir artifacts
    python src/train.py --bump patch --output-dir artifacts
"""
import argparse
import json
import os
import sys
from datetime import datetime

from joblib import dump
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from src.versioning import read_version, bump_version_file


def run_pipeline(output_dir: str, version_file: str, bump: str | None = None) -> int:
    os.makedirs(output_dir, exist_ok=True)

    # Manage version
    if bump:
        version = bump_version_file(version_file, bump)
    else:
        version = read_version(version_file)

    # Load a small dataset (Iris)
    iris = datasets.load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = float(accuracy_score(y_test, preds))

    timestamp = datetime.utcnow().isoformat() + "Z"
    model_name = f"model_v{version}.pkl"
    metrics_name = f"metrics_v{version}.json"

    model_path = os.path.join(output_dir, model_name)
    metrics_path = os.path.join(output_dir, metrics_name)

    dump(model, model_path)

    metrics = {
        "version": version,
        "accuracy": acc,
        "timestamp": timestamp,
    }
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print(f"Saved model to {model_path}")
    print(f"Saved metrics to {metrics_path}")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="artifacts")
    parser.add_argument("--version-file", default="version.txt")
    parser.add_argument("--bump", choices=["patch", "minor", "major"], help="bump semantic version")
    args = parser.parse_args(argv)

    return run_pipeline(args.output_dir, args.version_file, args.bump)


if __name__ == "__main__":
    raise SystemExit(main())
