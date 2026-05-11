<template>
  <span class="inline-flex rounded-full px-2.5 py-1 text-xs font-semibold" :class="classes">
    {{ label }}
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { PedidoEstado } from '../../types/IPedido'

const props = defineProps<{
  estado: PedidoEstado | string
}>()

const labels: Record<string, string> = {
  solicitado: 'Solicitado',
  confirmado: 'Confirmado',
  'en puerto': 'En puerto',
  'en tránsito': 'En tránsito',
  entregado: 'Entregado',
  rechazado: 'Rechazado',
  cancelado: 'Cancelado',
}

const styles: Record<string, string> = {
  solicitado: 'bg-yellow-100 text-yellow-800',
  confirmado: 'bg-blue-100 text-blue-800',
  'en puerto': 'bg-indigo-100 text-indigo-800',
  'en tránsito': 'bg-purple-100 text-purple-800',
  entregado: 'bg-green-100 text-green-800',
  rechazado: 'bg-red-100 text-red-800',
  cancelado: 'bg-gray-200 text-gray-700',
}

const label = computed(() => labels[props.estado] || props.estado)
const classes = computed(() => styles[props.estado] || 'bg-gray-100 text-gray-700')
</script>
