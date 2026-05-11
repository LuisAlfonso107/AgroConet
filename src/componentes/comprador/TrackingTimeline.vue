<template>
  <ol class="space-y-4">
    <li v-for="step in timeline" :key="step.estado" class="flex gap-3">
      <span
        class="mt-1 flex h-6 w-6 shrink-0 items-center justify-center rounded-full text-xs font-bold"
        :class="stepClasses(step.status)"
      >
        <span v-if="step.status === 'done'">✓</span>
        <span v-else-if="step.status === 'current'" class="h-2 w-2 animate-pulse rounded-full bg-white"></span>
      </span>
      <div>
        <p class="font-semibold text-gray-900">{{ step.label }}</p>
        <p class="text-sm text-gray-500">{{ step.descripcion }}</p>
        <p v-if="step.fecha" class="mt-1 text-xs text-gray-400">{{ formatDate(step.fecha) }}</p>
      </div>
    </li>
  </ol>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { PedidoEstado } from '../../types/IPedido'
import type { ITrackingEvento } from '../../types/ITracking'

const props = defineProps<{
  currentEstado: PedidoEstado
  eventos: ITrackingEvento[]
}>()

const steps: { estado: PedidoEstado; label: string; descripcion: string }[] = [
  { estado: 'solicitado', label: 'Pedido creado', descripcion: 'La solicitud fue registrada.' },
  { estado: 'confirmado', label: 'Confirmado por el productor', descripcion: 'El productor aceptó la compra.' },
  { estado: 'en puerto', label: 'En puerto de origen', descripcion: 'El producto llegó a puerto.' },
  { estado: 'en tránsito', label: 'En tránsito', descripcion: 'El pedido va camino al comprador.' },
  { estado: 'entregado', label: 'Entregado', descripcion: 'La entrega fue completada.' },
]

const terminalStates: PedidoEstado[] = ['rechazado', 'cancelado']

const timeline = computed(() => {
  const currentIndex = steps.findIndex((step) => step.estado === props.currentEstado)
  const terminal = terminalStates.includes(props.currentEstado)
  const lastEvent = props.eventos[props.eventos.length - 1]

  return steps.map((step, index) => {
    const event = props.eventos.find((item) => item.estado === step.estado)
    let status: 'done' | 'current' | 'future' | 'blocked' = 'future'

    if (terminal) {
      status = event ? 'done' : 'blocked'
    } else if (index < currentIndex) {
      status = 'done'
    } else if (index === currentIndex) {
      status = 'current'
    }

    return {
      ...step,
      status,
      descripcion: event?.descripcion || (terminal && !event ? `No alcanzado: pedido ${props.currentEstado}` : step.descripcion),
      fecha: event?.updatedAt || (step.estado === props.currentEstado ? lastEvent?.updatedAt : ''),
    }
  })
})

const stepClasses = (status: string) => {
  if (status === 'done') return 'bg-green-600 text-white'
  if (status === 'current') return 'bg-agro-green text-white ring-4 ring-green-100'
  if (status === 'blocked') return 'bg-red-100 text-red-600'
  return 'bg-gray-200 text-gray-400'
}

const formatDate = (date: string) => new Intl.DateTimeFormat('es-HN', {
  dateStyle: 'medium',
  timeStyle: 'short',
}).format(new Date(date))
</script>
