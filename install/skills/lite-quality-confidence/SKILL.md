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

**Write strategy**: **APPEND** to `.shipkit-lite/quality-checks/[feature-name].md`
- Each run appends a timestamped entry
- Preserves history of all quality checks
- Shows progression: initial gaps → fixes → re-check → passed
- Creates audit trail for "ready to ship" decisions

**See `references/example-outputs.md` for:**
- Complete report format with all sections
- Example output showing 7 gaps found (UI, API, edge cases)
- Multi-run audit trail example (initial → fixes → passed)

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

## Quality Checklists

**See `references/checklists.md` for complete quality checklists:**
- **UI Component Checklist** - Loading States, Error Handling, Success Feedback, Accessibility, Empty States
- **API/Server Action Checklist** - Input Validation, Auth Checks, Error Handling, Rate Limiting, Logging, Database Operations
- **Form Checklist** - Client/Server Validation, Submit States, Field Errors, Reset, Accessibility

Each checklist includes:
- WHY the item matters
- Patterns to search for (regex-compatible)
- Examples of good code
- Marking criteria (✓ / ⚠ / ✗)
- Gap categories (Blockers, Recommended, Nice to Have)

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

## When This Skill Integrates with Others

### Before This Skill

- `/lite-implement` - Implementation must be complete
  - **When**: User has finished coding the feature
  - **Why**: Can't check quality of incomplete code
  - **Trigger**: User says "ready to ship", "is this done?", or "check quality"

- `/lite-spec` - Provides acceptance criteria for verification
  - **When**: During spec creation (before implementation)
  - **Why**: Quality check verifies implementation matches spec acceptance criteria
  - **Trigger**: Quality check reads active spec to extract requirements

### After This Skill

**If PASSED (no blockers)**:

- Move spec to implemented/ - Feature completion workflow
  - **When**: All blockers and recommended items addressed
  - **Why**: Marks feature as production-ready
  - **Trigger**: Quality check passes with ✅ status

- `/lite-work-memory` - Update progress tracking
  - **When**: After moving spec to implemented/
  - **Why**: Document completed work and learnings
  - **Trigger**: User confirms they want to track completion

- `/lite-spec` or `/lite-plan` - Start next feature
  - **When**: Current feature complete
  - **Why**: Continue development workflow with next priority
  - **Trigger**: User wants to move on to next work item

**If FAILED (blockers exist)**:

- `/lite-implement` - Fix quality gaps
  - **When**: Blockers or recommended items found
  - **Why**: Address missing error handling, validation, auth checks, etc.
  - **Trigger**: User wants to fix gaps instead of shipping with issues

- `/lite-debug-systematically` - Investigate complex issues
  - **When**: Quality gaps reveal deeper architectural problems
  - **Why**: Root cause may require systematic debugging
  - **Trigger**: Simple fixes won't resolve quality issues

- Re-run `/lite-quality-confidence` - Verify fixes
  - **When**: After addressing quality gaps
  - **Why**: Confirm all issues resolved before shipping
  - **Trigger**: User believes gaps are fixed and wants re-validation

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

## Output Format

**See `references/example-outputs.md` for:**
- Complete terminal output template structure
- All checklist sections with [✓/✗] markers
- Gap summary format
- Ready to ship determination
- Suggested next actions for PASSED/FAILED scenarios

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
