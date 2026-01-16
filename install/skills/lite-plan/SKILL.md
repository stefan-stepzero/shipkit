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

1. **Which spec are you planning?**
   - List available specs from `.shipkit-lite/specs/active/`
   - Let user choose

2. **Implementation approach?**
   - "What's your preferred approach?" (if multiple options exist)
   - "Any specific patterns you want to use?"

3. **Complexity level?**
   - "Quick POC plan (minimal steps)?"
   - "Detailed plan (more thorough)?"

**Why ask first**: Avoid token-heavy generation if user wants different approach.

---

### Step 1.5: UI-Heavy Gate (CRITICAL)

**Before proceeding to planning, check if spec is UI-heavy.**

**Scan spec for UI keywords:**
```
UI-heavy indicators (if 3+ found, spec is UI-heavy):
- form, forms, input, field, validation
- modal, dialog, popup, drawer, sidebar
- table, list, grid, card, dashboard
- button, toggle, switch, checkbox, dropdown
- navigation, menu, tabs, breadcrumb
- layout, responsive, mobile, desktop
- animation, transition, loading, skeleton
- drag, drop, resize, sortable
- chart, graph, visualization
- upload, preview, gallery, carousel
```

**Check for existing prototype:**
```bash
# Check for prototype folder
ls .shipkit-mockups/[feature-name]*/index.html 2>/dev/null

# OR check if spec already has UI/UX section (from lite-prototype-to-spec)
grep -l "## UI/UX Patterns" .shipkit-lite/specs/active/[feature-name].md
```

**Decision logic:**

| UI-Heavy? | Prototype Exists? | Action |
|-----------|-------------------|--------|
| No | - | ✅ Proceed to Step 2 |
| Yes | Yes (folder or UI/UX section) | ✅ Proceed to Step 2 |
| Yes | No | ⛔ BLOCK - Require prototype first |

**If BLOCKED (UI-heavy + no prototype):**

```
⚠️  UI-Heavy Feature Detected

This spec describes significant UI/UX:
- Found: [list UI keywords found]

Before planning, you should validate the UI with a prototype.

**Why this matters:**
- UI assumptions are often wrong
- Prototyping takes 30 min, rebuilding takes days
- Users reveal issues immediately when they see mockups

**Options:**
1. Run `/lite-prototyping` now (recommended)
   → Creates HTML mockup with React + Tailwind
   → Iterate with user watching
   → Extract learnings with `/lite-prototype-to-spec`
   → Then return to `/lite-plan`

2. Skip prototype (user takes responsibility)
   → Acknowledge: "I accept risk of UI rework"
   → Proceed to planning

Which option? (1/2)
```

**If user chooses "1":** Stop and invoke `/lite-prototyping`
**If user chooses "2":** Log warning in plan, proceed with caution

**Log in plan if skipped:**
```markdown
## ⚠️ UI Prototype Skipped

User chose to skip UI prototyping for this UI-heavy feature.
Risk: May require significant UI rework during implementation.
```

---

### Step 2: Read Existing Context

**Read these files to understand project context**:

```bash
# Required
.shipkit-lite/specs/active/[feature-name].md

# Stack info (tech choices)
.shipkit-lite/stack.md

# Past decisions (patterns established)
.shipkit-lite/architecture.md
```

**Optional context** (load if relevant):
```bash
# Type definitions (if data-heavy feature)
.shipkit-lite/types.md

# Component contracts (if building on existing)
.shipkit-lite/component-contracts.md

# Schema (if database changes needed)
.shipkit-lite/schema.md
```

**Token budget**: Keep context reading under 2000 tokens.

---

### Step 2.5: Architecture Anti-Pattern Check (CRITICAL)

**Before generating plan, check for architecture anti-patterns that will cause rework.**

**Reference**: See `lite-spec/references/best-practices.md` → "Architecture Patterns (DRY & Centralization)"

**Scan spec and codebase for these patterns:**

#### 1. Auth Pattern Check

**Scan for**: Does spec mention auth/protected routes?

