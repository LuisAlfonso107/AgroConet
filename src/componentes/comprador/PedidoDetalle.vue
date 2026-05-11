<template>
  <section class="space-y-5">
    <router-link to="/dashboard/comprador/pedidos" class="text-sm font-semibold text-agro-green">Volver a pedidos</router-link>

    <div v-if="pedido" class="grid gap-5 lg:grid-cols-[1.2fr_0.8fr]">
      <article class="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
        <div class="flex flex-wrap items-start justify-between gap-3">
          <div>
            <p class="text-sm text-gray-500">Pedido #{{ pedido.id }}</p>
            <h2 class="text-2xl font-bold text-gray-900">{{ pedido.nombreProducto }}</h2>
            <p class="mt-1 text-sm text-gray-500">Solicitado el {{ formatDate(pedido.createdAt) }}</p>
          </div>
          <StatusBadge :estado="pedido.estado" />
        </div>

        <div class="mt-6 grid gap-4 md:grid-cols-2">
          <div class="rounded-lg bg-gray-50 p-4">
            <h3 class="font-semibold text-gray-900">Producto</h3>
            <p class="mt-2 text-sm text-gray-600">Tipo: {{ pedido.tipo || 'No especificado' }}</p>
            <p class="text-sm text-gray-600">Variedad: {{ pedido.variedad || 'No especificada' }}</p>
            <p class="text-sm text-gray-600">Certificaciones: {{ pedido.certificaciones?.join(', ') || 'Sin certificaciones' }}</p>
          </div>
          <div class="rounded-lg bg-gray-50 p-4">
            <h3 class="font-semibold text-gray-900">Transacción</h3>
            <p class="mt-2 text-sm text-gray-600">Cantidad: {{ pedido.cantidadQuintales }} Qq</p>
            <p class="text-sm text-gray-600">Precio unitario: {{ currency(pedido.precioUnitario) }}</p>
            <p class="text-sm text-gray-600">Impuestos: {{ currency(pedido.impuestos || 0) }}</p>
            <p class="mt-2 font-bold text-gray-900">Total: {{ currency(pedido.total + (pedido.impuestos || 0)) }}</p>
          </div>
        </div>

        <div class="mt-5 rounded-lg bg-gray-50 p-4">
          <h3 class="font-semibold text-gray-900">Productor</h3>
          <p class="mt-2 text-sm text-gray-600">Nombre/Finca: {{ pedido.productor }}</p>
          <p class="text-sm text-gray-600">Ubicación: {{ pedido.productorUbicacion || 'No disponible' }}</p>
          <p class="text-sm text-gray-600">Calificación: {{ pedido.productorCalificacion || '4.7' }}/5</p>
          <router-link :to="`/producto/${pedido.productoId}`" class="mt-3 inline-block text-sm font-semibold text-agro-green">Ver perfil del productor</router-link>
        </div>

        <div class="mt-5 flex flex-wrap gap-3">
          <button v-if="pedido.estado === 'solicitado'" class="rounded-lg bg-red-600 px-4 py-2 text-sm font-semibold text-white" @click="cancelarPedido">
            Cancelar Pedido
          </button>
          <router-link v-else to="/contacto" class="rounded-lg bg-agro-green px-4 py-2 text-sm font-semibold text-white">
            Solicitar Soporte
          </router-link>
        </div>
      </article>

      <article class="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
        <h3 class="mb-4 font-bold text-gray-900">Tracking</h3>
        <TrackingTimeline :current-estado="pedido.estado" :eventos="eventos" />
        <div v-if="pedido.agenciaNombre" class="mt-5 rounded-lg bg-blue-50 p-4 text-sm text-blue-900">
          Agencia: {{ pedido.agenciaNombre }} · {{ pedido.agenciaContacto }}
        </div>
      </article>
    </div>
    <p v-else class="rounded-lg bg-white p-6 text-gray-500">Cargando pedido...</p>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import StatusBadge from '../shared/StatusBadge.vue'
import TrackingTimeline from './TrackingTimeline.vue'
import { usePedidoStore } from '../../stores/pedidoStore'
import { useTrackingStore } from '../../stores/trackingStore'

const route = useRoute()
const pedidoId = computed(() => route.params.id as string)
const { selectedPedido: pedido, loadPedido, updateEstado } = usePedidoStore()
const { trackingByPedido, loadTracking } = useTrackingStore()
const eventos = computed(() => trackingByPedido.value[pedidoId.value] || [])

const currency = (value: number) => new Intl.NumberFormat('es-HN', { style: 'currency', currency: 'USD' }).format(value)
const formatDate = (date: string) => new Intl.DateTimeFormat('es-HN', { dateStyle: 'medium', timeStyle: 'short' }).format(new Date(date))

const cancelarPedido = async () => {
  await updateEstado(pedidoId.value, 'cancelado')
  await loadTracking(pedidoId.value)
}

onMounted(async () => {
  await loadPedido(pedidoId.value)
  await loadTracking(pedidoId.value)
})
</script>
