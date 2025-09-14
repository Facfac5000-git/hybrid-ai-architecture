import { Module } from '@nestjs/common';
import { HttpModule } from '@nestjs/axios';
import { ConfigModule } from '@nestjs/config';

import { TasksController } from './controllers/tasks.controller';
import { OrchestratorService } from './services/orchestrator.service';
import { AiService } from './ai-client/ai.service';

@Module({
  imports: [HttpModule, ConfigModule.forRoot({isGlobal: true})],
  controllers: [TasksController],
  providers: [OrchestratorService, AiService],
})
export class AppModule {}