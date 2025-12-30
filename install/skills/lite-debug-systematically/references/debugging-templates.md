# Debugging Templates Reference

Complete templates for each phase of systematic debugging used by `/lite-debug-systematically`.

---

## Evidence Collection Template

Use this template in Phase 1 to gather all observable facts before forming hypotheses.

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

## Where to Look for Evidence

| Symptom Type | Check These |
|--------------|-------------|
| UI not rendering | Browser console, React errors, component tree |
| API call failing | Network tab (status, headers, response), server logs |
| Authentication issues | Auth middleware logs, session/token validity |
| Database errors | Server logs, query output, migration status |
| Build failures | Terminal output, dependency versions |
| Styling broken | Browser DevTools, CSS specificity, Tailwind classes |

---

## Hypothesize Template

Use this template in Phase 2 to list possible causes ranked by likelihood based on evidence.

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

## Common Bug Pattern Hypotheses

| Evidence | Likely Hypotheses |
|----------|-------------------|
| 500 error in API call | Missing error handling, unhandled exception, database constraint violation |
| 401/403 error | Missing auth check, expired token, insufficient permissions |
| Network request not sent | Missing event handler, form not submitting, validation blocking |
| Blank screen | Uncaught exception in component, missing data causing crash |
| Infinite loop/hang | Missing dependency in useEffect, recursive call, circular reference |
| Styling not applied | CSS specificity conflict, Tailwind not compiling, typo in class name |

---

## Test Template

Use this template in Phase 3 to systematically validate each hypothesis.

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

## Test Methods by Bug Type

| Hypothesis Type | How to Test |
|-----------------|-------------|
| "Function not called" | Add console.log, check if it fires |
| "Wrong data returned" | Log the data, inspect actual values |
| "Auth check missing" | Read the server action code, verify auth validation exists |
| "Database constraint" | Check migration files, inspect schema |
| "Race condition" | Add delays, check timing of async calls |
| "Wrong component rendered" | React DevTools component tree inspection |

---

## Fix Template

Use this template in Phase 4 after root cause is confirmed.

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

---

## Documentation Template for Architecture.md

After fixing the bug, append this to `.shipkit-lite/architecture.md`:

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

## Documentation Example

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
