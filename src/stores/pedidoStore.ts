import { computed, ref } from 'vue'
import { PedidoService } from '../services/PedidoService'
import type { IPedidoDetalle, PedidoEstado, PedidoFiltros } from '../types/IPedido'

const pedidos = ref<IPedidoDetalle[]>([])
const selectedPedido = ref<IPedidoDetalle | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)
const pedidoService = new PedidoService()

const activeStates: PedidoEstado[] = ['solicitado', 'confirmado', 'en tránsito']

export function usePedidoStore() {
  const loadPedidos = async (compradorId: number | string) => {
    loading.value = true
    error.value = null
    try {
      pedidos.value = await pedidoService.listByComprador(compradorId)
    } catch {
      error.value = 'No se pudieron cargar los pedidos'
    } finally {
      loading.value = false
    }
  }

  const loadPedidosProductor = async (productorId: number | string) => {
    loading.value = true
    error.value = null
    try {
      pedidos.value = await pedidoService.listByProductor(productorId)
    } catch {
      error.value = 'No se pudieron cargar los pedidos'
    } finally {
      loading.value = false
    }
  }

  const loadPedido = async (id: number | string) => {
    loading.value = true
    error.value = null
    try {
      selectedPedido.value = await pedidoService.getById(id)
      return selectedPedido.value
    } catch {
      error.value = 'No se pudo cargar el pedido'
      return null
    } finally {
      loading.value = false
    }
  }

  const updateEstado = async (id: number | string, estado: PedidoEstado) => {
    const updated = await pedidoService.updateEstado(id, estado)
    pedidos.value = pedidos.value.map((pedido) => pedido.id === id ? updated : pedido)
    selectedPedido.value = selectedPedido.value?.id === id ? updated : selectedPedido.value
    return updated
  }

  const filterPedidos = (filtros: PedidoFiltros) => {
    return pedidos.value.filter((pedido) => {
      const matchesEstado = !filtros.estado || filtros.estado === 'todos' || pedido.estado === filtros.estado
      const createdDate = pedido.createdAt.slice(0, 10)
      const matchesInicio = !filtros.fechaInicio || createdDate >= filtros.fechaInicio
      const matchesFin = !filtros.fechaFin || createdDate <= filtros.fechaFin
      const query = filtros.busqueda.trim().toLowerCase()
      const matchesBusqueda = !query ||
        pedido.nombreProducto.toLowerCase().includes(query) ||
        pedido.productor.toLowerCase().includes(query)

      return matchesEstado && matchesInicio && matchesFin && matchesBusqueda
    })
  }

  const resumen = computed(() => {
    const now = Date.now()
    const thirtyDays = 30 * 24 * 60 * 60 * 1000
    return {
      activos: pedidos.value.filter((pedido) => activeStates.includes(pedido.estado)).length,
      entregados30: pedidos.value.filter((pedido) => {
        return pedido.estado === 'entregado' && now - new Date(pedido.createdAt).getTime() <= thirtyDays
      }).length,
      totalInvertido: pedidos.value.reduce((total, pedido) => total + pedido.total, 0),
    }
  })

  const resumenProductor = computed(() => {
    const pedidosPendientes = pedidos.value.filter((p) => p.estado === 'solicitado')
    const pedidosConfirmados = pedidos.value.filter((p) => p.estado === 'confirmado' || p.estado === 'en tránsito' || p.estado === 'entregado')
    return {
      pedidosPendientes: pedidosPendientes.length,
      totalVendidoQq: pedidosConfirmados.reduce((sum, p) => sum + p.cantidadQuintales, 0),
      ingresosEstimados: pedidosConfirmados.reduce((sum, p) => sum + p.total, 0),
    }
  })

  return {
    pedidos,
    selectedPedido,
    loading,
    error,
    resumen,
    resumenProductor,
    loadPedidos,
    loadPedidosProductor,
    loadPedido,
    updateEstado,
    filterPedidos,
  }
}
