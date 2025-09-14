from fastapi import FastAPI
from app.api import endpoints

app = FastAPI(
    title="Edge IA Microservice",
    description="Simulación de servicio de inferencia en el edge",
    version="0.1.0",
)

app.include_router(endpoints.router, prefix="/ia", tags=["Inferencia"])

@app.get("/")
def read_root():
    return {"message": "Servicio de Edge IA activo"}
