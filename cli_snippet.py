# CLI snippet commands
snippet_commands = '''import fs from 'fs-extra';
import path from 'path';
import os from 'os';
import chalk from 'chalk';
import ora from 'ora';
import clipboardy from 'clipboardy';
import inquirer from 'inquirer';

/**
 * Get snippets storage path
 * @returns {string}
 */
function getSnippetsPath() {
  return path.join(os.homedir(), '.devsuite', 'snippets.json');
}

/**
 * Load snippets from storage
 * @returns {Promise<Object>}
 */
async function loadSnippets() {
  const snippetsPath = getSnippetsPath();
  if (!await fs.pathExists(snippetsPath)) {
    return {};
  }
  return await fs.readJson(snippetsPath);
}

/**
 * Save snippets to storage
 * @param {Object} snippets
 */
async function saveSnippets(snippets) {
  const snippetsPath = getSnippetsPath();
  await fs.ensureDir(path.dirname(snippetsPath));
  await fs.writeJson(snippetsPath, snippets, { spaces: 2 });
}

/**
 * Add a new snippet from clipboard
 * @param {string} name - Snippet name
 * @param {Object} options - Command options
 */
export async function snippetAddCommand(name, options) {
  const spinner = ora('Reading clipboard...').start();
  
  try {
    const content = await clipboardy.read();
    
    if (!content || content.trim().length === 0) {
      spinner.fail(chalk.red('Clipboard is empty!'));
      return;
    }
    
    spinner.text = 'Saving snippet...';
    
    const snippets = await loadSnippets();
    
    snippets[name] = {
      content,
      language: options.language || 'text',
      createdAt: new Date().toISOString(),
      size: content.length
    };
    
    await saveSnippets(snippets);
    
    spinner.succeed(chalk.green(`✅ Snippet "${name}" saved!`));
    
    // Show preview
    const preview = content.slice(0, 100).replace(/\\n/g, ' ');
    console.log(chalk.dim(`\\nPreview: ${preview}${content.length > 100 ? '...' : ''}`));
    console.log(chalk.gray(`Size: ${content.length} characters`));
    
  } catch (error) {
    spinner.fail(chalk.red(`Error: ${error.message}`));
    console.log(chalk.yellow('\\nTip: Make sure you have copied content to clipboard'));
  }
}

/**
 * List all saved snippets
 * @param {Object} options - Command options
 */
export async function snippetListCommand(options) {
  const spinner = ora('Loading snippets...').start();
  
  try {
    const snippets = await loadSnippets();
    const names = Object.keys(snippets);
    
    spinner.stop();
    
    if (names.length === 0) {
      console.log(chalk.yellow('📭 No snippets saved yet.'));
      console.log(chalk.dim('\\nTo add a snippet:'));
      console.log(chalk.white('  devsuite snippet add <name>'));
      return;
    }
    
    // Filter by language if specified
    let filteredSnippets = names;
    if (options.language) {
      filteredSnippets = names.filter(name => 
        snippets[name].language === options.language
      );
    }
    
    console.log(chalk.bold(`\\n📚 Saved Snippets (${filteredSnippets.length})\\n`));
    
    // Group by language
    const byLanguage = {};
    filteredSnippets.forEach(name => {
      const lang = snippets[name].language || 'text';
      if (!byLanguage[lang]) byLanguage[lang] = [];
      byLanguage[lang].push(name);
    });
    
    Object.entries(byLanguage).forEach(([lang, items]) => {
      console.log(chalk.cyan(`${lang.toUpperCase()}:`));
      items.forEach(name => {
        const snippet = snippets[name];
        const date = new Date(snippet.createdAt).toLocaleDateString();
        const size = snippet.size || snippet.content.length;
        console.log(chalk.white(`  • ${name}`));
        console.log(chalk.gray(`    ${size} chars • ${date}`));
      });
      console.log();
    });
    
    console.log(chalk.dim('💡 Use: devsuite snippet use <name> to copy to clipboard'));
    
  } catch (error) {
    spinner.fail(chalk.red(`Error: ${error.message}`));
  }
}

/**
 * Copy a snippet to clipboard
 * @param {string} name - Snippet name
 */
export async function snippetUseCommand(name) {
  const spinner = ora('Loading snippet...').start();
  
  try {
    const snippets = await loadSnippets();
    
    if (!snippets[name]) {
      spinner.fail(chalk.red(`Snippet "${name}" not found!`));
      
      // Suggest similar names
      const names = Object.keys(snippets);
      const similar = names.filter(n => 
        n.toLowerCase().includes(name.toLowerCase()) ||
        name.toLowerCase().includes(n.toLowerCase())
      );
      
      if (similar.length > 0) {
        console.log(chalk.yellow('\\nDid you mean:'));
        similar.forEach(n => console.log(chalk.cyan(`  • ${n}`)));
      }
      
      return;
    }
    
    const snippet = snippets[name];
    await clipboardy.write(snippet.content);
    
    spinner.succeed(chalk.green(`✅ Copied "${name}" to clipboard!`));
    
    // Show preview
    const preview = snippet.content.slice(0, 150).replace(/\\n/g, ' ');
    console.log(chalk.dim(`\\n${preview}${snippet.content.length > 150 ? '...' : ''}`));
    
  } catch (error) {
    spinner.fail(chalk.red(`Error: ${error.message}`));
  }
}
'''

with open(f"{base_path}/packages/cli/src/commands/snippet.js", "w") as f:
    f.write(snippet_commands)

print("✅ CLI snippet commands created")
