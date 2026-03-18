<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 pt-20">
    <!-- Hero Section -->
    <section class="relative overflow-hidden py-16 sm:py-24 text-center">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 transition-all duration-1000"
           :class="mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'">
        <h1 class="text-4xl sm:text-5xl md:text-6xl font-extrabold text-gray-900 dark:text-white tracking-tight mb-6">
          Cómo Funciona <span class="text-transparent bg-clip-text bg-gradient-to-r from-agro-green to-agro-green-light">AgroConet</span><br/>
          <span class="text-3xl sm:text-4xl md:text-5xl block mt-2 text-gray-700 dark:text-gray-300">Simple, directo y transparente</span>
        </h1>
        <p class="mt-4 max-w-2xl mx-auto text-xl text-gray-600 dark:text-gray-300 mb-10">
          Del campo a tu mesa en pocos pasos. Sin intermediarios caros, con trazabilidad total.
        </p>
        <div class="flex justify-center flex-col sm:flex-row gap-4">
          <router-link to="/catalogo" class="px-8 py-4 text-lg font-bold rounded-xl text-white bg-gradient-to-r from-agro-green to-agro-green-light hover:shadow-lg hover:scale-105 transition-all duration-200">
            Explorar catálogo ahora
          </router-link>
        </div>
      </div>
    </section>

    <!-- Pasos Principales -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div class="relative">
        <div class="hidden md:block absolute left-1/2 transform -translate-x-1/2 w-1 h-full bg-agro-green/20 rounded-full"></div>
        <div class="space-y-16">
          <div v-for="(paso, index) in pasos" :key="index" 
               class="relative flex flex-col md:flex-row items-center gap-8 md:gap-16 step-animation opacity-0 cursor-default"
               :class="{'md:flex-row-reverse': index % 2 !== 0}">
            
            <!-- Step Number - Mobile Top, Desktop Center -->
            <div class="md:absolute md:left-1/2 md:-ml-6 flex items-center justify-center w-12 h-12 rounded-full bg-agro-green text-white font-bold text-xl z-10 shadow-lg">
              {{ index + 1 }}
            </div>

            <!-- Content -->
            <div class="w-full md:w-1/2 p-6 bg-white dark:bg-gray-800 rounded-2xl shadow-md border border-gray-100 dark:border-gray-700 transition-all hover:shadow-xl hover:-translate-y-1">
              <div class="flex items-center gap-4 mb-4">
                <span class="text-4xl" aria-hidden="true">{{ paso.icono }}</span>
                <h3 class="text-2xl font-bold text-gray-900 dark:text-white">{{ paso.titulo }}</h3>
              </div>
              <p class="text-gray-600 dark:text-gray-300 text-lg sm:text-base">{{ paso.descripcion }}</p>
              <div v-if="paso.accion" class="mt-6">
                <router-link :to="paso.accion.ruta" :class="paso.accion.clase" :aria-label="paso.accion.texto">
                  {{ paso.accion.texto }}
                </router-link>
              </div>
            </div>

            <!-- Illustration placeholder -->
            <div class="w-full md:w-1/2 flex justify-center p-4">
              <div class="w-full max-w-sm aspect-[4/3] rounded-2xl bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-700 dark:to-gray-800 flex items-center justify-center text-gray-400 dark:text-gray-500 shadow-inner">
                <span class="text-6xl opacity-50" aria-label="ilustración descriptiva" role="img">{{ paso.iconoPrincipal }}</span>
              </div>
            </div>

          </div>
        </div>
      </div>
    </section>

    <!-- Beneficios Clave -->
    <section class="bg-white dark:bg-gray-800 py-20 border-y border-gray-100 dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center pb-8">
        <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-12">Nuestros Beneficios</h2>
        <div class="grid grid-cols-2 md:grid-cols-5 gap-8">
          <div v-for="(beneficio, i) in beneficios" :key="i" class="flex flex-col items-center gap-3">
            <div class="w-16 h-16 flex items-center justify-center rounded-2xl bg-agro-green/10 text-agro-green text-3xl mb-2 hover:scale-110 transition-transform">
              {{ beneficio.icono }}
            </div>
            <h4 class="font-bold text-gray-900 dark:text-white">{{ beneficio.titulo }}</h4>
          </div>
        </div>
      </div>
    </section>

    <!-- FAQ -->
    <section class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
      <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-8 text-center">Preguntas Frecuentes</h2>
      <div class="space-y-4">
        <div v-for="(faq, i) in faqs" :key="i" 
             class="border border-gray-200 dark:border-gray-700 rounded-xl bg-white dark:bg-gray-800 overflow-hidden">
          <button @click="toggleFaq(i)" 
                  class="w-full px-6 py-4 flex items-center justify-between text-left focus:outline-none focus:ring-2 focus:ring-agro-green"
                  :aria-expanded="faqAbierto === i">
            <span class="font-bold text-gray-900 dark:text-white">{{ faq.pregunta }}</span>
            <span class="text-gray-500 transition-transform" :class="{'rotate-180': faqAbierto === i}" aria-hidden="true">▼</span>
          </button>
          <div v-show="faqAbierto === i" class="px-6 pb-4">
            <p class="text-gray-600 dark:text-gray-300">{{ faq.respuesta }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Final -->
    <section class="py-20 bg-gradient-to-br from-agro-green to-agro-naranja text-center px-4">
      <h2 class="text-4xl text-white font-extrabold mb-6">¿Listo para empezar?</h2>
      <p class="text-white/90 text-xl mb-10 max-w-2xl mx-auto">Únete a la mayor comunidad de agricultura directa. Regístrate en segundos.</p>
      <div class="flex justify-center flex-col sm:flex-row gap-4">
        <router-link to="/catalogo" class="px-8 py-4 text-lg font-bold rounded-xl bg-white text-agro-green hover:shadow-lg hover:scale-105 transition-all duration-200">
          Explorar catálogo
        </router-link>
        <router-link to="/registro" class="px-8 py-4 text-lg font-bold rounded-xl bg-gray-900 text-white hover:shadow-lg hover:scale-105 transition-all duration-200">
          Registrarme
        </router-link>
      </div>
    </section>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const mounted = ref(false)
const faqAbierto = ref<number | null>(null)

const toggleFaq = (index: number) => {
  faqAbierto.value = faqAbierto.value === index ? null : index
}

// Datos
const pasos = [
  {
    titulo: 'Regístrate gratis',
    descripcion: 'Crea tu cuenta en 1 minuto. Elige si eres Productor o Comprador.',
    icono: '👤',
    iconoPrincipal: '📱',
    accion: { texto: 'Registrarme', ruta: '/registro', clase: 'inline-block px-5 py-2 text-sm font-semibold rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors' }
  },
  {
    titulo: 'Publica o busca productos',
    descripcion: 'Para productores: Sube fotos reales de tu cosecha y certificaciones. Para compradores: Explora el catálogo con filtros avanzados.',
    icono: '🔍',
    iconoPrincipal: '📸'
  },
  {
    titulo: 'Conecta directamente',
    descripcion: 'Contacta al productor o comprador vía chat. Negocia precio y cantidad sin intermediarios.',
    icono: '🤝',
    iconoPrincipal: '💬'
  },
  {
    titulo: 'Gestiona tu pedido',
    descripcion: 'Crea el pedido, confirma detalles y asegura tu acuerdo fácilmente.',
    icono: '📋',
    iconoPrincipal: '📦'
  },
  {
    titulo: 'Trazabilidad completa',
    descripcion: 'Sigue tu pedido en tiempo real: desde la finca, puerto, hasta entrega. Agencias actualizan los estados.',
    icono: '📍',
    iconoPrincipal: '🗺️'
  },
  {
    titulo: 'Recibe y disfruta',
    descripcion: 'Recibe tu producto fresco. Califica la transacción y ayuda a mejorar la comunidad.',
    icono: '⭐',
    iconoPrincipal: '🚚'
  }
]

const beneficios = [
  { titulo: 'Precios justos', icono: '💰' },
  { titulo: 'Trazabilidad real', icono: '🌾' },
  { titulo: 'Sin intermediarios', icono: '🚫' },
  { titulo: 'Comunidad fuerte', icono: '🫂' },
  { titulo: 'Fácil desde celular', icono: '📲' }
]

const faqs = [
  { pregunta: '¿Es gratis registrarse?', respuesta: 'Sí, crear una cuenta y acceder al catálogo como comprador o listar tus productos como productor es totalmente gratuito.' },
  { pregunta: '¿Cómo se pagan los productos?', respuesta: 'Actualmente, el acuerdo de pago se hace directamente entre las partes usando el canal de comunicación provisto, asegurando flexibilidad y sin retenciones abusivas.' },
  { pregunta: '¿Qué hago si hay problemas?', respuesta: 'Nuestro equipo de soporte está disponible 24/7 para mediar en disputas y existe un sistema de calificación que penaliza las malas prácticas.' },
  { pregunta: '¿Funciona en zonas con internet lento?', respuesta: 'Sí. Nuestra plataforma está optimizada y construida "mobile-first" para que cargue lo más rápido posible, incluso en conexiones de baja velocidad.' }
]

onMounted(() => {
  mounted.value = true

  // Intersection Observer para Animaciones de Scroll
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.remove('opacity-0', 'translate-y-8')
        entry.target.classList.add('opacity-100', 'translate-y-0')
      }
    })
  }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' })

  document.querySelectorAll('.step-animation').forEach(el => {
    el.classList.add('translate-y-8', 'transition-all', 'duration-700', 'ease-out')
    observer.observe(el)
  })
})
</script>
