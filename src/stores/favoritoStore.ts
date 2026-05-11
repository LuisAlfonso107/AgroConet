import { ref } from 'vue'
import { FavoritoService } from '../services/FavoritoService'
import type { IFavoritoDetalle } from '../types/IFavorito'

const favoritos = ref<IFavoritoDetalle[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const favoritoService = new FavoritoService()

export function useFavoritoStore() {
  const loadFavoritos = async (compradorId: number | string) => {
    loading.value = true
    error.value = null
    try {
      favoritos.value = await favoritoService.listByComprador(compradorId)
    } catch {
      error.value = 'No se pudieron cargar los favoritos'
    } finally {
      loading.value = false
    }
  }

  const removeFavorito = async (id: number | string) => {
    await favoritoService.remove(id)
    favoritos.value = favoritos.value.filter((favorito) => favorito.id !== id)
  }

  return {
    favoritos,
    loading,
    error,
    loadFavoritos,
    removeFavorito,
  }
}
