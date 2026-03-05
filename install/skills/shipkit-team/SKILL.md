---
name: shipkit-team
id: SKL-TEAM
description: Execute a spec+plan with a coordinated agent team. Decomposes plan tasks by file ownership, spawns implementer and reviewer teammates. Reviewer validates against spec acceptance criteria and gates quality. Use when ready to implement a planned feature with parallel execution.
argument-hint: "<plan-name-or-path>"
context: fork
agent: shipkit-implementer-agent
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Skill
---

# shipkit-team

Execute a spec+plan pair with a coordinated Agent Team — implementers build in parallel, a reviewer validates against spec criteria, and the lead manages phase gates.

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

**When NOT to use — use `/batch` instead:**
- Clusters are fully independent with zero file overlap
- Work is mechanical (migrations, renames, repetitive changes)
- You want one PR per unit of work

`/shipkit-team` is for coordinated implementation where teammates share a workspace, a reviewer validates quality, and phase gates control flow.

---

## Arguments

If `$ARGUMENTS` is provided (e.g. `/shipkit-team recipe-sharing`), use it as the plan name or path. Try:
1. `$ARGUMENTS` directly (if it contains `/`)
2. `.shipkit/plans/todo/$ARGUMENTS.json`
3. `.shipkit/plans/active/$ARGUMENTS.json`

If found, skip plan selection and proceed to Step 2. If not found, fall back to listing available plans.

---

## Process

### Step 1: Select Plan and Load Context

If no plan path provided as argument:
1. Glob `.shipkit/plans/todo/*.json`
2. If one plan → use it
3. If multiple → list them and ask user to pick
4. If none → tell user to run `/shipkit-plan` first

Read the plan JSON. Extract:
- `plan.phases[]` — phase structure
- `plan.phases[].tasks[]` — tasks with dependencies, files, acceptance criteria
- `plan.phases[].gate` — phase gate conditions
- `plan.overview.goal` — high-level objective
- `plan.codebasePatterns[]` — patterns teammates must follow
- `plan.specId` — to locate the corresponding spec

Read the spec file for acceptance criteria.

Also read (if they exist):
- `.shipkit/stack.json` — project patterns and tech stack
- `.shipkit/architecture.json` — architecture decisions

### Step 2: Create Feature Branch

Create an isolated branch for the team's work:

```bash
git checkout -b impl/{feature-slug}
```

This ensures team work is isolated from the main branch. If the team fails midway, the branch can be reset or deleted cleanly. On success, the branch becomes a PR.

### Step 3: Derive File Ownership Clusters

Group tasks into **ownership clusters** — sets of tasks that share file directories, assigned to one implementer teammate.

**Algorithm:**
1. For each task, collect all paths from `files.create` and `files.modify`
2. Extract the top-level directory for each path (e.g., `src/components/auth/` → `src/components/`)
3. Group tasks that share directories into clusters
4. Tasks with no file overlap can be in separate clusters

**Rules:**
- If a task modifies a file another cluster creates → same cluster OR explicit dependency
- Clusters with 1-2 tasks → merge with closest related cluster
- Clusters with 8+ tasks → split by subdirectory
- Aim for 2-4 clusters

### Step 4: Build Task List with Dependencies

Convert plan phases/tasks into Agent Teams task items:

**For each phase:**
1. Create task items from `plan.phases[N].tasks[]`
   - Description = task.description + task.acceptanceCriteria
   - Dependencies = task.dependencies mapped to task list IDs
2. Create a **gate task** from `plan.phases[N].gate`
   - Description: `"GATE: {gate.condition}"`
   - Dependencies: all tasks in the phase
   - Assigned to: reviewer
3. All tasks in phase N+1 depend on phase N's gate task

**Dependency mapping:**
```
Plan task 1.1 (no deps)       → Task "1.1" (no deps)
Plan task 1.2 (deps: [1.1])  → Task "1.2" (deps: ["1.1"])
Plan gate 1                   → Task "GATE-1" (deps: ["1.1", "1.2", "1.3"])
Plan task 2.1 (deps: [1.2])  → Task "2.1" (deps: ["GATE-1"])
```

### Step 5: Write Team State

Write `.shipkit/team-state.local.json` before creating the team:

```json
{
  "planPath": ".shipkit/plans/todo/{feature}.json",
  "specPath": ".shipkit/specs/todo/{feature}.json",
  "branch": "impl/{feature-slug}",
  "created": "ISO timestamp",
  "clusters": [
    {
      "name": "cluster-name",
      "teammate": "implementer-1",
      "taskIds": ["1.1", "1.2", "1.3"],
      "ownedPaths": ["src/types/", "src/stores/"]
    }
  ],
  "gateTasks": ["GATE-1", "GATE-2"]
}
```

This file is read by the `TaskCompleted` and `TeammateIdle` hooks for validation.

### Step 6: Create the Team

**Team roles:**

| Role | Count | Model | Purpose |
|------|-------|-------|---------|
| Lead (you) | 1 | Current | Coordinates, manages phase gates, final verification |
| Implementers | 1 per cluster | Sonnet | Implements tasks, owns specific files |
| Reviewer | 1 | Sonnet | Validates against spec, gates quality, has `/shipkit-verify` |

**Team size guidance:**

| Plan complexity | Implementers | Reviewer | Total |
|----------------|-------------|----------|-------|
| 1-3 tasks | 1 | 0 (lead reviews) | 1 |
| 4-9 tasks | 2 | 1 | 3 |
| 10-15 tasks | 3 | 1 | 4 |
| 16+ tasks | 4 | 1 | 5 |

