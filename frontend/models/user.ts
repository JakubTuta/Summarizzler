export interface IUser {
  id: string
  username: string
  email: string
  favorites: string[]
  likes: string[]
  dislikes: string[]
}

export function mapUser(user: Partial<IUser>): IUser {
  return {
    id: user?.id || '',
    username: user?.username || '',
    email: user?.email || '',
    favorites: user?.favorites?.map(String) || [],
    likes: user?.likes?.map(String) || [],
    dislikes: user?.dislikes?.map(String) || [],
  }
}
