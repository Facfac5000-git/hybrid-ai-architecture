from pydantic import BaseModel

class PredictionInput(BaseModel):
    entrada: str
