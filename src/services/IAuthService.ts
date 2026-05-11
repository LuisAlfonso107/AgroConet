import type { IUser } from '../types/IUser'

export interface IAuthService {
  getUser(id: number | string): Promise<IUser>
  updateUser(id: number | string, payload: Partial<IUser>): Promise<IUser>
}
