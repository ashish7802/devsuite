# CLI env commands
env_commands = '''import fs from 'fs-extra';
import path from 'path';
import chalk from 'chalk';
import ora from 'ora';

/**
 * Read and parse .env file
 * @param {string} filePath - Path to .env file
 * @returns {Object} - Parsed key-value pairs
 */
async function parseEnvFile(filePath) {
  if (!await fs.pathExists(filePath)) {
    return null;
  }
  
  const content = await fs.readFile(filePath, 'utf-8');
  const env = {};
  
  content.split('\\n').forEach(line => {
    // Skip comments and empty lines
    if (!line || line.startsWith('#')) return;
    
    const match = line.match(/^([^=]+)=(.*)$/);
    if (match) {
      const key = match[1].trim();
      const value = match[2].trim();
      if (key) {
        env[key] = value;
      }
    }
  });
  
  return env;
}

/**
 * Compare .env and .env.example files
 */
export async function envCheckCommand() {
  const spinner = ora('Checking environment files...').start();
  
  try {
    const envPath = path.join(process.cwd(), '.env');
    const examplePath = path.join(process.cwd(), '.env.example');
    
    const env = await parseEnvFile(envPath);
    const example = await parseEnvFile(examplePath);
    
    spinner.stop();
    
    if (!env && !example) {
      console.log(chalk.red('❌ Neither .env nor .env.example found!'));
      return;
    }
    
    if (!env) {
      console.log(chalk.red('❌ .env file not found!'));
      console.log(chalk.dim('Create one based on .env.example'));
      return;
    }
    
    if (!example) {
      console.log(chalk.yellow('⚠️  .env.example not found!'));
      console.log(chalk.dim('Run: devsuite env:gen to create one'));
      return;
    }
    
    const envKeys = Object.keys(env);
    const exampleKeys = Object.keys(example);
    
    const missingInEnv = exampleKeys.filter(key => !envKeys.includes(key));
    const missingInExample = envKeys.filter(key => !exampleKeys.includes(key));
    const presentInBoth = envKeys.filter(key => exampleKeys.includes(key));
    
    console.log(chalk.bold('\\n📋 Environment Variables Check\\n'));
    
    // Show present variables
    if (presentInBoth.length > 0) {
      console.log(chalk.green(`✅ ${presentInBoth.length} variables present in both files:`));
      presentInBoth.forEach(key => {
        const masked = env[key] ? '*****' : chalk.red('(empty)');
        console.log(chalk.dim(`   ${key}=${masked}`));
      });
      console.log();
    }
    
    // Show missing in .env
    if (missingInEnv.length > 0) {
      console.log(chalk.red(`❌ ${missingInEnv.length} variables missing from .env:`));
      missingInEnv.forEach(key => {
        console.log(chalk.red(`   ${key}`));
      });
      console.log();
    }
    
    // Show extra in .env
    if (missingInExample.length > 0) {
      console.log(chalk.yellow(`⚠️  ${missingInExample.length} variables in .env but not in .env.example:`));
      missingInExample.forEach(key => {
        console.log(chalk.yellow(`   ${key}`));
      });
      console.log();
    }
    
    // Summary
    if (missingInEnv.length === 0 && missingInExample.length === 0) {
      console.log(chalk.green('✨ All environment variables are in sync!'));
    } else {
      console.log(chalk.cyan('💡 To fix:'));
      if (missingInEnv.length > 0) {
        console.log(chalk.white(`   - Add missing variables to .env`));
      }
      if (missingInExample.length > 0) {
        console.log(chalk.white(`   - Run: devsuite env:gen to update .env.example`));
      }
    }
    
  } catch (error) {
    spinner.fail(chalk.red(`Error: ${error.message}`));
  }
}

/**
 * Generate .env.example from .env
 */
export async function envGenCommand() {
  const spinner = ora('Generating .env.example...').start();
  
  try {
    const envPath = path.join(process.cwd(), '.env');
    const examplePath = path.join(process.cwd(), '.env.example');
    
    if (!await fs.pathExists(envPath)) {
      spinner.fail(chalk.red('.env file not found!'));
      return;
    }
    
    const content = await fs.readFile(envPath, 'utf-8');
    
    // Mask values while preserving comments and structure
    const lines = content.split('\\n');
    const exampleLines = lines.map(line => {
      // Preserve comments and empty lines
      if (!line || line.startsWith('#')) return line;
      
      const match = line.match(/^([^=]+)=(.*)$/);
      if (match) {
        const key = match[1].trim();
        const value = match[2].trim();
        
        // Don't mask empty values
        if (!value) return `${key}=`;
        
        // Mask the value
        return `${key}=YOUR_${key.toUpperCase().replace(/[^A-Z0-9]/g, '_')}_HERE`;
      }
      
      return line;
    });
    
    await fs.writeFile(examplePath, exampleLines.join('\\n'));
    
    spinner.succeed(chalk.green('✅ Generated .env.example'));
    console.log(chalk.dim(`\\nLocation: ${examplePath}`));
    
    // Show preview
    const preview = exampleLines.slice(0, 10).join('\\n');
    console.log(chalk.cyan('\\nPreview:'));
    console.log(chalk.gray(preview));
    
    if (exampleLines.length > 10) {
      console.log(chalk.dim(`... and ${exampleLines.length - 10} more lines`));
    }
    
  } catch (error) {
    spinner.fail(chalk.red(`Error: ${error.message}`));
  }
}
'''

with open(f"{base_path}/packages/cli/src/commands/env.js", "w") as f:
    f.write(env_commands)

print("✅ CLI env commands created")
