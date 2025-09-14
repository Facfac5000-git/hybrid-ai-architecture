FROM node:18-alpine

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apk add --no-cache curl

# Copiar archivos de dependencias
COPY package*.json ./

# Instalar NestJS CLI globalmente y todas las dependencias (incluidas dev)
RUN npm install -g @nestjs/cli && npm ci

# Copiar código fuente
COPY src/ ./src/
COPY tsconfig*.json ./
COPY nest-cli.json ./

# Compilar TypeScript
RUN npm run build

# Exponer puerto
EXPOSE 3000

# Variables de entorno
ENV NODE_ENV=production
ENV PORT=3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# Comando de inicio
CMD ["node", "dist/main"]
