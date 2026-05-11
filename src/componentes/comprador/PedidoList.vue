<template>
  <section class="space-y-5">
    <div class="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
      <div>
        <p class="text-sm font-medium text-agro-green">Mis Pedidos</p>
        <h2 class="text-2xl font-bold text-gray-900">Historial y seguimiento</h2>
      </div>
      <button class="rounded-lg bg-agro-green px-4 py-2 text-sm font-semibold text-white" @click="downloadCsv">
        Descargar reporte CSV
      </button>
    </div>

    <SearchFilter v-model="filtros" />

    <div class="overflow-x-auto rounded-lg border border-gray-200 bg-white shadow-sm">
      <table class="min-w-[980px] w-full text-left text-sm">
        <thead class="bg-gray-50 text-gray-500">
          <tr>
            <th class="px-4 py-3">ID Pedido</th>
            <th class="px-4 py-3">Producto</th>
            <th class="px-4 py-3">Productor</th>
            <th class="px-4 py-3">Cantidad</th>
            <th class="px-4 py-3">Precio Unitario</th>
            <th class="px-4 py-3">Total</th>
            <th class="px-4 py-3">Fecha</th>
            <th class="px-4 py-3">Estado</th>
            <th class="px-4 py-3">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="pedido in paginatedPedidos" :key="pedido.id" class="border-t border-gray-100">
            <td class="px-4 py-3 font-semibold text-gray-900">#{{ pedido.id }}</td>
            <td class="px-4 py-3">{{ pedido.nombreProducto }}</td>
            <td class="px-4 py-3">{{ pedido.productor }}</td>
            <td class="px-4 py-3">{{ pedido.cantidadQuintales }} Qq</td>
            <td class="px-4 py-3">{{ currency(pedido.precioUnitario) }}</td>
            <td class="px-4 py-3">{{ currency(pedido.total) }}</td>
            <td class="px-4 py-3">{{ formatDate(pedido.createdAt) }}</td>
            <td class="px-4 py-3">
              <StatusBadge :estado="pedido.estado" />
              <p v-if="pedido.estado === 'solicitado'" class="mt-1 text-xs text-yellow-700">Pendiente de confirmación</p>
            </td>
            <td class="px-4 py-3">
              <div class="flex flex-wrap gap-2">
                <router-link :to="`/dashboard/comprador/pedidos/${pedido.id}`" class="font-semibold text-agro-green">Detalle</router-link>
                <router-link :to="`/dashboard/comprador/tracking/${pedido.id}`" class="font-semibold text-gray-600">Tracking</router-link>
                <a :href="whatsappLink(pedido)" target="_blank" rel="noopener noreferrer" class="font-semibold text-gray-600">Contactar</a>
              </div>
            </td>
          </tr>
          <tr v-if="!paginatedPedidos.length">
            <td colspan="9" class="px-4 py-8 text-center text-gray-500">No hay pedidos con los filtros actuales.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <Pagination v-model:page="page" :total-pages="totalPages" />
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import SearchFilter from '../shared/SearchFilter.vue'
import Pagination from '../shared/Pagination.vue'
import StatusBadge from '../shared/StatusBadge.vue'
import { useAuthStore } from '../../stores/authStore'
import { usePedidoStore } from '../../stores/pedidoStore'
import type { IPedidoDetalle, PedidoFiltros } from '../../types/IPedido'

const { currentUser } = useAuthStore()
const { loadPedidos, filterPedidos } = usePedidoStore()
const page = ref(1)
const pageSize = 10
const filtros = ref<PedidoFiltros>({
  estado: 'todos',
  fechaInicio: '',
  fechaFin: '',
  busqueda: '',
})

const filteredPedidos = computed(() => filterPedidos(filtros.value))
const totalPages = computed(() => Math.max(1, Math.ceil(filteredPedidos.value.length / pageSize)))
const paginatedPedidos = computed(() => {
  const start = (page.value - 1) * pageSize
  return filteredPedidos.value.slice(start, start + pageSize)
})

watch(filtros, () => {
  page.value = 1
}, { deep: true })

const currency = (value: number) => new Intl.NumberFormat('es-HN', { style: 'currency', currency: 'USD' }).format(value)
const formatDate = (date: string) => new Intl.DateTimeFormat('es-HN', { dateStyle: 'medium' }).format(new Date(date))
const whatsappLink = (pedido: IPedidoDetalle) => `https://wa.me/${(pedido.productorTelefono || '+50488880000').replace(/\D/g, '')}`

const downloadCsv = () => {
  const rows = [
    ['ID', 'Producto', 'Productor', 'Cantidad', 'Precio Unitario', 'Total', 'Fecha', 'Estado'],
    ...filteredPedidos.value.map((pedido) => [
      pedido.id,
      pedido.nombreProducto,
      pedido.productor,
      pedido.cantidadQuintales,
      pedido.precioUnitario,
      pedido.total,
      pedido.createdAt,
      pedido.estado,
    ]),
  ]
  const csv = rows.map((row) => row.map((cell) => `"${String(cell).replace(/"/g, '""')}"`).join(',')).join('\n')
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = 'pedidos-comprador.csv'
  link.click()
  URL.revokeObjectURL(url)
}

onMounted(() => {
  if (currentUser.value) loadPedidos(currentUser.value.id)
})
</script>
