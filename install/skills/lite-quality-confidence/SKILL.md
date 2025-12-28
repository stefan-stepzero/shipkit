---
name: lite-quality-confidence
description: Pre-ship quality verification that scans implementation files against comprehensive checklists (UI, API, Forms) to detect missing error handling, loading states, accessibility, validation, auth checks, and rate limiting. Blocks shipping if gaps exist. Use when user asks "ready to ship?", "is this done?", or before moving specs to implemented/.
---

# quality-confidence-lite - Pre-Ship Quality Verification

**Purpose**: Block feature completion if quality gaps exist. Scans implementation files for common missing items (loading states, error handling, accessibility, validation, auth checks, rate limiting) against acceptance criteria from specs. Reports gaps with specific line numbers or "NOT FOUND" markers.

---

## When to Invoke

**User triggers**:
- "Ready to ship?"
- "Is this feature complete?"
- "Check quality"
- "Can I mark this done?"
- "Verify implementation"

**Before**:
- Moving spec from `.shipkit-lite/specs/active/` to `.shipkit-lite/specs/implemented/`
- Marking feature as "done" in progress tracking
- Creating PR or merging feature branch
- User says "this is finished"

---

## Prerequisites

**Required**:
- Active spec exists: `.shipkit-lite/specs/active/[feature-name].md`
- Implementation files exist (components, routes, actions)

**Optional but helpful**:
- Stack info: `.shipkit-lite/stack.md` (determines checklist variants)
- Implementation notes: `.shipkit-lite/implementations.md` (finds file paths faster)

---

## Process

### Step 1: Identify Feature to Check

**Before scanning, ask user**:

**Question 1**: "Which feature are you checking?"
- If only 1 active spec → Use that one
- If multiple active specs → List them, let user choose
- Show: `ls .shipkit-lite/specs/active/*.md`

**Question 2**: "Which files implement this feature?"
- Ask user for file paths (comma-separated)
- If user unsure → Offer to scan implementations.md for hints
- If implementations.md exists → Extract file paths from relevant section

**Example interaction**:
```
User: "Ready to ship recipe sharing"

Claude: "I see 1 active spec: recipe-sharing.md

Which files implement this feature? (comma-separated paths)

Hint: Check your component files, routes, server actions, API routes"

User: "src/app/recipes/[id]/page.tsx, src/app/actions/share.ts"

Claude: "Got it. Checking:
  • src/app/recipes/[id]/page.tsx
  • src/app/actions/share.ts

Starting quality scan..."
```

---

### Step 2: Read Context

**Read these files to understand requirements**:

```bash
# Feature spec (acceptance criteria)
.shipkit-lite/specs/active/[feature-name].md

# Stack info (determine checklist type)
.shipkit-lite/stack.md (optional)

# Implementation files (user-provided paths)
[file-path-1]
[file-path-2]
[file-path-3]
```

**Token budget**: Keep file reading focused (read only specified files, not entire codebase).

---

### Step 3: Determine Applicable Checklists

**Based on file types and stack, choose which checklists to apply**:

| File Type | Checklist to Use |
|-----------|------------------|
| `.tsx`, `.jsx` with JSX syntax | UI Component Checklist |
| `/app/actions/*.ts`, `/api/` routes | API/Server Action Checklist |
| Files with `<form>` or `useForm` | Form Checklist |
| `.ts`, `.js` without UI | API/Server Action Checklist |

**Multiple checklists can apply to one file** (e.g., a page with form uses UI + Form checklists).

---

### Step 4: Scan Implementation Files

**For each file, scan for patterns using grep/regex**:

**How to scan**:
1. Read file content (already done in Step 2)
2. Search for patterns (case-insensitive)
3. Mark ✓ if found, ✗ if NOT FOUND
4. Record line numbers where found (for ✓ items)

**Example scan logic**:
```
Looking for: Loading states
Pattern: isLoading|isPending|loading|pending
Result: FOUND at line 47: "const [isLoading, setIsLoading] = useState(false)"
Mark: ✓
```

```
Looking for: Rate limiting
Pattern: rateLimit|rate-limit|throttle
Result: NOT FOUND
Mark: ✗
```

---

### Step 5: Compare Against Acceptance Criteria

