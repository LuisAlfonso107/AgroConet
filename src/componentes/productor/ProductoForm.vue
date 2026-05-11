<template>
  <section class="mx-auto max-w-2xl space-y-6">
    <div>
      <p class="text-sm font-medium text-agro-green">{{ esEdicion ? 'Editar' : 'Nuevo' }}</p>
      <h2 class="text-2xl font-bold text-gray-900">{{ esEdicion ? 'Editar Producto' : 'Publicar Nuevo Producto' }}</h2>
    </div>

    <form class="space-y-5 rounded-lg border border-gray-200 bg-white p-6 shadow-sm" @submit.prevent="handleSubmit">
      <div v-if="submitError" class="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">{{ submitError }}</div>

      <div class="grid gap-5 sm:grid-cols-2">
        <div>
          <label class="mb-1 block text-sm font-medium text-gray-700">Nombre *</label>
          <input v-model="form.nombre" class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-agro-green focus:outline-none" :class="{ 'border-red-400': errors.nombre }" />
          <p v-if="errors.nombre" class="mt-1 text-xs text-red-600">{{ errors.nombre }}</p>
        </div>
        <div>
          <label class="mb-1 block text-sm font-medium text-gray-700">Tipo *</label>
          <select v-model="form.tipo" class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-agro-green focus:outline-none" :class="{ 'border-red-400': errors.tipo }">
            <option value="">Seleccionar...</option>
            <option value="cafe">Café</option>
            <option value="maiz">Maíz</option>
            <option value="frijol">Frijol</option>
            <option value="arroz">Arroz</option>
            <option value="otros">Otros</option>
          </select>
          <p v-if="errors.tipo" class="mt-1 text-xs text-red-600">{{ errors.tipo }}</p>
        </div>
        <div>
          <label class="mb-1 block text-sm font-medium text-gray-700">Precio por quintal (USD) *</label>
          <input v-model.number="form.precio" type="number" min="0" step="0.01" class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-agro-green focus:outline-none" :class="{ 'border-red-400': errors.precio }" />
          <p v-if="errors.precio" class="mt-1 text-xs text-red-600">{{ errors.precio }}</p>
        </div>
        <div>
          <label class="mb-1 block text-sm font-medium text-gray-700">Cantidad (quintales) *</label>
          <input v-model.number="form.stock" type="number" min="0" step="1" class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-agro-green focus:outline-none" :class="{ 'border-red-400': errors.stock }" />
          <p v-if="errors.stock" class="mt-1 text-xs text-red-600">{{ errors.stock }}</p>
        </div>
        <div>
          <label class="mb-1 block text-sm font-medium text-gray-700">Humedad (%) *</label>
          <input v-model.number="form.humedad" type="number" min="0" max="25" step="0.1" class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-agro-green focus:outline-none" :class="{ 'border-red-400': errors.humedad }" />
          <p v-if="errors.humedad" class="mt-1 text-xs text-red-600">{{ errors.humedad }}</p>
        </div>
        <div>
          <label class="mb-1 block text-sm font-medium text-gray-700">Variedad *</label>
          <input v-model="form.variedad" class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-agro-green focus:outline-none" :class="{ 'border-red-400': errors.variedad }" />
          <p v-if="errors.variedad" class="mt-1 text-xs text-red-600">{{ errors.variedad }}</p>
        </div>
        <div>
          <label class="mb-1 block text-sm font-medium text-gray-700">Región *</label>
          <input v-model="form.region" class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-agro-green focus:outline-none" :class="{ 'border-red-400': errors.region }" />
          <p v-if="errors.region" class="mt-1 text-xs text-red-600">{{ errors.region }}</p>
        </div>
        <div>
          <label class="mb-1 block text-sm font-medium text-gray-700">País *</label>
          <input v-model="form.pais" class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-agro-green focus:outline-none" :class="{ 'border-red-400': errors.pais }" />
          <p v-if="errors.pais" class="mt-1 text-xs text-red-600">{{ errors.pais }}</p>
        </div>
      </div>
      <div>
        <label class="mb-1 block text-sm font-medium text-gray-700">Altura (msnm) *</label>
        <input v-model="form.altura" class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-agro-green focus:outline-none" :class="{ 'border-red-400': errors.altura }" />
        <p v-if="errors.altura" class="mt-1 text-xs text-red-600">{{ errors.altura }}</p>
      </div>
      <div>
        <label class="mb-1 block text-sm font-medium text-gray-700">Certificaciones</label>
        <div class="flex flex-wrap gap-3">
          <label v-for="cert in certificacionesOptions" :key="cert" class="flex items-center gap-2 text-sm text-gray-700">
            <input v-model="form.certificaciones" :value="cert" type="checkbox" class="rounded border-gray-300 text-agro-green focus:ring-agro-green" />
            {{ cert }}
          </label>
        </div>
      </div>
      <div>
        <label class="mb-1 block text-sm font-medium text-gray-700">Descripción</label>
        <textarea v-model="form.descripcion" rows="3" class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-agro-green focus:outline-none"></textarea>
      </div>
      <div>
        <label class="mb-1 block text-sm font-medium text-gray-700">URL de imagen</label>
        <input v-model="form.imagen" class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-agro-green focus:outline-none" />
      </div>
      <div class="flex justify-end gap-3 border-t border-gray-100 pt-5">
        <router-link to="/dashboard/productor/productos" class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-semibold text-gray-700">
          Cancelar
        </router-link>
        <button type="submit" :disabled="saving" class="rounded-lg bg-agro-green px-6 py-2 text-sm font-semibold text-white disabled:opacity-50">
          {{ saving ? 'Guardando...' : esEdicion ? 'Guardar Cambios' : 'Publicar Producto' }}
        </button>
      </div>
    </form>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/authStore'
