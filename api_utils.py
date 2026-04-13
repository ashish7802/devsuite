# API Directory lib/utils.ts
api_utils = '''import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export interface API {
  id: string
  name: string
  category: string
  description: string
  base_url: string
  auth_type: 'none' | 'apikey' | 'oauth'
  docs_url: string
  example_endpoint: string
  tags: string[]
  status: 'online' | 'offline' | 'unknown'
}

export const CATEGORIES = [
  'All',
  'Weather',
  'Finance',
  'AI',
  'Maps',
  'Entertainment',
  'Social',
  'Developer Tools',
  'News',
  'Science',
  'Data',
  'Food & Drink',
  'Books',
  'Images',
  'Security',
  'Games'
] as const

export type Category = typeof CATEGORIES[number]

export function getAuthBadgeColor(authType: string): string {
  switch (authType) {
    case 'none':
      return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
    case 'apikey':
      return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400'
    case 'oauth':
      return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
    default:
      return 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-400'
  }
}

export function generateCurlExample(api: API): string {
  const url = api.base_url + api.example_endpoint
  
  if (api.auth_type === 'apikey') {
    return `curl "${url}" \\\
  -H "Authorization: Bearer YOUR_API_KEY"`
  } else if (api.auth_type === 'oauth') {
    return `curl "${url}" \\\
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"`
  }
  
  return `curl "${url}"`
}

export function generateFetchExample(api: API): string {
  const url = api.base_url + api.example_endpoint
  
  let headers = ''
  if (api.auth_type === 'apikey') {
    headers = `, {
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY'
  }
}`
  } else if (api.auth_type === 'oauth') {
    headers = `, {
  headers: {
    'Authorization': 'Bearer YOUR_ACCESS_TOKEN'
  }
}`
  }
  
  return `fetch('${url}'${headers})
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));`
}
'''

with open(f"{base_path}/packages/api-directory/lib/utils.ts", "w") as f:
    f.write(api_utils)

print("✅ API Directory utils.ts created")
