---
description: Execute the implementation plan by processing and executing all tasks defined in tasks.md
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---

## Agent Personas

**Load these personas before execution:**

| Phase | Agent | File | Adopt |
|-------|-------|------|-------|
| Implementation | Implementer | `.claude/agents/implementer-agent.md` | TDD discipline, minimal code, verify before claiming done |
| Reviews | Reviewer | `.claude/agents/reviewer-agent.md` | Spec compliance + code quality checks |

**For subagent mode:** Include the relevant persona in each dispatch prompt.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Execution Mode

**Choose execution mode based on task count:**

| Tasks | Recommended Mode | Why |
|-------|------------------|-----|
| 1-5 | Direct | Low overhead, fast |
| 6+ | Subagent | Fresh context per task, no pollution |

**Ask user at start:**
```
Implementation has N tasks. How would you like to execute?

1. Direct mode - I execute each task (faster for small plans)
2. Subagent mode - Fresh agent per task (better for large plans)
```

## Required Skills Integration

**This skill integrates devkit for quality execution:**

| Skill | When Used | Purpose |
|-------|-----------|---------|
| `/test-driven-development` | Every task | RED-GREEN-REFACTOR cycle enforced |
| `/verification-before-completion` | Before marking task done | Evidence before claims |
| `/systematic-debugging` | When tests fail | Root cause investigation |
| `/finishing-a-development-branch` | After all tasks complete | Merge/PR workflow |

## Outline

1. Run `{SCRIPT}` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Check checklists status** (if FEATURE_DIR/checklists/ exists):
   - Scan all checklist files in the checklists/ directory
   - For each checklist, count:
     - Total items: All lines matching `- [ ]` or `- [X]` or `- [x]`
     - Completed items: Lines matching `- [X]` or `- [x]`
     - Incomplete items: Lines matching `- [ ]`
   - Create a status table:

     ```text
     | Checklist | Total | Completed | Incomplete | Status |
     |-----------|-------|-----------|------------|--------|
     | ux.md     | 12    | 12        | 0          | ✓ PASS |
     | test.md   | 8     | 5         | 3          | ✗ FAIL |
     | security.md | 6   | 6         | 0          | ✓ PASS |
     ```

   - **If any checklist is incomplete**: STOP and ask user whether to proceed
   - **If all checklists complete**: Proceed to step 3

3. Load and analyze the implementation context:
   - **REQUIRED**: Read tasks.md for the complete task list and execution plan
   - **REQUIRED**: Read plan.md for tech stack, architecture, and file structure
   - **REQUIRED**: Read spec.md for user stories and acceptance criteria
   - **IF EXISTS**: Read data-model.md, contracts/, research.md, quickstart.md

4. **Project Setup Verification**:
   - Create/verify ignore files (.gitignore, .dockerignore, etc.) based on tech stack
   - See Appendix A for technology-specific patterns

