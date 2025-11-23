# routers/resumen.py
from fastapi import APIRouter
from pydantic import BaseModel
from transformers import pipeline

router = APIRouter()
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Modelo de datos para el POST
class Reporte(BaseModel):
    texto: str

@router.post("/predict")
def resumen_predict(reporte: Reporte):
    """
    Recibe un reporte y devuelve un resumen breve en JSON.
    """
    resumen = summarizer(reporte.texto, max_length=60, min_length=20, do_sample=False)
    return {"resumen": resumen[0]['summary_text']}
