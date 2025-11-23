from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import openrouteservice

router = APIRouter()

# Configuración
ORS_API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImFjYmQ0YmNjZTNmYTQ1NjFhODk1ODdhZWNhYmMzMDVhIiwiaCI6Im11cm11cjY0In0="
client = openrouteservice.Client(key=ORS_API_KEY)

# Pesos fijos
ALPHA = 1.1  # peso de puntuación de categoría
BETA = 0.2   # peso del tiempo de llegada (minutos)

class Tecnico(BaseModel):
    numero_empleado: int
    puntuacion_categoria: int
    coordenadas: List[float]  # [lat, lon]

class RequestData(BaseModel):
    tecnicos: List[Tecnico]
    coordenadas_objetivo: List[float]  # [lat, lon]

def tiempo_real(origen, destino):
    """
    Devuelve tiempo en minutos usando ORS
    origen y destino: [lat, lon]
    """
    coords = [[origen[1], origen[0]], [destino[1], destino[0]]]  # ORS usa [lon, lat]
    route = client.directions(coords)
    duracion_segundos = route['routes'][0]['summary']['duration']
    return duracion_segundos / 60  # minutos

@router.post("/ranking")
def ranking_tecnicos(data: RequestData):
    resultados = []
    for t in data.tecnicos:
        tiempo = tiempo_real(t.coordenadas, data.coordenadas_objetivo)
        score = ALPHA * t.puntuacion_categoria - BETA * tiempo
        resultados.append({
            "numero_empleado": t.numero_empleado,
            "puntuacion_categoria": t.puntuacion_categoria,
            "tiempo_estimado_min": round(tiempo, 2),
            "score": round(score, 2)
        })
    
    resultados.sort(key=lambda x: x["score"], reverse=True)
    return {"ranking": resultados}
