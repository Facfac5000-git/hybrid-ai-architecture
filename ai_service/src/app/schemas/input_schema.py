from pydantic import BaseModel, Field, validator
from typing import Optional, List
from enum import Enum

class ModelType(str, Enum):
    """Tipos de modelos disponibles"""
    BASICO = "modelo_basico"
    AVANZADO = "modelo_avanzado"
    EDGE = "modelo_edge"

class PriorityLevel(str, Enum):
    """Niveles de prioridad con tres categorías"""
    ALTA = "alta"
    MEDIA = "media"
    BAJA = "baja"

class PredictionInput(BaseModel):
    """Esquema de entrada para predicciones con validación avanzada"""
    entrada: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Texto de entrada para clasificar"
    )
    modelo: Optional[ModelType] = Field(
        default=ModelType.BASICO,
        description="Modelo a utilizar para la predicción"
    )
    contexto: Optional[dict] = Field(
        default=None,
        description="Contexto adicional para la predicción"
    )
    metadata: Optional[dict] = Field(
        default=None,
        description="Metadatos adicionales"
    )
    
    @validator('entrada')
    def validate_entrada(cls, v):
        """Validación personalizada para entrada"""
        if not v or v.isspace():
            raise ValueError('La entrada no puede estar vacía o contener solo espacios')
        
        # Sanitización básica
        v = v.strip()
        
        # Verificar caracteres peligrosos (Zero Trust AI)
        dangerous_chars = ['<', '>', '&', '"', "'"]
        if any(char in v for char in dangerous_chars):
            raise ValueError('La entrada contiene caracteres no permitidos')
        
        return v
    
    @validator('contexto')
    def validate_contexto(cls, v):
        """Validación del contexto"""
        if v is not None:
            # Validar que el contexto no sea demasiado grande
            if len(str(v)) > 500:
                raise ValueError('El contexto es demasiado grande')
        return v

class PredictionOutput(BaseModel):
    """Esquema de salida para predicciones"""
    prediction: str = Field(..., description="Resultado de la predicción")
    model_used: str = Field(..., description="Modelo utilizado")
    inference_time_ms: float = Field(..., description="Tiempo de inferencia en ms")
    confidence: float = Field(
        ..., 
        ge=0.0, 
        le=1.0, 
        description="Nivel de confianza (0-1)"
    )
    timestamp: str = Field(..., description="Timestamp de la predicción")
    
class ModelStatsOutput(BaseModel):
    """Esquema para estadísticas del modelo"""
    total_predictions: int = Field(..., description="Total de predicciones realizadas")
    model_usage: dict = Field(..., description="Uso por modelo")
    available_models: List[str] = Field(..., description="Modelos disponibles")

class HealthCheckOutput(BaseModel):
    """Esquema para health check"""
    status: str = Field(..., description="Estado del servicio")
    timestamp: str = Field(..., description="Timestamp del check")
    version: str = Field(..., description="Versión del servicio")
    models_loaded: int = Field(..., description="Número de modelos cargados")

class ErrorResponse(BaseModel):
    """Esquema para respuestas de error"""
    error: str = Field(..., description="Mensaje de error")
    error_code: str = Field(..., description="Código de error")
    timestamp: str = Field(..., description="Timestamp del error")
    request_id: Optional[str] = Field(None, description="ID de la solicitud")