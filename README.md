<div align="center">

```
██████╗ ███████╗██╗   ██╗███████╗██╗   ██╗██╗████████╗███████╗
██╔══██╗██╔════╝██║   ██║██╔════╝██║   ██║██║╚══██╔══╝██╔════╝
██║  ██║█████╗  ██║   ██║███████╗██║   ██║██║   ██║   █████╗  
██║  ██║██╔══╝  ╚██╗ ██╔╝╚════██║██║   ██║██║   ██║   ██╔══╝  
██████╔╝███████╗ ╚████╔╝ ███████║╚██████╔╝██║   ██║   ███████╗
╚═════╝ ╚══════╝  ╚═══╝  ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   ╚══════╝
```

<h1>DevSuite</h1>

<p><strong>The Developer's Swiss Army Knife</strong></p>

<p>A collection of essential developer tools in a modern, open-source monorepo.</p>

[![npm version](https://badge.fury.io/js/devsuite-cli.svg)](https://www.npmjs.com/package/devsuite-cli)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/ashish7802/devsuite/pulls)
[![Made with Node.js](https://img.shields.io/badge/Made%20with-Node.js-green)](https://nodejs.org)
[![GitHub stars](https://img.shields.io/github/stars/ashish7802/devsuite?style=social)](https://github.com/ashish7802/devsuite)

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Contributing](#contributing) • [License](#license)

</div>

---

## ✨ What is DevSuite?

**DevSuite** is a comprehensive collection of developer tools designed to streamline your workflow and boost productivity. Built as a modern monorepo, it includes three powerful packages:

1. **🛠️ DevToolkit CLI** - A command-line Swiss Army Knife for developers
2. **📚 Snippet Vault** - A beautiful code snippet manager
3. **🌍 API Graveyard** - A curated directory of 50+ free public APIs

Whether you're scaffolding projects, managing environment variables, organizing code snippets, or discovering new APIs, DevSuite has you covered.

---

## 🚀 Features Overview

| Package | Description | Key Features |
|---------|-------------|--------------|
| **CLI** | Command-line toolkit | Project scaffolding, Git helpers, Env management, System utilities, Snippet manager |
| **Web** | Snippet Vault | Syntax highlighting, Search & filter, Import/Export, Dark mode, Keyboard shortcuts |
| **API Directory** | Public API catalog | 55+ APIs, Live status checking, Code examples, Category filtering |

---

## 📁 Monorepo Structure

```
devsuite/
├── 📦 packages/
│   ├── 🖥️ cli/                  # DevToolkit CLI (Node.js + Commander.js)
│   │   ├── src/
│   │   │   ├── commands/        # CLI command implementations
│   │   │   │   ├── init.js      # Project scaffolding
│   │   │   │   ├── git.js       # Git operations
│   │   │   │   ├── env.js       # Environment management
│   │   │   │   ├── system.js    # System utilities
│   │   │   │   └── snippet.js   # Snippet management
│   │   │   └── index.js         # CLI entry point
│   │   ├── package.json
│   │   └── README.md
│   │
│   ├── 🌐 web/                  # Snippet Vault (Next.js 14 + Tailwind)
│   │   ├── app/
│   │   │   ├── page.tsx         # Main application
│   │   │   ├── layout.tsx       # Root layout
│   │   │   └── globals.css      # Global styles
│   │   ├── lib/
│   │   │   ├── utils.ts         # Utility functions
│   │   │   └── highlighter.ts   # Shiki syntax highlighter
│   │   ├── package.json
│   │   └── README.md
│   │
│   └── 📡 api-directory/        # API Graveyard (Next.js 14 + SWR)
│       ├── app/
│       │   ├── page.tsx         # Main application
│       │   ├── layout.tsx       # Root layout
│       │   └── globals.css      # Global styles
│       ├── lib/
│       │   └── utils.ts         # Utility functions
│       ├── data/
│       │   └── apis.json        # 55+ API entries
│       ├── package.json
│       └── README.md
│
├── 📄 README.md                 # This file
├── 📄 CONTRIBUTING.md           # Contribution guidelines
├── 📄 LICENSE                   # MIT License
├── 📄 package.json              # Root package.json with workspaces
└── 📄 .gitignore               # Git ignore rules
```

---

## 🏁 Quick Start

### Prerequisites

- Node.js 18+ 
- npm 9+ or yarn/pnpm

### Clone & Install

```bash
# Clone the repository
git clone https://github.com/ashish7802/devsuite.git
cd devsuite

# Install all dependencies
npm install
npm install --workspaces
```

---

## 🖥️ Package 1: DevToolkit CLI

A powerful command-line toolkit that simplifies common development tasks.

### Installation

```bash
# Global installation
npm install -g devsuite-cli

# Or use with npx
npx devsuite-cli <command>
```

### Commands Reference

| Command | Description | Example |
|---------|-------------|---------|
| `init <name>` | Scaffold new project | `devsuite init my-app --template react` |
| `git:sync` | Pull, resolve conflicts, push | `devsuite git:sync` |
| `git:undo` | Undo last commit safely | `devsuite git:undo` |
| `env:check` | Compare .env vs .env.example | `devsuite env:check` |
| `env:gen` | Generate .env.example | `devsuite env:gen` |
| `ports` | Show ports in use | `devsuite ports` |
| `clean` | Clean temp files | `devsuite clean --dry-run` |
| `snippet add <name>` | Save snippet from clipboard | `devsuite snippet add "react-hook"` |
| `snippet list` | List all snippets | `devsuite snippet list` |
| `snippet use <name>` | Copy snippet to clipboard | `devsuite snippet use "react-hook"` |

### Available Templates

- **node** - Node.js project with Jest
- **react** - React + Vite project
- **next** - Next.js 14 project
- **python** - Python project with pytest
- **fastapi** - FastAPI project with Docker

### Demo

```bash
# Create a new React project
devsuite init my-awesome-app --template react

# Output:
# ✅ Created React (Vite) project: my-awesome-app
#
# Next steps:
#   cd my-awesome-app
#   npm install
#   npm run dev
```

---

## 📚 Package 2: Snippet Vault

A beautiful, fast code snippet manager with syntax highlighting.

### Features

- ✨ **Syntax Highlighting** - 50+ languages powered by Shiki
- 🔍 **Instant Search** - Search by title, tags, or description
- 🏷️ **Tagging** - Organize snippets with custom tags
- 📋 **One-click Copy** - Copy code to clipboard instantly
- 🌙 **Dark Mode** - Toggle between light and dark themes
- 📤 **Import/Export** - Backup and restore your snippets
- ⌨️ **Keyboard Shortcuts** - Ctrl+K to focus search
- 💾 **Local Storage** - All data stays in your browser

### Run Locally

```bash
cd packages/web
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

### Screenshots

<div align="center">
  <p><em>Screenshot placeholder - Main interface with snippet grid</em></p>
  <p><em>Screenshot placeholder - Add snippet modal</em></p>
  <p><em>Screenshot placeholder - Syntax highlighted code view</em></p>
</div>

---

## 🌍 Package 3: API Graveyard

A curated directory of 55+ free public APIs with live status checking.

### Features

- 📚 **55+ APIs** - Carefully curated free public APIs
- 🔍 **Search & Filter** - Find APIs by name, category, or tags
- 🟢 **Live Status** - Real-time availability checking
- 📋 **Code Examples** - cURL and JavaScript fetch snippets
- 🔐 **Auth Info** - Clear indication of authentication requirements
- 🏷️ **Categories** - Weather, Finance, AI, Maps, Entertainment, and more
- 🌙 **Dark Mode** - Easy on the eyes

### Included APIs (55 Total)

<details>
<summary>Click to expand full API list</summary>

| Name | Category | Auth | Description |
|------|----------|------|-------------|
| OpenWeatherMap | Weather | API Key | Comprehensive weather data |
| NewsAPI | News | API Key | News headlines and articles |
| JSONPlaceholder | Developer Tools | None | Fake REST API for testing |
| CoinGecko | Finance | None | Cryptocurrency data |
| PokéAPI | Entertainment | None | Pokémon data |
| Dog CEO | Entertainment | None | Random dog images |
| OpenAI | AI | API Key | GPT models and AI tools |
| GitHub | Developer Tools | OAuth | Repository and user data |
| NASA APOD | Science | API Key | Astronomy Picture of the Day |
| REST Countries | Data | None | Country information |
| Open Brewery DB | Food & Drink | None | Brewery database |
| The Cat API | Entertainment | API Key | Cat images and breeds |
| Random User Generator | Developer Tools | None | Mock user data |
| IPify | Developer Tools | None | IP address lookup |
| HTTPBin | Developer Tools | None | HTTP testing service |
| Chuck Norris Jokes | Entertainment | None | Jokes API |
| Deck of Cards | Entertainment | None | Card game API |
| Open Library | Books | None | Book metadata |
| Unsplash | Images | API Key | Free photos |
| Reqres | Developer Tools | None | Testing API |
| Exchange Rate API | Finance | None | Currency conversion |
| The Cocktail DB | Food & Drink | None | Cocktail recipes |
| Agify.io | Data | None | Age prediction |
| Genderize.io | Data | None | Gender prediction |
| Nationalize.io | Data | None | Nationality prediction |
| Bored API | Entertainment | None | Activity suggestions |
| Quote Garden | Entertainment | None | Quotes API |
| Kanye.rest | Entertainment | None | Kanye West quotes |
| Rick and Morty | Entertainment | None | TV show data |
| SpaceX API | Science | None | SpaceX rocket data |
| JSONBin | Developer Tools | API Key | JSON storage |
| QRCode Monkey | Developer Tools | None | QR code generator |
| URLhaus | Security | None | Malicious URL database |
| Have I Been Pwned | Security | API Key | Breach checking |
| OpenStreetMap Nominatim | Maps | None | Geocoding service |
| Zippopotam.us | Data | None | Postal code data |
| Dad Jokes | Entertainment | None | Jokes API |
| JokeAPI | Entertainment | None | Programming jokes |
| Giphy | Entertainment | API Key | GIFs and stickers |
| Pixabay | Images | API Key | Free images |
| Numbers API | Entertainment | None | Number facts |
| UUID Generator | Developer Tools | None | UUID generation |
| ZipCodeBase | Data | API Key | Postal code data |
| World Bank | Finance | None | Economic data |
| Open Trivia Database | Entertainment | None | Trivia questions |
| Shibe.online | Entertainment | None | Shiba Inu pictures |
| PlaceKitten | Images | None | Placeholder images |
| PlaceBear | Images | None | Bear placeholder images |
| Lorem Picsum | Images | None | Random placeholder images |
| Meta Weather | Weather | None | Weather data |
| CoinDesk | Finance | None | Bitcoin price index |
| Breaking Bad Quotes | Entertainment | None | TV show quotes |
| Studio Ghibli | Entertainment | None | Anime film data |
| Open Food Facts | Food & Drink | None | Food product data |
| FreeToGame | Games | None | Free games database |

</details>

### Run Locally

```bash
cd packages/api-directory
npm install
npm run dev
```

Open [http://localhost:3001](http://localhost:3001)

### How to Add an API

1. Edit `packages/api-directory/data/apis.json`
2. Add a new entry following this schema:

```json
{
  "id": "unique-id",
  "name": "API Name",
  "category": "Category",
  "description": "Brief description",
  "base_url": "https://api.example.com",
  "auth_type": "none",
  "docs_url": "https://docs.example.com",
  "example_endpoint": "/endpoint",
  "tags": ["tag1", "tag2"]
}
```

3. Submit a PR!

---

## 🤝 Contributing

We welcome contributions from the community! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Start for Contributors

```bash
# Fork and clone
git clone https://github.com/ashish7802/devsuite.git
cd devsuite

# Create a branch
git checkout -b feature/amazing-feature

# Make changes and commit
git commit -m 'Add amazing feature'

# Push and create PR
git push origin feature/amazing-feature
```

---

## 🗺️ Roadmap

- [ ] **VS Code Extension** - Access snippets directly in VS Code
- [ ] **Browser Extension** - Save snippets from any webpage
- [ ] **AI-Powered Search** - Smart snippet recommendations
- [ ] **Cloud Sync** - Sync snippets across devices
- [ ] **Team Sharing** - Share snippets with your team
- [ ] **More Templates** - Additional project scaffolding templates
- [ ] **Plugin System** - Extend CLI with custom plugins

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Commander.js](https://github.com/tj/commander.js/) - CLI framework
- [Next.js](https://nextjs.org/) - React framework
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS
- [Shiki](https://shiki.matsu.io/) - Syntax highlighter
- [Lucide](https://lucide.dev/) - Beautiful icons

---

<div align="center">

**Made with ❤️ by the Ashish Yadav**

[⭐ Star us on GitHub](https://github.com/ashish7802/devsuite) • [🐛 Report Bug](https://github.com/ashish7802/devsuite/issues) • [💡 Request Feature](https://github.com/ashish7802/devsuite/issues)

</div>
'''

with open(f"{base_path}/README.md", "w") as f:
    f.write(readme_content)

print("✅ Massive README.md created")
