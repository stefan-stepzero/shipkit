---
name: shipkit-dev-team-status
description: Shows current Agent Team status — active teammates, task progress, phase gates, and blockers. Reads team-state file and task list to produce a progress dashboard. Use during team execution to monitor progress.
argument-hint: "[--verbose]"
---

# shipkit-dev-team-status - Team Progress Dashboard

**Purpose**: Quick visibility into team progress during Agent Teams execution

**What it does**:
- Reads `.shipkit/team-state.local.json` (distributed) or `.claude/team-state.local.json` (dev)
- Reads the plan file referenced in team state
- Counts completed vs pending vs in-progress tasks
- Shows phase gate status
- Identifies blockers

---

## When to Invoke

**User says:**
- "Team status"
- "How's the team doing?"
- "What's the progress?"
- "Show team dashboard"

---

## Process

### Step 1: Find Team State

Check for active team state:
1. `.shipkit/team-state.local.json` — distributed team (from `/shipkit-team`)
2. `.claude/team-state.local.json` — dev team (from `/shipkit-dev-team`)

If neither exists: "No active team found. Start one with `/shipkit-team` or `/shipkit-dev-team`."

### Step 2: Read Plan

From team state, read `planPath` to load the plan. Count tasks by status.

### Step 3: Present Dashboard

```
## Team Status: {feature-name}

**Started**: {created timestamp}
**Template**: {template name}

### Progress
██████████░░░░░░░░░░ 50% (6/12 tasks)

### Phases
| Phase | Status | Tasks | Gate |
|-------|--------|-------|------|
| 1. Foundation | ✓ Complete | 3/3 | npm run dev starts |
| 2. UI Components | ◐ In Progress | 2/4 | Login form renders |
| 3. Integration | ○ Blocked | 0/3 | Waiting on Phase 2 |
| 4. Polish | ○ Pending | 0/2 | Tests pass |

### Teammates
| Name | Role | Tasks Done | Status |
|------|------|-----------|--------|
| implementer-1 | Cluster A (types, stores) | 3/4 | Working on 2.1 |
| implementer-2 | Cluster B (components) | 2/3 | Waiting for GATE-1 |
| reviewer | Quality validation | 1/2 | Reviewing 1.3 |

### Blockers
- None currently

### Next Gate
Phase 2 gate: "Login form renders at /login"
Remaining tasks: 2.3, 2.4
```

### Step 4: Suggest Actions

Based on status:
- **All tasks done**: "Ready for `/shipkit-verify` + `/shipkit-preflight`"
- **Blockers exist**: "Message {teammate} about {blocker}"
- **Phase gate ready**: "Verify gate: {condition}"
- **Stalled**: "Check if teammates need help — message them directly"

---

## Context Files This Skill Reads

- `.shipkit/team-state.local.json` or `.claude/team-state.local.json` — Team configuration
- Plan file referenced in team state — Task status and phases

## Context Files This Skill Writes

- None — read-only status view
