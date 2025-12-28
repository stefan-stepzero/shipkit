---
name: lite-debug-systematically
description: Structured 4-phase debugging methodology to find root causes instead of random fixes. Guides through Observe, Hypothesize, Test, Fix phases with evidence-based investigation. Documents bugs in architecture.md for future reference.
---

# debug-systematically-lite - Evidence-Based Debugging

**Purpose**: Replace "try this fix" debugging cycles with systematic root cause investigation. Find the real problem before writing code.

---

## When to Invoke

**User triggers**:
- "This isn't working"
- "I'm getting an error"
- "Bug in [feature]"
- "Sharing/auth/feature X is broken"
- "Why is this failing?"

**Auto-invoked by**:
- `/lite-implement` when tests fail unexpectedly
- `/lite-quality-confidence` when verification fails

---

## Prerequisites

**Optional but helpful**:
- Spec exists: `.shipkit-lite/specs/active/[feature].md` (to understand expected behavior)
- Implementation exists: `.shipkit-lite/implementations.md` (to understand current code)
- Stack defined: `.shipkit-lite/stack.md` (to know tech being debugged)

**Can run standalone**: User reports bug without any prior context.

---

## The Anti-Pattern We're Preventing

**Random Fix Debugging (BAD)**:
```
User: "Sharing isn't working"
Developer: "Try adding await here"
[doesn't work]
Developer: "Maybe the permissions are wrong, try this"
[doesn't work]
Developer: "Let's refactor the whole thing"
[30 minutes wasted, still broken]
```

**Systematic Debugging (GOOD)**:
```
User: "Sharing isn't working"
Developer: "Let me observe the exact error first"
[Sees: 500 error in network tab]
Developer: "Hypothesis: Server action is failing. Test: Check server logs"
[Finds: Missing auth check throwing error]
Developer: "Root cause found. Fix: Add auth validation"
[Fixed in 5 minutes]
```

**The rule**: Evidence first, fixes last. No code changes until root cause is identified.

---

## Process

### Phase 1: OBSERVE - Gather Evidence

**Before asking hypothetical questions, collect facts.**

**Ask user these questions**:

1. **What is the exact symptom?**
   - "What did you try to do?"
   - "What happened instead?"
   - "Is there an error message? (exact text)"

2. **When does it happen?**
   - "Every time or intermittent?"
   - "Did this ever work?"
   - "What changed recently?"

3. **Where is the evidence?**
   - "Check browser console - any errors?"
   - "Check network tab - any failed requests?"
   - "Check server logs - any output?"
   - "Check terminal - any error traces?"

**Evidence Collection Template**:

```markdown
## Bug Investigation - [Feature/Component]

**Started**: [timestamp]
**Reported by**: User
**Status**: Investigating

---

### Phase 1: OBSERVE

**Symptom**:
- User action: [what they tried]
- Expected: [what should happen]
- Actual: [what happened instead]

**Evidence**:
- Browser console: [errors/warnings]
- Network tab: [failed requests, status codes, response bodies]
- Server logs: [error traces, stack traces]
- Terminal output: [build errors, runtime errors]

**Environment**:
- Browser: [Chrome/Firefox/Safari]
- Environment: [dev/staging/prod]
- User state: [logged in/out, permissions]

**Recent changes**:
- [What was modified recently that might be related]

---
```

**Where to look for evidence** (guide user):

| Symptom Type | Check These |
|--------------|-------------|
| UI not rendering | Browser console, React errors, component tree |
| API call failing | Network tab (status, headers, response), server logs |
| Authentication issues | Auth middleware logs, session/token validity |
| Database errors | Server logs, query output, migration status |
| Build failures | Terminal output, dependency versions |
| Styling broken | Browser DevTools, CSS specificity, Tailwind classes |

**Complete Phase 1 before moving to Phase 2.** No guessing yet.

---

### Phase 2: HYPOTHESIZE - List Possible Causes

**Now that we have evidence, what could explain it?**

**Based on evidence collected, list 3-5 hypotheses ranked by likelihood**:

