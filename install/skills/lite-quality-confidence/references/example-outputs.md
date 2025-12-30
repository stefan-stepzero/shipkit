# Example Quality Check Outputs

Complete example outputs showing report format and different scenarios.

---

## Full Quality Check Report Example

**File format** (append to `.shipkit-lite/quality-checks/[feature-name].md`):

```markdown
---
Quality Check Run: [YYYY-MM-DD HH:MM:SS]
Status: [PASSED / FAILED]
Gaps: [N blockers, M recommended, P nice-to-have]
---

🔍 Quality Check: [Feature Name]

════════════════════════════════════════════════════

SCOPE

**Spec**: .shipkit-lite/specs/active/[feature-name].md
**Files checked**:
  • [file-path-1]
  • [file-path-2]
  • [file-path-3]

════════════════════════════════════════════════════

UI COMPONENT CHECKLIST ([ComponentName] - [file-path])

Loading States:
  ✓ Loading state variable (line 47: isLoading)
  ✓ Spinner/skeleton UI (line 89: <Spinner />)
  ✓ Disabled buttons during load (line 102: disabled={isLoading})

Error Handling:
  ✓ Catch blocks with user errors (line 134: catch block with toast)
  ✗ Error boundaries (NOT FOUND: no ErrorBoundary component)
  ✓ Toast/alert on errors (line 137: toast.error())

Success Feedback:
  ✓ Success message (line 142: toast.success())
  ✓ Visual confirmation (line 145: checkmark icon)

Accessibility:
  ✓ aria-label on buttons (line 67: aria-label="Share recipe")
  ✓ Keyboard support (line 78: onKeyDown handler)
  ⚠ Focus management (PARTIAL: focus set, but not restored)
  ✗ Color contrast (NOT VERIFIED: manual check needed)

Empty States:
  ✗ Empty data handling (NOT FOUND: no check for empty recipe)
  ✗ No data message (NOT FOUND: what if recipe deleted?)

════════════════════════════════════════════════════

API/SERVER ACTION CHECKLIST (shareRecipe - [file-path])

Input Validation:
  ✓ Zod schema validation (line 12: RecipeShareSchema.parse())
  ✓ Type checking (line 15: typeof recipeId === 'string')

Auth Checks:
  ✓ User authentication (line 23: await getUser())
  ✗ Permission checks (NOT FOUND: no ownership verification)
  ✓ Unauthorized handling (line 26: throw if !user)

Error Handling:
  ✓ Try/catch blocks (line 31: try/catch)
  ✓ Proper error messages (line 45: descriptive errors)
  ⚠ HTTP status codes (PARTIAL: throws errors, status implicit)

Rate Limiting:
  ✗ Rate limit middleware (NOT FOUND: no rate limiting)
  ✗ Throttling (NOT FOUND: could spam share action)

Logging:
  ✗ Error logging (NOT FOUND: no Sentry/logging service)
  ✗ Audit logs (NOT FOUND: no record of share actions)

Database Operations:
  ✓ Database transaction (line 38: supabase.from().update())
  ✓ Error handling on DB calls (line 42: handles DB errors)

════════════════════════════════════════════════════

ACCEPTANCE CRITERIA (from spec)

✓ Toggle generates unique token (crypto.randomUUID() line 23)
✓ Copy-to-clipboard works (navigator.clipboard line 56)
✓ Toggle off revokes access (delete token line 78)
⚠ Network failure handling (PARTIAL: catch block exists, no retry)
✗ Token generation timeout (NOT HANDLED: no timeout logic)
✗ Concurrent share attempts (NOT HANDLED: race condition possible)

════════════════════════════════════════════════════

GAPS SUMMARY

🚨 7 gaps found:

UI Issues (3):
  1. Missing: Error boundary component
  2. Missing: Empty state handling (deleted/missing recipe)
  3. Incomplete: Focus management (not restored after actions)

API/Security Issues (3):
  4. Missing: Ownership verification (can anyone share any recipe?)
  5. Missing: Rate limiting (spam protection)
  6. Missing: Error logging/monitoring

Edge Cases (1):
  7. Missing: Token generation timeout handling

════════════════════════════════════════════════════

READY TO SHIP?

❌ NO - Address 7 gaps before shipping

**Blockers** (must fix):
  • Ownership verification (security issue)
  • Rate limiting (abuse prevention)

**Recommended** (should fix):
  • Error boundary (better UX)
  • Empty state handling (edge case)
  • Error logging (observability)
  • Token timeout (edge case)
  • Focus management (accessibility)

════════════════════════════════════════════════════

NEXT STEPS

1. Fix blocker gaps (ownership + rate limiting)
2. Fix recommended gaps (5 items)
3. Run `/lite-quality-confidence` again to verify
4. If passed → Move spec to implemented/

Ready to fix gaps, or proceed anyway? (I recommend fixing blockers first)
```

**Write strategy**: **APPEND** to `.shipkit-lite/quality-checks/[feature-name].md`
- Each run appends a timestamped entry
- Preserves history of all quality checks
- Shows progression: initial gaps → fixes → re-check → passed
- Creates audit trail for "ready to ship" decisions

**Example file after 3 runs**:

```markdown
---
Quality Check Run: 2025-01-15 10:30:00
Status: FAILED
Gaps: 2 blockers, 5 recommended, 0 nice-to-have
---
[Full report from first run...]

---
Quality Check Run: 2025-01-15 14:45:00
Status: FAILED
Gaps: 0 blockers, 2 recommended, 0 nice-to-have
---
[Full report from second run - blockers fixed...]

---
Quality Check Run: 2025-01-15 16:20:00
Status: PASSED
Gaps: 0 blockers, 0 recommended, 0 nice-to-have
---
[Full report from third run - all gaps addressed...]
```

