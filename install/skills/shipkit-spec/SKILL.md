---
name: shipkit-spec
description: "Use when user describes a feature to build. Triggers: 'spec this', 'create specification', 'define requirements', 'I want to build'."
argument-hint: "<feature name or description>"
---

# shipkit-spec - Lightweight Feature Specification

**Purpose**: Transform feature descriptions into Given/When/Then specifications with comprehensive edge case coverage, creating clear acceptance criteria for implementation without heavyweight documentation overhead.

---

## When to Invoke

**User triggers**:
- "Spec this feature"
- "Create a specification"
- "What are the requirements?"
- "Define the feature properly"
- User describes a new feature idea

**Before**:
- `/shipkit-plan` (this creates the spec that planning needs)
- `implement (no skill needed)` (need spec before implementing)

**Workflow position**:
- After feature concept is clear
- Before implementation planning
- Can be used standalone for requirement clarification

---

## Prerequisites

**Recommended**:
- Stack defined: `.shipkit/stack.md` (to understand tech constraints)
- Schema defined: `.shipkit/schema.md` (to understand data model)

**Optional but helpful**:
- Architecture decisions: `.shipkit/architecture.md`
- Existing specs: `.shipkit/specs/active/*.md` (check for similar patterns)

**If missing**: Ask user basic questions about tech stack and data instead

---

## Process

### Step 1: Understand the Feature

**Before generating anything**, use AskUserQuestion tool to gather requirements:

**Question 1 - Feature Type:**
```
header: "Type"
question: "What type of feature are you specifying?"
options:
  - label: "User-facing UI"
    description: "Forms, dashboards, navigation, visual components"
  - label: "API/Backend"
    description: "Endpoints, services, data processing"
  - label: "Integration"
    description: "Third-party services, webhooks, external APIs"
  - label: "Infrastructure"
    description: "Auth, caching, database changes"
```

**Question 2 - Complexity:**
```
header: "Scope"
question: "How complex is this feature?"
options:
  - label: "Simple (Recommended)"
    description: "Single component/endpoint, minimal state"
  - label: "Medium"
    description: "Multiple components, some state management"
  - label: "Complex"
    description: "Cross-cutting concerns, significant architecture"
```

**If user selects "Other"**: Follow up with clarifying questions about their specific needs.

**Why ask first**: Avoid generating wrong spec based on assumptions.

---

### Step 2: Read Existing Context

**Read these files to understand project context**:

```bash
# Tech constraints
.shipkit/stack.md

# Data model
.shipkit/schema.md

# Past decisions
.shipkit/architecture.md

# Check for similar specs
.shipkit/specs/active/*.md
```

**Token budget**: Keep context reading under 1500 tokens.

**If files don't exist**: Proceed without them, ask user about tech/data as needed.

---

### Step 3: Generate Specification

**Create spec file using Write tool**:

**Location**: `.shipkit/specs/active/[feature-name].md`

**Use kebab-case for filename**: `recipe-sharing.md`, `user-authentication.md`

**Template structure:** See Spec Template Structure section below

---

### Step 4: Validate Completeness

**Before saving spec, verify**:

- [ ] User story clearly states WHO, WHAT, WHY
- [ ] At least 2-3 Given/When/Then scenarios
- [ ] ALL 6 edge case categories applied
- [ ] Must Have / Should Have / Won't Have prioritization
- [ ] Technical notes include database/API changes
- [ ] Next steps suggest appropriate skills

**See `references/tips-and-examples.md` for quality checklist**

---

### Step 5: Save and Suggest Next Step

**Use Write tool to create**: `.shipkit/specs/active/[feature-name].md`

**Output to user**:
```
✅ Specification created

📁 Location: .shipkit/specs/active/[feature-name].md

📋 Summary:
  • [X] core scenarios
  • [Y] edge cases identified
  • [Z] acceptance criteria

🎯 Completeness:
  • User story: ✓
  • Given/When/Then: ✓
  • Edge cases: ✓ (all 6 categories)
  • Acceptance criteria: ✓

```

---

## Completion Checklist

Copy and track:
- [ ] Asked 2-3 clarifying questions
- [ ] Created spec with Given/When/Then scenarios
- [ ] Applied all 6 edge case categories
- [ ] Saved to `.shipkit/specs/active/[name].md`

---

## Spec Template Structure

**Every spec MUST follow this template**:

