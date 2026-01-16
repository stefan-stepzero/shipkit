---
name: lite-plan
description: "Use when a spec exists and user wants implementation steps. Triggers: 'how to implement', 'create plan', 'plan this', 'what are the steps'."
---

# plan-lite - Lightweight Implementation Planning

**Purpose**: Transform feature specifications into focused implementation plans that guide coding while staying lightweight for POC/MVP work.

---

## When to Invoke

**User triggers**:
- "Plan how to build this"
- "Create implementation plan"
- "How should we implement this feature?"
- "Design the technical approach"

**After**:
- `/lite-spec` has created specification for the feature
- Feature is ready for implementation planning

---

## Prerequisites

**Check before starting**:
- Spec exists: `.shipkit-lite/specs/active/[feature-name].md`
- Stack defined: `.shipkit-lite/stack.md` (from project-context-lite)

**UI-Heavy Feature Check** (CRITICAL):
- If spec describes significant UI/UX → Prototype MUST exist before planning
- Check: `.shipkit-mockups/[feature-name]/` OR spec contains `## UI/UX Patterns` section
- See "Step 1.5: UI-Heavy Gate" below

**Optional but helpful**:
- Architecture decisions: `.shipkit-lite/architecture.md`
- Type definitions: `.shipkit-lite/types.md`

---

## Process

### Step 1: Confirm Scope

**Before generating anything**, ask user 2-3 questions:

1. **Which spec are you planning?** (List available specs from `.shipkit-lite/specs/active/`)
2. **Implementation approach?** ("What's your preferred approach?" if multiple options exist)
3. **Complexity level?** ("Quick POC plan or detailed plan?")

---

### Step 1.5: UI-Heavy Gate (CRITICAL)

**Before proceeding to planning, check if spec is UI-heavy.**

**UI-heavy indicators** (if 3+ found): form, modal, table, grid, dashboard, navigation, animation, drag/drop, chart, upload

**Decision logic:**
- UI-heavy + No prototype → BLOCK - Require prototype first
- UI-heavy + Prototype exists → Proceed to Step 2
- Not UI-heavy → Proceed to Step 2

**If BLOCKED**: Suggest `/lite-prototyping` or let user skip with acknowledgment of risk.

---

### Step 2: Read Existing Context

**Read these files to understand project context**:
- `.shipkit-lite/specs/active/[feature-name].md` (Required)
- `.shipkit-lite/stack.md` (Stack info)
- `.shipkit-lite/architecture.md` (Past decisions)

**Optional context** (load if relevant): types.md, component-contracts.md, schema.md

**Token budget**: Keep context reading under 2000 tokens.

---

### Step 2.5: Architecture Anti-Pattern Check (CRITICAL)

**Before generating plan, check for architecture anti-patterns.**

**Reference**: See `lite-spec/references/best-practices.md` → "Architecture Patterns"

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

### Step 3: Generate Implementation Plan

**Create plan file using Write tool**:

**Location**: `.shipkit-lite/plans/active/[feature-name]-plan.md`

**Plan structure**:

```markdown
# Implementation Plan - [Feature Name]

**Created**: [timestamp]
**Spec**: specs/active/[feature-name].md
**Status**: Planning

---

## Overview

**Goal**: [1-2 sentence summary]
**Complexity**: [Simple/Medium/Complex]
**Estimated effort**: [X hours/days]

---

## Tech Stack Alignment

**From stack.md:** Framework, Database, Key libraries
**Patterns from architecture.md:** [Patterns to follow]

---

## Implementation Steps

### Phase 1: Setup
- [ ] [Setup tasks - include centralized patterns if missing]

### Phase 2: Core Implementation
- [ ] [Core tasks]

### Phase 3: Integration
- [ ] [Integration tasks]

### Phase 4: Testing
- [ ] [Test tasks]

---

## Data Model Changes

**New/Modified entities:** [List]
**Database changes needed:** [Migrations]

---

## File Structure

**Modularity check:**
- [ ] Each file < 200 lines
- [ ] Types in separate files
- [ ] No circular dependencies

**New files:** [List with paths]
**Files to modify:** [List with paths]

---

## Key Decisions

**Decision 1**: [What/Why/Alternative not chosen]

---

## Acceptance Criteria

From spec.md: [List]

---

## Potential Gotchas

- [Gotcha]: [How to avoid]

---

## Next Steps

After plan approval:
1. Run `/lite-implement` to start coding
2. Follow TDD-lite approach
```

