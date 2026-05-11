<template>
  <section class="space-y-6">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <p class="text-sm font-medium text-agro-green">Reportes</p>
        <h2 class="text-2xl font-bold text-gray-900">Historial de Ventas</h2>
      </div>
      <button class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-semibold text-gray-700 hover:bg-gray-50" @click="exportCSV">
        Descargar reporte CSV
      </button>
    </div>

    <div class="rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
      <h3 class="mb-4 font-bold text-gray-900">Ventas por mes (últimos 6 meses)</h3>
      <div class="flex items-end gap-3" style="min-height: 120px">
        <div
          v-for="mes in ventasPorMes"
          :key="mes.mes"
          class="flex flex-1 flex-col items-center"
        >
          <span class="mb-1 text-xs font-semibold text-gray-700">${{ mes.total }}</span>
          <div
            class="w-full rounded-t bg-agro-green transition-all"
            :style="{ height: barHeight(mes.total) + 'px' }"
          ></div>
          <span class="mt-1 text-xs text-gray-500">{{ mes.label }}</span>
        </div>
        <div v-if="!ventasPorMes.length" class="w-full py-8 text-center text-sm text-gray-500">
          No hay ventas en los últimos 6 meses.
        </div>
      </div>
    </div>

    <div class="overflow-x-auto rounded-lg border border-gray-200 bg-white shadow-sm">
      <table class="min-w-full text-left text-sm">
        <thead class="bg-gray-50 text-gray-500">
          <tr>
            <th class="px-4 py-3">Pedido</th>
            <th class="px-4 py-3">Producto</th>
            <th class="px-4 py-3">Comprador</th>
            <th class="px-4 py-3">Cantidad</th>
            <th class="px-4 py-3">Total</th>
            <th class="px-4 py-3">Fecha</th>
            <th class="px-4 py-3">Estado</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="pedido in ventasEntregadas" :key="pedido.id" class="border-t border-gray-100 hover:bg-gray-50">
            <td class="px-4 py-3 font-mono text-xs text-gray-500">#{{ pedido.id }}</td>
            <td class="px-4 py-3 font-medium text-gray-900">{{ pedido.nombreProducto }}</td>
            <td class="px-4 py-3 text-gray-600">{{ pedido.compradorNombre }}</td>
            <td class="px-4 py-3 text-gray-600">{{ pedido.cantidadQuintales }} qq</td>
            <td class="px-4 py-3 font-medium text-gray-900">{{ currency(pedido.total) }}</td>
            <td class="px-4 py-3 text-xs text-gray-500">{{ formatDate(pedido.createdAt) }}</td>
            <td class="px-4 py-3"><StatusBadge :estado="pedido.estado" /></td>
          </tr>
          <tr v-if="!ventasEntregadas.length">
            <td colspan="7" class="py-10 text-center text-gray-500">Aún no tienes ventas completadas.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import StatusBadge from '../shared/StatusBadge.vue'
import { useAuthStore } from '../../stores/authStore'
import { usePedidoStore } from '../../stores/pedidoStore'

const { currentUser } = useAuthStore()
const { pedidos, loadPedidosProductor } = usePedidoStore()

const ventasEntregadas = computed(() => pedidos.value.filter((p) => p.estado === 'entregado'))

const currency = (value: number) => new Intl.NumberFormat('es-HN', { style: 'currency', currency: 'USD' }).format(value)
const formatDate = (date: string) => new Date(date).toLocaleDateString('es-HN', { day: '2-digit', month: '2-digit', year: '2-digit' })

interface VentasMes {
  mes: string
  label: string
  total: number
}

const ventasPorMes = computed(() => {
  const now = new Date()
  const meses: VentasMes[] = []
  for (let i = 5; i >= 0; i--) {
    const d = new Date(now.getFullYear(), now.getMonth() - i, 1)
    const key = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`
    const label = d.toLocaleDateString('es-HN', { month: 'short' })
    const total = ventasEntregadas.value
      .filter((p) => p.createdAt.startsWith(key))
      .reduce((sum, p) => sum + p.total, 0)
    meses.push({ mes: key, label, total })
  }
  return meses
})

const maxTotal = computed(() => Math.max(...ventasPorMes.value.map((m) => m.total), 1))
const barHeight = (total: number) => Math.max(4, (total / maxTotal.value) * 100)

const exportCSV = () => {
  const headers = ['ID Pedido,Producto,Comprador,Cantidad (qq),Total,Estado,Fecha']
  const rows = ventasEntregadas.value.map((p) =>
    `${p.id},"${p.nombreProducto}","${p.compradorNombre}",${p.cantidadQuintales},${p.total},"${p.estado}","${p.createdAt}"`
  )
  const csv = [...headers, ...rows].join('\n')
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `ventas-${new Date().toISOString().slice(0, 10)}.csv`
  a.click()
  URL.revokeObjectURL(url)
}

onMounted(async () => {
  if (currentUser.value) {
    await loadPedidosProductor(currentUser.value.id)
  }
})
</script>
