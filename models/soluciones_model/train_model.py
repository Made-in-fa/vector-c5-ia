import pandas as pd
import joblib
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import json

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "soluciones_dataset.csv"
MODEL_PATH = BASE_DIR / "models" / "soluciones_model" / "model.pkl"
CONFIG_PATH = BASE_DIR / "models" / "soluciones_model" / "config.json"

def train():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    # Combinar elemento + categoría como input
    X = df["elemento"] + " " + df["categoria"]
    y = df["solucion"]

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", MultinomialNB()),
    ])

    print("Training soluciones model...")
    pipeline.fit(X, y)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)

    config = {"labels": sorted(df["solucion"].unique())}
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

    print("Training completed successfully!")

if __name__ == "__main__":
    train()
