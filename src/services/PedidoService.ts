import { useApi } from '../composables/useApi'
import type { IPedidoService } from './IPedidoService'
import type { IPedidoDetalle, PedidoEstado } from '../types/IPedido'

export class PedidoService implements IPedidoService {
  private api = useApi().api

  async listByComprador(compradorId: number | string): Promise<IPedidoDetalle[]> {
    const response = await this.api.get<IPedidoDetalle[]>('/pedidos')
    return response.data
      .filter((pedido) => String(pedido.compradorId) === String(compradorId))
      .sort(sortByDateDesc)
  }

  async listByProductor(productorId: number | string): Promise<IPedidoDetalle[]> {
    const response = await this.api.get<IPedidoDetalle[]>('/pedidos')
    return response.data
      .filter((pedido) => String(pedido.productorId) === String(productorId))
      .sort(sortByDateDesc)
  }

  async getById(id: number | string): Promise<IPedidoDetalle> {
    const response = await this.api.get<IPedidoDetalle>(`/pedidos/${id}`)
    return response.data
  }

  async updateEstado(id: number | string, estado: PedidoEstado): Promise<IPedidoDetalle> {
    const response = await this.api.patch<IPedidoDetalle>(`/pedidos/${id}`, { estado })
    return response.data
  }
}

const sortByDateDesc = (a: IPedidoDetalle, b: IPedidoDetalle) => {
  return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
}
