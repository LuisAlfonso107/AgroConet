import { computed, ref } from 'vue'
import { useApi } from './useApi'

export type UserRole = 'comprador' | 'productor' | 'agencia'

export interface AuthUser {
  id: number | string
  name: string
  email: string
  userType: UserRole
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
    localStorage.removeItem('agroconet_access_token')
    localStorage.removeItem('agroconet_refresh_token')
    return
  }
  localStorage.setItem(STORAGE_KEY, JSON.stringify(user))
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
    const response = await api.post('/auth/login', { email, password })
    const { access_token, refresh_token, user } = response.data.data

    localStorage.setItem('agroconet_access_token', access_token)
    localStorage.setItem('agroconet_refresh_token', refresh_token)

    const authUser: AuthUser = {
      id: user.id,
      name: user.name,
      email: user.email,
      userType: user.user_type,
    }
    setUser(authUser)
    return authUser
  }

  const register = async (name: string, email: string, password: string, userType: UserRole): Promise<AuthUser> => {
    const response = await api.post('/auth/register', {
      name, email, password, user_type: userType,
    })
    const user = response.data.data
    const authUser: AuthUser = {
      id: user.id,
      name: user.name,
      email: user.email,
      userType: user.user_type,
    }
    return authUser
  }

  const logout = async () => {
    try {
      const token = localStorage.getItem('agroconet_refresh_token')
      if (token) {
        await api.post('/auth/logout', {}, {
          headers: { Authorization: `Bearer ${token}` },
        })
      }
    } catch {
    } finally {
      setUser(null)
    }
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
    register,
    logout,
    dashboardPathForRole,
  }
}
