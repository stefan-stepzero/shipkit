---
name: lite-milestone-detector
description: Hidden coordinator skill that detects which workflow milestone was just completed (spec, plan, implement, pre-ship) and routes to appropriate detection skill to create bug-prevention queues. Auto-triggered by SessionStop hook. System skill - not user-invocable.
---

# lite-milestone-detector - Milestone Coordinator

**Purpose**: Detect which workflow milestone just completed and route to the appropriate detection skill to create bug-prevention queues.

**Type**: System skill (hidden from users, auto-triggered)

**Trigger**: SessionStop hook (after any skill completes)

---

## What This Skill Does

**Detection:**
1. Checks file modification times in `.shipkit-lite/`
2. Determines which skill just completed:
   - Spec created → Route to lite-post-spec-check
   - Plan created → Route to lite-post-plan-check
   - Implementation done → Route to lite-post-implement-check
   - Quality check starting → Route to lite-pre-ship-check
3. Invokes appropriate detection skill

**Routing Logic:**
```python
if spec_just_created():
    invoke('lite-post-spec-check')
elif plan_just_created():
    invoke('lite-post-plan-check')
elif implementation_just_done():
    invoke('lite-post-implement-check')
elif quality_check_about_to_run():
    invoke('lite-pre-ship-check')
else:
    # No milestone detected, exit silently
    pass
```

**Output:**
- Detection skill runs and creates queue files
- lite-whats-next will suggest next actions based on queues

---

## Detection Algorithm

**Check modification times:**

```python
from pathlib import Path
from datetime import datetime, timedelta

def detect_milestone():
    """Detect which milestone just occurred"""
    now = datetime.now()
    recent = timedelta(minutes=2)  # Files modified in last 2 minutes

    # Check for new spec
    specs = Path('.shipkit-lite/specs/active').glob('*.md')
    for spec in specs:
        mtime = datetime.fromtimestamp(spec.stat().st_mtime)
        if now - mtime < recent:
            return 'post-spec'

    # Check for new plan
    plans = Path('.shipkit-lite/plans').glob('*.md')
    for plan in plans:
        mtime = datetime.fromtimestamp(plan.stat().st_mtime)
        if now - mtime < recent:
            return 'post-plan'

    # Check for implementation (modified source files)
    src_patterns = ['src/**/*.ts', 'src/**/*.tsx', 'src/**/*.js']
    for pattern in src_patterns:
        for file in Path('.').glob(pattern):
            mtime = datetime.fromtimestamp(file.stat().st_mtime)
            if now - mtime < recent:
                return 'post-implement'

    return None
```

---

## Routing Table

| Detected Milestone | Detection Skill | Queue Created |
|-------------------|-----------------|---------------|
| `post-spec` | lite-post-spec-check | fetch-integration-docs.md |
| `post-plan` | lite-post-plan-check | define-data-contracts.md |
| `post-implement` | lite-post-implement-check | components-to-document.md, routes-to-document.md |
| `pre-ship` | lite-pre-ship-check | ux-audit-needed.md |

---

## Script Location

**Coordinator script:** `scripts/route-to-check.py`

**Invocation:**
```bash
python .claude/skills/lite-milestone-detector/scripts/route-to-check.py
```

**Returns:**
- Exit 0: Success (detection skill invoked or no milestone detected)
- Exit 1: Error

---

## Integration with SessionStop Hook

**settings.json configuration:**
```json
{
  "hooks": {
    "SessionStop": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "python -X utf8 .claude/skills/lite-milestone-detector/scripts/route-to-check.py"
          }
        ]
      }
    ]
  }
}
```

**When it runs:**
- After EVERY message/skill completion
- Checks if a milestone was reached
- Routes to detection skill only if milestone detected
- Otherwise exits silently (no overhead)

---

## When This Skill Integrates with Others

### Before This Skill

**All user-facing skills** - Any skill that creates specs, plans, or implementation
- **When**: Skill completes, SessionStop hook fires
- **Why**: Need to detect what milestone was reached
- **Trigger**: SessionStop hook after skill completion

### After This Skill

**Detection skills** - Routes to appropriate detection skill
- lite-post-spec-check
- lite-post-plan-check
- lite-post-implement-check
- lite-pre-ship-check

**lite-whats-next** - Reads queues created by detection skills
- **When**: After detection skills create queues
- **Why**: Suggests next preventative action based on queue contents
- **Trigger**: User asks "what's next?" or explicit invocation

---

## Context Files This Skill Reads

**Checks modification times:**
- `.shipkit-lite/specs/active/*.md`
- `.shipkit-lite/plans/*.md`
- `src/**/*.ts`, `src/**/*.tsx`, `src/**/*.js`

**Does not read file contents** - Only timestamps to detect recent changes

---

## Context Files This Skill Writes

**Writes:** None (coordinator only, delegates to detection skills)

---

## Success Criteria

Coordination is successful when:
- [ ] Milestone detected correctly
- [ ] Appropriate detection skill invoked
- [ ] Detection skill runs successfully
- [ ] Queue files created (if applicable)
- [ ] No errors or crashes

---

## Edge Cases

**Multiple milestones in one session:**
- Prioritize most recent milestone
- Spec + Plan in 2 minutes → Route to post-plan only

**No milestone detected:**
- Exit silently (exit code 0)
- No output to terminal (avoid noise)

**Detection skill fails:**
- Log error but don't crash
- Return exit code 1 to signal issue

**SessionStop fires too frequently:**
- Only detect if files modified in last 2 minutes
- Avoid re-detecting same milestone

---

## Performance Considerations

**Lightweight detection:**
- Only checks file modification times (no content parsing)
- Globs limited to specific patterns
- Exits quickly if no milestone detected

**Expected overhead:**
- ~50-100ms per SessionStop invocation
- Only runs Python detection if milestone found

---

**Remember**: This is the glue that connects workflow milestones to automatic bug prevention. Users never see it, but it ensures detection skills run at the right time.
