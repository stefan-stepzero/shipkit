'use strict';

const path = require('path');

function parseArgs(argv) {
  const args = {
    command: null,
    flags: {
      profile: null,
      allSkills: false,
      allAgents: false,
      noAgents: false,
      noMcps: false,
      claudeMd: null,
      yes: false,
      target: null,
    }
  };

  let i = 0;
  // First positional = command
  while (i < argv.length) {
    const arg = argv[i];
    if (!arg.startsWith('-') && !args.command) {
      args.command = arg;
      i++;
      continue;
    }
    switch (arg) {
      case '--profile':
        args.flags.profile = argv[++i];
        break;
      case '--all-skills':
        args.flags.allSkills = true;
        break;
      case '--all-agents':
        args.flags.allAgents = true;
        break;
      case '--no-agents':
        args.flags.noAgents = true;
        break;
      case '--no-mcps':
        args.flags.noMcps = true;
        break;
      case '--claude-md':
        args.flags.claudeMd = argv[++i];
        break;
      case '-y':
      case '--yes':
        args.flags.yes = true;
        break;
      case '--target':
        args.flags.target = argv[++i];
        break;
      default:
        // ignore unknown flags
        break;
    }
    i++;
  }
  return args;
}

function getPackageRoot() {
  return path.resolve(__dirname, '..', '..');
}

async function run(argv) {
  const { command, flags } = parseArgs(argv);
  const packageRoot = getPackageRoot();

  switch (command) {
    case 'init': {
      const { init } = require('./init');
      await init(packageRoot, flags);
      break;
    }
    case 'update': {
      const { update } = require('./update');
      await update(packageRoot, flags);
      break;
    }
    case 'sync-docs': {
      const { syncDocs } = require('./sync-docs');
      const { skillCount, agentCount, results } = syncDocs(packageRoot);
      console.log(`Manifest: ${skillCount} skills, ${agentCount} agents`);
      for (const r of results) {
        const label = r.updated ? '\x1b[32m✓\x1b[0m' : '\x1b[90m-\x1b[0m';
        const name = require('path').relative(packageRoot, r.path);
        console.log(`  ${label} ${name}${r.reason ? ` (${r.reason})` : ''}`);
      }
      break;
    }
    case 'version': {
      const fs = require('fs');
      const version = fs.readFileSync(path.join(packageRoot, 'VERSION'), 'utf8').trim();
      console.log('Shipkit v' + version);
      break;
    }
    case 'help':
    case undefined:
      printHelp();
      break;
    default:
      console.error(`Unknown command: ${command}\n`);
      printHelp();
      process.exit(1);
  }
}

function printHelp() {
  console.log(`
Shipkit — Streamlined product development framework for Claude Code

Usage:
  npx shipkit-dev <command> [options]

Commands:
  init       Install Shipkit into the current project
  update     Update an existing Shipkit installation
  sync-docs  Regenerate skill/agent counts in docs from manifest
  version    Print the installed version
  help       Show this help message

Options:
  --profile <name>     Edition: shipkit (default), discovery, minimal
  --all-skills         Install all skills without prompting
  --all-agents         Install all agents without prompting
  --no-agents          Skip agent installation
  --no-mcps            Skip MCP example file creation
  --claude-md <mode>   CLAUDE.md handling: skip, overwrite, merge
  --target <path>      Installation directory (default: current directory)
  -y, --yes            Non-interactive mode (accept all defaults)

Examples:
  npx shipkit-dev init                    Interactive install
  npx shipkit-dev init -y                 Install with defaults (all skills, all agents)
  npx shipkit-dev init --profile minimal  Install minimal profile
  npx shipkit-dev update                  Update to latest version
`);
}

module.exports = { run };
