<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 pb-20 overflow-hidden">
    <!-- Hero Section -->
    <section class="relative h-[80vh] min-h-[600px] flex items-center justify-center fade-in-section">
      <!-- Background Graphic -->
      <div class="absolute inset-0 bg-gradient-to-br from-agro-green-light/20 to-agro-naranja/20 dark:from-agro-green-dark/30 dark:to-orange-900/30"></div>
      <div class="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1595841696677-6489ff3f8cd1?auto=format&fit=crop&q=80')] bg-cover bg-center mix-blend-overlay opacity-30 dark:opacity-20 hidden md:block"></div>
      
      <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center mt-16">
        <h1 class="text-4xl md:text-6xl font-extrabold text-gray-900 dark:text-white mb-6 tracking-tight">
          Quiénes <span class="text-agro-green">Somos</span>
          <br class="hidden md:block"/>
          <span class="text-3xl md:text-5xl text-gray-700 dark:text-gray-300">Conectando el campo directo con el mundo</span>
        </h1>
        <p class="mt-4 text-xl md:text-2xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto mb-10">
          Una plataforma nacida en Centroamérica para eliminar intermediarios y dar voz a los productores reales.
        </p>
        <div class="flex flex-col sm:flex-row justify-center gap-4">
          <router-link 
            to="/catalogo"
            class="px-8 py-4 bg-gradient-to-r from-agro-green to-agro-green-light text-white font-bold rounded-xl shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300 focus:ring-4 focus:ring-agro-green/50 text-lg"
          >
            Explorar catálogo
          </router-link>
          <router-link 
            to="/registro?rol=productor"
            class="px-8 py-4 bg-white dark:bg-gray-800 text-agro-green dark:text-agro-green-light font-bold rounded-xl shadow-lg border-2 border-transparent hover:border-agro-green hover:shadow-xl hover:scale-105 transition-all duration-300 focus:ring-4 focus:ring-agro-green/50 text-lg"
          >
            Unirse como productor
          </router-link>
        </div>
      </div>
    </section>

    <!-- Misión Section -->
    <section class="py-20 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto relative fade-in-section" v-observe-visibility="onVisibility">
      <div class="bg-white/80 dark:bg-gray-800/80 backdrop-blur-md rounded-3xl p-8 md:p-12 shadow-xl text-center border border-gray-100 dark:border-gray-700">
        <div class="inline-flex items-center justify-center w-20 h-20 bg-agro-green/10 rounded-full mb-6">
          <span class="text-4xl">🤝</span>
        </div>
        <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-6">Nuestra Misión</h2>
        <p class="text-xl text-gray-600 dark:text-gray-300 leading-relaxed max-w-3xl mx-auto">
          En AgroConet creemos que el café, maíz y granos básicos deben llegar directamente del productor al comprador. Sin intermediarios innecesarios, con precios justos y trazabilidad total.
        </p>
      </div>
    </section>

    <!-- Historia Timeline Section -->
    <section class="py-20 px-4 sm:px-6 lg:px-8 max-w-6xl mx-auto fade-in-section" v-observe-visibility="onVisibility">
      <div class="text-center mb-16">
        <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-4">Nuestra Historia / Origen</h2>
        <p class="text-lg text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
          Nacimos en Honduras en 2025, inspirados en caficultores de Santa Bárbara que perdían hasta 40% de su ganancia por intermediarios. Hoy conectamos fincas de toda Centroamérica con tostadores, molinos y familias en el mundo.
        </p>
      </div>

      <!-- Timeline -->
      <div class="relative max-w-4xl mx-auto">
        <!-- Vertical Line (Mobile) / Horizontal Line (Desktop) -->
        <div class="absolute md:hidden left-1/2 transform -translate-x-1/2 h-full w-1 bg-gradient-to-b from-agro-green to-agro-naranja rounded-full"></div>
        <div class="hidden md:block absolute top-1/2 transform -translate-y-1/2 w-full h-1 bg-gradient-to-r from-agro-green to-agro-naranja rounded-full"></div>

        <div class="flex flex-col md:flex-row justify-between relative z-10 gap-12 md:gap-4">
          <!-- Hito 1 -->
          <div class="flex flex-col items-center md:w-1/3">
            <div class="w-12 h-12 bg-white dark:bg-gray-800 border-4 border-agro-green rounded-full flex items-center justify-center font-bold text-agro-green z-10 shadow-lg text-xl">💡</div>
            <div class="mt-4 md:mt-6 text-center bg-white dark:bg-gray-800 p-4 rounded-xl shadow-md w-full max-w-[250px]">
              <h3 class="font-bold text-lg text-gray-900 dark:text-white mb-1">La Idea (2025)</h3>
              <p class="text-sm text-gray-600 dark:text-gray-400">Nace AgroConet en Honduras.</p>
            </div>
          </div>

          <!-- Hito 2 -->
          <div class="flex flex-col items-center md:w-1/3">
            <div class="w-12 h-12 bg-white dark:bg-gray-800 border-4 border-agro-naranja rounded-full flex items-center justify-center font-bold text-agro-naranja z-10 shadow-lg mb-4 md:mb-0 md:mt-24 text-xl">📦</div>
            <div class="mt-0 md:-mt-48 text-center bg-white dark:bg-gray-800 p-4 rounded-xl shadow-md w-full max-w-[250px] md:order-first mb-4 md:mb-0">
              <h3 class="font-bold text-lg text-gray-900 dark:text-white mb-1">Primer Lote (2026)</h3>
              <p class="text-sm text-gray-600 dark:text-gray-400">Vendido directamente a tostadores.</p>
            </div>
          </div>

          <!-- Hito 3 -->
          <div class="flex flex-col items-center md:w-1/3">
            <div class="w-12 h-12 bg-white dark:bg-gray-800 border-4 border-agro-green-light rounded-full flex items-center justify-center font-bold text-agro-green-light z-10 shadow-lg text-xl">👥</div>
            <div class="mt-4 md:mt-6 text-center bg-white dark:bg-gray-800 p-4 rounded-xl shadow-md w-full max-w-[250px]">
              <h3 class="font-bold text-lg text-gray-900 dark:text-white mb-1">Crecimiento</h3>
              <p class="text-sm text-gray-600 dark:text-gray-400">+500 productores conectados hoy.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Valores Section -->
    <section class="py-20 px-4 sm:px-6 lg:px-8 bg-white dark:bg-gray-900 fade-in-section" v-observe-visibility="onVisibility">
      <div class="max-w-7xl mx-auto">
        <h2 class="text-3xl font-bold text-center text-gray-900 dark:text-white mb-16">Nuestros Valores Principales</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div v-for="(valor, index) in valores" :key="index" class="bg-gray-50/50 dark:bg-gray-800/50 backdrop-blur border border-gray-100 dark:border-gray-700 rounded-2xl p-8 hover:shadow-xl hover:-translate-y-2 transition-all duration-300">
            <div class="text-4xl mb-4 p-4 bg-white dark:bg-gray-700 inline-block rounded-xl shadow-sm">{{ valor.icono }}</div>
            <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3">{{ valor.titulo }}</h3>
            <p class="text-gray-600 dark:text-gray-400">{{ valor.descripcion }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Equipo Section (Opcional) -->
    <section class="py-20 px-4 sm:px-6 lg:px-8 bg-gray-50 dark:bg-gray-800/30 fade-in-section" v-observe-visibility="onVisibility">
      <div class="max-w-6xl mx-auto text-center">
         <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-12">El Equipo Detrás del Cambio</h2>
         <div class="flex flex-wrap justify-center gap-12">
            <!-- Perfil 1 -->
            <div class="flex flex-col items-center max-w-[250px]">
               <div class="w-32 h-32 rounded-full overflow-hidden bg-gray-200 dark:bg-gray-700 border-4 border-agro-green mb-4 shadow-lg shrink-0 flex items-center justify-center text-4xl">🧑‍🌾</div>
               <h3 class="text-lg font-bold text-gray-900 dark:text-white">Carlos Membreño</h3>
               <p class="text-sm text-agro-green font-medium mb-2">Fundador & Caficultor</p>
               <p class="text-sm text-gray-600 dark:text-gray-400 italic">"Caficultor de 3ª generación buscando precio justo."</p>
            </div>
            <!-- Perfil 2 -->
            <div class="flex flex-col items-center max-w-[250px]">
               <div class="w-32 h-32 rounded-full overflow-hidden bg-gray-200 dark:bg-gray-700 border-4 border-agro-naranja mb-4 shadow-lg shrink-0 flex items-center justify-center text-4xl">👩‍🔬</div>
               <h3 class="text-lg font-bold text-gray-900 dark:text-white">Ana Rivera</h3>
               <p class="text-sm text-agro-green font-medium mb-2">Co-fundadora & Tostadora</p>
               <p class="text-sm text-gray-600 dark:text-gray-400 italic">"Tostadora con 15 años de experiencia internacional."</p>
            </div>
         </div>
      </div>
    </section>

    <!-- Impacto Section -->
    <section class="py-24 px-4 sm:px-6 lg:px-8 relative fade-in-section overflow-hidden" v-observe-visibility="onImpactVisibility">
      <div class="absolute inset-0 bg-agro-green dark:bg-agro-green-dark skew-y-3 transform origin-top-left -z-10"></div>
      <div class="max-w-6xl mx-auto text-center text-white relative z-10 pt-8 pb-12">
        <h2 class="text-3xl font-bold mb-12">Impacto Actual</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="p-6">
            <div class="text-5xl font-extrabold mb-2" ref="counterProductores">+{{ displayProductores }}</div>
            <div class="text-xl opacity-90">Productores Conectados</div>
          </div>
          <div class="p-6">
            <div class="text-5xl font-extrabold mb-2" ref="counterQuintales">+{{ displayQuintales }}k</div>
            <div class="text-xl opacity-90">Quintales Vendidos</div>
          </div>
          <div class="p-6">
            <div class="text-5xl font-extrabold mb-2" ref="counterPaises">{{ displayPaises }}</div>
            <div class="text-xl opacity-90">Países Alcanzados</div>
          </div>
        </div>
        <div class="mt-12 text-sm opacity-75">Fuente: Datos propios – Marzo 2026</div>
      </div>
    </section>

    <!-- CTA Final -->
    <section class="py-24 px-4 sm:px-6 lg:px-8 text-center fade-in-section" v-observe-visibility="onVisibility">
      <div class="max-w-4xl mx-auto">
        <h2 class="text-4xl font-extrabold text-gray-900 dark:text-white mb-8">¿Listo para ser parte del cambio?</h2>
        <div class="flex flex-col sm:flex-row justify-center gap-6">
          <router-link 
            to="/catalogo"
            class="px-8 py-4 bg-gray-900 dark:bg-white text-white dark:text-gray-900 font-bold rounded-xl shadow-xl hover:scale-105 transition-all duration-300 text-lg"
          >
            Explorar productos
          </router-link>
          <router-link 
            to="/registro"
            class="px-8 py-4 bg-gradient-to-r from-agro-green to-agro-naranja text-white font-bold rounded-xl shadow-xl hover:scale-105 transition-all duration-300 text-lg"
          >
            Registrarme como productor
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const valores = [
  { icono: '🔍', titulo: 'Transparencia', descripcion: 'Precios reales y trazabilidad desde el origen hasta tu mesa.' },
  { icono: '⚖️', titulo: 'Justicia', descripcion: 'Márgenes justos garantizados directamente para los productores.' },
  { icono: '🌱', titulo: 'Sostenibilidad', descripcion: 'Apoyo constante a certificaciones orgánicas y buenas prácticas.' },
  { icono: '🤝', titulo: 'Comunidad', descripcion: 'Construimos puentes y conexión directa entre campo y mesa.' },
  { icono: '📱', titulo: 'Innovación', descripcion: 'Tecnología accesible y fácil de usar para agricultores reales.' }
]

// Animated counters state
const countProductores = ref(500)
const countQuintales = ref(120)
const countPaises = ref(15)

const displayProductores = ref(0)
const displayQuintales = ref(0)
const displayPaises = ref(0)

const animateValue = (displayRef: any, end: number, duration: number) => {
  let startTimestamp: number | null = null;
  const step = (timestamp: number) => {
    if (!startTimestamp) startTimestamp = timestamp;
    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
    // ease out quad
    const easeOutStr = 1 - (1 - progress) * (1 - progress);
    displayRef.value = Math.floor(easeOutStr * end);
    if (progress < 1) {
      window.requestAnimationFrame(step);
    } else {
      displayRef.value = end;
    }
  };
  window.requestAnimationFrame(step);
}

// Custom simple directive to handle Intersection Observer without huge libraries
const vObserveVisibility = {
  mounted: (el: HTMLElement, binding: any) => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          el.classList.add('is-visible')
          if (typeof binding.value === 'function') {
            binding.value(true)
          }
          // Optional: observer.unobserve(el) to only run once
          observer.unobserve(el)
        }
      },
      { threshold: 0.1 }
    )
    observer.observe(el)
  }
}

const onVisibility = () => {
  // simple callback, handled mostly by css .is-visible
}

const onImpactVisibility = (isVisible: boolean) => {
  if (isVisible) {
    animateValue(displayProductores, countProductores.value, 2000)
    animateValue(displayQuintales, countQuintales.value, 2000)
    animateValue(displayPaises, countPaises.value, 2000)
  }
}
</script>

<style scoped>
.fade-in-section {
  opacity: 0;
  transform: translateY(40px);
  transition: opacity 0.8s ease-out, transform 0.8s ease-out;
  will-change: opacity, visibility;
}

.fade-in-section.is-visible {
  opacity: 1;
  transform: none;
}
</style>
