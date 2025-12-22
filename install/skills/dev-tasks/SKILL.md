---
name: dev-tasks
description: Generate dependency-ordered task breakdowns organized by user story with parallel execution markers and TDD integration. Use when the user asks to "break into tasks", "create tasks", "what are the steps", "task breakdown", or "implementation tasks" after planning is complete.
version: 1.0.0
triggers:
  - "break this into tasks"
  - "what are the steps"
  - "create tasks"
  - "task breakdown"
  - "implementation tasks"
agent: dev-architect
dependencies:
  - dev-specify
  - dev-plan
scripts:
  bash: .shipkit/skills/dev-tasks/scripts/create-tasks.sh
outputs:
  - .shipkit/skills/dev-tasks/outputs/specs/*/tasks.md
---

# Dev-Tasks: Dependency-Ordered Task Breakdown

**Purpose:** Transform technical plans into executable, dependency-ordered tasks organized by user story for independent implementation and testing.

**Agent Persona:** dev-architect (systems thinker, dependency analyzer, task organizer)

---

## When to Invoke

Run `/dev-tasks` when you have:
- ✅ Feature spec (spec.md) from `/dev-specify`
- ✅ Technical plan (plan.md) from `/dev-plan`
- ✅ Optional: constitution.md from `/dev-constitution`

**Timing:** After planning, before implementation

**User might say:**
- "Break this into tasks"
- "What are the implementation steps?"
- "Create a task list"
- "I need a task breakdown"

---

## What This Skill Does

### Input
Reads from feature directory (e.g., `specs/1-user-authentication/`):
- **spec.md** - User stories with priorities (REQUIRED)
- **plan.md** - Technical design (REQUIRED)
- **constitution.md** - Technical standards (RECOMMENDED)
- **data-model.md** - Entities (OPTIONAL)
- **contracts/** - API definitions (OPTIONAL)
- **research.md** - Technical decisions (OPTIONAL)
- **quickstart.md** - Test scenarios (OPTIONAL)

### Output
Generates `tasks.md` with:
- **Dependency-ordered tasks:** Sequential execution order respecting dependencies
- **User story organization:** One phase per story (US1, US2, US3...)
- **Parallel markers:** [P] indicates tasks that can run simultaneously
- **TDD integration:** Test tasks before implementation tasks (if TDD requested)
- **Constitution compliance:** Task patterns follow established standards
- **Clear file paths:** Every task specifies exact file location

### Structure
```
Phase 1: Setup (Project initialization)
Phase 2: Foundational (Blocking prerequisites - CRITICAL)
Phase 3: User Story 1 (Priority P1) 🎯 MVP
Phase 4: User Story 2 (Priority P2)
Phase 5: User Story 3 (Priority P3)
...
Phase N: Polish & Cross-Cutting Concerns
```

---

## Process

### Step 1: Run Script

The script (`create-tasks.sh`) will:
1. Validate feature directory exists
2. Check for required files (spec.md, plan.md)
3. Scan for optional files (data-model.md, contracts/, etc.)
4. Determine available context
5. Output paths to Claude

**Example invocation:**
```bash
.shipkit/skills/dev-tasks/scripts/create-tasks.sh specs/1-user-authentication
```

or with flags:

```bash
.shipkit/skills/dev-tasks/scripts/create-tasks.sh specs/1-user-authentication --update
```

### Step 2: Read All Input Documents

**ALWAYS read extended documentation FIRST**:

1. **References** (CRITICAL - read before generating tasks):
   - `.shipkit/skills/dev-tasks/references/reference.md` - Complete task generation guide
   - `.shipkit/skills/dev-tasks/references/examples.md` - Real-world examples

2. **Template:**
   ```
   .shipkit/skills/dev-tasks/templates/tasks-template.md
   ```

3. **Constitution (if exists):**
   ```
   .shipkit/skills/dev-constitution/outputs/constitution.md
   ```
   Extract:
   - Project structure (file paths)
   - Testing requirements (TDD? Coverage?)
   - Architectural patterns (Repository? Service layer?)
   - Naming conventions (PascalCase? camelCase?)

4. **Feature Spec (REQUIRED):**
   ```
   specs/N-feature-name/spec.md
   ```
   Extract:
   - User stories with priorities (P1, P2, P3...)
   - Acceptance criteria per story
   - TDD requirements

5. **Feature Plan (REQUIRED):**
   ```
   specs/N-feature-name/plan.md
   ```
   Extract:
   - Tech stack and libraries
   - Project structure (paths)
   - Architecture patterns
   - Component breakdown

6. **Optional Documents:**
   ```
   specs/N-feature-name/data-model.md      → Map entities to user stories
   specs/N-feature-name/contracts/         → Map endpoints to user stories
   specs/N-feature-name/research.md        → Extract setup decisions
   specs/N-feature-name/quickstart.md      → Extract test scenarios
   ```

### Step 3: Analyze Dependencies

**See** [reference.md](references/reference.md#dependency-analysis) for detailed guidance on:
- Data dependencies
- Infrastructure dependencies
- Cross-story dependencies
- Testing dependencies (TDD)

### Step 4: Generate Task Breakdown

Organize tasks following phase structure:

#### Phase 1: Setup (Shared Infrastructure)
**Purpose:** Project initialization
**Contains:** Project structure, dependencies, build config, linting

#### Phase 2: Foundational (Blocking Prerequisites)
**Purpose:** Core infrastructure ALL stories depend on
**⚠️ CRITICAL:** This phase BLOCKS all user story work
**Contains:** Database, auth framework, API routing, base models, error handling, logging

**Checkpoint:**
```markdown
**Checkpoint:** Foundation ready - user story implementation can now begin in parallel
```

#### Phase 3+: User Story Phases
**Purpose:** Deliver vertical slices of functionality
**One phase per user story from spec.md, ordered by priority (P1, P2, P3...)**

**See** [reference.md](references/reference.md#user-story-phases) for detailed phase structure

#### Final Phase: Polish & Cross-Cutting Concerns
**Purpose:** Improvements affecting multiple stories
**Contains:** Documentation, refactoring, performance, security, cross-cutting concerns

### Step 5: Apply Task Format

**EVERY task MUST follow this exact format:**

```
- [ ] [TaskID] [P?] [Story?] Description with file path
```

**Components:**
1. **Checkbox:** `- [ ]` (always present)
2. **Task ID:** T001, T002, T003... (sequential, in execution order)
3. **[P] marker:** ONLY if task can run in parallel
4. **[Story] label:** [US1], [US2], [US3] (REQUIRED for user story phases)
5. **Description:** Action verb + what + exact file path

**Examples:**
- ✅ `- [ ] T001 Create project structure per implementation plan`
- ✅ `- [ ] T012 [P] [US1] Create User model in src/models/user.py`
- ✅ `- [ ] T014 [US1] Implement UserService in src/services/user_service.py`
- ❌ `- [ ] Create models` (missing ID, Story label, file path)

**See** [reference.md](references/reference.md#task-format) for complete format rules

### Step 6: Document Dependencies

**See** [reference.md](references/reference.md#documenting-dependencies) for complete guidance

Create Dependencies & Execution Order section documenting:
- Phase dependencies
- User story dependencies
- Parallel opportunities

### Step 7: Include Implementation Strategy

**See** [reference.md](references/reference.md#implementation-strategy) for complete strategy patterns

Add strategy section showing:
- MVP First approach (User Story 1 only)
- Incremental delivery
- Parallel team strategy

### Step 8: Write Tasks File

Write the complete tasks.md to:
```
.shipkit/skills/dev-tasks/outputs/specs/[feature-name]/tasks.md
```

**File is PROTECTED:** Can only be modified by re-running the skill with `--update`

### Step 9: Report Summary

Report to user:
- Total task count
- Task count per phase
- Task count per user story
- Parallel opportunities identified
- MVP scope (typically User Story 1 only)
- Output file location

**Example:**
```
✅ Task breakdown complete!

📊 Summary:
  • Total tasks: 45
  • Setup: 5 tasks
  • Foundational: 8 tasks (CRITICAL PATH)
  • User Story 1 (MVP): 12 tasks
  • User Story 2: 10 tasks
  • User Story 3: 7 tasks
  • Polish: 3 tasks
  • Parallel opportunities: 18 tasks marked [P]

🎯 MVP Scope:
  • Setup + Foundational + User Story 1 = 25 tasks
  • Delivers core value independently

📁 Generated:
  • .shipkit/skills/dev-tasks/outputs/specs/1-user-authentication/tasks.md

👉 Next: Review task breakdown, then run /dev-implement to start execution
```

---

## Constitution Integration

### Read Constitution FIRST

Before generating any tasks, read:
```
.shipkit/skills/dev-constitution/outputs/constitution.md
```

### Constitution Influences Tasks

**See** [reference.md](references/reference.md#constitution-integration) for detailed integration patterns

Constitution defines:
1. **File Structure** → Tasks use correct paths
2. **Testing Requirements** → Tasks include appropriate tests
3. **Architectural Patterns** → Tasks follow established patterns
4. **Naming Conventions** → Descriptions use correct naming

---

## TDD Integration

**See** [reference.md](references/reference.md#tdd-integration) for complete TDD workflow

If spec.md or constitution.md require TDD, integrate RED-GREEN-REFACTOR cycle:

- 🔴 **RED Phase:** Write failing tests FIRST
- 🟢 **GREEN Phase:** Implement minimal code to pass
- 🔵 **REFACTOR Phase:** Clean up while keeping tests passing

---

## Key Constraints

### MUST Do

- ✅ Organize tasks by user story (one phase per story)
- ✅ Use strict task format: `- [ ] [ID] [P?] [Story?] Description with path`
- ✅ Read constitution.md FIRST before generating tasks
- ✅ Include [Story] labels on all user story phase tasks
- ✅ Make each user story independently testable
- ✅ Put only truly shared infrastructure in Foundational phase
- ✅ Mark parallel tasks with [P]
- ✅ Include exact file paths in every task
- ✅ Respect dependencies (task order must be execution order)

### MUST NOT Do

- ❌ Organize by technical layer (all models, then all services...)
- ❌ Create vague tasks without file paths
- ❌ Mark tasks [P] if they have dependencies
- ❌ Put story-specific infrastructure in Foundational phase
- ❌ Create cross-story dependencies (minimize coupling)
- ❌ Skip [Story] labels on user story tasks
- ❌ Ignore constitution standards

---

## Flags

- `--update` - Regenerate tasks if spec/plan changed (archives old version)
- `--archive` - Archive current tasks.md and create new version
- `--skip-prereqs` - Skip prerequisite checks
- `--cancel` - Cancel operation
- `--help` - Show usage information

---

## Handoffs

### After This Skill

**Next:** `/dev-analyze` (optional) or `/dev-implement`

**Optional quality gate:** Run `/dev-analyze` to check consistency between spec, plan, and tasks before implementing.

**Execute:** Run `/dev-implement` to start task execution with TDD, verification, and debugging integrated.

---

## Success Criteria

A good tasks.md has:
- ✅ Every task in correct format with ID, [P?], [Story?], path
- ✅ User story organization (one phase per story)
- ✅ Clear dependencies (sequential tasks in dependency order)
- ✅ Parallel opportunities identified ([P] markers)
- ✅ Independent test criteria per story
- ✅ MVP path clear (Setup + Foundational + US1)
- ✅ Constitution compliance documented
- ✅ TDD integration (if requested)
- ✅ Exact file paths for every task
- ✅ Checkpoints after each story

---

**For detailed guidance**, see:
- [reference.md](references/reference.md) - Complete task generation process
- [examples.md](references/examples.md) - Real-world examples
- [README.md](references/README.md) - Reference folder guide

**Remember**: Task generation balances structure (dependencies) with flexibility (parallel execution). Each task should be completable in 1-4 hours.
