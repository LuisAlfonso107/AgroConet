<template>
  <div class="min-h-screen bg-gray-50 lg:flex">
    <PanelSidebar
      :open="sidebarOpen"
      :notification-count="0"
      role="agencia"
      @close="sidebarOpen = false"
      @logout="handleLogout"
    />
    <div class="min-w-0 flex-1">
      <PanelHeader
        :user-name="currentUser?.name || 'Agencia'"
        :notification-count="0"
        role="agencia"
        @toggle="sidebarOpen = !sidebarOpen"
      />
      <main class="p-4 lg:p-6">
        <div class="mb-6">
          <p class="text-sm font-medium text-agro-green">Panel de Agencia</p>
          <h2 class="text-2xl font-bold text-gray-900">Pedidos Pendientes de Envío</h2>
        </div>

        <div class="mb-6 grid gap-4 sm:grid-cols-3">
          <StatsCard label="Total Pedidos" :value="stats.total" hint="Registrados" />
          <StatsCard label="Pendientes de gestión" :value="stats.pendientes" hint="Confirmados" />
          <StatsCard label="Volumen total" :value="`${stats.volumen} Qq`" hint="Quintales" />
        </div>

        <div class="overflow-x-auto rounded-lg border border-gray-200 bg-white shadow-sm">
          <table v-if="pedidos.length" class="min-w-[980px] w-full text-left text-sm">
            <thead class="bg-gray-50 text-gray-500">
              <tr>
                <th class="px-4 py-3">ID Pedido</th>
                <th class="px-4 py-3">Producto</th>
                <th class="px-4 py-3">Productor</th>
                <th class="px-4 py-3">Comprador</th>
                <th class="px-4 py-3">Cantidad</th>
                <th class="px-4 py-3">Total</th>
                <th class="px-4 py-3">Estado</th>
                <th class="px-4 py-3">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="pedido in pedidos" :key="pedido.id" class="border-t border-gray-100">
                <td class="px-4 py-3 font-semibold text-gray-900">#{{ pedido.id }}</td>
                <td class="px-4 py-3">{{ pedido.nombreProducto }}</td>
                <td class="px-4 py-3">{{ pedido.productor }}</td>
                <td class="px-4 py-3">{{ pedido.compradorNombre }}</td>
                <td class="px-4 py-3">{{ pedido.cantidadQuintales }} Qq</td>
                <td class="px-4 py-3">{{ currency(pedido.total) }}</td>
                <td class="px-4 py-3">
                  <StatusBadge :estado="pedido.estado" />
                </td>
                <td class="px-4 py-3">
                  <div class="flex flex-wrap gap-2">
                    <button
                      class="rounded bg-agro-green px-3 py-1 text-xs font-semibold text-white"
                      @click="openUpdateModal(pedido)"
                    >
                      Actualizar estado
                    </button>
                    <button
                      class="rounded bg-gray-100 px-3 py-1 text-xs font-semibold text-gray-700"
                      @click="openTracking(pedido)"
                    >
                      Ver tracking
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
          <div v-else class="p-8 text-center text-gray-500">
            <p v-if="loading">Cargando pedidos...</p>
            <p v-else>No hay pedidos pendientes de gestión.</p>
          </div>
        </div>
      </main>
    </div>

    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4" @click.self="showModal = false">
      <div class="w-full max-w-md rounded-lg bg-white p-6 shadow-xl">
        <h3 class="text-lg font-bold text-gray-900">Actualizar estado</h3>
        <p class="mt-1 text-sm text-gray-500">Pedido #{{ selectedPedido?.id }} - {{ selectedPedido?.nombreProducto }}</p>

        <div class="mt-4 space-y-3">
          <StatusBadge :estado="selectedPedido?.estado || 'solicitado'" />
          <select v-model="nuevoEstado" class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm">
            <option value="" disabled>Seleccionar nuevo estado</option>
            <option value="en puerto">En puerto</option>
            <option value="en transito">En tránsito</option>
            <option value="entregado">Entregado</option>
          </select>
          <textarea
            v-model="descripcion"
            placeholder="Descripción del evento (opcional)"
            class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
            rows="3"
          ></textarea>
        </div>

        <div class="mt-6 flex justify-end gap-3">
          <button class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-semibold text-gray-700" @click="showModal = false">
            Cancelar
          </button>
          <button
            class="rounded-lg bg-agro-green px-4 py-2 text-sm font-semibold text-white disabled:opacity-50"
            :disabled="!nuevoEstado || updating"
            @click="handleUpdate"
          >
            {{ updating ? 'Actualizando...' : 'Actualizar' }}
          </button>
        </div>
      </div>
    </div>

    <div v-if="showTracking" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4" @click.self="showTracking = false">
      <div class="w-full max-w-lg rounded-lg bg-white p-6 shadow-xl">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-bold text-gray-900">Tracking - Pedido #{{ trackingPedido?.id }}</h3>
          <button class="text-gray-400 hover:text-gray-600" @click="showTracking = false">X</button>
        </div>
        <div class="mt-4">
          <TrackingTimeline v-if="trackingEventos.length" :current-estado="trackingPedido?.estado || 'solicitado'" :eventos="trackingEventos" />
          <p v-else class="text-center text-gray-500">No hay eventos de tracking registrados.</p>
        </div>
        <div class="mt-4 text-right">
          <button class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-semibold text-gray-700" @click="showTracking = false">
            Cerrar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useApi } from '../composables/useApi'