---

## Terminal Output Template

**Structure**:

```
🔍 Quality Check: [Feature Name]

════════════════════════════════════════════════════

SCOPE
**Spec**: [spec-path]
**Files checked**: [list]

════════════════════════════════════════════════════

UI COMPONENT CHECKLIST ([ComponentName] - [file])

Loading States:
  [✓/✗] Loading state variable [line N: code snippet OR "NOT FOUND"]
  [✓/✗] Spinner/skeleton UI [line N OR "NOT FOUND"]
  [✓/✗] Disabled buttons [line N OR "NOT FOUND"]

Error Handling:
  [✓/✗] Catch blocks [line N OR "NOT FOUND"]
  [✓/✗] Error boundaries [line N OR "NOT FOUND"]
  [✓/✗] User-facing errors [line N OR "NOT FOUND"]

Success Feedback:
  [✓/✗] Success messages [line N OR "NOT FOUND"]
  [✓/✗] Visual indicators [line N OR "NOT FOUND"]

Accessibility:
  [✓/✗] aria-label [line N OR "NOT FOUND"]
  [✓/✗] Keyboard support [line N OR "NOT FOUND"]
  [✓/✗] Focus management [line N OR "NOT FOUND"]

Empty States:
  [✓/✗] Empty data checks [line N OR "NOT FOUND"]
  [✓/✗] No data messages [line N OR "NOT FOUND"]

════════════════════════════════════════════════════

API/SERVER ACTION CHECKLIST ([ActionName] - [file])

Input Validation:
  [✓/✗] Zod validation [line N OR "NOT FOUND"]
  [✓/✗] Type checking [line N OR "NOT FOUND"]

Auth Checks:
  [✓/✗] User authentication [line N OR "NOT FOUND"]
  [✓/✗] Permission checks [line N OR "NOT FOUND"]
  [✓/✗] Unauthorized handling [line N OR "NOT FOUND"]

Error Handling:
  [✓/✗] Try/catch blocks [line N OR "NOT FOUND"]
  [✓/✗] Error messages [line N OR "NOT FOUND"]

Rate Limiting:
  [✓/✗] Rate limit [line N OR "NOT FOUND"]
  [✓/✗] Throttling [line N OR "NOT FOUND"]

Logging:
  [✓/✗] Error logging [line N OR "NOT FOUND"]
  [✓/✗] Audit logs [line N OR "NOT FOUND"]

Database Operations:
  [✓/✗] Transactions [line N OR "NOT FOUND"]
  [✓/✗] Error handling [line N OR "NOT FOUND"]

════════════════════════════════════════════════════

FORM CHECKLIST ([FormName] - [file])

Validation:
  [✓/✗] Client validation [line N OR "NOT FOUND"]
  [✓/✗] Server validation [line N OR "NOT FOUND"]
  [✓/✗] Error messages [line N OR "NOT FOUND"]

Submit States:
  [✓/✗] isSubmitting state [line N OR "NOT FOUND"]
  [✓/✗] Disabled button [line N OR "NOT FOUND"]

Error Display:
  [✓/✗] Field errors [line N OR "NOT FOUND"]
  [✓/✗] Form errors [line N OR "NOT FOUND"]

Accessibility:
  [✓/✗] Label association [line N OR "NOT FOUND"]
  [✓/✗] Required indicators [line N OR "NOT FOUND"]
  [✓/✗] Error announcements [line N OR "NOT FOUND"]

════════════════════════════════════════════════════

ACCEPTANCE CRITERIA (from spec)

[✓/⚠/✗] [AC 1] [(code evidence OR gap description)]
[✓/⚠/✗] [AC 2] [(code evidence OR gap description)]
[✓/⚠/✗] [AC 3] [(code evidence OR gap description)]

════════════════════════════════════════════════════

GAPS SUMMARY

[🚨/✅] [N] gaps found:

Blockers (must fix):
  [List critical security/data integrity gaps]

Recommended (should fix):
  [List UX/accessibility/observability gaps]

Nice to have (optional):
  [List minor improvements]

════════════════════════════════════════════════════

READY TO SHIP?

[✅ YES / ❌ NO] - [Reason]

**Next**: [Action based on pass/fail]

════════════════════════════════════════════════════
```

---

## Suggested Next Actions (Different Scenarios)

### Scenario 1: Quality Check PASSED (no blockers)

```
✅ Quality check PASSED!

**Summary**: All critical items addressed. [N] minor gaps (optional).

**Next**:
  Option 1: Move spec to implemented/ folder (marks feature complete)
  Option 2: Address minor gaps first
  Option 3: Start next feature

Move .shipkit-lite/specs/active/[feature].md to specs/implemented/?
```

### Scenario 2: Quality Check FAILED (blockers exist)

```
❌ Quality check FAILED - [N] blockers found

**Critical gaps**:
  • [Gap 1]
  • [Gap 2]

**Next**:
  Option 1: Fix blockers (I can help implement)
  Option 2: Review gap details again
  Option 3: Proceed anyway (NOT recommended - security/data risk)

What would you like to do?
```

### Scenario 3: After Moving Spec to Implemented

```
✅ Spec moved to implemented/

**Status**: [Feature] is complete!

**Next**:
  • Update progress tracking? (Run `/lite-work-memory`)
  • Start next feature? (Run `/lite-spec` or `/lite-plan`)
  • Document this component? (Run `/lite-component-knowledge`)
```
