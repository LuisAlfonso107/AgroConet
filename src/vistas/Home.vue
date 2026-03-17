<template>
  <div class="min-h-screen bg-crema">
    <!-- Navigation -->
   

    <!-- Hero Section -->
    <section class="relative h-screen min-h-[600px] flex items-center justify-center overflow-hidden">
      <!-- Rotating Background Images -->
      <div class="absolute inset-0">
        <img 
          v-for="(image, index) in heroImages" 
          :key="index"
          :src="image"
          :alt="'Imagen de campo ' + (index + 1)"
          class="absolute inset-0 w-full h-full object-cover transition-opacity duration-1000"
          :class="currentHeroImage === index ? 'opacity-100' : 'opacity-0'"
          loading="eager"
        />
        <!-- Overlay -->
        <div class="absolute inset-0 bg-gradient-to-b from-black/50 via-black/40 to-black/60"></div>
      </div>

      <!-- Hero Content -->
      <div class="relative z-10 text-center px-4 max-w-4xl mx-auto">
        <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-6 leading-tight drop-shadow-lg">
          Del campo directo a tu negocio o mesa
        </h1>
        <p class="text-lg md:text-xl text-gray-100 mb-8 max-w-2xl mx-auto drop-shadow-md">
          Conecta productores agrícolas con compradores honestos. Café, maíz, frijol y más – sin intermediarios innecesarios.
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <router-link 
            to="/catalogo" 
            class="px-8 py-4 bg-agro-green hover:bg-agro-green-light text-white text-lg font-semibold rounded-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
          >
            Explorar productos disponibles
          </router-link>
          <router-link 
            to="/registro?rol=productor" 
            class="px-8 py-4 bg-transparent border-2 border-white hover:bg-white/10 text-white text-lg font-semibold rounded-lg transition-all duration-300"
          >
            Soy productor – publica tu cosecha
          </router-link>
        </div>
      </div>

      <!-- Hero Indicators -->
      <div class="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex gap-2 z-10">
        <button 
          v-for="(_, index) in heroImages" 
          :key="index"
          @click="currentHeroImage = index"
          class="w-3 h-3 rounded-full transition-all duration-300"
          :class="currentHeroImage === index ? 'bg-white w-8' : 'bg-white/50'"
        />
      </div>
    </section>

    <!-- Value Cards Section -->
    <section class="py-16 md:py-24 px-4 bg-white">
      <div class="max-w-7xl mx-auto">
        <h2 class="text-3xl md:text-4xl font-bold text-center text-gray-800 mb-12">
          ¿Por qué elegir AgroConet?
        </h2>
        <div class="grid md:grid-cols-3 gap-8">
          <!-- Card 1: Para Compradores -->
          <div class="bg-crema rounded-2xl p-6 shadow-lg hover:shadow-xl transition-shadow duration-300">
            <div class="h-48 mb-4 rounded-xl overflow-hidden bg-gray-200">
              <img 
                src="https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=500&q=80" 
                alt="Tostador revisando granos"
                class="w-full h-full object-cover"
                loading="lazy"
              />
            </div>
            <h3 class="text-xl font-bold text-agro-green mb-3">Para compradores</h3>
            <p class="text-gray-600 mb-4">Encuentra granos de calidad directo de finca. Variedades, taza, humedad, certificaciones, precios transparentes. Compra por quintal o contenedor.</p>
            <router-link to="/catalogo" class="inline-flex items-center text-agro-green font-semibold hover:underline">
              Ver catálogo ahora
              <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </router-link>
          </div>

          <!-- Card 2: Para Productores -->
          <div class="bg-crema rounded-2xl p-6 shadow-lg hover:shadow-xl transition-shadow duration-300">
            <div class="h-48 mb-4 rounded-xl overflow-hidden bg-gray-200">
              <img 
                src="https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=500&q=80" 
                alt="Agricultor en finca"
                class="w-full h-full object-cover"
                loading="lazy"
              />
            </div>
            <h3 class="text-xl font-bold text-agro-green mb-3">Para productores</h3>
            <p class="text-gray-600 mb-4">Vende sin intermediarios caros. Publica tu café, maíz o frijol. Llega a tostadores, molinos y exportadores. Controla precios y condiciones.</p>
            <router-link to="/registro?rol=productor" class="inline-flex items-center text-agro-green font-semibold hover:underline">
              Comenzar a vender
              <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </router-link>
          </div>

          <!-- Card 3: Trazabilidad -->
          <div class="bg-crema rounded-2xl p-6 shadow-lg hover:shadow-xl transition-shadow duration-300">
            <div class="h-48 mb-4 rounded-xl overflow-hidden bg-gray-200">
              <img 
                src="https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=500&q=80" 
                alt="Mapa de seguimiento"
                class="w-full h-full object-cover"
                loading="lazy"
              />
            </div>
            <h3 class="text-xl font-bold text-agro-green mb-3">Trazabilidad y confianza</h3>
            <p class="text-gray-600 mb-4">Seguimiento completo + conexión real. Las agencias exportadoras actualizan estados. Sabes dónde está tu pedido o tu compra en todo momento.</p>
            <button class="inline-flex items-center text-gray-500 font-medium hover:text-agro-green">
              Cómo funciona
              <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Featured Harvests Section -->
    <section class="py-16 md:py-24 px-4 bg-gray-50">
      <div class="max-w-7xl mx-auto">
        <h2 class="text-3xl md:text-4xl font-bold text-center text-gray-800 mb-4">
          Cosechas Destacadas
        </h2>
        <p class="text-center text-gray-600 mb-12 max-w-2xl mx-auto">
          Productos frescos directamente de las fincas más confiables de la región
        </p>
        
        <div v-if="loading" class="flex justify-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-4 border-agro-green border-t-transparent"></div>
        </div>
        
        <div v-else-if="error" class="text-center py-12">
          <p class="text-red-500">{{ error }}</p>
          <button @click="fetchFeaturedProducts" class="mt-4 px-6 py-2 bg-agro-green text-white rounded-lg hover:bg-agro-green-light">
            Reintentar
          </button>
        </div>
        
        <div v-else class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <div 
            v-for="product in featuredProducts" 
            :key="product.id"
            class="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-xl transition-shadow duration-300"
          >
            <div class="h-48 bg-gray-200">
              <img 
                :src="product.imagen || 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=500&q=80'" 
                :alt="product.nombre"
                class="w-full h-full object-cover"
                loading="lazy"
              />
            </div>
            <div class="p-4">
              <h3 class="font-bold text-gray-800 mb-1 truncate">{{ product.nombre }}</h3>
              <p class="text-sm text-gray-500 mb-2">{{ product.region }}</p>
              <div class="flex items-center justify-between mb-3">
                <span class="text-lg font-bold text-agro-green">${{ product.precio }}/qq</span>
                <span v-if="product.humedad" class="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                  Humedad: {{ product.humedad }}%
                </span>
              </div>
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <span class="text-yellow-500">★</span>
                  <span class="text-sm text-gray-600 ml-1">{{ product.calificacion || '4.5' }}</span>
                </div>
                <router-link 
                  :to="'/producto/' + product.id" 
                  class="text-sm text-agro-green font-semibold hover:underline"
                >
                  Ver detalles
                </router-link>
              </div>
            </div>
          </div>
        </div>
        
        <div v-if="!loading && !error && featuredProducts.length > 0" class="text-center mt-10">
          <router-link 
            to="/catalogo" 
            class="inline-block px-8 py-3 bg-agro-green text-white font-semibold rounded-lg hover:bg-agro-green-light transition-colors"
          >
            Ver todos los productos
          </router-link>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-800 text-white py-8 px-4">
      <div class="max-w-7xl mx-auto text-center">
        <p class="text-lg font-semibold mb-2">🌾 AgroConet</p>
        <p class="text-gray-400 text-sm">Conectando el campo con el mundo</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useProductos } from '../composables/useProductos'

const { featuredProducts, loading, error, fetchFeaturedProducts } = useProductos()

const mobileMenuOpen = ref(false)

const heroImages = ref([
  'https://images.unsplash.com/photo-1524350876685-274059332603?w=1200&q=80',
  'https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1200&q=80',
  'https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=1200&q=80',
  'https://images.unsplash.com/photo-1592982537447-6f2a6a0c7c18?w=1200&q=80',
])

const currentHeroImage = ref(0)
let heroInterval = null

const startHeroRotation = () => {
  heroInterval = setInterval(() => {
    currentHeroImage.value = (currentHeroImage.value + 1) % heroImages.value.length
  }, 7000)
}

onMounted(() => {
  startHeroRotation()
  fetchFeaturedProducts()
})

onUnmounted(() => {
  if (heroInterval) {
    clearInterval(heroInterval)
  }
})
</script>

<style scoped>
.bg-crema {
  background-color: #FFF8E1;
}
</style>
