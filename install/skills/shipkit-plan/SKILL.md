---
name: shipkit-plan
description: "Use when a spec exists and user wants implementation steps. Triggers: 'how to implement', 'create plan', 'plan this', 'what are the steps'."
argument-hint: "[spec name]"
model: opus
agent: shipkit-architect-agent
---

# shipkit-plan - Implementation Planning with Failure Mode Prevention

**Purpose**: Transform feature specifications into validated implementation plans that prevent common planning failures: orphaned foundations, magical steps, codebase blindness, and incomplete coverage.

---

## When to Invoke

**User triggers**:
- "Plan how to build this"
- "Create implementation plan"
- "How should we implement this feature?"
- "Design the technical approach"

**After**:
- `/shipkit-spec` has created specification for the feature
- Feature is ready for implementation planning

---

## Prerequisites

**Check before starting**:
- Spec exists: `.shipkit/specs/active/[feature-name].md`
- Stack defined: `.shipkit/stack.md` (from shipkit-project-context)

**UI-Heavy Feature Check** (CRITICAL):
- If spec describes significant UI/UX → Prototype MUST exist before planning
- Check: `.shipkit-mockups/[feature-name]/` OR spec contains `## UI/UX Patterns` section
- See "Step 1.5: UI-Heavy Gate" below

**Optional but helpful**:
- Architecture decisions: `.shipkit/architecture.md`
- Type definitions: `.shipkit/types.md`

---

## Process

**Subagent Principle**: Use Explore subagents for codebase scanning and verification tasks. They're faster, use less context, and return focused results. See Steps 2.7 and 3 for specific subagent prompts.

---

### Step 1: Confirm Scope

**First, scan available specs:**
```bash
ls .shipkit/specs/active/*.md 2>/dev/null || echo "No specs found"
```

**Then use AskUserQuestion tool:**

**Question 1 - Spec Selection:** (if multiple specs exist)
```
header: "Spec"
question: "Which spec are you planning?"
options:
  - (dynamically list spec files found)
```

**Question 2 - Plan Detail:**
```
header: "Detail"
question: "What level of planning do you need?"
options:
  - label: "Quick POC (Recommended)"
    description: "Minimal steps, get something working fast"
  - label: "Standard"
    description: "Balanced detail, covers major concerns"
  - label: "Detailed"
    description: "Comprehensive plan with alternatives"
```

**If user selects "Other"**: Ask clarifying questions about their specific needs.

---

### Step 1.5: UI-Heavy Gate (CRITICAL)

**Before proceeding to planning, check if spec is UI-heavy.**

**UI-heavy indicators** (if 3+ found): form, modal, table, grid, dashboard, navigation, animation, drag/drop, chart, upload

**Decision logic:**
- UI-heavy + No prototype → BLOCK - Require prototype first
- UI-heavy + Prototype exists → Proceed to Step 2
- Not UI-heavy → Proceed to Step 2

**If BLOCKED**: Suggest `/shipkit-prototyping` or let user skip with acknowledgment of risk.

---

### Step 2: Read Existing Context

**Read these files to understand project context**:
- `.shipkit/specs/active/[feature-name].md` (Required)
- `.shipkit/stack.md` (Stack info)
- `.shipkit/architecture.md` (Past decisions)

**Optional context** (load if relevant): types.md, component-contracts.md, schema.md

**Extract from spec:**
- All requirements (for coverage mapping later)
- Acceptance criteria
- Integration points mentioned

**Token budget**: Keep context reading under 2000 tokens.

---

### Step 2.5: Architecture Anti-Pattern Check

**Before generating plan, check for architecture anti-patterns.**

**Reference**: See `shipkit-spec/references/best-practices.md` for frontend/backend patterns.

**Quick checks:**
1. **Auth**: Does spec mention auth? Is centralized auth in place? If not, add to Phase 1.
2. **Error Handling**: Global error boundary exists? If not, add to Phase 1.
3. **Data Fetching**: Shared data needed? Provider pattern exists? If not, add to Phase 1.

**Pattern Checklist** (ensure these exist or will be created in Phase 1):
- Auth: Centralized middleware/layout
- Errors: Global error boundary
- Data: Provider pattern (if needed)
- Config: Env validation
- API Response: Consistent format

---