**Create the team with this structure:**

```
Create an agent team to implement: {plan.overview.goal}

## Shared Context
- Plan: {planPath}
- Spec: {specPath}
- Stack: .shipkit/stack.json
- Architecture: .shipkit/architecture.json

## Teammates

### implementer-1 (Sonnet)
Owns: {cluster A owned paths}
Tasks: {cluster A task IDs and descriptions}
Instructions:
- Implement your assigned tasks in dependency order
- Build after each task — fix compile errors before moving on
- Run tests — fix failures before moving on
- Do NOT edit files outside your owned paths
- Message the reviewer when tasks are ready for review
- If reviewer requests changes, fix them and re-notify

### implementer-2 (Sonnet)
Owns: {cluster B owned paths}
Tasks: {cluster B task IDs and descriptions}
Instructions: [same pattern with cluster B context]

### reviewer (Sonnet)
Skills: /shipkit-verify
Role: Quality gatekeeper — validate, do NOT write code
Instructions:
- Read the spec for acceptance criteria
- When an implementer notifies you of completed work:
  1. Read the changed files
  2. Verify against spec acceptance criteria
  3. Check for correctness, security issues, edge cases
  4. If issues → message the implementer with specifics
  5. If approved → mark the corresponding gate task as complete
- When all implementation tasks are done, run /shipkit-verify on the full changeset
- Report final verification result to the lead

## Task List
{Generated task list with dependencies from Step 4}

## Rules
- Implementers: stay within your owned paths
- Reviewer: read-only — never edit files
- Lead: coordinate only — never implement
- Gate tasks are owned by the reviewer
```

### Step 7: Monitor and Complete

After team creation:

1. Implementers self-claim tasks and begin working
2. Implementers build and test after each task (inline instructions)
3. Implementers notify reviewer when ready
4. Reviewer validates, ping-pongs fixes with implementers if needed
5. Reviewer marks gate tasks complete when satisfied
6. Lead watches gate tasks — unblocks next phase when gate completes
7. `TaskCompleted` hook validates build+test on each task completion
8. `TeammateIdle` hook keeps teammates working until all tasks done

**When all tasks and gates complete:**
- Lead runs `/shipkit-verify` on full changeset (final check)
- Lead runs `/shipkit-preflight` for production readiness
- Report results to user

### Step 8: Cleanup

After team completion (success or failure):

1. **Shut down teammates**
2. **Delete team state** — remove `.shipkit/team-state.local.json`
3. **Move plan** — `todo/` → `shipped/` (or `parked/` if incomplete)
4. **Create PR** — `gh pr create --base {original-branch} --title "{feature}: {summary}"`
5. **Report summary:**
   ```
   ## Team Complete: {feature}
   - Branch: impl/{feature-slug}
   - Tasks: {completed}/{total}
   - Verify: {PASS/FAIL}
   - Preflight: {PASS/FAIL}
   - PR: {url}
   ```

**If team failed or was cancelled:**
- Still delete `.shipkit/team-state.local.json` (prevents hook interference)
- Plan stays in `todo/` for retry
- Branch preserved for manual recovery

---

## Context Files

**Reads:**
- `.shipkit/plans/todo/{feature}.json` — plan structure
- `.shipkit/specs/todo/{feature}.json` — acceptance criteria
- `.shipkit/stack.json` — project patterns
- `.shipkit/architecture.json` — design decisions

**Writes:**
- `.shipkit/team-state.local.json` — team state for hooks (deleted after cleanup)

---

## When This Skill Integrates with Others

### Before This Skill
- `/shipkit-spec` — Feature specification (required)
- `/shipkit-plan` — Implementation plan (required)
- `/shipkit-project-context` — Stack detection (recommended)

### After This Skill
- `/shipkit-work-memory` — Log the team execution
- `/shipkit-communications` — Stakeholder report

---

## Error Handling

| Problem | Action |
|---------|--------|
| No plan found | Tell user to run `/shipkit-plan` first |
| Agent Teams not enabled | Tell user to set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` |
| Teammate gets stuck | Message them with more context; if unrecoverable, shut down and spawn replacement |
| File conflict between teammates | Stop both, reassign conflicting file to one owner, resume |
| Gate fails after all tasks done | Create fix tasks, assign to appropriate implementer |

---

<!-- SECTION:success-criteria -->
## Success Criteria

- [ ] Plan read and tasks decomposed into ownership clusters
- [ ] Feature branch created (`impl/{feature}`)
- [ ] Team state file written
- [ ] Agent Team created with implementers + reviewer
- [ ] Reviewer validated all work against spec acceptance criteria
- [ ] All gate tasks completed
- [ ] `/shipkit-verify` passed on full changeset
- [ ] `/shipkit-preflight` passed
- [ ] PR created from feature branch
- [ ] Team cleaned up, state file deleted
<!-- /SECTION:success-criteria -->

---

<!-- SECTION:after-completion -->
## After Completion

**Team succeeded:** PR created with all tasks complete, verify + preflight passed. Review and merge the PR.

**Team partially completed:** Branch preserved with partial work. Check task list status, restart team or finish manually.

**Next steps:**
- Review and merge the PR
- `/shipkit-work-memory` — Log the execution for session continuity
<!-- /SECTION:after-completion -->

---

## Constraints

- Requires Agent Teams experimental feature enabled
- One team per session (Claude Code limitation)
- No nested teams — teammates cannot create sub-teams
- Lead session is fixed for team lifetime
- Teammates cannot be resumed after session ends
