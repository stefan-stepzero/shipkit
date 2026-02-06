# Remaining Enhancements

**Status:** Parked
**Created:** 2026-02-06
**Parked:** 2026-02-06
**Reason:** Low-value polish items. Core audit improvements complete.
**Source:** Consolidated from completed audit specs

## Overview

Lower-priority enhancements identified during the Claude Code capabilities audit. These are optional improvements that can be implemented as time permits.

---

## Priority 2: Setup Hook

**Source:** AUDIT-HOOKS-UTILIZATION.md

**Purpose:** Installation verification and maintenance via `--init` and `--maintenance` flags.

**Implementation:**

Create `install/shared/hooks/shipkit-setup-hook.py`:

```python
#!/usr/bin/env python3
"""
Shipkit Setup Hook - Installation verification and maintenance.

Triggered by:
  --init: First-time setup wizard
  --maintenance: Health check and cleanup
"""

import sys
import os
import json
from pathlib import Path

def verify_installation():
    """Verify all Shipkit files are properly installed."""
    required_files = [
        '.claude/settings.json',
        '.claude/skills/shipkit-master/SKILL.md',
        '.claude/hooks/session-start.py',
    ]

    missing = []
    for f in required_files:
        if not Path(f).exists():
            missing.append(f)

    if missing:
        print("⚠️  Shipkit installation incomplete:")
        for f in missing:
            print(f"   Missing: {f}")
        print("\nRun the installer again to fix.")
        return False

    print("✓ Shipkit installation verified")
    return True

def run_maintenance():
    """Run cleanup and health checks."""
    print("🔧 Running Shipkit maintenance...")

    # Clean up stale temp files
    stale_patterns = [
        '.shipkit/.last-skill',
        '.shipkit/relentless-state.local.md',
    ]

    cleaned = 0
    for pattern in stale_patterns:
        p = Path(pattern)
        if p.exists():
            p.unlink()
            cleaned += 1

    if cleaned:
        print(f"   Cleaned {cleaned} temporary file(s)")

    # Verify JSON files are valid
    json_files = ['.claude/settings.json', '.shipkit/codebase-index.json']
    for jf in json_files:
        p = Path(jf)
        if p.exists():
            try:
                json.loads(p.read_text())
            except json.JSONDecodeError:
                print(f"   ⚠️  Invalid JSON: {jf}")

    print("✓ Maintenance complete")

def main():
    trigger = os.environ.get('CLAUDE_SETUP_TRIGGER', '')

    if trigger == 'init':
        verify_installation()
    elif trigger == 'maintenance':
        run_maintenance()
    else:
        # Default: just verify
        verify_installation()

if __name__ == '__main__':
    main()
```

**Settings addition:**
```json
"Setup": [
  {
    "hooks": [
      {
        "type": "command",
        "command": "python -X utf8 .claude/hooks/shipkit-setup-hook.py"
      }
    ]
  }
]
```

---

## ~~Priority 3: Modular Rules Structure~~ ✅ IMPLEMENTED

**Status:** Implemented (Option B - Split by Stability)

**What was done:**
- Created `install/rules/shipkit.md` with all framework-managed content
- Restructured `install/claude-md/shipkit.md` to only contain user-editable sections + import
- Updated installer to copy rules to `.claude/rules/shipkit.md`
- Updated shipkit-update, shipkit-claude-md skills
- Updated documentation (README.md, CLAUDE.md)

**New structure:**
```
CLAUDE.md                        # User-editable (preferences, learnings)
.claude/rules/shipkit.md         # Framework rules (replaced on update)
```

---

## Priority 4: Validation Hooks

**Source:** AUDIT-SKILLS-FRONTMATTER.md

**Purpose:** Add PostToolUse hooks to validate skill outputs before saving.

**Skills affected:**
| Skill | Hook | Validation |
|-------|------|------------|
| `shipkit-spec` | PostToolUse on Write | Check spec has all required sections |
| `shipkit-plan` | PostToolUse on Write | Check plan passes validation checklist |
| `shipkit-architecture-memory` | PostToolUse on Write | Check for contradictions |

