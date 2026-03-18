<template>
  <div class="min-h-screen bg-crema pt-20 px-4 pb-8">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-800">Catálogo de Productos</h1>
        <p class="text-gray-600 mt-2">Descubre productos agrícolas de alta calidad de toda Centroamérica</p>
      </div>

      <!-- Error Banner -->
      <div v-if="error" class="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-6 rounded">
        <p class="text-yellow-700">{{ error }}</p>
        <p class="text-sm text-yellow-600 mt-1">Mostrando datos locales</p>
      </div>

      <!-- Filtros -->
      <div class="bg-white rounded-xl shadow-md p-4 mb-6">
        <!-- Busqueda -->
        <div class="mb-4">
          <input
            v-model="filtros.busqueda"
            type="text"
            placeholder="Buscar por nombre, región, variedad..."
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
          />
        </div>

        <!-- Filtros en fila -->
        <div class="flex flex-wrap gap-4">
          <!-- Tipo -->
          <select
            v-model="filtros.tipo"
            class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
          >
            <option value="">Todos los tipos</option>
            <option v-for="tipo in tiposDisponibles" :key="tipo" :value="tipo">
              {{ capitalize(tipo) }}
            </option>
          </select>

          <!-- Región -->
          <select
            v-model="filtros.region"
            class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
          >
            <option value="">Todas las regiones</option>
            <option v-for="region in regionesDisponibles" :key="region" :value="region">
              {{ region }}
            </option>
          </select>

          <!-- Rango Precio -->
          <div class="flex items-center gap-2">
            <input
              v-model.number="filtros.precioMin"
              type="number"
              placeholder="Min"
              class="w-20 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
            />
            <span class="text-gray-400">-</span>
            <input
              v-model.number="filtros.precioMax"
              type="number"
              placeholder="Max"
              class="w-20 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
            />
            <span class="text-sm text-gray-500">USD/qq</span>
          </div>

          <!-- Reset -->
          <button
            v-if="hayFiltrosActivos"
            @click="resetearFiltros"
            class="px-4 py-2 text-green-600 hover:text-green-800 transition-colors"
          >
            Limpiar filtros
          </button>
        </div>

        <!-- Certificaciones -->
        <div v-if="certificacionesDisponibles.length" class="mt-4">
          <span class="text-sm text-gray-600 mr-2">Certificaciones:</span>
          <button
            v-for="cert in certificacionesDisponibles"
            :key="cert"
            @click="toggleCertificacion(cert)"
            :class="[
              'px-3 py-1 text-xs rounded-full mr-2 transition-colors',
              filtros.certificaciones.includes(cert)
                ? 'bg-green-100 text-green-700 border border-green-300'
                : 'bg-gray-100 text-gray-600 border border-gray-200'
            ]"
          >
            {{ cert }}
          </button>
        </div>
      </div>

      <!-- Results count -->
      <div class="mb-4 text-gray-600">
        {{ productosFiltrados.length }} producto{{ productosFiltrados.length !== 1 ? 's' : '' }} encontrado{{ productosFiltrados.length !== 1 ? 's' : '' }}
      </div>

      <!-- Loading Skeleton -->
      <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <div
          v-for="i in 8"
          :key="i"
          class="bg-white rounded-xl shadow-md overflow-hidden animate-pulse"
        >
          <div class="h-48 bg-gray-200"></div>
          <div class="p-4 space-y-3">
            <div class="h-4 bg-gray-200 rounded w-3/4"></div>
            <div class="h-3 bg-gray-200 rounded w-1/2"></div>
            <div class="h-6 bg-gray-200 rounded w-1/3"></div>
          </div>
        </div>
      </div>

      <!-- Grid de Productos -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <div
          v-for="producto in productosFiltrados"
          :key="producto.id"
          class="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow cursor-pointer"
          @click="irADetalle(producto.id)"
        >
          <!-- Imagen -->
          <div class="relative h-48 bg-gray-100">
            <img
              :src="producto.imagen"
              :alt="producto.nombre"
              class="w-full h-full object-cover"
              loading="lazy"
              @error="handleImageError"
            />
            <!-- Badge tipo -->
            <span class="absolute top-2 left-2 bg-green-600 text-white text-xs px-2 py-1 rounded-full capitalize">
              {{ producto.tipo }}
            </span>
            <!-- Certificaciones -->
            <div v-if="producto.certificaciones?.length" class="absolute top-2 right-2 flex gap-1">
              <span
                v-for="cert in producto.certificaciones.slice(0, 2)"
                :key="cert"
                class="bg-white/90 text-green-700 text-xs px-2 py-0.5 rounded-full"
              >
                {{ cert }}
              </span>
            </div>
          </div>

          <!-- Info -->
          <div class="p-4">
            <h3 class="font-bold text-gray-800 mb-1 line-clamp-1">{{ producto.nombre }}</h3>
            <p class="text-sm text-gray-500 mb-2">{{ producto.region }}, {{ producto.pais }}</p>
            
            <!-- Datos de mercado (API) -->
            <div v-if="getProductoMercado(producto.id)" class="bg-green-50 rounded-lg p-2 mb-3">
              <div class="flex justify-between items-center">
                <span class="text-xs text-gray-600">Precio mercado:</span>
                <span class="text-sm font-bold text-green-700">
                  ${{ getProductoMercado(producto.id).precio }}/qq
                </span>
              </div>
              <div class="flex justify-between items-center mt-1">
                <span class="text-xs text-gray-500">{{ getProductoMercado(producto.id).fuente }}</span>
                <span
                  :class="[
                    'text-xs font-medium',
                    getProductoMercado(producto.id).cambio >= 0 ? 'text-green-600' : 'text-red-600'
                  ]"
                >
                  {{ getProductoMercado(producto.id).cambio >= 0 ? '↑' : '↓' }}
                  {{ Math.abs(getProductoMercado(producto.id).cambio).toFixed(1) }}%
                </span>
              </div>
            </div>

            <!-- Datos climáticos (API Open-Meteo) -->
            <div v-if="getProductoClima(producto.id)" class="flex items-center gap-2 text-xs text-gray-500 mb-3">
              <span>🌡️ {{ getProductoClima(producto.id).temperatura }}°C</span>
              <span>💧 {{ getProductoClima(producto.id).humedad }}%</span>
            </div>

            <!-- Info local -->
            <div class="flex justify-between items-center">
              <div>
                <span class="text-lg font-bold text-gray-800">${{ producto.precio }}</span>
                <span class="text-xs text-gray-500">/qq</span>
              </div>
              <span class="text-xs text-gray-400">Var: {{ producto.variedad }}</span>
            </div>

            <!-- Botón -->
            <button
              class="w-full mt-3 bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition-colors"
            >
              Ver detalles
            </button>
          </div>
        </div>
      </div>

      <!-- No results -->
      <div v-if="!loading && productosFiltrados.length === 0" class="text-center py-12">
        <p class="text-gray-500 text-lg">No se encontraron productos con los filtros seleccionados</p>
        <button
          @click="resetearFiltros"
          class="mt-4 text-green-600 hover:text-green-800"
        >
          Limpiar filtros
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCatalogoProductos } from '../composables/useCatalogoProductos'
import { useFiltrosProductos } from '../composables/useFiltrosProductos'

const router = useRouter()

const {
  productos,
  loading,
  error,
  datosClima,
  datosMercado,
  fetchProductos
} = useCatalogoProductos()

// Usar filtros
const { 
  filtros, 
  tiposDisponibles, 
  regionesDisponibles,
  certificacionesDisponibles,
  productosFiltrados,
  resetearFiltros,
  toggleCertificacion,
  hayFiltrosActivos
} = useFiltrosProductos(productos)

// Helper functions
const capitalize = (s: string) => s.charAt(0).toUpperCase() + s.slice(1)

const getProductoMercado = (id: number) => datosMercado.value[id]
const getProductoClima = (id: number) => datosClima.value[id]

const irADetalle = (id: number) => {
  router.push(`/producto/${id}`)
}

// Handle image error
const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.src = 'https://images.unsplash.com/photo-1620574387735-3624d75b2dbc?w=500&q=80'
}

// Cargar datos al montar
onMounted(() => {
  fetchProductos()
})
</script>

<style scoped>
.bg-crema {
  background-color: #FFF8E1;
}

.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>