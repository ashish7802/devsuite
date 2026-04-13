
# CLI package.json
cli_package = '''{
  "name": "devsuite-cli",
  "version": "1.0.0",
  "description": "DevToolkit CLI - A Swiss Army Knife for developers",
  "main": "src/index.js",
  "bin": {
    "devsuite": "./src/index.js"
  },
  "scripts": {
    "start": "node src/index.js",
    "dev": "node src/index.js",
    "test": "jest"
  },
  "keywords": [
    "cli",
    "developer-tools",
    "git",
    "productivity",
    "devsuite"
  ],
  "author": "DevSuite Team",
  "license": "MIT",
  "dependencies": {
    "commander": "^11.1.0",
    "chalk": "^5.3.0",
    "ora": "^7.0.1",
    "inquirer": "^9.2.12",
    "fs-extra": "^11.2.0",
    "clipboardy": "^4.0.0",
    "execa": "^8.0.1",
    "glob": "^10.3.10"
  },
  "engines": {
    "node": ">=18.0.0"
  }
}
'''

with open(f"{base_path}/packages/cli/package.json", "w") as f:
    f.write(cli_package)

# CLI README.md
cli_readme = '''# DevSuite CLI

A powerful command-line toolkit for developers that streamlines common development workflows.

## Installation

```bash
npm install -g devsuite-cli
```

## Commands

### Project Scaffolding
- `devsuite init <project-name>` - Scaffold a new project with templates

### Git Operations
- `devsuite git:sync` - Pull, auto-resolve conflicts, and push
- `devsuite git:undo` - Safely undo the last commit

### Environment Management
- `devsuite env:check` - Compare .env vs .env.example
- `devsuite env:gen` - Auto-generate .env.example from .env

### System Utilities
- `devsuite ports` - Show all ports in use with process names
- `devsuite clean` - Remove node_modules, __pycache__, .DS_Store recursively

### Snippet Management
- `devsuite snippet add <name>` - Save a code snippet from clipboard
- `devsuite snippet list` - List all saved snippets
- `devsuite snippet use <name>` - Copy snippet to clipboard

## Usage Examples

```bash
# Initialize a new React project
devsuite init my-app --template react

# Sync your git repository
devsuite git:sync

# Check environment variables
devsuite env:check

# Clean up project
devsuite clean

# Save a snippet from clipboard
devsuite snippet add "react-hook"
```
'''

with open(f"{base_path}/packages/cli/README.md", "w") as f:
    f.write(cli_readme)

print("✅ CLI package.json and README created")
