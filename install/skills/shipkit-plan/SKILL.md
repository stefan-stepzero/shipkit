---
name: shipkit-plan
description: "Use when a spec exists and user wants implementation steps. Triggers: 'how to implement', 'create plan', 'plan this', 'what are the steps'."
argument-hint: "[spec name]"
---

# shipkit-plan - Lightweight Implementation Planning

**Purpose**: Transform feature specifications into focused implementation plans that guide coding while staying lightweight for POC/MVP work.

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

**Token budget**: Keep context reading under 2000 tokens.

---

### Step 2.5: Architecture Anti-Pattern Check (CRITICAL)

**Before generating plan, check for architecture anti-patterns.**

**Reference**: See `shipkit-spec/references/best-practices.md` → "Architecture Patterns"

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

**Location**: `.shipkit/plans/active/[feature-name]-plan.md`

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
1. Run `implement (no skill needed)` to start coding
2. Follow TDD-lite approach
```

---

### Step 4: Log Decision (if significant)

**If plan makes architectural decision**, offer to log it via `/shipkit-architecture-memory`

---

### Step 5: Suggest Next Step

**Output to user**: Summary of plan location, steps count, files to create/modify, complexity, estimated effort.

---

## Completion Checklist

Copy and track:
- [ ] Read spec from `.shipkit/specs/active/`
- [ ] Created step-by-step implementation plan
- [ ] Identified files to create/modify
- [ ] Saved to `.shipkit/plans/active/[name]-plan.md`

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
- If questioning WHAT to build → Go back to `/shipkit-spec`
- Plan is technical roadmap, not requirements document

**The fix**: Before planning, read the spec. Plan what's in the spec. Nothing more.

---

## When This Skill Integrates with Others

### Before This Skill
- `/shipkit-spec` - Creates feature specification
- `/shipkit-project-context` - Generates stack.md, schema.md
- `/shipkit-architecture-memory` - Logs past decisions

### After This Skill
- `implement (no skill needed)` - Executes the plan with TDD-lite
- `/shipkit-architecture-memory` - Logs significant decisions (optional)

---

## Context Files This Skill Reads

**Always reads**:
- `.shipkit/specs/active/[feature].md` - Feature requirements
- `.shipkit/stack.md` - Tech stack info

**Conditionally reads**:
- `.shipkit/architecture.md` - Past decisions
- `.shipkit/types.md` - Type definitions
- `.shipkit/schema.md` - Database schema

---

## Context Files This Skill Writes

**Creates**:
- `.shipkit/plans/active/[feature]-plan.md` - Implementation plan

**Write Strategy**: **OVERWRITE AND REPLACE**

**Rationale**: Each plan is feature-specific and tied to a single spec. If user re-plans the same feature, they want a fresh plan based on current context.

**Never modifies**: Specs, stack, architecture (read-only)

---

## Lazy Loading Behavior

**This skill loads context ON DEMAND**:

1. User invokes `/shipkit-plan`
2. Claude asks user which spec to plan
3. Claude reads only relevant spec + stack
4. Claude optionally reads architecture/types if needed
5. Claude generates plan
6. Context loaded: ~1500-2500 tokens (focused)

---

<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Has important context been saved to `.shipkit/`?
2. **Prerequisites** - Does the next action need a spec or plan first?
3. **Session length** - Long session? Consider `/shipkit-work-memory` for continuity.

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