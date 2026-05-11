import { computed, ref } from 'vue'
import { useApi } from './useApi'

export type UserRole = 'comprador' | 'productor' | 'agencia'

export interface AuthUser {
  id: number | string
  name: string
  email: string
  userType: UserRole
}

interface UserRecord extends AuthUser {
  password?: string
  createdAt?: string
}

const STORAGE_KEY = 'agroconet_auth_user'

const currentUser = ref<AuthUser | null>(readStoredUser())

function readStoredUser(): AuthUser | null {
  try {
    const rawUser = localStorage.getItem(STORAGE_KEY)
    return rawUser ? JSON.parse(rawUser) as AuthUser : null
  } catch {
    return null
  }
}

function persistUser(user: AuthUser | null) {
  if (!user) {
    localStorage.removeItem(STORAGE_KEY)
    return
  }

  localStorage.setItem(STORAGE_KEY, JSON.stringify(user))
}

function toAuthUser(user: UserRecord): AuthUser {
  return {
    id: user.id,
    name: user.name,
    email: user.email,
    userType: user.userType,
  }
}

export function useAuth() {
  const { api } = useApi()
  const isAuthenticated = computed(() => currentUser.value !== null)
  const role = computed(() => currentUser.value?.userType ?? null)

  const setUser = (user: AuthUser | null) => {
    currentUser.value = user
    persistUser(user)
  }

  const login = async (email: string, password: string): Promise<AuthUser> => {
    const response = await api.get<UserRecord[]>('/users', {
      params: { email: email.trim().toLowerCase() },
    })
    const user = response.data[0]

    if (!user || (user.password && user.password !== password)) {
      throw new Error('Credenciales inválidas')
    }

    const authUser = toAuthUser(user)
    setUser(authUser)
    return authUser
  }

  const logout = () => {
    setUser(null)
  }

  const dashboardPathForRole = (userRole: UserRole) => {
    const paths: Record<UserRole, string> = {
      comprador: '/dashboard/comprador',
      productor: '/dashboard/productor',
      agencia: '/dashboard/agencia',
    }
    return paths[userRole]
  }

  return {
    currentUser,
    isAuthenticated,
    role,
    setUser,
    login,
    logout,
    dashboardPathForRole,
  }
}
