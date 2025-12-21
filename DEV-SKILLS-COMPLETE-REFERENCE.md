# Dev Skills - Complete Reference

**Created:** 2025-12-21
**Purpose:** Comprehensive listing of all 20 dev skills with purposes, order, and dependencies

---

## Skill Categories

### 1. Core Pipeline (Artifact-Generating) - 5 Skills
Create structured artifacts that guide development

### 2. Workflow & Process - 5 Skills
Guide execution and coordination

### 3. Quality & Methodology - 3 Skills
Enforce discipline and best practices

### 4. Git & Collaboration - 4 Skills
Version control and code review workflows

### 5. Agent Orchestration - 2 Skills
Parallel execution and subagent patterns

### 6. Meta & Documentation - 2 Skills
Skill creation and planning (1 deprecated)

---

## Complete Skill List

### Core Pipeline Skills (Artifact-Generating)

#### 1. dev-constitution-builder
**Purpose:** Build project constitution at two key phases
**Creates:** Product principles (after strategic thinking) and technical standards (before specify)
**Depends on:**
- Product phase: `/prod-strategic-thinking` (optional)
- Technical phase: `/dev-plan` (optional)
**Order:** Can be called twice:
1. After `/prod-strategic-thinking` → product constitution
2. Before `/dev-specify` or after `/dev-plan` → technical constitution

**Artifact:** `/.devkit/memory/constitution.md`

---

#### 2. dev-specify
**Purpose:** Create feature specification from natural language description
**Creates:** Detailed spec with requirements, scenarios, acceptance criteria
**Depends on:**
- Optional: Product discovery artifacts (`.prodkit/` folder)
- Optional: Technical constitution
**Order:** First step in dev pipeline (after optional prod discovery)
**Handoffs:** → dev-plan, dev-clarify

**Artifacts:**
- `specs/N-short-name/spec.md`
- Creates feature branch `N-short-name`

---

#### 3. dev-clarify
**Purpose:** Identify underspecified areas and clarify requirements
**Creates:** Updated spec.md with clarifications
**Depends on:** dev-specify (requires spec.md)
**Order:** Optional step between specify and plan (reduces downstream rework)
**Handoffs:** → dev-plan

**Artifact:** Updates existing spec.md

---

#### 4. dev-plan
**Purpose:** Execute implementation planning workflow
**Creates:** Technical design artifacts (plan, data model, contracts, research)
**Depends on:** dev-specify (requires spec.md)
**Order:** After specify, before tasks
**Handoffs:** → dev-tasks, dev-checklist

**Artifacts:**
- `specs/N-short-name/plan.md`
- `specs/N-short-name/research.md`
- `specs/N-short-name/data-model.md`
- `specs/N-short-name/contracts/` (API definitions)
- `specs/N-short-name/quickstart.md`

---

#### 5. dev-tasks
**Purpose:** Generate actionable, dependency-ordered tasks
**Creates:** Executable task list organized by user stories
**Depends on:** dev-plan (requires plan.md, spec.md)
**Order:** After plan, before implementation
**Handoffs:** → dev-analyze, dev-implement

**Artifact:** `specs/N-short-name/tasks.md`

---

#### 6. dev-checklist
**Purpose:** Generate domain-specific quality checklists
**Creates:** "Unit tests for requirements" - validates spec completeness
**Depends on:** dev-specify or dev-plan (optional context)
**Order:** Can be called anytime after spec exists
**Note:** NOT for testing implementation - for validating requirement quality

**Artifact:** `specs/N-short-name/checklists/*.md`

---

### Workflow & Process Skills

#### 7. dev-analyze
**Purpose:** Cross-artifact consistency analysis
**Creates:** Analysis report (read-only, does not modify files)
**Depends on:** dev-tasks (requires spec.md, plan.md, tasks.md)
**Order:** After tasks, before implement (validates consistency)
**Note:** Strictly read-only, identifies issues without fixing

**Artifact:** Analysis report (output only)

---

#### 8. dev-implement
**Purpose:** Execute implementation with TDD and optional subagent mode
**Creates:** Working code, tests, commits
**Depends on:** dev-tasks (requires tasks.md)
**Order:** After tasks (and optional analyze)
**Integrates:** TDD, verification, debugging, two-stage code review
**Modes:**
- Direct (1-5 tasks)
- Subagent (6+ tasks, fresh context per task)

**Artifacts:** Source code, tests, git commits

---

#### 9. dev-taskstoissues
**Purpose:** Convert tasks.md to GitHub issues
**Creates:** GitHub issues matching tasks
**Depends on:** dev-tasks (requires tasks.md)
**Order:** After tasks (optional workflow step)
**Requires:** GitHub remote, GitHub MCP server

**Artifact:** GitHub issues

---

#### 10. dev-constitution
**Purpose:** Update project constitution (different from builder)
**Creates:** Updated constitution with versioning
**Depends on:** Existing constitution template
**Order:** Can be called anytime to update constitution
**Note:** Different from constitution-builder (this updates, builder creates)

**Artifact:** `/.devkit/memory/constitution.md`

---

