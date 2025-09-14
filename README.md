# Arquitectura Híbrida Extensible para Sistemas IA-Ready

Una implementación práctica de la arquitectura híbrida propuesta en el paper académico "Una Arquitectura Híbrida Extensible para Sistemas IA-Ready" por Facundo Leonardo Chayle.

## 🏗️ Arquitectura

### Componentes Principales

- **Orchestration Service** (NestJS): Servicio principal de orquestación y lógica de negocio
- **AI Service** (FastAPI): Microservicio especializado en procesamiento inteligente
- **Edge Agent** (FastAPI): Agente opcional para inferencia local de baja latencia
- **Redis**: Caché y comunicación asíncrona
- **Nginx**: Load balancer y reverse proxy (producción)
- **Prometheus + Grafana**: Monitoreo y métricas (opcional)

### Características Implementadas

✅ **Orquestación Dinámica**: Selección contextual entre cloud y edge  
✅ **Zero Trust AI**: Validación rigurosa de entrada/salida  
✅ **Múltiples Modelos**: Soporte para diferentes modelos de IA  
✅ **Logging Estructurado**: Trazabilidad completa con request IDs  
✅ **Health Checks**: Monitoreo de salud de servicios  
✅ **Validación Pydantic**: Schemas robustos con sanitización  
✅ **Métricas de Performance**: Tiempos de inferencia y estadísticas  

## 🚀 Inicio Rápido

### Prerrequisitos

- Docker y Docker Compose
- Node.js 18+ (para desarrollo local)
- Python 3.11+ (para desarrollo local)
- Poetry (para gestión de dependencias Python)

### Configuración

1. **Clonar el repositorio**
```bash
git clone https://github.com/Facfac5000-git/hybrid-ai-architecture.git
cd hybrid-ai-architecture
```

2. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env según necesidades
```

3. **Ejecutar con Docker Compose**

**Desarrollo (servicios básicos):**
```bash
docker-compose -f docker-compose.dev.yml up --build
```

**Producción (todos los servicios):**
```bash
docker-compose up --build
```

**Con Edge Agent:**
```bash
docker-compose --profile edge up --build
```

**Con Monitoreo:**
```bash
docker-compose --profile monitoring up --build
```

### Endpoints Principales

- **Orchestration Service**: http://localhost:3000
  - `POST /procesar-tarea` - Procesamiento de tareas
  - `GET /health` - Health check

- **AI Service**: http://localhost:8000
  - `POST /predict` - Predicción de IA
  - `GET /stats` - Estadísticas del servicio
  - `GET /models` - Modelos disponibles
  - `GET /health` - Health check

- **Edge Agent**: http://localhost:8001 (opcional)
  - `POST /predict` - Predicción edge
  - `GET /health` - Health check

## 🔧 Desarrollo Local

### AI Service (FastAPI)

```bash
cd ai_service
poetry install
poetry run uvicorn app.main:app --reload --port 8000
```

### Orchestration Service (NestJS)

```bash
cd orchestration_service
npm install
npm run start:dev
```

### Edge Agent (FastAPI)

```bash
cd edge_agent
poetry install
poetry run uvicorn app.main:app --reload --port 8001
```

## 📊 Monitoreo

### Prometheus
- URL: http://localhost:9090
- Métricas de aplicación y sistema

### Grafana
- URL: http://localhost:3001
- Usuario: admin
- Contraseña: admin123

## 🧪 Testing y Validación

### Estado Actual: ✅ ARQUITECTURA COMPLETAMENTE FUNCIONAL

La arquitectura híbrida ha sido probada exitosamente end-to-end con todos los componentes operativos.

### Comandos de Prueba Validados

#### 1. Orquestación Dinámica (Endpoint Principal)
```bash
# Procesar tarea a través del orquestador - Demuestra orquestación inteligente
curl -X POST http://localhost:3000/procesar-tarea \
  -H "Content-Type: application/json" \
  -d '{
    "entrada": "Necesito procesar esta tarea urgente",
    "contexto": "Procesamiento de alta prioridad"
  }'

