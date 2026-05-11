<template>
  <section class="space-y-6">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <p class="text-sm font-medium text-agro-green">Gestión</p>
        <h2 class="text-2xl font-bold text-gray-900">Mis Productos</h2>
      </div>
      <router-link to="/dashboard/productor/nuevo-producto" class="rounded-lg bg-agro-green px-4 py-2 text-sm font-semibold text-white">
        Publicar Nuevo Producto
      </router-link>
    </div>

    <div v-if="loading" class="py-10 text-center text-gray-500">Cargando productos...</div>
    <div v-else-if="error" class="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700">{{ error }}</div>

    <div v-else class="overflow-x-auto rounded-lg border border-gray-200 bg-white shadow-sm">
      <table class="min-w-full text-left text-sm">
        <thead class="bg-gray-50 text-gray-500">
          <tr>
            <th class="px-4 py-3">Producto</th>
            <th class="px-4 py-3">Tipo</th>
            <th class="px-4 py-3">Precio</th>
            <th class="px-4 py-3">Stock</th>
            <th class="px-4 py-3">Humedad</th>
            <th class="px-4 py-3">Estado</th>
            <th class="px-4 py-3">Publicado</th>
            <th class="px-4 py-3">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="producto in paginaActual" :key="producto.id" class="border-t border-gray-100 hover:bg-gray-50">
            <td class="px-4 py-3 font-medium text-gray-900">{{ producto.nombre }}</td>
            <td class="px-4 py-3 text-gray-600 capitalize">{{ producto.tipo }}</td>
            <td class="px-4 py-3 text-gray-600">{{ currency(producto.precio) }}/qq</td>
            <td class="px-4 py-3 text-gray-600">{{ producto.stock }} qq</td>
            <td class="px-4 py-3 text-gray-600">{{ producto.humedad }}%</td>
            <td class="px-4 py-3">
              <span class="inline-flex rounded-full px-2.5 py-1 text-xs font-semibold" :class="estadoClass(producto.estado)">
                {{ estadoLabel(producto.estado) }}
              </span>
            </td>
            <td class="px-4 py-3 text-gray-500 text-xs">{{ formatDate(producto.createdAt) }}</td>
            <td class="px-4 py-3">
              <div class="flex gap-2">
                <router-link :to="`/dashboard/productor/editar-producto/${producto.id}`" class="rounded bg-blue-50 px-2 py-1 text-xs font-semibold text-blue-700 hover:bg-blue-100">
                  Editar
                </router-link>
                <button class="rounded px-2 py-1 text-xs font-semibold" :class="toggleBtnClass(producto.estado)" @click="cambiaEstado(producto)">
                  {{ producto.estado === 'pausado' ? 'Reanudar' : 'Pausar' }}
                </button>
                <button class="rounded bg-red-50 px-2 py-1 text-xs font-semibold text-red-700 hover:bg-red-100" @click="confirmarEliminar(producto)">
                  Eliminar
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="!productosPaginados.length">
            <td colspan="8" class="py-10 text-center text-gray-500">
              No tienes productos publicados aún.
              <router-link to="/dashboard/productor/nuevo-producto" class="ml-1 font-semibold text-agro-green">Publica tu primer producto</router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <Pagination v-if="totalPages > 1" :page="page" :total-pages="totalPages" @update:page="page = $event" />

    <div v-if="showConfirm" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4">
      <div class="w-full max-w-sm rounded-lg bg-white p-6 shadow-lg">
        <h3 class="text-lg font-bold text-gray-900">¿Eliminar producto?</h3>
        <p class="mt-2 text-sm text-gray-600">Esta acción no se puede deshacer. ¿Estás seguro de eliminar "{{ productoEliminar?.nombre }}"?</p>
        <div class="mt-5 flex justify-end gap-3">
          <button class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-semibold text-gray-700" @click="showConfirm = false">Cancelar</button>
          <button class="rounded-lg bg-red-600 px-4 py-2 text-sm font-semibold text-white" @click="eliminarProducto">Eliminar</button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import Pagination from '../shared/Pagination.vue'
import { useAuthStore } from '../../stores/authStore'
import { useProductoStore } from '../../stores/productoStore'
import type { IProducto, ProductoEstado } from '../../types/IProducto'

const { currentUser } = useAuthStore()
const { productos, loading, error, loadProductos, updateProducto, removeProducto } = useProductoStore()

const page = ref(1)
const perPage = 10
const showConfirm = ref(false)
const productoEliminar = ref<IProducto | null>(null)

const productosPaginados = computed(() => productos.value)
const totalPages = computed(() => Math.max(1, Math.ceil(productosPaginados.value.length / perPage)))
const paginaActual = computed(() => productosPaginados.value.slice((page.value - 1) * perPage, page.value * perPage))

const currency = (value: number) => new Intl.NumberFormat('es-HN', { style: 'currency', currency: 'USD' }).format(value)

const formatDate = (date: string) => new Date(date).toLocaleDateString('es-HN', { day: '2-digit', month: '2-digit', year: '2-digit' })

const estadoLabel = (estado: string) => {
  const labels: Record<string, string> = { disponible: 'Disponible', agotado: 'Agotado', pausado: 'Pausado' }
  return labels[estado] || estado
}

const estadoClass = (estado: string) => {
  const classes: Record<string, string> = {
    disponible: 'bg-green-100 text-green-800',
    agotado: 'bg-gray-200 text-gray-700',
    pausado: 'bg-yellow-100 text-yellow-800',
  }
  return classes[estado] || 'bg-gray-100 text-gray-700'
}

const toggleBtnClass = (estado: string) => {
  return estado === 'pausado'
    ? 'bg-green-50 text-green-700 hover:bg-green-100'
    : 'bg-yellow-50 text-yellow-700 hover:bg-yellow-100'
}

const cambiaEstado = async (producto: IProducto) => {
  const nuevoEstado: ProductoEstado = producto.estado === 'pausado' ? 'disponible' : 'pausado'
  await updateProducto(producto.id, { estado: nuevoEstado } as Partial<IProducto>)
}

const confirmarEliminar = (producto: IProducto) => {
  productoEliminar.value = producto
  showConfirm.value = true
}

const eliminarProducto = async () => {
  if (!productoEliminar.value) return
  const success = await removeProducto(productoEliminar.value.id)
  if (success) showConfirm.value = false
}

onMounted(async () => {
  if (currentUser.value) {
    await loadProductos(currentUser.value.id)
  }
})
</script>
