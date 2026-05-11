import type { IProducto, IProductoForm } from '../types/IProducto'

export interface IProductoService {
  listByProductor(productorId: number | string): Promise<IProducto[]>
  getById(id: number | string): Promise<IProducto>
  create(payload: IProductoForm & { productor: string; productorId: number | string; estado: string; createdAt: string }): Promise<IProducto>
  update(id: number | string, payload: Partial<IProducto>): Promise<IProducto>
  remove(id: number | string): Promise<void>
}
