import { useApi } from '../composables/useApi'
import type { IProductoService } from './IProductoService'
import type { IProducto, IProductoForm } from '../types/IProducto'

export class ProductoService implements IProductoService {
  private api = useApi().api

  async listByProductor(productorId: number | string): Promise<IProducto[]> {
    const response = await this.api.get<IProducto[]>('/productos')
    return response.data
      .filter((producto) => String(producto.productorId) === String(productorId))
      .sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime())
  }

  async getById(id: number | string): Promise<IProducto> {
    const response = await this.api.get<IProducto>(`/productos/${id}`)
    return response.data
  }

  async create(payload: IProductoForm & { productor: string; productorId: number | string; estado: string; createdAt: string }): Promise<IProducto> {
    const response = await this.api.post<IProducto>('/productos', payload)
    return response.data
  }

  async update(id: number | string, payload: Partial<IProducto>): Promise<IProducto> {
    const response = await this.api.patch<IProducto>(`/productos/${id}`, payload)
    return response.data
  }

  async remove(id: number | string): Promise<void> {
    await this.api.delete(`/productos/${id}`)
  }
}
