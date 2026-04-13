
# CLI main entry point (index.js)
cli_index = '''#!/usr/bin/env node

import { program } from 'commander';
import chalk from 'chalk';
import { initCommand } from './commands/init.js';
import { gitSyncCommand, gitUndoCommand } from './commands/git.js';
import { envCheckCommand, envGenCommand } from './commands/env.js';
import { portsCommand, cleanCommand } from './commands/system.js';
import { snippetAddCommand, snippetListCommand, snippetUseCommand } from './commands/snippet.js';

const logo = `
${chalk.cyan('╔════════════════════════════════════╗')}
${chalk.cyan('║')}     ${chalk.bold('⚡ DevSuite CLI')} v1.0.0        ${chalk.cyan('║')}
${chalk.cyan('║')}     ${chalk.dim("The Developer's Swiss Army Knife")}  ${chalk.cyan('║')}
${chalk.cyan('╚════════════════════════════════════╝')}
`;

console.log(logo);

program
  .name('devsuite')
  .description('A powerful CLI toolkit for developers')
  .version('1.0.0');

// Init command
program
  .command('init <project-name>')
  .description('Scaffold a new project with templates')
  .option('-t, --template <type>', 'Project template (node, react, next, python, fastapi)', 'node')
  .action(initCommand);

// Git commands
program
  .command('git:sync')
  .description('Pull, auto-resolve simple conflicts, and push')
  .action(gitSyncCommand);

program
  .command('git:undo')
  .description('Safely undo the last commit (preserves changes)')
  .option('--hard', 'Hard reset (discard changes)', false)
  .action(gitUndoCommand);

// Environment commands
program
  .command('env:check')
  .description('Compare .env vs .env.example and show missing variables')
  .action(envCheckCommand);

program
  .command('env:gen')
  .description('Auto-generate .env.example from .env (masks values)')
  .action(envGenCommand);

// System commands
program
  .command('ports')
  .description('Show all ports in use with process names')
  .action(portsCommand);

program
  .command('clean')
  .description('Remove node_modules, __pycache__, .DS_Store recursively')
  .option('-d, --dry-run', 'Show what would be deleted without deleting', false)
  .action(cleanCommand);

// Snippet commands
program
  .command('snippet add <name>')
  .description('Save a code snippet from clipboard')
  .option('-l, --language <lang>', 'Programming language', 'text')
  .action(snippetAddCommand);

program
  .command('snippet list')
  .description('List all saved snippets')
  .option('-l, --language <lang>', 'Filter by language')
  .action(snippetListCommand);

program
  .command('snippet use <name>')
  .description('Copy a saved snippet to clipboard')
  .action(snippetUseCommand);

program.parse();
'''

with open(f"{base_path}/packages/cli/src/index.js", "w") as f:
    f.write(cli_index)

print("✅ CLI index.js created")
