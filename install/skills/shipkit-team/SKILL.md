---
name: shipkit-team
description: Create an agent team from an implementation plan to build features in parallel. Reads plan.json, decomposes tasks by file ownership, spawns implementer and reviewer teammates with quality gates. Use when ready to implement a plan with parallel team execution.
argument-hint: "<plan-file-path>"
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

## Arguments

If `$ARGUMENTS` is provided (e.g. `/shipkit-team recipe-sharing`), use it as the plan name or path. Try to read:
1. `$ARGUMENTS` directly (if it contains `/`)
2. `.shipkit/plans/todo/$ARGUMENTS.json`
3. `.shipkit/plans/active/$ARGUMENTS.json`

If found, skip plan selection and proceed to Step 2. If not found, fall back to listing available plans.

If `$ARGUMENTS` is empty, proceed normally from Step 1.

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
   - Run `/shipkit-verify` on full changeset
   - Run `/shipkit-preflight` for production readiness
   - Report results to user

### Step 8: Team Cleanup

After team completion (success or failure):
1. **Shut down teammates** — ask each teammate to stop
2. **Delete team state** — remove `.shipkit/team-state.local.json` so hooks deactivate
3. **Move plan** — move plan from `todo/` to `shipped/` (or `parked/` if incomplete)
4. **Log results** — optionally run `/shipkit-work-memory` to record team execution
5. **Report summary**:
   ```
   ## Team Complete: {feature}
   - Tasks: {completed}/{total}
   - Duration: {time}
   - Verify: {PASS/FAIL}
   - Preflight: {PASS/FAIL}
   - Files changed: {count}
   ```

**If team failed or was cancelled:**
- Still delete `.shipkit/team-state.local.json` (prevents hook interference in future sessions)
- Note incomplete tasks in the summary
- Plan stays in `todo/` for retry

---

## Pipeline Template

**Trigger**: `/shipkit-team --template pipeline "Build a [product description]"`

The pipeline template orchestrates the full product development lifecycle — from a single user goal through discovery, definition, specification, architecture, planning, implementation, and verification.

### Pipeline Arguments

- `$ARGUMENTS` must contain `--template pipeline` to activate
- Everything after `--template pipeline` is the **product goal** (e.g., "Build a learning app with spaced repetition")
- `--yolo` flag: auto-confirm all artifact gates (autonomous mode)
- Without `--yolo`: pause at each phase gate for user confirmation (default)

### Pipeline Phases

```
Phase 1: Discovery ──────→ Phase 2: Solution Design ─────→ Phase 3: Specification
    │                            │                              │
    ▼                            ▼                              ▼
why.json                  product-definition.json          specs/*.json
product-discovery.json    (solution blueprint:             (one per feature,
stack.json (parallel)      mechanisms, patterns,            batch from product-def)
                           differentiators, MVP)
                          goals.json
                          (success criteria +
                           stage gates)
                                │
                          Phase 4: Architecture ──→ Phase 5: Planning
                               │                        │
                               ▼                        ▼
                          architecture.json         plans/*.json
                          (solution architect)      (one per spec)
                                                        │
                               Phase 6: Implementation + Verification
                                   │
                                   ▼
                               Code + tests + verify + preflight
```

### Phase Details

#### Phase 1: Discovery
- **Agent**: Product Owner (Sonnet)
- **Skills**: `/shipkit-why-project`, `/shipkit-product-discovery` (sequential); `/shipkit-project-context` (parallel if codebase exists)
- **Gate**: `why.json` + `product-discovery.json` written and confirmed
- **Notes**: Vision first — why-project has no dependencies, discovery flows from it. Sequential: why → discovery (personas, user needs, journeys). `project-context` runs in parallel because it reads the codebase (not vision artifacts). For greenfield projects with no code yet, `project-context` may produce minimal output and can re-run after scaffolding. The product goal from `$ARGUMENTS` is passed as context to each skill.

#### Phase 2: Solution Design
- **Agent**: Product Owner (Sonnet)
- **Skills**: `/shipkit-product-definition`, `/shipkit-goals` (sequential)
- **Gate**: `product-definition.json` + `goals.json` written and confirmed — solution blueprint with success criteria
- **Notes**: **KEY GATE** — This is where the solution design is confirmed. Product definition creates the solution blueprint (mechanisms, UX patterns, differentiators, MVP boundary). Goals derives measurable success criteria from the blueprint. All downstream work derives from these artifacts. Reads: product-discovery.json, why.json, stack.json. In default mode, always pause here regardless of previous auto-confirms.

