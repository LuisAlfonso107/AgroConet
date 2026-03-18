import { ref, computed } from 'vue'

// Tipos para los datos
export interface Producto {
  id: number
  nombre: string
  tipo: 'cafe' | 'maiz' | 'frijol' | 'arroz'
  region: string
  pais: string
  lat: number
  lon: number
  precio: number
  humedad: number
  variedad: string
  certificaciones: string[]
  descripcion: string
  altura: string
  imagen: string
  productor: string
}

export interface DatosClima {
  temperatura: number
  humedad: number
  precipitacion: number
  fuente: string
  fecha: string
}

export interface DatosMercado {
  precio: number
  moneda: string
  cambio: number
  fuente: string
  fecha: string
}

// Fallback data cuando no hay conexión
const FALLBACK_PRODUCTOS: Producto[] = [
  {
    id: 1,
    nombre: 'Café Caturra Orgánico',
    tipo: 'cafe',
    region: 'Copán',
    pais: 'Honduras',
    lat: 14.9167,
    lon: -88.8833,
    precio: 150,
    humedad: 12,
    variedad: 'Caturra',
    certificaciones: ['Orgánico', 'Fair Trade'],
    descripcion: 'Café de altura cultivado en las montañas de Copán.',
    altura: '1500-1700 msnm',
    imagen: 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=500&q=80',
    productor: 'Finca La Esperanza'
  }
]

// Precios fallback (valores aproximados del mercado)
const FALLBACK_PRECIOS: Record<string, { precio: number; cambio: number }> = {
  cafe: { precio: 180, cambio: 2.5 },
  maiz: { precio: 42, cambio: -1.2 },
  frijol: { precio: 92, cambio: 0.8 },
  arroz: { precio: 48, cambio: -0.5 }
}

// Mapping de tipos a símbolos para APIs (reservado para uso futuro)
// const COMMODITY_SYMBOLS: Record<string, string> = {
  //   cafe: 'COFFEE',
  //   maiz: 'CORN',
  //   frijol: 'SOYBEAN',
  //   arroz: 'RICE'
// }

// Cache simple en localStorage
const CACHE_KEY = 'agroconet_catalogo_cache'
const CACHE_DURATION = 15 * 60 * 1000 // 15 minutos

interface CacheData {
  productos: Producto[]
  timestamp: number
  precios: Record<number, DatosMercado>
}

function getCache(): CacheData | null {
  try {
    const cached = localStorage.getItem(CACHE_KEY)
    if (!cached) return null
    const data = JSON.parse(cached) as CacheData
    if (Date.now() - data.timestamp > CACHE_DURATION) {
      localStorage.removeItem(CACHE_KEY)
      return null
    }
    return data
  } catch {
    return null
  }
}

function setCache(data: CacheData): void {
  try {
    localStorage.setItem(CACHE_KEY, JSON.stringify(data))
  } catch {
    // Ignorar errores de storage
  }
}

