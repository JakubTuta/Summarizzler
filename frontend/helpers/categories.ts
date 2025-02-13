export const categories = [
  { title: 'Technology', value: 'technology' },
  { title: 'Business', value: 'business' },
  { title: 'Health & Wellness', value: 'health & wellness' },
  { title: 'Education', value: 'education' },
  { title: 'Lifestyle', value: 'lifestyle' },
  { title: 'Entertainment', value: 'entertainment' },
  { title: 'Science', value: 'science' },
  { title: 'Politics', value: 'politics' },
  { title: 'Art & Culture', value: 'art & culture' },
  { title: 'Sports', value: 'sports' },
  { title: 'Food & Drink', value: 'food & drink' },
  { title: 'Travel', value: 'travel' },
  { title: 'Other', value: 'other' },
]

export function getCategory(value: string): { title: string, value: string } | null {
  return categories.find(category => category.value === value) ?? null
}

const categoryColors: Record<string, string> = {
  'technology': 'indigo',
  'business': 'blue-grey',
  'health & wellness': 'teal',
  'education': 'deep-purple',
  'lifestyle': 'pink',
  'entertainment': 'deep-orange',
  'science': 'light-blue',
  'politics': 'red',
  'art & culture': 'purple',
  'sports': 'green',
  'food & drink': 'amber',
  'travel': 'cyan',
}

export function getCategoryColor(category: string): string {
  return categoryColors[category.toLowerCase()] ?? 'grey'
}