#### Phase 3: Specification
- **Agent**: Product Owner (Opus)
- **Skills**: `/shipkit-spec` (batch mode from product-definition)
- **Gate**: All MVP features in `product-definition.json` have specs written
- **Notes**: Uses Opus for complex spec reasoning. Iterates MVP features in dependency order from `product-definition.json`.

#### Phase 4: Architecture
- **Agent**: Architect (Sonnet)
- **Skills**: `/shipkit-architecture-memory --propose` (solution architect mode)
- **Gate**: `architecture.json` written and confirmed
- **Notes**: Reads all Phase 1-3 artifacts for informed architecture proposal. Optionally runs `/shipkit-data-contracts` first if specs reference complex entity relationships (produces `contracts.json` which informs architecture).

#### Phase 5: Planning
- **Agent**: Architect (Sonnet)
- **Skills**: `/shipkit-plan`
- **Gate**: Plan files for all specs written
- **Notes**: One plan per spec. Plans produced in dependency order. Each plan reads previous plans as context. Optionally runs `/shipkit-test-cases` to generate test case specs before implementation.

#### Phase 6: Implementation + Verification
- **Agents**: Implementers (Sonnet, parallel) + Reviewer (Opus)
- **Skills**: `/shipkit-build-relentlessly`, `/shipkit-test-relentlessly`, `/shipkit-lint-relentlessly`, `/shipkit-verify`, `/shipkit-preflight`
- **Gate**: All features implemented, tests pass, lint clean, verification passes
- **Notes**: File ownership from plans. Features implemented in dependency order from product-definition. `/shipkit-integration-docs` triggered on-demand when implementers encounter external services. Verify + preflight run after all features complete. For apps with UI, `/shipkit-qa-visual` and `/shipkit-semantic-qa` can run as optional quality checks.

### Full Skill Coverage (36 user-facing skills)

Every Shipkit skill has a defined role relative to this pipeline. No skill is "cross-cutting" — each is either a core pipeline step, a phase-specific augmentation, a pre-pipeline prerequisite, or explicitly manual-mode-only. (`shipkit-detect` is system hook infrastructure, not counted as a user-facing skill.)

#### Core Pipeline Skills (14)

These are invoked directly by the pipeline phases:

