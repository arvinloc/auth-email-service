import joblib
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parent.parent.parent.parent / \
    "models" / "sentiment_analyzer.joblib"


pipeline = None


def get_pipeline():
    global pipeline

    if pipeline is None:
        pipeline = joblib.load(MODEL_PATH)
    return pipeline
