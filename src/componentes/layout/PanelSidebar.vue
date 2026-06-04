<template>
  <aside
    class="fixed inset-y-0 left-0 z-40 w-72 border-r border-gray-200 bg-white px-4 py-5 transition-transform lg:static lg:translate-x-0"
    :class="open ? 'translate-x-0' : '-translate-x-full'"
  >
    <div class="flex items-center justify-between">
      <router-link to="/" class="text-xl font-bold text-agro-green">AgroConet</router-link>
      <button class="rounded-lg px-2 py-1 text-gray-500 lg:hidden" @click="$emit('close')">X</button>
    </div>
    <div class="mt-4 inline-flex items-center gap-2 rounded-full bg-green-50 px-3 py-1 text-sm font-semibold text-green-700">
      {{ roleLabel }}
    </div>
    <nav class="mt-8 space-y-2">
      <router-link
        v-for="item in visibleItems"
        :key="item.to"
        :to="item.to"
        class="flex items-center justify-between rounded-lg px-3 py-2 text-sm font-medium text-gray-700 hover:bg-green-50 hover:text-agro-green"
        active-class="bg-green-50 text-agro-green"
        @click="$emit('close')"
      >
        <span>{{ item.label }}</span>
        <span v-if="item.badge" class="rounded-full bg-red-100 px-2 py-0.5 text-xs text-red-700">{{ item.badge }}</span>
      </router-link>
    </nav>
    <button class="mt-8 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm font-semibold text-gray-700" @click="$emit('logout')">
      Cerrar sesión
    </button>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { UserRole } from '../../types/IUser'

const props = defineProps<{
  open: boolean
  notificationCount: number
  role: UserRole
}>()

defineEmits<{
  close: []
  logout: []
}>()

const roleLabel = computed(() => {
  const labels: Record<UserRole, string> = {
    comprador: 'Comprador',
    productor: 'Productor',
    agencia: 'Agencia',
  }
  return labels[props.role]
})

const itemsByRole: Record<UserRole, { label: string; to: string }[]> = {
  comprador: [
    { label: 'Resumen', to: '/dashboard/comprador' },
    { label: 'Mis Pedidos', to: '/dashboard/comprador/pedidos' },
    { label: 'Productos Favoritos', to: '/dashboard/comprador/favoritos' },
    { label: 'Catálogo', to: '/catalogo' },
    { label: 'Mi Perfil', to: '/dashboard/comprador/perfil' },
  ],
  productor: [
    { label: 'Resumen', to: '/dashboard/productor' },
    { label: 'Mis Productos', to: '/dashboard/productor/productos' },
    { label: 'Publicar Nuevo', to: '/dashboard/productor/nuevo-producto' },
    { label: 'Pedidos Recibidos', to: '/dashboard/productor/pedidos' },
    { label: 'Historial de Ventas', to: '/dashboard/productor/historial' },
    { label: 'Mi Perfil', to: '/dashboard/productor/perfil' },
  ],
  agencia: [
    { label: 'Panel Principal', to: '/dashboard/agencia' },
    { label: 'Catálogo', to: '/catalogo' },
  ],
}

interface NavItem {
  label: string
  to: string
  badge?: string
}

const visibleItems = computed(() => {
  const items = itemsByRole[props.role] || itemsByRole.comprador
  const basePath = props.role === 'comprador' ? '/dashboard/comprador' : '/dashboard/productor'
  return items.map((item) => {
    if (item.to === basePath && props.notificationCount > 0) {
      return { ...item, badge: String(props.notificationCount) } as NavItem
    }
    return item as NavItem
  })
})
</script>
