
# Root package.json
root_package = '''{
  "name": "devsuite",
  "version": "1.0.0",
  "description": "The Developer's Swiss Army Knife - A collection of essential developer tools",
  "private": true,
  "workspaces": [
    "packages/*"
  ],
  "scripts": {
    "build": "npm run build --workspaces",
    "test": "npm run test --workspaces",
    "lint": "npm run lint --workspaces",
    "dev:cli": "npm run dev -w packages/cli",
    "dev:web": "npm run dev -w packages/web",
    "dev:api": "npm run dev -w packages/api-directory",
    "install:all": "npm install && npm install --workspaces"
  },
  "repository": {
    "type": "git",
    "url": "https://github.com/yourusername/devsuite.git"
  },
  "keywords": [
    "developer-tools",
    "cli",
    "snippets",
    "api-directory",
    "monorepo",
    "productivity"
  ],
  "author": "DevSuite Team",
  "license": "MIT",
  "engines": {
    "node": ">=18.0.0"
  }
}
'''

with open(f"{base_path}/package.json", "w") as f:
    f.write(root_package)

# Root .gitignore
gitignore = '''# Dependencies
node_modules/
.pnp
.pnp.js

# Production builds
dist/
build/
.next/
out/

# Environment files
.env
.env.local
.env.*.local

# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
lerna-debug.log*

# OS files
.DS_Store
Thumbs.db

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# Testing
coverage/
.nyc_output/

# Misc
.cache/
temp/
tmp/
*.tgz
'''

with open(f"{base_path}/.gitignore", "w") as f:
    f.write(gitignore)

# LICENSE
license_content = '''MIT License

Copyright (c) 2024 DevSuite Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

with open(f"{base_path}/LICENSE", "w") as f:
    f.write(license_content)

print("✅ Root package.json, .gitignore, and LICENSE created")
