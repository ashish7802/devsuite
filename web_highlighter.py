
# Web highlighter.ts (Shiki syntax highlighter)
web_highlighter = '''import { getHighlighter, Highlighter } from 'shiki'

class ShikiHighlighter {
  private highlighter: Highlighter | null = null
  private initPromise: Promise<void> | null = null

  async init() {
    if (this.initPromise) return this.initPromise
    
    this.initPromise = (async () => {
      this.highlighter = await getHighlighter({
        themes: ['github-dark', 'github-light'],
        langs: [
          'javascript', 'typescript', 'python', 'go', 'rust', 'java',
          'cpp', 'c', 'csharp', 'php', 'ruby', 'swift', 'kotlin',
          'sql', 'bash', 'powershell', 'html', 'css', 'scss',
          'json', 'yaml', 'markdown', 'dockerfile', 'nginx',
          'vim', 'lua', 'perl', 'r', 'dart', 'elixir', 'haskell',
          'clojure', 'scala', 'groovy', 'julia', 'matlab',
          'pascal', 'erlang', 'ocaml', 'fsharp', 'scheme',
          'prolog', 'ada', 'lisp', 'basic', 'fortran', 'text'
        ]
      })
    })()
    
    return this.initPromise
  }

  async highlight(code: string, lang: string): Promise<string> {
    await this.init()
    
    if (!this.highlighter) {
      return `<pre>${code}</pre>`
    }

    const isDark = document.documentElement.classList.contains('dark')
    const theme = isDark ? 'github-dark' : 'github-light'

    try {
      const html = this.highlighter.codeToHtml(code, {
        lang: lang === 'text' ? 'plaintext' : lang,
        theme
      })
      return html
    } catch (err) {
      // Fallback for unsupported languages
      return `<pre class="shiki" style="background-color: ${isDark ? '#24292e' : '#ffffff'}; color: ${isDark ? '#e1e4e8' : '#24292e'}"><code>${code}</code></pre>`
    }
  }
}

export const shikiHighlighter = new ShikiHighlighter()
'''

with open(f"{base_path}/packages/web/lib/highlighter.ts", "w") as f:
    f.write(web_highlighter)

# Web README.md
web_readme = '''# Snippet Vault

A beautiful, fast code snippet manager built with Next.js 14 and Shiki syntax highlighting.

## Features

- ✨ Save code snippets with title, language, tags, and description
- 🎨 Syntax highlighting for 50+ languages using Shiki
- 🔍 Instant search by title, tags, or description
- 📋 One-click copy to clipboard
- 🌙 Dark/light mode toggle
- 📤 Export all snippets as JSON
- 📥 Import snippets from JSON
- 🏷️ Language filter dropdown
- ⌨️ Keyboard shortcut (Ctrl+K) for search
- 💾 All data stored locally in browser

## Getting Started

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

Open [http://localhost:3000](http://localhost:3000) with your browser.

## Usage

1. Click "Add Snippet" to create a new snippet
2. Fill in the title, language, tags, and code
3. Use the search bar (Ctrl+K) to find snippets
4. Filter by language using the dropdown
5. Click the copy button to copy code to clipboard
6. Export your snippets as JSON for backup
7. Import snippets from JSON files

## Technologies

- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Shiki (syntax highlighting)
- Lucide React (icons)
- Radix UI (primitives)
'''

with open(f"{base_path}/packages/web/README.md", "w") as f:
    f.write(web_readme)

print("✅ Web highlighter.ts and README created")
