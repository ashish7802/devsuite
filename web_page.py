
# Web page.tsx (main app)
web_page = ''''use client'

import { useState, useEffect, useCallback } from 'react'
import { Search, Plus, Moon, Sun, Download, Upload, Code2, Tag, X, Edit2, Trash2, Copy, Check } from 'lucide-react'
import { Snippet, LANGUAGES, Language, generateId, formatDate } from '@/lib/utils'
import { cn } from '@/lib/utils'
import { shikiHighlighter } from '@/lib/highlighter'

export default function SnippetVault() {
  const [snippets, setSnippets] = useState<Snippet[]>([])
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedLanguage, setSelectedLanguage] = useState<string>('all')
  const [isDarkMode, setIsDarkMode] = useState(false)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingSnippet, setEditingSnippet] = useState<Snippet | null>(null)
  const [copiedId, setCopiedId] = useState<string | null>(null)

  // Form state
  const [formData, setFormData] = useState({
    title: '',
    code: '',
    language: 'javascript' as Language,
    tags: '',
    description: ''
  })

  // Load snippets from localStorage
  useEffect(() => {
    const stored = localStorage.getItem('devsuite-snippets')
    if (stored) {
      try {
        setSnippets(JSON.parse(stored))
      } catch (e) {
        console.error('Failed to parse snippets:', e)
      }
    }

    // Load theme preference
    const darkMode = localStorage.getItem('devsuite-darkmode') === 'true'
    setIsDarkMode(darkMode)
    if (darkMode) {
      document.documentElement.classList.add('dark')
    }
  }, [])

  // Save snippets to localStorage
  useEffect(() => {
    localStorage.setItem('devsuite-snippets', JSON.stringify(snippets))
  }, [snippets])

  // Toggle dark mode
  const toggleDarkMode = () => {
    const newMode = !isDarkMode
    setIsDarkMode(newMode)
    localStorage.setItem('devsuite-darkmode', String(newMode))
    document.documentElement.classList.toggle('dark', newMode)
  }

  // Filter snippets
  const filteredSnippets = snippets.filter(snippet => {
    const matchesSearch = 
      snippet.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      snippet.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase())) ||
      snippet.description.toLowerCase().includes(searchQuery.toLowerCase())
    
    const matchesLanguage = selectedLanguage === 'all' || snippet.language === selectedLanguage
    
    return matchesSearch && matchesLanguage
  })

  // Add or update snippet
  const saveSnippet = () => {
    if (!formData.title.trim() || !formData.code.trim()) return

    const now = new Date().toISOString()
    const tags = formData.tags.split(',').map(t => t.trim()).filter(Boolean)

    if (editingSnippet) {
      setSnippets(prev => prev.map(s => 
        s.id === editingSnippet.id 
          ? { ...s, ...formData, tags, updatedAt: now }
          : s
      ))
    } else {
      const newSnippet: Snippet = {
        id: generateId(),
        ...formData,
        tags,
        createdAt: now,
        updatedAt: now
      }
      setSnippets(prev => [newSnippet, ...prev])
    }

    closeModal()
  }

  // Delete snippet
  const deleteSnippet = (id: string) => {
    if (confirm('Are you sure you want to delete this snippet?')) {
      setSnippets(prev => prev.filter(s => s.id !== id))
    }
  }

  // Edit snippet
  const editSnippet = (snippet: Snippet) => {
    setEditingSnippet(snippet)
    setFormData({
      title: snippet.title,
      code: snippet.code,
      language: snippet.language as Language,
      tags: snippet.tags.join(', '),
      description: snippet.description
    })
    setIsModalOpen(true)
  }

  // Close modal
  const closeModal = () => {
    setIsModalOpen(false)
    setEditingSnippet(null)
    setFormData({
      title: '',
      code: '',
      language: 'javascript',
      tags: '',
      description: ''
    })
  }

  // Copy to clipboard
  const copyToClipboard = async (code: string, id: string) => {
    try {
      await navigator.clipboard.writeText(code)
      setCopiedId(id)
      setTimeout(() => setCopiedId(null), 2000)
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  // Export snippets
  const exportSnippets = () => {
    const dataStr = JSON.stringify(snippets, null, 2)
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr)
    const exportFileDefaultName = `snippets-${new Date().toISOString().split('T')[0]}.json`
    
    const linkElement = document.createElement('a')
    linkElement.setAttribute('href', dataUri)
    linkElement.setAttribute('download', exportFileDefaultName)
    linkElement.click()
  }

  // Import snippets
  const importSnippets = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    const reader = new FileReader()
    reader.onload = (e) => {
      try {
        const imported = JSON.parse(e.target?.result as string)
        if (Array.isArray(imported)) {
          setSnippets(prev => [...imported, ...prev])
          alert(`Imported ${imported.length} snippets!`)
        }
      } catch (err) {
        alert('Invalid JSON file')
      }
    }
    reader.readAsText(file)
    event.target.value = ''
  }

  // Keyboard shortcut: Ctrl+K for search
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault()
        document.getElementById('search-input')?.focus()
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border sticky top-0 z-10 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center">
                <Code2 className="w-6 h-6 text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-foreground">Snippet Vault</h1>
                <p className="text-xs text-muted-foreground">DevSuite</p>
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
              
              <label className="p-2 rounded-lg hover:bg-muted transition-colors cursor-pointer" title="Import snippets">
                <Upload className="w-5 h-5" />
                <input type="file" accept=".json" onChange={importSnippets} className="hidden" />
              </label>
              
              <button
                onClick={exportSnippets}
                className="p-2 rounded-lg hover:bg-muted transition-colors"
                title="Export snippets"
              >
                <Download className="w-5 h-5" />
              </button>

              <button
                onClick={() => setIsModalOpen(true)}
                className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
              >
                <Plus className="w-4 h-4" />
                <span className="hidden sm:inline">Add Snippet</span>
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
              id="search-input"
              type="text"
              placeholder="Search snippets... (Ctrl+K)"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 bg-background border border-input rounded-lg focus:outline-none focus:ring-2 focus:ring-ring"
            />
          </div>
          
          <select
            value={selectedLanguage}
            onChange={(e) => setSelectedLanguage(e.target.value)}
            className="px-4 py-2 bg-background border border-input rounded-lg focus:outline-none focus:ring-2 focus:ring-ring"
          >
            <option value="all">All Languages</option>
            {LANGUAGES.map(lang => (
              <option key={lang} value={lang}>{lang.charAt(0).toUpperCase() + lang.slice(1)}</option>
            ))}
          </select>
        </div>

        {/* Stats */}
        <div className="mt-4 flex items-center gap-4 text-sm text-muted-foreground">
          <span>{snippets.length} total snippets</span>
          {selectedLanguage !== 'all' && (
            <span className="px-2 py-1 bg-muted rounded-full text-xs">
              Filtered: {filteredSnippets.length}
            </span>
          )}
        </div>
      </div>

      {/* Snippets Grid */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
        {filteredSnippets.length === 0 ? (
          <div className="text-center py-20">
            <Code2 className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-lg font-medium text-foreground">No snippets found</h3>
            <p className="text-muted-foreground mt-2">
              {snippets.length === 0 
                ? "Get started by adding your first snippet!" 
                : "Try adjusting your search or filters."}
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
            {filteredSnippets.map(snippet => (
              <SnippetCard
                key={snippet.id}
                snippet={snippet}
                onEdit={() => editSnippet(snippet)}
                onDelete={() => deleteSnippet(snippet.id)}
                onCopy={() => copyToClipboard(snippet.code, snippet.id)}
                copied={copiedId === snippet.id}
              />
            ))}
          </div>
        )}
      </main>

      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
          <div className="bg-background rounded-xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between p-6 border-b border-border">
              <h2 className="text-xl font-semibold">
                {editingSnippet ? 'Edit Snippet' : 'Add New Snippet'}
              </h2>
              <button onClick={closeModal} className="p-2 hover:bg-muted rounded-lg">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Title</label>
                <input
                  type="text"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  placeholder="e.g., React useEffect Hook"
                  className="w-full px-3 py-2 border border-input rounded-lg focus:outline-none focus:ring-2 focus:ring-ring"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Language</label>
                  <select
                    value={formData.language}
                    onChange={(e) => setFormData({ ...formData, language: e.target.value as Language })}
                    className="w-full px-3 py-2 border border-input rounded-lg focus:outline-none focus:ring-2 focus:ring-ring"
                  >
                    {LANGUAGES.map(lang => (
                      <option key={lang} value={lang}>{lang.charAt(0).toUpperCase() + lang.slice(1)}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">Tags (comma separated)</label>
                  <input
                    type="text"
                    value={formData.tags}
                    onChange={(e) => setFormData({ ...formData, tags: e.target.value })}
                    placeholder="react, hooks, async"
                    className="w-full px-3 py-2 border border-input rounded-lg focus:outline-none focus:ring-2 focus:ring-ring"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Description</label>
                <input
                  type="text"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  placeholder="Brief description of what this snippet does..."
                  className="w-full px-3 py-2 border border-input rounded-lg focus:outline-none focus:ring-2 focus:ring-ring"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Code</label>
                <textarea
                  value={formData.code}
                  onChange={(e) => setFormData({ ...formData, code: e.target.value })}
                  placeholder="Paste your code here..."
                  rows={10}
                  className="w-full px-3 py-2 border border-input rounded-lg focus:outline-none focus:ring-2 focus:ring-ring font-mono text-sm"
                />
              </div>
            </div>

            <div className="flex justify-end gap-3 p-6 border-t border-border">
              <button
                onClick={closeModal}
                className="px-4 py-2 text-muted-foreground hover:text-foreground transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={saveSnippet}
                disabled={!formData.title.trim() || !formData.code.trim()}
                className="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {editingSnippet ? 'Update' : 'Save'} Snippet
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

// Snippet Card Component
function SnippetCard({ 
  snippet, 
  onEdit, 
  onDelete, 
  onCopy,
  copied 
}: { 
  snippet: Snippet
  onEdit: () => void
  onDelete: () => void
  onCopy: () => void
  copied: boolean
}) {
  const [highlightedCode, setHighlightedCode] = useState('')

  useEffect(() => {
    const highlight = async () => {
      try {
        const html = await shikiHighlighter.highlight(snippet.code, snippet.language)
        setHighlightedCode(html)
      } catch (err) {
        setHighlightedCode(`<pre>${snippet.code}</pre>`)
      }
    }
    highlight()
  }, [snippet.code, snippet.language])

  return (
    <div className="group bg-card border border-border rounded-xl overflow-hidden hover:shadow-lg transition-shadow">
      <div className="p-4 border-b border-border">
        <div className="flex items-start justify-between">
          <div>
            <h3 className="font-semibold text-foreground">{snippet.title}</h3>
            <p className="text-sm text-muted-foreground mt-1">{snippet.description}</p>
          </div>
          <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
            <button
              onClick={onEdit}
              className="p-1.5 hover:bg-muted rounded-lg text-muted-foreground hover:text-foreground"
              title="Edit"
            >
              <Edit2 className="w-4 h-4" />
            </button>
            <button
              onClick={onDelete}
              className="p-1.5 hover:bg-destructive/10 rounded-lg text-muted-foreground hover:text-destructive"
              title="Delete"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        </div>

        <div className="flex items-center gap-2 mt-3 flex-wrap">
          <span className="px-2 py-1 bg-primary/10 text-primary text-xs rounded-full font-medium">
            {snippet.language}
          </span>
          {snippet.tags.map(tag => (
            <span key={tag} className="px-2 py-1 bg-muted text-muted-foreground text-xs rounded-full flex items-center gap-1">
              <Tag className="w-3 h-3" />
              {tag}
            </span>
          ))}
        </div>
      </div>

      <div className="relative bg-muted/50">
        <button
          onClick={onCopy}
          className="absolute top-2 right-2 p-2 bg-background/90 backdrop-blur rounded-lg shadow-sm opacity-0 group-hover:opacity-100 transition-opacity hover:bg-background"
          title="Copy to clipboard"
        >
          {copied ? <Check className="w-4 h-4 text-green-500" /> : <Copy className="w-4 h-4" />}
        </button>

        <div 
          className="p-4 overflow-x-auto max-h-64 overflow-y-auto"
          dangerouslySetInnerHTML={{ __html: highlightedCode }}
        />
      </div>

      <div className="px-4 py-2 bg-muted/30 text-xs text-muted-foreground flex justify-between items-center">
        <span>Created {formatDate(snippet.createdAt)}</span>
        <span>{snippet.code.length} chars</span>
      </div>
    </div>
  )
}
'''

with open(f"{base_path}/packages/web/app/page.tsx", "w") as f:
    f.write(web_page)

print("✅ Web page.tsx created")
