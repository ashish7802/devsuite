# Create CONTRIBUTING.md
contributing = '''# Contributing to DevSuite

Thank you for your interest in contributing to DevSuite! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs

- Check if the bug has already been reported in the Issues section
- If not, create a new issue with a clear title and description
- Include steps to reproduce, expected behavior, and actual behavior
- Add screenshots if applicable

### Suggesting Features

- Open an issue with the label `enhancement`
- Describe the feature and its use case
- Explain why this feature would be useful

### Pull Requests

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Run tests: `npm test`
5. Commit your changes: `git commit -m 'Add some feature'`
6. Push to the branch: `git push origin feature/your-feature-name`
7. Open a Pull Request

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/devsuite.git
cd devsuite

# Install dependencies
npm install
npm install --workspaces

# Run CLI in development
npm run dev:cli

# Run Web app
npm run dev:web

# Run API Directory
npm run dev:api
```

### Code Style

- Use TypeScript for type safety
- Follow existing code patterns
- Add JSDoc comments for functions
- Use meaningful variable names
- Keep functions small and focused

### Commit Message Guidelines

- Use present tense: "Add feature" not "Added feature"
- Use imperative mood: "Move cursor to..." not "Moves cursor to..."
- Limit first line to 72 characters
- Reference issues and PRs where appropriate

### Testing

- Add tests for new features
- Ensure all tests pass before submitting PR
- Maintain or improve code coverage

## Project Structure

```
devsuite/
├── packages/
│   ├── cli/           # DevToolkit CLI
│   ├── web/           # Snippet Vault
│   └── api-directory/ # API Graveyard
```

## Questions?

Feel free to open an issue for any questions or join our discussions.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
'''

with open(f"{base_path}/CONTRIBUTING.md", "w") as f:
    f.write(contributing)

print("✅ CONTRIBUTING.md created")