```markdown
### Phase 2: HYPOTHESIZE

**Possible causes** (ranked by likelihood):

1. **[Most likely cause]**
   - Why: [Evidence that points to this]
   - If true: [What we'd expect to see]

2. **[Second possibility]**
   - Why: [Evidence that suggests this]
   - If true: [What we'd expect to see]

3. **[Third possibility]**
   - Why: [Less evidence but still possible]
   - If true: [What we'd expect to see]

4. **[Edge case]**
   - Why: [Rare but matches symptoms]
   - If true: [What we'd expect to see]

**Ruled out**:
- [X] [Hypothesis we can eliminate based on evidence]
- [X] [Another ruled-out option]

---
```

**Common Bug Patterns to Check**:

| Evidence | Likely Hypotheses |
|----------|-------------------|
| 500 error in API call | Missing error handling, unhandled exception, database constraint violation |
| 401/403 error | Missing auth check, expired token, insufficient permissions |
| Network request not sent | Missing event handler, form not submitting, validation blocking |
| Blank screen | Uncaught exception in component, missing data causing crash |
| Infinite loop/hang | Missing dependency in useEffect, recursive call, circular reference |
| Styling not applied | CSS specificity conflict, Tailwind not compiling, typo in class name |

**Ask user**:
- "Based on [evidence], my top hypothesis is [X]. Does that align with what you're seeing?"
- "Should I test hypothesis #1 first, or do you have a different theory?"

**Don't skip this phase.** Writing down hypotheses prevents tunnel vision.

---

### Phase 3: TEST - Validate Hypotheses

**Design tests to prove/disprove each hypothesis.**

**For each hypothesis, determine the fastest way to test it**:

```markdown
### Phase 3: TEST

**Testing Hypothesis #1: [hypothesis]**

**Test method**:
- [Specific action to take to validate]

**Executing test**:
[Use Read, Grep, Bash, or Browser tools to investigate]

**Result**:
- ✅ Confirmed: [Evidence found]
- ❌ Ruled out: [Evidence contradicts this]
- ⚠️ Partial: [Mixed evidence, need more testing]

**Findings**:
[What we learned from this test]

---

**Testing Hypothesis #2: [hypothesis]**
[Repeat above]

---
```

**Test Methods by Bug Type**:

| Hypothesis Type | How to Test |
|-----------------|-------------|
| "Function not called" | Add console.log, check if it fires |
| "Wrong data returned" | Log the data, inspect actual values |
| "Auth check missing" | Read the server action code, verify auth validation exists |
| "Database constraint" | Check migration files, inspect schema |
| "Race condition" | Add delays, check timing of async calls |
| "Wrong component rendered" | React DevTools component tree inspection |

**Evidence-based testing**:
- Use Read tool to check actual code
- Use Grep to find relevant functions/imports
- Use Bash to run tests, check logs
- Use Browser tools for runtime inspection

**Keep testing until ONE hypothesis is confirmed as root cause.**

---

### Phase 4: FIX - Implement Solution

**Only execute this phase once root cause is identified.**

**Before writing code**:

1. **Confirm root cause**:
   - "The root cause is: [specific problem]"
   - "Evidence: [what we found in testing]"
   - "The fix: [what needs to change]"

2. **Plan minimal fix**:
   - Don't refactor everything
   - Fix the specific issue
   - Add test to prevent regression (if appropriate)

3. **Execute fix**:

```markdown
### Phase 4: FIX

**Root cause identified**:
[Specific technical problem]

**Fix implemented**:
- File: [path to file]
- Change: [what was modified]
- Why: [how this addresses root cause]

**Verification**:
- [ ] Original symptom is gone
- [ ] No new errors introduced
- [ ] Test added (if applicable)

**Testing the fix**:
[Specific steps to verify fix works]

**Result**:
✅ Bug resolved
❌ Fix didn't work (return to Phase 2 with new evidence)

---
```

**After fix verified**, document the bug:

---

### Step 5: Document in Architecture

**Use Write tool to APPEND to `.shipkit-lite/architecture.md`**:

```markdown
---

## Bug Fix - [Feature/Component] - [Date]

**Symptom**: [What was broken]

**Root cause**: [Technical problem that caused it]

**Fix**: [What was changed]

**File(s)**: [Paths to modified files]

**Lesson learned**: [Pattern to avoid in future, or check to add]

**Prevention**: [How to prevent this bug type in future]

---
```

**Example documentation**:

```markdown
---

## Bug Fix - Recipe Sharing - 2025-12-28

**Symptom**: Users couldn't share recipes - got 500 error when clicking Share button

**Root cause**: Server Action `shareRecipe()` had no auth validation, threw exception when accessing `user.id` with null user

**Fix**: Added `requireAuth()` check at start of Server Action before accessing user data

**File(s)**:
- `app/actions/share-recipe.ts` - Added auth check

**Lesson learned**: All Server Actions that access user data need auth validation

**Prevention**: Template for Server Actions should include auth check boilerplate

---
```

**Why document bugs?**
- Future debugging reference (similar bugs → check past fixes)
- Team learning (avoid same mistakes)
- Architecture memory (patterns to enforce)

---

## What Makes This "Lite"

**Included**:
- ✅ 4-phase systematic methodology
- ✅ Evidence gathering before guessing
- ✅ Hypothesis ranking
- ✅ Test-driven investigation
- ✅ Minimal targeted fixes
- ✅ Bug documentation in architecture.md

**Not included** (vs full dev-systematic-debugging):
- ❌ Git bisect automation
- ❌ Performance profiling
- ❌ Memory leak detection
- ❌ Distributed tracing
- ❌ Integration test harness
- ❌ Regression test suite generation

**Philosophy**: Get to root cause fast, fix it cleanly, document it. Good enough for POC/MVP debugging.

---

## Integration with Other Skills

**Before debug-systematically-lite**:
- `/lite-implement` - May auto-invoke this when tests fail
- `/lite-quality-confidence` - May auto-invoke when verification fails

**During debug-systematically-lite**:
- May read: `.shipkit-lite/specs/active/[feature].md` (expected behavior)
- May read: `.shipkit-lite/implementations.md` (current code context)
- May read: `.shipkit-lite/stack.md` (tech stack debugging tips)

**After debug-systematically-lite**:
- `/lite-architecture-memory` - If fix reveals architectural pattern to remember
- `/lite-quality-confidence` - Verify fix didn't break other things
- `/lite-implement` - Continue implementation after fix

---

## Context Files This Skill Reads

**Optional context** (load if helpful):
- `.shipkit-lite/specs/active/[feature].md` - Expected behavior
- `.shipkit-lite/implementations.md` - Current code
- `.shipkit-lite/stack.md` - Tech stack
- `.shipkit-lite/architecture.md` - Past bug patterns

**None are required.** Can debug from zero context.

---

## Context Files This Skill Writes

**Write Strategy**: **APPEND** (preserves all historical bug documentation)

**Updates**:
- `.shipkit-lite/architecture.md` - Appends bug documentation after each fix

**Why APPEND?**
- Builds architectural memory of bug patterns over time
- Enables pattern recognition (similar bugs → check past fixes)
- Preserves team learning history
- Chronological bug log helps identify recurring issues
- Referenced by future debugging sessions to avoid repeated mistakes

---

## Success Criteria

Debug session is complete when:
- [ ] Root cause identified with evidence
- [ ] Fix implemented and verified
- [ ] Original symptom gone
- [ ] No new errors introduced
- [ ] Bug documented in architecture.md
- [ ] User can demonstrate feature works

---

## Common Debugging Scenarios

### Scenario 1: API Call Failing

```
User: "The share button isn't working"

Phase 1 - OBSERVE:
- Network tab shows: 500 error on POST /api/share
- Response body: "Cannot read property 'id' of null"
- Browser console: No client errors
- Server logs: Stack trace points to shareRecipe function

Phase 2 - HYPOTHESIZE:
1. Missing auth check (most likely - null user)
2. Database constraint violation (possible)
3. Missing form data (less likely - error says null user)

Phase 3 - TEST:
- Read app/actions/share-recipe.ts
- Find: No auth validation, directly accesses user.id
- Confirmed: Hypothesis #1 is correct

Phase 4 - FIX:
- Add requireAuth() at start of function
- Verify: Share button now works
- Document: Append to architecture.md
```

