---
name: lite-implement
description: Guides TDD-lite implementation of features by providing real-time coding guidance and verification. Use when user asks to "start implementing", "build this", "code the feature", or after plan exists.
---

# implement-lite - TDD-Lite Implementation Guidance

**Purpose**: Guide feature implementation using lightweight TDD principles - write test, write code, verify it works - without heavyweight process overhead.

---

## When to Invoke

**User triggers**:
- "Start implementing"
- "Let's build this"
- "Begin coding"
- "Implement the feature"

**After**:
- `/lite-plan` has created implementation plan (recommended)
- OR spec exists and user wants to code directly

---

## Prerequisites

**Recommended**:
- Plan exists: `.shipkit-lite/plans/[feature]-plan.md`
- Spec exists: `.shipkit-lite/specs/active/[feature].md`

**Optional but helpful**:
- Stack defined: `.shipkit-lite/stack.md`
- Types defined: `.shipkit-lite/types.md`

---

## Process

### Step 1: Confirm What to Build

**Before starting**, ask user:

1. **Which feature are we implementing?**
   - List available plans from `.shipkit-lite/plans/`
   - OR list specs from `.shipkit-lite/specs/active/`
   - Let user choose

2. **Starting from scratch or continuing?**
   - "New feature?" → Follow plan from step 1
   - "Continue existing?" → Ask what's done, what's next

3. **TDD level?**
   - "Full TDD (test first, always)?"
   - "Lite TDD (test critical paths)?"
   - "Manual testing only?"

**Why ask**: Don't assume - confirm approach before writing code.

---

### Step 2: Read Context

**Read to understand what to build**:

```bash
# If plan exists (recommended)
.shipkit-lite/plans/[feature]-plan.md

# If no plan, read spec directly
.shipkit-lite/specs/active/[feature].md

# Tech stack (to know what tools to use)
.shipkit-lite/stack.md
```

**Optional context** (load if relevant):
```bash
# Types (if building on existing data structures)
.shipkit-lite/types.md

# Architecture (if following established patterns)
.shipkit-lite/architecture.md

# Implementations (if integrating with existing components)
.shipkit-lite/implementations.md
```

**Token budget**: Keep context reading under 2000 tokens.

---

### Step 3: TDD-Lite Cycle

**For EACH implementation task, follow this cycle**:

```
┌─────────────────────────────────────────┐
│ 🔴 RED - Write Test First (Optional)   │
│ ─────────────────────────────────────── │
│ • For critical logic: Write test first  │
│ • For simple UI: Skip to coding         │
│ • Run test → Should FAIL                │
└─────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│ 🟢 GREEN - Write Minimal Code          │
│ ─────────────────────────────────────── │
│ • Write simplest code that works        │
│ • Reference stack.md for tech choices   │
│ • Reference architecture.md for patterns│
│ • If test exists: Make it pass          │
│ • If no test: Build and verify manually │
└─────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│ ✅ VERIFY - Does It Work?              │
│ ─────────────────────────────────────── │
│ • Run tests (if they exist)             │
│ • Manual test in browser/terminal       │
│ • Check against acceptance criteria     │
│ • EVIDENCE required before "done"       │
└─────────────────────────────────────────┘
```

**The Lite TDD Rule**:
```
Test critical paths. Manual test the rest. But ALWAYS verify before claiming done.
```

---

### Step 4: Implementation Guidance

**As you code, provide real-time guidance**:

**Before writing each file**:
- "This implements [task] from the plan"
- "Using [pattern] from architecture.md"
- "Following [tech] from stack.md"

**While writing code**:
- Keep it simple (POC mindset)
- Happy path first, edge cases later
- No premature optimization
- Comment non-obvious decisions

**After writing code**:
- "Created [file]"
- "Test it by: [specific steps]"
- "Expected result: [what should happen]"

---

### Step 5: Track Progress

**After completing each major piece**, offer to update:

