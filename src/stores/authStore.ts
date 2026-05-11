import { ref } from 'vue'
import { AuthService } from '../services/AuthService'
import { useAuth } from '../composables/useAuth'
import type { IUser } from '../types/IUser'

const profile = ref<IUser | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)
const authService = new AuthService()

export function useAuthStore() {
  const { currentUser, setUser, logout } = useAuth()

  const loadProfile = async () => {
    if (!currentUser.value) return null
    loading.value = true
    error.value = null
    try {
      profile.value = await authService.getUser(currentUser.value.id)
      return profile.value
    } catch {
      error.value = 'No se pudo cargar el perfil'
      return null
    } finally {
      loading.value = false
    }
  }

  const saveProfile = async (payload: Partial<IUser>) => {
    if (!currentUser.value) return null
    loading.value = true
    error.value = null
    try {
      profile.value = await authService.updateUser(currentUser.value.id, payload)
      setUser({
        id: profile.value.id,
        name: profile.value.name,
        email: profile.value.email,
        userType: profile.value.userType,
      })
      return profile.value
    } catch {
      error.value = 'No se pudo guardar el perfil'
      return null
    } finally {
      loading.value = false
    }
  }

  return {
    currentUser,
    profile,
    loading,
    error,
    loadProfile,
    saveProfile,
    logout,
  }
}
