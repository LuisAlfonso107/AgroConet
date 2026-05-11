<template>
  <header class="sticky top-0 z-30 border-b border-gray-200 bg-white/95 px-4 py-3 backdrop-blur">
    <div class="flex items-center justify-between gap-3">
      <div class="flex items-center gap-3">
        <button class="rounded-lg border border-gray-300 px-3 py-2 text-sm lg:hidden" @click="$emit('toggle')">
          Menu
        </button>
        <div>
          <p class="text-sm text-gray-500">Panel del {{ roleLabel }}</p>
          <h1 class="text-lg font-bold text-gray-900">{{ userName }}</h1>
        </div>
      </div>
      <div class="relative">
        <button class="rounded-lg border border-gray-300 px-3 py-2 text-sm" @click="$emit('readNotifications')">
          Notificaciones
          <span v-if="notificationCount" class="ml-2 rounded-full bg-red-600 px-2 py-0.5 text-xs text-white">{{ notificationCount }}</span>
        </button>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { UserRole } from '../../types/IUser'

const props = defineProps<{
  userName: string
  notificationCount: number
  role: UserRole
}>()

defineEmits<{
  toggle: []
  readNotifications: []
}>()

const roleLabel = computed(() => {
  const labels: Record<UserRole, string> = {
    comprador: 'comprador',
    productor: 'productor',
    agencia: 'agencia',
  }
  return labels[props.role]
})
</script>
