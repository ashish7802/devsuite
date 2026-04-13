# API Directory page.tsx
api_page = ''''use client'

import { useState, useEffect, useMemo } from 'react'
import { Search, Globe, Key, Lock, Unlock, ExternalLink, Copy, Check, Code, Moon, Sun, Zap } from 'lucide-react'
import { API, CATEGORIES, Category, getAuthBadgeColor, generateCurlExample, generateFetchExample } from '@/lib/utils'
import { cn } from '@/lib/utils'
import apisData from '@/data/apis.json'

export default function APIDirectory() {
  const [apis, setApis] = useState<API[]>(apisData as API[])
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState<Category>('All')
  const [isDarkMode, setIsDarkMode] = useState(false)
  const [selectedAPI, setSelectedAPI] = useState<API | null>(null)
  const [copiedEndpoint, setCopiedEndpoint] = useState<string | null>(null)
  const [statusMap, setStatusMap] = useState<Record<string, 'online' | 'offline' | 'unknown'>>({})

  // Load theme preference
  useEffect(() => {
    const darkMode = localStorage.getItem('devsuite-api-darkmode') === 'true'
    setIsDarkMode(darkMode)
    if (darkMode) {
      document.documentElement.classList.add('dark')
    }
  }, [])

  // Toggle dark mode
  const toggleDarkMode = () => {
    const newMode = !isDarkMode
    setIsDarkMode(newMode)
    localStorage.setItem('devsuite-api-darkmode', String(newMode))
    document.documentElement.classList.toggle('dark', newMode)
  }

  // Check API status
  useEffect(() => {
    const checkStatus = async (api: API) => {
      try {
        // For APIs that support CORS and are safe to check
        const controller = new AbortController()
        const timeoutId = setTimeout(() => controller.abort(), 5000)
        
        // Try HEAD request first
        let response
        try {
          response = await fetch(api.base_url, {
            method: 'HEAD',
            signal: controller.signal,
            mode: 'no-cors'
          })
        } catch {
          // If HEAD fails, try GET
          try {
            response = await fetch(api.base_url, {
              method: 'GET',
              signal: controller.signal,
              mode: 'no-cors'
            })
          } catch {
            // Mark as unknown if we can't determine
            setStatusMap(prev => ({ ...prev, [api.id]: 'unknown' }))
            return
          }
        }
        
        clearTimeout(timeoutId)
        
        // Since we're using no-cors, we can't read the status
        // So we'll mark as online if no error was thrown
        setStatusMap(prev => ({ ...prev, [api.id]: 'online' }))
      } catch {
        setStatusMap(prev => ({ ...prev, [api.id]: 'offline' }))
      }
    }

    // Check status for a subset of APIs (first 10 to avoid rate limiting)
    apis.slice(0, 10).forEach(api => {
      checkStatus(api)
    })
  }, [apis])

  // Filter APIs
  const filteredAPIs = useMemo(() => {
    return apis.filter(api => {
      const matchesSearch = 
        api.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        api.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
        api.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()))
      
      const matchesCategory = selectedCategory === 'All' || api.category === selectedCategory
      
      return matchesSearch && matchesCategory
    })
  }, [apis, searchQuery, selectedCategory])

  // Get status color
  const getStatusColor = (apiId: string) => {
    const status = statusMap[apiId]
    if (status === 'online') return 'bg-green-500'
    if (status === 'offline') return 'bg-red-500'
    return 'bg-yellow-500'
  }

  // Copy to clipboard
  const copyToClipboard = async (text: string, type: string) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopiedEndpoint(type)
      setTimeout(() => setCopiedEndpoint(null), 2000)
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border sticky top-0 z-10 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-primary to-primary/70 rounded-xl flex items-center justify-center">
                <Globe className="w-6 h-6 text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-foreground">API Graveyard</h1>
                <p className="text-xs text-muted-foreground">{apis.length}+ Free Public APIs</p>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={toggleDarkMode}
                className="p-2 rounded-lg hover:bg-muted transition-colors"
                title="Toggle dark mode"
              >
                {isDarkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Search and Filter */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
            <input
              type="text"
              placeholder="Search APIs by name, description, or tags..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 bg-background border border-input rounded-lg focus:outline-none focus:ring-2 focus:ring-ring"
            />
          </div>
          
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value as Category)}
            className="px-4 py-2 bg-background border border-input rounded-lg focus:outline-none focus:ring-2 focus:ring-ring"
          >
            {CATEGORIES.map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
        </div>

        {/* Stats */}
        <div className="mt-4 flex items-center gap-4 text-sm text-muted-foreground">
          <span>{filteredAPIs.length} APIs found</span>
          {selectedCategory !== 'All' && (
            <span className="px-2 py-1 bg-muted rounded-full text-xs">
              Category: {selectedCategory}
            </span>
          )}
          <div className="flex items-center gap-4 ml-auto">
            <span className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-green-500"></span>
              Online
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-red-500"></span>
              Offline
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-yellow-500"></span>
              Unknown
            </span>
          </div>
        </div>
      </div>

      {/* API Grid */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
        {filteredAPIs.length === 0 ? (
          <div className="text-center py-20">
            <Globe className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-lg font-medium text-foreground">No APIs found</h3>
            <p className="text-muted-foreground mt-2">Try adjusting your search or filters.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredAPIs.map(api => (
              <APICard
                key={api.id}
                api={api}
                statusColor={getStatusColor(api.id)}
                onClick={() => setSelectedAPI(api)}
              />
            ))}
          </div>
        )}
      </main>

      {/* API Detail Modal */}
      {selectedAPI && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
          <div className="bg-background rounded-xl shadow-2xl w-full max-w-3xl max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b border-border">
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div className={cn("w-3 h-3 rounded-full", getStatusColor(selectedAPI.id))} />
                  <div>
                    <h2 className="text-2xl font-bold">{selectedAPI.name}</h2>
                    <p className="text-muted-foreground">{selectedAPI.category}</p>
                  </div>
                </div>
                <button 
                  onClick={() => setSelectedAPI(null)}
                  className="p-2 hover:bg-muted rounded-lg"
                >
                  <span className="sr-only">Close</span>
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>

            <div className="p-6 space-y-6">
              <p className="text-foreground">{selectedAPI.description}</p>

              <div className="flex flex-wrap gap-2">
                <span className={cn("px-3 py-1 rounded-full text-sm font-medium", getAuthBadgeColor(selectedAPI.auth_type))}>
                  {selectedAPI.auth_type === 'none' && <Unlock className="w-3.5 h-3.5 inline mr-1" />}
                  {selectedAPI.auth_type === 'apikey' && <Key className="w-3.5 h-3.5 inline mr-1" />}
                  {selectedAPI.auth_type === 'oauth' && <Lock className="w-3.5 h-3.5 inline mr-1" />}
                  {selectedAPI.auth_type === 'none' ? 'No Auth' : selectedAPI.auth_type === 'apikey' ? 'API Key' : 'OAuth'}
                </span>
                {selectedAPI.tags.map(tag => (
                  <span key={tag} className="px-3 py-1 bg-muted text-muted-foreground rounded-full text-sm">
                    {tag}
                  </span>
                ))}
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Base URL</label>
                <div className="flex gap-2">
                  <code className="flex-1 p-3 bg-muted rounded-lg text-sm font-mono break-all">
                    {selectedAPI.base_url}
                  </code>
                  <button
                    onClick={() => copyToClipboard(selectedAPI.base_url, 'baseurl')}
                    className="px-3 py-2 bg-secondary hover:bg-secondary/80 rounded-lg transition-colors"
                  >
                    {copiedEndpoint === 'baseurl' ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Example Endpoint</label>
                <code className="block p-3 bg-muted rounded-lg text-sm font-mono break-all">
                  {selectedAPI.example_endpoint}
                </code>
              </div>

              <div className="space-y-3">
                <label className="text-sm font-medium flex items-center gap-2">
                  <Code className="w-4 h-4" />
                  Code Examples
                </label>
                
                <div className="space-y-2">
                  <p className="text-xs text-muted-foreground">cURL</p>
                  <div className="relative">
                    <pre className="p-3 bg-muted rounded-lg text-sm font-mono overflow-x-auto">
                      {generateCurlExample(selectedAPI)}
                    </pre>
                    <button
                      onClick={() => copyToClipboard(generateCurlExample(selectedAPI), 'curl')}
                      className="absolute top-2 right-2 p-1.5 bg-background/80 hover:bg-background rounded"
                    >
                      {copiedEndpoint === 'curl' ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                    </button>
                  </div>
                </div>

                <div className="space-y-2">
                  <p className="text-xs text-muted-foreground">JavaScript Fetch</p>
                  <div className="relative">
                    <pre className="p-3 bg-muted rounded-lg text-sm font-mono overflow-x-auto">
                      {generateFetchExample(selectedAPI)}
                    </pre>
                    <button
                      onClick={() => copyToClipboard(generateFetchExample(selectedAPI), 'fetch')}
                      className="absolute top-2 right-2 p-1.5 bg-background/80 hover:bg-background rounded"
                    >
                      {copiedEndpoint === 'fetch' ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                    </button>
                  </div>
                </div>
              </div>

              <a
                href={selectedAPI.docs_url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
              >
                <ExternalLink className="w-4 h-4" />
                View Documentation
              </a>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

// API Card Component
function APICard({ 
  api, 
  statusColor,
  onClick 
}: { 
  api: API
  statusColor: string
  onClick: () => void
}) {
  return (
    <div 
      onClick={onClick}
      className="group bg-card border border-border rounded-xl p-5 hover:shadow-lg transition-all cursor-pointer hover:border-primary/50"
    >
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2">
          <div className={cn("w-2.5 h-2.5 rounded-full", statusColor)} />
          <h3 className="font-semibold text-foreground group-hover:text-primary transition-colors">
            {api.name}
          </h3>
        </div>
        <span className={cn("px-2 py-0.5 rounded-full text-xs font-medium", getAuthBadgeColor(api.auth_type))}>
          {api.auth_type === 'none' ? 'Free' : api.auth_type}
        </span>
      </div>

      <p className="text-sm text-muted-foreground mb-4 line-clamp-2">{api.description}</p>

      <div className="flex items-center justify-between">
        <span className="text-xs text-muted-foreground">{api.category}</span>
        <div className="flex gap-1">
          {api.tags.slice(0, 2).map(tag => (
            <span key={tag} className="px-2 py-0.5 bg-muted text-muted-foreground rounded text-xs">
              {tag}
            </span>
          ))}
          {api.tags.length > 2 && (
            <span className="px-2 py-0.5 bg-muted text-muted-foreground rounded text-xs">
              +{api.tags.length - 2}
            </span>
          )}
        </div>
      </div>
    </div>
  )
}
'''

