import { computed, ref } from 'vue'
import type { IPedidoDetalle } from '../types/IPedido'

export interface NotificacionPanel {
  id: string
  text: string
  read: boolean
}

const notifications = ref<NotificacionPanel[]>([])

export function useNotificacionStore() {
  const refreshFromPedidos = (pedidos: IPedidoDetalle[]) => {
    notifications.value = pedidos
      .filter((pedido) => ['confirmado', 'en tránsito', 'entregado'].includes(pedido.estado))
      .slice(0, 5)
      .map((pedido) => ({
        id: String(pedido.id),
        text: `Tu pedido #${pedido.id} de ${pedido.nombreProducto} está ${pedido.estado}.`,
        read: false,
      }))
  }

  const markAllRead = () => {
    notifications.value = notifications.value.map((notification) => ({ ...notification, read: true }))
  }

  const unreadCount = computed(() => notifications.value.filter((notification) => !notification.read).length)

  return {
    notifications,
    unreadCount,
    refreshFromPedidos,
    markAllRead,
  }
}
