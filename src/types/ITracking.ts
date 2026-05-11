import type { PedidoEstado } from './IPedido'

export interface ITrackingEvento {
  id: number | string
  pedidoId: number | string
  estado: PedidoEstado
  descripcion: string
  updatedAt: string
}
