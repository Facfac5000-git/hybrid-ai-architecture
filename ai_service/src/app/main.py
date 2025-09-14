from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.api import endpoints

app = FastAPI(
    title="AI Microservice",
    description="Microservicio de inferencia con FastAPI",
    version="0.1.0",
)

# Incluir rutas desde el archivo de endpoints
app.include_router(endpoints.router, prefix="/ia", tags=["Inferencia"])

# Para pruebas rápidas
@app.get("/")
def read_root():
    return {"message": "Servicio de IA funcionando correctamente"}