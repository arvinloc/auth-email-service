import joblib

MODEL_PATH = '../models/sentiment_analyzer.joblib'


pipeline = None

def get_pipeline():
    global pipeline

    if pipeline is None:
        pipeline = joblib.load(MODEL_PATH)
    return pipeline