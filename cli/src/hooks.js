'use strict';

/**
 * Canonical hooks configuration — single source of truth.
 * Must match install/settings/shipkit.settings.json exactly.
 */
function buildHooksConfig() {
  return {
    SessionStart: [
      {
        matcher: 'startup|resume|clear|compact',
        hooks: [
          {
            type: 'command',
            command: 'python -X utf8 .claude/hooks/session-start.py',
          },
        ],
      },
    ],
    PostToolUse: [
      {
        matcher: 'Skill',
        hooks: [
          {
            type: 'command',
            command: 'python -X utf8 .claude/hooks/shipkit-track-skill-usage.py',
          },
        ],
      },
    ],
    PreToolUse: [],
    Stop: [
      {
        hooks: [
          {
            type: 'command',
            command: 'python -X utf8 .claude/hooks/after-skill-router.py',
          },
        ],
      },
      {
        hooks: [
          {
            type: 'command',
            command: 'python -X utf8 .claude/hooks/shipkit-relentless-stop-hook.py',
            timeout: 180,
          },
        ],
      },
    ],
    PreCompact: [
      {
        hooks: [
          {
            type: 'prompt',
            prompt:
              'Context compaction is approaching. If significant work is in progress, consider running /shipkit-work-memory to save your current work state before details are lost.',
          },
        ],
      },
    ],
    TeammateIdle: [
      {
        hooks: [
          {
            type: 'command',
            command: 'python -X utf8 .claude/hooks/shipkit-teammate-idle-hook.py',
          },
        ],
      },
    ],
    TaskCompleted: [
      {
        hooks: [
          {
            type: 'command',
            command: 'python -X utf8 .claude/hooks/shipkit-task-completed-hook.py',
            timeout: 120,
          },
        ],
      },
    ],
  };
}

module.exports = { buildHooksConfig };