```
✅ Completed: [component/route/feature part]

📁 Files created/modified:
  • [file 1]
  • [file 2]

Would you like me to:
1. Document this component? (/lite-component-knowledge)
2. Log this decision? (/lite-architecture-memory)
3. Continue to next task?
```

---

### Step 6: Verification Gates

**Before marking feature "done", verify**:

```markdown
## Feature Verification Checklist

**Functionality**:
- [ ] Core feature works (manual test)
- [ ] Acceptance criteria met (from spec)
- [ ] Happy path tested

**Code Quality** (lite checks):
- [ ] Code is readable
- [ ] No obvious bugs
- [ ] Follows stack.md tech choices
- [ ] Follows architecture.md patterns

**Optional** (POC can skip):
- [ ] Error handling (basic)
- [ ] Loading states (if applicable)
- [ ] Edge cases (defer to later)

**Evidence**:
- Screenshot/log showing it works
- Test output (if tests exist)
- Description of manual verification
```

**If gaps exist**: List what's missing, ask if acceptable for POC.

---

### Step 7: Document Completion

**When feature is done, use Write tool to create**:

**Location**: `.shipkit-lite/implementations.md` (APPEND)

**Format**:
```markdown
---

## [Feature Name] - Implemented [Date]

**Files**:
- [file 1]
- [file 2]

**What it does**:
[1-2 sentence description]

**How to use**:
[Quick usage example]

**Tech used**:
- [Framework/library 1]
- [Framework/library 2]

**Decisions made**:
- [Decision 1]: [Why]
- [Decision 2]: [Why]

**Test coverage**:
- [What was tested]
- [What was verified manually]

**Known limitations** (POC):
- [Limitation 1]
- [Limitation 2]

**Next steps** (if feature continues):
- [Future improvement 1]
- [Future improvement 2]

---
```

---

### Step 8: Suggest Next Step

**After implementation complete**:

```
✅ Feature implemented and verified

📁 Updated: .shipkit-lite/implementations.md

🎯 Completed:
  • [X] files created
  • [Y] acceptance criteria met
  • [Z] tests passing

📝 Documentation:
  • Implementation logged
  • [Decisions logged to architecture.md] (if applicable)

👉 Next options:
  1. /lite-quality-confidence - Pre-ship verification
  2. /lite-component-knowledge - Document complex components
  3. /lite-work-memory - Log session progress
  4. Continue to next feature

What would you like to do?
```

---

## What Makes This "Lite"

**Included**:
- ✅ TDD-lite cycle (test critical, manual test rest)
- ✅ Real-time implementation guidance
- ✅ References context (stack, architecture, types)
- ✅ Verification before "done"
- ✅ Implementation logging

**Not included** (vs full dev-implement):
- ❌ Mandatory TDD for everything
- ❌ Two-stage code review (spec compliance + quality)
- ❌ Systematic debugging workflow
- ❌ Subagent task orchestration
- ❌ Comprehensive test coverage requirements

**Philosophy**: Get it working with reasonable quality, not production-perfect.

---

## TDD-Lite Decision Tree

**When to write test first**:
- ✅ Business logic (calculations, algorithms)
- ✅ Data transformations
- ✅ API endpoints
- ✅ Critical user flows

**When manual testing is fine**:
- ✅ Simple UI components
- ✅ Static pages
- ✅ Styling/layout
- ✅ One-off scripts

**The rule**: If it breaks, users notice immediately = test it. If it's visual/simple = manual test.

---

## Integration with Other Skills

**Before implement-lite**:
- `/lite-spec` - Feature requirements
- `/lite-plan` - Implementation steps
- `/lite-project-context` - Stack/schema info

**During implement-lite**:
- `/lite-integration-guardrails` - Warns about service integration mistakes
- `/lite-data-consistency` - Ensures types stay consistent
- `/lite-ux-coherence` - Guides UI patterns

**After implement-lite**:
- `/lite-component-knowledge` - Documents complex components
- `/lite-quality-confidence` - Pre-ship verification
- `/lite-work-memory` - Logs session progress

---

## Context Files This Skill Reads

