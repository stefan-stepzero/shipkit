'use strict';

const fs = require('fs');
const path = require('path');
const ui = require('./ui');
const { createInterface, confirm, promptForSkills, promptForAgents } = require('./prompt');
const { loadManifest, getAllSkillNames, getAllAgentNames } = require('./manifest');
const { mergeSettings } = require('./settings');
const { ensureDir, copyFile, copyDir, makeExecutable } = require('./copy');

// Hook files: source name -> destination name (same as init)
const HOOK_FILES = {
  'shipkit-session-start.py': 'session-start.py',
  'shipkit-after-skill-router.py': 'after-skill-router.py',
  'shipkit-relentless-stop-hook.py': 'shipkit-relentless-stop-hook.py',
  'shipkit-track-skill-usage.py': 'shipkit-track-skill-usage.py',
  'shipkit-task-completed-hook.py': 'shipkit-task-completed-hook.py',
  'shipkit-teammate-idle-hook.py': 'shipkit-teammate-idle-hook.py',
};

async function update(packageRoot, flags) {
  const version = fs.readFileSync(path.join(packageRoot, 'VERSION'), 'utf8').trim();
  const targetDir = path.resolve(flags.target || process.cwd());
  const nonInteractive = flags.yes;
  const installDir = path.join(packageRoot, 'install');

  ui.logo(version);
  ui.section('Update Shipkit');
  ui.info(`Target: ${targetDir}`);

  // Verify existing installation
  const settingsPath = path.join(targetDir, '.claude', 'settings.json');
  if (!fs.existsSync(settingsPath)) {
    throw new Error(
      'No existing Shipkit installation found (.claude/settings.json missing).\n' +
      'Run "npx shipkit init" for a fresh install.'
    );
  }

  // Read current settings to determine installed state
  const currentSettings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'));
  const currentSkills = (currentSettings.shipkit && currentSettings.shipkit.installedSkills) || [];

  // Check installed version
  const versionPath = path.join(targetDir, '.shipkit', 'VERSION');
  const installedVersion = fs.existsSync(versionPath)
    ? fs.readFileSync(versionPath, 'utf8').trim()
    : 'unknown';

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
    ensureDir(path.join(targetDir, '.claude', 'hooks'));
    const hooksDir = path.join(installDir, 'shared', 'hooks');
    for (const [src, dest] of Object.entries(HOOK_FILES)) {
      const srcPath = path.join(hooksDir, src);
      const destPath = path.join(targetDir, '.claude', 'hooks', dest);
      if (fs.existsSync(srcPath)) {
        copyFile(srcPath, destPath);
        makeExecutable(destPath);
      }
    }
    ui.success('Hooks updated');

    // 2. Update rules (overwrite)
    const rulesDir = path.join(installDir, 'rules');
    if (fs.existsSync(rulesDir)) {
      ensureDir(path.join(targetDir, '.claude', 'rules'));
      copyDir(rulesDir, path.join(targetDir, '.claude', 'rules'));
    }
    ui.success('Rules updated');

    // 3. Update scripts (overwrite)
    const pythonScriptsDir = path.join(installDir, 'shared', 'scripts', 'python');
    if (fs.existsSync(pythonScriptsDir)) {
      ensureDir(path.join(targetDir, '.shipkit', 'scripts'));
      copyDir(pythonScriptsDir, path.join(targetDir, '.shipkit', 'scripts'));
    }
    ui.success('Scripts updated');

    // 4. Update VERSION
    copyFile(path.join(packageRoot, 'VERSION'), path.join(targetDir, '.shipkit', 'VERSION'));

    // 5. Merge settings.json
    const merged = mergeSettings(settingsPath, selectedSkills);
    fs.writeFileSync(settingsPath, JSON.stringify(merged, null, 2) + '\n', 'utf8');
    ui.success('settings.json merged (custom permissions preserved)');

    // 6. Update skills (overwrite selected, remove deselected)
    const skillsDestDir = path.join(targetDir, '.claude', 'skills');
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
    const agentsDestDir = path.join(targetDir, '.claude', 'agents');
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

    // 8. Update HTML overview
    const overviewSrc = path.join(packageRoot, 'docs', 'generated', 'shipkit-overview.html');
    if (fs.existsSync(overviewSrc)) {
      let html = fs.readFileSync(overviewSrc, 'utf8');
      html = html.replace(/\{\{SHIPKIT_VERSION\}\}/g, `v${version}`);
      fs.writeFileSync(path.join(targetDir, '.shipkit', 'shipkit-overview.html'), html, 'utf8');
    }

    // Done!
    console.log();
    ui.section('Update Complete');
    ui.success(`Shipkit updated to v${version}`);
    console.log();
    ui.bullet('CLAUDE.md was not modified (user-managed file)');
    ui.bullet('.gitignore was not modified');
    ui.info('If you need to regenerate CLAUDE.md, run: npx shipkit init --claude-md overwrite');
    console.log();

  } finally {
    if (rl) rl.close();
  }
}

module.exports = { update };
