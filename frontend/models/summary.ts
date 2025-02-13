import type { IUser } from './user'

export interface ISummary {
  id: number
  title: string
  summary: string
  author: IUser | null
  category: string
  contentType: string
  userPrompt: string
  likes: number
  dislikes: number
  favorites: number
  tags: string[]
  isPrivate: boolean
  url: string
  rawText: string
  createdAt: Date
}

export function mapSummary(summary: any): ISummary {
  return {
    id: summary?.id || 0,
    title: summary?.title || '',
    summary: summary?.summary || '',
    author: summary?.author || null,
    category: summary?.category || '',
    contentType: summary?.content_type || '',
    userPrompt: summary?.user_prompt || '',
    likes: summary?.likes || 0,
    dislikes: summary?.dislikes || 0,
    favorites: summary?.favorites || 0,
    tags: summary?.tags || [],
    isPrivate: summary?.is_private || false,
    url: summary?.url || '',
    rawText: summary?.raw_text || '',
    createdAt: mapDate(summary?.created_at || new Date()),
  }
}

function mapDate(date: string | Date): Date {
  return new Date(date)
}
