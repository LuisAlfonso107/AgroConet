import { ref } from 'vue'
import { useApi } from './useApi'

const FALLBACK_PRODUCTOS = [
  {
    id: 1,
    nombre: 'Café Caturra Orgánico',
    region: 'Copán, Honduras',
    precio: 150,
    humedad: 12,
    calificacion: 4.8,
    imagen: 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=500&q=80'
  },
  {
    id: 2,
    nombre: 'Maíz Amarillo Premium',
    region: 'Olancho, Honduras',
    precio: 45,
    humedad: 14,
    calificacion: 4.5,
    imagen: 'https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=500&q=80'
  },
  {
    id: 3,
    nombre: 'Café Geisha Selección',
    region: 'Antigua Guatemala',
    precio: 280,
    humedad: 11,
    calificacion: 4.9,
    imagen: 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=500&q=80'
  },
  {
    id: 4,
    nombre: 'Frijol Rojo Nacional',
    region: 'Nicaragua',
    precio: 85,
    humedad: 13,
    calificacion: 4.6,
    imagen: 'https://images.unsplash.com/photo-1600490036275-35f5f1656861?w=500&q=80'
  }
]

export function useProductos() {
  const { api } = useApi()
  
  const productos = ref<any[]>([])
  const featuredProducts = ref<any[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchProductos = async (limit = 10) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/productos', {
        params: { _limit: limit }
      })
      productos.value = response.data
    } catch (err) {
      console.error('Error fetching productos:', err)
      error.value = 'Error al cargar productos'
      productos.value = []
    } finally {
      loading.value = false
    }
  }

  const fetchFeaturedProducts = async (limit = 4) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/productos', {
        params: {
          _limit: limit,
          estado: 'disponible',
          _sort: 'createdAt',
          _order: 'desc'
        }
      })
      featuredProducts.value = response.data
    } catch (err) {
      console.error('Error fetching featured products:', err)
      featuredProducts.value = FALLBACK_PRODUCTOS
    } finally {
      loading.value = false
    }
  }

  const fetchProductoById = async (id: number): Promise<any> => {
    loading.value = true
    error.value = null
    try {
      const response = await api.get(`/productos/${id}`)
      return response.data
    } catch (err) {
      console.error('Error fetching producto:', err)
      error.value = 'Error al cargar producto'
      return null
    } finally {
      loading.value = false
    }
  }

  return {
    productos,
    featuredProducts,
    loading,
    error,
    fetchProductos,
    fetchFeaturedProducts,
    fetchProductoById
  }
}
