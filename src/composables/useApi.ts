import axios from 'axios'

function toCamelCase(str: string): string {
  return str.replace(/_([a-z])/g, (_, c) => c.toUpperCase())
}

function toSnakeCase(str: string): string {
  return str.replace(/[A-Z]/g, (c) => `_${c.toLowerCase()}`)
}

function transformKeys(obj: unknown, transform: (s: string) => string): unknown {
  if (Array.isArray(obj)) {
    return obj.map((item) => transformKeys(item, transform))
  }
  if (obj !== null && typeof obj === 'object') {
    const result: Record<string, unknown> = {}
    for (const [key, value] of Object.entries(obj)) {
      result[transform(key)] = transformKeys(value, transform)
    }
    return result
  }
  return obj
}

const api = axios.create({
  baseURL: 'http://localhost:3000/api',
  timeout: 10000,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('agroconet_access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  if (config.data && typeof config.data === 'object') {
    config.data = transformKeys(config.data, toSnakeCase)
  }
  if (config.params && typeof config.params === 'object') {
    config.params = transformKeys(config.params, toSnakeCase)
  }
  return config
})

api.interceptors.response.use(
  (response) => {
    if (response.data && typeof response.data === 'object') {
      response.data = transformKeys(response.data, toCamelCase)
    }
    return response
  },
  async (error) => {
    const originalRequest = error.config
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      const refreshToken = localStorage.getItem('agroconet_refresh_token')
      if (refreshToken) {
        try {
          const { data } = await axios.post('http://localhost:3000/api/auth/refresh', {}, {
            headers: { Authorization: `Bearer ${refreshToken}` },
          })
          localStorage.setItem('agroconet_access_token', data.data.access_token)
          originalRequest.headers.Authorization = `Bearer ${data.data.access_token}`
          return api(originalRequest)
        } catch {
          localStorage.removeItem('agroconet_access_token')
          localStorage.removeItem('agroconet_refresh_token')
          localStorage.removeItem('agroconet_auth_user')
          window.location.href = '/login'
        }
      }
    }
    return Promise.reject(error)
  }
)

export function useApi() {
  return { api }
}