### Step 2.7: Codebase Pattern Scan (CRITICAL - Prevents Codebase Blindness)

**Before proposing ANY pattern, verify what the codebase actually uses.**

**Why this matters**: Claude defaults to training data patterns. If codebase uses SWR but Claude proposes React Query, the plan creates inconsistency and technical debt.

**USE SUBAGENT FOR THIS STEP** - Launch an Explore subagent to scan the codebase efficiently:

```
Task tool with subagent_type: "Explore"
Prompt: "Scan codebase for existing patterns. Find and report:
1. State management pattern (useState/useReducer/Redux/Zustand/Jotai/signals)
2. Data fetching pattern (fetch/axios/SWR/React Query/tRPC)
3. Error handling pattern (ErrorBoundary/try-catch/error middleware)
4. Auth pattern (session/JWT/middleware/protected routes)
5. Component structure pattern (feature folders/atomic/etc)

For each, provide: pattern name, example file path, brief code snippet showing usage.
Be thorough - check multiple directories."
```

**Why subagent**:
- Explore agent is optimized for codebase scanning
- Reduces context usage in main conversation
- Can search multiple patterns in parallel
- Returns focused summary instead of raw grep output

**Fallback** (if subagent unavailable): Manual grep commands:
```bash
# State management
grep -r "useReducer\|create.*Store\|configureStore" --include="*.ts" --include="*.tsx" -l | head -3

# Data fetching
grep -r "useSWR\|useQuery\|createApi" --include="*.ts" --include="*.tsx" -l | head -3

# Error handling
grep -r "ErrorBoundary\|onError\|handleError" --include="*.ts" --include="*.tsx" -l | head -3
```

**After subagent returns**, read 1-2 representative files if more detail needed.

**Record findings** (will go into plan):
| Concern | Pattern Found | Example File |
|---------|---------------|--------------|
| State | [e.g., Zustand] | [file path] |
| Data fetching | [e.g., SWR] | [file path] |
| Error handling | [e.g., ErrorBoundary] | [file path] |
| Auth | [e.g., JWT middleware] | [file path] |
| Components | [e.g., feature folders] | [file path] |

**Iron rule:** Plan MUST use patterns found here. If codebase uses pattern X, plan uses pattern X. No exceptions without explicit justification.

---

### Step 3: Generate Implementation Plan

**Create plan file using Write tool**:

**Location**: `.shipkit/plans/active/[feature-name]-plan.md`

**During generation, apply these rules:**

1. **Existence Verification**: Before referencing ANY existing code ("use the UserService", "extend the auth middleware"):
   - Read or Grep to confirm it exists
   - If not found: add creation step to plan
   - Never assume code exists without verification

   **For multiple references** (3+ existing files/functions to verify), use Explore subagent:
   ```
   Task tool with subagent_type: "Explore"
   Prompt: "Verify these code artifacts exist and return their locations:
   1. [UserService or similar]
   2. [Auth middleware]
   3. [Error handler]
   For each: confirm exists (yes/no), file path, brief description of what it does."
   ```

2. **Granularity Check**: Each step must be:
   - Completable in < 2 hours
   - Have a clear done state
   - NOT be a project in disguise

   **Red flag phrases that need decomposition:**
   - "Implement authentication" → Break into: create token util, add middleware, add login endpoint, etc.
   - "Set up testing" → Break into: install deps, create first test file, add test script
   - "Add error handling" → Break into: create error boundary, add to layout, create error types
   - "Create API layer" → Break into: create fetch wrapper, add first endpoint, add types

3. **Consumption Requirement**: Every artifact created must have a consumer defined in the same plan.

4. **Permission Pre-declaration**: Track all actions that will need permission during implementation:
   - Count files to create vs modify
   - List bash commands that will run (tests, build, migrations)
   - Note any new dependencies to install
   - This populates the "Implementation Permissions" section

**Plan structure:**

