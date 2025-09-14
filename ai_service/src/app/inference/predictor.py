import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class ModelService:
    """Servicio de modelos que permite múltiples modelos y selección dinámica"""
    
    def __init__(self):
        self.models = {
            "modelo_basico": self._modelo_basico,
            "modelo_avanzado": self._modelo_avanzado,
            "modelo_edge": self._modelo_edge
        }
        self.prediction_count = 0
        self.model_stats = {model: 0 for model in self.models.keys()}
        # Métricas de confianza para aprendizaje autónomo
        self.confidence_history = []
        self.last_retrain = None
        self.model_version = 1
    
    def predict(self, input_data, model_name: str = "modelo_basico") -> Dict[str, Any]:
        """Realiza predicción con el modelo especificado"""
        try:
            if model_name not in self.models:
                logger.warning(f"Modelo {model_name} no encontrado, usando modelo_basico")
                model_name = "modelo_basico"
            
            # Incrementar contadores
            self.prediction_count += 1
            self.model_stats[model_name] += 1
            
            # Ejecutar predicción
            start_time = datetime.now()
            prediction = self.models[model_name](input_data)
            end_time = datetime.now()
            
            # Calcular tiempo de inferencia
            inference_time = (end_time - start_time).total_seconds() * 1000  # en ms
            
            logger.info(f"Predicción realizada con {model_name} en {inference_time:.2f}ms")
            
            confidence = self._calculate_confidence(input_data, prediction)
            # Guardar confianza para métricas
            self.confidence_history.append(confidence)
            return {
                "prediction": prediction,
                "model_used": model_name,
                "inference_time_ms": round(inference_time, 2),
                "confidence": confidence,
                "timestamp": datetime.now().isoformat(),
                "model_version": self.model_version
            }
            
        except Exception as e:
            logger.error(f"Error en predicción con {model_name}: {str(e)}")
            raise
    
    def _modelo_basico(self, input_data) -> str:
        """Modelo básico de clasificación de prioridad"""
        entrada = input_data.entrada.lower()
        if "urgente" in entrada or "crítico" in entrada:
            return "alta"
        elif "importante" in entrada:
            return "media"
        else:
            return "baja"
    
    def _modelo_avanzado(self, input_data) -> str:
        """Modelo avanzado con tres categorías de prioridad"""
        entrada = input_data.entrada.lower()
        palabras_alta = ["emergencia", "urgente", "crítico"]
        palabras_media = ["importante", "revisar", "atención"]
        
        if any(palabra in entrada for palabra in palabras_alta):
            return "alta"
        elif any(palabra in entrada for palabra in palabras_media):
            return "media"
        else:
            return "baja"
    
    def _modelo_edge(self, input_data) -> str:
        """Modelo optimizado para edge (más simple y rápido)"""
        entrada = input_data.entrada.lower()
        if "urgente" in entrada or "crítico" in entrada:
            return "alta"
        elif "importante" in entrada:
            return "media"
        else:
            return "baja"
    
    def _calculate_confidence(self, input_data, prediction) -> float:
        """Calcula confianza simulada basada en la entrada"""
        entrada = input_data.entrada.lower()
        # Simulación simple de confianza
        if len(entrada) < 5:
            return 0.6
        elif any(word in entrada for word in ["urgente", "crítico", "importante"]):
            return 0.9
        else:
            return 0.75
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas del servicio y métricas de confianza"""
        avg_confidence = round(sum(self.confidence_history)/len(self.confidence_history), 4) if self.confidence_history else None
        min_conf = min(self.confidence_history) if self.confidence_history else None
        max_conf = max(self.confidence_history) if self.confidence_history else None
        return {
            "total_predictions": self.prediction_count,
            "model_usage": self.model_stats,
            "available_models": list(self.models.keys()),
            "model_version": self.model_version,
            "last_retrain": self.last_retrain,
            "confidence_metrics": {
                "count": len(self.confidence_history),
                "avg_confidence": avg_confidence,
                "min_confidence": min_conf,
                "max_confidence": max_conf
            }
        }

    def should_trigger_retrain(self, threshold: float = 0.75, min_samples: int = 10) -> bool:
        """Evalúa si la confianza promedio es baja y se debe reentrenar el modelo"""
        if len(self.confidence_history) < min_samples:
            return False
        avg_conf = sum(self.confidence_history)/len(self.confidence_history)
        return avg_conf < threshold

    def retrain_model(self):
        """Simula reentrenamiento y resetea historial de confianza"""
        self.model_version += 1
        self.last_retrain = datetime.now().isoformat()
        self.confidence_history.clear()
        logger.info(f"Modelo reentrenado. Nueva versión: {self.model_version}")

    
    def get_available_models(self) -> list:
        """Retorna lista de modelos disponibles"""
        return list(self.models.keys())

# --- Model Governance (Registry & Audit) ---

class ModelRegistry:
    def __init__(self):
        self.models = {}
        self.audit_log = []
        # Registrar modelos iniciales
        for name in ["modelo_basico", "modelo_avanzado", "modelo_edge"]:
            self.register_model(name, version=1, state="active" if name=="modelo_basico" else "staging")

    def register_model(self, name, version=1, state="staging"):
        key = f"{name}_v{version}"
        self.models[key] = {
            "name": name,
            "version": version,
            "state": state,
            "registered_at": datetime.now().isoformat()
        }
        self.audit_log.append({
            "event": "register",
            "model": key,
            "state": state,
            "timestamp": datetime.now().isoformat()
        })

    def promote_model(self, name, version):
        key = f"{name}_v{version}"
        if key in self.models:
            self.models[key]["state"] = "active"
            self.audit_log.append({
                "event": "promote",
                "model": key,
                "timestamp": datetime.now().isoformat()
            })
            # Archivar otros activos
            for k, v in self.models.items():
                if v["name"] == name and v["version"] != version and v["state"] == "active":
                    v["state"] = "archived"
        else:
            raise ValueError(f"Modelo {key} no encontrado")

    def archive_model(self, name, version):
        key = f"{name}_v{version}"
        if key in self.models:
            self.models[key]["state"] = "archived"
            self.audit_log.append({
                "event": "archive",
                "model": key,
                "timestamp": datetime.now().isoformat()
            })
        else:
            raise ValueError(f"Modelo {key} no encontrado")

    def list_models(self):
        return list(self.models.values())

    def get_audit_log(self):
        return self.audit_log

# Instancias globales
model_registry = ModelRegistry()
model_service = ModelService()

# Función de compatibilidad hacia atrás
def dummy_predict(input_data):
    """Función legacy para compatibilidad"""
    result = model_service.predict(input_data)
    return result["prediction"]