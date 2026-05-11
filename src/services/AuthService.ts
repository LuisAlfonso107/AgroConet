import { useApi } from '../composables/useApi'
import type { IAuthService } from './IAuthService'
import type { IUser } from '../types/IUser'

export class AuthService implements IAuthService {
  private api = useApi().api

  async getUser(id: number | string): Promise<IUser> {
    const response = await this.api.get<IUser>(`/users/${id}`)
    return response.data
  }

  async updateUser(id: number | string, payload: Partial<IUser>): Promise<IUser> {
    const response = await this.api.patch<IUser>(`/users/${id}`, payload)
    return response.data
  }
}