```bash
# Check if project has centralized auth
grep -r "middleware" src/ --include="*.ts" --include="*.tsx" | head -5
grep -r "ProtectedLayout\|AuthProvider\|useAuth" src/ --include="*.tsx" | head -5
```

**Decision logic:**

| Spec Mentions Auth? | Centralized Auth Exists? | Action |
|---------------------|-------------------------|--------|
| No | - | ✅ Proceed |
| Yes | Yes (middleware/layout) | ✅ Proceed |
| Yes | No | ⚠️ WARN: Add auth setup to plan Phase 1 |

**If no centralized auth:**
```
⚠️  Auth Anti-Pattern Risk

This feature requires authentication, but no centralized auth found.

**Risk**: Per-page auth checks → patching every page later

**Recommendation**: Add to plan Phase 1:
1. Create auth middleware OR protected layout
2. Define protected route patterns
3. Then implement feature

Add centralized auth to plan? (Y/n)
```

---

#### 2. Error Handling Pattern Check

**Scan for**: Does spec mention error states?

```bash
# Check if project has global error boundary
grep -r "error\.tsx\|ErrorBoundary" src/ --include="*.tsx" | head -3
```

**If no global error boundary:**
```
⚠️  Error Handling Anti-Pattern Risk

No global error boundary found.

**Risk**: Scattered try/catch → inconsistent error UI

**Recommendation**: Add to plan Phase 1:
1. Create app/error.tsx (Next.js) or ErrorBoundary component
2. Add Sentry/logging integration
3. Then implement feature

Add error boundary to plan? (Y/n)
```

---

#### 3. Data Fetching Pattern Check

**Scan for**: Does spec mention fetching same data in multiple places?

```bash
# Check for existing providers/contexts
grep -r "createContext\|Provider\|useSWR\|useQuery" src/ --include="*.tsx" | head -5
```

**If spec needs shared data but no provider exists:**
```
⚠️  Data Fetching Anti-Pattern Risk

This feature shares data across components, but no provider pattern found.

**Risk**: Prop drilling or duplicate fetches

**Recommendation**: Add to plan Phase 1:
1. Create context/provider for shared data
2. Add caching (SWR/React Query)
3. Then implement feature

Add data provider to plan? (Y/n)
```

---

#### 4. TypeScript Pattern Check (if TypeScript project)

**Scan existing code for anti-patterns:**

```bash
# Check for any abuse
grep -r ": any" src/ --include="*.ts" --include="*.tsx" | wc -l

# Check for ! abuse
grep -r "!\." src/ --include="*.ts" --include="*.tsx" | wc -l

# Check for Zod usage
grep -r "from 'zod'\|from \"zod\"" src/ --include="*.ts" | head -1
```

**Report findings:**
```
📊 TypeScript Pattern Scan

- `any` usage: 15 occurrences (⚠️ high - consider typing)
- `!.` assertions: 8 occurrences (⚠️ consider null handling)
- Zod validation: ✅ Found (good - use for this feature too)

**Recommendation**: Plan should use Zod for validation, avoid any/!
```

---

#### 5. Centralized Patterns Summary

**Before generating plan, ensure these exist or will be created:**

```
Architecture Pattern Checklist:
- [ ] Auth: Centralized middleware/layout exists OR will be created in Phase 1
- [ ] Errors: Global error boundary exists OR will be created in Phase 1
- [ ] Data: Provider pattern exists OR will be created in Phase 1 (if needed)
- [ ] Config: Env validation exists OR will be created in Phase 1
- [ ] Logging: Central logger exists OR will be created in Phase 1
- [ ] API Response: Consistent format exists OR will be defined in Phase 1
```

**If any pattern missing and spec needs it:**
- Add to plan Phase 1 as "Setup centralized [pattern]"
- This prevents the "patching 10 pages later" problem

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

**From stack.md:**
- Framework: [from stack.md]
- Database: [from stack.md]
- Key libraries: [from stack.md]