**Implementation:** Add `hooks` field to skill frontmatter:
```yaml
hooks:
  PostToolUse:
    - matcher: "Write"
      command: "python -X utf8 .claude/hooks/validate-spec.py"
```

---

## Priority 4: SubagentStart/Stop Hooks

**Source:** AUDIT-HOOKS-UTILIZATION.md

**Purpose:** Track agent workflow and optionally inject context.

**Implementation:**

Create `install/shared/hooks/shipkit-agent-hooks.py`:
```python
#!/usr/bin/env python3
"""Track agent invocations for workflow optimization."""

import json
import os
from pathlib import Path
from datetime import datetime

def log_agent_event(event_type: str):
    agent_name = os.environ.get('CLAUDE_AGENT_NAME', 'unknown')
    usage_file = Path('.shipkit/agent-usage.json')

    data = {'agents': {}}
    if usage_file.exists():
        data = json.loads(usage_file.read_text())

    if agent_name not in data['agents']:
        data['agents'][agent_name] = {'count': 0, 'firstUsed': '', 'lastUsed': ''}

    now = datetime.now().isoformat()
    if event_type == 'start':
        data['agents'][agent_name]['count'] += 1
        if not data['agents'][agent_name]['firstUsed']:
            data['agents'][agent_name]['firstUsed'] = now
        data['agents'][agent_name]['lastUsed'] = now

    usage_file.parent.mkdir(exist_ok=True)
    usage_file.write_text(json.dumps(data, indent=2))

if __name__ == '__main__':
    import sys
    event = sys.argv[1] if len(sys.argv) > 1 else 'start'
    log_agent_event(event)
```

---

## Priority 5: PreToolUse Write Guard

**Source:** AUDIT-HOOKS-UTILIZATION.md

**Purpose:** Protect critical `.shipkit/` context files from accidental modification.

**Protected files:**
- `.shipkit/architecture.md` (append-only, use skill)
- `.shipkit/stack.md` (use /shipkit-project-context)
- `.shipkit/schema.md` (use /shipkit-project-context)

**Implementation:**
```python
#!/usr/bin/env python3
"""Warn before modifying protected context files."""

import os
import json

PROTECTED = [
    '.shipkit/architecture.md',
    '.shipkit/stack.md',
    '.shipkit/schema.md',
]

def main():
    tool_input = json.loads(os.environ.get('CLAUDE_TOOL_INPUT', '{}'))
    file_path = tool_input.get('file_path', '')

    for protected in PROTECTED:
        if file_path.endswith(protected):
            print(f"⚠️  Warning: Modifying protected file: {protected}")
            print(f"   Use the appropriate skill instead for structured updates.")
            # Don't block, just warn
            break

if __name__ == '__main__':
    main()
```

---

## Priority 5: Explicit allowed-tools

**Source:** AUDIT-SKILLS-FRONTMATTER.md

**Purpose:** Add explicit tool restrictions to skills that don't have them.

**Skills to update:**
| Skill | Tools to allow |
|-------|---------------|
| `shipkit-spec` | Read, Write, Glob, Grep |
| `shipkit-plan` | Read, Write, Glob, Grep, Bash, Task |
| `shipkit-feedback-bug` | Read, Write, Glob, Grep, Task |
| `shipkit-work-memory` | Read, Write, Bash |
| `shipkit-communications` | Read, Write, Glob |

---

## Priority 5: Language Setting

**Source:** AUDIT-MEMORY-CONTEXT.md

**Purpose:** Add optional language preference prompt to installer.

**Implementation:**
- Add prompt in installer: "Preferred response language? (Enter for English)"
- If set, add `"language": "<value>"` to settings.json

---

## Implementation Order

1. **Setup hook** (P2) - Most value for installation confidence
2. ~~**Modular rules** (P3) - Structural improvement, higher effort~~ ✅ DONE
3. **Validation hooks** (P4) - Quality enforcement
4. **Agent tracking** (P4) - Workflow insights
5. **Write guard** (P5) - Safety improvement
6. **allowed-tools** (P5) - Cleanup
7. **Language setting** (P5) - Accessibility

---

## Notes

- All items are optional enhancements
- Core audit implementation is complete
- These can be implemented incrementally as needed
- Some items (modular rules) have higher risk and should be tested carefully
