<template>
  <section class="space-y-5">
    <router-link to="/dashboard/comprador/pedidos" class="text-sm font-semibold text-agro-green">Volver a pedidos</router-link>
    <article v-if="pedido" class="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
      <div class="mb-5 flex flex-wrap items-start justify-between gap-3">
        <div>
          <p class="text-sm text-gray-500">Tracking pedido #{{ pedido.id }}</p>
          <h2 class="text-2xl font-bold text-gray-900">{{ pedido.nombreProducto }}</h2>
        </div>
        <StatusBadge :estado="pedido.estado" />
      </div>
      <TrackingTimeline :current-estado="pedido.estado" :eventos="eventos" />
      <div v-if="pedido.agenciaNombre" class="mt-6 rounded-lg bg-blue-50 p-4 text-sm text-blue-900">
        Agencia asignada: {{ pedido.agenciaNombre }} · {{ pedido.agenciaContacto }}
      </div>
    </article>
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
const { selectedPedido: pedido, loadPedido } = usePedidoStore()
const { trackingByPedido, loadTracking } = useTrackingStore()
const eventos = computed(() => trackingByPedido.value[pedidoId.value] || [])

onMounted(async () => {
  await loadPedido(pedidoId.value)
  await loadTracking(pedidoId.value)
})
</script>
