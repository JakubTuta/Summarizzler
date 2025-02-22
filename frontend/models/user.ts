export interface IUser {
  id: string
  username: string
  email: string
  favorites: any[]
}

export function mapUser(user: any): IUser {
  return {
    id: user?.id || '',
    username: user?.username || '',
    email: user?.email || '',
    favorites: user?.favorites || [],
  }
}