#### 11. dev-using-git-worktrees
**Purpose:** Create isolated git worktrees for feature work
**Creates:** Isolated workspace
**Depends on:** None
**Order:** Before starting feature work (isolation from main workspace)
**Note:** Validates .gitignore safety

**Artifact:** Git worktree directory

---

### Quality & Methodology Skills

#### 12. dev-test-driven-development
**Purpose:** TDD methodology - write test first, watch fail, implement
**Creates:** Tests and implementation following RED-GREEN-REFACTOR
**Depends on:** None (methodology skill)
**Order:** Integrated into dev-implement, but can be invoked explicitly
**Core Principle:** NO PRODUCTION CODE WITHOUT FAILING TEST FIRST

**Pattern:** RED (failing test) → GREEN (minimal code) → REFACTOR (clean up)

---

#### 13. dev-verification-before-completion
**Purpose:** Evidence-based completion verification
**Creates:** Verification evidence before claiming success
**Depends on:** None (methodology skill)
**Order:** Before any completion claim (integrated into dev-implement)
**Core Principle:** NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE

**Pattern:** Identify command → Run → Read output → Verify → Claim (with evidence)

---

#### 14. dev-systematic-debugging
**Purpose:** Root cause investigation before fixing
**Creates:** Root cause analysis and targeted fixes
**Depends on:** None (methodology skill)
**Order:** When encountering bugs/failures (integrated into dev-implement)
**Core Principle:** NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST

**Pattern:** Root cause → Minimal fix → Verify fix → Prevent recurrence

---

### Git & Collaboration Skills

#### 15. dev-finishing-a-development-branch
**Purpose:** Complete development work with structured options
**Creates:** Merged code or PR
**Depends on:** Passing tests
**Order:** After implementation complete
**Options:** Merge locally, create PR, keep as-is, discard

**Pattern:** Verify tests → Determine base → Present options → Execute choice

---

#### 16. dev-requesting-code-review
**Purpose:** Request code review via subagent
**Creates:** Review dispatch and feedback
**Depends on:** Completed code
**Order:** After tasks, major features, or before merge
**Note:** Dispatches code-reviewer subagent

**Pattern:** Get SHAs → Dispatch reviewer → Act on feedback

---

#### 17. dev-receiving-code-review
**Purpose:** Handle code review feedback with technical rigor
**Creates:** Verified implementation of feedback
**Depends on:** Received review feedback
**Order:** After receiving review
**Core Principle:** Verify before implementing, ask before assuming

**Pattern:** Read → Understand → Verify → Evaluate → Respond → Implement

---

### Agent Orchestration Skills

#### 18. dev-dispatching-parallel-agents
**Purpose:** Dispatch multiple agents for independent tasks
**Creates:** Parallel investigation/fixes
**Depends on:** Multiple independent problems
**Order:** When facing 2+ independent failures
**Use when:** 3+ test files failing independently, different subsystems broken

**Pattern:** Identify domains → Create focused tasks → Dispatch parallel → Review/integrate

---

#### 19. dev-subagent-driven-development
**Status:** DEPRECATED - Integrated into dev-implement
**Purpose:** Fresh agent per task (now subagent mode in dev-implement)
**Replacement:** Use `/dev-implement` with subagent mode option

---

### Meta & Documentation Skills

#### 20. dev-writing-skills
**Purpose:** Guide for creating new skills using TDD
**Creates:** New skills
**Depends on:** Understanding of dev-test-driven-development
**Order:** When creating skills
**Core Principle:** Skills ARE test-driven development for process docs

**Pattern:** Baseline test (agent fails) → Write skill → Verify compliance → Close loopholes

---

#### 21. dev-writing-plans (DEPRECATED)
**Status:** DEPRECATED - Use dev-plan instead
**Replacement:** Use standard workflow: `/dev-specify → /dev-plan → /dev-tasks → /dev-implement`

---

## Dependency Graph

### Core Development Pipeline

```
[Optional: Product Discovery Skills (prod-*)]
           ↓
[dev-constitution-builder --product]  ← After strategic thinking
           ↓
[dev-specify] ← Feature description
           ↓
[dev-clarify] ← Optional: Reduce ambiguity
           ↓
[dev-constitution-builder --technical] ← Optional: Before planning
           ↓
[dev-plan] ← Creates design artifacts
           ↓
[dev-tasks] ← Breaks down into executable tasks
           ↓
[dev-checklist] ← Optional: Create domain checklists
           ↓
[dev-analyze] ← Optional: Validate consistency
           ↓
[dev-implement] ← Execute with TDD
    ├─ Integrates: dev-test-driven-development
    ├─ Integrates: dev-verification-before-completion
    ├─ Integrates: dev-systematic-debugging (when needed)
    ├─ Integrates: dev-requesting-code-review (per task)
    └─ Uses: dev-dispatching-parallel-agents (for independent tasks)
           ↓
[dev-finishing-a-development-branch] ← Merge or PR
```

### Supporting/Parallel Workflows