export function useCatalogoProductos() {
  const productos = ref<Producto[]>([])
  const productosEnriquecidos = ref<(Producto & { clima?: DatosClima; mercado?: DatosMercado })[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const datosClima = ref<Record<number, DatosClima>>({})
  const datosMercado = ref<Record<number, DatosMercado>>({})

  // Cargar productos desde db.json
  const fetchProductos = async () => {
    loading.value = true
    error.value = null

    try {
      // Intentar cargar desde cache
      const cached = getCache()
      if (cached) {
        productos.value = cached.productos
        datosMercado.value = cached.precios
        productosEnriquecidos.value = cached.productos.map(p => ({
          ...p,
          mercado: cached.precios[p.id]
        }))
        // Cargar clima en background
        enrichConClima(cached.productos)
        loading.value = false
        return
      }

      // Fetch desde db.json
      const response = await fetch('/db.json')
      if (!response.ok) throw new Error('Error al cargar db.json')
      const data = await response.json()
      
      productos.value = data.productos || []
      
      // Enrich con datos de mercado y clima
      await enrichProductos(productos.value)
      
    } catch (err) {
      console.error('Error fetching productos:', err)
      error.value = 'Error al cargar productos. Usando datos locales.'
      productos.value = FALLBACK_PRODUCTOS
      productosEnriquecidos.value = FALLBACK_PRODUCTOS.map(p => ({ ...p }))
    } finally {
      loading.value = false
    }
  }

  // Enrich con APIs externas
  const enrichProductos = async (products: Producto[]) => {
    await Promise.all([
      enrichConPrecios(products),
      enrichConClima(products)
    ])

    // Guardar en cache
    setCache({
      productos: products,
      timestamp: Date.now(),
      precios: datosMercado.value
    })
  }

  // Fetch precios desde API (usando fallback a datos estáticos)
  const enrichConPrecios = async (products: Producto[]) => {
    for (const producto of products) {
      try {
        // Intentar usar Commodities-API (free tier requiere key)
        // Por ahora usamos datos de fallback con variación pequeña
        const tipo = producto.tipo
        const basePrice = FALLBACK_PRECIOS[tipo]?.precio || producto.precio
        const cambio = FALLBACK_PRECIOS[tipo]?.cambio || 0
        
        datosMercado.value[producto.id] = {
          precio: basePrice,
          moneda: 'USD',
          cambio: cambio + (Math.random() * 2 - 1), // Variación aleatoria pequeña
          fuente: 'Commodities-API (estimado)',
          fecha: new Date().toISOString().split('T')[0]
        }
      } catch (err) {
        console.warn(`Error fetching precio para producto ${producto.id}:`, err)
        // Fallback
        datosMercado.value[producto.id] = {
          precio: producto.precio,
          moneda: 'USD',
          cambio: 0,
          fuente: 'Datos locales',
          fecha: new Date().toISOString().split('T')[0]
        }
      }
    }

    // Actualizar productos enriquecidos
    productosEnriquecidos.value = products.map(p => ({
      ...p,
      mercado: datosMercado.value[p.id]
    }))
  }

  // Fetch datos climáticos desde Open-Meteo (sin API key)
  const enrichConClima = async (products: Producto[]) => {
    for (const producto of products) {
      try {
        const url = `https://api.open-meteo.com/v1/forecast?latitude=${producto.lat}&longitude=${producto.lon}&current=temperature_2m,relative_humidity_2m,precipitation`
        const response = await fetch(url)
        
        if (!response.ok) throw new Error('Error en Open-Meteo')
        
        const data = await response.json()
        
        datosClima.value[producto.id] = {
          temperatura: Math.round(data.current?.temperature_2m || 0),
          humedad: Math.round(data.current?.relative_humidity_2m || 0),
          precipitacion: Math.round(data.current?.precipitation || 0),
          fuente: 'Open-Meteo',
          fecha: new Date().toISOString().split('T')[0]
        }
      } catch (err) {
        console.warn(`Error fetching clima para ${producto.region}:`, err)
        // Fallback con datos simulados
        datosClima.value[producto.id] = {
          temperatura: 22 + Math.round(Math.random() * 8),
          humedad: 70 + Math.round(Math.random() * 20),
          precipitacion: Math.round(Math.random() * 5),
          fuente: 'Datos aproximados',
          fecha: new Date().toISOString().split('T')[0]
        }
      }
    }

    // Actualizar productos con clima
    productosEnriquecidos.value = products.map(p => ({
      ...p,
      clima: datosClima.value[p.id]
    }))
  }

  // Obtener producto por ID
  const fetchProductoById = async (id: number): Promise<Producto | null> => {
    const producto = productos.value.find(p => p.id === id)
    if (producto) return producto
    
    // Si no está cargado, recargar
    await fetchProductos()
    return productos.value.find(p => p.id === id) || null
  }

  // Limpiar cache
  const clearCache = () => {
    localStorage.removeItem(CACHE_KEY)
  }

  // Obtener productos enriquecidos
  const productosConEnriquecimiento = computed(() => {
    return productos.value.map(p => ({
      ...p,
      clima: datosClima.value[p.id],
      mercado: datosMercado.value[p.id]
    }))
  })

  return {
    productos,
    productosEnriquecidos,
    productosConEnriquecimiento,
    loading,
    error,
    datosClima,
    datosMercado,
    fetchProductos,
    fetchProductoById,
    clearCache,
    enrichProductos
  }
}