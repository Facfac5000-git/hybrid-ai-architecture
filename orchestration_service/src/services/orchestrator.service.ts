import { Injectable, Logger } from '@nestjs/common';
import { AiService } from '../ai-client/ai.service';

interface ContextoOperativo {
  latencia_requerida: number; // ms
  edge_disponible: boolean;
  carga_sistema: number; // 0-1
  prioridad: 'alta' | 'media' | 'baja';
  ubicacion: 'local' | 'remoto';
  datos_sensibles: boolean;
}

interface DecisionOrquestacion {
  motor_seleccionado: 'cloud' | 'edge';
  modelo_recomendado: string;
  razon: string;
  confianza_decision: number;
}

@Injectable()
export class OrchestratorService {
  private readonly logger = new Logger(OrchestratorService.name);
  private readonly LATENCIA_LIMITE_EDGE = 100; // ms
  private readonly CARGA_LIMITE_CLOUD = 0.8;
  
  constructor(private readonly aiService: AiService) {}

  async procesarTarea(datos: any): Promise<any> {
    const requestId = this.generarRequestId();
    const startTime = Date.now();
    
    this.logger.log(`[${requestId}] Iniciando procesamiento de tarea`);
    
    try {
      // 1. Obtener contexto operativo
      const contexto = await this.obtenerContexto(datos);
      
      // 2. Aplicar orquestación dinámica (CORE del paper)
      const decision = this.seleccionarMotorIA(datos, contexto);
      
      this.logger.log(`[${requestId}] Motor seleccionado: ${decision.motor_seleccionado} - ${decision.razon}`);
      
      // 3. Ejecutar inferencia según decisión
      let resultadoIA;
      if (decision.motor_seleccionado === 'edge') {
        resultadoIA = await this.ejecutarEnEdge(datos, decision.modelo_recomendado);
      } else {
        resultadoIA = await this.ejecutarEnCloud(datos, decision.modelo_recomendado);
      }
      
      // 4. Aplicar reglas de negocio post-inferencia
      const resultadoFinal = await this.aplicarReglasNegocio(resultadoIA, contexto);
      
      const endTime = Date.now();
      const totalTime = endTime - startTime;
      
      this.logger.log(`[${requestId}] Tarea completada en ${totalTime}ms`);
      
      return {
        resultado: resultadoFinal,
        metadata: {
          request_id: requestId,
          motor_usado: decision.motor_seleccionado,
          modelo_usado: decision.modelo_recomendado,
          tiempo_total_ms: totalTime,
          contexto_evaluado: contexto,
          decision_info: decision
        },
        mensaje: `Tarea procesada con ${decision.motor_seleccionado} (${decision.modelo_recomendado})`
      };
      
    } catch (error) {
      this.logger.error(`[${requestId}] Error procesando tarea: ${error.message}`);
      throw error;
    }
  }

  /**
   * CORE: Implementación del algoritmo de orquestación dinámica del paper
   * Replica el pseudocódigo: seleccionar_motor_ia(entrada, contexto)
   */
  private seleccionarMotorIA(entrada: any, contexto: ContextoOperativo): DecisionOrquestacion {
    let puntuacionEdge = 0;
    let puntuacionCloud = 0;
    let razon = '';
    
    // Factor 1: Latencia (crítico para edge)
    if (contexto.latencia_requerida < this.LATENCIA_LIMITE_EDGE) {
      puntuacionEdge += 30;
      razon += 'Baja latencia requerida. ';
    } else {
      puntuacionCloud += 20;
    }
    
    // Factor 2: Disponibilidad del edge
    if (contexto.edge_disponible) {
      puntuacionEdge += 25;
    } else {
      puntuacionCloud += 40;
      razon += 'Edge no disponible. ';
    }
    
    // Factor 3: Carga del sistema cloud
    if (contexto.carga_sistema > this.CARGA_LIMITE_CLOUD) {
      puntuacionEdge += 20;
      razon += 'Alta carga en cloud. ';
    } else {
      puntuacionCloud += 15;
    }
    
    // Factor 4: Prioridad de la tarea
    if (contexto.prioridad === 'alta') {
      puntuacionCloud += 25; // Cloud para alta prioridad (más recursos)
    } else {
      puntuacionEdge += 10;
    }
    
    // Factor 5: Datos sensibles (Zero Trust AI)
    if (contexto.datos_sensibles && contexto.ubicacion === 'local') {
      puntuacionEdge += 35;
      razon += 'Datos sensibles, procesamiento local. ';
    }
    
    // Decisión final
    const motorSeleccionado = puntuacionEdge > puntuacionCloud ? 'edge' : 'cloud';
    const modeloRecomendado = this.seleccionarModelo(motorSeleccionado, contexto);
    const confianza = Math.max(puntuacionEdge, puntuacionCloud) / 100;
    
    if (!razon) {
      razon = motorSeleccionado === 'edge' ? 
        'Condiciones favorables para edge' : 
        'Condiciones favorables para cloud';
    }
    
    return {
      motor_seleccionado: motorSeleccionado,
      modelo_recomendado: modeloRecomendado,
      razon: razon.trim(),
      confianza_decision: Math.min(confianza, 1.0)
    };
  }
  
