'use strict';

const fs = require('fs');
const path = require('path');

/**
 * sync-docs: Generate skill/agent counts and lists from the manifest
 * into docs files using marker comments.
 *
 * Markers:
 *   <!-- sync:SECTION_NAME -->
 *   ...generated content...
 *   <!-- /sync:SECTION_NAME -->
 *
 * For HTML stat-number spans:
 *   <!-- sync:skill_count --><span class="stat-number">36</span><!-- /sync:skill_count -->
 */

// ---------------------------------------------------------------------------
// Manifest reading
// ---------------------------------------------------------------------------

function loadManifest(packageRoot) {
  const manifestPath = path.join(packageRoot, 'install', 'profiles', 'shipkit.manifest.json');
  return JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
}

// Infrastructure skills are auto-triggered hooks, not user-invocable.
// They appear in mandatory[] but are excluded from the public skill count.
const INFRASTRUCTURE_SKILLS = ['shipkit-detect'];

function countSkills(manifest) {
  const mandatory = (manifest.skills.mandatory || [])
    .filter(s => !INFRASTRUCTURE_SKILLS.includes(s));
  const optional = manifest.skills.optional || {};
  let count = mandatory.length;
  for (const category of Object.values(optional)) {
    count += category.length;
  }
  return count;
}

function countAgents(manifest) {
  return (manifest.agents || []).length;
}

function getAgents(manifest) {
  return manifest.agents || [];
}

function getSkillsByCategory(manifest) {
  return manifest.skills.optional || {};
}

function getMandatorySkills(manifest) {
  return manifest.skills.mandatory || [];
}

// ---------------------------------------------------------------------------
// Marker-based replacement
// ---------------------------------------------------------------------------

/**
 * Replace content between <!-- sync:NAME --> and <!-- /sync:NAME --> markers.
 * Supports both block markers (content on separate lines) and inline markers
 * (content on same line).
 */
function replaceMarker(content, name, replacement) {
  // Block pattern: markers on their own lines with content between
  const blockPattern = new RegExp(
    `(<!-- sync:${name} -->)\\n[\\s\\S]*?\\n(<!-- /sync:${name} -->)`,
    'g'
  );
  if (blockPattern.test(content)) {
    return content.replace(blockPattern, `$1\n${replacement}\n$2`);
  }

  // Inline pattern: markers on same line (for HTML spans, etc.)
  const inlinePattern = new RegExp(
    `(<!-- sync:${name} -->)[\\s\\S]*?(<!-- /sync:${name} -->)`,
    'g'
  );
  return content.replace(inlinePattern, `$1${replacement}$2`);
}

// ---------------------------------------------------------------------------
// Generators — produce replacement content for each marker
// ---------------------------------------------------------------------------

function generateReadmeSummary(manifest) {
  const categories = getSkillsByCategory(manifest);
  const lines = [];
  for (const [catName, skills] of Object.entries(categories)) {
    lines.push(`- **${catName}** (${skills.length}) - ${skills.map(s => s.name.replace('shipkit-', '')).slice(0, 3).join(', ')}${skills.length > 3 ? ', ...' : ''}`);
  }
  return lines.join('\n');
}

function generateReadmeAgentTable(manifest) {
  const agents = getAgents(manifest);
  const lines = [
    '| Agent | Used For |',
    '|-------|----------|',
  ];
  for (const agent of agents) {
    lines.push(`| \`${agent.name}\` | ${agent.desc} |`);
  }
  return lines.join('\n');
}

// ---------------------------------------------------------------------------
// File processors
// ---------------------------------------------------------------------------

function processFile(filePath, manifest) {
  if (!fs.existsSync(filePath)) return { path: filePath, updated: false, reason: 'not found' };

  const original = fs.readFileSync(filePath, 'utf8');
  let content = original;

  const skillCount = countSkills(manifest);
  const agentCount = countAgents(manifest);

  // Universal count markers
  content = replaceMarker(content, 'skill_count', String(skillCount));
  content = replaceMarker(content, 'agent_count', String(agentCount));

  // README-specific markers
  content = replaceMarker(content, 'readme_summary', generateReadmeSummary(manifest));
  content = replaceMarker(content, 'readme_agent_table', generateReadmeAgentTable(manifest));

  // HTML stat-number markers (inline)
  content = replaceMarker(content, 'html_skill_count', `<span class="stat-number">${skillCount}</span>`);
  content = replaceMarker(content, 'html_agent_count', `<span class="stat-number">${agentCount}</span>`);

  if (content !== original) {
    fs.writeFileSync(filePath, content, 'utf8');
    return { path: filePath, updated: true };
  }
  return { path: filePath, updated: false, reason: 'no changes' };
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

function syncDocs(packageRoot) {
  const manifest = loadManifest(packageRoot);
  const skillCount = countSkills(manifest);
  const agentCount = countAgents(manifest);

  const targets = [
    path.join(packageRoot, 'README.md'),
    path.join(packageRoot, 'installers', 'README.md'),
    path.join(packageRoot, 'docs', 'generated', 'shipkit-overview.html'),
  ];

  const results = targets.map(f => processFile(f, manifest));

  return { skillCount, agentCount, results };
}

module.exports = { syncDocs, loadManifest, countSkills, countAgents };
