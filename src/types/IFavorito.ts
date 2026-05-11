import type { Producto } from '../composables/useCatalogoProductos'

export interface IFavorito {
  id: number | string
  compradorId: number | string
  productoId: number
  createdAt: string
}

export interface IFavoritoDetalle extends IFavorito {
  producto?: Producto
}
