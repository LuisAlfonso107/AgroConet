import { useApi } from '../composables/useApi'
import type { IAuthService } from './IAuthService'
import type { IUser } from '../types/IUser'

export class AuthService implements IAuthService {
  private api = useApi().api

  async getUser(_id: number | string): Promise<IUser> {
    const response = await this.api.get('/users/me')
    return response.data.data
  }

  async updateUser(_id: number | string, payload: Partial<IUser>): Promise<IUser> {
    const response = await this.api.patch('/users/me', payload)
    return response.data.data
  }
}
