'use strict';

const fs = require('fs');
const path = require('path');
const ui = require('./ui');
const { createInterface, confirm, promptForProfile, promptForSkills, promptForAgents, promptForClaudeMdAction } = require('./prompt');
const { loadManifest, getAllSkillNames, getAllAgentNames } = require('./manifest');
const { generateSettings } = require('./settings');
const { handleClaudeMd } = require('./claude-md');
const { generateMcpExample } = require('./mcp');
const { ensureDir, copyFile, copyDir, copyFileIfNotExists, makeExecutable } = require('./copy');

// Hook files: source name -> destination name
const HOOK_FILES = {
  'shipkit-session-start.py': 'session-start.py',
  'shipkit-after-skill-router.py': 'after-skill-router.py',
  'shipkit-relentless-stop-hook.py': 'shipkit-relentless-stop-hook.py',
  'shipkit-track-skill-usage.py': 'shipkit-track-skill-usage.py',
  'shipkit-task-completed-hook.py': 'shipkit-task-completed-hook.py',
  'shipkit-teammate-idle-hook.py': 'shipkit-teammate-idle-hook.py',
};

async function init(packageRoot, flags) {
  const version = fs.readFileSync(path.join(packageRoot, 'VERSION'), 'utf8').trim();
  const targetDir = path.resolve(flags.target || process.cwd());
  const nonInteractive = flags.yes;

  ui.logo(version);
  ui.section('Install Shipkit');
  ui.info(`Target: ${targetDir}`);

  // Verify source files exist
  const installDir = path.join(packageRoot, 'install');
  if (!fs.existsSync(installDir)) {
    throw new Error(`Install directory not found: ${installDir}`);
  }

  let rl;
  if (!nonInteractive) {
    rl = createInterface();
  }

  try {
    // 1. Select profile
    let profile;
    if (flags.profile) {
      profile = flags.profile;
    } else if (nonInteractive) {
      profile = 'shipkit';
    } else {
      profile = await promptForProfile(rl);
    }

    const manifest = loadManifest(packageRoot, profile);
    ui.success(`Profile: ${profile} (${manifest.description})`);

    // 2. Select skills
    let selectedSkills;
    if (flags.allSkills || nonInteractive) {
      selectedSkills = getAllSkillNames(manifest);
    } else {
      selectedSkills = await promptForSkills(rl, manifest);
    }
    ui.success(`Skills: ${selectedSkills.length} selected`);

    // 3. Select agents
    let selectedAgents;
    if (flags.noAgents) {
      selectedAgents = [];
    } else if (flags.allAgents || nonInteractive) {
      selectedAgents = getAllAgentNames(manifest);
    } else {
      selectedAgents = await promptForAgents(rl, manifest);
    }
    ui.success(`Agents: ${selectedAgents.length} selected`);

    // 4. CLAUDE.md action
    let claudeMdAction;
    if (flags.claudeMd) {
      claudeMdAction = flags.claudeMd;
    } else if (nonInteractive) {
      claudeMdAction = fs.existsSync(path.join(targetDir, 'CLAUDE.md')) ? 'merge' : 'install';
    } else {
      claudeMdAction = await promptForClaudeMdAction(rl, targetDir);
    }

    // 5. Confirm
    if (!nonInteractive) {
      console.log();
      ui.section('Summary');
      ui.bullet(`Profile: ${profile}`);
      ui.bullet(`Skills: ${selectedSkills.length}`);
      ui.bullet(`Agents: ${selectedAgents.length}`);
      ui.bullet(`CLAUDE.md: ${claudeMdAction}`);
      ui.bullet(`Target: ${targetDir}`);
      console.log();

      const ok = await confirm(rl, 'Install Shipkit with these settings?');
      if (!ok) {
        ui.warning('Installation cancelled.');
        return;
      }
    }

    // Close readline before file operations
    if (rl) rl.close();
    rl = null;

    console.log();
    ui.section('Installing');

    // 6. Create directories
    ensureDir(path.join(targetDir, '.claude', 'hooks'));
    ensureDir(path.join(targetDir, '.claude', 'rules'));
    ensureDir(path.join(targetDir, '.claude', 'skills'));
    ensureDir(path.join(targetDir, '.claude', 'agents'));
    ensureDir(path.join(targetDir, '.shipkit'));
    ensureDir(path.join(targetDir, '.shipkit', 'scripts'));

    // 7. Install hooks
    const hooksDir = path.join(installDir, 'shared', 'hooks');
    for (const [src, dest] of Object.entries(HOOK_FILES)) {
      const srcPath = path.join(hooksDir, src);
      const destPath = path.join(targetDir, '.claude', 'hooks', dest);
      if (fs.existsSync(srcPath)) {
        copyFile(srcPath, destPath);
        makeExecutable(destPath);
      }
    }
    ui.success('Hooks installed (6 files)');

    // 8. Install rules
    const rulesDir = path.join(installDir, 'rules');
    if (fs.existsSync(rulesDir)) {
      copyDir(rulesDir, path.join(targetDir, '.claude', 'rules'));
    }
    ui.success('Rules installed');

    // 9. Install Python scripts
    const pythonScriptsDir = path.join(installDir, 'shared', 'scripts', 'python');
    if (fs.existsSync(pythonScriptsDir)) {
      copyDir(pythonScriptsDir, path.join(targetDir, '.shipkit', 'scripts'));
    }
    ui.success('Scripts installed');

    // 10. Copy VERSION
    copyFile(path.join(packageRoot, 'VERSION'), path.join(targetDir, '.shipkit', 'VERSION'));

    // 11. .gitignore and .gitattributes
    const sharedDir = path.join(installDir, 'shared');
    const gitignoreSrc = path.join(sharedDir, '.gitignore');
    const gitattribsSrc = path.join(sharedDir, '.gitattributes');

    if (fs.existsSync(gitignoreSrc)) {
      if (copyFileIfNotExists(gitignoreSrc, path.join(targetDir, '.gitignore'))) {
        ui.success('.gitignore created');
      } else {
        ui.info('.gitignore already exists (skipped)');
      }
    }
    if (fs.existsSync(gitattribsSrc)) {
      if (copyFileIfNotExists(gitattribsSrc, path.join(targetDir, '.gitattributes'))) {
        ui.success('.gitattributes created');
      } else {
        ui.info('.gitattributes already exists (skipped)');
      }
    }

    // 12. Generate settings.json
    const settingsDest = path.join(targetDir, '.claude', 'settings.json');
    if (fs.existsSync(settingsDest)) {
      ui.warning('settings.json already exists — merging skill permissions and hooks');
      const { mergeSettings } = require('./settings');
      const merged = mergeSettings(settingsDest, selectedSkills);
      fs.writeFileSync(settingsDest, JSON.stringify(merged, null, 2) + '\n', 'utf8');
    } else {
      const settings = generateSettings(manifest, selectedSkills);
      fs.writeFileSync(settingsDest, JSON.stringify(settings, null, 2) + '\n', 'utf8');
    }
    ui.success('settings.json configured');

    // 13. CLAUDE.md
    if (handleClaudeMd(packageRoot, targetDir, version, claudeMdAction)) {
      ui.success(`CLAUDE.md ${claudeMdAction === 'install' ? 'created' : claudeMdAction + 'ed'}`);
    } else {
      ui.info('CLAUDE.md skipped');
    }

    // 14. Install skills
    const skillsDir = path.join(installDir, 'skills');
    let skillCount = 0;
    for (const skillName of selectedSkills) {
      const src = path.join(skillsDir, skillName);
      if (fs.existsSync(src)) {
        copyDir(src, path.join(targetDir, '.claude', 'skills', skillName));
        skillCount++;
      }
    }
    ui.success(`${skillCount} skills installed`);

    // 15. Install agents
    const agentsDir = path.join(installDir, 'agents');
    let agentCount = 0;
    for (const agentName of selectedAgents) {
      const src = path.join(agentsDir, `${agentName}.md`);
      if (fs.existsSync(src)) {
        copyFile(src, path.join(targetDir, '.claude', 'agents', `${agentName}.md`));
        agentCount++;
      }
    }
    ui.success(`${agentCount} agents installed`);

    // 16. MCP example
    if (!flags.noMcps) {
      if (generateMcpExample(manifest, targetDir)) {
        ui.success('.mcp.json.example created');
      }
    }

    // 17. HTML overview
    const overviewSrc = path.join(packageRoot, 'docs', 'generated', 'shipkit-overview.html');
    if (fs.existsSync(overviewSrc)) {
      let html = fs.readFileSync(overviewSrc, 'utf8');
      html = html.replace(/\{\{SHIPKIT_VERSION\}\}/g, `v${version}`);
      fs.writeFileSync(path.join(targetDir, '.shipkit', 'shipkit-overview.html'), html, 'utf8');
      ui.success('Overview page installed');
    }

    // Done!
    console.log();
    ui.section('Installation Complete');
    ui.success(`Shipkit v${version} installed to ${targetDir}`);
    console.log();
    ui.bullet('Open Claude Code in this directory to start using Shipkit');
    ui.bullet('Run /shipkit-master to see available skills');
    ui.bullet('Run /shipkit-why-project to define your project vision');
    console.log();
    ui.info(`To enable MCPs: ${ui.colors.dim}cp .mcp.json.example .mcp.json${ui.colors.reset}`);
    ui.info(`To update later: ${ui.colors.dim}npx shipkit update${ui.colors.reset}`);
    console.log();

  } finally {
    if (rl) rl.close();
  }
}

module.exports = { init };
