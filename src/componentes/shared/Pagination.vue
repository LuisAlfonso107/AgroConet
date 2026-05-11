<template>
  <div class="flex items-center justify-between gap-3">
    <button
      class="rounded-lg border border-gray-300 px-3 py-2 text-sm font-medium text-gray-700 disabled:opacity-40"
      :disabled="page <= 1"
      @click="$emit('update:page', page - 1)"
    >
      Anterior
    </button>
    <span class="text-sm text-gray-500">Página {{ page }} de {{ totalPages }}</span>
    <button
      class="rounded-lg border border-gray-300 px-3 py-2 text-sm font-medium text-gray-700 disabled:opacity-40"
      :disabled="page >= totalPages"
      @click="$emit('update:page', page + 1)"
    >
      Siguiente
    </button>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  page: number
  totalPages: number
}>()

defineEmits<{
  'update:page': [page: number]
}>()
</script>
