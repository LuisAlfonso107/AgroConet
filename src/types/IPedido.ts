export type PedidoEstado = 'solicitado' | 'confirmado' | 'en puerto' | 'en tránsito' | 'entregado' | 'rechazado' | 'cancelado'

export interface IPedidoResumen {
  id: number | string
  productoId: number
  nombreProducto: string
  compradorId: number | string
  productor: string
  cantidadQuintales: number
  precioUnitario: number
  total: number
  estado: PedidoEstado
  createdAt: string
}

export interface IPedidoDetalle extends IPedidoResumen {
  compradorNombre?: string
  productorId?: number | string
  productorTelefono?: string
  productorUbicacion?: string
  productorCalificacion?: number
  agenciaNombre?: string
  agenciaContacto?: string
  tipo?: string
  variedad?: string
  certificaciones?: string[]
  impuestos?: number
}

export interface PedidoFiltros {
  estado: string
  fechaInicio: string
  fechaFin: string
  busqueda: string
}