```
[dev-taskstoissues] ← After dev-tasks (parallel to implement)

[dev-using-git-worktrees] ← Before starting (isolation)

[dev-constitution] ← Anytime (update constitution)

[dev-receiving-code-review] ← After reviews received

[dev-writing-skills] ← Anytime (create new skills)
```

---

## Execution Order Recommendations

### Full Pipeline (New Feature)

1. **Optional Product Discovery** (prod skills)
2. **dev-constitution-builder --product** (if doing product discovery)
3. **dev-specify** "Add user authentication"
4. **dev-clarify** (optional, reduces rework)
5. **dev-constitution-builder --technical** (optional)
6. **dev-plan**
7. **dev-tasks**
8. **dev-checklist** (optional, validate requirements)
9. **dev-analyze** (optional, check consistency)
10. **dev-implement** (choose direct or subagent mode)
11. **dev-finishing-a-development-branch**

### Quick Feature (Minimal Path)

1. **dev-specify** "Add feature"
2. **dev-plan**
3. **dev-tasks**
4. **dev-implement**
5. **dev-finishing-a-development-branch**

### Bug Fix

1. **dev-systematic-debugging** (find root cause)
2. **dev-test-driven-development** (write failing test)
3. Fix implementation
4. **dev-verification-before-completion** (verify fix)
5. **dev-finishing-a-development-branch**

---

## Prerequisites Summary

| Skill | Required Prerequisites | Optional Prerequisites |
|-------|----------------------|----------------------|
| dev-specify | None | Product discovery artifacts |
| dev-clarify | spec.md | - |
| dev-plan | spec.md | constitution.md |
| dev-tasks | plan.md, spec.md | - |
| dev-checklist | spec.md or plan.md | - |
| dev-analyze | spec.md, plan.md, tasks.md | constitution.md |
| dev-implement | tasks.md | All design artifacts |
| dev-taskstoissues | tasks.md | GitHub remote |
| dev-constitution-builder | - | strategic-thinking (product phase), plan.md (tech phase) |
| dev-using-git-worktrees | Git repo | - |
| dev-finishing-a-development-branch | Passing tests | - |
| dev-requesting-code-review | Completed code | - |
| dev-receiving-code-review | Review feedback | - |
| dev-dispatching-parallel-agents | Multiple independent tasks | - |

---

## Migration Categories

### Artifact-Generating (Need full structure)

**Need:** scripts/ + templates/ + references/ + outputs/

1. ✅ **dev-specify** - Already has infrastructure
2. **dev-plan** - Creates plan.md
3. **dev-tasks** - Creates tasks.md
4. **dev-constitution-builder** - Creates constitution.md
5. **dev-checklist** - Creates checklists/*.md

### Workflow Skills (Need only references/)

**Need:** references/ (reference.md, examples.md, README.md)

All others (15 skills):
- dev-implement
- dev-analyze
- dev-clarify
- dev-taskstoissues
- dev-constitution
- dev-requesting-code-review
- dev-receiving-code-review
- dev-finishing-a-development-branch
- dev-using-git-worktrees
- dev-systematic-debugging
- dev-test-driven-development
- dev-verification-before-completion
- dev-dispatching-parallel-agents
- dev-subagent-driven-development (deprecated)
- dev-writing-skills
- dev-writing-plans (deprecated)

---

## Integration Points

### dev-implement Integrations

dev-implement is the orchestrator that integrates multiple skills:

```
dev-implement
├─ Per Task:
│  ├─ dev-test-driven-development (RED-GREEN-REFACTOR)
│  ├─ dev-verification-before-completion (evidence before claims)
│  ├─ dev-systematic-debugging (when tests fail)
│  └─ dev-requesting-code-review (two-stage review)
│
└─ After All Tasks:
   └─ dev-finishing-a-development-branch (merge/PR workflow)
```

### Methodology Skills

Three methodology skills are referenced throughout:
1. **dev-test-driven-development** - Core to dev-implement
2. **dev-verification-before-completion** - Gate before completion claims
3. **dev-systematic-debugging** - Invoked when bugs occur

---

## Key Patterns

### Constitution Flow

```
Product Phase:
  /prod-strategic-thinking
    → /dev-constitution-builder --product
    → product principles

Technical Phase:
  /dev-plan
    → /dev-constitution-builder --technical
    → technical standards
```

### Clarification Flow

```
/dev-specify
  → [NEEDS CLARIFICATION markers]
  → /dev-clarify (resolve ambiguities)
  → Updated spec.md
  → /dev-plan (less rework)
```

### Quality Gates

```
/dev-tasks
  → /dev-analyze (optional: check consistency)
  → /dev-checklist (optional: validate requirements)
  → /dev-implement (TDD + verification enforced)
  → /dev-finishing-a-development-branch (tests must pass)
```

---

## Notes

1. **2 deprecated skills:** dev-subagent-driven-development, dev-writing-plans
2. **2 constitution skills:**
   - dev-constitution-builder (creates from scratch)
   - dev-constitution (updates existing)
3. **TDD is core:** Integrated into dev-implement, dev-writing-skills
4. **Verification is mandatory:** dev-verification-before-completion gates all completion claims
5. **Review is two-stage:** Spec compliance + code quality (in dev-implement)
