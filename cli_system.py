# CLI system commands (ports, clean)
system_commands = '''import { execa } from 'execa';
import fs from 'fs-extra';
import path from 'path';
import chalk from 'chalk';
import ora from 'ora';
import { glob } from 'glob';
import os from 'os';

/**
 * Check which ports are in use
 */
export async function portsCommand() {
  const spinner = ora('Scanning ports...').start();
  
  try {
    let command, args;
    
    if (process.platform === 'darwin' || process.platform === 'linux') {
      command = 'lsof';
      args = ['-i', '-P', '-n'];
    } else {
      command = 'netstat';
      args = ['-ano'];
    }
    
    const result = await execa(command, args);
    spinner.stop();
    
    console.log(chalk.bold('\\n🔌 Active Network Connections\\n'));
    
    const lines = result.stdout.split('\\n');
    const portData = [];
    
    if (process.platform === 'darwin' || process.platform === 'linux') {
      // Parse lsof output
      for (const line of lines) {
        if (line.includes('LISTEN') || line.includes('ESTABLISHED')) {
          const parts = line.trim().split(/\\s+/);
          if (parts.length >= 9) {
            const process = parts[0];
            const pid = parts[1];
            const protocol = parts[7];
            const address = parts[8];
            
            if (address.includes(':')) {
              const port = address.split(':').pop();
              portData.push({ process, pid, port, protocol });
            }
          }
        }
      }
    }
    
    // Group by port
    const portMap = {};
    portData.forEach(item => {
      if (!portMap[item.port]) {
        portMap[item.port] = [];
      }
      portMap[item.port].push(item);
    });
    
    // Display results
    const sortedPorts = Object.keys(portMap).sort((a, b) => parseInt(a) - parseInt(b));
    
    if (sortedPorts.length === 0) {
      console.log(chalk.yellow('No listening ports found.'));
      return;
    }
    
    console.log(chalk.cyan('PORT      PROCESS       PID'));
    console.log(chalk.gray('─'.repeat(40)));
    
    sortedPorts.forEach(port => {
      const items = portMap[port];
      items.forEach((item, idx) => {
        const portStr = idx === 0 ? port.padEnd(9) : ' '.repeat(9);
        const procStr = item.process.padEnd(13);
        console.log(`${portStr}${procStr}${item.pid}`);
      });
    });
    
    console.log(chalk.dim(`\\nTotal: ${sortedPorts.length} ports in use`));
    
  } catch (error) {
    spinner.fail(chalk.red(`Error: ${error.message}`));
    console.log(chalk.yellow('\\nTip: Try running with sudo if no results appear'));
  }
}

/**
 * Clean up temporary and generated files
 * @param {Object} options - Command options
 */
export async function cleanCommand(options) {
  const spinner = ora('Scanning for files to clean...').start();
  
  try {
    const patterns = [
      '**/node_modules',
      '**/__pycache__',
      '**/*.pyc',
      '**/.pytest_cache',
      '**/.mypy_cache',
      '**/.DS_Store',
      '**/Thumbs.db',
      '**/.next',
      '**/dist',
      '**/build',
      '**/.turbo',
      '**/*.log',
      '**/.coverage',
      '**/coverage',
      '**/.nyc_output'
    ];
    
    const filesToDelete = [];
    
    for (const pattern of patterns) {
      const matches = await glob(pattern, { 
        cwd: process.cwd(),
        absolute: true,
        onlyDirectories: pattern.includes('node_modules') || pattern.includes('__pycache__'),
        dot: true
      });
      filesToDelete.push(...matches);
    }
    
    // Remove duplicates
    const uniqueFiles = [...new Set(filesToDelete)];
    
    spinner.stop();
    
    if (uniqueFiles.length === 0) {
      console.log(chalk.green('✨ Nothing to clean!'));
      return;
    }
    
    console.log(chalk.bold(`\\n🧹 Found ${uniqueFiles.length} items to clean\\n`));
    
    // Group by type
    const groups = {};
    uniqueFiles.forEach(file => {
      const basename = path.basename(file);
      if (!groups[basename]) groups[basename] = [];
      groups[basename].push(file);
    });
    
    Object.entries(groups).forEach(([type, files]) => {
      console.log(chalk.cyan(`${type}:`));
      files.slice(0, 3).forEach(f => {
        console.log(chalk.dim(`  ${path.relative(process.cwd(), f)}`));
      });
      if (files.length > 3) {
        console.log(chalk.dim(`  ... and ${files.length - 3} more`));
      }
    });
    
    if (options.dryRun) {
      console.log(chalk.yellow('\\n⚠️  Dry run - no files were deleted'));
      return;
    }
    
    console.log();
    
    // Delete files
    let deletedCount = 0;
    let errorCount = 0;
    
    for (const file of uniqueFiles) {
      try {
        const stat = await fs.stat(file);
        if (stat.isDirectory()) {
          await fs.remove(file);
        } else {
          await fs.unlink(file);
        }
        deletedCount++;
      } catch (err) {
        errorCount++;
      }
    }
    
    if (errorCount === 0) {
      console.log(chalk.green(`✅ Successfully cleaned ${deletedCount} items`));
    } else {
      console.log(chalk.yellow(`⚠️  Cleaned ${deletedCount} items, ${errorCount} errors`));
    }
    
    // Show potential space saved (rough estimate)
    console.log(chalk.dim('\\n💡 Tip: Run with --dry-run to preview without deleting'));
    
  } catch (error) {
    spinner.fail(chalk.red(`Error: ${error.message}`));
  }
}
'''

with open(f"{base_path}/packages/cli/src/commands/system.js", "w") as f:
    f.write(system_commands)

print("✅ CLI system commands created")
