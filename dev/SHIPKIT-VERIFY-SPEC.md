# shipkit-verify Spec

Batch verification on demand — Claude reviews your work across multiple quality dimensions.

---

## Core Concept

User stays in flow, implements multiple things, then asks Claude to verify everything:

```
User: /verify

Claude: [Reviews changes across 12 quality dimensions]
        [Reports findings with priorities]
        [User decides what to act on]
```

**Report only** — doesn't fix, just surfaces issues. User decides next steps.

---

## Triggers

| Trigger | Action |
|---------|--------|
| `/verify` | Review all recent changes |
| `/verify auth` | Focus on specific feature |
| "Check my work" | Same as `/verify` |
| "Ready to commit?" | Verify, then user decides |

---

## Scope Detection

Claude determines what to verify (in order):

1. **Git diff** — uncommitted changes
2. **Session memory** — what Claude worked on this session
3. **User specifies** — "verify the auth feature"

```bash
git diff --name-only HEAD
```

---

## The 12 Quality Dimensions

Claude works through these contextually based on what changed:

### 1. Structural Integrity
- Orphan code (defined but never used)
- Missing wiring (component exists but not rendered)
- Broken imports (importing deleted file)
- Circular dependencies
- Incomplete refactors

### 2. Spec & Intent Alignment
- Implementation matches spec (if spec exists)
- All acceptance criteria covered
- Edge cases from spec handled

### 3. Error Resilience
- Unhandled promise rejections
- Missing try/catch on async
- Empty/null/undefined not handled
- API failure handling missing
- Missing error boundaries

### 4. State & Data
- Race conditions possible
- Stale cache issues
- Missing loading states
- Optimistic updates without rollback
- N+1 query patterns

### 5. Security
- Auth checks on new routes
- Input validation missing
- Raw queries (SQL injection)
- Secrets in code
- XSS vectors

### 6. Edge Cases
- Empty state (zero items)
- Boundary values (0, negative, huge)
- Unicode/special chars
- Timezone issues
- Concurrent access

### 7. Performance Landmines
- Unnecessary re-renders
- Missing memoization
- Heavy deps for light use
- Unoptimized queries
- Missing pagination

### 8. UX Completeness
- Missing loading indicators
- No feedback on actions
- Broken flows
- Missing destructive action confirmation

### 9. Maintainability
- Magic numbers/strings
- Duplicated logic
- Confusing naming
- Missing types on public interfaces
- TODOs left behind

### 10. Environment & Config
- New env vars not documented
- Hardcoded URLs
- Works locally, breaks in prod
- Docker/CI not updated

### 11. API Contract
- Breaking changes to endpoints
- Inconsistent response shapes
- Missing input validation
- Undocumented endpoints

### 12. Database Integrity
- Schema changes without migrations
- Missing indexes
- Orphan records possible
- Cascading deletes missing

---

## Contextual Depth

Not all dimensions every time. Claude emphasizes based on what changed:

| Changes In | Emphasize |
|------------|-----------|
| Auth/middleware | Security, Error Resilience |
| UI components | UX Completeness, Performance |
| API routes | API Contract, Security, Error Resilience |
| Database/models | Database Integrity, State & Data |
| Config/env | Environment & Config |
| Refactoring | Structural Integrity, Maintainability |

---

## Context Claude Reads

| File | Why |
|------|-----|
| Git diff | What changed |
| Active spec | Check compliance |
| `architecture.md` | Check pattern consistency |
| `codebase-index.json` | Find related code |
| Changed files | Analyze the actual code |

---

## Output Format

Ephemeral report with priorities:

```
## Verification Report

Reviewed: 5 files (src/api/auth/*, src/middleware/*)
Context: Auth feature implementation

### 🔴 Critical (fix before commit)

**Security: Missing auth check**
- `src/api/users/[id]/route.ts` — endpoint accessible without auth
- Any user can access any other user's data

**Error Resilience: Unhandled rejection**
- `src/api/auth/login.ts:34` — await without try/catch
- Will crash on invalid credentials

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

**Spec Alignment: Edge case not covered**
- Spec mentions "rate limit after 5 attempts"
- Not implemented (maybe post-MVP?)

---

2 critical | 2 should fix | 2 minor
```

---

## What This Skill Does NOT Do

- **Fix issues** — report only, user decides
- **Block anything** — it's informational
- **Persist results** — ephemeral output
- **Run automated tools** — this is Claude reasoning, not linting

---

## SKILL.md Structure

```markdown
---
name: shipkit-verify
description: Review recent changes across 12 quality dimensions — report issues by priority
invoke: user
model: sonnet
tools:
  - Read
  - Glob
  - Bash
---

# shipkit-verify

Batch verification — Claude reviews your work and reports findings.

---

## When to Invoke

- `/verify` — review all recent changes
- `/verify <feature>` — focus on specific area
- "Check my work", "Ready to commit?"

---

## What It Does

1. Detect what changed (git diff + session memory)
2. Read relevant context (specs, architecture, changed files)
3. Work through quality dimensions contextually
4. Report findings with priorities:
   - 🔴 Critical — fix before commit
   - 🟡 Should fix — quality issues
   - 🟢 Minor — suggestions

---

## Quality Dimensions

1. Structural Integrity
2. Spec & Intent Alignment
3. Error Resilience
4. State & Data
5. Security
6. Edge Cases
7. Performance Landmines
8. UX Completeness
9. Maintainability
10. Environment & Config
11. API Contract
12. Database Integrity

Dimensions emphasized based on what changed.

---

## Output

Ephemeral report. Doesn't fix, doesn't persist.

User sees findings → decides what to address → asks Claude to fix if needed.

---

## Context Files This Skill Reads

- Git status/diff
- `.shipkit/specs/active/*` — check spec compliance
- `.shipkit/architecture.md` — check patterns
- `.shipkit/codebase-index.json` — find related code
- Changed source files — the actual code

---

## Context Files This Skill Writes

None. Report only.
```

---

## Success Criteria

- [ ] Detects scope from git diff + session
- [ ] Contextually emphasizes relevant dimensions
- [ ] Reads specs/architecture for compliance checking
- [ ] Clear priority-based output (🔴🟡🟢)
- [ ] Ephemeral — no file artifacts
- [ ] Report only — doesn't offer fixes
