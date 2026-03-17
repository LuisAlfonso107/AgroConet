<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-agro-crema via-white to-agro-green/10 py-12 px-4">
    <div class="max-w-md w-full">
      <!-- Logo -->
      <div class="text-center mb-8">
        <router-link to="/" class="inline-flex items-center gap-2 text-3xl font-bold text-agro-green hover:scale-105 transition-transform">
          <span class="text-4xl">🌾</span>
          <span class="bg-gradient-to-r from-agro-green to-agro-green-light bg-clip-text text-transparent">
            AgroConet
          </span>
        </router-link>
      </div>

      <!-- Login Card -->
      <div class="bg-white/80 backdrop-blur-md rounded-2xl shadow-xl p-8 border border-gray-100">
        <h1 class="text-2xl font-bold text-gray-800 text-center mb-2">
          ¡Bienvenido de nuevo!
        </h1>
        <p class="text-gray-500 text-center mb-8">
          Inicia sesión para continuar
        </p>

        <form @submit.prevent="handleLogin" class="space-y-5">
          <!-- Email -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
              Correo electrónico
            </label>
            <input 
              id="email"
              v-model="email"
              type="email" 
              required
              class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-agro-green focus:ring-2 focus:ring-agro-green/20 
                     transition-all duration-200 outline-none"
              placeholder="tu@email.com"
            />
          </div>

          <!-- Password -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
              Contraseña
            </label>
            <input 
              id="password"
              v-model="password"
              type="password" 
              required
              class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-agro-green focus:ring-2 focus:ring-agro-green/20 
                     transition-all duration-200 outline-none"
              placeholder="••••••••"
            />
          </div>

          <!-- Remember & Forgot -->
          <div class="flex items-center justify-between">
            <label class="flex items-center gap-2 cursor-pointer">
              <input type="checkbox" class="w-4 h-4 text-agro-green rounded border-gray-300 focus:ring-agro-green" />
              <span class="text-sm text-gray-600">Recordarme</span>
            </label>
            <a href="#" class="text-sm text-agro-green hover:underline">
              ¿Olvidaste tu contraseña?
            </a>
          </div>

          <!-- Submit Button -->
          <button 
            type="submit"
            class="w-full py-3 bg-gradient-to-r from-agro-green to-agro-green-light text-white font-semibold rounded-lg
                   hover:shadow-lg hover:scale-[1.02] active:scale-[0.98] transition-all duration-200"
          >
            Iniciar sesión
          </button>
        </form>

        <!-- Divider -->
        <div class="relative my-6">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-300"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-4 bg-white text-gray-500">o</span>
          </div>
        </div>

        <!-- Social Login -->
        <button 
          type="button"
          class="w-full py-3 flex items-center justify-center gap-3 border-2 border-gray-300 rounded-lg
                 hover:bg-gray-50 transition-colors duration-200"
        >
          <img src="https://www.google.com/favicon.ico" alt="Google" class="w-5 h-5" />
          <span class="font-medium text-gray-700">Continuar con Google</span>
        </button>
      </div>

      <!-- Register Link -->
      <p class="text-center mt-6 text-gray-600">
        ¿No tienes cuenta?
        <router-link to="/registro" class="text-agro-green font-semibold hover:underline">
          Regístrate
        </router-link>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const email = ref('')
const password = ref('')

const handleLogin = () => {
  // Placeholder - lógica de autenticación se implementará en US posterior
  console.log('Login:', email.value)
  router.push('/')
}
</script>
