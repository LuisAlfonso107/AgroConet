import { ref } from 'vue'
import { TrackingService } from '../services/TrackingService'
import type { ITrackingEvento } from '../types/ITracking'

const trackingByPedido = ref<Record<string, ITrackingEvento[]>>({})
const loading = ref(false)
const error = ref<string | null>(null)
const trackingService = new TrackingService()

export function useTrackingStore() {
  const loadTracking = async (pedidoId: number | string) => {
    loading.value = true
    error.value = null
    try {
      const events = await trackingService.listByPedido(pedidoId)
      trackingByPedido.value[String(pedidoId)] = events
      return events
    } catch {
      error.value = 'No se pudo cargar el tracking'
      return []
    } finally {
      loading.value = false
    }
  }

  return {
    trackingByPedido,
    loading,
    error,
    loadTracking,
  }
}
