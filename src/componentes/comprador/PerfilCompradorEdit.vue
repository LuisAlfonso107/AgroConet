<template>
  <section class="space-y-5">
    <div>
      <p class="text-sm font-medium text-agro-green">Mi Perfil</p>
      <h2 class="text-2xl font-bold text-gray-900">Configuración del comprador</h2>
    </div>

    <form class="space-y-5 rounded-lg border border-gray-200 bg-white p-5 shadow-sm" @submit.prevent="save">
      <div class="grid gap-4 md:grid-cols-2">
        <label class="text-sm font-medium text-gray-700">
          Nombre
          <input v-model="form.name" readonly class="mt-1 w-full rounded-lg border border-gray-200 bg-gray-50 px-3 py-2" />
        </label>
        <label class="text-sm font-medium text-gray-700">
          Email
          <input v-model="form.email" readonly class="mt-1 w-full rounded-lg border border-gray-200 bg-gray-50 px-3 py-2" />
        </label>
        <label class="text-sm font-medium text-gray-700">
          Teléfono
          <input v-model="form.telefono" class="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2" />
        </label>
        <label class="text-sm font-medium text-gray-700">
          Foto de perfil
          <input v-model="form.fotoPerfil" class="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2" placeholder="URL de imagen" />
        </label>
        <label class="text-sm font-medium text-gray-700">
          Empresa
          <input v-model="form.empresa" class="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2" />
        </label>
        <label class="text-sm font-medium text-gray-700">
          País
          <input v-model="form.pais" class="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2" />
        </label>
      </div>

      <label class="block text-sm font-medium text-gray-700">
        Dirección preferida
        <textarea v-model="form.direccionEnvio" class="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2" rows="3"></textarea>
      </label>

      <div>
        <div class="mb-2 flex items-center justify-between">
          <h3 class="font-semibold text-gray-900">Direcciones de envío</h3>
          <button type="button" class="text-sm font-semibold text-agro-green" @click="addAddress">Agregar dirección</button>
        </div>
        <div class="space-y-2">
          <input
            v-for="(_, index) in form.direccionesEnvio"
            :key="index"
            v-model="form.direccionesEnvio[index]"
            class="w-full rounded-lg border border-gray-300 px-3 py-2"
          />
        </div>
      </div>

      <div class="flex flex-wrap gap-4">
        <label class="flex items-center gap-2 text-sm text-gray-700">
          <input v-model="form.preferenciasNotificacion.email" type="checkbox" />
          Notificar por email
        </label>
        <label class="flex items-center gap-2 text-sm text-gray-700">
          <input v-model="form.preferenciasNotificacion.whatsapp" type="checkbox" />
          Notificar por WhatsApp
        </label>
      </div>

      <div class="flex flex-wrap gap-3">
        <button class="rounded-lg bg-agro-green px-4 py-2 text-sm font-semibold text-white" type="submit">Guardar cambios</button>
        <button class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-semibold text-gray-500" type="button" disabled>Cambiar contraseña (fase 2)</button>
      </div>
      <p v-if="message" class="text-sm text-green-700">{{ message }}</p>
    </form>
  </section>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { useAuthStore } from '../../stores/authStore'

const { profile, loadProfile, saveProfile } = useAuthStore()
const message = ref('')
const form = reactive({
  name: '',
  email: '',
  telefono: '',
  fotoPerfil: '',
  empresa: '',
  direccionEnvio: '',
  direccionesEnvio: [''],
  pais: '',
  preferenciasNotificacion: {
    email: true,
    whatsapp: false,
  },
})

const fillForm = () => {
  if (!profile.value) return
  form.name = profile.value.name
  form.email = profile.value.email
  form.telefono = profile.value.telefono || ''
  form.fotoPerfil = profile.value.fotoPerfil || ''
  form.empresa = profile.value.empresa || ''
  form.direccionEnvio = profile.value.direccionEnvio || ''
  form.direccionesEnvio = profile.value.direccionesEnvio?.length ? [...profile.value.direccionesEnvio] : ['']
  form.pais = profile.value.pais || ''
  form.preferenciasNotificacion = profile.value.preferenciasNotificacion || { email: true, whatsapp: false }
}

const addAddress = () => {
  form.direccionesEnvio.push('')
}

const save = async () => {
  await saveProfile({
    telefono: form.telefono,
    fotoPerfil: form.fotoPerfil,
    empresa: form.empresa,
    direccionEnvio: form.direccionEnvio,
    direccionesEnvio: form.direccionesEnvio.filter(Boolean),
    pais: form.pais,
    preferenciasNotificacion: form.preferenciasNotificacion,
  })
  message.value = 'Perfil actualizado correctamente.'
}

onMounted(async () => {
  await loadProfile()
  fillForm()
})
</script>
