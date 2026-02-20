---
name: shipkit-dev-team
description: Orchestrates Shipkit framework development using Agent Teams. Creates coordinated teams from dev plans for parallel implementation, review, and release. Use when a framework change is big enough for team execution.
argument-hint: "<feature-name> [--template skill|refactor|review|release|self-improve]"
---

# shipkit-dev-team - Framework Development Team Orchestrator

**Purpose**: Coordinate parallel framework development using Agent Teams

**What it does**:
- Reads a plan from `.claude/plans/{feature}.json`
- Creates a coordinated team tailored to framework development
- Assigns tasks with file ownership boundaries
- Sets up quality gates using local dev skills
- Monitors progress and handles phase transitions

---

## When to Invoke

**User says:**
- "Team build this"
- "Create a dev team"
- "Parallel implement the plan"
- "Run the self-improvement team"
- "Team review this"

**Automated trigger:**
- After `/shipkit-dev-plan` produces a plan
- When the plan has 3+ parallel tasks (otherwise solo is fine)

---

## Prerequisites

**Required**:
- Agent Teams enabled: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`
- A plan at `.claude/plans/{feature}.json` (unless using a built-in template)

**Helpful context**:
- `.claude/specs/{feature}.json` — spec for the feature
- `CLAUDE.md` — framework rules
- Current git branch and status

---

## Team Templates

### Template: `skill` — New Skill Development

**When**: Building a new distributed skill (7-file integration).

**Team**:
| Role | Model | Responsibilities |
|------|-------|-----------------|
| **Lead** (you) | — | Coordinate, approve gates, run validation |
| **Implementer A** | Sonnet | Write SKILL.md + references |
| **Implementer B** | Sonnet | Update integration files (manifest, settings, routing, overview) |
| **Reviewer** | Opus | Validate against spec, check Skill Value Test, design quality |

**File ownership**:
- A: `install/skills/shipkit-{name}/`
- B: `install/settings/`, `install/profiles/`, `install/skills/shipkit-master/`, `docs/generated/`, `install/claude-md/`
- Reviewer: read-only everywhere

**Phase flow**:
1. A writes SKILL.md → Gate: file exists, frontmatter valid
2. B updates integration files → Gate: 7-file checklist passes
3. Reviewer validates → Gate: review verdict PASS
4. Lead runs `/shipkit-framework-integrity`

---

### Template: `refactor` — Multi-File Refactor

**When**: Structural changes across multiple framework components.

**Team**:
| Role | Model | Responsibilities |
|------|-------|-----------------|
| **Lead** (you) | — | Coordinate, resolve conflicts |
| **Implementer per cluster** | Sonnet | Own a file cluster (skills, agents, hooks, config) |
| **Reviewer** | Opus | Check nothing breaks, pattern consistency |

**File ownership**: Derived from plan's ownership clusters.

---

### Template: `review` — Multi-Lens Review

**When**: Thorough review of framework changes from multiple perspectives.

**Team**:
| Role | Model | Responsibilities |
|------|-------|-----------------|
| **Lead** (you) | — | Synthesize findings |
| **Design Reviewer** | Opus | Skill Value Test, scope discipline, pattern consistency |
| **Compatibility Reviewer** | Sonnet | CC compatibility, deprecated patterns, frontmatter validity |
| **Integration Reviewer** | Sonnet | 7-file integration, cross-references, manifest sync |

**All reviewers are read-only.**

---

### Template: `release` — Release Pipeline

**When**: Preparing a new Shipkit version.

**Team**:
| Role | Model | Responsibilities |
|------|-------|-----------------|
| **Lead** (you) | — | Version bump, changelog, final push |
| **Validator** | Sonnet | Run framework-integrity, validate changed skills |
| **Auditor** | Sonnet | Secrets scan, installer check, count audit |

---

### Template: `self-improve` — Shipkit Self-Improvement

**When**: Running the full intelligence → implementation cycle.

**Team**:
| Role | Model | Responsibilities |
|------|-------|-----------------|
| **Lead** (you) | — | Coordinate pipeline, approve specs/plans |
| **Scout** | Haiku | Run `/shipkit-scout` → scout-report.json |
| **Analyst** | Sonnet | Run `/shipkit-analyst` → analyst-report.json |
| **Ideator** | Sonnet | Run `/shipkit-ideator` → opportunities.json |

**Phase flow**:
1. Scout fetches CC docs and changelog → Gate: scout-report.json written
2. Analyst maps against Shipkit → Gate: analyst-report.json written
3. Ideator brainstorms → Gate: opportunities.json written
4. Lead presents top opportunities to user for selection
5. (Optional) Lead runs `/shipkit-dev-spec` + `/shipkit-dev-plan` for selected opportunity
6. (Optional) Spawn implementation team from plan

**Note**: Phases 1-3 are serial (each reads previous output). Phase 5-6 can reuse the `skill` or `refactor` template.

---

## Process

### Step 1: Select Template or Load Plan

If `--template` specified, use the corresponding template above.

Otherwise, read `.claude/plans/{feature}.json`:
- Extract phases, tasks, ownership clusters, parallel groups
- Determine team size from task count and cluster count

### Step 2: Write Team State

Create `.claude/team-state.local.json`:

```json
{
  "feature": "{feature-name}",
  "template": "skill|refactor|review|release|self-improve",
  "planPath": ".claude/plans/{feature}.json",
  "specPath": ".claude/specs/{feature}.json",
  "createdAt": "2026-02-20T...",
  "teammates": {
    "implementer-a": {"cluster": "A", "tasks": ["1.1", "1.2"]},
    "implementer-b": {"cluster": "B", "tasks": ["2.1", "2.2"]},
    "reviewer": {"cluster": "readonly", "tasks": ["3.1"]}
  },
  "phases": [
    {"id": 1, "status": "in_progress", "gate": "..."},
    {"id": 2, "status": "pending", "gate": "..."}
  ]
}
```

### Step 3: Create Spawn Prompts

For each teammate, build a prompt that includes:

```markdown
# You are {role} on the Shipkit framework development team

