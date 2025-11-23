from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from ..models_loader import MODELS

router = APIRouter()

class SolucionInput(BaseModel):
    elemento: str
    categoria: str

@router.post("/predict")
def predict_solucion(payload: SolucionInput):
    model = MODELS.get('soluciones')
    if model is None:
        return {"error": "Modelo de soluciones no cargado."}

    text = (payload.elemento or "") + " " + (payload.categoria or "")
    pred = model.predict([text])[0]

    return {"solucion": pred}
