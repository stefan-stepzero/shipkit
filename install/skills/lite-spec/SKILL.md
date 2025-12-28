---
name: lite-spec
description: Converts feature descriptions into Given/When/Then specifications with edge cases, acceptance criteria, and test scenarios. Creates lightweight specs for POC/MVP features. Use when user describes new feature or says "spec this".
---

# spec-lite - Lightweight Feature Specification

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
- `/lite-plan` (this creates the spec that planning needs)
- `/lite-implement` (need spec before implementing)

**Workflow position**:
- After feature concept is clear
- Before implementation planning
- Can be used standalone for requirement clarification

---

## Prerequisites

**Recommended**:
- Stack defined: `.shipkit-lite/stack.md` (to understand tech constraints)
- Schema defined: `.shipkit-lite/schema.md` (to understand data model)

**Optional but helpful**:
- Architecture decisions: `.shipkit-lite/architecture.md`
- Existing specs: `.shipkit-lite/specs/active/*.md` (check for similar patterns)

**If missing**: Ask user basic questions about tech stack and data instead

---

## Process

### Step 1: Understand the Feature

**Before generating anything**, ask user 2-3 clarifying questions:

1. **What feature are you specifying?**
   - Get clear feature name
   - Understand core purpose

2. **What's the core user goal?**
   - What problem does this solve?
   - Who benefits?

