'use strict';

const fs = require('fs');
const path = require('path');

/**
 * Load the canonical settings template from install/settings/shipkit.settings.json.
 * That file is the single source of truth for hooks, env, permissions scaffold,
 * and workspace config. This loader strips the editorial _notes block and replaces
 * the skill allow-list with the caller's selected set.
 */
function loadCanonicalSettings(packageRoot) {
  const canonicalPath = path.join(
    packageRoot,
    'install',
    'settings',
    'shipkit.settings.json'
  );
  const raw = fs.readFileSync(canonicalPath, 'utf8');
  return JSON.parse(raw);
}

function applySkillAllowList(settings, selectedSkills) {
  settings.permissions = settings.permissions || {};
  const allow = Array.isArray(settings.permissions.allow)
    ? settings.permissions.allow.filter(p => !p.startsWith('Skill('))
    : [];
  for (const skill of selectedSkills) {
    allow.push(`Skill(${skill})`);
  }
  settings.permissions.allow = allow;
  return settings;
}

/**
 * Generate a fresh settings.json for a new install.
 * Reads install/settings/shipkit.settings.json verbatim and splices in the
 * selected skill allow-list. No hand-maintained duplication.
 */
function generateSettings(packageRoot, manifest, selectedSkills) {
  const settings = loadCanonicalSettings(packageRoot);
  applySkillAllowList(settings, selectedSkills);

  delete settings._notes;
  settings._notes = {
    edition: `${manifest.edition} - ${manifest.description}`,
    customization: 'Users can override by editing this file',
  };

  return settings;
}

/**
 * Merge existing settings.json — preserve non-shipkit customization, refresh
 * the shipkit-owned sections (hooks, skill allow-list) from the canonical JSON.
 */
function mergeSettings(packageRoot, settingsPath, selectedSkills) {
  const existing = JSON.parse(fs.readFileSync(settingsPath, 'utf8'));
  const canonical = loadCanonicalSettings(packageRoot);

  existing.permissions = existing.permissions || {};
  const existingAllow = Array.isArray(existing.permissions.allow)
    ? existing.permissions.allow.filter(p => !p.startsWith('Skill('))
    : [];
  for (const skill of selectedSkills) {
    existingAllow.push(`Skill(${skill})`);
  }
  existing.permissions.allow = existingAllow;

  existing.hooks = canonical.hooks;

  existing.shipkit = existing.shipkit || {};
  existing.shipkit.installedSkills = selectedSkills;

  return existing;
}

module.exports = { generateSettings, mergeSettings };
