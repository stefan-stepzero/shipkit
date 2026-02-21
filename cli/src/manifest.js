'use strict';

const fs = require('fs');
const path = require('path');

function loadManifest(packageRoot, profile) {
  const manifestPath = path.join(packageRoot, 'install', 'profiles', `${profile}.manifest.json`);
  if (!fs.existsSync(manifestPath)) {
    throw new Error(`Profile "${profile}" not found at ${manifestPath}`);
  }
  return JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
}

function getAllSkillNames(manifest) {
  const mandatory = manifest.skills.mandatory || [];
  const optional = [];
  for (const category of Object.values(manifest.skills.optional || {})) {
    for (const skill of category) {
      optional.push(skill.name);
    }
  }
  return [...mandatory, ...optional];
}

function getAllAgentNames(manifest) {
  return (manifest.agents || []).map(a => a.name);
}

module.exports = { loadManifest, getAllSkillNames, getAllAgentNames };
