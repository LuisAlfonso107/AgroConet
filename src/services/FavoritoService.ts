import { useApi } from '../composables/useApi'
import type { Producto } from '../composables/useCatalogoProductos'
import type { IFavorito, IFavoritoDetalle } from '../types/IFavorito'
import type { IFavoritoService } from './IFavoritoService'

export class FavoritoService implements IFavoritoService {
  private api = useApi().api

  async listByComprador(compradorId: number | string): Promise<IFavoritoDetalle[]> {
    const [favoritosResponse, productosResponse] = await Promise.all([
      this.api.get<IFavorito[]>('/favoritos'),
      this.api.get<Producto[]>('/productos'),
    ])
    const productos = new Map(productosResponse.data.map((producto) => [String(producto.id), producto]))

    return favoritosResponse.data
      .filter((favorito) => String(favorito.compradorId) === String(compradorId))
      .map((favorito) => ({
        ...favorito,
        producto: productos.get(String(favorito.productoId)),
      }))
  }

  async remove(id: number | string): Promise<void> {
    await this.api.delete(`/favoritos/${id}`)
  }

  async create(payload: Omit<IFavorito, 'id'>): Promise<IFavorito> {
    const response = await this.api.post<IFavorito>('/favoritos', payload)
    return response.data
  }
}
