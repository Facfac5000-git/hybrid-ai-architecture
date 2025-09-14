import { Injectable } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import { firstValueFrom } from 'rxjs';
import { ConfigService } from '@nestjs/config';

@Injectable()
export class AiService {
  constructor(
    private readonly httpService: HttpService,
    private readonly configService: ConfigService
  ) {}

  async inferir(datos: any): Promise<any> {
    try {
      const aiServiceUrl = this.configService.get<string>('AI_SERVICE_URL');
      if (!aiServiceUrl) {
        throw new Error('AI_SERVICE_URL no configurada');
      }
      const respuesta = await firstValueFrom(
        this.httpService.post(aiServiceUrl, datos)
      );
      return respuesta.data;
    } catch (error) {
      console.error('Error al comunicarse con el microservicio de IA:', error);
      throw new Error('Fallo en la inferencia IA');
    }
  }
}