**Read acceptance criteria from spec**:
- Extract "Acceptance Criteria" section from spec
- For each criterion, determine if implementation satisfies it
- Mark: ✓ (satisfied), ⚠ (partial), ✗ (missing)

**How to evaluate**:
- Manual review (read code logic vs requirement)
- Check for relevant functions/components
- Look for edge case handling mentioned in spec

**Example**:
```
AC: "Toggle generates unique token"
Code check: Search for token generation logic
Found: crypto.randomUUID() in share.ts line 23
Mark: ✓

AC: "Network failure shows retry option"
Code check: Search for retry logic
Found: catch block exists, but no retry UI
Mark: ⚠ Partially handled (error caught, no retry option)
```

---

### Step 6: Generate Gap Report (Terminal + File)

**Output comprehensive report to:**
1. **Terminal** (immediate feedback)
2. **File** (append to audit log): `.shipkit-lite/quality-checks/[feature-name].md`

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

### Step 7: Determine Pass/Fail

**Passing criteria**:
- ALL acceptance criteria satisfied (✓)
- NO critical gaps (security, auth, data integrity)
- All blockers addressed

**Failing criteria** (any of these fails the check):
- ✗ Auth checks missing
- ✗ Input validation missing
- ✗ Critical edge cases not handled
- ⚠ Partial handling of critical requirements

**Categories of gaps**:
1. **Blockers** (MUST fix before shipping):
   - Security issues (auth, permissions, injection)
   - Data integrity issues (validation, race conditions)
   - Critical user flows broken

2. **Recommended** (SHOULD fix before shipping):
   - Accessibility gaps
   - Error handling gaps
   - Logging/observability gaps
   - Edge case handling

3. **Nice to have** (Can defer):
   - Color contrast checks (needs manual verification)
   - Performance optimization
   - Advanced error recovery

---

### Step 8: Write Audit Log & Offer Next Actions

**After generating report, write to file**:
1. Create directory if needed: `.shipkit-lite/quality-checks/`
2. Append full report to: `.shipkit-lite/quality-checks/[feature-name].md`
3. Include timestamp header: `Quality Check Run: [YYYY-MM-DD HH:MM:SS]`
4. Include status summary: `Status: [PASSED/FAILED], Gaps: [counts]`

**Then offer next actions:**

**If PASSED (no gaps or only "nice to have" gaps)**:
```
✅ Quality check PASSED!

**Summary**: All blockers and recommended items addressed.

**Logged to**: .shipkit-lite/quality-checks/[feature-name].md

**Next**: Move spec to implemented folder?
  • From: .shipkit-lite/specs/active/[feature].md
  • To: .shipkit-lite/specs/implemented/[feature].md

Proceed with moving spec? (yes/no)
```

**If user says yes**:
1. Move file: `specs/active/[feature].md` → `specs/implemented/[feature].md`
2. Append completion note to implementations.md (optional)
3. Suggest: "Feature complete! Update progress or start next feature?"

**If FAILED (blockers or recommended gaps exist)**:
```
❌ Quality check FAILED

**Gaps**: 7 items (2 blockers, 5 recommended)

**Logged to**: .shipkit-lite/quality-checks/[feature-name].md

**Next**: Fix gaps, then run `/lite-quality-confidence` again

**Or**: Proceed anyway (not recommended - blockers exist)

What would you like to do?
  1. Fix gaps now (I can help implement fixes)
  2. Review gap list again
  3. Proceed anyway (skip quality gate)
```

---

## UI Component Checklist (INLINE)

**Scan for these patterns in `.tsx`, `.jsx` files**:

### Loading States
**Why**: Users need feedback during async operations.

**Patterns to search**:
- `isLoading|isPending|loading|pending` (state variables)
- `<Spinner|<Skeleton|<Loading|loading=` (UI indicators)
- `disabled={.*loading|disabled={.*pending` (disabled buttons)

**Examples of GOOD code**:
```tsx
const [isLoading, setIsLoading] = useState(false)
{isLoading && <Spinner />}
<button disabled={isLoading}>Submit</button>
```

**Mark ✓ if**: At least 2 of 3 patterns found (state + UI indicator + disabled button).

**Mark ✗ if**: No loading state management found.

---

### Error Handling
**Why**: Users need to know when things go wrong.

