<template>
  <div class="min-h-screen bg-crema pt-20 px-4 pb-8">
    <div class="max-w-5xl mx-auto">
      <!-- Loading -->
      <div v-if="loading" class="animate-pulse">
        <div class="h-8 bg-gray-200 rounded w-32 mb-4"></div>
        <div class="h-64 bg-gray-200 rounded-xl mb-6"></div>
        <div class="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
        <div class="h-4 bg-gray-200 rounded w-1/2"></div>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="bg-red-50 border-l-4 border-red-400 p-4 rounded">
        <p class="text-red-700">{{ error }}</p>
        <router-link to="/catalogo" class="text-green-600 hover:underline mt-2 inline-block">
          ← Volver al catálogo
        </router-link>
      </div>

      <!-- Producto -->
      <div v-else-if="producto">
        <!-- Back button -->
        <router-link to="/catalogo" class="text-green-600 hover:underline mb-4 inline-block">
          ← Volver al catálogo
        </router-link>

        <!-- Main content -->
        <div class="grid md:grid-cols-2 gap-6 mb-8">
          <!-- Imagen -->
          <div class="bg-white rounded-xl shadow-md overflow-hidden">
            <img
              :src="producto.imagen"
              :alt="producto.nombre"
              class="w-full h-80 object-cover"
              @error="handleImageError"
            />
          </div>

          <!-- Info principal -->
          <div class="bg-white rounded-xl shadow-md p-6">
            <!-- Badge tipo -->
            <span class="inline-block bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm capitalize mb-2">
              {{ producto.tipo }}
            </span>
            
            <h1 class="text-3xl font-bold text-gray-800 mb-2">{{ producto.nombre }}</h1>
            <p class="text-gray-600 mb-4">{{ producto.region }}, {{ producto.pais }}</p>

            <!-- Productor -->
            <div class="flex items-center gap-2 mb-4">
              <span class="text-gray-500">Productor:</span>
              <span class="font-medium text-gray-800">{{ producto.productor }}</span>
            </div>

            <!-- Precio -->
            <div class="mb-4">
              <span class="text-gray-500">Precio:</span>
              <span class="text-3xl font-bold text-green-600 ml-2">${{ producto.precio }}</span>
              <span class="text-gray-500">/quintal</span>
            </div>

            <!-- Certificaciones -->
            <div v-if="producto.certificaciones?.length" class="mb-4">
              <span class="text-gray-500 mr-2">Certificaciones:</span>
              <span
                v-for="cert in producto.certificaciones"
                :key="cert"
                class="inline-block bg-green-50 text-green-700 px-2 py-1 rounded-full text-xs mr-1"
              >
                {{ cert }}
              </span>
            </div>

            <!-- Variedad -->
            <div class="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span class="text-gray-500">Variedad:</span>
                <span class="font-medium text-gray-800 ml-1">{{ producto.variedad }}</span>
              </div>
              <div>
                <span class="text-gray-500">Humedad:</span>
                <span class="font-medium text-gray-800 ml-1">{{ producto.humedad }}%</span>
              </div>
              <div>
                <span class="text-gray-500">Altura:</span>
                <span class="font-medium text-gray-800 ml-1">{{ producto.altura }}</span>
              </div>
            </div>

            <!-- Descripción -->
            <p class="mt-4 text-gray-600">{{ producto.descripcion }}</p>

            <!-- Botones acción -->
            <div class="flex gap-3 mt-6">
              <button class="flex-1 bg-green-600 text-white py-3 rounded-lg hover:bg-green-700 transition-colors font-medium">
                Hacer pedido
              </button>
              <button class="flex-1 border-2 border-green-600 text-green-600 py-3 rounded-lg hover:bg-green-50 transition-colors font-medium">
                Contactar productor
              </button>
            </div>
          </div>
        </div>

        <!-- Sección Mercado y Clima -->
        <div class="bg-white rounded-xl shadow-md p-6 mb-8">
          <h2 class="text-xl font-bold text-gray-800 mb-4">📊 Mercado y Clima</h2>
          
          <div class="grid md:grid-cols-2 gap-6">
            <!-- Datos de Mercado -->
            <div class="bg-gradient-to-br from-green-50 to-green-100 rounded-xl p-4">
              <h3 class="font-semibold text-green-800 mb-3">💹 Precio del Commodity</h3>
              
              <div v-if="mercadoActual">
                <div class="flex justify-between items-end mb-2">
                  <span class="text-3xl font-bold text-green-700">${{ mercadoActual.precio }}</span>
                  <span class="text-sm text-gray-600">USD/quintal</span>
                </div>
                
                <div class="flex items-center gap-2 mb-2">
                  <span
                    :class="[
                      'px-2 py-1 rounded text-sm font-medium',
                      mercadoActual.cambio >= 0 ? 'bg-green-200 text-green-800' : 'bg-red-200 text-red-800'
                    ]"
                  >
                    {{ mercadoActual.cambio >= 0 ? '↑' : '↓' }}
                    {{ Math.abs(mercadoActual.cambio).toFixed(2) }}%
                  </span>
                  <span class="text-sm text-gray-600">vs día anterior</span>
                </div>
                
                <p class="text-xs text-gray-500 mt-2">
                  Fuente: {{ mercadoActual.fuente }} · {{ mercadoActual.fecha }}
                </p>
              </div>
              <div v-else class="text-gray-500">
                <p>Datos de mercado no disponibles</p>
                <p class="text-sm">Precio local: ${{ producto.precio }}/qq</p>
              </div>
            </div>

            <!-- Datos Climáticos -->
            <div class="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-4">
              <h3 class="font-semibold text-blue-800 mb-3">🌤️ Clima Local</h3>
              
              <div v-if="climaActual" class="space-y-2">
                <div class="flex justify-between">
                  <span class="text-gray-600">Temperatura actual:</span>
                  <span class="font-semibold text-gray-800">{{ climaActual.temperatura }}°C</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Humedad relativa:</span>
                  <span class="font-semibold text-gray-800">{{ climaActual.humedad }}%</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Precipitación:</span>
                  <span class="font-semibold text-gray-800">{{ climaActual.precipitacion }} mm</span>
                </div>
                
                <p class="text-xs text-gray-500 mt-3 pt-2 border-t border-blue-200">
                  Fuente: {{ climaActual.fuente }} · {{ climaActual.fecha }}
                </p>
              </div>
              <div v-else class="text-gray-500">
                <p>Datos climáticos no disponibles</p>
                <p class="text-sm">Clima típico: 22°C · 75% humedad</p>
              </div>
            </div>
          </div>

          <!-- Información adicional -->
          <div class="mt-4 p-4 bg-gray-50 rounded-lg">
            <h4 class="font-medium text-gray-700 mb-2">📈 Análisis rápido</h4>
            <p class="text-sm text-gray-600">
              <template v-if="producto.tipo === 'cafe'">
                El precio del café en los mercados internacionales muestra tendencia 
                {{ (mercadoActual?.cambio ?? 0) >= 0 ? 'al alza' : 'a la baja' }}. 
                Las condiciones climáticas en {{ producto.region }} 
                ({{ climaActual?.temperatura ?? '--' }}°C, {{ climaActual?.humedad ?? '--' }}% humedad) 
                son {{ climaActual && climaActual.humedad > 60 ? 'favorables' : 'moderadas' }} 
                para la calidad del grano.
              </template>
              <template v-else-if="producto.tipo === 'maiz'">
                El mercado de maíz presenta 
                {{ (mercadoActual?.cambio ?? 0) >= 0 ? 'incremento' : 'ligera baja' }} en precios. 
                La humedad del {{ climaActual?.humedad ?? '--' }}% en la zona es 
                {{ climaActual && climaActual.humedad > 60 ? 'adecuada' : 'baja' }} 
                para almacenamiento seguro.
              </template>
              <template v-else>
                Datos de mercado y clima actualizados para {{ producto.region }}. 
                La información ayudarte tomar decisiones informadas sobre tu compra.
              </template>
            </p>
          </div>
        </div>

        <!-- Productos relacionados (simulado) -->
        <div class="bg-white rounded-xl shadow-md p-6">
          <h2 class="text-xl font-bold text-gray-800 mb-4">Productos relacionados</h2>
          <p class="text-gray-500">Explora más productos del mismo tipo o región</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useCatalogoProductos, type DatosClima, type DatosMercado } from '../composables/useCatalogoProductos'

const route = useRoute()

const {
  productos,
  loading,
  error,
  datosClima,
  datosMercado,
  fetchProductos
} = useCatalogoProductos()

const producto = ref<any>(null)

// Computed para obtener datos específicos
const productoId = computed(() => Number(route.params.id))

const climaActual = computed((): DatosClima | null => {
  return datosClima.value[productoId.value] || null
})

const mercadoActual = computed((): DatosMercado | null => {
  return datosMercado.value[productoId.value] || null
})

// Cargar producto
onMounted(async () => {
  // Primero asegurar que tenemos los productos cargados
  if (productos.value.length === 0) {
    await fetchProductos()
  }
  
  // Buscar el producto
  producto.value = productos.value.find(p => p.id === productoId.value)
})

// Handle image error
const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.src = 'https://images.unsplash.com/photo-1620574387735-3624d75b2dbc?w=500&q=80'
}
</script>

<style scoped>
.bg-crema {
  background-color: #FFF8E1;
}
</style>