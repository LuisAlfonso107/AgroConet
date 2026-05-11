import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useApi } from './useApi'
import { useAuth } from './useAuth'
import type { Producto } from './useCatalogoProductos'

type ActionStatus = 'idle' | 'success' | 'error'

interface PedidoPayload {
  productoId: number
  nombreProducto: string
  compradorId: number | string
  compradorNombre: string
  productor: string
  productorId?: number | string
  cantidadQuintales: number
  precioUnitario: number
  total: number
  estado: 'solicitado'
  createdAt: string
}

interface ContactoPayload {
  productoId: number
  usuarioId: number | string
  productor: string
  mensaje: string
  estado: 'pendiente'
  createdAt: string
}

interface FavoritoPayload {
  productoId: number
  compradorId: number | string
  createdAt: string
}

const FAVORITOS_STORAGE_KEY = 'agroconet_favoritos_locales'

function readLocalFavorites(): FavoritoPayload[] {
  try {
    const rawFavorites = localStorage.getItem(FAVORITOS_STORAGE_KEY)
    return rawFavorites ? JSON.parse(rawFavorites) as FavoritoPayload[] : []
  } catch {
    return []
  }
}

function writeLocalFavorites(favoritos: FavoritoPayload[]) {
  localStorage.setItem(FAVORITOS_STORAGE_KEY, JSON.stringify(favoritos))
}

export function useMarketplaceActions(producto: () => Producto | null) {
  const router = useRouter()
  const { api } = useApi()
  const { currentUser, isAuthenticated } = useAuth()
  const loading = ref(false)
  const status = ref<ActionStatus>('idle')
  const message = ref('')
  const favoritosLocales = ref<FavoritoPayload[]>(readLocalFavorites())

  const isFavorite = computed(() => {
    const currentProducto = producto()
    const user = currentUser.value
    if (!currentProducto || !user) return false

    return favoritosLocales.value.some((favorito) => {
      return favorito.productoId === currentProducto.id && favorito.compradorId === user.id
    })
  })

  const ensureAuthenticated = () => {
    if (isAuthenticated.value) return true

    status.value = 'error'
    message.value = 'Inicia sesión para continuar con esta acción.'
    router.push('/login')
    return false
  }

  const hacerPedido = async () => {
    const currentProducto = producto()
    if (!currentProducto || !ensureAuthenticated()) return
    const user = currentUser.value
    if (!user) return

    loading.value = true
    status.value = 'idle'
    message.value = ''

    const pedido: PedidoPayload = {
      productoId: currentProducto.id,
      nombreProducto: currentProducto.nombre,
      compradorId: user.id,
      compradorNombre: user.name,
      productor: currentProducto.productor,
      productorId: currentProducto.productorId,
      cantidadQuintales: 1,
      precioUnitario: currentProducto.precio,
      total: currentProducto.precio,
      estado: 'solicitado',
      createdAt: new Date().toISOString(),
    }

    try {
      await api.post('/pedidos', pedido)
      status.value = 'success'
      message.value = 'Pedido solicitado. El productor podrá revisar la solicitud.'
    } catch {
      status.value = 'error'
      message.value = 'No se pudo guardar el pedido. Revisa que json-server esté activo.'
    } finally {
      loading.value = false
    }
  }

  const contactarProductor = async () => {
    const currentProducto = producto()
    if (!currentProducto || !ensureAuthenticated()) return
    const user = currentUser.value
    if (!user) return

    loading.value = true
    status.value = 'idle'
    message.value = ''

    const contacto: ContactoPayload = {
      productoId: currentProducto.id,
      usuarioId: user.id,
      productor: currentProducto.productor,
      mensaje: `Estoy interesado en ${currentProducto.nombre}.`,
      estado: 'pendiente',
      createdAt: new Date().toISOString(),
    }

    try {
      await api.post('/contactos', contacto)
      status.value = 'success'
      message.value = 'Mensaje enviado al productor para iniciar la conversación.'
    } catch {
      status.value = 'error'
      message.value = 'No se pudo registrar el contacto. Revisa la API mock.'
    } finally {
      loading.value = false
    }
  }

  const toggleFavorito = async () => {
    const currentProducto = producto()
    if (!currentProducto || !ensureAuthenticated()) return
    const user = currentUser.value
    if (!user) return

    const exists = isFavorite.value
    favoritosLocales.value = exists
      ? favoritosLocales.value.filter((favorito) => {
          return !(favorito.productoId === currentProducto.id && favorito.compradorId === user.id)
        })
      : [
          ...favoritosLocales.value,
          {
            productoId: currentProducto.id,
            compradorId: user.id,
            createdAt: new Date().toISOString(),
          },
        ]
    writeLocalFavorites(favoritosLocales.value)

    if (!exists) {
      await api.post('/favoritos', {
        productoId: currentProducto.id,
        compradorId: user.id,
        createdAt: new Date().toISOString(),
      }).catch(() => undefined)
    }

    status.value = 'success'
    message.value = exists ? 'Producto quitado de favoritos.' : 'Producto guardado en favoritos.'
  }

  return {
    loading,
    status,
    message,
    isFavorite,
    hacerPedido,
    contactarProductor,
    toggleFavorito,
  }
}
