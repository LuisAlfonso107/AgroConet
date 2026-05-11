<template>
  <section class="space-y-6">
    <div>
      <p class="text-sm font-medium text-agro-green">Gestión</p>
      <h2 class="text-2xl font-bold text-gray-900">Pedidos Recibidos</h2>
    </div>

    <div v-if="loading" class="py-10 text-center text-gray-500">Cargando pedidos...</div>
    <div v-else-if="error" class="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700">{{ error }}</div>

    <div v-else class="overflow-x-auto rounded-lg border border-gray-200 bg-white shadow-sm">
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
            <th class="px-4 py-3">Acción</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="pedido in pedidos" :key="pedido.id" class="border-t border-gray-100 hover:bg-gray-50">
            <td class="px-4 py-3 font-mono text-xs text-gray-500">#{{ pedido.id }}</td>
            <td class="px-4 py-3 font-medium text-gray-900">{{ pedido.nombreProducto }}</td>
            <td class="px-4 py-3 text-gray-600">{{ pedido.compradorNombre }}</td>
            <td class="px-4 py-3 text-gray-600">{{ pedido.cantidadQuintales }} qq</td>
            <td class="px-4 py-3 font-medium text-gray-900">{{ currency(pedido.total) }}</td>
            <td class="px-4 py-3 text-xs text-gray-500">{{ formatDate(pedido.createdAt) }}</td>
            <td class="px-4 py-3"><StatusBadge :estado="pedido.estado" /></td>
            <td class="px-4 py-3">
              <div v-if="pedido.estado === 'solicitado'" class="flex gap-2">
                <button class="rounded bg-green-50 px-2.5 py-1 text-xs font-semibold text-green-700 hover:bg-green-100" @click="confirmarPedido(pedido)">
                  Confirmar
                </button>
                <button class="rounded bg-red-50 px-2.5 py-1 text-xs font-semibold text-red-700 hover:bg-red-100" @click="rechazarPedido(pedido)">
                  Rechazar
                </button>
              </div>
              <router-link v-else :to="`/dashboard/productor/tracking/${pedido.id}`" class="rounded bg-blue-50 px-2.5 py-1 text-xs font-semibold text-blue-700 hover:bg-blue-100">
                Ver Tracking
              </router-link>
            </td>
          </tr>
          <tr v-if="!pedidos.length">
            <td colspan="8" class="py-10 text-center text-gray-500">No hay pedidos recibidos aún.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import StatusBadge from '../shared/StatusBadge.vue'
import { useAuthStore } from '../../stores/authStore'
import { usePedidoStore } from '../../stores/pedidoStore'
import { TrackingService } from '../../services/TrackingService'
import type { IPedidoDetalle } from '../../types/IPedido'

const { currentUser } = useAuthStore()
const { pedidos, loading, error, loadPedidosProductor, updateEstado } = usePedidoStore()
const trackingService = new TrackingService()

const currency = (value: number) => new Intl.NumberFormat('es-HN', { style: 'currency', currency: 'USD' }).format(value)
const formatDate = (date: string) => new Date(date).toLocaleDateString('es-HN', { day: '2-digit', month: '2-digit', year: '2-digit' })

const confirmarPedido = async (pedido: IPedidoDetalle) => {
  await updateEstado(pedido.id, 'confirmado')
  await trackingService.create({
    pedidoId: pedido.id,
    estado: 'confirmado',
    descripcion: 'Confirmado por el productor.',
    updatedAt: new Date().toISOString(),
  })
}

const rechazarPedido = async (pedido: IPedidoDetalle) => {
  await updateEstado(pedido.id, 'rechazado')
  await trackingService.create({
    pedidoId: pedido.id,
    estado: 'rechazado',
    descripcion: 'Rechazado por el productor.',
    updatedAt: new Date().toISOString(),
  })
}

onMounted(async () => {
  if (currentUser.value) {
    await loadPedidosProductor(currentUser.value.id)
  }
})
</script>