```markdown
# Implementation Plan - [Feature Name]

**Created**: [timestamp]
**Spec**: specs/active/[feature-name].md
**Status**: Planning

---

## Overview

**Goal**: [1-2 sentence summary from spec]
**Complexity**: [Simple/Medium/Complex]

---

## Codebase Patterns (from Step 2.7 scan)

| Concern | Current Pattern | Source File | Plan Will Use |
|---------|-----------------|-------------|---------------|
| State | [pattern] | [file] | [same pattern] |
| Data fetching | [pattern] | [file] | [same pattern] |
| Error handling | [pattern] | [file] | [same pattern] |
| Auth | [pattern] | [file] | [same pattern] |

**Pattern divergence**: [None / If diverging, explain why]

---

## Implementation Phases

### Phase 1: [Name]

**Gate**: [Specific testable condition - command to run OR behavior to verify]

| Step | Description | Creates | Consumed By |
|------|-------------|---------|-------------|
| 1.1 | [Specific actionable task] | [Artifact: file, function, type] | [File:function OR Step X.Y] |
| 1.2 | [Specific actionable task] | [Artifact] | [Consumer] |

### Phase 2: [Name]

**Gate**: [Specific testable condition]

| Step | Description | Creates | Consumed By |
|------|-------------|---------|-------------|
| 2.1 | [Specific actionable task] | [Artifact] | [Consumer] |
| 2.2 | [Specific actionable task] | [Artifact] | [Consumer] |

### Phase 3: [Name]

**Gate**: [Specific testable condition]

| Step | Description | Creates | Consumed By |
|------|-------------|---------|-------------|
| 3.1 | [Specific actionable task] | [Artifact] | [Consumer] |

[Continue for all phases needed...]

---

## Consumption Map

**Purpose**: Verify no orphaned foundations - everything created is used.

| Creates | Type | Consumed By | Status |
|---------|------|-------------|--------|
| [Artifact 1] | [file/function/type/config] | [Specific consumer] | ✓ |
| [Artifact 2] | [file/function/type/config] | [Specific consumer] | ✓ |
| [Every artifact from all phases...] | | | |

**Orphan check**: [0 orphans ✓ / X orphans - MUST FIX BEFORE PROCEEDING]

---

## Spec Coverage Map

**Purpose**: Verify plan addresses all spec requirements.

| Spec Requirement | Plan Step(s) | Status |
|------------------|--------------|--------|
| [Requirement 1 from spec] | Phase X, Step Y | ✓ |
| [Requirement 2 from spec] | Phase X, Step Y | ✓ |
| [Every requirement from spec...] | | |

**Coverage check**: [X/X requirements mapped ✓ / X unmapped - MUST FIX]

---

## Phase Gates Summary

**Purpose**: Ensure each phase has verifiable completion criteria.

| Phase | Gate Condition | Verification Method |
|-------|----------------|---------------------|
| 1 | [Specific condition] | [Command: `npm test` / Manual: check X in browser] |
| 2 | [Specific condition] | [Command / Manual check] |
| 3 | [Specific condition] | [Command / Manual check] |

**Gate quality check**: All gates are specific and testable ✓

**Bad gates** (never use these):
- "Setup complete" → Instead: "`npm run dev` starts without errors"
- "Core done" → Instead: "User can see login form at /login"
- "It works" → Instead: "Token appears in localStorage after successful login"

---

## Files

**New files to create:**
- [path/to/file.ts] - [purpose]
- [path/to/file.ts] - [purpose]

**Existing files to modify** (verified to exist):
- [path/to/file.ts] - [what changes]
- [path/to/file.ts] - [what changes]

---

## Implementation Permissions

**Actions needed to execute this plan** (pre-declare for smoother implementation):

| Category | Actions | Scope |
|----------|---------|-------|
| Create files | [X] new files | [list paths] |
| Modify files | [X] existing files | [list paths] |
| Run commands | [list: tests, build, lint, etc.] | [specific commands if known] |
| Database | [migrations, seeds, etc.] | [migration names if known] |
| Install deps | [if any new deps needed] | [package names] |

**Why this matters**: Approving the plan pre-grants these permission categories, avoiding constant prompts during implementation. User sees full scope upfront.

---

## Key Decisions

**Decision 1**: [What decision / Why this choice / What alternative was considered]

[Only if plan makes architectural decisions or diverges from existing patterns]

---

## Validation Summary

```
Consumption:      X creates, X consumed, 0 orphans ✓
Granularity:      X steps, 0 oversized ✓
Existence:        X references to existing code, X verified ✓
Phase gates:      X phases, X testable gates ✓
Spec coverage:    X/X requirements mapped ✓
Pattern alignment: Aligned with codebase ✓
Permissions:      X new files, X modified, X commands declared ✓
```

**Plan status**: VALID - Ready for implementation
```

