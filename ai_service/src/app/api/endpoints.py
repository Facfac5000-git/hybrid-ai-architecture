from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
import logging
import uuid
from datetime import datetime
from typing import Dict, Any

from app.schemas.input_schema import (
    PredictionInput, 
    PredictionOutput, 
    ModelStatsOutput, 
    HealthCheckOutput,
    ErrorResponse
)
from app.inference.predictor import model_service

# Configurar logging estructurado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/predict", response_model=PredictionOutput)
async def predict(input_data: PredictionInput, request: Request):
    """Endpoint principal de predicción con logging y manejo de errores"""
    request_id = str(uuid.uuid4())
    start_time = datetime.now()
    
    logger.info(f"[{request_id}] Nueva solicitud de predicción", extra={
        "request_id": request_id,
        "model_requested": input_data.modelo,
        "input_length": len(input_data.entrada),
        "client_ip": request.client.host if request.client else "unknown"
    })
    
    try:
        # Realizar predicción
        result = model_service.predict(input_data, input_data.modelo.value)
        
        # Log de éxito
        end_time = datetime.now()
        total_time = (end_time - start_time).total_seconds() * 1000
        
        logger.info(f"[{request_id}] Predicción exitosa", extra={
            "request_id": request_id,
            "model_used": result["model_used"],
            "inference_time_ms": result["inference_time_ms"],
            "total_time_ms": round(total_time, 2),
            "confidence": result["confidence"]
        })
        
        return PredictionOutput(**result)
        
    except ValueError as e:
        logger.warning(f"[{request_id}] Error de validación: {str(e)}", extra={
            "request_id": request_id,
            "error_type": "validation_error"
        })
        raise HTTPException(
            status_code=400,
            detail={
                "error": str(e),
                "error_code": "VALIDATION_ERROR",
                "request_id": request_id,
                "timestamp": datetime.now().isoformat()
            }
        )
    
    except Exception as e:
        logger.error(f"[{request_id}] Error interno: {str(e)}", extra={
            "request_id": request_id,
            "error_type": "internal_error"
        })
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Error interno del servidor",
                "error_code": "INTERNAL_ERROR",
                "request_id": request_id,
                "timestamp": datetime.now().isoformat()
            }
        )

@router.get("/stats", response_model=ModelStatsOutput)
async def get_stats():
    """Endpoint para obtener estadísticas del servicio"""
    logger.info("Solicitud de estadísticas")
    try:
        stats = model_service.get_stats()
        return ModelStatsOutput(**stats)
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {str(e)}")
        raise HTTPException(status_code=500, detail="Error obteniendo estadísticas")

@router.get("/metrics")
async def get_metrics():
    """Métricas de confianza y trigger de reentrenamiento"""
    try:
        stats = model_service.get_stats()
        retrain_needed = model_service.should_trigger_retrain()
        return {
            "confidence_metrics": stats["confidence_metrics"],
            "model_version": stats["model_version"],
            "last_retrain": stats["last_retrain"],
            "should_retrain": retrain_needed
        }
    except Exception as e:
        logger.error(f"Error obteniendo métricas: {str(e)}")
        raise HTTPException(status_code=500, detail="Error obteniendo métricas")

@router.post("/retrain")
async def retrain_model():
    """Trigger manual de reentrenamiento simulado"""
    try:
        model_service.retrain_model()
        return {"status": "ok", "message": "Modelo reentrenado", "new_version": model_service.model_version}
    except Exception as e:
        logger.error(f"Error reentrenando modelo: {str(e)}")
        raise HTTPException(status_code=500, detail="Error reentrenando modelo")

@router.get("/health", response_model=HealthCheckOutput)
async def health_check():
    """Health check endpoint"""
    try:
        available_models = model_service.get_available_models()
        return HealthCheckOutput(
            status="healthy",
            timestamp=datetime.now().isoformat(),
            version="0.1.0",
            models_loaded=len(available_models)
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthCheckOutput(
            status="unhealthy",
            timestamp=datetime.now().isoformat(),
            version="0.1.0",
            models_loaded=0
        )

@router.get("/models")
async def get_available_models():
    """Endpoint para listar modelos disponibles"""
    try:
        models = model_service.get_available_models()
        return {
            "available_models": models,
            "default_model": "modelo_basico",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error listando modelos: {str(e)}")
        raise HTTPException(status_code=500, detail="Error listando modelos")

# --- Model Governance endpoints ---

from app.inference.predictor import model_registry

@router.get("/registry")
async def list_models():
    """Lista todos los modelos en el registry"""
    return model_registry.list_models()

@router.post("/promote")
async def promote_model(name: str, version: int):
    """Promueve un modelo a active y archiva otros"""
    try:
        model_registry.promote_model(name, version)
        return {"status": "ok", "message": f"Modelo {name} v{version} promovido a active"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/archive")
async def archive_model(name: str, version: int):
    """Archiva un modelo"""
    try:
        model_registry.archive_model(name, version)
        return {"status": "ok", "message": f"Modelo {name} v{version} archivado"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/auditlog")
async def audit_log():
    """Devuelve el historial de eventos de gobernanza"""
    return model_registry.get_audit_log()

# Nota: El manejador global de excepciones debe agregarse en main.py, no en el router