3. **Any specific edge cases to consider?**
   - Beyond standard ones (we'll add those automatically)
   - Domain-specific scenarios
   - Known problem areas

**Why ask first**: Avoid generating wrong spec based on assumptions.

---

### Step 2: Read Existing Context

**Read these files to understand project context**:

```bash
# Tech constraints
.shipkit-lite/stack.md

# Data model
.shipkit-lite/schema.md

# Past decisions
.shipkit-lite/architecture.md

# Check for similar specs
.shipkit-lite/specs/active/*.md
```

**Token budget**: Keep context reading under 1500 tokens.

**If files don't exist**: Proceed without them, ask user about tech/data as needed.

---

### Step 3: Generate Specification

**Create spec file using Write tool**:

**Location**: `.shipkit-lite/specs/active/[feature-name].md`

**Use kebab-case for filename**: `recipe-sharing.md`, `user-authentication.md`

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

**Apply the edge case checklist below to EVERY feature.**

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

---

## Next Steps

**After spec approval:**
1. Run `/lite-plan` to create implementation plan
2. Or run `/lite-ux-coherence` for UX review first (optional)
3. Or run `/lite-architecture-memory` to log architectural decisions

---

## References

- Stack: .shipkit-lite/stack.md
- Schema: .shipkit-lite/schema.md
- Architecture: .shipkit-lite/architecture.md
```

---

## Edge Case Checklist Reference

**Use this checklist when generating ANY spec. Apply ALL categories.**

### 1. Loading States
Standard async operation handling:
- Initial load (show skeleton/spinner)
- Action in progress (disable controls, show feedback)
- Timeout handling (>5 seconds, show error/retry)
- Prevent duplicate actions (debounce, disable on submit)

### 2. Error States
Comprehensive error handling:
- **Network failures**: Offline, timeout, connection dropped
- **Server errors**: 500, 502, 503 (show user-friendly message)
- **Validation errors**: Client-side and server-side
- **Permission errors**: 401 (auth required), 403 (forbidden)
- **Not found errors**: 404 (resource missing)

### 3. Empty States
Zero-data scenarios:
- No data available (new user, fresh install)
- Search with no results
- Deleted/archived items
- Filter applied with no matches
- First-time user experience (onboarding)

### 4. Permission States
Access control scenarios:
- Unauthenticated users (redirect to login)
- Authenticated but unauthorized (access denied)
- Role-based restrictions (hide unavailable features)
- Ownership checks (only owner can modify)
- Shared resource permissions (viewer vs editor)

### 5. Boundary Conditions
Limits and extremes:
- **Minimum values**: 0, empty string, null, undefined
- **Maximum values**: String length (255, 1000, 10000 chars), array size, number ranges
- **Rate limits**: Too many requests (429), cooldown periods
- **Quota limits**: Storage limits, API call limits, feature usage caps
- **Character limits**: Input field maximums, textarea limits

### 6. Data Consistency
State management edge cases:
- Stale data (refresh on focus, visibility change)
- Partial updates (some fields succeed, others fail)
- Cache invalidation (clear related caches)
- Optimistic updates (revert on failure)
- Referential integrity (handle cascading deletes)
- Concurrent modifications (last-write-wins vs conflict detection)

---

## Given/When/Then Pattern Guide

**How to write effective scenarios**:

### Pattern Structure

```
**Given**: [Preconditions - state before action]
**When**: [User action - what they do]
**Then**: [Expected outcomes - what should happen]
```

### Good Examples

**Example 1: Feature activation**
```markdown
**Given**: User owns a recipe
**When**: User toggles "Share publicly" switch
**Then**:
- System generates unique share token
- Share link becomes available to copy
- Recipe is publicly accessible via link
- Success toast appears: "Recipe shared successfully"
```

**Example 2: Reversal**
```markdown
**Given**: User has previously shared a recipe
**When**: User toggles share off
**Then**:
- Share token is revoked immediately
- Public link returns "Recipe not available"
- Original recipe remains in user's account
- Share button changes to "Share recipe"
```

**Example 3: Error scenario**
```markdown
**Given**: User attempts to share recipe
**When**: Network request fails
**Then**:
- Toggle switch reverts to previous state
- Error toast appears: "Failed to share. Try again."
- Retry button appears
- Error is logged to console
```

### Tips for Writing Scenarios

**Be Specific**:
- ✅ "Toggle 'Share publicly' switch"
- ❌ "Share the recipe"

**State Expected UI Changes**:
- ✅ "Share button changes to 'Share recipe'"
- ❌ "UI updates"

**Include User Feedback**:
- ✅ "Success toast appears: 'Recipe shared'"
- ❌ "User knows it worked"

**Cover State Changes**:
- ✅ "Recipe is publicly accessible via link"
- ❌ "Recipe is shared"

---

### Step 4: Validate Completeness

**Before saving spec, verify**:

- [ ] User story clearly states WHO, WHAT, WHY
- [ ] At least 2-3 Given/When/Then scenarios
- [ ] ALL 6 edge case categories applied
- [ ] Must Have / Should Have / Won't Have prioritization
- [ ] Technical notes include database/API changes
- [ ] Next steps suggest appropriate skills

---

### Step 5: Save and Suggest Next Step

**Use Write tool to create**: `.shipkit-lite/specs/active/[feature-name].md`

**Output to user**:
```
✅ Specification created

📁 Location: .shipkit-lite/specs/active/[feature-name].md

📋 Summary:
  • [X] core scenarios
  • [Y] edge cases identified
  • [Z] acceptance criteria

🎯 Completeness:
  • User story: ✓
  • Given/When/Then: ✓
  • Edge cases: ✓ (all 6 categories)
  • Acceptance criteria: ✓

👉 Next steps:
  1. /lite-plan - Create implementation plan
  2. /lite-ux-coherence - Review UX patterns (optional)
  3. /lite-architecture-memory - Log architectural decisions (if any)

Ready to plan implementation?
```

---

## What Makes This "Lite"

**Included**:
- ✅ Given/When/Then scenarios (clear, actionable)
- ✅ Comprehensive edge case checklist (inline in SKILL.md)
- ✅ Acceptance criteria with prioritization
- ✅ Technical notes for context
- ✅ Moves to implemented/ folder when done

**Not included** (vs full behavior-clarity):
- ❌ Formal Cucumber/Gherkin syntax
- ❌ Automated test generation
- ❌ BDD framework integration
- ❌ Extensive examples library
- ❌ Multi-stakeholder review workflow

**Philosophy**: Clear enough to implement correctly, concise enough to read quickly.

---

## Integration with Other Skills

**Before spec-lite**:
- `/lite-project-context` - Generates stack.md, schema.md (recommended)
- User describes feature idea

**After spec-lite**:
- `/lite-plan` - Creates implementation plan from spec
- `/lite-ux-coherence` - Reviews UX patterns (optional)
- `/lite-architecture-memory` - Logs architectural decisions (optional)

**Async skills** (can interrupt):
- No async skills interrupt spec-lite (it's a quick workflow)

---

## Context Files This Skill Reads

**Recommended** (read if exist):
- `.shipkit-lite/stack.md` - Tech stack constraints
- `.shipkit-lite/schema.md` - Data model
- `.shipkit-lite/architecture.md` - Past decisions

**Optional** (read if relevant):
- `.shipkit-lite/specs/active/*.md` - Check for similar specs

**If missing**: Ask user for needed context

---

## Context Files This Skill Writes

**Write Strategy: OVERWRITE AND ARCHIVE**

**Creates**:
- `.shipkit-lite/specs/active/[feature-name].md` - New specification

**Update Behavior**:
- Active specs can be modified during planning/implementation (overwrites previous version)
- Each update REPLACES the file contents completely
- No version history maintained in active/ folder

**Archive Behavior** (when feature complete):
- Moves: `.shipkit-lite/specs/active/[feature-name].md` → `.shipkit-lite/specs/implemented/[feature-name].md`
- Adds completion metadata (date implemented, who implemented, final notes)
- Archived specs become read-only historical records
- Moving specs: Either manual or via `/lite-quality-confidence` when feature ships

**Why OVERWRITE AND ARCHIVE:**
- Specs are living documents during development (can be refined)
- Each feature gets its own independent file (not appending to shared file)
- History preserved by moving completed specs to implemented/ folder
- Completion metadata captures final state for audit trail

---

## Lazy Loading Behavior

**This skill loads context ON DEMAND**:

1. User invokes `/lite-spec` or describes feature
2. shipkit-master-lite tells Claude to read this SKILL.md
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

## Success Criteria

Spec is complete when:
- [ ] User story clearly defined (WHO, WHAT, WHY)
- [ ] 2-3 Given/When/Then scenarios documented
- [ ] All 6 edge case categories applied and checked
- [ ] Acceptance criteria prioritized (Must/Should/Won't)
- [ ] Technical notes include DB/API changes
- [ ] File saved to `.shipkit-lite/specs/active/`

---

## Common Scenarios

### Scenario 1: New Feature from Scratch

```
User: "I want to add recipe sharing"

Claude:
1. Ask: "What's the core user goal with sharing?"
   User: "Let users share recipes publicly via link"
2. Ask: "Any specific edge cases?"
   User: "Handle revocation, expired links"
3. Read .shipkit-lite/stack.md (Next.js + Supabase)
4. Read .shipkit-lite/schema.md (recipes table)
5. Generate spec with:
   - User story (recipe author shares publicly)
   - Given/When/Then (toggle share, generate token)
   - Apply all 6 edge case categories
   - Must Have: toggle, token, public page
   - Technical: Add share_token field to recipes
6. Save to .shipkit-lite/specs/active/recipe-sharing.md
7. Suggest: /lite-plan next
```

### Scenario 2: Clarify Existing Idea

```
User: "We need better search"

Claude:
1. Ask: "What should search cover? Recipes, users, both?"
   User: "Just recipes"
2. Ask: "What should be searchable? Title, ingredients, tags?"
   User: "All of those"
3. Ask: "Any specific requirements?"
   User: "Fast, show results as they type"
4. Read stack.md (understand search tech available)
5. Generate spec with:
   - User story (find recipes quickly)
   - Given/When/Then (type query, see results)
   - Edge cases: no results, slow queries, typos
   - Must Have: real-time search, highlight matches
   - Technical: Add search index, API endpoint
6. Save spec
7. Suggest: /lite-plan or /lite-architecture-memory (search approach is architectural decision)
```

### Scenario 3: No Stack Context

```
User: "Spec a login feature"

Claude:
1. Check .shipkit-lite/stack.md (doesn't exist)
2. Ask: "What's your auth approach? Email/password, OAuth, magic link?"
   User: "Email/password for now"
3. Ask: "Any specific security requirements?"
   User: "Standard stuff - secure password, remember me"
4. Generate spec with:
   - User story (access account securely)
   - Given/When/Then (enter credentials, get authenticated)
   - Edge cases: wrong password, account locked, forgot password
   - Must Have: secure login, remember me, password reset
   - Technical: Auth table, session management, bcrypt
5. Save spec
6. Suggest: Run /lite-project-context first to generate stack.md, or proceed with /lite-plan
```

---

## Tips for Effective Specs

**Keep it actionable**:
- Given/When/Then should be implementable
- Avoid vague language ("works well" → "responds in <200ms")
- Specific UI feedback ("show error toast: 'Invalid email'")

**Apply ALL edge case categories**:
- Don't skip categories - every feature needs all 6
- Loading, errors, empty, permissions, boundaries, consistency
- Check boxes force systematic thinking

**Prioritize ruthlessly**:
- Must Have = MVP cannot ship without this
- Should Have = Improve UX but not critical
- Won't Have = Explicitly excluded (prevent scope creep)

**Include technical context**:
- Database changes needed
- API endpoints required
- Tech constraints from stack.md

**When to upgrade to full /dev-specify**:
- Complex multi-system integration
- Formal compliance requirements (SOC2, HIPAA)
- Multiple stakeholder sign-off needed
- Generated code from specs required

---

## Spec Lifecycle

**Active specs** (`.shipkit-lite/specs/active/`):
- Feature not yet implemented
- Can be modified during planning/implementation
- Source of truth during development

**Implemented specs** (`.shipkit-lite/specs/implemented/`):
- Feature is live in production
- Historical record (don't modify)
- Include completion metadata:

```markdown
---
**Status**: Implemented
**Date**: 2025-01-20
**Implemented by**: Claude + User
**Final notes**: Shipped with all Must Have criteria. Deferred Should Have items to v2.
---
```

**Moving specs**: Either manual or via `/lite-quality-confidence` when shipping

---

## Edge Case Checklist (Complete Reference)

**This checklist is embedded in the spec template. Apply ALL categories to EVERY feature.**

### Loading States
Standard async operation handling:
- [ ] Initial load - Show skeleton/spinner during data fetch
- [ ] Action in progress - Disable controls, show loading indicator
- [ ] Timeout handling - >5 seconds, show error/retry option
- [ ] Prevent duplicate actions - Debounce, disable on submit

### Error States
Comprehensive error handling:
- [ ] Network failures - Offline, timeout, connection dropped → Show retry
- [ ] Server errors - 500, 502, 503 → User-friendly message, log to monitoring
- [ ] Validation errors - Client-side and server-side → Inline feedback
- [ ] Permission errors - 401 (auth required), 403 (forbidden) → Redirect or message
- [ ] Not found errors - 404 → Show "not found" page

### Empty/Missing States
Zero-data scenarios:
- [ ] No data available - New user, fresh install → Show helpful CTA
- [ ] Search with no results - Show "no results" with suggestions
- [ ] Deleted/archived items - Handle gracefully, show tombstone
- [ ] Filter applied with no matches - "No items match this filter"
- [ ] First-time user experience - Onboarding, tutorial, sample data

### Permission States
Access control scenarios:
- [ ] Unauthenticated users - Redirect to login or show public-safe view
- [ ] Authenticated but unauthorized - "You don't have access to this"
- [ ] Role-based restrictions - Hide unavailable features for role
- [ ] Ownership checks - Only owner can edit/delete
- [ ] Shared resource permissions - Viewer vs editor vs admin

### Boundary Conditions
Limits and extremes:
- [ ] Minimum values - 0, empty string, null, undefined
- [ ] Maximum values - String length (255, 1000, 10000), array size, number ranges
- [ ] Rate limits - Too many requests (429) → "Slow down, try again in X seconds"
- [ ] Quota limits - Storage, API calls, feature usage → Upgrade prompt
- [ ] Character limits - Input fields (show "X/255 characters")
- [ ] Pagination limits - Max page size, deep pagination performance

### Data Consistency
State management edge cases:
- [ ] Stale data - Refresh on focus, visibility change, pull-to-refresh
- [ ] Partial updates - Some fields succeed, others fail → Rollback or retry
- [ ] Cache invalidation - Clear related caches on mutation
- [ ] Optimistic updates - Revert on failure with error message
- [ ] Referential integrity - Cascading deletes, orphaned references
- [ ] Concurrent modifications - Last-write-wins vs conflict detection vs merge

---

**Remember**: This is a lightweight spec for POC/MVP work. Get enough clarity to build correctly, but don't over-specify. Ship, learn, iterate.
