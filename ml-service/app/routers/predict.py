from fastapi import APIRouter, Depends
from app.schemas.predictModel import PredictRequest, PredictResponse
from app.dependencies.dependencies import get_current_user_id
from app.core.load.model import get_pipeline

router = APIRouter()


@router.post('/predict', response_model=PredictResponse)
def predict(payload: PredictRequest, user_id: int = Depends(get_current_user_id)):
    pipeline = get_pipeline()

    prediction = pipeline.predict([payload.text])[0]

    proba = pipeline.predict_proba([payload.text])[0]

    label = 'positive' if prediction == 'positive' else 'negative'

    probaility = float(max(proba))

    return PredictResponse(
        label=label,
        proba=probaility)
