from pathlib import Path
from typing import Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

BASE_DIR = Path(__file__).resolve().parents[3]  # Go up to backend/
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "house_price_project" / "models"

DATASET_PATH = DATA_DIR / "houses.csv"
MODEL_PATH = MODELS_DIR / "latest_model.joblib"
SCALER_PATH = MODELS_DIR / "latest_scaler.joblib"
METRICS_PATH = MODELS_DIR / "latest_metrics.json"
COLUMNS_PATH = MODELS_DIR / "columns.json"


def load_dataset():
    df = pd.read_csv(DATASET_PATH)
    return df


def build_pipeline(numeric_features):
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("regressor", LinearRegression()),
        ]
    )
    return model, numeric_features


def train_and_evaluate():
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    df = load_dataset()

    numeric_features = ["size", "bedrooms", "age"]
    target_col = "price"

    X = df[numeric_features]
    y = df[target_col]

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model, feature_names = build_pipeline(numeric_features)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_val)
    mae = float(mean_absolute_error(y_val, y_pred))
    r2 = float(r2_score(y_val, y_pred))

    # Save the complete model pipeline (includes scaler + regressor)
    joblib.dump(model, MODEL_PATH)
    
    # Extract and save the scaler separately
    # The scaler is in the preprocessor step of the pipeline
    preprocessor = model.named_steps['preprocessor']
    scaler = preprocessor.named_transformers_['num']  # Extract StandardScaler
    joblib.dump(scaler, SCALER_PATH)
    
    # Clear the model cache so new predictions use the updated model
    clear_model_cache()

    import json

    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump({"mae": mae, "r2": r2, "rows": int(len(df))}, f)

    with open(COLUMNS_PATH, "w", encoding="utf-8") as f:
        json.dump({"numeric": feature_names, "target": target_col}, f)

    return {
        "mae": mae,
        "r2": r2,
        "rows": int(len(df)),
        "model_path": str(MODEL_PATH),
        "scaler_path": str(SCALER_PATH),
    }


_MODEL_CACHE: Pipeline | None = None


def clear_model_cache():
    """Clear the cached model so it will be reloaded from disk"""
    global _MODEL_CACHE
    _MODEL_CACHE = None


def load_model():
    global _MODEL_CACHE
    if _MODEL_CACHE is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Model file not found at {MODEL_PATH}. "
                "Please train the model first by calling train_and_evaluate() or triggering training via API."
            )
        _MODEL_CACHE = joblib.load(MODEL_PATH)
    return _MODEL_CACHE


def predict_price(features):
    model = load_model()
    numeric_features = ["size", "bedrooms", "age"]
    # Convert to DataFrame (ColumnTransformer needs DataFrame, not numpy array)
    x = pd.DataFrame(
        [[float(features["size"]), float(features["bedrooms"]), float(features["age"])]],
        columns=numeric_features
    )
    pred = model.predict(x)[0]
    return float(round(pred, 2))