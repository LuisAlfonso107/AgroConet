export type ProductoEstado = 'disponible' | 'agotado' | 'pausado'
export type ProductoTipo = 'cafe' | 'maiz' | 'frijol' | 'arroz' | 'otros'

export interface IProductoBase {
  id: number | string
  nombre: string
  tipo: ProductoTipo
  precio: number
  stock: number
  estado: ProductoEstado
  productor: string
}

export interface IProducto extends IProductoBase {
  productorId: number | string
  humedad: number
  variedad: string
  region: string
  pais: string
  altura: string
  certificaciones: string[]
  descripcion?: string
  imagen?: string
  lat?: number
  lon?: number
  createdAt: string
}

export interface IProductoForm {
  nombre: string
  tipo: ProductoTipo
  precio: number | null
  stock: number | null
  humedad: number | null
  variedad: string
  region: string
  pais: string
  altura: string
  certificaciones: string[]
  descripcion: string
  imagen: string
}
