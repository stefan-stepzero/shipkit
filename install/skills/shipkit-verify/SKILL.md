---
name: shipkit-verify
description: Review recent changes across 12 quality dimensions — report issues by priority. Use after a chunk of work, before commit, or when asked to check work.
invoke: user
model: sonnet
tools:
  - Read
  - Glob
  - Bash
---

# shipkit-verify

Batch verification — Claude reviews your work across quality dimensions and reports findings.

**Report only.** Doesn't fix, doesn't persist. User sees issues, decides what to address.

---

## When to Invoke

- `/verify` — review all recent changes
- `/verify <feature>` — focus on specific area
- "Check my work", "Am I ready to commit?"

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

### Step 2: Read Context

Load relevant context for the review:

| File | Purpose |
|------|---------|
| Changed files | The actual code to review |
| `.shipkit/specs/active/*` | Check spec compliance |
| `.shipkit/architecture.md` | Check pattern consistency |
| `.shipkit/codebase-index.json` | Find related code |

### Step 3: Work Through Quality Dimensions

Review changes against these 12 dimensions, emphasizing based on what changed:

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

### 9. Maintainability
- Magic numbers/strings
- Duplicated logic (same thing multiple ways)
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

## Contextual Emphasis

Not all dimensions every time. Emphasize based on what changed:

| Changes In | Emphasize |
|------------|-----------|
| Auth/middleware | Security, Error Resilience |
| UI components | UX Completeness, Performance, Edge Cases |
| API routes | API Contract, Security, Error Resilience |
| Database/models | Database Integrity, State & Data |
| Config/env files | Environment & Config |
| Refactoring | Structural Integrity, Maintainability |
| New feature | Spec Alignment, all dimensions lightly |

---

## Output Format

Ephemeral report with clear priorities:

```
## Verification Report

Reviewed: 5 files (src/api/auth/*, src/middleware/*)
Context: Auth feature implementation

### 🔴 Critical (fix before commit)

**Security: Missing auth check**
- `src/api/users/[id]/route.ts` — endpoint accessible without auth
- Impact: Any user can access any other user's data

**Error Resilience: Unhandled rejection**
- `src/api/auth/login.ts:34` — await without try/catch
- Impact: Will crash on invalid credentials

### 🟡 Should Fix

**Structural: Orphan code**
- `src/utils/oldAuth.ts` — exported but never imported
- Likely leftover from refactor

**UX: Missing loading state**
- `src/components/LoginForm.tsx` — no loading indicator during submit

### 🟢 Minor / Consider

**Maintainability: Magic string**
- `src/api/auth/login.ts:12` — hardcoded "7d" for token expiry
- Consider: `const TOKEN_EXPIRY = "7d"`

---

2 critical | 2 should fix | 2 minor
```

---

## Priority Definitions

| Priority | Meaning | Action |
|----------|---------|--------|
| 🔴 Critical | Will cause bugs, security issues, or crashes | Fix before commit |
| 🟡 Should Fix | Quality issues, tech debt, incomplete work | Fix soon |
| 🟢 Minor | Suggestions, nice-to-haves, style | Consider |

---

## What This Skill Does NOT Do

- **Fix issues** — report only, user decides what to address
- **Block commits** — informational, not a gate
- **Persist results** — ephemeral output only
- **Run linters/tests** — this is Claude reasoning, not tooling
- **Guarantee completeness** — best effort review

---

## Context Files This Skill Reads

| File | Purpose |
|------|---------|
| Git diff | What changed |
| `.shipkit/specs/active/*` | Check spec compliance |
| `.shipkit/architecture.md` | Check pattern consistency |
| `.shipkit/codebase-index.json` | Find related code |
| Source files | The actual code |

---

## Context Files This Skill Writes

None. This is a read-only reporting tool.

---

<!-- SECTION:after-completion -->
## After Completion

Report is delivered. User decides next steps:
- Fix critical issues (ask Claude to help)
- Defer should-fix items
- Ignore minor suggestions
- Proceed with commit

No follow-up skill automatically triggered.
<!-- /SECTION:after-completion -->

---

<!-- SECTION:success-criteria -->
## Success Criteria

- [ ] Scope detected from git diff or session context
- [ ] Relevant quality dimensions emphasized
- [ ] Specs/architecture read for compliance
- [ ] Clear prioritized output (🔴🟡🟢)
- [ ] Findings are specific and actionable
- [ ] Report only — no unsolicited fixes
<!-- /SECTION:success-criteria -->

<!-- Shipkit v1.1.0 -->
