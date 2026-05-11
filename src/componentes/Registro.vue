<template>
  <div class="min-h-screen bg-crema pt-20 px-4">
    <div class="max-w-md mx-auto py-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-8 text-center">Registro</h1>
      <form @submit.prevent="handleRegister" class="bg-white p-6 rounded-xl shadow-md">
        <div class="mb-4">
          <label for="register-name" class="block text-gray-700 mb-2">Nombre completo</label>
          <input id="register-name" v-model="name" type="text" class="w-full px-4 py-2 border rounded-lg" placeholder="Ingrese su nombre completo" />
          <p v-if="errors.name" class="text-red-500 text-sm mt-1">{{ errors.name }}</p>
        </div>
        <div class="mb-4">
          <label for="register-email" class="block text-gray-700 mb-2">Email</label>
          <input id="register-email" v-model="email" type="email" class="w-full px-4 py-2 border rounded-lg" placeholder="Ingrese su email" />
          <p v-if="errors.email" class="text-red-500 text-sm mt-1">{{ errors.email }}</p>
        </div>
        <div class="mb-4">
          <label for="register-password" class="block text-gray-700 mb-2">Contraseña</label>
          <input id="register-password" v-model="password" type="password" class="w-full px-4 py-2 border rounded-lg" placeholder="Crea una contraseña" />
          <p v-if="errors.password" class="text-red-500 text-sm mt-1">{{ errors.password }}</p>
        </div>
        <div class="mb-4">
          <label for="register-user-type" class="block text-gray-700 mb-2">Tipo de usuario</label>
          <select id="register-user-type" v-model="userType" class="w-full px-4 py-2 border rounded-lg">
            <option value="comprador">Comprador</option>
            <option value="productor">Productor</option>
            <option value="agencia">Agencia Exportadora</option>
          </select>
        </div>
        <button 
          type="submit" 
          :disabled="loading"
          class="w-full bg-agro-green text-white py-3 rounded-lg font-semibold hover:bg-agro-green-light transition-colors"
        >
          {{ loading ? 'Registrando...' : 'Registrarse' }}
        </button>
        <p v-if="successMessage" class="mt-4 text-green-600 text-center">{{ successMessage }}</p>
        <p v-if="errorMessage" class="mt-4 text-red-600 text-center">{{ errorMessage }}</p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useApi } from '@/composables/useApi'
import { useRouter } from 'vue-router'
import { useAuth, type UserRole } from '@/composables/useAuth'

const { api } = useApi()
const router = useRouter()
const { setUser } = useAuth()

const name = ref('')
const email = ref('')
const password = ref('')
const userType = ref<UserRole>('comprador')
const loading = ref(false)
const errors = ref<Record<string, string>>({})
const successMessage = ref('')
const errorMessage = ref('')

const validate = () => {
  const newErrors: Record<string, string> = {}
  if (!name.value.trim()) {
    newErrors.name = 'El nombre es requerido'
  }
  if (!email.value.trim()) {
    newErrors.email = 'El email es requerido'
  } else {
    // Simple email regex
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(email.value)) {
      newErrors.email = 'El email no es válido'
    }
  }
  if (password.value.length < 6) {
    newErrors.password = 'La contraseña debe tener al menos 6 caracteres'
  }
  errors.value = newErrors
  return Object.keys(newErrors).length === 0
}

const handleRegister = async () => {
  if (!validate()) {
    return
  }

  loading.value = true
  successMessage.value = ''
  errorMessage.value = ''

  try {
      const existing = await api.get('/users', {
        params: { email: email.value.trim().toLowerCase() }
      })

      if (existing.data.length > 0) {
        errorMessage.value = 'Ya existe una cuenta con este email.'
        return
      }

      const response = await api.post('/users', {
        name: name.value.trim(),
        email: email.value.trim().toLowerCase(),
        password: password.value,
        userType: userType.value,
        createdAt: new Date().toISOString()
      })

    setUser({
      id: response.data.id,
      name: response.data.name,
      email: response.data.email,
      userType: response.data.userType
    })

    successMessage.value = 'Registro exitoso. Redirigiendo al catálogo...'
    setTimeout(() => {
      router.push('/catalogo')
    }, 1500)
  } catch (err) {
    console.error('Registration error:', err)
    errorMessage.value = 'Error al registrar. Ejecuta npm run mock e intenta nuevamente.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.bg-crema {
  background-color: #FFF8E1;
}
</style>
