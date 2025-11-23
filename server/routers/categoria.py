from fastapi import APIRouter 
from pydantic import BaseModel 
from typing import Optional 
from ..models_loader import MODELS

router = APIRouter()

class CategoriaInput(BaseModel): 
    descripcion: str 
    sistema: Optional[str] = None 
    subsistema: Optional[str] = None

@router.post("/predict") 
def predict_categoria(payload: CategoriaInput): 
    model = MODELS.get('categoria') 
    if model is None: 
        return {"error": "Modelo de categoria no cargado."}

    text = (payload.descripcion or "") + " " + (payload.sistema or "") + " " + (payload.subsistema or "")
    pred = model.predict([text])[0]
    return {"categoria": str(pred)}