**Patterns to search**:
- `catch.*toast|catch.*alert|catch.*setError` (error display)
- `ErrorBoundary|error-boundary` (React error boundaries)
- `toast\.error|alert\(.*error` (user-facing error messages)

**Examples of GOOD code**:
```tsx
try {
  await shareRecipe(id)
  toast.success('Recipe shared!')
} catch (error) {
  toast.error('Failed to share: ' + error.message)
}

<ErrorBoundary fallback={<ErrorFallback />}>
  <RecipeContent />
</ErrorBoundary>
```

**Mark ✓ if**: Catch blocks exist with user-facing error display.

**Mark ✗ if**: No error handling or silent failures (catch without user feedback).

---

### Success Feedback
**Why**: Users need confirmation that actions succeeded.

**Patterns to search**:
- `toast\.success|alert.*success|setSuccess` (success messages)
- `checkmark|check-circle|success-icon` (visual indicators)
- `color.*green|bg-green|text-green` (success styling)

**Examples of GOOD code**:
```tsx
toast.success('Recipe shared successfully!')
<CheckCircleIcon className="text-green-500" />
```

**Mark ✓ if**: Success message or visual indicator found.

**Mark ✗ if**: No success feedback (user unsure if action worked).

---

### Accessibility
**Why**: Users with disabilities need equal access.

**Patterns to search**:
- `aria-label|aria-labelledby|aria-describedby` (screen reader labels)
- `onKeyDown|onKeyPress|onKeyUp` (keyboard support)
- `tabIndex|role=` (focus management)
- `focus\(|blur\(|\.focus|\.blur` (programmatic focus)

**Examples of GOOD code**:
```tsx
<button aria-label="Share recipe">
  <ShareIcon />
</button>

<input onKeyDown={handleKeyDown} />

useEffect(() => {
  inputRef.current?.focus()
}, [])
```

**Mark ✓ if**: Interactive elements have aria-labels AND keyboard support.

**Mark ✗ if**: Icon buttons lack labels OR no keyboard handling.

