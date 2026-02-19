---
name: shipkit-team
description: Create an agent team from an implementation plan to build features in parallel. Reads plan.json, decomposes tasks by file ownership, spawns implementer and reviewer teammates with quality gates. Use after /shipkit-plan when ready to implement.
argument-hint: "<plan-file-path>"
triggers:
  - create a team
  - team implement
  - implement with a team
  - build this with a team
  - parallel team implementation
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task
---

# shipkit-team

Create an agent team from a Shipkit plan to implement features in parallel with quality gates.

---

## When to Invoke

**User triggers:**
- "Create a team to implement this plan"
- "Build this feature with a team"
- "Team implement [feature]"

**Prerequisites:**
- Plan exists in `.shipkit/plans/todo/{feature}.json` (run `/shipkit-plan` first)
- Spec exists in `.shipkit/specs/todo/{feature}.json` (run `/shipkit-spec` first)
- Agent Teams enabled (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in settings or env)

---

## Process

### Step 1: Select Plan

If no plan path provided as argument:
1. Glob `.shipkit/plans/todo/*.json`
2. If one plan → use it
3. If multiple → list them and ask user to pick
4. If none → tell user to run `/shipkit-plan` first

Read the plan JSON. Extract:
- `plan.phases[]` — the phase structure
- `plan.phases[].tasks[]` — individual tasks with dependencies, files, acceptance criteria
- `plan.phases[].gate` — phase gate conditions
- `plan.overview.goal` — the high-level objective
- `plan.codebasePatterns[]` — patterns teammates must follow
- `plan.specId` — to locate the corresponding spec

Read the spec file for acceptance criteria context.

### Step 2: Derive File Ownership Groups

Group tasks into **ownership clusters** — sets of tasks that share file directories and can be assigned to one teammate.

**Algorithm:**
1. For each task, collect all paths from `files.create` and `files.modify`
2. Extract the top-level directory for each path (e.g., `src/components/auth/` → `src/components/`)
3. Group tasks that share directories into clusters
4. Tasks with no file overlap can be in separate clusters

**Example from auth plan:**
```
Cluster A (Foundation): tasks 1.1, 1.2, 1.3
  → src/types/, src/stores/, src/utils/

Cluster B (UI): tasks 2.1, 2.2, 2.3
  → src/components/auth/, src/pages/auth/

Cluster C (Integration): tasks 3.1, 3.2, 3.3
  → src/components/auth/ProtectedRoute.tsx, src/App.tsx, src/components/Header.tsx
```

**Rules:**
- If a task modifies a file another cluster creates, it must be in the same cluster OR depend on the creating task
- If clusters are too small (1-2 tasks), merge with the closest related cluster
- If a cluster is too large (8+ tasks), split by subdirectory
- Aim for 2-4 clusters for typical features

### Step 3: Build Task List with Dependencies

Convert plan phases/tasks into Agent Teams task list items:

**For each phase:**
1. Create task items from `plan.phases[N].tasks[]`
   - Task description = task.description + task.acceptanceCriteria joined
   - Dependencies = task.dependencies mapped to task list IDs
2. Create a **gate task** from `plan.phases[N].gate`
   - Description: `"GATE: {gate.condition}"`
   - Dependencies: all tasks in the phase
   - Assigned to: lead or reviewer
3. All tasks in phase N+1 depend on phase N's gate task

**Dependency mapping:**
```
Plan task 1.1 (no deps)          → Team task "1.1" (no deps)
Plan task 1.2 (deps: [1.1])     → Team task "1.2" (deps: ["1.1"])
Plan gate 1                      → Team task "GATE-1" (deps: ["1.1", "1.2", "1.3"])
Plan task 2.1 (deps: [1.2])     → Team task "2.1" (deps: ["GATE-1"])
```

### Step 4: Determine Team Composition

**Lead (you, the current session):**
- Coordinates work, monitors progress
- Verifies gate tasks
- Runs `/shipkit-verify` and `/shipkit-preflight` after all tasks complete
- Does NOT implement — only coordinates

**Implementer teammates:**
- One per ownership cluster from Step 2
- Model: Sonnet (cost-effective for implementation)
- Each owns a specific set of files — NO overlap between teammates

**Reviewer teammate:**
- One reviewer for the entire team
- Model: Opus (needs deep reasoning for review quality)
- Read-only: validates completed tasks against spec acceptance criteria
- Reports issues to implementers directly via messaging

**Team size guidance:**
| Plan complexity | Implementers | Reviewer | Total |
|----------------|-------------|----------|-------|
| 1-3 tasks | 1 | 0 (lead reviews) | 1 |
| 4-9 tasks | 2 | 1 | 3 |
| 10-15 tasks | 3 | 1 | 4 |
| 16+ tasks | 4 | 1 | 5 |

### Step 5: Write Team State File

