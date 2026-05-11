import type { IPedidoDetalle, PedidoEstado } from '../types/IPedido'

export interface IPedidoService {
  listByComprador(compradorId: number | string): Promise<IPedidoDetalle[]>
  listByProductor(productorId: number | string): Promise<IPedidoDetalle[]>
  getById(id: number | string): Promise<IPedidoDetalle>
  updateEstado(id: number | string, estado: PedidoEstado): Promise<IPedidoDetalle>
}
