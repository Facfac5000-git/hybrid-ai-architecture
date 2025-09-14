import { Controller, Post, Body } from '@nestjs/common';
import { OrchestratorService } from '../services/orchestrator.service';

@Controller()
export class TasksController {
  constructor(private readonly orchestratorService: OrchestratorService) {}

  @Post('procesar-tarea')
  async procesar(@Body() entrada: any) {
    return this.orchestratorService.procesarTarea(entrada);
  }
}