from fastapi import FastAPI 
import uvicorn 
from .routers import categoria 
from . import models_loader

app = FastAPI(title="VECTOR C5 - IA API")

app.include_router(categoria.router, prefix="/api/categoria", tags=["categoria"])

@app.on_event("startup") 
def startup_event(): models_loader.load_all()

#Para correr localmente desde project_root:
#uvicorn server.server:app --reload --port 8000

if __name__ == "__main__": 
    uvicorn.run("server.server:app", host="0.0.0.0", port=8000, reload=True)