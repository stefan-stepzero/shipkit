---
name: shipkit-dev-plan
description: Breaks a framework spec into implementation steps with file ownership, dependencies, and phase gates. Outputs a plan compatible with shipkit-dev-team for parallel execution. Use after running shipkit-dev-spec.
argument-hint: "<feature-name> [--parallel] [--phases N]"
---

# shipkit-dev-plan - Framework Implementation Planner

**Purpose**: Turn a spec into an ordered, parallelizable implementation plan for the Shipkit repo

**What it does**:
- Reads a spec from `.claude/specs/{feature}.json`
- Decomposes into phases with tasks, dependencies, and file ownership
- Identifies what can run in parallel vs must be serial
- Outputs plan to `.claude/plans/{feature}.json`
- Plan is compatible with `/shipkit-dev-team` for team execution

---

## When to Invoke

**User says:**
- "Plan the implementation"
- "Break this into tasks"
- "How should we build this?"
- "Create the plan"

**Automated trigger:**
- After `/shipkit-dev-spec` produces a spec
- Before running `/shipkit-dev-team`

---

## Prerequisites

**Required**:
- `.claude/specs/{feature}.json` exists (run `/shipkit-dev-spec` first)

**Helpful context**:
- `CLAUDE.md` — Framework structure, component locations
- Current git status — what's already in progress

---

## Process

### Step 1: Load Spec

Read `.claude/specs/{feature}.json`. Extract:
- `changeType` — determines planning strategy
- `files.create` / `files.modify` / `files.delete` — the work
- `acceptanceCriteria` — what must pass
- `integrations` — dependency context
- `risks` — what to watch for

### Step 2: Choose Planning Strategy

| Change Type | Strategy |
|-------------|----------|
| `new-skill` | 7-file sequential: SKILL.md first → integration files → validation |
| `new-local-skill` | Simple: write SKILL.md, done |
| `new-agent` | Agent file → manifest → settings |
| `new-hook` | Hook script → settings registration → test |
| `skill-update` | Read current → modify → validate → update integration if needed |
| `refactor` | Phase by component boundary, with gates between |
| `architecture` | Research → design → implement by layer → validate |

### Step 3: Group by File Ownership

For parallel execution, group files into ownership clusters:

```
Cluster A: install/skills/shipkit-{name}/ (all files in this skill)
Cluster B: install/shared/hooks/ (hook files)
Cluster C: install/settings/, install/profiles/ (config files)
Cluster D: docs/generated/, install/claude-md/ (documentation)
Cluster E: install/skills/shipkit-master/ (routing — depends on A)
```

**Rule**: Tasks within a cluster can be done by one teammate. Tasks across clusters can be parallel as long as dependencies allow.

### Step 4: Define Phases and Dependencies

Organize tasks into phases with gates:

**Phase 1 — Core Implementation**:
- Create/modify the primary files (SKILL.md, hook scripts, agent files)
- No dependencies on other phases
- Gate: "Core files exist and are syntactically valid"

**Phase 2 — Integration**:
- Update manifest, settings, routing, overview
- Depends on Phase 1 (needs to know exact names/descriptions)
- Gate: "All 7-file integration points updated"

**Phase 3 — Validation**:
- Run `/shipkit-framework-integrity` (for any change)
- Depends on Phase 2
- Gate: "Zero errors from validation"

**Phase 4 — Documentation** (if needed):
- Update README counts, changelog entries
- Depends on Phase 3 (validation passes first)
- Gate: "Docs match reality"

### Step 5: Define Tasks

For each task:

```json
{
  "id": "1.1",
  "phase": 1,
  "description": "Create SKILL.md for shipkit-{name}",
  "files": {
    "create": ["install/skills/shipkit-{name}/SKILL.md"],
    "modify": []
  },
  "ownershipCluster": "A",
  "dependsOn": [],
  "acceptanceCriteria": ["AC-1", "AC-2"],
  "skills": [],
  "estimatedEffort": "medium"
}
```

### Step 6: Identify Parallel Opportunities

Mark which tasks can run simultaneously:

