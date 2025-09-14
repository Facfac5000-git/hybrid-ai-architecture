from fastapi import APIRouter
from app.schemas.input_schema import PredictionInput
from app.inference.predictor import edge_predict

router = APIRouter()

@router.post("/predict")
def predict(input_data: PredictionInput):
    result = edge_predict(input_data)
    return {"prediction": result}
