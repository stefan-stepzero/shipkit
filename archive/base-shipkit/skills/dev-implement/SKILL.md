---
name: dev-implement
description: Execute feature implementation following Test-Driven Development with evidence-based verification and two-stage code review integrating TDD, systematic debugging, and verification gates. Use when the user asks to "implement", "build", "execute tasks", "start implementing", "code this", or after tasks are defined with dev-tasks.
---

# Implementation Execution

## Agent Persona

**Load:** `.claude/agents/implementer-agent.md`

Adopt: TDD discipline, minimal code, verify before claiming done, systematic debugging when issues arise.

## Purpose

Execute feature implementation following Test-Driven Development, with evidence-based verification and two-stage code review (spec compliance + code quality).

**Critical:** This skill enforces discipline through instructions, not script orchestration. You must follow the TDD cycle and verification gates.

## When to Trigger

User says:
- "Start implementing"
- "Execute the tasks"
- "Build the feature"
- "Implement the plan"
- After creating tasks with `/dev-tasks`

Or explicitly:
- `/dev-implement`
- `/dev-implement --mode=direct`
- `/dev-implement --mode=subagent`

## Prerequisites

**Required:**
- Tasks (`.shipkit/skills/dev-tasks/outputs/specs/NNN/tasks.md`)
- Constitution (`.shipkit/skills/dev-constitution/outputs/constitution.md`)

**Recommended:**
- Spec (`.shipkit/skills/dev-specify/outputs/specs/NNN/spec.md`)
- Plan (`.shipkit/skills/dev-plan/outputs/specs/NNN/plan.md`)

## Inputs

