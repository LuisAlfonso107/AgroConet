<template>
  <section class="space-y-6">
    <div>
      <p class="text-sm font-medium text-agro-green">Resumen</p>
      <h2 class="text-2xl font-bold text-gray-900">Tu actividad de venta</h2>
    </div>
    <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      <StatsCard label="Productos Activos" :value="productosActivos" hint="Publicados" />
      <StatsCard label="Pedidos Pendientes" :value="resumenProductor.pedidosPendientes" hint="Por atender" />
      <StatsCard label="Total Vendido" :value="`${resumenProductor.totalVendidoQq} qq`" hint="Quintales" />
      <StatsCard label="Ingresos Estimados" :value="currency(resumenProductor.ingresosEstimados)" hint="Histórico" />
    </div>

    <div class="rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
      <div class="mb-4 flex items-center justify-between gap-3">
        <h3 class="font-bold text-gray-900">Últimos pedidos recibidos</h3>
        <router-link to="/dashboard/productor/pedidos" class="text-sm font-semibold text-agro-green">Ver todos</router-link>
      </div>
      <div class="overflow-x-auto">
        <table class="min-w-full text-left text-sm">
          <thead class="text-gray-500">
            <tr>
              <th class="py-2">Producto</th>
              <th class="py-2">Comprador</th>
              <th class="py-2">Cantidad</th>
              <th class="py-2">Total</th>
              <th class="py-2">Estado</th>
              <th class="py-2">Acción</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="pedido in ultimosPedidos" :key="pedido.id" class="border-t border-gray-100">
              <td class="py-3 font-medium text-gray-900">{{ pedido.nombreProducto }}</td>
              <td class="py-3 text-gray-600">{{ pedido.compradorNombre }}</td>
              <td class="py-3 text-gray-600">{{ pedido.cantidadQuintales }} qq</td>
              <td class="py-3 text-gray-600">{{ currency(pedido.total) }}</td>
              <td class="py-3"><StatusBadge :estado="pedido.estado" /></td>
              <td class="py-3">
                <router-link :to="`/dashboard/productor/pedidos`" class="font-semibold text-agro-green">Ver detalle</router-link>
              </td>
            </tr>
            <tr v-if="!ultimosPedidos.length">
              <td colspan="6" class="py-6 text-center text-gray-500">Aún no tienes pedidos recibidos.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import StatsCard from '../shared/StatsCard.vue'
import StatusBadge from '../shared/StatusBadge.vue'
import { useAuthStore } from '../../stores/authStore'
import { usePedidoStore } from '../../stores/pedidoStore'
import { useProductoStore } from '../../stores/productoStore'

const { currentUser } = useAuthStore()
const { pedidos, resumenProductor, loadPedidosProductor } = usePedidoStore()
const { productos, loadProductos } = useProductoStore()

const ultimosPedidos = computed(() => pedidos.value.slice(0, 5))
const productosActivos = computed(() => productos.value.filter((p) => p.estado === 'disponible').length)

const currency = (value: number) => new Intl.NumberFormat('es-HN', { style: 'currency', currency: 'USD' }).format(value)

onMounted(async () => {
  if (currentUser.value) {
    await Promise.all([
      loadPedidosProductor(currentUser.value.id),
      loadProductos(currentUser.value.id),
    ])
  }
})
</script>