# Respuesta esperada: Decisión automática entre cloud/edge con metadata completa
```

#### 2. AI Service Directo
```bash
# Predicción directa en AI Service
curl -X POST http://localhost:8000/ia/predict \
  -H "Content-Type: application/json" \
  -d '{
    "entrada": "Tarea importante para revisar",
    "modelo": "modelo_avanzado"
  }'

# Ver estadísticas del servicio
curl http://localhost:8000/ia/stats

# Listar modelos disponibles
curl http://localhost:8000/ia/models

# Health check AI Service
curl http://localhost:8000/ia/health
```

#### 3. Monitoreo y Estado
```bash
# Ver estado de contenedores
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Ver logs en tiempo real
docker logs -f hybrid-ai-architecture-orchestration-service-1
docker logs -f hybrid-ai-architecture-ai-service-1

# Verificar Redis
docker exec hybrid-ai-architecture-redis-1 redis-cli ping
```

### Ejemplo de Respuesta de Orquestación

```json
{
  "resultado": {
    "prediction": "alta",
    "model_used": "modelo_edge",
    "inference_time_ms": 9.63,
    "confidence": 0.85,
    "source": "edge"
  },
  "metadata": {
    "request_id": "req_1757893202680_o3l0k5euf",
    "motor_usado": "edge",
    "modelo_usado": "modelo_edge",
    "contexto_evaluado": {
      "latencia_requerida": 92.48,
      "edge_disponible": true,
      "carga_sistema": 0.82,
      "prioridad": "alta",
      "datos_sensibles": false
    },
    "decision_info": {
      "motor_seleccionado": "edge",
      "razon": "Baja latencia requerida. Alta carga en cloud.",
      "confianza_decision": 0.75
    }
  },
  "mensaje": "Tarea procesada con edge (modelo_edge)"
}
```

### Validación de Características

✅ **Orquestación Dinámica**: Selección automática edge vs cloud basada en contexto  
✅ **Zero Trust AI**: Validación de entrada con sanitización  
✅ **Múltiples Modelos**: 3 modelos disponibles (básico, avanzado, edge)  
✅ **Logging Estructurado**: Request IDs únicos y trazabilidad completa  
✅ **Métricas de Performance**: Tiempos de inferencia y estadísticas  
✅ **Containerización**: Docker Compose funcional con hot-reload  
✅ **API Documentation**: Swagger UI en http://localhost:8000/docs  

### Casos de Prueba Específicos

```bash
# Caso 1: Datos sensibles (debería ir a edge)
curl -X POST http://localhost:3000/procesar-tarea \
  -H "Content-Type: application/json" \
  -d '{"entrada": "Información personal confidencial", "contexto": "Datos privados"}'

# Caso 2: Baja prioridad (debería ir a edge por eficiencia)
curl -X POST http://localhost:3000/procesar-tarea \
  -H "Content-Type: application/json" \
  -d '{"entrada": "Tarea de rutina", "contexto": "Procesamiento normal"}'

# Caso 3: Alta prioridad (puede ir a cloud por recursos)
curl -X POST http://localhost:3000/procesar-tarea \
  -H "Content-Type: application/json" \
  -d '{"entrada": "Emergencia crítica urgente", "contexto": "Máxima prioridad"}'