---

### Step 4: Log Decision (if significant)

**If plan makes architectural decision**, offer to log it via `/lite-architecture-memory`

---

### Step 5: Suggest Next Step

**Output to user**: Summary of plan location, steps count, files to create/modify, complexity, estimated effort.

---

## Completion Checklist

Copy and track:
- [ ] Read spec from `.shipkit-lite/specs/active/`
- [ ] Created step-by-step implementation plan
- [ ] Identified files to create/modify
- [ ] Saved to `.shipkit-lite/plans/active/[name]-plan.md`

---

## What Makes This "Lite"

**Included**:
- Step-by-step implementation guide
- References existing context (stack, architecture)
- File structure planning
- Key technical decisions

**Not included** (vs full dev-plan):
- Research phase (no unknowns investigation)
- API contracts (OpenAPI/GraphQL schemas)
- Detailed data model design
- Performance benchmarks
- Security threat modeling

**Philosophy**: Good enough plan to start coding, not exhaustive design doc.

---

## The Iron Law

**PLANS ANSWER "HOW", NOT "WHY" OR "WHAT"**

- Plan assumes spec already defined the "what" and "why"
- Plan focuses solely on "how" (implementation approach, file structure, steps)
- If questioning WHAT to build → Go back to `/lite-spec`
- Plan is technical roadmap, not requirements document

**The fix**: Before planning, read the spec. Plan what's in the spec. Nothing more.

---

## When This Skill Integrates with Others

### Before This Skill
- `/lite-spec` - Creates feature specification
- `/lite-project-context` - Generates stack.md, schema.md
- `/lite-architecture-memory` - Logs past decisions

### After This Skill
- `/lite-implement` - Executes the plan with TDD-lite
- `/lite-architecture-memory` - Logs significant decisions (optional)

---

## Context Files This Skill Reads

**Always reads**:
- `.shipkit-lite/specs/active/[feature].md` - Feature requirements
- `.shipkit-lite/stack.md` - Tech stack info

**Conditionally reads**:
- `.shipkit-lite/architecture.md` - Past decisions
- `.shipkit-lite/types.md` - Type definitions
- `.shipkit-lite/schema.md` - Database schema

---

## Context Files This Skill Writes

**Creates**:
- `.shipkit-lite/plans/active/[feature]-plan.md` - Implementation plan

**Write Strategy**: **OVERWRITE AND REPLACE**

**Rationale**: Each plan is feature-specific and tied to a single spec. If user re-plans the same feature, they want a fresh plan based on current context.

**Never modifies**: Specs, stack, architecture (read-only)

---

## Lazy Loading Behavior

**This skill loads context ON DEMAND**:

1. User invokes `/lite-plan`
2. Claude asks user which spec to plan
3. Claude reads only relevant spec + stack
4. Claude optionally reads architecture/types if needed
5. Claude generates plan
6. Context loaded: ~1500-2500 tokens (focused)

---

<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Has important context been saved to `.shipkit-lite/`?
2. **Prerequisites** - Does the next action need a spec or plan first?
3. **Session length** - Long session? Consider `/lite-work-memory` for continuity.

**Natural capabilities** (no skill needed): Implementation, debugging, testing, refactoring, code documentation.

**Suggest skill when:** User needs to make decisions, create persistence, or check project status.
<!-- /SECTION:after-completion -->

<!-- SECTION:success-criteria -->
## Success Criteria

Plan is complete when:
- [ ] All implementation steps identified
- [ ] File structure defined
- [ ] Database changes documented
- [ ] Key decisions explained
- [ ] References existing patterns from architecture.md
- [ ] Respects tech stack from stack.md
- [ ] Acceptance criteria from spec included
<!-- /SECTION:success-criteria -->
---

**Remember**: This is a POC/MVP plan. Get something working, then refine. Don't spend hours planning what you could learn in minutes of coding.