### Scenario 2: UI Not Rendering

```
User: "Recipe list is blank"

Phase 1 - OBSERVE:
- Browser console: "Cannot read property 'map' of undefined"
- Component: RecipeList.tsx
- Network tab: GET /api/recipes returns []
- Expected: Should show sample recipes

Phase 2 - HYPOTHESIZE:
1. Component expects array but gets undefined (most likely)
2. API returns empty array incorrectly (possible)
3. Conditional rendering bug (less likely)

Phase 3 - TEST:
- Read components/RecipeList.tsx
- Find: recipes.map() called without null check
- API actually returns null on first load
- Confirmed: Hypothesis #1

Phase 4 - FIX:
- Change: recipes?.map() or default to []
- Verify: List renders empty state gracefully
- Document: "UI components should handle null/undefined data"
```

### Scenario 3: Build Error

```
User: "Build is failing"

Phase 1 - OBSERVE:
- Terminal: "Module not found: 'lucide-react'"
- Error in: components/Icon.tsx
- Recent change: Added new icon imports

Phase 2 - HYPOTHESIZE:
1. Package not installed (most likely)
2. Import path wrong (possible)
3. Version mismatch (less likely)

Phase 3 - TEST:
- Check package.json: lucide-react is listed
- Check node_modules: lucide-react folder missing
- Confirmed: Hypothesis #1

Phase 4 - FIX:
- Run: npm install
- Verify: Build succeeds
- Document: "After adding dependencies, run install"
```

---

## Tips for Effective Debugging

**Resist the urge to fix immediately**:
- Observation phase is fastest in the long run
- 5 minutes of evidence gathering saves 30 minutes of wrong fixes

**Use browser/server logs first**:
- Errors tell you exactly what's wrong
- Stack traces point to exact lines
- Network tab shows what data is moving

**Narrow the scope**:
- Binary search: Is it client or server?
- Is it data, code, or infrastructure?
- When did it last work?

**Document even "obvious" bugs**:
- Future you will forget
- Team members hit the same issues
- Patterns emerge over time

**When to upgrade to full /dev-systematic-debugging**:
- Production incidents requiring RCA
- Performance issues needing profiling
- Intermittent bugs requiring statistical analysis
- Complex distributed system debugging
- Regression requiring git bisect

---

## Suggest Next Skill at Completion

**After documenting the bug fix, suggest**:

**If debugging during implementation**:
```
✅ Bug fixed and documented

📁 Updated: .shipkit-lite/architecture.md
🐛 Root cause: [brief description]
🔧 Fix: [brief description]

👉 Next: /lite-implement
   Continue implementation where you left off

Ready to continue?
```

**If debugging after implementation**:
```
✅ Bug fixed and documented

📁 Updated: .shipkit-lite/architecture.md
🐛 Root cause: [brief description]
🔧 Fix: [brief description]

👉 Next: /lite-quality-confidence
   Verify this fix didn't break other things

Ready to verify?
```

**If architectural pattern discovered**:
```
✅ Bug fixed and documented

📁 Updated: .shipkit-lite/architecture.md
🐛 Root cause: [brief description]
🔧 Fix: [brief description]

💡 This fix reveals a pattern: [pattern description]

👉 Consider: /lite-architecture-memory
   Log this pattern to prevent future bugs

Document the pattern?
```

---

## The Golden Rule

**Evidence → Hypothesis → Test → Fix**

Never skip phases. Never guess before observing. Never fix before confirming root cause.

Systematic debugging is slower at first, but 10x faster overall because you fix the real problem the first time.

---

**Remember**: POC debugging prioritizes speed, but systematic beats random every time. Spend 5 minutes investigating, save 30 minutes of wrong fixes.
