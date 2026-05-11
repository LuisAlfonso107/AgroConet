import type { IFavorito, IFavoritoDetalle } from '../types/IFavorito'

export interface IFavoritoService {
  listByComprador(compradorId: number | string): Promise<IFavoritoDetalle[]>
  remove(id: number | string): Promise<void>
  create(payload: Omit<IFavorito, 'id'>): Promise<IFavorito>
}