---

### Step 3.5: Plan Validation Gate (CRITICAL - Do Not Skip)

**Before outputting plan, run all validation checks.**

#### Check 1: Consumption Tracing (Prevents Orphaned Foundations)

Review Consumption Map:
- [ ] Every "Creates" has specific artifact (not vague like "setup")
- [ ] Every "Consumed By" references specific location (file:function) or step (Phase X.Y)
- [ ] Zero rows have empty or vague "Consumed By"

**If orphan found**:
- Option A: Add a step that consumes the artifact
- Option B: Remove the creation step (it's not needed)
- Option C: The artifact is an entry point (API endpoint, CLI command, UI page) - mark as "Entry point"

**Never proceed with orphans.**

#### Check 2: Granularity Validation (Prevents Magical Steps)

Review every step:
- [ ] Each step completable in < 2 hours
- [ ] Each step has clear, unambiguous done state
- [ ] No step is a project disguised as a task

**Red flags to find and decompose:**
- "Implement [feature]" - What specific files/functions?
- "Set up [system]" - What specific configuration steps?
- "Add [broad capability]" - What specific components?
- "Create [layer]" - What specific modules?

**If oversized step found**: Decompose into 2-5 specific sub-steps.

#### Check 3: Existence Verification (Prevents Dependency Assumptions)

Review every reference to existing code:
- [ ] File paths verified via Read or Grep during Step 3
- [ ] If file not found, creation step added to plan
- [ ] No assumptions about existing code structure

**Common dangerous assumptions:**
- "Extend the existing UserService" - Does UserService exist?
- "Add to the utils folder" - Is there a utils folder? What's the pattern?
- "Use the auth middleware" - Does auth middleware exist? Where?

**If unverified reference found**: Verify now or add creation step.

#### Check 4: Phase Gate Quality (Prevents Missing Checkpoints)

Review Phase Gates Summary:
- [ ] Every phase has a gate
- [ ] Every gate is testable (can run command or check specific behavior)
- [ ] No vague gates ("done", "complete", "works")

**Gate test**: Could a different developer verify this gate passed? If no, make it more specific.

#### Check 5: Spec Coverage (Prevents Incomplete Plans)

Review Spec Coverage Map:
- [ ] Every requirement from spec has at least one plan step
- [ ] No spec requirements left unmapped
- [ ] Coverage is genuine (step actually addresses requirement, not just tangentially related)

**If gap found**:
- Add missing steps
- Or flag that spec requirement is out of scope (explicit decision)

#### Check 6: Pattern Alignment (Prevents Codebase Blindness)

Review Codebase Patterns table:
- [ ] Every "Plan Will Use" matches "Current Pattern"
- [ ] If diverging, explicit justification provided
- [ ] No training-data patterns introduced without verification

**Validation output** (include in plan):
```
Consumption:      [X] creates, [X] consumed, [0] orphans [✓/✗]
Granularity:      [X] steps, [0] oversized [✓/✗]
Existence:        [X] references, [X] verified [✓/✗]
Phase gates:      [X] phases, [X] testable [✓/✗]
Spec coverage:    [X]/[X] requirements [✓/✗]
Pattern alignment: [Aligned/Divergence justified] [✓/✗]
Permissions:      [X] new files, [X] modified, [X] commands [✓/✗]
```

**If ANY check fails**: Fix before proceeding. Do not output plan with known failures.

---

### Step 4: Log Decision (if significant)

**If plan makes architectural decision**, offer to log it via `/shipkit-architecture-memory`

---

### Step 5: Suggest Next Step

**Output to user**:
- Plan location
- Summary: X phases, Y steps, Z files to create/modify
- Validation status (all checks passing)
- Next action: "Ready to implement - start with Phase 1"

---

## Completion Checklist

Copy and track:
- [ ] Read spec from `.shipkit/specs/active/`
- [ ] Completed codebase pattern scan
- [ ] Created plan with all required sections
- [ ] Consumption map has zero orphans
- [ ] All steps are granular (< 2 hours each)
- [ ] All existing code references verified
- [ ] All phases have testable gates
- [ ] All spec requirements mapped to steps
- [ ] Pattern alignment confirmed
- [ ] Saved to `.shipkit/plans/active/[name]-plan.md`

---

## What Makes This Plan Robust

**Failure modes prevented:**

| Failure Mode | Prevention Mechanism |
|--------------|---------------------|
| Orphaned foundations | Consumption Map + Check 1 |
| Magical steps | Granularity rules + Check 2 |
| Codebase blindness | Pattern Scan (Step 2.7) + Check 6 |
| Dependency assumptions | Existence Verification + Check 3 |
| Missing checkpoints | Phase Gates + Check 4 |
| Incomplete coverage | Spec Coverage Map + Check 5 |

**What's NOT included** (vs full design doc):
- Research phase (no unknowns investigation)
- API contracts (OpenAPI/GraphQL schemas)
- Detailed data model design
- Performance benchmarks
- Security threat modeling

**Philosophy**: Validated plan that catches common failures, not exhaustive design doc.

---

## The Iron Laws

**LAW 1: PLANS ANSWER "HOW", NOT "WHY" OR "WHAT"**
- Plan assumes spec defined "what" and "why"
- If questioning WHAT to build → Go back to `/shipkit-spec`

**LAW 2: NO ORPHANS**
- Every artifact created must be consumed
- If nothing uses it, don't create it

**LAW 3: NO MAGIC**
- Every step must be specific and actionable
- If you can't explain exactly what to do, decompose further

**LAW 4: VERIFY, DON'T ASSUME**
- Before referencing existing code, prove it exists
- Before proposing a pattern, check what codebase uses

**LAW 5: GATES MUST BE TESTABLE**
- If you can't verify a phase is complete, the gate is bad
- Another developer should be able to check the gate

---

## When This Skill Integrates with Others

### Before This Skill
- `/shipkit-spec` - Creates feature specification (required)
- `/shipkit-project-context` - Generates stack.md, schema.md
- `/shipkit-architecture-memory` - Logs past decisions
- `/shipkit-prototyping` - Creates UI prototypes (if UI-heavy)

### After This Skill
- `implement (no skill needed)` - Executes the plan
- `/shipkit-architecture-memory` - Logs significant decisions (optional)
- `/shipkit-verify` - Validates implementation matches plan

---

## Context Files This Skill Reads

**Always reads**:
- `.shipkit/specs/active/[feature].md` - Feature requirements
- `.shipkit/stack.md` - Tech stack info

**Scans** (for pattern detection):
- Existing source files matching patterns (state, fetch, error, auth)

**Conditionally reads**:
- `.shipkit/architecture.md` - Past decisions
- `.shipkit/types.md` - Type definitions
- `.shipkit/schema.md` - Database schema

---

## Context Files This Skill Writes

**Creates**:
- `.shipkit/plans/active/[feature]-plan.md` - Validated implementation plan

**Write Strategy**: **OVERWRITE AND REPLACE**

**Rationale**: Each plan is feature-specific and tied to a single spec. If user re-plans the same feature, they want a fresh plan based on current context.

**Never modifies**: Specs, stack, architecture (read-only)

---

<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Plan saved to `.shipkit/plans/active/`
2. **Validation** - All 6 checks passing
3. **Prerequisites** - Implementation can start with Phase 1

**Natural capabilities** (no skill needed): Implementation, debugging, testing, refactoring, code documentation.

**Suggest skill when:** User needs to make decisions, create persistence, or check project status.
<!-- /SECTION:after-completion -->

<!-- SECTION:success-criteria -->
## Success Criteria

Plan is complete when:
- [ ] Codebase pattern scan completed
- [ ] All implementation steps identified with Creates/Consumed By
- [ ] Consumption map has zero orphans
- [ ] All steps are granular (< 2 hours)
- [ ] All existing code references verified
- [ ] Every phase has testable gate
- [ ] Every spec requirement maps to step(s)
- [ ] Patterns align with codebase
- [ ] Implementation permissions declared (files, commands, deps)
- [ ] Validation summary shows all checks passing
<!-- /SECTION:success-criteria -->

---

**Remember**: A validated plan catches failures before they happen. The 15 minutes spent on validation saves hours of rework from orphaned foundations, missing pieces, and codebase conflicts.
