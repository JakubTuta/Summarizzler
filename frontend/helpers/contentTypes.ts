export const contentTypes = [
  { title: 'Text', value: 'text' },
  { title: 'Website', value: 'website' },
  { title: 'PDF', value: 'pdf' },
  { title: 'Video', value: 'video' },
]

export function getContentType(value: string): { title: string, value: string } | null {
  return contentTypes.find(contentType => contentType.value === value) ?? null
}

const contentTypeColors: Record<string, string> = {
  text: 'purple',
  website: 'green',
  pdf: 'orange',
  video: 'blue',
}

export function getContentTypeColor(contentType: string): string {
  return contentTypeColors[contentType] ?? 'grey'
}