```

## 🏛️ Arquitectura Detallada

### Flujo de Procesamiento

1. **Cliente** → `POST /procesar-tarea` → **Orchestration Service**
2. **Orchestration Service** evalúa contexto operativo
3. Decisión dinámica: **Cloud AI Service** vs **Edge Agent**
4. Procesamiento con modelo seleccionado
5. Aplicación de reglas de negocio
6. Respuesta estructurada al cliente

### Factores de Orquestación

- **Latencia requerida** (< 100ms → Edge preferido)
- **Disponibilidad de Edge** (Edge disponible/no disponible)
- **Carga del sistema Cloud** (> 80% → Edge preferido)
- **Prioridad de tarea** (Alta → Cloud, Media/Baja → Edge)
- **Datos sensibles** (Sensibles → Edge local)

### Modelos Disponibles

- `modelo_basico`: Clasificación simple de prioridad
- `modelo_avanzado`: Clasificación avanzada con más categorías
- `modelo_edge`: Optimizado para edge (rápido y eficiente)

## 🔒 Seguridad (Zero Trust AI)

- **Validación de entrada**: Sanitización y verificación de caracteres
- **Detección de datos sensibles**: Identificación automática
- **Procesamiento local**: Datos sensibles procesados en edge
- **Logging de seguridad**: Auditoría completa de decisiones
- **Límites de recursos**: Prevención de ataques DoS

## 📁 Estructura del Proyecto

```
hybrid-ai-architecture/
├── ai_service/                 # Microservicio de IA (FastAPI)
│   ├── src/app/
│   │   ├── api/endpoints.py    # Endpoints REST
│   │   ├── inference/predictor.py  # Lógica de modelos
│   │   ├── schemas/input_schema.py # Validación Pydantic
│   │   └── main.py            # Aplicación FastAPI
│   ├── Dockerfile
│   └── pyproject.toml
├── orchestration_service/      # Servicio de orquestación (NestJS)
│   ├── src/
│   │   ├── controllers/       # Controladores REST
│   │   ├── services/          # Lógica de orquestación
│   │   └── ai-client/         # Cliente HTTP para AI Service
│   ├── Dockerfile
│   └── package.json
├── edge_agent/                # Agente edge (FastAPI)
│   ├── src/app/
│   ├── Dockerfile
│   └── pyproject.toml
├── docker-compose.yml         # Configuración producción
├── docker-compose.dev.yml     # Configuración desarrollo
├── .env.example              # Variables de entorno ejemplo
└── README.md                 # Este archivo
```

## 🚧 Próximas Extensiones (Roadmap)

### Fase 1: Comunicación Asíncrona
- [ ] **WebSockets/Events**: Implementar comunicación asíncrona real-time
- [ ] **Message Queues**: Redis Pub/Sub para eventos entre servicios
- [ ] **Event-Driven Architecture**: Patrones reactivos para alta concurrencia

### Fase 2: Aprendizaje Autónomo
- [ ] **Métricas de Performance**: Sistema de evaluación continua de modelos
- [ ] **Reentrenamiento Automático**: Trigger automático basado en degradación
- [ ] **A/B Testing**: Comparación automática entre modelos
- [ ] **Feedback Loop**: Incorporación de feedback de usuarios

### Fase 3: Gobernanza Avanzada
- [ ] **Model Registry**: Versionado y lineage de modelos
- [ ] **Lifecycle Management**: Promoción automática dev→staging→prod
- [ ] **Compliance**: Auditoría y trazabilidad completa
- [ ] **Rollback**: Reversión automática ante fallos

### Fase 4: Integración ML Real
- [ ] **scikit-learn**: Integración con modelos tradicionales
- [ ] **HuggingFace**: Soporte para transformers y LLMs
- [ ] **TensorFlow/PyTorch**: Modelos de deep learning
- [ ] **MLflow**: Tracking de experimentos

### Fase 5: Observabilidad Avanzada
- [ ] **Dashboard Web**: Interfaz de monitoreo en tiempo real
- [ ] **Alertas Inteligentes**: Notificaciones basadas en anomalías
- [ ] **Performance Analytics**: Análisis predictivo de carga
- [ ] **Cost Optimization**: Optimización automática de recursos

### Comandos para Continuar Desarrollo

```bash
# Levantar arquitectura base
colima start
docker-compose -f docker-compose.dev.yml up --build -d

# Verificar estado
docker ps
curl http://localhost:3000/procesar-tarea -X POST -H "Content-Type: application/json" -d '{"entrada": "test"}'

# Desarrollo con hot-reload activo
docker logs -f hybrid-ai-architecture-orchestration-service-1
docker logs -f hybrid-ai-architecture-ai-service-1

# Parar servicios
docker-compose -f docker-compose.dev.yml down
```

## 📚 Referencias

- Paper: "Una Arquitectura Híbrida Extensible para Sistemas IA-Ready"
- Autor: Facundo Leonardo Chayle (UAI) & Antonela Tommasel (UNICEN-ISISTAN-CONICET)
- Repositorio: https://github.com/Facfac5000-git/hybrid-ai-architecture

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.