**Primary**:
- `.shipkit-lite/plans/[feature]-plan.md` - Implementation steps
- `.shipkit-lite/specs/active/[feature].md` - Feature requirements
- `.shipkit-lite/stack.md` - Tech stack

**Secondary** (on demand):
- `.shipkit-lite/architecture.md` - Established patterns
- `.shipkit-lite/types.md` - Type definitions
- `.shipkit-lite/implementations.md` - Existing components

---

## Context Files This Skill Writes

**Write Strategy**: **APPEND** (preserves all historical implementation records)

**Updates**:
- `.shipkit-lite/implementations.md` - **APPEND ONLY** - Adds new implementation records while preserving all historical entries
  - **Why APPEND**: Implementation history is valuable for understanding code evolution, past decisions, and accumulated technical debt
  - **Format**: Each entry separated by `---` with timestamp, creating a chronological log
  - **Never deletes**: Old implementations remain as permanent documentation of what was built
  - **Lookup pattern**: Searched when integrating with existing components (line 350)

**Never modifies**:
- Specs, plans, stack, architecture (read-only during implementation)

---

## Lazy Loading Behavior

**This skill loads context progressively**:

1. User invokes `/lite-implement`
2. Claude asks which feature to implement
3. Claude reads plan + spec (~1000 tokens)
4. Claude reads stack.md (~200 tokens)
5. **During coding**, Claude loads on demand:
   - Types when creating data structures
   - Architecture when making decisions
   - Implementations when integrating
6. Total context: ~1500-3000 tokens (focused)

**Not loaded unless needed**:
- Unrelated specs/plans
- User tasks
- Session logs
- Other features' implementations

---

## Success Criteria

Implementation is complete when:
- [ ] All critical functionality works (verified)
- [ ] Acceptance criteria met (from spec)
- [ ] Code follows stack.md tech choices
- [ ] Code follows architecture.md patterns (if established)
- [ ] Evidence of testing provided
- [ ] Implementation logged to implementations.md
- [ ] User can demo the feature

---

## Common Scenarios

### Scenario 1: Starting Fresh Feature

```
User: "Let's implement the recipe sharing feature"

Claude:
1. Read .shipkit-lite/plans/recipe-sharing-plan.md
2. Read .shipkit-lite/stack.md (see we're using Next.js + Supabase)
3. Guide user through implementation steps from plan
4. For each component:
   - Suggest test if critical
   - Write minimal code
   - Verify it works
5. Log to implementations.md when done
```

### Scenario 2: Continuing Partial Work

```
User: "Continue implementing - the form is done, need to add the API"

Claude:
1. Read .shipkit-lite/implementations.md (see what's complete)
2. Read .shipkit-lite/plans/[feature]-plan.md (see what's next)
3. Focus on API endpoint step
4. Reference stack.md for API patterns
5. Write test for endpoint
6. Implement endpoint
7. Verify with curl/Postman
8. Update implementations.md
```

### Scenario 3: No Plan Exists

```
User: "Build the logout button"

Claude:
1. "No plan exists. Create plan first? (/lite-plan)"
2. If user says "just build it":
   - Read .shipkit-lite/stack.md
   - Read .shipkit-lite/architecture.md
   - Ask a few clarifying questions
   - Guide simple implementation
   - No need for formal plan for simple features
```

---

## Tips for Effective Implementation

**Start simple**:
- Hardcode first, refactor later
- Happy path only initially
- Skip edge cases for POC

**Verify continuously**:
- Test after each component
- Don't wait until "done"
- Get visual/manual feedback

**Document as you go**:
- Log significant decisions
- Update implementations.md
- Don't defer documentation

**When to pause and plan**:
- Feature is more complex than expected
- Needs research or investigation
- Multiple approaches possible

**When to upgrade to full /dev-implement**:
- Production-critical feature
- Complex integration requiring TDD discipline
- Multiple developers coordinating
- Comprehensive test coverage required

---

**Remember**: POC implementation prioritizes learning and iteration. Get it working, get feedback, then refine. Perfect is the enemy of done.
