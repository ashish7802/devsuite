
# Web lib/utils.ts
web_utils = '''import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export interface Snippet {
  id: string
  title: string
  code: string
  language: string
  tags: string[]
  description: string
  createdAt: string
  updatedAt: string
}

export const LANGUAGES = [
  'javascript',
  'typescript',
  'python',
  'go',
  'rust',
  'java',
  'cpp',
  'c',
  'csharp',
  'php',
  'ruby',
  'swift',
  'kotlin',
  'sql',
  'bash',
  'powershell',
  'html',
  'css',
  'scss',
  'json',
  'yaml',
  'markdown',
  'dockerfile',
  'nginx',
  'vim',
  'lua',
  'perl',
  'r',
  'dart',
  'elixir',
  'haskell',
  'clojure',
  'scala',
  'groovy',
  'julia',
  'matlab',
  'octave',
  'pascal',
  'delphi',
  'fortran',
  'cobol',
  'erlang',
  'ocaml',
  'fsharp',
  'scheme',
  'racket',
  'prolog',
  'smalltalk',
  'ada',
  'lisp',
  'basic',
  'vbnet',
  'apex',
  'solidity',
  'vyper',
  'move',
  'cairo',
  'noir',
  'circom',
  'text'
] as const

export type Language = typeof LANGUAGES[number]

export function generateId(): string {
  return Math.random().toString(36).substring(2, 15)
}

export function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}
'''

with open(f"{base_path}/packages/web/lib/utils.ts", "w") as f:
    f.write(web_utils)

print("✅ Web utils.ts created")