**Manual checks** (can't automate):
- Color contrast (needs visual inspection)
- Screen reader testing

---

### Empty States
**Why**: Handle cases where data is missing.

**Patterns to search**:
- `if.*length === 0|if.*!.*length|if.*\.length < 1` (empty checks)
- `No.*found|No.*available|empty.*state` (empty messages)
- `placeholder|Empty|Nothing to show` (empty UI)

**Examples of GOOD code**:
```tsx
{recipes.length === 0 ? (
  <EmptyState message="No recipes found" />
) : (
  <RecipeList recipes={recipes} />
)}
```

**Mark ✓ if**: Conditional rendering for empty data.

**Mark ✗ if**: No empty state handling (blank screen if no data).

---

## API/Server Action Checklist (INLINE)

**Scan for these patterns in `/api/`, `/actions/`, server-side `.ts` files**:

### Input Validation
**Why**: Prevent invalid data from entering the system.

**Patterns to search**:
- `\.parse\(|\.safeParse\(|zod|Zod|z\.` (Zod validation)
- `typeof.*===|instanceof|Array\.isArray` (type checking)
- `validate|schema|Schema` (validation schemas)

**Examples of GOOD code**:
```ts
const RecipeShareSchema = z.object({
  recipeId: z.string().uuid(),
  userId: z.string()
})

const validated = RecipeShareSchema.parse(input)
```

**Mark ✓ if**: Zod schema validation OR explicit type checks found.

**Mark ✗ if**: No validation (directly using user input).

---

### Auth Checks
**Why**: Ensure user is authenticated and authorized.

**Patterns to search**:
- `getUser|getSession|auth\(|authenticate` (auth checks)
- `await.*user|await.*session` (async auth)
- `if.*!user|if.*!session|throw.*401|throw.*403` (auth enforcement)
- `role.*===|permission|can\(|authorize` (permission checks)

**Examples of GOOD code**:
```ts
const user = await getUser()
if (!user) {
  throw new Error('Unauthorized', { status: 401 })
}

// Check ownership
const recipe = await db.recipe.findUnique({ where: { id } })
if (recipe.userId !== user.id) {
  throw new Error('Forbidden', { status: 403 })
}
```

**Mark ✓ if**: User authentication AND ownership/permission checks found.

**Mark ⚠ if**: Authentication exists but no permission checks.

**Mark ✗ if**: No auth checks (publicly accessible).

---

### Error Handling
**Why**: Gracefully handle failures.

**Patterns to search**:
- `try.*catch|catch\s*\(` (try/catch blocks)
- `throw new Error|throw\s+\{|throw\s+new` (proper error throwing)
- `status.*:|statusCode|res\.status` (HTTP status codes for API routes)

**Examples of GOOD code**:
```ts
try {
  const result = await shareRecipe(id)
  return { success: true, data: result }
} catch (error) {
  console.error('Share failed:', error)
  throw new Error('Failed to share recipe', { status: 500 })
}
```

**Mark ✓ if**: Try/catch with proper error messages.

**Mark ✗ if**: No error handling (unhandled promise rejections).

---

### Rate Limiting
**Why**: Prevent abuse and spam.

**Patterns to search**:
- `rateLimit|rate-limit|RateLimit` (rate limit middleware)
- `throttle|Throttle|debounce` (throttling)
- `Ratelimit|upstash.*ratelimit` (rate limit libraries)

**Examples of GOOD code**:
```ts
import { Ratelimit } from '@upstash/ratelimit'

const ratelimit = new Ratelimit({
  redis: redis,
  limiter: Ratelimit.slidingWindow(10, '1 m')
})

const { success } = await ratelimit.limit(userId)
if (!success) {
  throw new Error('Rate limit exceeded', { status: 429 })
}
```

**Mark ✓ if**: Rate limit middleware or checks found.

**Mark ✗ if**: No rate limiting (vulnerable to spam).

**Note**: Not all actions need rate limiting (read-only operations OK). Focus on:
- Write operations (create, update, delete)
- Expensive operations (external API calls, heavy computation)
- Public endpoints

---

### Logging
**Why**: Observability and debugging.

**Patterns to search**:
- `console\.error|console\.warn|logger\.error` (error logging)
- `Sentry|sentry|captureException` (error tracking services)
- `log\(|logger\.|winston|pino` (logging libraries)
- `audit|auditLog|createAuditLog` (audit trails)

**Examples of GOOD code**:
```ts
import * as Sentry from '@sentry/nextjs'

try {
  await shareRecipe(id)
  auditLog.create({ action: 'share', userId, recipeId })
} catch (error) {
  console.error('Share failed:', error)
  Sentry.captureException(error)
  throw error
}
```

**Mark ✓ if**: Error logging AND audit logs for sensitive actions.

**Mark ⚠ if**: Console logging only (no external service).

**Mark ✗ if**: No logging (silent failures).

---

### Database Operations
**Why**: Ensure data integrity.

**Patterns to search**:
- `transaction|\.transaction\(|prisma\.\$transaction` (transactions)
- `\.create\(|\.update\(|\.delete\(|\.upsert\(` (DB operations)
- `catch.*database|catch.*db|PrismaClientKnownRequestError` (DB error handling)

**Examples of GOOD code**:
```ts
try {
  await db.$transaction([
    db.recipe.update({ where: { id }, data: { shared: true } }),
    db.shareToken.create({ data: { recipeId: id, token } })
  ])
} catch (error) {
  if (error instanceof PrismaClientKnownRequestError) {
    // Handle DB-specific errors
  }
  throw error
}
```

**Mark ✓ if**: DB operations with error handling.

**Mark ⚠ if**: DB operations without transactions (race conditions possible).

**Mark ✗ if**: DB operations without error handling.

---

## Form Checklist (INLINE)

**Scan for these patterns in files with `<form>`, `useForm`, `react-hook-form`**:

### Validation
**Why**: Ensure form data is valid before submission.

**Patterns to search**:
- `useForm|react-hook-form|register\(` (form library)
- `zodResolver|yupResolver|resolver:` (schema validation)
- `z\.object|z\.string|Yup\.object` (validation schemas)
- `errors\.|formState\.errors|error\.message` (error display)

**Examples of GOOD code**:
```tsx
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'

const schema = z.object({
  recipeName: z.string().min(3, 'Name too short'),
  ingredients: z.array(z.string()).min(1, 'Add at least one ingredient')
})

const { register, handleSubmit, formState: { errors } } = useForm({
  resolver: zodResolver(schema)
})

{errors.recipeName && <span>{errors.recipeName.message}</span>}
```

**Mark ✓ if**: Client-side validation (Zod + react-hook-form) AND server-side validation.

**Mark ⚠ if**: Client-side only (no server validation).

**Mark ✗ if**: No validation schema.

---

### Submit States
**Why**: Prevent double submissions, show progress.

**Patterns to search**:
- `isSubmitting|isPending|formState\.isSubmitting` (submit state)
- `disabled={.*isSubmitting|disabled={.*isPending` (disabled button)
- `onSubmit|handleSubmit` (submit handler)

**Examples of GOOD code**:
```tsx
const { handleSubmit, formState: { isSubmitting } } = useForm()

<form onSubmit={handleSubmit(onSubmit)}>
  <button disabled={isSubmitting}>
    {isSubmitting ? 'Saving...' : 'Save'}
  </button>
</form>
```

**Mark ✓ if**: Submit state tracked AND button disabled during submit.

**Mark ✗ if**: No submit state (can double-submit).

---

### Error Display
**Why**: Show validation errors to user.

**Patterns to search**:
- `errors\.|formState\.errors` (form errors)
- `error\.message|error\.type` (error details)
- `<span|<div|<p.*error|className.*error` (error UI)
- `setError|toast.*error` (manual error setting)

**Examples of GOOD code**:
```tsx
{errors.recipeName && (
  <span className="text-red-500">{errors.recipeName.message}</span>
)}

{formError && <div className="alert-error">{formError}</div>}
```

**Mark ✓ if**: Field-level errors AND form-level errors displayed.

**Mark ✗ if**: No error display (user doesn't know what's wrong).

---

### Accessibility
**Why**: Forms must be accessible to all users.

**Patterns to search**:
- `htmlFor|id=.*{|id="` (label association)
- `required|aria-required` (required field indicators)
- `aria-invalid|aria-describedby` (error announcements)
- `aria-live|role="alert"` (dynamic error announcements)

**Examples of GOOD code**:
```tsx
<label htmlFor="recipeName">
  Recipe Name <span aria-label="required">*</span>
</label>
<input
  id="recipeName"
  aria-invalid={!!errors.recipeName}
  aria-describedby={errors.recipeName ? 'name-error' : undefined}
  {...register('recipeName')}
/>
{errors.recipeName && (
  <span id="name-error" role="alert">
    {errors.recipeName.message}
  </span>
)}
```

**Mark ✓ if**: Labels associated (htmlFor) AND required indicators AND error announcements.

**Mark ✗ if**: Labels missing OR no required indicators.

---

## Scan Patterns Reference

**How to scan files for patterns**:

### Method 1: Grep-style Search (Recommended)
```
Read file content
For each checklist item:
  Search for pattern (case-insensitive, regex)
  If match found:
    Record line number
    Mark ✓
  Else:
    Mark ✗ NOT FOUND
```

### Method 2: Manual Code Review
For complex checks (acceptance criteria, edge cases):
- Read relevant code sections
- Evaluate logic against requirement
- Mark ✓ / ⚠ / ✗ based on judgment

**Example patterns**:

| Checklist Item | Search Pattern | Found Example |
|----------------|----------------|---------------|
| Loading state | `isLoading\|isPending\|loading` | `const [isLoading, setIsLoading]` |
| Error boundary | `ErrorBoundary\|error-boundary` | `<ErrorBoundary>` |
| Zod validation | `\.parse\(\|\.safeParse\(\|z\.` | `schema.parse(data)` |
| Auth check | `getUser\|getSession\|auth\(` | `const user = await getUser()` |
| Rate limiting | `rateLimit\|Ratelimit\|throttle` | `await ratelimit.limit(userId)` |
| Logging | `console\.error\|Sentry\|logger\.` | `Sentry.captureException(error)` |

---

## What Makes This "Lite"

**Included**:
- ✅ Comprehensive checklists (UI, API, Forms) inline in SKILL.md
- ✅ Pattern-based scanning (grep/regex)
- ✅ Acceptance criteria verification
- ✅ Terminal output with line numbers
- ✅ Audit log (appends to `.shipkit-lite/quality-checks/[feature].md`)
- ✅ Pass/fail determination
- ✅ Blocking quality gate (prevents shipping with gaps)
- ✅ Can move specs to implemented/ after passing

**Not included** (vs full quality-confidence):
- ❌ AST analysis (no code parsing, just pattern matching)
- ❌ Automated testing execution (doesn't run tests)
- ❌ Performance profiling (no benchmarks)
- ❌ Security vulnerability scanning (no static analysis tools)
- ❌ Test coverage metrics (assumes tests exist)
- ❌ Accessibility automated testing (no axe-core integration)
- ❌ External references (all checklists inline)

**Philosophy**: Catch common missing items with pattern matching. Good enough to prevent obvious gaps, not exhaustive security audit.

---

## Integration with Other Skills

**Before quality-confidence-lite**:
- `/lite-implement` - Feature implementation complete
- User believes feature is "done"

**After quality-confidence-lite**:

**If PASSED**:
- Suggest moving spec to implemented/ folder
- Suggest updating progress tracking
- Suggest starting next feature

**If FAILED**:
- Suggest fixing gaps (offer to help implement)
- Suggest running `/lite-implement` again to address gaps
- Re-run `/lite-quality-confidence` after fixes

---

## Context Files This Skill Reads

**Always reads**:
- `.shipkit-lite/specs/active/[feature].md` - Acceptance criteria
- Implementation files (user-provided paths)

**Conditionally reads**:
- `.shipkit-lite/stack.md` - Determine tech stack (if exists)
- `.shipkit-lite/implementations.md` - Find file paths (if user unsure)

---

## Context Files This Skill Writes

**Appends to** (write strategy: APPEND):
- `.shipkit-lite/quality-checks/[feature-name].md` - Quality check audit log
  - **When**: After each quality check run
  - **Content**: Full gap report with timestamp, status, and findings
  - **Why APPEND**: Creates audit trail showing quality progression over multiple runs (initial gaps → fixes → re-check → passed)
  - **Format**: Timestamped markdown entries separated by `---` dividers

**Can move files**:
- `.shipkit-lite/specs/active/[feature].md` → `.shipkit-lite/specs/implemented/[feature].md` (only if user confirms after passing)

**Never modifies**:
- Implementation files (read-only inspection)
- Stack, architecture files (read-only)

---

## Output Format Template

**Terminal output structure**:

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

## What to Suggest After Completion

**If quality check PASSED (no blockers)**:

```
✅ Quality check PASSED!

**Summary**: All critical items addressed. [N] minor gaps (optional).

**Next**:
  Option 1: Move spec to implemented/ folder (marks feature complete)
  Option 2: Address minor gaps first
  Option 3: Start next feature

Move .shipkit-lite/specs/active/[feature].md to specs/implemented/?
```

**If quality check FAILED (blockers exist)**:

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

**After moving spec to implemented/**:

```
✅ Spec moved to implemented/

**Status**: [Feature] is complete!

**Next**:
  • Update progress tracking? (Run `/lite-work-memory`)
  • Start next feature? (Run `/lite-spec` or `/lite-plan`)
  • Document this component? (Run `/lite-component-knowledge`)
```

---

## Special Notes

**This skill is a quality gate**:
- Blocks shipping if critical gaps exist
- Forces conversation about trade-offs
- Prevents common mistakes (no auth, no validation, no error handling)

**Design decisions**:
- Pattern-based (fast, simple, no AST parsing)
- All checklists inline (no external references)
- Dual output: Terminal (immediate) + file (audit trail)
- Appends to quality-checks/ (preserves history across runs)
- Can move specs to implemented/ after passing

**When to run**:
- Before marking feature "done"
- Before creating PR
- Before moving spec to implemented/
- When user says "ready to ship"

**What this catches**:
- Missing loading states (bad UX)
- Missing error handling (crashes)
- Missing auth checks (security holes)
- Missing validation (data corruption)
- Missing rate limiting (abuse vectors)
- Missing accessibility (exclusionary)
- Unhandled edge cases (bugs)

**What this doesn't catch**:
- Logic errors (requires tests)
- Performance issues (requires profiling)
- Security vulnerabilities (requires SAST tools)
- Visual bugs (requires screenshots)
- Complex race conditions (requires deep analysis)

**When to upgrade to full /quality-confidence**:
- Need automated test execution
- Need security vulnerability scanning
- Need performance benchmarks
- Need test coverage metrics
- Need CI/CD integration

---

**Remember**: This is a pre-ship checklist, not a substitute for testing. It catches common missing items via pattern matching. Always write tests for logic verification.
