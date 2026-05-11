export type UserRole = 'comprador' | 'productor' | 'agencia'

export interface IUserBase {
  id: number | string
  name: string
  email: string
  userType: UserRole
  password?: string
  createdAt?: string
}

export interface IUser extends IUserBase {
  telefono?: string
  fotoPerfil?: string
  empresa?: string
  direccionEnvio?: string
  direccionesEnvio?: string[]
  pais?: string
  preferenciasNotificacion?: {
    email: boolean
    whatsapp: boolean
  }
  finca?: string
  ubicacion?: string
  descripcion?: string
}
