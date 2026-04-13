# CLI git commands
git_commands = '''import { execa } from 'execa';
import ora from 'ora';
import chalk from 'chalk';
import inquirer from 'inquirer';

/**
 * Execute git commands with error handling
 * @param {string[]} args - Git command arguments
 * @param {Object} options - Execution options
 * @returns {Promise<Object>} - Execution result
 */
async function execGit(args, options = {}) {
  try {
    const result = await execa('git', args, { 
      cwd: process.cwd(),
      ...options 
    });
    return { success: true, stdout: result.stdout, stderr: result.stderr };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

/**
 * Check if we're in a git repository
 * @returns {Promise<boolean>}
 */
async function isGitRepo() {
  const result = await execGit(['rev-parse', '--git-dir']);
  return result.success;
}

/**
 * Get current branch name
 * @returns {Promise<string|null>}
 */
async function getCurrentBranch() {
  const result = await execGit(['branch', '--show-current']);
  return result.success ? result.stdout.trim() : null;
}

/**
 * Check if there are uncommitted changes
 * @returns {Promise<boolean>}
 */
async function hasUncommittedChanges() {
  const result = await execGit(['status', '--porcelain']);
  return result.success && result.stdout.trim().length > 0;
}

/**
 * Sync git repository: pull, resolve conflicts, push
 */
export async function gitSyncCommand() {
  const spinner = ora('Checking git status...').start();
  
  try {
    // Check if we're in a git repo
    if (!await isGitRepo()) {
      spinner.fail(chalk.red('Not a git repository!'));
      return;
    }
    
    // Check for uncommitted changes
    if (await hasUncommittedChanges()) {
      spinner.stop();
      console.log(chalk.yellow('⚠️  You have uncommitted changes:'));
      const status = await execGit(['status', '--short']);
      console.log(status.stdout);
      
      const { action } = await inquirer.prompt([{
        type: 'list',
        name: 'action',
        message: 'What would you like to do?',
        choices: [
          { name: 'Stash changes and continue', value: 'stash' },
          { name: 'Commit changes first', value: 'commit' },
          { name: 'Cancel', value: 'cancel' }
        ]
      }]);
      
      if (action === 'cancel') {
        console.log(chalk.yellow('Sync cancelled.'));
        return;
      }
      
      spinner.start('Processing...');
      
      if (action === 'stash') {
        const stashResult = await execGit(['stash']);
        if (!stashResult.success) {
          spinner.fail(chalk.red('Failed to stash changes'));
          return;
        }
      } else if (action === 'commit') {
        spinner.stop();
        const { message } = await inquirer.prompt([{
          type: 'input',
          name: 'message',
          message: 'Commit message:',
          default: 'WIP: sync changes'
        }]);
        spinner.start('Committing...');
        
        await execGit(['add', '.']);
        const commitResult = await execGit(['commit', '-m', message]);
        if (!commitResult.success) {
          spinner.fail(chalk.red('Failed to commit'));
          return;
        }
      }
    }
    
    const branch = await getCurrentBranch();
    spinner.text = `Pulling latest changes on ${branch}...`;
    
    // Fetch first
    const fetchResult = await execGit(['fetch', 'origin']);
    if (!fetchResult.success) {
      spinner.fail(chalk.red('Failed to fetch from origin'));
      return;
    }
    
    // Try to pull
    const pullResult = await execGit(['pull', 'origin', branch]);
    
    if (!pullResult.success) {
      // Check if it's a merge conflict
      if (pullResult.error.includes('conflict') || pullResult.error.includes('CONFLICT')) {
        spinner.warn(chalk.yellow('Merge conflicts detected!'));
        
        const conflicts = await execGit(['diff', '--name-only', '--diff-filter=U']);
        console.log(chalk.red('\\nConflicting files:'));
        console.log(conflicts.stdout);
        
        console.log(chalk.cyan('\\nPlease resolve conflicts manually and run:'));
        console.log(chalk.white('  git add .'));
        console.log(chalk.white('  git commit -m "Merge resolved"'));
        console.log(chalk.white('  git push'));
        return;
      }
      
      spinner.fail(chalk.red(`Pull failed: ${pullResult.error}`));
      return;
    }
    
    // Check if there were merge conflicts in the output
    if (pullResult.stdout.includes('CONFLICT') || pullResult.stderr.includes('CONFLICT')) {
      spinner.warn(chalk.yellow('Merge conflicts detected!'));
      console.log(chalk.cyan('\\nPlease resolve conflicts manually.'));
      return;
    }
    
    spinner.text = 'Pushing changes...';
    const pushResult = await execGit(['push', 'origin', branch]);
    
    if (!pushResult.success) {
      spinner.fail(chalk.red(`Push failed: ${pushResult.error}`));
      return;
    }
    
    spinner.succeed(chalk.green(`✅ Synced ${branch} successfully!`));
    
    // Show summary
    const logResult = await execGit(['log', '--oneline', '-3']);
    console.log(chalk.dim('\\nRecent commits:'));
    console.log(chalk.gray(logResult.stdout));
    
  } catch (error) {
    spinner.fail(chalk.red(`Error: ${error.message}`));
  }
}

/**
 * Undo the last commit safely
 * @param {Object} options - Command options
 */
export async function gitUndoCommand(options) {
  const spinner = ora('Checking repository...').start();
  
  try {
    if (!await isGitRepo()) {
      spinner.fail(chalk.red('Not a git repository!'));
      return;
    }
    
    // Get the last commit info
    const logResult = await execGit(['log', '-1', '--format=%h %s']);
    if (!logResult.success) {
      spinner.fail(chalk.red('Failed to get commit history'));
      return;
    }
    
    const lastCommit = logResult.stdout.trim();
    spinner.stop();
    
    console.log(chalk.yellow('⚠️  You are about to undo the last commit:'));
    console.log(chalk.cyan(`   ${lastCommit}`));
    
    const { confirm } = await inquirer.prompt([{
      type: 'confirm',
      name: 'confirm',
      message: options.hard 
        ? 'This will permanently DELETE the commit and changes. Continue?' 
        : 'This will keep changes in your working directory. Continue?',
      default: false
    }]);
    
    if (!confirm) {
      console.log(chalk.yellow('Undo cancelled.'));
      return;
    }
    
    spinner.start('Undoing commit...');
    
    const resetMode = options.hard ? '--hard' : '--soft';
    const resetResult = await execGit(['reset', resetMode, 'HEAD~1']);
    
    if (!resetResult.success) {
      spinner.fail(chalk.red(`Undo failed: ${resetResult.error}`));
      return;
    }
    
    spinner.succeed(chalk.green('✅ Last commit undone successfully!'));
    
    if (!options.hard) {
      const status = await execGit(['status', '--short']);
      if (status.stdout.trim()) {
        console.log(chalk.cyan('\\nYour changes are preserved:'));
        console.log(chalk.gray(status.stdout));
        console.log(chalk.dim('\\nYou can now:'));
        console.log(chalk.white('  - Re-commit with: git commit -m "new message"'));
        console.log(chalk.white('  - Stage different files: git add <files>'));
        console.log(chalk.white('  - Discard changes: git checkout -- <files>'));
      }
    } else {
      console.log(chalk.yellow('\\n⚠️  Changes have been permanently deleted.'));
    }
    
  } catch (error) {
    spinner.fail(chalk.red(`Error: ${error.message}`));
  }
}
'''

with open(f"{base_path}/packages/cli/src/commands/git.js", "w") as f:
    f.write(git_commands)

print("✅ CLI git commands created")
