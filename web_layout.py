
# Web layout.tsx
web_layout = '''import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Snippet Vault - DevSuite',
  description: 'A beautiful code snippet manager for developers',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>{children}</body>
    </html>
  )
}
'''

with open(f"{base_path}/packages/web/app/layout.tsx", "w") as f:
    f.write(web_layout)

print("✅ Web layout.tsx created")
