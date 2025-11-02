from typing import List
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.versioning import read_version

app = FastAPI(
    title="ML Pipeline API",
    description="Serve Iris predictions from our versioned ML pipeline",
    version="1.0.0",
)

# Load the latest model on startup
VERSION = read_version("version.txt")
try:
    model = joblib.load(f"artifacts/model_v{VERSION}.pkl")
except Exception as e:
    raise RuntimeError(f"Failed to load model version {VERSION}: {e}")


class PredictionRequest(BaseModel):
    features: List[float]

    class Config:
        schema_extra = {
            "example": {
                "features": [5.1, 3.5, 1.4, 0.2]  # Example Iris features
            }
        }


class PredictionResponse(BaseModel):
    prediction: int
    model_version: str


@app.get("/")
def read_root():
    return {
        "message": "ML Pipeline API is running",
        "model_version": VERSION,
        "docs_url": "/docs"
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    if len(request.features) != 4:
        raise HTTPException(
            status_code=400,
            detail="Expected 4 features (sepal length, sepal width, petal length, petal width)"
        )
    try:
        prediction = int(model.predict([request.features])[0])
        return PredictionResponse(
            prediction=prediction,
            model_version=VERSION
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)