```
Phase 1:
  Task 1.1 (create SKILL.md)     ─┐
  Task 1.2 (create hook script)   ├─ PARALLEL (different clusters)
  Task 1.3 (create agent file)   ─┘

Phase 2: (depends on all of Phase 1)
  Task 2.1 (update manifest)     ─┐
  Task 2.2 (update settings)      ├─ PARALLEL (independent config files)
  Task 2.3 (update overview.html) ─┘
  Task 2.4 (update master routing) ── SERIAL (depends on 2.1 for exact name)
```

### Step 7: Write Plan

Write `.claude/plans/{feature}.json`:

```json
{
  "$schema": "shipkit-dev-artifact",
  "type": "framework-plan",
  "version": "1.0",
  "createdAt": "2026-02-20T...",
  "source": "shipkit-dev-plan",
  "feature": "{feature-name}",
  "spec": ".claude/specs/{feature}.json",
  "overview": {
    "goal": "From spec",
    "totalTasks": 12,
    "totalPhases": 4,
    "parallelOpportunities": 3,
    "estimatedEffort": "medium"
  },
  "phases": [
    {
      "id": 1,
      "name": "Core Implementation",
      "gate": {
        "description": "Core files exist and pass syntax check",
        "verification": "ls install/skills/shipkit-{name}/SKILL.md"
      },
      "tasks": [
        {
          "id": "1.1",
          "description": "Create SKILL.md",
          "files": {"create": [...], "modify": [...]},
          "ownershipCluster": "A",
          "dependsOn": [],
          "acceptanceCriteria": ["AC-1"],
          "skills": [],
          "effort": "medium",
          "parallelGroup": "P1"
        }
      ]
    }
  ],
  "parallelGroups": {
    "P1": ["1.1", "1.2", "1.3"],
    "P2": ["2.1", "2.2", "2.3"]
  },
  "teamComposition": {
    "recommended": {
      "implementers": 2,
      "reviewers": 1,
      "models": {"implementers": "sonnet", "reviewers": "opus"}
    },
    "solo": "All tasks can be done by one session if preferred"
  }
}
```

### Step 8: Present Summary

```
## Plan: {feature-name}

**Phases**: {N} | **Tasks**: {N} | **Parallel groups**: {N}

### Phase 1: Core Implementation
- 1.1: Create SKILL.md [cluster A]
- 1.2: Create hook script [cluster B] ← parallel with 1.1
- Gate: Files exist and valid

### Phase 2: Integration
- 2.1: Update manifest [cluster C]
- 2.2: Update settings [cluster C]
- Gate: 7-file integration complete

### Phase 3: Validation
- 3.1: Run framework-integrity
- Gate: Zero errors

**Team**: 2 implementers (Sonnet) + 1 reviewer (Opus)
**Solo**: Achievable in one session

Ready to execute? Options:
- `/shipkit-dev-team {feature}` — team execution
- Implement manually in this session
```

---

## Output Quality Checklist

- [ ] Every file from the spec is covered by at least one task
- [ ] Dependencies form a DAG (no cycles)
- [ ] Parallel groups contain only independent tasks
- [ ] Phase gates are concrete and verifiable
- [ ] Acceptance criteria from spec are mapped to tasks
- [ ] Effort estimates are realistic
- [ ] Team composition matches task count and complexity

---

## When This Skill Integrates with Others

### Before This Skill
- `/shipkit-dev-spec` — Provides the spec to plan from
  - **Trigger**: Spec must exist
  - **Why**: Plan implements a spec — can't plan without knowing what

### After This Skill
- `/shipkit-dev-team` — Executes the plan with a team
  - **Trigger**: Plan written and confirmed
  - **Why**: Plan defines work; team executes it
- Manual execution — User implements the plan in the current session

---

## Context Files This Skill Reads

- `.claude/specs/{feature}.json` — Spec to plan from (required)
- `.claude/plans/*.json` — Previous plans (reference)
- `CLAUDE.md` — Framework structure

## Context Files This Skill Writes

- `.claude/plans/{feature}.json` — Implementation plan
