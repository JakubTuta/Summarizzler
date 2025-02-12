import type { IUser } from './user'

export interface ISummary {
  id: number
  url: string
  title: string
  contentType: string
  summary: string
  author: IUser | null
  userPrompt: string
  isPrivate: boolean
  likes: number
  dislikes: number
  favorites: number
  tags: string[]
  createdAt: string
}

export function mapSummary(summary: any): ISummary {
  return {
    id: summary?.id || 0,
    url: summary?.url || '',
    title: summary?.title || '',
    contentType: summary?.content_type || '',
    summary: summary?.summary || '',
    author: summary?.author || null,
    userPrompt: summary?.user_prompt || '',
    isPrivate: summary?.is_private || false,
    likes: summary?.likes || 0,
    dislikes: summary?.dislikes || 0,
    favorites: summary?.favorites || 0,
    tags: summary?.tags || [],
    createdAt: summary?.created_at || '',
  }
}
