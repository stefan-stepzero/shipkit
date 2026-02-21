'use strict';

const fs = require('fs');
const path = require('path');

/**
 * Read the CLAUDE.md template and replace the version placeholder.
 */
function readTemplate(packageRoot, version) {
  const templatePath = path.join(packageRoot, 'install', 'claude-md', 'shipkit.md');
  const content = fs.readFileSync(templatePath, 'utf8');
  return content.replace(/\{\{SHIPKIT_VERSION\}\}/g, `v${version}`);
}

/**
 * Install CLAUDE.md (fresh — no existing file).
 */
function installClaudeMd(packageRoot, targetDir, version) {
  const content = readTemplate(packageRoot, version);
  fs.writeFileSync(path.join(targetDir, 'CLAUDE.md'), content, 'utf8');
}

/**
 * Overwrite existing CLAUDE.md with template.
 */
function overwriteClaudeMd(packageRoot, targetDir, version) {
  installClaudeMd(packageRoot, targetDir, version);
}

/**
 * Merge Shipkit sections into existing CLAUDE.md.
 * Appends sections that don't already exist.
 */
function mergeClaudeMd(packageRoot, targetDir, version) {
  const destPath = path.join(targetDir, 'CLAUDE.md');
  const existing = fs.readFileSync(destPath, 'utf8');
  const template = readTemplate(packageRoot, version);

  // Already merged? Check for Shipkit markers
  if (existing.includes('/shipkit-') && existing.includes('Shipkit')) {
    // Looks like Shipkit sections already present — check for version update
    const versionPattern = /# Shipkit Integration v[\d.]+/;
    if (versionPattern.test(existing)) {
      // Update version in existing merge header
      const updated = existing.replace(versionPattern, `# Shipkit Integration v${version}`);
      if (updated !== existing) {
        fs.writeFileSync(destPath, updated, 'utf8');
      }
      return;
    }
    // Has Shipkit content but no merge header — leave it alone
    return;
  }

  // Extract sections from template to append
  const sections = [
    '## Working Preferences',
    '## Project Learnings',
  ];

  const sectionsToAdd = [];
  for (const sectionHeader of sections) {
    if (template.includes(sectionHeader) && !existing.includes(sectionHeader)) {
      const startIdx = template.indexOf(sectionHeader);
      // Find next section or end of file
      let endIdx = template.length;
      for (const other of sections) {
        if (other !== sectionHeader) {
          const otherIdx = template.indexOf(other);
          if (otherIdx > startIdx && otherIdx < endIdx) {
            endIdx = otherIdx;
          }
        }
      }
      sectionsToAdd.push(template.slice(startIdx, endIdx).trim());
    }
  }

  // Also add the @import lines if not present
  const imports = [];
  const importPattern = /^@[^\n]+$/gm;
  let match;
  while ((match = importPattern.exec(template)) !== null) {
    if (!existing.includes(match[0])) {
      imports.push(match[0]);
    }
  }

  if (sectionsToAdd.length === 0 && imports.length === 0) return;

  let appendContent = `\n\n---\n\n# Shipkit Integration v${version}\n\n`;
  if (imports.length > 0) {
    appendContent += imports.join('\n') + '\n\n';
  }
  if (sectionsToAdd.length > 0) {
    appendContent += sectionsToAdd.join('\n\n---\n\n') + '\n';
  }

  fs.writeFileSync(destPath, existing.trimEnd() + appendContent, 'utf8');
}

/**
 * Handle CLAUDE.md based on the chosen action.
 */
function handleClaudeMd(packageRoot, targetDir, version, action) {
  switch (action) {
    case 'install':
    case 'overwrite':
      installClaudeMd(packageRoot, targetDir, version);
      return true;
    case 'merge':
      mergeClaudeMd(packageRoot, targetDir, version);
      return true;
    case 'skip':
      return false;
    default:
      return false;
  }
}

module.exports = { handleClaudeMd };
