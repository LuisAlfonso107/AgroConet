<template>
  <section class="mx-auto max-w-2xl space-y-6">
    <div>
      <p class="text-sm font-medium text-agro-green">Configuración</p>
      <h2 class="text-2xl font-bold text-gray-900">Mi Perfil</h2>
    </div>

    <div v-if="loading" class="py-10 text-center text-gray-500">Cargando perfil...</div>

    <form v-else class="space-y-5 rounded-lg border border-gray-200 bg-white p-6 shadow-sm" @submit.prevent="handleSave">
      <div v-if="successMsg" class="rounded-lg border border-green-200 bg-green-50 p-3 text-sm text-green-700">{{ successMsg }}</div>
      <div v-if="error" class="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">{{ error }}</div>

      <div class="grid gap-5 sm:grid-cols-2">
        <div>
          <label class="mb-1 block text-sm font-medium text-gray-700">Nombre</label>
          <input :value="profile?.name" disabled class="w-full rounded-lg border border-gray-200 bg-gray-50 px-3 py-2 text-sm text-gray-500" />
        </div>
        <div>
          <label class="mb-1 block text-sm font-medium text-gray-700">Email</label>
          <input :value="profile?.email" disabled class="w-full rounded-lg border border-gray-200 bg-gray-50 px-3 py-2 text-sm text-gray-500" />
        </div>
        <div>
          <label class="mb-1 block text-sm font-medium text-gray-700">Teléfono</label>
          <input v-model="form.telefono" class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-agro-green focus:outline-none" />
        </div>
        <div>
          <label class="mb-1 block text-sm font-medium text-gray-700">Nombre de la finca</label>
          <input v-model="form.finca" class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-agro-green focus:outline-none" />
        </div>
      </div>
      <div>
        <label class="mb-1 block text-sm font-medium text-gray-700">Ubicación</label>
        <input v-model="form.ubicacion" class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-agro-green focus:outline-none" placeholder="Ej: Copán, Honduras" />
      </div>
      <div>
        <label class="mb-1 block text-sm font-medium text-gray-700">Descripción breve</label>
        <textarea v-model="form.descripcion" rows="3" class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-agro-green focus:outline-none" placeholder="Describe tu finca y productos"></textarea>
      </div>
      <div>
        <label class="mb-1 block text-sm font-medium text-gray-700">URL de foto de perfil</label>
        <input v-model="form.fotoPerfil" class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-agro-green focus:outline-none" />
      </div>
      <div class="flex justify-end gap-3 border-t border-gray-100 pt-5">
        <button type="button" class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-semibold text-gray-700" @click="resetForm">
          Restablecer
        </button>
        <button type="submit" :disabled="saving" class="rounded-lg bg-agro-green px-6 py-2 text-sm font-semibold text-white disabled:opacity-50">
          {{ saving ? 'Guardando...' : 'Guardar Cambios' }}
        </button>
      </div>
    </form>
  </section>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { useAuthStore } from '../../stores/authStore'

const { profile, loading, error, loadProfile, saveProfile } = useAuthStore()

const saving = ref(false)
const successMsg = ref<string | null>(null)

const form = reactive({
  telefono: '',
  finca: '',
  ubicacion: '',
  descripcion: '',
  fotoPerfil: '',
})

const resetForm = () => {
  if (profile.value) {
    form.telefono = profile.value.telefono || ''
    form.finca = profile.value.finca || ''
    form.ubicacion = profile.value.ubicacion || ''
    form.descripcion = profile.value.descripcion || ''
    form.fotoPerfil = profile.value.fotoPerfil || ''
  }
}

const handleSave = async () => {
  saving.value = true
  successMsg.value = null
  const result = await saveProfile({ ...form })
  if (result) {
    successMsg.value = 'Perfil actualizado exitosamente'
    setTimeout(() => { successMsg.value = null }, 3000)
  }
  saving.value = false
}

onMounted(async () => {
  await loadProfile()
  resetForm()
})
</script>
