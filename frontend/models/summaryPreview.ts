import type { IUser } from './user'

export interface ISummaryPreview {
  id: string
  title: string
  summary: string
  author: IUser | null
  category: string
  contentType: string
  likes: number
  favorites: number
  isPrivate: boolean
  createdAt: Date
}

export function mapSummaryPreview(summary: any): ISummaryPreview {
  return {
    id: summary?.id || '',
    title: summary?.title || '',
    summary: summary?.summary || '',
    author: summary?.author || null,
    category: summary?.category || '',
    contentType: summary?.content_type || '',
    likes: summary?.likes || 0,
    favorites: summary?.favorites || 0,
    isPrivate: summary?.is_private || false,
    createdAt: new Date(summary?.created_at || new Date()),
  }
}