## Your Assignment
{tasks from plan, with specific file paths}

## File Ownership
You own: {list of file paths/directories}
DO NOT modify files outside your ownership boundary.

## Context
- Read CLAUDE.md for framework rules
- Read .claude/specs/{feature}.json for requirements
- Read .claude/plans/{feature}.json for the full plan

## Skills Available
{relevant local dev skills for this role}

## Quality Requirements
- All acceptance criteria from spec must be met
- Your changes must pass validation
- Report completion to lead when done

## Communication
- Message lead when you hit a blocker
- Message reviewer when ready for review
- Broadcast to team if you discover a shared concern
```

### Step 4: Create the Team

Use Claude Code's team creation capabilities:
- Create team with name: `shipkit-{feature}-{date}`
- Create shared task list derived from plan
- Set task dependencies from plan
- Spawn teammates with their prompts
- Assign tasks to teammates

### Step 5: Monitor and Gate

As lead:

1. **Watch task completions** — `TaskCompleted` hook validates build/test
2. **Verify phase gates** — When all tasks in a phase complete, verify the gate condition
3. **Unblock next phase** — Mark gate task complete to unblock dependent tasks
4. **Handle blockers** — If a teammate reports a blocker, help resolve or reassign

### Step 6: Finalize

When all tasks complete:

1. Run `/shipkit-dev-review --scope recent`
2. If review passes, ask user if they want to release
3. If yes, run `/shipkit-dev-release`

---

## When This Skill Integrates with Others

### Before This Skill
- `/shipkit-dev-plan` — Produces the plan this skill executes
  - **Trigger**: Plan must exist (unless using built-in template)
- `/shipkit-dev-spec` — Produces the spec the plan implements

### After This Skill
- `/shipkit-dev-review` — Review completed team work
- `/shipkit-dev-release` — Release if review passes

### During Execution (by teammates)
- `/shipkit-framework-integrity` — Validation during and after implementation
- `/shipkit-scout`, `/shipkit-analyst`, `/shipkit-ideator` — Self-improvement template

---

## Context Files This Skill Reads

- `.claude/plans/{feature}.json` — Implementation plan (required unless template)
- `.claude/specs/{feature}.json` — Feature spec
- `CLAUDE.md` — Framework rules
- `.claude/team-state.local.json` — Previous team state (if resuming)

## Context Files This Skill Writes

- `.claude/team-state.local.json` — Active team state (for hooks)
