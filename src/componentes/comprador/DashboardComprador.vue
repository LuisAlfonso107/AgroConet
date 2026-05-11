<template>
  <div class="min-h-screen bg-gray-50 lg:flex">
    <PanelSidebar
      :open="sidebarOpen"
      :notification-count="unreadCount"
      role="comprador"
      @close="sidebarOpen = false"
      @logout="handleLogout"
    />
    <div class="min-w-0 flex-1">
      <PanelHeader
        :user-name="currentUser?.name || 'Comprador'"
        :notification-count="unreadCount"
        role="comprador"
        @toggle="sidebarOpen = !sidebarOpen"
        @read-notifications="markAllRead"
      />
      <main class="p-4 lg:p-6">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import PanelHeader from '../layout/PanelHeader.vue'
import PanelSidebar from '../layout/PanelSidebar.vue'
import { useAuthStore } from '../../stores/authStore'
import { usePedidoStore } from '../../stores/pedidoStore'
import { useNotificacionStore } from '../../stores/notificacionStore'

const router = useRouter()
const sidebarOpen = ref(false)
const { currentUser, logout } = useAuthStore()
const { pedidos, loadPedidos } = usePedidoStore()
const { unreadCount, refreshFromPedidos, markAllRead } = useNotificacionStore()

const handleLogout = () => {
  logout()
  router.push('/')
}

onMounted(async () => {
  if (currentUser.value) {
    await loadPedidos(currentUser.value.id)
    refreshFromPedidos(pedidos.value)
  }
})
</script>