with open(f"{base_path}/packages/api-directory/app/page.tsx", "w") as f:
    f.write(api_page)

# API Directory README.md
api_readme = '''# API Graveyard

A curated directory of 50+ free public APIs with live status checking.

## Features

- 📚 55+ curated free/public APIs
- 🔍 Search by name, description, or tags
- 🏷️ Filter by category (Weather, Finance, AI, Maps, etc.)
- 🟢 Live status checking (green/red/yellow indicators)
- 📋 Copy base URL and code examples
- 💻 cURL and JavaScript fetch examples
- 🔐 Auth type badges (None, API Key, OAuth)
- 🌙 Dark/light mode

## Getting Started

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

Open [http://localhost:3001](http://localhost:3001) with your browser.

## API Data

APIs are stored in `data/apis.json`. Each API entry includes:

```json
{
  "id": "1",
  "name": "API Name",
  "category": "Category",
  "description": "Description",
  "base_url": "https://api.example.com",
  "auth_type": "none|apikey|oauth",
  "docs_url": "https://docs.example.com",
  "example_endpoint": "/endpoint",
  "tags": ["tag1", "tag2"]
}
```

## Adding a New API

1. Edit `data/apis.json`
2. Add a new entry following the schema
3. Submit a PR

## Technologies

- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- SWR (for data fetching)
- Lucide React (icons)
'''

with open(f"{base_path}/packages/api-directory/README.md", "w") as f:
    f.write(api_readme)

print("✅ API Directory page.tsx and README created")