**From tasks.md:**
- Task list with dependencies
- [P] markers for parallel execution
- [US#] labels for user story tracking

**From constitution.md:**
- Technical standards
- Architectural patterns
- Coding conventions
- Testing requirements

**From spec.md (if exists):**
- User story acceptance criteria
- Functional requirements

**From plan.md (if exists):**
- Tech stack details
- File structure
- API contracts

## Process

### 1. Run Script

```bash
.shipkit/skills/dev-implement/scripts/start-implementation.sh specs/NNN
```

**Available flags:**
- `--mode=direct` - Force direct mode (single context)
- `--mode=subagent` - Force subagent mode (fresh context per task)

**Script behavior:**

The script determines execution mode based on task count:

**Task Count Analysis:**
- Reads tasks.md
- Counts total tasks
- **1-5 tasks:** Recommends direct mode (low overhead, fast)
- **6+ tasks:** Recommends subagent mode (fresh context per task)

**Mode Selection:**
- If flag provided → Use specified mode
- Otherwise → Ask user to choose mode

Script output:
- Display task count and complexity analysis
- Show mode recommendation
- Point to references for TDD, verification, debugging
- Ready for Claude

### 2. Read References

Read all files in the skill's references directory:
```bash
.shipkit/skills/dev-implement/references/
```

**If >2 files exist:** Ask the user which files are most relevant for this task.

This includes built-in guidance (reference.md, examples.md) and any user-added files (PDFs, research, notes).

---

### 3. Read Constitution FIRST

**MANDATORY - Read constitution before EVERY code write:**

```bash
# Read this BEFORE writing any code
.shipkit/skills/dev-constitution/outputs/constitution.md
```

**Constitution guides:**
- Which patterns to follow
- What coding standards apply
- Testing requirements
- Performance targets
- Security standards

**Red Flag:**
- Writing code without consulting constitution = violation
- "I'll check constitution later" = STOP, read it NOW

### 4. Read Task Context

**Read all available context:**

```bash
# Required
.shipkit/skills/dev-tasks/outputs/specs/NNN/tasks.md

# If exists
.shipkit/skills/dev-specify/outputs/specs/NNN/spec.md
.shipkit/skills/dev-plan/outputs/specs/NNN/plan.md
.shipkit/skills/dev-plan/outputs/specs/NNN/data-model.md
.shipkit/skills/dev-plan/outputs/specs/NNN/contracts/
```

**Also read extended references:**
```bash
.shipkit/skills/dev-implement/references/tdd-reference.md
.shipkit/skills/dev-implement/references/verification-reference.md
.shipkit/skills/dev-implement/references/debugging-reference.md
```

### 5. Execute Tasks with TDD Cycle

**For EACH task, follow RED-GREEN-REFACTOR:**

```
┌─────────────────────────────────────────────────────────────┐
│ 🔴 RED - Write Failing Test FIRST                          │
│ ─────────────────────────────────────────────────────────── │
│ • Consult constitution.md for testing patterns             │
│ • Write test that demonstrates desired behavior            │
│ • Run test → MUST FAIL (proving test works)                │
│ • If test passes immediately → test is wrong, fix it       │
│ • Never write production code before the test              │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 🟢 GREEN - Write Minimal Code to Pass                      │
│ ─────────────────────────────────────────────────────────── │
│ • Consult constitution.md for patterns to follow           │
│ • Write MINIMAL code that makes test pass                  │
│ • No extra features, no premature optimization             │
│ • Run test → MUST PASS                                     │
│ • Run ALL tests → MUST PASS (no regressions)               │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 🔵 REFACTOR - Clean Up While Tests Pass                    │
│ ─────────────────────────────────────────────────────────── │
│ • Validate against constitution.md standards               │
│ • Improve code structure                                   │
│ • Remove duplication                                        │
│ • Run tests → MUST STILL PASS                              │
└─────────────────────────────────────────────────────────────┘
```

**The Iron Law of TDD:**
```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over.

**When tests fail:** Use systematic debugging (see references/debugging-reference.md)

### 6. Two-Stage Code Review

**After TDD cycle completes, run BOTH reviews:**

#### Stage 1: Spec Compliance Review

**Check against spec.md requirements:**
- Does it match user story acceptance criteria?
- Nothing extra added (YAGNI)?
- Nothing missing from requirements?
- Follows constitution patterns?

**If issues found:**
→ Fix issues
→ Re-run spec compliance review
→ Repeat until compliant

#### Stage 2: Code Quality Review

**Check implementation quality:**
- Magic numbers/strings?
- Missing error handling?
- Poor naming?
- Unnecessary complexity?
- Constitution standards violated?

**If issues found:**
→ Fix issues (keep tests green)
→ Re-run code quality review
→ Repeat until approved

### 7. Verification Before Completion

**MANDATORY - Evidence before claims:**

```bash
# Run full test suite
npm test  # or pytest, go test, cargo test, etc.

# Capture the output
# Verify: All tests pass? (with evidence)
# Verify: No warnings/errors in output?
```

**ONLY THEN mark task complete.**

**Evidence requirements:**
- Fresh output (not cached/remembered)
- Complete output (not partial/summarized)
- Relevant to claim (tests pass = tests shown passing)

**Red Flags:**
- "Should be working now" (without running tests)
- "Looks good" (without verification)
- "Probably fixed" (without evidence)
- "Let me know if it works" (shifting verification to user)

**See:** `references/verification-reference.md` for details

### 8. Mode Selection

**Direct Mode (1-5 tasks):**
- Execute all tasks in single context
- Faster for small implementations
- Use when tasks are tightly coupled

**Subagent Mode (6+ tasks):**
- Fresh context per task
- Controller maintains overview
- Subagents focus on details
- Better for large implementations

**Script recommends mode, but user can override with flags.**

## Outputs

**Code artifacts:**
- Source code (in project directories)
- Tests (in project test directories)
- Git commits (incremental)

**NO outputs in .shipkit/** - Implementation produces project code, not skill artifacts.

## Constraints

- **MUST** read constitution.md BEFORE writing code
- **MUST** follow TDD cycle (RED-GREEN-REFACTOR)
- **MUST** run two-stage code review (spec + quality)
- **MUST** verify before claiming completion
- **NEVER** skip steps or take shortcuts
- **NO** "quick fixes" without root cause investigation
- **NO** completion claims without evidence

## Integration with Other Skills

**Automatically integrates:**

| Skill | Integration Point | Purpose |
|-------|-------------------|---------|
| **dev-test-driven-development** | Every task | Enforces RED-GREEN-REFACTOR |
| **dev-verification-before-completion** | Before marking done | Evidence before claims |
| **dev-systematic-debugging** | When tests fail | Root cause investigation |

**You don't invoke these separately - they're part of this workflow.**

## Execution Modes

### Direct Mode

**Single context execution:**

1. Read all context (tasks, spec, plan, constitution)
2. For each task:
   - 🔴 Write failing test
   - 🟢 Implement to pass
   - 🔵 Refactor
   - ✓ Spec compliance review
   - ✓ Code quality review
   - ✓ Verification
   - Mark task complete
3. Report progress after each task
4. Continue until all tasks complete

### Subagent Mode

**Fresh context per task:**

**Controller (you):**
1. Read all context
2. For each task:
   - Extract task details
   - Gather relevant context
   - Dispatch implementation subagent
   - Review subagent's work (spec compliance)
   - Review code quality
   - Verify and mark complete
   - Report progress

**Subagent prompt template:**
```
Implement this task using TDD:

Task: [full task text]
Context: [spec excerpts, plan details]
Constitution: [relevant standards]

Requirements:
1. Read constitution.md FIRST
2. Write failing test FIRST
3. Implement minimal code to pass
4. Refactor if needed
5. Commit your changes

Return: Summary + test results
```

## The Iron Rules

**TDD is NOT optional:**
- NO production code without a failing test first
- Code before test? Delete it. Start over.
- Test passes immediately? Test is wrong.

**Constitution compliance is NOT optional:**
- Read constitution.md BEFORE writing code
- Validate against standards DURING refactor
- Check compliance in code quality review

**Verification is NOT optional:**
- NO claiming "done" without running verification
- NO "should pass" - run the command, show the output
- Evidence before claims, always.

**Reviews are NOT optional:**
- Spec compliance review catches over/under-building
- Code quality review catches implementation issues
- Both must pass before marking task complete

## When Things Go Wrong

**Tests fail:**
1. Use systematic debugging (references/debugging-reference.md)
2. Find root cause BEFORE fixing
3. Create focused test for the bug
4. Fix root cause (not symptom)
5. Verify fix with evidence

**Can't complete task:**
1. Report blocker clearly
2. Suggest next steps
3. Don't skip or work around
4. Ask user for guidance

**3+ fix attempts fail:**
- Question the architecture
- Don't attempt fix #4
- Report to user for architectural review

## Next Steps

After all tasks complete:
- All tests passing (with verification output)
- All tasks marked [X] in tasks.md
- Ready for: `/dev-finish` (merge/PR workflow)

## Common Mistakes to Avoid

1. **Skipping constitution read** - "I'll check it later" → STOP, read NOW
2. **Code before test** - Delete it, start with failing test
3. **"Looks good" without evidence** - Run the command, show output
4. **Quick fixes without debugging** - Find root cause first
5. **Skipping reviews** - Both reviews required, no exceptions
6. **Constitution violations** - Validate against standards during refactor

## Reference Files

All files in `references/` are read when running this skill:

- **tdd-reference.md** - Complete TDD methodology (RED-GREEN-REFACTOR)
- **verification-reference.md** - Evidence-based completion
- **debugging-reference.md** - Root cause investigation
- **README.md** - Folder explanation

Add your own references to customize guidance.

## Context

This is the **execution skill** in the development pipeline.

**Workflow:**
```
dev-constitution → dev-specify → dev-plan → dev-tasks
                                              ↓
                                     dev-implement ← YOU ARE HERE
                                              ↓
                                         dev-finish
```

**Remember:** Constitution guides ALL decisions. Read it FIRST, reference it THROUGHOUT implementation.