| Phase | Skill | Role |
|-------|-------|------|
| 1 | `/shipkit-why-project` | Vision → why.json |
| 1 | `/shipkit-product-discovery` | User needs → product-discovery.json |
| 1 | `/shipkit-project-context` | Stack detection → stack.json (parallel) |
| 2 | `/shipkit-product-definition` | Solution blueprint → product-definition.json |
| 2 | `/shipkit-goals` | Success criteria → goals.json |
| 3 | `/shipkit-spec` | Feature specs → specs/*.json (batch) |
| 4 | `/shipkit-architecture-memory` | Architecture proposal → architecture.json |
| 5 | `/shipkit-plan` | Implementation plans → plans/*.json |
| 6 | `/shipkit-build-relentlessly` | Build until it compiles |
| 6 | `/shipkit-test-relentlessly` | Test until green |
| 6 | `/shipkit-lint-relentlessly` | Lint until clean |
| 6 | `/shipkit-implement-independently` | Autonomous single-agent implementation |
| 6 | `/shipkit-verify` | Verify against spec |
| 6 | `/shipkit-preflight` | Production readiness audit |

#### Phase-Specific Optional Skills (15)

Augment specific phases when the project needs them:

| Phase | Skill | When to use |
|-------|-------|-------------|
| 1 | `/shipkit-thinking-partner` | Complex domain needing brainstorming |
| 1 | `/shipkit-feedback-bug` | Existing user feedback to incorporate |
| 4 | `/shipkit-data-contracts` | Complex entity relationships in specs |
| 5 | `/shipkit-test-cases` | Generate test case specs before implementation |
| 6 | `/shipkit-integration-docs` | External API integration detected during implementation |
| 6 | `/shipkit-cleanup-worktrees` | After parallel worktree-based implementation |
| 6 | `/shipkit-qa-visual` | UI-heavy app needing visual QA |
| 6 | `/shipkit-semantic-qa` | API/LLM output quality verification |
| 6 | `/shipkit-ux-audit` | UX pattern review |
| 6 | `/shipkit-scale-ready` | Production scaling concerns |
| 6 | `/shipkit-prompt-audit` | AI prompt quality in LLM apps |
| 6 | `/shipkit-user-instructions` | Track manual tasks (env vars, service signups) |
| post | `/shipkit-communications` | Stakeholder report after build completes |
| post | `/shipkit-work-memory` | Session handoff if pipeline is interrupted or completed |
| post | `/shipkit-team` | This skill — orchestrates implementation (Phase 6 uses its own standard team flow) |

#### Pre-Pipeline Prerequisites (5)

Run before starting the pipeline — one-time setup, not build steps:

| Skill | Purpose |
|-------|---------|
| `/shipkit-update` | Ensure Shipkit version is current |
| `/shipkit-claude-md` | Configure project CLAUDE.md preferences |
| `/shipkit-codebase-index` | Semantic index for large existing codebases |
| `/shipkit-get-skills` | Discover and install community Claude Code skills |
| `/shipkit-get-mcps` | Discover and install MCP servers for integrations |

#### Manual-Mode-Only Skills (2)

These skills are for ad-hoc usage outside the pipeline. The pipeline replaces their function:

| Skill | Why excluded |
|-------|-------------|
| `/shipkit-master` | Pipeline template replaces master's routing |
| `/shipkit-project-status` | Pipeline state replaces gap analysis |

### Pipeline State

Write `.shipkit/team-state.local.json` with pipeline-specific fields:

```json
{
  "template": "pipeline",
  "productGoal": "Build a learning app with spaced repetition",
  "mode": "default",
  "created": "ISO timestamp",
  "phases": [
    {"id": 1, "name": "Discovery", "status": "in_progress", "gate": "why + personas/discovery confirmed"},
    {"id": 2, "name": "Solution Design", "status": "pending", "gate": "product-definition.json + goals.json confirmed"},
    {"id": 3, "name": "Specification", "status": "pending", "gate": "All feature specs written"},
    {"id": 4, "name": "Architecture", "status": "pending", "gate": "architecture.json confirmed"},
    {"id": 5, "name": "Planning", "status": "pending", "gate": "All plans written"},
    {"id": 6, "name": "Implementation", "status": "pending", "gate": "All features built + verified"}
  ],
  "currentPhase": 1,
  "gateAutoConfirm": false,
  "artifacts": {
    "why": null,
    "goals": null,
    "personas": null,
    "stack": null,
    "productDefinition": null,
    "specs": [],
    "contracts": null,
    "architecture": null,
    "plans": []
  }
}
```

### Artifact-Aware Startup

On pipeline startup, scan `.shipkit/` before doing anything else. Map existing artifacts to phases and start from the first incomplete phase — never redo work that already exists.

#### Artifact → Phase Mapping

| Phase | Required Artifacts | Complete When |
|-------|--------------------|---------------|
| 1 Discovery | `why.json`, `product-discovery.json` | Both exist and non-empty. `stack.json` optional (parallel). |
| 2 Solution Design | `product-definition.json`, `goals.json` | Both exist. Definition has `features[]` array. Goals has `criteria[]` array. |
| 3 Specification | `specs/todo/*.json` or `specs/active/*.json` | Spec count ≥ feature count from product-definition. |
| 4 Architecture | `architecture.json` | Exists with at least one entry. `contracts.json` optional. |
| 5 Planning | `plans/todo/*.json` or `plans/active/*.json` | Plan count ≥ spec count. |
| 6 Implementation | (code is the artifact) | All features built, tests pass, verify passes. |

#### Scan Logic

```
1. Read .shipkit/ directory listing
2. For each phase 1→5, check if required artifacts exist
3. For Phase 3: count spec files, compare to product-definition.features.length
4. For Phase 5: count plan files, compare to spec count
5. Find earliest phase with missing or incomplete artifacts
6. Mark all prior phases as "completed" in pipeline state
```

#### Partial Phase Detection

Phase 3 (Specification) and Phase 5 (Planning) can be **partially complete** — some specs or plans exist but not all. When detected:
- Count existing vs required
- Only generate the missing items
- Display which items are done and which remain

#### Startup Display

Always show the scan result before proceeding:

```
Pipeline Artifact Scan:
  ✅ Phase 1 (Discovery): why.json, product-discovery.json, stack.json
  ✅ Phase 2 (Solution Design): product-definition.json, goals.json (12 criteria, 2 gates)
  ⚠️ Phase 3 (Specification): 3/12 specs written — 9 remaining
  ❌ Phase 4 (Architecture): not started
  ❌ Phase 5 (Planning): not started
  ❌ Phase 6 (Implementation): not started

Starting from Phase 3 — completing 9 remaining specs.
Proceed?
```

Status icons:
- ✅ = phase complete (all artifacts present and valid)
- ⚠️ = phase partially complete (some artifacts exist)
- ❌ = phase not started (no artifacts)

If ALL phases are complete (rare — means artifacts exist but code wasn't built), start at Phase 6.
If NO artifacts exist, start at Phase 1 (normal greenfield flow).

### Gate Logic

**Default mode** (`gateAutoConfirm: false`):
- After each phase completes, present the produced artifacts to the user
- Wait for confirmation: "Confirm and proceed to Phase {N+1}, or adjust?"
- User can: confirm, adjust artifacts, switch to YOLO mode, or stop

**YOLO mode** (`gateAutoConfirm: true`):
- Auto-confirm all artifact gates
- Only stop on: build/test failures, ambiguity requiring user input, or PR creation
- User can interrupt at any time and switch to default mode

**Mode switching**: User can say "switch to yolo" or "switch to default" at any gate. Update `gateAutoConfirm` in team state.

### Pipeline Execution Flow

```
1. Parse $ARGUMENTS for product goal, --yolo flag
2. Run artifact scan (see Artifact-Aware Startup above)
3. Display scan results to user
4. If scan found completed phases: "Starting from Phase {N}. Proceed?"
   - In YOLO mode: auto-proceed
   - In default mode: wait for user confirmation
5. Write pipeline team state (with completed phases pre-marked)
6. For each pending/partial phase:
   a. Spawn appropriate agent(s) with skills
   b. Pass product goal + ALL existing artifacts as context (including from completed phases)
   c. For partial phases: pass list of already-completed items so agent skips them
   d. Wait for phase completion
   e. Verify gate condition
   f. If default mode: present artifacts, wait for confirmation
   g. If YOLO mode: auto-proceed (unless failure)
   h. Update team state
7. After Phase 6: report full summary
8. Cleanup: delete team state, move plans to shipped/
```

### Phase 6 Team Composition

Phase 6 uses the standard team pattern from this skill (Steps 2-8 above):
1. Read all plans from `.shipkit/plans/todo/`
2. Derive file ownership clusters from plan tasks
3. Spawn implementer teammates (one per cluster)
4. Spawn reviewer teammate
5. Monitor, gate, and complete per standard team flow

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

<!-- SECTION:success-criteria -->
## Success Criteria

- [ ] Plan read and tasks decomposed into ownership clusters
- [ ] Team state file written to `.shipkit/team-state.local.json`
- [ ] Agent team created with implementers + reviewer
- [ ] All tasks completed and gate conditions verified
- [ ] `/shipkit-verify` run on full changeset
- [ ] `/shipkit-preflight` run for production readiness
- [ ] Team cleaned up, state file deleted
<!-- /SECTION:success-criteria -->

---

<!-- SECTION:after-completion -->
## After Completion

**Team succeeded:** All tasks done, verify + preflight passed. Review the changes and commit/PR.

**Team partially completed:** Some tasks may remain. Check task list status, spawn replacement teammates if needed.

**Next steps:**
- Commit changes or create PR
- `/shipkit-work-memory` — Log the team execution for session continuity
- `/shipkit-verify` — Re-run if additional changes were made post-team
<!-- /SECTION:after-completion -->

---

## Constraints

- Requires Agent Teams experimental feature enabled
- One team per session (Claude Code limitation)
- No nested teams — teammates cannot create sub-teams
- Lead session is fixed for team lifetime
- Teammates cannot be resumed after session ends
