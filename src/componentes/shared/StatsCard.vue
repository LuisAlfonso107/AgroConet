<template>
  <article class="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
    <p class="text-sm font-medium text-gray-500">{{ label }}</p>
    <div class="mt-3 flex items-end justify-between gap-3">
      <p class="text-3xl font-bold text-gray-900">{{ value }}</p>
      <span class="rounded-full bg-green-50 px-3 py-1 text-xs font-semibold text-green-700">{{ hint }}</span>
    </div>
  </article>
</template>

<script setup lang="ts">
defineProps<{
  label: string
  value: string | number
  hint: string
}>()
</script>
