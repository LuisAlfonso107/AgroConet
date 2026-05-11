import { ref } from 'vue'
import { ProductoService } from '../services/ProductoService'
import type { IProducto, IProductoForm, ProductoEstado } from '../types/IProducto'

const productos = ref<IProducto[]>([])
const selectedProducto = ref<IProducto | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)
const productoService = new ProductoService()

export function useProductoStore() {
  const loadProductos = async (productorId: number | string) => {
    loading.value = true
    error.value = null
    try {
      productos.value = await productoService.listByProductor(productorId)
    } catch {
      error.value = 'No se pudieron cargar los productos'
    } finally {
      loading.value = false
    }
  }

  const loadProducto = async (id: number | string) => {
    loading.value = true
    error.value = null
    try {
      selectedProducto.value = await productoService.getById(id)
      return selectedProducto.value
    } catch {
      error.value = 'No se pudo cargar el producto'
      return null
    } finally {
      loading.value = false
    }
  }

  const createProducto = async (payload: IProductoForm & { productor: string; productorId: number | string }) => {
    loading.value = true
    error.value = null
    try {
      const nuevo = await productoService.create({
        ...payload,
        estado: 'disponible',
        createdAt: new Date().toISOString(),
      })
      productos.value.unshift(nuevo)
      return nuevo
    } catch {
      error.value = 'No se pudo crear el producto'
      return null
    } finally {
      loading.value = false
    }
  }

  const updateProducto = async (id: number | string, payload: Partial<IProducto>) => {
    loading.value = true
    error.value = null
    try {
      const updated = await productoService.update(id, payload)
      productos.value = productos.value.map((p) => (p.id === id ? updated : p))
      selectedProducto.value = selectedProducto.value?.id === id ? updated : selectedProducto.value
      return updated
    } catch {
      error.value = 'No se pudo actualizar el producto'
      return null
    } finally {
      loading.value = false
    }
  }

  const toggleEstado = async (id: number | string, estado: ProductoEstado) => {
    return updateProducto(id, { estado } as Partial<IProducto>)
  }

  const removeProducto = async (id: number | string) => {
    loading.value = true
    error.value = null
    try {
      await productoService.remove(id)
      productos.value = productos.value.filter((p) => p.id !== id)
      return true
    } catch {
      error.value = 'No se pudo eliminar el producto'
      return false
    } finally {
      loading.value = false
    }
  }

  return {
    productos,
    selectedProducto,
    loading,
    error,
    loadProductos,
    loadProducto,
    createProducto,
    updateProducto,
    toggleEstado,
    removeProducto,
  }
}
