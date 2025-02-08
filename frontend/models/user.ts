export interface IUser {
  username: string
  email: string
  favorites: any[]
}

export function mapUser(user: any): IUser {
  return {
    username: user?.username || '',
    email: user?.email || '',
    favorites: user?.favorites || [],
  }
}
