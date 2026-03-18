import { ref, computed } from 'vue'
import type { Producto } from './useCatalogoProductos'

export interface FiltrosState {
  tipo: string
  region: string
  precioMin: number | null
  precioMax: number | null
  busqueda: string
  certificaciones: string[]
}

const TIPOS_PRODUCTO = ['cafe', 'maiz', 'frijol', 'arroz']
const REGIONES = ['Copán', 'Olancho', 'Antigua', 'Matagalpa', 'Chinandega', 'Santa Bárbara', 'Francisco Morazán', 'Guanacaste']

export function useFiltrosProductos(productos: ReturnType<typeof ref<Producto[]>>) {
  const filtros = ref<FiltrosState>({
    tipo: '',
    region: '',
    precioMin: null,
    precioMax: null,
    busqueda: '',
    certificaciones: []
  })

  const tiposDisponibles = ref(TIPOS_PRODUCTO)
  const regionesDisponibles = ref(REGIONES)

  // Opciones de certificaciones únicas de los productos
  const certificacionesDisponibles = computed(() => {
    const certs = new Set<string>()
    productos.value?.forEach(p => {
      p.certificaciones?.forEach(c => certs.add(c))
    })
    return Array.from(certs)
  })

  // Rango de precios
  const rangoPrecios = computed(() => {
    if (!productos.value?.length) return { min: 0, max: 1000 }
    const precios = productos.value.map(p => p.precio)
    return {
      min: Math.min(...precios),
      max: Math.max(...precios)
    }
  })

  // Productos filtrados
  const productosFiltrados = computed(() => {
    if (!productos.value) return []
    
    return productos.value.filter(producto => {
      // Filtro por tipo
      if (filtros.value.tipo && producto.tipo !== filtros.value.tipo) {
        return false
      }

      // Filtro por región
      if (filtros.value.region && producto.region !== filtros.value.region) {
        return false
      }

      // Filtro por rango de precio
      if (filtros.value.precioMin !== null && producto.precio < filtros.value.precioMin) {
        return false
      }
      if (filtros.value.precioMax !== null && producto.precio > filtros.value.precioMax) {
        return false
      }

      // Filtro por búsqueda
      if (filtros.value.busqueda) {
        const busqueda = filtros.value.busqueda.toLowerCase()
        const matchNombre = producto.nombre.toLowerCase().includes(busqueda)
        const matchRegion = producto.region.toLowerCase().includes(busqueda)
        const matchVariedad = producto.variedad.toLowerCase().includes(busqueda)
        const matchPais = producto.pais.toLowerCase().includes(busqueda)
        
        if (!matchNombre && !matchRegion && !matchVariedad && !matchPais) {
          return false
        }
      }

      // Filtro por certificaciones
      if (filtros.value.certificaciones.length > 0) {
        const tieneTodas = filtros.value.certificaciones.every(
          cert => producto.certificaciones?.includes(cert)
        )
        if (!tieneTodas) return false
      }

      return true
    })
  })

  // Resetear filtros
  const resetearFiltros = () => {
    filtros.value = {
      tipo: '',
      region: '',
      precioMin: null,
      precioMax: null,
      busqueda: '',
      certificaciones: []
    }
  }

  // Toggle certificación
  const toggleCertificacion = (cert: string) => {
    const index = filtros.value.certificaciones.indexOf(cert)
    if (index === -1) {
      filtros.value.certificaciones.push(cert)
    } else {
      filtros.value.certificaciones.splice(index, 1)
    }
  }

  // Verificar si hay filtros activos
  const hayFiltrosActivos = computed(() => {
    return !!(
      filtros.value.tipo ||
      filtros.value.region ||
      filtros.value.precioMin !== null ||
      filtros.value.precioMax !== null ||
      filtros.value.busqueda ||
      filtros.value.certificaciones.length > 0
    )
  })

  return {
    filtros,
    tiposDisponibles,
    regionesDisponibles,
    certificacionesDisponibles,
    rangoPrecios,
    productosFiltrados,
    resetearFiltros,
    toggleCertificacion,
    hayFiltrosActivos
  }
}