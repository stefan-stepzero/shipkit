'use strict';

const fs = require('fs');
const { buildHooksConfig } = require('./hooks');

/**
 * Generate a fresh settings.json object for a new install.
 * Matches install/settings/shipkit.settings.json structure.
 */
function generateSettings(manifest, selectedSkills) {
  const skillPerms = selectedSkills.map(s => `Skill(${s})`);

  return {
    permissions: {
      allow: [
        // Read permissions
        'Read',
        'Read(.env.example)',
        'Read(**/.env.example)',
        'Read(.env.*.example)',
        'Read(**/.env.*.example)',

        // Write permissions — source code
        'Write(src/**)',
        'Write(app/**)',
        'Write(components/**)',
        'Write(lib/**)',
        'Write(utils/**)',
        'Write(tests/**)',
        'Write(__tests__/**)',
        'Write(*.ts)',
        'Write(*.tsx)',
        'Write(*.js)',
        'Write(*.jsx)',
        'Write(*.py)',
        'Write(*.json)',
        'Write(*.md)',
        'Write(*.yaml)',
        'Write(*.yml)',
        'Write(*.toml)',
        'Write(*.html)',
        'Write(*.css)',
        'Write(*.scss)',
        'Write(*.sass)',
        'Write(*.sh)',
        'Write(*.sql)',
        'Write(*.xml)',
        'Write(*.txt)',
        'Write(package.json)',
        'Write(pyproject.toml)',
        'Write(requirements.txt)',

        // Write permissions — framework
        'Write(.claude/**)',
        'Write(.shipkit/**)',
        'Write(.shipkit-archive/**)',

        // Bash permissions
        'Bash(git *)',
        'Bash(python *)',
        'Bash(pip *)',
        'Bash(poetry *)',
        'Bash(pytest *)',
        'Bash(black *)',
        'Bash(ruff *)',
        'Bash(mypy *)',
        'Bash(uvicorn *)',
        'Bash(node *)',
        'Bash(npm *)',
        'Bash(npx *)',
        'Bash(pnpm *)',
        'Bash(yarn *)',
        'Bash(tsc *)',
        'Bash(eslint *)',
        'Bash(prettier *)',
        'Bash(vercel *)',
        'Bash(docker *)',
        'Bash(docker-compose *)',
        'Bash(ls *)',
        'Bash(cat *)',
        'Bash(grep *)',
        'Bash(find *)',
        'Bash(wc *)',
        'Bash(chmod *)',
        'Bash(pwd *)',
        'Bash(cd *)',
        'Bash(echo *)',
        'Bash(mkdir *)',
        'Bash(touch *)',
        'Bash(mv *)',
        'Bash(cp *)',
        'Bash(rm *)',
        'Bash(curl *)',
        'Bash(wget *)',
        'Bash(sed *)',
        'Bash(awk *)',
        'Bash(sort *)',
        'Bash(uniq *)',
        'Bash(diff *)',
        'Bash(tree *)',
        'Bash(gh *)',

        // WebFetch permissions
        'WebFetch(domain:github.com)',
        'WebFetch(domain:raw.githubusercontent.com)',
        'WebFetch(domain:docs.anthropic.com)',
        'WebFetch(domain:nextjs.org)',
        'WebFetch(domain:python.org)',
        'WebFetch(domain:fastapi.tiangolo.com)',
        'WebFetch(domain:pypi.org)',
        'WebFetch(domain:npmjs.com)',
        'WebFetch(domain:stackoverflow.com)',
        'WebFetch(domain:developer.mozilla.org)',

        // Skill permissions
        ...skillPerms,
      ],

      deny: [
        'Bash(sudo *)',
        'Bash(su *)',
        'Bash(ssh *)',
      ],
    },

    env: {
      CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS: '1',
    },

    teammateMode: 'in-process',
    defaultMode: 'acceptEdits',

    hooks: buildHooksConfig(),

    skills: {
      description: 'Skill configuration and defaults',
      autoLoadConstitutions: false,
    },

    workspace: {
      description: 'Workspace paths and conventions',
      contextPath: '.shipkit',
      specsPath: '.shipkit/specs',
      plansPath: '.shipkit/plans',
    },

    _notes: {
      edition: `${manifest.edition} - ${manifest.description}`,
      permissionsPhilosophy: 'Allow by default, deny only critical infrastructure and context files.',
      customization: 'Users can override by editing this file',
    },
  };
}

/**
 * Merge existing settings.json — preserve custom config, update Skill() + hooks.
 */
function mergeSettings(settingsPath, selectedSkills) {
  const settings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'));

  // Strip old Skill() entries
  if (settings.permissions && settings.permissions.allow) {
    settings.permissions.allow = settings.permissions.allow.filter(
      p => !p.startsWith('Skill(')
    );
  } else {
    settings.permissions = settings.permissions || {};
    settings.permissions.allow = [];
  }

  // Add new Skill() entries
  for (const skill of selectedSkills) {
    settings.permissions.allow.push(`Skill(${skill})`);
  }

  // Replace hooks entirely (canonical source of truth)
  settings.hooks = buildHooksConfig();

  // Update metadata
  settings.shipkit = settings.shipkit || {};
  settings.shipkit.installedSkills = selectedSkills;

  return settings;
}

module.exports = { generateSettings, mergeSettings };