Before creating the team, write `.shipkit/team-state.local.json`:

```json
{
  "planPath": ".shipkit/plans/todo/{feature}.json",
  "specPath": ".shipkit/specs/todo/{feature}.json",
  "created": "ISO timestamp",
  "clusters": [
    {
      "name": "cluster-name",
      "teammate": "implementer-1",
      "taskIds": ["1.1", "1.2", "1.3"],
      "ownedPaths": ["src/types/", "src/stores/", "src/utils/"]
    }
  ],
  "gateTasks": ["GATE-1", "GATE-2", "GATE-3"]
}
```

This file is read by the `TaskCompleted` and `TeammateIdle` hooks for validation.

### Step 6: Create the Team

Now instruct Claude to create the agent team. Use this structure:

```
Create an agent team to implement: {plan.overview.goal}

## Shared Context
- Plan: {planPath} (read this for task details and acceptance criteria)
- Spec: {specPath} (read this for feature requirements)
- Stack: .shipkit/stack.json (read this for project patterns)
- Architecture: .shipkit/architecture.json (read this for design decisions)

## Teammates

### implementer-1 (Sonnet)
Owns: {cluster A owned paths}
Tasks: {cluster A task descriptions with acceptance criteria}
Instructions:
- Read the plan file for full task details
- Follow codebase patterns from stack.json
- Use /shipkit-build-relentlessly after implementing each task
- Use /shipkit-test-relentlessly to verify tests pass
- Do NOT edit files outside your owned paths
- Message the reviewer when a task is ready for review

### implementer-2 (Sonnet)
Owns: {cluster B owned paths}
Tasks: {cluster B task descriptions with acceptance criteria}
Instructions: [same as above with cluster B paths]

### reviewer (Opus)
Role: Quality validation — do NOT write code
Instructions:
- Read the spec for acceptance criteria
- When an implementer messages you about a completed task:
  1. Read the changed files
  2. Verify against acceptance criteria from the spec
  3. Check for security issues, error handling, edge cases
  4. If issues found → message the implementer directly with specifics
  5. If approved → report to lead
- Use /shipkit-verify on the full changeset when all implementation tasks are done

## Task List
{Generated task list with dependencies from Step 3}

## Rules
- Implementers: do NOT touch files outside your owned paths
- Reviewer: do NOT edit any files — read-only analysis
- Lead: do NOT implement — coordinate only
- When all tasks complete, lead runs /shipkit-verify then /shipkit-preflight

## Phase Gates
{For each gate: condition and verification method}
Lead verifies each gate before unblocking next phase.
```

### Step 7: Monitor and Complete

After team creation:
1. Teammates self-claim tasks and begin working
2. `TaskCompleted` hook validates build+test on each task
3. `TeammateIdle` hook keeps teammates working until all tasks done
4. Lead verifies phase gates between phases
5. When all tasks complete:
   - Ask reviewer to shut down
   - Ask implementers to shut down
   - Run `/shipkit-verify` on full changeset
   - Run `/shipkit-preflight` for production readiness
   - Clean up the team
   - Report results to user

---

## Context Files

**Reads:**
- `.shipkit/plans/todo/{feature}.json` — plan structure
- `.shipkit/specs/todo/{feature}.json` — acceptance criteria
- `.shipkit/stack.json` — project patterns
- `.shipkit/architecture.json` — design decisions

**Writes:**
- `.shipkit/team-state.local.json` — team configuration for hooks

**Cleanup:**
- Delete `.shipkit/team-state.local.json` after team cleanup

---

## When This Skill Integrates with Others

### Before This Skill
- `/shipkit-spec` — Feature specification (required)
- `/shipkit-plan` — Implementation plan (required)
- `/shipkit-project-context` — Stack detection (recommended)

### During Team Execution
- `/shipkit-build-relentlessly` — Used by implementer teammates
- `/shipkit-test-relentlessly` — Used by implementer teammates
- `/shipkit-verify` — Used by reviewer and lead

### After This Skill
- `/shipkit-preflight` — Production readiness audit
- `/shipkit-work-memory` — Log the team execution

---

## Error Handling

**No plan found:**
- Tell user to run `/shipkit-plan` first

**Agent Teams not enabled:**
- Tell user to add `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` to settings.json env

**Teammate gets stuck:**
- Message them directly with more context
- If unrecoverable, shut down and spawn replacement

**File conflict between teammates:**
- Stop both teammates
- Reassign the conflicting file to one owner
- Resume

**All tasks done but gate fails:**
- Create new tasks to fix the gate failure
- Assign to appropriate implementer

---

## Constraints

- Requires Agent Teams experimental feature enabled
- One team per session (Claude Code limitation)
- No nested teams — teammates cannot create sub-teams
- Lead session is fixed for team lifetime
- Teammates cannot be resumed after session ends
