import joblib
from pathlib import Path

path = Path(__file__).resolve().parent


def load_model():
    model = joblib.load(f"{path}/model.pkl")
    vectorizer = joblib.load(f"{path}/vectorizer.pkl")
    return model, vectorizer