5. Parse tasks.md and extract phases, dependencies, [P] markers, [US#] labels.

6. **Execute Tasks with TDD and Review** (per-task workflow):

   ```
   FOR EACH task in tasks.md:

   ┌─────────────────────────────────────────────────────────────┐
   │ STEP 1: TDD - Write Failing Test (RED)                     │
   │ ─────────────────────────────────────────────────────────── │
   │ • Write test that demonstrates desired behavior             │
   │ • Run test → MUST FAIL                                      │
   │ • If test passes immediately → test is wrong, fix it        │
   │ • Commit failing test                                       │
   └─────────────────────────────────────────────────────────────┘
                              ↓
   ┌─────────────────────────────────────────────────────────────┐
   │ STEP 2: TDD - Minimal Implementation (GREEN)                │
   │ ─────────────────────────────────────────────────────────── │
   │ • Write MINIMAL code to make test pass                      │
   │ • No extra features, no "improvements"                      │
   │ • Run test → MUST PASS                                      │
   │ • Run ALL tests → MUST PASS (no regressions)                │
   └─────────────────────────────────────────────────────────────┘
                              ↓
   ┌─────────────────────────────────────────────────────────────┐
   │ STEP 3: TDD - Refactor (keep tests green)                   │
   │ ─────────────────────────────────────────────────────────── │
   │ • Clean up code while tests stay green                      │
   │ • Remove duplication, improve names                         │
   │ • Commit implementation                                     │
   └─────────────────────────────────────────────────────────────┘
                              ↓
   ┌─────────────────────────────────────────────────────────────┐
   │ STEP 4: Spec Compliance Review                              │
   │ ─────────────────────────────────────────────────────────── │
   │ • Compare implementation against spec.md requirements       │
   │ • Check: Does it match the user story acceptance criteria?  │
   │ • Check: Nothing extra added (YAGNI)?                       │
   │ • Check: Nothing missing from requirements?                 │
   │                                                             │
   │ IF issues found:                                            │
   │   → Fix issues                                              │
   │   → Re-run spec compliance review                           │
   │   → Repeat until compliant                                  │
   └─────────────────────────────────────────────────────────────┘
                              ↓
   ┌─────────────────────────────────────────────────────────────┐
   │ STEP 5: Code Quality Review                                 │
   │ ─────────────────────────────────────────────────────────── │
   │ • Review for code quality issues:                           │
   │   - Magic numbers/strings                                   │
   │   - Missing error handling                                  │
   │   - Poor naming                                             │
   │   - Unnecessary complexity                                  │
   │                                                             │
   │ IF issues found:                                            │
   │   → Fix issues (keep tests green)                           │
   │   → Re-run code quality review                              │
   │   → Repeat until approved                                   │
   └─────────────────────────────────────────────────────────────┘
                              ↓
   ┌─────────────────────────────────────────────────────────────┐
   │ STEP 6: Verification Before Completion                      │
   │ ─────────────────────────────────────────────────────────── │
   │ • Run full test suite → capture output                      │
   │ • Verify: All tests pass? (with evidence)                   │
   │ • Verify: No warnings/errors in output?                     │
   │ • ONLY THEN: Mark task [X] in tasks.md                      │
   │                                                             │
   │ NO "should pass" or "looks good" - EVIDENCE REQUIRED        │
   └─────────────────────────────────────────────────────────────┘
   ```

7. **Phase Checkpoints**:
   - After each phase, run full test suite
   - Report: "Phase N complete. X/Y tests passing."
   - If user story phase complete: "User Story N independently testable."

8. **Error Handling**:
   - If tests fail during implementation → Use `/systematic-debugging`
   - If task cannot be completed → Report blocker, suggest next steps
   - Never skip TDD steps or reviews

9. **Completion**:
   - All tasks marked [X] in tasks.md
   - All tests passing (with verification output)
   - Run `/finishing-a-development-branch` for merge/PR workflow

---

## Subagent Execution Mode

**When user chooses subagent mode, execute each task via fresh subagent:**

```
FOR EACH task:

┌─────────────────────────────────────────────────────────────┐
│ CONTROLLER: Prepare task context                            │
│ ─────────────────────────────────────────────────────────── │
│ • Extract task from tasks.md (full text + dependencies)     │
│ • Gather context: spec.md requirements, plan.md structure   │
│ • Note: Which user story? What acceptance criteria?         │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ DISPATCH: Implementation subagent                           │
│ ─────────────────────────────────────────────────────────── │
│ Prompt:                                                     │
│ "Implement this task using TDD:                             │
│                                                             │
│  Task: [full task text from tasks.md]                       │
│  Context: [relevant spec.md excerpts]                       │
│  Files: [exact paths from task]                             │
│                                                             │
│  Requirements:                                              │
│  1. Write failing test FIRST                                │
│  2. Implement minimal code to pass                          │
│  3. Refactor if needed                                      │
│  4. Commit your changes                                     │
│                                                             │
│  Return: Summary of what you implemented and test results"  │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ CONTROLLER: Spec Compliance Review                          │
│ ─────────────────────────────────────────────────────────── │
│ • Review subagent's changes against spec.md                 │
│ • Check: Matches acceptance criteria?                       │
│ • Check: Nothing extra (YAGNI)?                             │
│                                                             │
│ IF issues: Dispatch fix subagent → re-review                │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ CONTROLLER: Code Quality Review                             │
│ ─────────────────────────────────────────────────────────── │
│ • Review for quality issues                                 │
│ • Check: Clean code? Good names? Error handling?            │
│                                                             │
│ IF issues: Dispatch fix subagent → re-review                │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ CONTROLLER: Verify and mark complete                        │
│ ─────────────────────────────────────────────────────────── │
│ • Run full test suite                                       │
│ • Verify output shows all passing                           │
│ • Mark task [X] in tasks.md                                 │
│ • Report: "Task N complete. X/Y tests passing."             │
└─────────────────────────────────────────────────────────────┘
```

**Benefits of subagent mode:**
- Fresh context per task (no pollution from previous tasks)
- Controller maintains overview, subagents focus on details
- Parallel-safe (subagents don't interfere with each other)
- Better for large implementations (6+ tasks)

**When NOT to use subagent mode:**
- Small implementations (1-5 tasks)
- Tasks are tightly coupled and need shared context
- Debugging issues that span multiple tasks

## The Iron Rules

**TDD is NOT optional:**
- NO production code without a failing test first
- Code before test? Delete it. Start over.
- Test passes immediately? Test is wrong.

**Verification is NOT optional:**
- NO claiming "done" without running verification
- NO "should pass" - run the command, show the output
- Evidence before claims, always.

**Reviews are NOT optional:**
- Spec compliance review catches over/under-building
- Code quality review catches implementation issues
- Both must pass before marking task complete

## Appendix A: Ignore File Patterns

**Common Patterns by Technology** (from plan.md tech stack):
- **Node.js/JavaScript/TypeScript**: `node_modules/`, `dist/`, `build/`, `*.log`, `.env*`
- **Python**: `__pycache__/`, `*.pyc`, `.venv/`, `venv/`, `dist/`, `*.egg-info/`
- **Java**: `target/`, `*.class`, `*.jar`, `.gradle/`, `build/`
- **Go**: `*.exe`, `*.test`, `vendor/`, `*.out`
- **Rust**: `target/`, `debug/`, `release/`, `*.rs.bk`, `.idea/`, `*.log`, `.env*`
- **Universal**: `.DS_Store`, `Thumbs.db`, `*.tmp`, `*.swp`, `.vscode/`, `.idea/`

Note: This command assumes tasks.md exists. If missing, run `/tasks` first.
