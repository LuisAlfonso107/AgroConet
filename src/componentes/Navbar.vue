<template>
  <header class="fixed top-0 left-0 right-0 z-50 transition-all duration-300"
    :class="[
      scrolled 
        ? 'bg-white/90 dark:bg-gray-900/90 backdrop-blur-md shadow-sm py-3' 
        : 'bg-transparent py-4'
    ]">
    <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16 md:h-20">
        <!-- Logo -->
        <router-link 
          to="/" 
          class="flex items-center gap-2 text-xl md:text-2xl font-bold text-agro-green hover:scale-105 transition-transform duration-200"
          aria-label="AgroConet - Inicio"
        >
          <span class="text-2xl md:text-3xl">🌾</span>
          <span class="bg-gradient-to-r from-agro-green to-agro-green-light bg-clip-text text-transparent">
            AgroConet
          </span>
        </router-link>

        <!-- Desktop Navigation -->
        <div class="hidden md:flex items-center gap-8">
        
          <a 
            href="#como-funciona" 
            class="text-gray-700 dark:text-gray-200 hover:text-agro-green hover:scale-105 transition-all duration-200 font-medium"
          >
            Cómo funciona
          </a>
          <a 
            href="https://wa.me/1234567890" 
            target="_blank"
            rel="noopener noreferrer"
            class="text-gray-700 dark:text-gray-200 hover:text-agro-green hover:scale-105 transition-all duration-200 font-medium"
          >
            Contacto
          </a>
        </div>

        <!-- Desktop Actions -->
        <div class="hidden md:flex items-center gap-3">
          <router-link 
            to="/catalogo"
            class="px-4 py-2 bg-gradient-to-r from-agro-green to-agro-green-light text-white font-medium rounded-lg
                   hover:shadow-lg hover:scale-105 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-agro-green focus:ring-offset-2"
          >
            Explorar catálogo
          </router-link>
          <router-link 
            to="/login"
            class="px-4 py-2 text-agro-green font-medium rounded-lg border-2 border-agro-green
                   hover:bg-agro-green/10 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-agro-green focus:ring-offset-2"
          >
            Iniciar sesión
          </router-link>
          <router-link 
            to="/registro"
            class="px-4 py-2 bg-gradient-to-r from-agro-green to-agro-naranja text-white font-medium rounded-lg
                   hover:shadow-lg hover:scale-105 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-agro-naranja focus:ring-offset-2"
          >
            Registrarse
          </router-link>
        </div>

        <!-- Mobile Hamburger Button -->
        <button 
          @click="toggleMobileMenu"
          class="md:hidden p-2 rounded-lg text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-800
                 focus:outline-none focus:ring-2 focus:ring-agro-green transition-colors duration-200"
          :aria-label="isMobileMenuOpen ? 'Cerrar menú' : 'Abrir menú'"
          :aria-expanded="isMobileMenuOpen"
        >
          <svg 
            v-if="!isMobileMenuOpen" 
            class="w-6 h-6" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
          <svg 
            v-else 
            class="w-6 h-6" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </nav>

    <!-- Mobile Menu -->
    <Transition 
      enter-active-class="transition-all duration-300 ease-out"
      enter-from-class="opacity-0 -translate-y-4"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition-all duration-200 ease-in"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 -translate-y-4"
    >
      <div 
        v-if="isMobileMenuOpen"
        class="md:hidden absolute top-full left-0 right-0 bg-white/95 dark:bg-gray-900/95 backdrop-blur-md shadow-lg border-t border-gray-100 dark:border-gray-800"
      >
        <div class="px-4 py-6 space-y-4">
          <!-- Mobile Links -->
          <router-link 
            to="/catalogo"
            @click="closeMobileMenu"
            class="block px-4 py-3 text-lg font-medium text-gray-700 dark:text-gray-200 
                   hover:bg-agro-green/10 hover:text-agro-green rounded-lg transition-all duration-200"
            active-class="bg-agro-green/10 text-agro-green font-semibold"
          >
            📦 Catálogo
          </router-link>
          <a 
            href="#como-funciona"
            @click="closeMobileMenu"
            class="block px-4 py-3 text-lg font-medium text-gray-700 dark:text-gray-200 
                   hover:bg-agro-green/10 hover:text-agro-green rounded-lg transition-all duration-200"
          >
            ❓ Cómo funciona
          </a>
          <a 
            href="https://wa.me/1234567890"
            target="_blank"
            rel="noopener noreferrer"
            @click="closeMobileMenu"
            class="block px-4 py-3 text-lg font-medium text-gray-700 dark:text-gray-200 
                   hover:bg-agro-green/10 hover:text-agro-green rounded-lg transition-all duration-200"
          >
            📞 Contacto
          </a>

          <!-- Mobile Actions -->
          <div class="pt-4 space-y-3 border-t border-gray-200 dark:border-gray-700">
            <router-link 
              to="/catalogo"
              @click="closeMobileMenu"
              class="block w-full px-4 py-3 text-center bg-gradient-to-r from-agro-green to-agro-green-light 
                     text-white font-semibold rounded-lg hover:shadow-lg transition-all duration-200"
            >
              🔍 Explorar catálogo
            </router-link>
            <router-link 
              to="/login"
              @click="closeMobileMenu"
              class="block w-full px-4 py-3 text-center text-agro-green font-semibold rounded-lg 
                     border-2 border-agro-green hover:bg-agro-green/10 transition-all duration-200"
            >
              🔑 Iniciar sesión
            </router-link>
            <router-link 
              to="/registro"
              @click="closeMobileMenu"
              class="block w-full px-4 py-3 text-center bg-gradient-to-r from-agro-green to-agro-naranja 
                     text-white font-semibold rounded-lg hover:shadow-lg transition-all duration-200"
            >
              ✨ Registrarse
            </router-link>
          </div>
        </div>
      </div>
    </Transition>
  </header>
</template>

<script setup lang="ts">
import { useNavbar } from '../composables/useNavbar'

const { isMobileMenuOpen, scrolled, toggleMobileMenu, closeMobileMenu } = useNavbar()
</script>

<style scoped>
/* Custom focus styles for accessibility */
button:focus-visible,
a:focus-visible,
router-link:focus-visible {
  outline: 2px solid #2E7D32;
  outline-offset: 2px;
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}
</style>