```markdown
# [Feature Name]

**Created**: [YYYY-MM-DD]
**Status**: Active

---

## User Story

As a [user type], I want to [action], so that [benefit].

**Example:**
As a recipe author, I want to share my recipes publicly via a unique link, so others can view them without signing up.

---

## Core Scenarios

### Given/When/Then

**Scenario 1: [Primary happy path]**

**Given**: [Initial state]
**When**: [User action]
**Then**:
- [Expected outcome 1]
- [Expected outcome 2]
- [Expected outcome 3]

**Scenario 2: [Alternative flow]**

**Given**: [Different initial state]
**When**: [User action]
**Then**:
- [Expected outcome]

**Scenario 3: [Reversal/undo]**

**Given**: [State after scenario 1]
**When**: [Reversal action]
**Then**:
- [Expected outcome]

---

## Edge Cases

**Apply all 6 edge case categories to EVERY feature.**

**See `references/edge-case-checklist.md` for complete checklist:**
- Loading States (spinners, disable controls, timeout, prevent duplicates)
- Error States (network, server, validation, permission, not found)
- Empty/Missing States (no data, no results, deleted items, first-time user)
- Permission States (unauthenticated, unauthorized, role-based, ownership)
- Boundary Conditions (min/max values, rate limits, quotas, character limits)
- Data Consistency (stale data, partial updates, cache invalidation, conflicts)

**See `references/best-practices.md` for frontend and backend quality standards:**
- Frontend: State management, user feedback, accessibility, performance, security, forms, navigation
- Backend: Input validation, authentication, error handling, data integrity, security, performance, API design

### Loading States
- [ ] Show spinner/skeleton during initial load
- [ ] Disable UI controls during async operations
- [ ] Handle timeout scenarios (>5 seconds)
- [ ] Prevent duplicate submissions (double-click)

### Error States
- [ ] Network failure during operation → Show error toast, revert UI state
- [ ] Server error (500) → Show user-friendly message, log error
- [ ] Validation errors → Show inline feedback, highlight fields
- [ ] Permission errors (401/403) → Redirect to login or show access denied

### Empty/Missing States
- [ ] No data available → Show empty state with helpful CTA
- [ ] Search with no results → Show "no results" with suggestions
- [ ] Deleted/missing resource → Show "not found" message
- [ ] First-time user experience → Show onboarding/tutorial

### Permission States
- [ ] Unauthenticated user access → Redirect to login
- [ ] Authenticated but unauthorized → Show access denied
- [ ] Role-based restrictions → Hide unavailable features
- [ ] Ownership checks → Only owner can edit/delete

### Boundary Conditions
- [ ] Minimum values (0, empty string, null)
- [ ] Maximum values (string length limits, array size limits)
- [ ] Rate limits → Show "too many requests" message
- [ ] Quota/usage limits → Show limit warning, upgrade prompt
- [ ] Concurrent access → Handle optimistic locking conflicts

### Data Consistency
- [ ] Stale data → Refresh on focus/visibility change
- [ ] Partial updates → Handle partial failures gracefully
- [ ] Cache invalidation → Clear related caches
- [ ] Referential integrity → Handle cascading deletes

### SaaS-Specific (if applicable)
- [ ] Multi-tenancy → User ID on every query, RLS policies
- [ ] Subscription state → Handle active/expired/cancelled
- [ ] Payment failures → Graceful degradation, retry prompts
- [ ] Plan limits → Enforce quotas, show upgrade prompts
- [ ] Trial expiry → Clear messaging, conversion flow
- [ ] Webhook reliability → Idempotency, retry handling

---

## Acceptance Criteria

### Must Have
✓ [Critical requirement 1]
✓ [Critical requirement 2]
✓ [Critical requirement 3]
✓ All edge cases handled gracefully

### Should Have
- [Nice to have feature 1]
- [Nice to have feature 2]

### Won't Have (this iteration)
- [Explicitly excluded feature 1]
- [Explicitly excluded feature 2]

---

## Technical Notes

**Implementation hints** (inform planning, not requirements):
- [Technical constraint 1]
- [Technical constraint 2]
- [Suggested approach]

**Database changes needed:**
- [Table/field additions]
- [Migration notes]

**API endpoints:**
- [New endpoint 1]
- [Modified endpoint 2]

**Best practices to apply** (see `references/best-practices.md`):
- Frontend: [State management, user feedback, accessibility, performance, security, forms, navigation]
- Backend: [Input validation, auth, error handling, data integrity, security, performance, API design]

---

## Next Steps

**After spec approval:**
1. Run `/shipkit-plan` to create implementation plan
2. Or run `/shipkit-prototyping` for UI mockup first (if UI-heavy feature)
3. Or run `/shipkit-architecture-memory` to log architectural decisions

---

## References

- Stack: .shipkit/stack.md
- Schema: .shipkit/schema.md
- Architecture: .shipkit/architecture.md
```

---

## What Makes This "Lite"

**Included**:
- ✅ Given/When/Then scenarios (clear, actionable)
- ✅ Comprehensive edge case checklist (6 categories)
- ✅ Acceptance criteria with prioritization
- ✅ Technical notes for context
- ✅ Moves to implemented/ folder when done

**Not included** (vs full /dev-specify):
- ❌ Formal Cucumber/Gherkin syntax
- ❌ Automated test generation
- ❌ BDD framework integration
- ❌ Extensive examples library
- ❌ Multi-stakeholder review workflow

