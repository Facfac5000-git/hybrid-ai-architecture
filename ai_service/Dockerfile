FROM python:3.12-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python directamente
RUN pip install fastapi uvicorn pydantic

# Copiar código fuente
COPY src/ ./src/

# Crear directorio de logs
RUN mkdir -p /app/logs

# Exponer puerto
EXPOSE 8000

# Variables de entorno
ENV PYTHONPATH=/app/src
ENV LOG_LEVEL=INFO

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando de inicio
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
