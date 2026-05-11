import { useApi } from '../composables/useApi'
import type { ITrackingEvento } from '../types/ITracking'
import type { ITrackingService } from './ITrackingService'

export class TrackingService implements ITrackingService {
  private api = useApi().api

  async listByPedido(pedidoId: number | string): Promise<ITrackingEvento[]> {
    const response = await this.api.get<ITrackingEvento[]>('/tracking', {
      params: {
        pedidoId,
        _sort: 'updatedAt',
        _order: 'asc',
      },
    })
    return response.data
  }

  async create(payload: { pedidoId: number | string; estado: string; descripcion: string; updatedAt: string }): Promise<ITrackingEvento> {
    const response = await this.api.post<ITrackingEvento>('/tracking', payload)
    return response.data
  }
}
