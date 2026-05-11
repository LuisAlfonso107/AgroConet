import type { ITrackingEvento } from '../types/ITracking'

export interface ITrackingService {
  listByPedido(pedidoId: number | string): Promise<ITrackingEvento[]>
  create(payload: { pedidoId: number | string; estado: string; descripcion: string; updatedAt: string }): Promise<ITrackingEvento>
}