import { useProductoStore } from '../../stores/productoStore'
import type { IProductoForm, ProductoTipo } from '../../types/IProducto'

const route = useRoute()
const router = useRouter()
const { currentUser } = useAuthStore()
const { createProducto, updateProducto, loadProducto } = useProductoStore()

const esEdicion = computed(() => !!route.params.id)
const saving = ref(false)
const submitError = ref<string | null>(null)

const form = reactive<IProductoForm>({
  nombre: '', tipo: '' as ProductoTipo, precio: null, stock: null,
  humedad: null, variedad: '', region: '', pais: '', altura: '',
  certificaciones: [], descripcion: '', imagen: '',
})

const errors = reactive<Record<string, string>>({})

const certificacionesOptions = ['Orgánico', 'Fair Trade', 'Rainforest Alliance', 'Non-GMO', 'UTZ']

const validate = (): boolean => {
  Object.keys(errors).forEach((k) => delete errors[k])
  if (!form.nombre || form.nombre.trim().length < 3) errors.nombre = 'Mínimo 3 caracteres'
  if (!form.tipo) errors.tipo = 'Selecciona un tipo'
  if (form.precio === null || form.precio <= 0) errors.precio = 'Debe ser un número positivo'
  if (form.stock === null || form.stock <= 0 || !Number.isInteger(Number(form.stock))) errors.stock = 'Debe ser un número entero positivo'
  if (form.humedad === null || form.humedad < 5 || form.humedad > 25) errors.humedad = 'Debe estar entre 5 y 25'
  if (!form.variedad.trim()) errors.variedad = 'Campo requerido'
  if (!form.region.trim()) errors.region = 'Campo requerido'
  if (!form.pais.trim()) errors.pais = 'Campo requerido'
  if (!form.altura.trim()) errors.altura = 'Campo requerido'
  return Object.keys(errors).length === 0
}

const handleSubmit = async () => {
  if (!validate()) return
  saving.value = true
  submitError.value = null

  if (!currentUser.value) return

  const payload = {
    ...form,
    precio: Number(form.precio),
    stock: Number(form.stock),
    humedad: Number(form.humedad),
  }

  if (esEdicion.value) {
    const result = await updateProducto(route.params.id as string, payload)
    if (result) {
      router.push('/dashboard/productor/productos')
    } else {
      submitError.value = 'No se pudo guardar el producto'
    }
  } else {
    const result = await createProducto({
      ...payload,
      productor: currentUser.value.name,
      productorId: currentUser.value.id,
    })
    if (result) {
      router.push('/dashboard/productor/productos')
    } else {
      submitError.value = 'No se pudo crear el producto'
    }
  }
  saving.value = false
}

onMounted(async () => {
  if (esEdicion.value && route.params.id) {
    const producto = await loadProducto(route.params.id as string)
    if (producto) {
      form.nombre = producto.nombre
      form.tipo = producto.tipo as ProductoTipo
      form.precio = producto.precio
      form.stock = producto.stock
      form.humedad = producto.humedad
      form.variedad = producto.variedad
      form.region = producto.region
      form.pais = producto.pais
      form.altura = producto.altura
      form.certificaciones = [...producto.certificaciones]
      form.descripcion = producto.descripcion || ''
      form.imagen = producto.imagen || ''
    }
  }
})
</script>
