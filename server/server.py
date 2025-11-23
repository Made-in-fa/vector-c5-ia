# server.py
from fastapi import FastAPI 
import uvicorn 
from .routers import categoria, resumen, tecnicos, soluciones  # <-- agregamos resumen
from . import models_loader

app = FastAPI(title="VECTOR C5 - IA API")

app.include_router(categoria.router, prefix="/api/categoria", tags=["categoria"])
app.include_router(resumen.router, prefix="/api/resumen", tags=["resumen"])  # <-- nuevo router
app.include_router(tecnicos.router, prefix="/api/tecnicos", tags=["tecnicos"])  # <-- nuevo router
app.include_router(soluciones.router, prefix="/api/soluciones", tags=["soluciones"])

@app.on_event("startup") 
def startup_event(): 
    models_loader.load_all()

if __name__ == "__main__": 
    uvicorn.run("server.server:app", host="0.0.0.0", port=8000, reload=True)
