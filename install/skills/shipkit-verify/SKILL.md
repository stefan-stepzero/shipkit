---
name: shipkit-verify
description: Verify and fix — review changes across 12 quality dimensions, auto-fix critical issues, loop up to 4 times. Use after a chunk of work or before commit.
argument-hint: "[scope or feature]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task
---

# shipkit-verify

Batch verification with auto-fix — Claude reviews your work across quality dimensions, fixes critical issues, re-verifies, and reports what remains.

**Fix-and-recheck loop.** Runs up to 4 passes: verify → fix → re-verify → fix. The relentless stop hook prevents early exit. User sees the final state after auto-remediation.

---

## When to Invoke

- `/verify` — review all recent changes
- `/verify <feature>` — focus on specific area
- "Check my work", "Am I ready to commit?"

**For deeper review:** If user asks for "deep check", "thorough review", or "really scrutinize this" → see [Deeper Review Option](#deeper-review-option) below.

---

## Session ID

Your session-start context includes `Session ID: {sid8}`.
Use this 8-character ID in all state file names below. If not found in session context, use `unknown`.

---

## Arguments

If `$ARGUMENTS` is provided (e.g. `/shipkit-verify auth module`), use it as the explicit verification scope. Skip scope detection and treat it as the answer to "What should I verify?".

If `$ARGUMENTS` is empty, proceed normally with automatic scope detection (git diff, session context).

---

## Process

### Step 1: Detect Scope

Determine what to verify:

```bash
# Get uncommitted changes
git diff --name-only HEAD

# If nothing uncommitted, check recent commits
git diff --name-only HEAD~3..HEAD
```

Also consider: What did Claude work on this session?

If unclear, ask: "What should I verify?"

### Step 1.1: Quick Pre-Scan (Before Loop)

Run a **lightweight first pass** across the 12 dimensions on the changed files only (no pattern ripple yet). This is a fast scan to surface the landscape of findings.

Present a summary to the user:

```
## Pre-Scan Summary

Found findings across these themes:

| # | Finding | L · I · E |
|---|---------|-----------|
| 1 | 🔴 Missing auth checks on 2 API routes | L:High · I:High · E:Low |
| 2 | 🔴 Broken import in Dashboard.tsx | L:High · I:High · E:Low |
| 3 | 🟡 Magic numbers in config (3 instances) | L:Low · I:Low · E:Low |
| 4 | 🟡 Missing loading states on admin pages | L:Medium · I:Medium · E:Medium |
| 5 | 🟢 console.logs left in (4 files) | L:Low · I:Low · E:Low |

**Any themes to dismiss?** I'll skip dismissed themes during the fix-and-verify loop.
(Reply "none" to proceed with all, or list numbers to dismiss)
```

**Wait for user response.** The user may:
- Dismiss themes: "dismiss 3 and 4" → those won't be flagged or fixed
- Dismiss none: "none" or "go" → proceed with everything
- Add context: "3 is intentional, 4 is low priority" → record the reasoning

### Step 1.2: Activate Relentless Loop

Create the relentless state file to prevent early exit:

```bash
mkdir -p .shipkit
```

Write `.shipkit/relentless-verify.{sid8}.local.md` — include dismissed themes in the body so the hook feeds them back on each iteration:

```markdown
---
skill: verify
iteration: 1
max_iterations: 4
enabled: true
completion_promise: "Zero 🔴 Critical and zero 🟡 Should Fix findings on re-verification (excluding dismissed themes). 🟢 Minor findings are noted but never fixed."
---
Verify and fix across 12 quality dimensions.
Fix all critical findings. Re-verify until clean or max iterations reached.

## Dismissed Themes (do not flag or fix)
- Magic numbers in config — user: "those are intentional"
- Missing loading states on admin pages — user: "low priority"
```

If user dismissed nothing, omit the Dismissed Themes section.

**This file activates the relentless stop hook.** Claude cannot stop until either:
- Zero critical findings remain, excluding dismissed themes (delete the state file, then stop)
- Max iterations (4) reached (hook auto-stops)

**During all subsequent verification passes, skip dismissed themes entirely.** Do not report them, do not fix them, do not count them toward the completion promise.

### Step 1.5: Expand Scope via Pattern Ripple

Changed files may affect other files using the same patterns. Expand verification scope:

**Index-Accelerated Ripple** — If `.shipkit/codebase-index.json` exists, use `concepts` mapping to immediately identify related files by concept area (e.g., if a changed file is in `concepts.auth`, all auth files are in the ripple scope). This narrows the Explore agent's search significantly.

**USE SUBAGENT FOR PATTERN RIPPLE** - Launch Explore subagent for efficient parallel scanning:

```
Task tool with subagent_type: "Explore"
Prompt: "Detect pattern ripple from these changed files: [list files]
[If index exists, include: 'The codebase index maps these concept areas: [list concepts with their files]. Use this to immediately identify same-concept files. Focus your scanning on cross-concept ripple effects the index doesn't capture.']

For each file, identify which patterns it uses:
- Auth: getSession, requireAuth, isAuthorized
- API Response: NextResponse, Response.json
- Error Handling: try/catch, .catch(
- Validation: zod, schema.parse
- Data Fetching: fetch, useSWR, useQuery

Then expand: find ALL other files using the same patterns.
Return: pattern type → list of affected files (both changed and ripple)."
```

**Why subagent**: Pattern ripple requires multiple parallel greps across the codebase. Explore agent handles this efficiently and returns a focused summary.

**Fallback** (if subagent unavailable) - Manual pattern detection:

| Pattern Type | Detection (in changed files) | Expansion (find all instances) |
|--------------|------------------------------|--------------------------------|
| Auth | `getSession\|requireAuth\|isAuthorized` | Grep all files with auth patterns |
| API Response | `NextResponse\|Response.json` | Glob all API routes |
| Error Handling | `try\s*{\|\.catch\(` | Grep async code for consistency |
| Validation | `zod\|schema\.parse` | Grep all form/input handlers |
| Data Fetching | `fetch\(\|useSWR\|useQuery` | Grep all data fetching code |
| External Service | `openai\|anthropic\|gemini\|stripe\|fetch\(` | Grep all files with external calls, check for timeout/limits |

**Expansion logic:**

1. For each changed file, grep for pattern indicators
2. If pattern detected, expand scope:
   - Auth pattern → `Grep: pattern="getSession|requireAuth|isAuthorized" glob="**/*.{ts,tsx}"`
   - API route changed → `Glob: pattern="**/api/**/route.{ts,js}"`
   - Validation pattern → `Grep: pattern="zod|schema\.parse" glob="**/*.{ts,tsx}"`
3. Add ALL matches to verification scope
4. Mark as `RIPPLE:pattern-type` in output

**Scope categories:**

| Category | Description |
|----------|-------------|
| `CHANGED` | Files in git diff (always checked) |
| `RIPPLE:auth` | All files using auth patterns |
| `RIPPLE:api` | All API routes (check consistent response shapes) |
| `RIPPLE:error` | Files with error handling patterns |
| `RIPPLE:validation` | Files with validation schemas |

**Report ripple scope in output:**

```
Reviewed: 3 changed + 7 ripple files
- Changed: src/api/trips/route.ts, src/lib/auth.ts, src/components/Form.tsx
- Ripple (auth): +4 files (detected auth pattern change)
- Ripple (api): +3 files (detected API route change)
```

**When to expand:**
- Auth file changed → Check ALL auth usages for consistency
- API route changed → Check other routes for response shape consistency
- Validation schema changed → Check all forms using that schema
- Error handling pattern changed → Check all async code for consistency

**When NOT to expand:**
- Simple typo fix in a comment
- Style-only changes
- Test file changes (contained scope)

### Step 2: Read Context

Load relevant context for the review:

| File | Purpose |
|------|---------|
| Changed files | The actual code to review |
| `.shipkit/specs/active/*` | Check spec compliance |
| `.shipkit/architecture.json` | Check pattern consistency |
| `.shipkit/codebase-index.json` | Find related code |

### Step 3: Work Through Quality Dimensions

Review changes against these 12 dimensions, emphasizing based on what changed.

**FOR LARGE CHANGE SETS (10+ files), USE PARALLEL SUBAGENTS:**

```
Launch these Task agents IN PARALLEL (single message, multiple tool calls):

1. STRUCTURAL & SPEC AGENT (subagent_type: "Explore")
   Prompt: "Verify structural integrity and spec alignment for these files: [list files]
   STRUCTURAL: Check for orphan code, missing wiring, broken imports, circular deps, incomplete refactors.
   SPEC: If .shipkit/specs/active/* exists, verify implementation matches spec criteria.
   Report findings with file:line evidence and classification (NOT_CREATED, CREATED_UNUSED, WIRING_MISSING, etc.)."

2. ERROR & SECURITY AGENT (subagent_type: "Explore")
   Prompt: "Verify error resilience and security for these files: [list files]
   ERROR: Check for unhandled async, missing try/catch, empty state handling, swallowed errors.
   SECURITY: Check for auth on routes, input validation, SQL injection risk, hardcoded secrets, XSS, IDOR.
   Report findings with file:line evidence and severity (critical/should-fix/minor)."

3. STATE & PERFORMANCE AGENT (subagent_type: "Explore")
   Prompt: "Verify state management, edge cases, and performance for these files: [list files]
   STATE: Check for race conditions, stale state, missing loading states, N+1 queries.
   EDGE CASES: Check for empty states, boundary values, unicode, timezone issues.
   PERFORMANCE: Check for unnecessary re-renders, missing memoization, heavy deps, unoptimized queries.
   Report findings with file:line evidence."

4. UX & MAINTAINABILITY AGENT (subagent_type: "Explore")
   Prompt: "Verify UX completeness and maintainability for these files: [list files]
   UX: Check for loading indicators, action feedback, destructive confirmations, data-testid/ARIA attrs.
   MAINTAINABILITY: Check for magic numbers, duplicated logic, component duplication, missing types, TODOs, console.logs.
   Report findings with file:line evidence."
```

**When to use parallel agents:**
- 10+ files in change set (including ripple files)
- Multiple categories of changes (UI + API + DB)
- Deep verify requested

**When to use single-pass:**
- Small change set (< 10 files)
- Single category focus
- Quick pre-commit check

**IMPORTANT:** When using subagents, include dismissed themes in the prompt: "Skip these dismissed themes: [list from state file]"

### Step 4: Fix Critical Findings

After verification, **fix issues automatically** in priority order:

1. **🔴 Critical findings first** — fix all of them
2. **🟡 Should Fix** — fix straightforward ones (broken imports, missing try/catch, orphan code removal)
3. **🟢 Minor** — **never fix, only note.** Minors are too subjective to auto-fix confidently. List them in the final report for the user to decide.

**Do NOT fix:**
- 🟢 Minor findings (report only)
- Dismissed themes (from state file)
- Anything requiring architectural decisions
- Anything where the "right fix" is ambiguous
- Security issues that need user input (e.g., which auth strategy)

**Track what was fixed:**

Keep a running list for the final report:
```
## Auto-Fixed
- ✅ Added try/catch to src/api/auth/login.ts:34
- ✅ Removed orphan file src/utils/oldAuth.ts
- ✅ Fixed broken import in src/pages/Dashboard.tsx:5
```

### Step 5: Re-Verify and Loop Exit

After fixing, **re-verify the changed files** (including files you just modified):

1. Re-run verification on all files touched in Step 4
2. Check: are there any remaining 🔴 Critical or 🟡 Should Fix findings (excluding dismissed themes)?
   - **YES** → Continue fixing. When you try to stop, the hook will block you and send you back.
   - **NO** → Delete `.shipkit/relentless-verify.{sid8}.local.md` and proceed to final report. Any 🟢 Minor findings are listed in the report but do not block completion.

The relentless hook manages the iteration. You don't need to count loops — just:
- Fix what you find
- Try to stop when you think you're done
- If the hook sends you back, re-verify and fix again

---

## The 12 Quality Dimensions

### 1. Structural Integrity
- Orphan code (defined but never used)
- Missing wiring (component exists but not rendered, route not registered)
- Broken imports (importing deleted/moved file)
- Circular dependencies
- Incomplete refactors (changed in one place, not others)

### 2. Spec & Intent Alignment
- Implementation matches active spec
- All acceptance criteria covered
- Edge cases from spec handled
- Feature actually solves the stated problem
- **Fix didn't break the general case** — if a bug spec exists (`.shipkit/specs/active/bug-*.json`), check that the fix handles the reported case WITHOUT regressing the happy path or other documented edge cases. Read `fix.robustness.findings` for what was considered.

### 3. Error Resilience
- Unhandled promise rejections
- Missing try/catch on async operations
- Empty/null/undefined states not handled
- API failure handling missing
- Missing error boundaries (React)
- Errors swallowed silently

### 4. State & Data
- Race conditions possible
- Stale cache / state issues
- Missing loading states
- Optimistic updates without rollback
- N+1 query patterns

### 5. Security
- Auth checks missing on new routes
- Input validation/sanitization missing
- Raw SQL queries (injection risk)
- Secrets/credentials in code
- XSS vulnerabilities
- IDOR (accessing other users' data)

### 6. Edge Cases
- Empty state not handled (zero items)
- Boundary values (0, negative, very large)
- Unicode/special characters
- Timezone issues
- Concurrent access scenarios
- **Overengineered edge case handling** — fix for one edge case broke or degraded the happy path or other cases (e.g., added loading guard that blocks normal render, validation so strict it rejects valid input, error handling that swallows success paths)

### 7. Performance Landmines
- Unnecessary re-renders
- Missing memoization where needed
- Heavy dependency for light use (moment.js for one format)
- Unoptimized queries
- Missing pagination on lists

### 8. UX Completeness
- Missing loading indicators
- No feedback on user actions
- Broken/incomplete flows
- Missing confirmation on destructive actions
- Inconsistent patterns vs rest of app
- Interactive elements missing `data-testid` or ARIA attributes (blocks AI testing)

### 9. Maintainability
- Magic numbers/strings
- Duplicated logic (same thing multiple ways)
- **Component duplication** (same component in multiple feature directories instead of shared)
- **Not using shared components** (shared version exists but feature has local copy)
- **Similar-purpose components** (Modal vs Dialog, Card vs Tile — should standardize)
- Confusing/misleading naming
- Missing types on public interfaces
- TODOs/FIXMEs left behind
- console.logs left in

### 10. Environment & Config
- New env vars not documented
- Hardcoded URLs/endpoints
- Works locally but will break in prod
- Docker/CI config not updated for new deps
- Missing feature flags for WIP features

### 10.5. External Service Boundaries
- External API calls without timeout config
- LLM/AI calls without token/output limits
- Serverless routes with external calls missing `maxDuration` export
- Streaming endpoints without keepalive signals
- Sequential external call chains without cumulative timeout tracking
- Pay-per-call services without cost visibility (token tracking, usage counters)

### 11. API Contract
- Breaking changes to existing endpoints
- Inconsistent response shapes
- Missing input validation
- Undocumented new endpoints
- Version compatibility issues

### 12. Database Integrity
- Schema changes without migrations
- Missing indexes on query patterns
- Orphan records possible (no cascading delete)
- Data type mismatches
- Missing foreign key constraints

---

## Verification Integrity Protocol

**Critical Rule: Never claim without evidence.**

Every finding MUST be backed by actual tool output. Claims like "file not created" or "component unused" without verification are verification theater.

### The 5-Step Verification Gate

Before reporting ANY finding, execute these steps:

| Step | Action | Example |
|------|--------|---------|
| **1. IDENTIFY** | What tool call proves this claim? | "I need to confirm `UserCard` is unused" |
| **2. RUN** | Execute the tool call | `Grep: pattern="UserCard" glob="**/*.{ts,tsx}"` |
| **3. READ** | Examine full output | "Found 2 matches: definition + one import" |
| **4. CLASSIFY** | Determine exact state from evidence | "CREATED_USED (imported in Dashboard.tsx:14)" |
| **5. REPORT** | State finding WITH evidence | "UserCard is imported in Dashboard.tsx:14" |

### Language Precision Rules

Use precise language that matches verification evidence:

| Claim | Required Evidence | Tool |
|-------|-------------------|------|
| "File not created" | Glob returns empty | `Glob: pattern="**/UserCard.*"` |
| "File exists but unused" | Glob finds file AND Grep for imports returns 0 | Glob + Grep |
| "Component orphaned" | File exists + no imports + no exports used | Glob + Grep |
| "Import broken" | Import statement exists + target file missing | Read + Glob |
| "Missing wiring" | Component exists + not rendered/registered anywhere | Grep for component usage |
| "Circular dependency" | A imports B AND B imports A | Read both files |

**Never say:**
- ❌ "This file is not used" (without grepping for imports)
- ❌ "This component doesn't exist" (without globbing)
- ❌ "The route is missing" (without checking route registration)

**Always say:**
- ✅ "Grep for `UserCard` returned 0 matches → unused"
- ✅ "Glob for `**/auth-callback.*` returned empty → not created"
- ✅ "Found `import UserCard` but Glob for UserCard.tsx returned empty → broken import"

### State Classification

Classify each finding into ONE of these states:

| State | Definition | Evidence Pattern |
|-------|------------|------------------|
| `NOT_CREATED` | File/component doesn't exist | Glob returns empty |
| `CREATED_UNUSED` | File exists but nothing imports/uses it | Glob finds file + Grep returns 0 imports |
| `CREATED_WRONG` | File exists but implementation doesn't match spec | Read file + compare to spec |
| `WIRING_MISSING` | Component exists but not connected to app | Grep for render/route registration returns 0 |
| `BROKEN_IMPORT` | Import statement points to nonexistent file | Read shows import + Glob for target returns empty |
| `CIRCULAR` | Mutual imports between files | Read both files show cross-imports |
| `STALE` | File exists but outdated vs related files | Compare timestamps or content |

### Evidence Requirements by Dimension

**Structural Integrity (Dimension 1):**
```
Orphan code:
  1. Glob: Find the file (confirm exists)
  2. Grep: Search for imports/uses of exported symbols
  3. If Grep returns 0: CREATED_UNUSED

Missing wiring:
  1. Glob: Confirm component exists
  2. Grep: Search for render/registration (JSX tags, route config)
  3. If Grep returns 0: WIRING_MISSING

Broken imports:
  1. Read: Find import statements
  2. For each import, Glob: Does target exist?
  3. If Glob returns empty: BROKEN_IMPORT
```

**Error Resilience (Dimension 3):**
```
Unhandled async:
  1. Grep: pattern="await " in changed files
  2. Read: Context around each await
  3. Check: Is it wrapped in try/catch?
  4. Report: file:line for unwrapped awaits
```

**Security (Dimension 5):**
```
Hardcoded secrets:
  1. Grep: pattern="(password|secret|key|token)\s*[:=]\s*['\"]"
  2. Exclude: .env files, test fixtures
  3. Report: file:line for matches
```

**Spec Alignment (Dimension 2):**
```
Acceptance criteria check:
  1. Read: Active spec file
  2. Extract: Each acceptance criterion
  3. For each criterion:
     - Grep/Read: Find implementing code
     - Verify: Does implementation satisfy criterion?
  4. Report: Which criteria verified vs not found
```

### Updated Output Format

Each finding MUST include evidence and an L-I-E assessment:

```
### 🔴 Critical (fix before commit)

**Structural: Orphan component** [CREATED_UNUSED] — `L:Medium · I:Low · E:Low`
- Evidence: `Glob("**/UserCard.tsx")` → found at src/components/UserCard.tsx
- Evidence: `Grep("UserCard" in "**/*.{ts,tsx}")` → 1 match (definition only)
- File: `src/components/UserCard.tsx`
- Classification: CREATED_UNUSED (exported but never imported)
- Why: Dead code ships to production, likely incomplete feature

**Structural: Broken import** [BROKEN_IMPORT] — `L:High · I:High · E:Low`
- Evidence: `Read("src/pages/Dashboard.tsx")` line 5: `import { AuthCard } from './AuthCard'`
- Evidence: `Glob("**/AuthCard.*")` → 0 matches
- File: `src/pages/Dashboard.tsx:5`
- Classification: BROKEN_IMPORT (import target doesn't exist)
- Why: Will crash at build or runtime on any page that loads Dashboard
```

### Anti-Patterns (What NOT to Do)

❌ **Assumption without verification:**
```
"The UserCard component appears unused"
→ No Grep was run to verify
```

❌ **Vague classification:**
```
"There might be issues with the auth flow"
→ No specific finding, no evidence, no file:line
```

❌ **Tool mention without execution:**
```
"You should check if UserCard is imported anywhere"
→ YOU should check, not tell user to check
```

❌ **Conflating states:**
```
"UserCard is missing"
→ Missing = not created? Or created but not wired? Different fixes.
```

✅ **Correct pattern:**
```
1. Run Glob to confirm file exists
2. Run Grep to check for usage
3. Classify: NOT_CREATED / CREATED_UNUSED / WIRING_MISSING
4. Report with evidence and file:line
```

**See `references/detection-patterns.md` for Glob/Grep patterns by issue type.**

---

## Contextual Emphasis

Not all dimensions every time. Emphasize based on what changed:

| Changes In | Emphasize |
|------------|-----------|
| Auth/middleware | Security, Error Resilience |
| UI components | UX Completeness, Performance, Edge Cases |
| API routes | API Contract, Security, Error Resilience, External Service Boundaries |
| Database/models | Database Integrity, State & Data |
| Config/env files | Environment & Config |
| External service integration | External Service Boundaries, Error Resilience |
| LLM/AI features | External Service Boundaries, Performance, Error Resilience |
| Refactoring | Structural Integrity, Maintainability |
| New feature | Spec Alignment, all dimensions lightly |

---

## Output Format

Final report after all fix-and-recheck passes:

```
## Verification Report

Reviewed: 5 files (src/api/auth/*, src/middleware/*)
Context: Auth feature implementation
Passes: 3 (2 critical fixed, 1 clean re-verify)

### ✅ Auto-Fixed (this session)

- ✅ Added try/catch to `src/api/auth/login.ts:34` (was: unhandled rejection)
- ✅ Removed orphan file `src/utils/oldAuth.ts` (was: exported but never imported)
- ✅ Fixed broken import in `src/pages/Dashboard.tsx:5`

### 🟡 Remaining — Should Fix

| Finding | L · I · E |
|---------|-----------|
| **UX: Missing loading state** | L:Medium · I:Medium · E:Low |

- `src/components/LoginForm.tsx` — no loading indicator during submit

### 🟢 Remaining — Minor / Consider

| Finding | L · I · E |
|---------|-----------|
| **Maintainability: Magic string** | L:Low · I:Low · E:Low |

- `src/api/auth/login.ts:12` — hardcoded "7d" for token expiry
- Consider: `const TOKEN_EXPIRY = "7d"`

### ⏭️ Dismissed (by user)

- Magic numbers in config (user: "intentional")
- Missing loading states on admin pages (user: "low priority")

---

3 auto-fixed | 0 critical remaining | 1 should fix | 1 minor | 2 dismissed
```

---

## Priority Definitions

| Priority | Meaning | Action |
|----------|---------|--------|
| 🔴 Critical | Will cause bugs, security issues, or crashes | Fix before commit |
| 🟡 Should Fix | Quality issues, tech debt, incomplete work | Fix soon |
| 🟢 Minor | Suggestions, nice-to-haves, style | Consider |

### L-I-E Assessment (Likelihood · Impact · Effort)

Every finding MUST include a compact **L-I-E** rating to help the user prioritize.

| Dimension | High | Medium | Low |
|-----------|------|--------|-----|
| **Likelihood** | Will hit in normal usage | May hit under certain conditions | Edge case, unlikely path |
| **Impact** | Crash, data loss, security breach, broken core flow | Degraded experience, incorrect non-critical behavior | Cosmetic, minor inconvenience, tech debt |
| **Effort** | 30+ min, multi-file or architectural change | 5–30 min, new function or section refactor | < 5 min, one-liner or config tweak |

**Notation:** Use inline format — `L:High · I:High · E:Low`

**Priority should follow from L-I-E:**
- 🔴 Critical = High likelihood OR high impact (regardless of effort)
- 🟡 Should Fix = Medium likelihood + medium impact, or high effort prevents auto-fix
- 🟢 Minor = Low likelihood AND low impact

---

## What This Skill Does NOT Do

- **Make architectural decisions** — fixes obvious issues, defers ambiguous ones to user
- **Override dismissals** — dismissed themes stay dismissed for the entire session
- **Block commits** — informational, not a gate
- **Persist results** — ephemeral output only (state file is cleaned up)
- **Run linters/tests** — this is Claude reasoning, not tooling
- **Guarantee completeness** — best effort review

---

## Team Mode

When running as part of an Agent Team:
- Check `.shipkit/team-state.local.json` — if present, you're in team mode
- **Read the spec** from the team state's `specPath` for acceptance criteria
- **Message the lead** with the verification verdict (PASS/FAIL + details)
- **Message implementers directly** when issues found in their files
- **Broadcast summary** to the whole team when verification completes
- The lead typically runs this after all implementation tasks complete

---

## Context Files This Skill Reads

| File | Purpose |
|------|---------|
| Git diff | What changed |
| `.shipkit/specs/active/*` | Check spec compliance |
| `.shipkit/architecture.json` | Check pattern consistency |
| `.shipkit/codebase-index.json` | Find related code |
| Source files | The actual code |

---

## Context Files This Skill Writes

None. This is a read-only reporting tool.

---

## Deeper Review Options

This skill provides a **fast single-pass review** — good for daily use.

For **visual UI verification**, use the dedicated visual QA skill:
- `/shipkit-qa-visual` — maintains UI goals (pages × personas), generates Playwright tests, runs headlessly

For **thorough multi-agent review**, two plugins are available:

| Plugin | Agents | Best For |
|--------|--------|----------|
| `code-review` | 4 parallel | Standard deep review |
| `pr-review-toolkit` | 6 parallel | Maximum scrutiny |

```bash
# Install (once)
/plugin install code-review@claude-code-plugins
/plugin install pr-review-toolkit@claude-code-plugins

# Use
/code-review                      # 4-agent review
/pr-review-toolkit:review-pr      # 6-agent deep analysis
```

**When to use deeper review:**
- Before merging to main
- Complex changes touching multiple systems
- Security-sensitive code
- When fast verify flags concerns worth investigating further

**Trade-off:** 4-6x token cost, slower, but catches more subtle issues.

---

<!-- SECTION:after-completion -->
## After Completion

Relentless loop is complete. State file has been deleted. Final report shows:
- What was auto-fixed (with before/after context)
- What remains unfixed (should-fix and minor)
- What was dismissed by user

User decides next steps:
- Address remaining should-fix items
- Ignore minor suggestions
- Proceed with commit

**Want deeper scrutiny?** Use `/code-review` (4 agents) or `/pr-review-toolkit:review-pr` (6 agents) — requires plugins.

No follow-up skill automatically triggered.
<!-- /SECTION:after-completion -->

---

<!-- SECTION:success-criteria -->
## Success Criteria

- [ ] Scope detected from git diff or session context
- [ ] Pre-scan presented to user with dismissal option
- [ ] Dismissed themes recorded in state file
- [ ] Relentless state file created with correct format
- [ ] Relevant quality dimensions emphasized (excluding dismissed)
- [ ] Specs/architecture read for compliance
- [ ] Critical findings auto-fixed with evidence
- [ ] Re-verification passes confirm fixes are clean
- [ ] State file deleted on completion
- [ ] Final report shows: auto-fixed, remaining, dismissed
<!-- /SECTION:success-criteria -->