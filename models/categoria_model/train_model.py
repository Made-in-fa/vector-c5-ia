import pandas as pd
import joblib
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import json

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "categoria_dataset.csv"
MODEL_PATH = BASE_DIR / "models" / "categoria_model" / "model.pkl"
CONFIG_PATH = BASE_DIR / "models" / "categoria_model" / "config.json"


def train():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at {DATA_PATH}. Genera data/categoria_dataset.csv primero."
        )

    print(f"Loading dataset from: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)

    X = df["descripcion"]
    y = df["categoria"]

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", MultinomialNB()),
    ])

    print("Training model...")
    pipeline.fit(X, y)

    print(f"Saving model to {MODEL_PATH}")
    joblib.dump(pipeline, MODEL_PATH)

    config = {"labels": sorted(df["categoria"].unique())}
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

    print("Training completed successfully!")


if __name__ == "__main__":
    train()