**Philosophy**: Clear enough to implement correctly, concise enough to read quickly.

---

## When This Skill Integrates with Others

### Before This Skill

- `/shipkit-project-context` - Generates stack.md and schema.md
  - **When**: Project initialization or when stack/schema missing
  - **Why**: Spec needs tech constraints and data model context
  - **Trigger**: Missing stack.md or schema.md detected during spec creation

- **User describes feature idea** - Provides initial feature concept
  - **When**: User has new feature to build
  - **Why**: Can't spec what hasn't been described
  - **Trigger**: User says "I want to add..." or "spec this feature"

### After This Skill

- `/shipkit-plan` - Creates implementation plan from spec
  - **When**: Spec is complete and approved
  - **Why**: Spec defines WHAT to build, plan defines HOW
  - **Trigger**: Spec saved to specs/active/, user confirms "ready to plan"

- `/shipkit-prototyping` - Creates rapid UI mockup
  - **When**: Spec includes significant UI/UX components (optional step)
  - **Why**: Validate UI direction before committing to full implementation
  - **Trigger**: User wants to see UI mockup before building real code

- `/shipkit-architecture-memory` - Logs architectural decisions made during spec
  - **When**: Spec reveals architectural choices (optional step)
  - **Why**: Document tech decisions for future reference
  - **Trigger**: Spec's Technical Notes section reveals important architectural choice

---

## Context Files This Skill Reads

**Recommended** (read if exist):
- `.shipkit/stack.md` - Tech stack constraints
- `.shipkit/schema.md` - Data model
- `.shipkit/architecture.md` - Past decisions

**Optional** (read if relevant):
- `.shipkit/specs/active/*.md` - Check for similar specs

**If missing**: Ask user for needed context

---

## Context Files This Skill Writes

**Write Strategy: CREATE (with ARCHIVE on completion)**

**Creates**:
- `.shipkit/specs/active/[feature-name].md` - New specification

**Update Behavior**:
- Active specs can be modified during planning/implementation (overwrites previous version)
- Each update REPLACES the file contents completely
- No version history maintained in active/ folder

**Archive Behavior** (when feature complete):
- Moves: `.shipkit/specs/active/[feature-name].md` → `.shipkit/specs/implemented/[feature-name].md`
- Adds completion metadata (date implemented, who implemented, final notes)
- Archived specs become read-only historical records
- Moving specs: Either manual or via `verify manually` when feature ships

**Why CREATE with ARCHIVE:**
- Specs are living documents during development (can be refined)
- Each feature gets its own independent file (not appending to shared file)
- History preserved by moving completed specs to implemented/ folder
- Completion metadata captures final state for audit trail

**See `references/spec-lifecycle.md` for complete lifecycle documentation**

---

## Lazy Loading Behavior

**This skill loads context ON DEMAND**:

1. User invokes `/shipkit-spec` or describes feature
2. shipkit-master tells Claude to read this SKILL.md
3. Claude asks 2-3 clarifying questions
4. Claude reads stack.md + schema.md (~500 tokens)
5. Claude optionally reads architecture.md if relevant (~300 tokens)
6. Claude generates spec
7. Total context loaded: ~1000-1500 tokens (focused)

**Not loaded unless needed**:
- Other specs (unless checking for similar patterns)
- Plans
- Implementations
- User tasks

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

Spec is complete when:
- [ ] User story clearly defined (WHO, WHAT, WHY)
- [ ] 2-3 Given/When/Then scenarios documented
- [ ] All 6 edge case categories applied and checked
- [ ] Acceptance criteria prioritized (Must/Should/Won't)
- [ ] Technical notes include DB/API changes
- [ ] File saved to `.shipkit/specs/active/`
<!-- /SECTION:success-criteria -->
---

## Reference Documentation

**For detailed patterns and examples:**

- **Edge case checklist** - `references/edge-case-checklist.md`
  - Complete 6-category checklist
  - Why each category matters
  - Application examples

- **Best practices** - `references/best-practices.md`
  - Frontend best practices (state management, user feedback, accessibility, performance, security, forms, navigation)
  - Backend best practices (input validation, auth, error handling, data integrity, security, performance, API design)
  - How to apply during spec creation
  - When to waive practices

- **Given/When/Then guide** - `references/gwt-pattern-guide.md`
  - Pattern structure and tips
  - Good vs bad examples
  - Common patterns and anti-patterns

- **Spec lifecycle** - `references/spec-lifecycle.md`
  - Active vs implemented states
  - Moving between states
  - Modification guidelines

- **Tips and examples** - `references/tips-and-examples.md`
  - Writing tips (actionable, specific)
  - Common scenarios walkthrough
  - Real-world examples

---

**Remember**: This is a lightweight spec for POC/MVP work. Get enough clarity to build correctly, but don't over-specify. Ship, learn, iterate.

<!-- Shipkit v1.2.0 -->
