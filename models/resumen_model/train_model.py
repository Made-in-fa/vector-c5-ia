from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
import uvicorn

# Inicializamos FastAPI
app = FastAPI(title="Resumen de Reportes Metro CDMX")

# Modelo de datos de entrada
class Reporte(BaseModel):
    texto: str

# Pipeline de resumen
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Endpoint para predecir resumen
@app.post("/api/resumen/predict")
def resumen_predict(reporte: Reporte):
    resumen = summarizer(reporte.texto, max_length=60, min_length=20, do_sample=False)
    return {"resumen": resumen[0]['summary_text'].replace("and", "y")}

# Para correr localmente
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
