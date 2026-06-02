'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const ui = require('./ui');
const { createInterface, confirm, promptForSkills, promptForAgents } = require('./prompt');
const { loadManifest, getAllSkillNames, getAllAgentNames } = require('./manifest');
const { mergeSettings } = require('./settings');
const { ensureDir, copyFile, copyDir, makeExecutable } = require('./copy');

// Hook files: source name -> destination name (same as init)
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
};

async function update(packageRoot, flags) {
  const version = fs.readFileSync(path.join(packageRoot, 'VERSION'), 'utf8').trim();
  const targetDir = path.resolve(flags.target || process.cwd());
  const nonInteractive = flags.yes;
  const installDir = path.join(packageRoot, 'install');

  // Scope split (mirrors init.js): user-level code in ~/.claude, no ~/.shipkit.
  const userScope = !!flags.user;
  const claudeDir = userScope ? path.join(os.homedir(), '.claude') : path.join(targetDir, '.claude');
  const dataDir = userScope ? null : path.join(targetDir, '.shipkit');

  ui.logo(version);
  ui.section(userScope ? 'Update Shipkit (user level)' : 'Update Shipkit');
  ui.info(`Target: ${userScope ? claudeDir : targetDir}`);

  // Verify existing installation
  const settingsPath = path.join(claudeDir, 'settings.json');
  if (!fs.existsSync(settingsPath)) {
    throw new Error(
      `No existing Shipkit installation found (${settingsPath} missing).\n` +
      `Run "npx github:stefan-stepzero/shipkit init${userScope ? ' --user' : ''}" for a fresh install.`
    );
  }

  // Read current settings to determine installed state
  const currentSettings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'));
  const currentSkills = (currentSettings.shipkit && currentSettings.shipkit.installedSkills) || [];

  // Check installed version: user scope records it in settings (no ~/.shipkit/VERSION).
  let installedVersion;
  if (userScope) {
    installedVersion = (currentSettings.shipkit && currentSettings.shipkit.version) || 'unknown';
  } else {
    const versionPath = path.join(dataDir, 'VERSION');
    installedVersion = fs.existsSync(versionPath)
      ? fs.readFileSync(versionPath, 'utf8').trim()
      : 'unknown';
  }

  ui.info(`Installed version: ${installedVersion}`);
  ui.info(`Updating to: ${version}`);

  if (installedVersion === version && !nonInteractive) {
    ui.info('Already on latest version.');
  }

  // Determine profile from settings or flag
  const profile = flags.profile ||
    (currentSettings._notes && currentSettings._notes.edition || '').split(' ')[0].toLowerCase() ||
    'shipkit';

  let manifest;
  try {
    manifest = loadManifest(packageRoot, profile);
  } catch (_) {
    manifest = loadManifest(packageRoot, 'shipkit');
  }

  let rl;
  if (!nonInteractive) {
    rl = createInterface();
  }

  try {
    // Select skills
    let selectedSkills;
    if (flags.allSkills || nonInteractive) {
      selectedSkills = getAllSkillNames(manifest);
    } else {
      // Show what changed
      const allAvailable = getAllSkillNames(manifest);
      const newSkills = allAvailable.filter(s => !currentSkills.includes(s));
      const removedSkills = currentSkills.filter(s => !allAvailable.includes(s));

      if (newSkills.length > 0) {
        console.log(`\n  ${ui.colors.green}New skills available:${ui.colors.reset}`);
        newSkills.forEach(s => ui.bullet(s));
      }
      if (removedSkills.length > 0) {
        console.log(`\n  ${ui.colors.yellow}Skills no longer available:${ui.colors.reset}`);
        removedSkills.forEach(s => ui.bullet(s));
      }

      selectedSkills = await promptForSkills(rl, manifest);
    }

    // Select agents
    let selectedAgents;
    if (flags.noAgents) {
      selectedAgents = [];
    } else if (flags.allAgents || nonInteractive) {
      selectedAgents = getAllAgentNames(manifest);
    } else {
      selectedAgents = await promptForAgents(rl, manifest);
    }

    // Confirm
    if (!nonInteractive) {
      console.log();
      ui.section('Update Summary');
      ui.bullet(`Skills: ${selectedSkills.length}`);
      ui.bullet(`Agents: ${selectedAgents.length}`);
      ui.bullet(`Version: ${installedVersion} -> ${version}`);
      console.log();

      const ok = await confirm(rl, 'Apply update?');
      if (!ok) {
        ui.warning('Update cancelled.');
        return;
      }
    }

    if (rl) rl.close();
    rl = null;

    console.log();
    ui.section('Updating');

    // 1. Update hooks (overwrite)
    ensureDir(path.join(claudeDir, 'hooks'));
    const hooksDir = path.join(installDir, 'shared', 'hooks');
    for (const [src, dest] of Object.entries(HOOK_FILES)) {
      const srcPath = path.join(hooksDir, src);
      const destPath = path.join(claudeDir, 'hooks', dest);
      if (fs.existsSync(srcPath)) {
        copyFile(srcPath, destPath);
        makeExecutable(destPath);
      }
    }
    ui.success('Hooks updated');

    // 2. Update rules (overwrite)
    const rulesDir = path.join(installDir, 'rules');
    if (fs.existsSync(rulesDir)) {
      const rulesDestDir = path.join(claudeDir, 'rules');
      ensureDir(rulesDestDir);
      copyDir(rulesDir, rulesDestDir);
      if (userScope) {
        // Re-apply Shipkit-project path gating (overwrite above stripped it).
        const shipkitRule = path.join(rulesDestDir, 'shipkit.md');
        if (fs.existsSync(shipkitRule)) {
          const body = fs.readFileSync(shipkitRule, 'utf8');
          if (!body.startsWith('---')) {
            fs.writeFileSync(shipkitRule, '---\npaths:\n  - "**/.shipkit/**"\n---\n\n' + body, 'utf8');
          }
        }
      }
    }
    ui.success(userScope ? 'Rules updated (scoped to Shipkit projects)' : 'Rules updated');

    // 3 / 3b / 4. Update scripts + VERSION marker (per-project .shipkit only)
    if (dataDir) {
      const pythonScriptsDir = path.join(installDir, 'shared', 'scripts', 'python');
      if (fs.existsSync(pythonScriptsDir)) {
        ensureDir(path.join(dataDir, 'scripts'));
        copyDir(pythonScriptsDir, path.join(dataDir, 'scripts'));
      }
      const obsScriptsDir = path.join(installDir, 'shared', 'scripts', 'observability');
      if (fs.existsSync(obsScriptsDir)) {
        const obsDestDir = path.join(dataDir, 'observability');
        ensureDir(obsDestDir);
        copyDir(obsScriptsDir, obsDestDir);
      }
      ui.success('Scripts updated');
      copyFile(path.join(packageRoot, 'VERSION'), path.join(dataDir, 'VERSION'));
    }

    // 5. Merge settings.json (user scope: also record the new version marker)
    const merged = mergeSettings(packageRoot, settingsPath, selectedSkills);
    if (userScope) {
      merged.shipkit = merged.shipkit || {};
      merged.shipkit.version = version;
    }
    fs.writeFileSync(settingsPath, JSON.stringify(merged, null, 2) + '\n', 'utf8');
    ui.success('settings.json merged (custom permissions preserved)');

    // 6. Update skills (overwrite selected, remove deselected)
    const skillsDestDir = path.join(claudeDir, 'skills');
    const skillsDir = path.join(installDir, 'skills');
    let skillsUpdated = 0;

    // Remove deselected skills (only shipkit-* prefixed)
    if (fs.existsSync(skillsDestDir)) {
      for (const entry of fs.readdirSync(skillsDestDir)) {
        if (entry.startsWith('shipkit-') && !selectedSkills.includes(entry)) {
          const fullPath = path.join(skillsDestDir, entry);
          fs.rmSync(fullPath, { recursive: true, force: true });
        }
      }
    }

    // Install/update selected skills
    for (const skillName of selectedSkills) {
      const src = path.join(skillsDir, skillName);
      if (fs.existsSync(src)) {
        copyDir(src, path.join(skillsDestDir, skillName));
        skillsUpdated++;
      }
    }
    ui.success(`${skillsUpdated} skills updated`);

    // 7. Update agents (overwrite selected, remove deselected)
    const agentsDestDir = path.join(claudeDir, 'agents');
    ensureDir(agentsDestDir);
    const agentsDir = path.join(installDir, 'agents');
    let agentsUpdated = 0;

    // Remove deselected agents (only shipkit-* prefixed)
    for (const entry of fs.readdirSync(agentsDestDir)) {
      if (entry.startsWith('shipkit-')) {
        const agentName = entry.replace('.md', '');
        if (!selectedAgents.includes(agentName)) {
          fs.rmSync(path.join(agentsDestDir, entry), { force: true });
        }
      }
    }

    // Install/update selected agents
    for (const agentName of selectedAgents) {
      const src = path.join(agentsDir, `${agentName}.md`);
      if (fs.existsSync(src)) {
        copyFile(src, path.join(agentsDestDir, `${agentName}.md`));
        agentsUpdated++;
      }
    }
    ui.success(`${agentsUpdated} agents updated`);

    // 8. Update HTML overview (per-project .shipkit only)
    if (dataDir) {
      const overviewSrc = path.join(packageRoot, 'docs', 'generated', 'shipkit-overview.html');
      if (fs.existsSync(overviewSrc)) {
        let html = fs.readFileSync(overviewSrc, 'utf8');
        html = html.replace(/\{\{SHIPKIT_VERSION\}\}/g, `v${version}`);
        fs.writeFileSync(path.join(dataDir, 'shipkit-overview.html'), html, 'utf8');
      }
    }

    // Done!
    console.log();
    ui.section('Update Complete');
    ui.success(`Shipkit updated to v${version}`);
    console.log();
    if (userScope) {
      ui.info(`  Framework rules are auto-loaded from ${path.join(claudeDir, 'rules', 'shipkit.md')} (scoped to Shipkit projects)`);
      ui.bullet('All projects pick up the update on their next session');
    } else {
      ui.warning('CLAUDE.md was not updated (your customizations were preserved)');
      ui.info(`  Framework rules are auto-loaded from .claude/rules/shipkit.md`);
      ui.info(`  To refresh CLAUDE.md: run /shipkit-claude-md in Claude Code`);
      ui.bullet('.gitignore was not modified');
    }
    console.log();

  } finally {
    if (rl) rl.close();
  }
}

module.exports = { update };