  private seleccionarModelo(motor: 'cloud' | 'edge', contexto: ContextoOperativo): string {
    if (motor === 'edge') {
      return 'modelo_edge'; // Modelo optimizado para edge
    }
    
    // Para cloud, seleccionar según prioridad
    switch (contexto.prioridad) {
      case 'alta':
        return 'modelo_avanzado';
      case 'media':
        return 'modelo_basico';
      default:
        return 'modelo_basico';
    }
  }
  
  private async obtenerContexto(datos: any): Promise<ContextoOperativo> {
    // Simulación de obtención de contexto operativo
    // En producción, esto vendría de métricas reales, monitoreo, etc.
    
    const latenciaSimulada = Math.random() * 200; // 0-200ms
    const cargaSimulada = Math.random(); // 0-1
    const edgeDisponible = Math.random() > 0.3; // 70% disponibilidad
    
    // Detectar prioridad desde los datos
    let prioridad: 'alta' | 'media' | 'baja' = 'baja';
    if (datos.entrada && typeof datos.entrada === 'string') {
      const entrada = datos.entrada.toLowerCase();
      if (entrada.includes('urgente') || entrada.includes('crítico')) {
        prioridad = 'alta';
      } else if (entrada.includes('importante')) {
        prioridad = 'media';
      }
    }
    
    // Detectar datos sensibles (Zero Trust AI)
    const datosSensibles = this.detectarDatosSensibles(datos);
    
    return {
      latencia_requerida: latenciaSimulada,
      edge_disponible: edgeDisponible,
      carga_sistema: cargaSimulada,
      prioridad,
      ubicacion: 'remoto', // Por defecto remoto
      datos_sensibles: datosSensibles
    };
  }
  
  private detectarDatosSensibles(datos: any): boolean {
    // Implementación básica de detección de datos sensibles
    if (datos.entrada && typeof datos.entrada === 'string') {
      const entrada = datos.entrada.toLowerCase();
      const palabrasSensibles = ['personal', 'privado', 'confidencial', 'secreto', 'dni', 'cuit'];
      return palabrasSensibles.some(palabra => entrada.includes(palabra));
    }
    return false;
  }
  
  private async ejecutarEnEdge(datos: any, modelo: string): Promise<any> {
    // TODO: Implementar cliente para edge agent
    this.logger.log(`Ejecutando en edge con modelo: ${modelo}`);
    
    // Por ahora, simulamos respuesta del edge
    return {
      prediction: 'edge_result',
      model_used: modelo,
      inference_time_ms: Math.random() * 50, // Edge más rápido
      confidence: 0.85,
      source: 'edge'
    };
  }
  
  private async ejecutarEnCloud(datos: any, modelo: string): Promise<any> {
    // Usar el servicio AI existente
    const payload = {
      entrada: datos.entrada,
      modelo: modelo
    };
    
    const resultado = await this.aiService.inferir(payload);
    resultado.source = 'cloud';
    return resultado;
  }
  
  private async aplicarReglasNegocio(resultadoIA: any, contexto: ContextoOperativo): Promise<any> {
    // Aplicar reglas de negocio específicas del dominio
    let resultadoFinal = { ...resultadoIA };
    
    // Ejemplo: Validación adicional para datos sensibles
    if (contexto.datos_sensibles) {
      resultadoFinal.security_validated = true;
      resultadoFinal.processing_location = 'secure_environment';
    }
    
    // Ejemplo: Ajuste de confianza según contexto
    if (contexto.prioridad === 'alta' && resultadoFinal.confidence < 0.8) {
      resultadoFinal.requires_human_review = true;
    }
    
    return resultadoFinal;
  }
  
  private generarRequestId(): string {
    return `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}