import { useAuth } from '../composables/useAuth'
import PanelHeader from '../componentes/layout/PanelHeader.vue'
import PanelSidebar from '../componentes/layout/PanelSidebar.vue'
import StatsCard from '../componentes/shared/StatsCard.vue'
import StatusBadge from '../componentes/shared/StatusBadge.vue'
import TrackingTimeline from '../componentes/comprador/TrackingTimeline.vue'
import type { PedidoEstado } from '../types/IPedido'
import type { ITrackingEvento } from '../types/ITracking'

interface PedidoRow {
  id: string
  nombreProducto: string
  productor: string
  compradorNombre: string
  cantidadQuintales: number
  total: number
  estado: PedidoEstado
}

const router = useRouter()
const { api } = useApi()
const { currentUser, logout } = useAuth()
const sidebarOpen = ref(false)
const pedidos = ref<PedidoRow[]>([])
const loading = ref(false)
const showModal = ref(false)
const showTracking = ref(false)
const selectedPedido = ref<PedidoRow | null>(null)
const trackingPedido = ref<PedidoRow | null>(null)
const trackingEventos = ref<ITrackingEvento[]>([])
const nuevoEstado = ref<string>('')
const descripcion = ref('')
const updating = ref(false)
const stats = ref({ total: 0, pendientes: 0, volumen: 0 })

const handleLogout = () => {
  logout()
  router.push('/')
}

const currency = (value: number) => new Intl.NumberFormat('es-HN', { style: 'currency', currency: 'USD' }).format(value)

const loadPedidos = async () => {
  loading.value = true
  try {
    const res = await api.get('/pedidos', { params: { limit: 100 } })
    const data = res.data.data || []
    const confirmados = data.filter((p: any) => p.estado === 'confirmado')
    pedidos.value = confirmados.map((p: any) => ({
      id: p.id,
      nombreProducto: p.nombre_producto,
      productor: p.productor?.name || 'N/A',
      compradorNombre: p.comprador?.name || 'N/A',
      cantidadQuintales: p.cantidad_quintales,
      total: p.total,
      estado: p.estado,
    }))
    stats.value = {
      total: data.length,
      pendientes: confirmados.length,
      volumen: confirmados.reduce((s: number, p: any) => s + p.cantidad_quintales, 0),
    }
  } catch {
    pedidos.value = []
  } finally {
    loading.value = false
  }
}

const openUpdateModal = (pedido: PedidoRow) => {
  selectedPedido.value = pedido
  nuevoEstado.value = ''
  descripcion.value = ''
  showModal.value = true
}

const openTracking = async (pedido: PedidoRow) => {
  trackingPedido.value = pedido
  showTracking.value = true
  trackingEventos.value = []
  try {
    const res = await api.get(`/pedidos/${pedido.id}/tracking`)
    const eventos = res.data.data || []
    trackingEventos.value = eventos.map((e: any) => ({
      id: e.id,
      pedidoId: e.pedido_id,
      estado: e.estado,
      descripcion: e.descripcion,
      updatedAt: e.created_at || e.updatedAt,
    }))
  } catch {
    trackingEventos.value = []
  }
}

const handleUpdate = async () => {
  if (!selectedPedido.value || !nuevoEstado.value) return
  updating.value = true
  try {
    await api.patch(`/pedidos/${selectedPedido.value.id}/estado`, {
      estado: nuevoEstado.value,
    })
    await api.post(`/pedidos/${selectedPedido.value.id}/tracking`, {
      estado: nuevoEstado.value,
      descripcion: descripcion.value || `Estado cambiado a ${nuevoEstado.value}`,
    })
    showModal.value = false
    await loadPedidos()
  } catch {
  } finally {
    updating.value = false
  }
}

onMounted(() => {
  loadPedidos()
})
</script>
