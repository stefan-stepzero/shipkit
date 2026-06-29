'use strict';

const fs = require('fs');
const os = require('os');
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
  'shipkit-track-skill-usage.py': 'shipkit-track-skill-usage.py',
  'shipkit-task-completed-hook.py': 'shipkit-task-completed-hook.py',
  'shipkit-teammate-idle-hook.py': 'shipkit-teammate-idle-hook.py',
  'shipkit-post-compact.py': 'shipkit-post-compact.py',
  'shipkit-session-end.py': 'shipkit-session-end.py',
  'shipkit-subagent-context.py': 'shipkit-subagent-context.py',
  'shipkit-diagnostics.py': 'shipkit-diagnostics.py',
  'shipkit-prereq-check.py': 'shipkit-prereq-check.py',
  'shipkit-pre-compact.py': 'shipkit-pre-compact.py',
  'shipkit-task-created-hook.py': 'shipkit-task-created-hook.py',
  'shipkit-permission-denied-hook.py': 'shipkit-permission-denied-hook.py',
  'shipkit-codebase-index-refresh.py': 'shipkit-codebase-index-refresh.py',
};

async function init(packageRoot, flags) {
  const version = fs.readFileSync(path.join(packageRoot, 'VERSION'), 'utf8').trim();
  const targetDir = path.resolve(flags.target || process.cwd());
  const nonInteractive = flags.yes;

  // Scope split: `.claude/` code can install per-project or at user level
  // (~/.claude, shared across all projects). `.shipkit/` data is ALWAYS
  // per-project — at user scope it is created at runtime by the skills, not here.
  const userScope = !!flags.user;
  const claudeDir = userScope ? path.join(os.homedir(), '.claude') : path.join(targetDir, '.claude');
  const dataDir = userScope ? null : path.join(targetDir, '.shipkit');

  ui.logo(version);
  ui.section(userScope ? 'Install Shipkit (user level)' : 'Install Shipkit');
  ui.info(`Target: ${userScope ? claudeDir + '  (shared across all projects)' : targetDir}`);

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
    ensureDir(path.join(claudeDir, 'hooks'));
    ensureDir(path.join(claudeDir, 'rules'));
    ensureDir(path.join(claudeDir, 'skills'));
    ensureDir(path.join(claudeDir, 'agents'));
    if (dataDir) {
      ensureDir(dataDir);
      ensureDir(path.join(dataDir, 'scripts'));
    }

    // 7. Install hooks
    const hooksDir = path.join(installDir, 'shared', 'hooks');
    for (const [src, dest] of Object.entries(HOOK_FILES)) {
      const srcPath = path.join(hooksDir, src);
      const destPath = path.join(claudeDir, 'hooks', dest);
      if (fs.existsSync(srcPath)) {
        copyFile(srcPath, destPath);
        makeExecutable(destPath);
      }
    }
    ui.success(`Hooks installed (${Object.keys(HOOK_FILES).length} files)`);

    // 8. Install rules
    const rulesDir = path.join(installDir, 'rules');
    if (fs.existsSync(rulesDir)) {
      const rulesDestDir = path.join(claudeDir, 'rules');
      copyDir(rulesDir, rulesDestDir);
      if (userScope) {
        // User-level rules load in EVERY project. Gate Shipkit's rules to actual
        // Shipkit projects via path-scoped frontmatter so they only enter context
        // once Claude touches a .shipkit/ file (not in unrelated projects).
        const shipkitRule = path.join(rulesDestDir, 'shipkit.md');
        if (fs.existsSync(shipkitRule)) {
          const body = fs.readFileSync(shipkitRule, 'utf8');
          if (!body.startsWith('---')) {
            const gated = '---\npaths:\n  - "**/.shipkit/**"\n---\n\n' + body;
            fs.writeFileSync(shipkitRule, gated, 'utf8');
          }
        }
      }
    }
    ui.success(userScope ? 'Rules installed (scoped to Shipkit projects)' : 'Rules installed');

    // 9 / 9b / 10. Install Python + observability scripts and the VERSION marker
    // into the per-project .shipkit/. Skipped at user scope — these are
    // project-level data; .shipkit/ is created per-project at runtime.
    if (dataDir) {
      const pythonScriptsDir = path.join(installDir, 'shared', 'scripts', 'python');
      if (fs.existsSync(pythonScriptsDir)) {
        copyDir(pythonScriptsDir, path.join(dataDir, 'scripts'));
      }
      const obsScriptsDir = path.join(installDir, 'shared', 'scripts', 'observability');
      if (fs.existsSync(obsScriptsDir)) {
        const obsDestDir = path.join(dataDir, 'observability');
        ensureDir(obsDestDir);
        copyDir(obsScriptsDir, obsDestDir);
      }
      ui.success('Scripts installed');
      copyFile(path.join(packageRoot, 'VERSION'), path.join(dataDir, 'VERSION'));
    }

    // 11. .gitignore and .gitattributes (project files — skipped at user scope)
    if (!userScope) {
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
    }

    // 12. Generate settings.json
    const settingsDest = path.join(claudeDir, 'settings.json');
    let settingsObj;
    if (fs.existsSync(settingsDest)) {
      ui.warning('settings.json already exists — merging skill permissions and hooks');
      const { mergeSettings } = require('./settings');
      settingsObj = mergeSettings(packageRoot, settingsDest, selectedSkills);
    } else {
      settingsObj = generateSettings(packageRoot, manifest, selectedSkills);
    }
    if (userScope) {
      // No per-machine .shipkit/VERSION at user scope — record the version in
      // settings so `update` can detect the installed version.
      settingsObj.shipkit = settingsObj.shipkit || {};
      settingsObj.shipkit.version = version;
    }
    fs.writeFileSync(settingsDest, JSON.stringify(settingsObj, null, 2) + '\n', 'utf8');
    ui.success('settings.json configured');

    // 13. CLAUDE.md (project-oriented template — skipped at user scope; framework
    // behavior is carried by the user-level rules file instead)
    let claudeMdPreserved = false;
    if (userScope) {
      ui.info('CLAUDE.md skipped (user scope — framework rules cover behavior)');
    } else if (handleClaudeMd(packageRoot, targetDir, version, claudeMdAction)) {
      ui.success(`CLAUDE.md ${claudeMdAction === 'install' ? 'created' : claudeMdAction + 'ed'}`);
    } else if (claudeMdAction === 'merge') {
      claudeMdPreserved = true;
      ui.info('CLAUDE.md preserved (already has Shipkit content)');
    } else {
      ui.info('CLAUDE.md skipped');
    }

    // 14. Install skills
    const skillsDir = path.join(installDir, 'skills');
    let skillCount = 0;
    for (const skillName of selectedSkills) {
      const src = path.join(skillsDir, skillName);
      if (fs.existsSync(src)) {
        copyDir(src, path.join(claudeDir, 'skills', skillName));
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
        copyFile(src, path.join(claudeDir, 'agents', `${agentName}.md`));
        agentCount++;
      }
    }
    ui.success(`${agentCount} agents installed`);

    // 16. MCP example (project file — skipped at user scope)
    if (!flags.noMcps && !userScope) {
      if (generateMcpExample(manifest, targetDir)) {
        ui.success('.mcp.json.example created');
      }
    }

    // 17. HTML overview (lives in per-project .shipkit/ — skipped at user scope)
    if (dataDir) {
      const overviewSrc = path.join(packageRoot, 'docs', 'generated', 'shipkit-overview.html');
      if (fs.existsSync(overviewSrc)) {
        let html = fs.readFileSync(overviewSrc, 'utf8');
        html = html.replace(/\{\{SHIPKIT_VERSION\}\}/g, `v${version}`);
        fs.writeFileSync(path.join(dataDir, 'shipkit-overview.html'), html, 'utf8');
        ui.success('Overview page installed');
      }
    }

    // Done!
    console.log();
    ui.section('Installation Complete');
    if (userScope) {
      ui.success(`Shipkit v${version} installed at user level (${claudeDir})`);
      console.log();
      ui.bullet('Shipkit skills/agents are now available in every project');
      ui.bullet('Open Claude Code in any project and run /shipkit-project-context to activate it there');
      ui.bullet('That first skill creates the project .shipkit/ folder; full context loads from then on');
      console.log();
    } else {
      ui.success(`Shipkit v${version} installed to ${targetDir}`);
      console.log();
      ui.bullet('Open Claude Code in this directory to start using Shipkit');
      ui.bullet('Run /shipkit-master to see available skills');
      ui.bullet('Run /shipkit-why-project to define your project vision');
      console.log();
    }
    if (claudeMdPreserved) {
      ui.warning('CLAUDE.md was not updated (your customizations were preserved)');
      ui.info(`  Framework rules are auto-loaded from .claude/rules/shipkit.md`);
      ui.info(`  To refresh CLAUDE.md: ${ui.colors.dim}run /shipkit-claude-md in Claude Code${ui.colors.reset}`);
      console.log();
    }
    ui.info(`To enable MCPs: ${ui.colors.dim}cp .mcp.json.example .mcp.json${ui.colors.reset}`);
    ui.info(`To update later: ${ui.colors.dim}npx github:stefan-stepzero/shipkit update${ui.colors.reset}`);
    console.log();

  } finally {
    if (rl) rl.close();
  }
}

module.exports = { init };