**Patterns from architecture.md:**
- [Pattern 1 we're following]
- [Pattern 2 we're following]

---

## Implementation Steps

### Phase 1: Setup
- [ ] [Setup task 1]
- [ ] [Setup task 2]

### Phase 2: Core Implementation
- [ ] [Core task 1]
- [ ] [Core task 2]
- [ ] [Core task 3]

### Phase 3: Integration
- [ ] [Integration task 1]
- [ ] [Integration task 2]

### Phase 4: Testing
- [ ] [Test task 1]
- [ ] [Test task 2]

---

## Data Model Changes

**New/Modified entities:**
- [Entity 1]: [description]
- [Entity 2]: [description]

**Database changes needed:**
- [ ] [Migration 1]
- [ ] [Migration 2]

---

## File Structure

**New files to create:**
```
[file-path-1]
[file-path-2]
```

**Files to modify:**
```
[file-path-1]
[file-path-2]
```

---

## Key Decisions

**Decision 1**: [What was decided]
- **Why**: [Rationale]
- **Alternative**: [What we didn't choose]

**Decision 2**: [What was decided]
- **Why**: [Rationale]

---

## Acceptance Criteria

From spec.md:
- [ ] [AC 1]
- [ ] [AC 2]
- [ ] [AC 3]

---

## Potential Gotchas

- [Gotcha 1]: [How to avoid]
- [Gotcha 2]: [How to avoid]

---

## Next Steps

After plan approval:
1. Run `/lite-implement` to start coding
2. Follow TDD-lite approach
3. Document as you build

---

## References

- Spec: .shipkit-lite/specs/active/[feature-name].md
- Stack: .shipkit-lite/stack.md
- Architecture: .shipkit-lite/architecture.md
```

---

### Step 4: Log Decision (if significant)

**If plan makes architectural decision**, offer to log it:

"This plan establishes [pattern/choice]. Should I log this to architecture-memory-lite?"

If yes, suggest:
```
/lite-architecture-memory
```

---

### Step 5: Suggest Next Step

**Output to user**:
```
✅ Implementation plan created

📁 Location: .shipkit-lite/plans/active/[feature-name]-plan.md

📋 Summary:
  • [X] implementation steps
  • [Y] files to create/modify
  • [Z] database changes

🎯 Complexity: [Simple/Medium/Complex]
⏱️  Estimated: [X hours/days]

```

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
- ✅ Step-by-step implementation guide
- ✅ References existing context (stack, architecture)
- ✅ File structure planning
- ✅ Key technical decisions

**Not included** (vs full dev-plan):
- ❌ Research phase (no unknowns investigation)
- ❌ API contracts (OpenAPI/GraphQL schemas)
- ❌ Detailed data model design
- ❌ Performance benchmarks
- ❌ Security threat modeling
- ❌ Deployment planning

**Philosophy**: Good enough plan to start coding, not exhaustive design doc.

---

## The Iron Law

**PLANS ANSWER "HOW", NOT "WHY" OR "WHAT"**

**What this means**:
- Plan assumes spec already defined the "what" (requirements) and "why" (value)
- Plan focuses solely on "how" (implementation approach, file structure, steps)
- If you're questioning WHAT to build → Go back to `/lite-spec`
- If you're questioning WHY to build it → Go back to `/lite-spec` or product discovery
- Plan is technical roadmap, not requirements document

**Breaking this law leads to**:
- Planning features nobody asked for
- Solving problems not in the spec
- Over-engineering solutions
- Mixing requirements gathering with implementation planning

**The fix**: Before planning, read the spec. Plan what's in the spec. Nothing more.

---

## Red Flags

**Watch for these rationalizations that violate the Iron Law**:

### 🚩 "While I'm planning, I should add..."
**The trap**: Scope creep during planning
**Why it's tempting**: "It would be easy to add feature X while building feature Y"
**The reality**: Spec didn't ask for feature X
**Alternative**: Note the idea in spec, let user decide if it belongs

### 🚩 "The spec doesn't say HOW to do X, so I'll figure it out"
**The trap**: Over-interpreting requirements
**Why it's tempting**: Spec has ambiguity, you want to be helpful
**The reality**: Ambiguity = ask user, don't assume
**Alternative**: Use `/lite-spec` to clarify before planning

### 🚩 "This plan needs more research/design/prototyping first"
**The trap**: Analysis paralysis
**Why it's tempting**: Want perfect plan before coding
**The reality**: POC/MVP plans should be "good enough to start"
**Alternative**: Plan with what you know, iterate as you learn

### 🚩 "Let me plan edge cases not in the spec"
**The trap**: Gold-plating
**Why it's tempting**: Want robust solution
**The reality**: POC/MVP = happy path first
**Alternative**: Note edge cases for future, plan only what spec requires

---

## When This Skill Integrates with Others

### Before This Skill
- `/lite-spec` - Creates feature specification
  - **When**: User has described what to build
  - **Why**: Plan needs a spec to reference - can't plan implementation without knowing requirements
  - **Trigger**: Spec file exists at `.shipkit-lite/specs/active/[feature].md`

- `/lite-project-context` - Generates stack.md, schema.md
  - **When**: New project or stack not yet documented
  - **Why**: Plan must align with chosen tech stack - prevents "planning for React when you're using Vue"
  - **Trigger**: First time planning any feature in project

- `/lite-architecture-memory` - Logs past decisions
  - **When**: Prior features have established patterns
  - **Why**: Plan should follow existing conventions - consistency matters
  - **Trigger**: architecture.md exists with logged decisions

### After This Skill
- `/lite-implement` - Executes the plan with TDD-lite
  - **When**: Plan approved and ready to code
  - **Why**: Plan provides roadmap for implementation - implement follows plan steps
  - **Trigger**: User says "start coding" or "implement this"

- `/lite-architecture-memory` - Logs significant decisions
  - **When**: Plan makes architectural choice (library selection, pattern adoption)
  - **Why**: Future plans should know about this decision - prevents reinventing choices
  - **Trigger**: Plan establishes new pattern not yet in architecture.md (optional)

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

**Rationale**:
- Each plan is feature-specific and tied to a single spec
- Plans are generated on-demand when user invokes `/lite-plan`
- If user re-plans the same feature, they want a fresh plan based on current context
- Old plans become stale as specs, stack, or architecture evolve
- No historical value: planning is forward-looking, not a historical record
- Checkboxes track implementation progress, but that state belongs in implementation tracking, not the plan itself

**Behavior**:
- If `.shipkit-lite/plans/active/[feature]-plan.md` exists, completely replace it
- Use Write tool (after Read) to overwrite with new content
- No archiving needed - plans are regenerated artifacts, not historical documents
- User can always re-generate by re-running `/lite-plan`

**When to re-plan**:
- Spec changed significantly (use `/lite-spec` to update, then re-run `/lite-plan`)
- Tech stack changed (stack.md updated, need new plan)
- Architecture patterns changed (architecture.md updated, need aligned plan)

**Never modifies**:
- Specs, stack, architecture (read-only)

---

## Lazy Loading Behavior

**This skill loads context ON DEMAND**:

1. User invokes `/lite-plan`
2. shipkit-master-lite tells Claude to read this SKILL.md
3. Claude asks user which spec to plan
4. Claude reads only relevant spec + stack
5. Claude optionally reads architecture/types if needed
6. Claude generates plan
7. Context loaded: ~1500-2500 tokens (focused)

**Not loaded unless needed**:
- Other specs
- Implementation docs
- User tasks
- Progress logs

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

## Tips for Effective Planning

**Keep it focused**:
- Plan ONE feature at a time
- 10-20 steps maximum for POC
- Don't over-design

**Reference context**:
- Check stack.md for approved tech
- Check architecture.md for established patterns
- Reuse existing components when possible

**Make it actionable**:
- Specific file paths
- Clear task descriptions
- Checkboxes for tracking

**When to upgrade to full /dev-plan**:
- Complex integrations requiring research
- API contracts needed
- Security-critical features
- Performance requirements
- Multi-service coordination

---

**Remember**: This is a POC/MVP plan. Get something working, then refine. Don't spend hours planning what you could learn in minutes of coding.
