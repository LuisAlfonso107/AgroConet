<template>
  <div class="grid gap-3 rounded-lg border border-gray-200 bg-white p-4 md:grid-cols-4">
    <input
      :value="modelValue.busqueda"
      @input="update('busqueda', ($event.target as HTMLInputElement).value)"
      class="rounded-lg border border-gray-300 px-3 py-2 text-sm"
      placeholder="Buscar producto o productor"
      type="search"
    />
    <select
      :value="modelValue.estado"
      @change="update('estado', ($event.target as HTMLSelectElement).value)"
      class="rounded-lg border border-gray-300 px-3 py-2 text-sm"
    >
      <option value="todos">Todos</option>
      <option value="solicitado">Solicitado</option>
      <option value="confirmado">Confirmado</option>
      <option value="en tránsito">En tránsito</option>
      <option value="entregado">Entregado</option>
      <option value="rechazado">Rechazado</option>
    </select>
    <input
      :value="modelValue.fechaInicio"
      @input="update('fechaInicio', ($event.target as HTMLInputElement).value)"
      class="rounded-lg border border-gray-300 px-3 py-2 text-sm"
      type="date"
    />
    <input
      :value="modelValue.fechaFin"
      @input="update('fechaFin', ($event.target as HTMLInputElement).value)"
      class="rounded-lg border border-gray-300 px-3 py-2 text-sm"
      type="date"
    />
  </div>
</template>

<script setup lang="ts">
import type { PedidoFiltros } from '../../types/IPedido'

const props = defineProps<{
  modelValue: PedidoFiltros
}>()

const emit = defineEmits<{
  'update:modelValue': [value: PedidoFiltros]
}>()

const update = (key: keyof PedidoFiltros, value: string) => {
  emit('update:modelValue', {
    ...props.modelValue,
    [key]: value,
  })
}
</script>
