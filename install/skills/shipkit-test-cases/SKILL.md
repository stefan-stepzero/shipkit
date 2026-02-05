---
name: shipkit-test-cases
description: Generate and maintain code-anchored test case specifications. Use when setting up test coverage, reviewing what to test, or before test-relentlessly.
argument-hint: "[feature or scope]"
---

# shipkit-test-cases - Code-Anchored Test Case Management

**Purpose**: Generate and maintain test case specifications anchored to source files, with automatic staleness detection when code changes. Optimized for AI execution via `test-relentlessly`.

---

## When to Invoke

**User triggers**:
- "Generate test cases"
- "What should we test?"
- "Set up test coverage"
- "Create test spec"
- "Test cases for [feature]"

**Workflow position**:
- After specs exist (helpful but not required)
- Before `test-relentlessly` (provides execution targets)
- Can run standalone against existing codebase

---

## Prerequisites

**Soft requirements** (helpful but not blocking):
- `.shipkit/specs/` — Helps derive cases from requirements
- `.shipkit/product/` — Helps infer priority from user personas

**No hard requirements** — Can analyze code directly without specs

---

## Process

### Step 1: Determine Scope

**If user specifies feature/scope:**
- Focus on that feature's source files
- Read relevant spec if exists

**If no scope specified:**
- Scan `src/` for code structure
- Check git diff for recently changed files
- Prioritize uncovered code

```bash
# Find source files
find src -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx"

# Check recent changes
git diff --name-only HEAD~5..HEAD
```

---

### Step 2: Read Context (Auto-Collect)

**Gather context automatically (no user input):**

| Source | What to Extract |
|--------|-----------------|
| Source files | Functions, endpoints, components |
| `.shipkit/specs/` | Requirements, acceptance criteria |
| `.shipkit/product/` | User personas, critical journeys |
| Existing tests | What's already covered |
| File paths | Priority signals (auth, payment = core) |

**Priority inference heuristics:**

| Signal | Inference |
|--------|-----------|
| Path contains `auth`, `payment`, `checkout`, `billing` | → Core |
| Spec says "must", "critical", "required" | → Core |
| High import count (many dependents) | → Core |
| Error handlers, catch blocks, edge conditions | → Edge |
| Code unchanged 6+ months | → Lower priority |

---

### Step 3: Read Existing Test Cases (Smart Merge)

**CRITICAL: Never regenerate from scratch. Always merge.**

```markdown
1. Read existing `.shipkit/test-cases/cases/*.md` files
2. Parse existing cases with their metadata:
   - ID, scenario, validates (files), verified date
3. Check file modification dates for validated files
4. Classify each existing case:
   - Code unchanged since verified → PRESERVE as-is
   - Code modified since verified → FLAG as ⚠️ stale
   - Validated file deleted → FLAG as ❓ orphaned
5. Identify new code without test cases → GENERATE new cases
```

**Merge rules:**
- PRESERVE cases where code unchanged
- FLAG cases where code modified (⚠️ needs re-verification)
- APPEND new cases for new/uncovered code
- NEVER delete user-accepted cases
- NEVER overwrite existing case priorities

---

### Step 4: Generate/Update Test Cases

**For each feature file, generate test cases:**

**Test case format:**

```markdown
## [ID]: [Scenario Name]

**Validates:** `src/path/to/file.ts`
**Type:** Core | Edge | Regression
**Category:** AI-verifiable | Human-required

**Action:**
[Specific, unambiguous action to perform]

**Verify:**
- [Checkable outcome 1]
- [Checkable outcome 2]

**Code modified:** [YYYY-MM-DD]
**Last verified:** [YYYY-MM-DD or "pending"]
**Status:** ✅ verified | 🆕 pending | ⚠️ stale | ❓ orphaned
```

**AI-optimized test cases:**
- Actions must be specific and executable
- Outcomes must be verifiable (not "feels responsive")
- Include exact values, status codes, field names

**Good:**
```markdown
**Action:** POST /api/auth/login with {email: "test@example.com", password: "valid"}
**Verify:** Status 200, response.token exists, response.user.email matches input
```

**Bad:**
```markdown
**Action:** Try to log in
**Verify:** Login works correctly
```

---

### Step 4.5: Enrich with Codebase Selectors (Optional)

**Purpose:** Transform abstract test actions into AI-executable steps by extracting actual selectors, routes, and element identifiers from the codebase.

**When to enrich:**
- UI/frontend test cases (components, pages)
- E2E test cases requiring element interaction
- When codebase uses data-testid, aria-label, or similar patterns

**Skip enrichment for:**
- Pure API tests (already specific with endpoints/payloads)
- Unit tests (code-level, not UI)
- Test cases marked `Human-required`

#### Enrichment Process

**Option A: Inline enrichment (few cases)**
1. Read the validated source file(s)
2. Extract element identifiers (see strategy below)
3. Map abstract actions to concrete selectors
4. Update test case with Steps table

**Option B: Agent delegation (many cases)**
```
Use Task tool with subagent_type=Explore:
"Enrich test case [ID] by scanning [validated files] for:
- data-testid attributes
- aria-label attributes
- role attributes
- form field names
- route definitions
Return a Steps table mapping actions to selectors."
```

#### Element Identification Strategy

**Priority order for selectors (best → worst):**

| Priority | Selector Type | Example | Why |
|----------|--------------|---------|-----|
| 1 | data-testid | `[data-testid="login-submit"]` | Explicit, stable, test-specific |
| 2 | aria-label | `[aria-label="Submit login"]` | Accessible, semantic |
| 3 | role + name | `button[role="button"]:has-text("Sign In")` | Semantic, visible |
| 4 | placeholder | `input[placeholder="Email"]` | Visible, but can change |
| 5 | CSS class | `.btn-primary` | Fragile, avoid |

**What to extract from source files:**

| File Type | Extract |
|-----------|---------|
| React/Vue components | data-testid, aria-*, role, form names |
| Route configs | Path patterns, route names |
| API handlers | Endpoint URLs, methods, params |
| Form schemas | Field names, validation rules |

#### Enriched Test Case Format

**Before enrichment (abstract):**
```markdown
**Action:** User logs in with valid credentials
**Verify:** User sees dashboard with welcome message
```

**After enrichment (AI-executable):**
```markdown
**Preconditions:**
- Route: `/login`
- Auth: logged out
- Test data: user "test@example.com" exists with password "Test123!"

**Steps:**
| # | Action | Target | Input | Wait |
|---|--------|--------|-------|------|
| 1 | navigate | `/login` | — | page load |
| 2 | fill | `[data-testid="email-input"]` | "test@example.com" | — |
| 3 | fill | `[data-testid="password-input"]` | "Test123!" | — |
| 4 | click | `[data-testid="login-submit"]` | — | network idle |
| 5 | waitFor | URL | matches `/dashboard` | 5s timeout |

**Verify:**
| # | Assertion | Target | Expected |
|---|-----------|--------|----------|
| 1 | URL | — | `/dashboard` |
| 2 | visible | `[data-testid="user-greeting"]` | — |
| 3 | textContent | `[data-testid="user-greeting"]` | contains "Welcome" |
```

#### Standard Action Vocabulary

| Action | Description | Example |
|--------|-------------|---------|
| `navigate` | Go to URL/route | `navigate` → `/login` |
| `fill` | Type into input | `fill` → `[data-testid="email"]` ← "test@example.com" |
| `click` | Click element | `click` → `[data-testid="submit"]` |
| `select` | Choose from dropdown | `select` → `[data-testid="country"]` ← "US" |
| `check` | Check checkbox | `check` → `[data-testid="terms"]` |
| `hover` | Hover over element | `hover` → `[data-testid="menu"]` |
| `waitFor` | Wait for condition | `waitFor` → URL matches `/dashboard` |
| `press` | Keyboard key | `press` → "Enter" |

#### Standard Assertion Vocabulary

| Assertion | Description | Example |
|-----------|-------------|---------|
| `visible` | Element is visible | `visible` → `[data-testid="success"]` |
| `hidden` | Element not visible | `hidden` → `[data-testid="error"]` |
| `textContent` | Text matches | `textContent` → `[data-testid="msg"]` = "Success" |
| `value` | Input value | `value` → `[data-testid="email"]` = "test@example.com" |
| `URL` | Current URL | `URL` matches `/dashboard` |
| `count` | Element count | `count` → `[data-testid="item"]` = 3 |
| `attribute` | Attribute value | `attribute` → `[data-testid="btn"]`.disabled = true |

#### Handling Missing Selectors

When enrichment finds no testid/aria-label:

```markdown
**Steps:**
| # | Action | Target | Input | ⚠️ |
|---|--------|--------|-------|-----|
| 3 | click | `button:has-text("Submit")` | — | Missing data-testid |

**Selector Gaps:**
- `src/components/LoginForm.tsx:42` — Submit button lacks data-testid
- Recommend: `<button data-testid="login-submit">Submit</button>`
```

This flags technical debt while still providing a workable (if fragile) selector.

---

### Step 5: Write Files

**File structure:**

```
.shipkit/
  test-cases/
    STRATEGY.md           # Auto-generated: priorities, approach
    cases/
      auth.md             # Per-feature test cases
      checkout.md
      ...
    COVERAGE.md           # Auto-generated: gaps report
```

**STRATEGY.md** (auto-generated, user can instruct Claude to edit):

```markdown
# Test Strategy

**Generated:** [YYYY-MM-DD]
**Source:** Inferred from codebase structure and specs

## Priority Areas (auto-inferred)
1. Auth flows — business critical (path: src/api/auth/)
2. [Other areas based on heuristics]

## Test Categories
- **Core:** Must pass for release (auth, payment, critical user journeys)
- **Edge:** Important but not blocking (error states, boundaries)
- **Regression:** Prevent known bugs returning

## Coverage Targets
- Core: 100% of cases verified
- Edge: Best effort
- Human-required: Flagged for user review
```

**cases/[feature].md** (append-only):

```markdown
# [Feature] Test Cases

**Generated:** [YYYY-MM-DD]
**Source:** `src/[path]/`

## Core

| ID | Scenario | Validates | Status |
|----|----------|-----------|--------|
| AUTH-01 | Valid login returns token | `login.ts` | 🆕 pending |
| AUTH-02 | Invalid password rejected | `login.ts` | 🆕 pending |

## Edge

| ID | Scenario | Validates | Status |
|----|----------|-----------|--------|
| AUTH-E01 | Malformed email format | `login.ts` | 🆕 pending |

## Regression

| ID | Scenario | Validates | Bug Ref | Status |
|----|----------|-----------|---------|--------|
| AUTH-R01 | Rate limiting after 5 attempts | `login.ts` | #142 | 🆕 pending |
```

**COVERAGE.md** (regenerated each run):

```markdown
# Test Coverage Report

**Generated:** [YYYY-MM-DD]

## Summary
- **Files with test cases:** X/Y (Z%)
- **Core cases:** N (M verified, P pending)
- **Stale cases:** Q (code changed since verification)

## Gaps (files without test cases)
- `src/api/billing/refund.ts` ⚠️ no coverage
- `src/services/notifications.ts` ⚠️ no coverage

## Stale Cases (need re-verification)
| Case | File Changed | Last Verified |
|------|--------------|---------------|
| AUTH-01 | 2024-01-20 | 2024-01-15 |

## Orphaned Cases (code deleted)
| Case | Original File |
|------|---------------|
| BILLING-03 | `src/api/billing/old.ts` (deleted) |
```

---

### Step 6: Output Summary

```
✅ Test cases updated

📁 Location: .shipkit/test-cases/

📊 Summary:
  • Core cases: 12 (8 verified, 4 pending)
  • Edge cases: 18 (10 verified, 8 pending)
  • Regression: 3

🔧 Enrichment:
  • UI cases enriched: 8/10
  • Selectors extracted: 24
  • Missing data-testid: 3 (flagged)

⚠️ Attention needed:
  • 2 stale cases (code changed)
  • 3 files without coverage
  • 3 elements need data-testid attributes

👉 Next: Run `/test-relentlessly` to execute pending cases
```

---

## File Ownership Model

| File | Created | Updated | Owner |
|------|---------|---------|-------|
| `STRATEGY.md` | Auto | User edits via Claude | User (steers via conversation) |
| `cases/*.md` | Auto | Append only (merge) | Shared (Claude generates, user can adjust) |
| `COVERAGE.md` | Auto | Regenerated each run | Skill (computed report) |

**User intervention model:** User does nothing unless they want to change something. If user disagrees, they tell Claude:
- "Make AUTH-03 core priority"
- "Add a test case for session timeout"
- "Remove the rate limiting tests"
- "Flag checkout as regression"

---

## Staleness Detection

**Code-anchored tracking:**

Each test case tracks which files it validates. Staleness = code modified after last verification.

| Condition | Status | Action |
|-----------|--------|--------|
| Code file unchanged | ✅ verified | Preserve as-is |
| Code file modified > last verified | ⚠️ stale | Flag for re-verification |
| Code file deleted | ❓ orphaned | Flag for review/removal |
| New code file, no cases | (gap) | Generate new cases |

**Granularity:** File level (simpler, maintainable)

---

## Integration with test-relentlessly

When `test-relentlessly` runs, it can:

1. Check git diff → which files changed?
2. Look up test cases anchored to those files
3. Prioritize running those cases first
4. Update "last verified" timestamps on pass

This makes test execution **change-aware**.

---

## What Makes This "Lite"

**Included**:
- Auto-generation from code/specs (zero input)
- AI-optimized test case format
- Code-anchored staleness detection
- Smart merge (preserve user decisions)
- Coverage gap reporting

**Not included** (vs full test management):
- Test execution (that's `test-relentlessly`)
- CI/CD integration
- Historical trends/analytics
- Multi-environment tracking
- Test flakiness detection

**Philosophy**: Generate what to test, track coverage, detect staleness. Execution is separate.

---

## When This Skill Integrates with Others

### Before This Skill

- `/shipkit-spec` — Creates specs that inform test case generation
  - **When:** Feature requirements defined
  - **Why:** Specs provide acceptance criteria to derive test cases

- `/shipkit-project-context` — Creates stack.md for tech understanding
  - **When:** Project initialization
  - **Why:** Helps understand what testing patterns apply

### After This Skill

- `/shipkit-test-relentlessly` — Executes test cases
  - **When:** Test cases defined, ready to verify
  - **Why:** Test cases define WHAT to test, test-relentlessly executes
  - **Integration:** Reads cases/*.md, runs tests, updates verified dates

- `/shipkit-verify` — Can use test cases for verification
  - **When:** Checking work before commit
  - **Why:** Test cases inform what to verify

### Related Skills

- `shipkit-verify` — Quality verification (uses test cases as input)
- `shipkit-spec` — Feature specs (source for test case derivation)
- `shipkit-test-relentlessly` — Test execution (consumes test cases)

---

## Context Files This Skill Reads

**Auto-collected (no user input):**
- `src/**/*.{ts,tsx,js,jsx}` — Source files to analyze
- `.shipkit/specs/` — Feature requirements
- `.shipkit/product/` — User personas, priorities
- `.shipkit/test-cases/` — Existing test cases (for merge)
- `tests/` or `__tests__/` — Existing automated tests
- Git history — Recent changes, file modification dates

---

## Context Files This Skill Writes

**Write Strategy: APPEND with SMART MERGE**

**Creates/Updates:**
- `.shipkit/test-cases/STRATEGY.md` — Test approach (auto-generated)
- `.shipkit/test-cases/cases/*.md` — Per-feature test cases (append-only)
- `.shipkit/test-cases/COVERAGE.md` — Coverage report (regenerated)

**Merge Behavior:**
- Reads existing files first
- Preserves user decisions (priorities, verified dates)
- Appends new cases for new code
- Flags stale cases (code changed)
- Never deletes user-accepted cases

---

## Lazy Loading Behavior

**This skill loads context ON DEMAND:**

1. User invokes `/shipkit-test-cases` or routes via master
2. Claude reads this SKILL.md
3. Claude scans source files (file list, not full content)
4. Claude reads specs if exist (~500 tokens)
5. Claude reads existing test cases (~500 tokens)
6. Claude generates/updates cases
7. Total context: ~1500-2500 tokens

**Not loaded unless needed:**
- Full source file contents (only reads when generating specific cases)
- Unrelated specs
- Architecture decisions (not relevant to test cases)

---

<!-- SECTION:after-completion -->
## After Completion

**Test cases are ready.** User can:
- Review generated cases and adjust priorities via conversation
- Run `/shipkit-test-relentlessly` to execute pending cases
- Commit test case specs to version control

**No automatic follow-up.** User decides when to run tests.
<!-- /SECTION:after-completion -->

---

<!-- SECTION:success-criteria -->
## Success Criteria

Test case generation is complete when:
- [ ] Source files analyzed for test targets
- [ ] Existing test cases merged (not overwritten)
- [ ] New cases generated with AI-executable format
- [ ] Cases anchored to source files
- [ ] STRATEGY.md reflects priorities
- [ ] COVERAGE.md shows gaps
- [ ] Stale cases flagged
- [ ] cases/*.md written

**If enrichment performed:**
- [ ] UI test cases have Steps tables with selectors
- [ ] Selectors extracted from actual source files
- [ ] Missing data-testid/aria-labels flagged
- [ ] Preconditions specified (route, auth state, test data)
<!-- /SECTION:success-criteria -->

---

## Example Output

**Generated `cases/auth.md`:**

```markdown
# Auth Test Cases

**Generated:** 2024-01-21
**Source:** `src/api/auth/`

## Core (auto-inferred: auth = business critical)

| ID | Scenario | Validates | Status |
|----|----------|-----------|--------|
| AUTH-01 | Valid login returns token | `login.ts` | 🆕 pending |
| AUTH-02 | Invalid password returns error | `login.ts` | 🆕 pending |
| AUTH-03 | Expired token refresh | `refresh.ts` | 🆕 pending |
| AUTH-04 | Logout invalidates session | `logout.ts` | 🆕 pending |

### AUTH-01: Valid Login Returns Token (API)

**Validates:** `src/api/auth/login.ts`
**Type:** Core | AI-verifiable

**Action:**
POST /api/auth/login with body:
```json
{"email": "test@example.com", "password": "validpassword123"}
```

**Verify:**
- Response status: 200
- Response body contains `token` field (non-empty string)
- Response body contains `user.email` matching input
- Response body contains `user.id` (non-empty)

**Code modified:** 2024-01-15
**Last verified:** pending
**Status:** 🆕 pending

---

### AUTH-02: Valid Login UI Flow (Enriched)

**Validates:** `src/components/auth/LoginForm.tsx`
**Type:** Core | AI-verifiable

**Preconditions:**
- Route: `/login`
- Auth: logged out
- Test data: user "test@example.com" exists with password "Test123!"

**Steps:**
| # | Action | Target | Input | Wait |
|---|--------|--------|-------|------|
| 1 | navigate | `/login` | — | page load |
| 2 | fill | `[data-testid="login-email"]` | "test@example.com" | — |
| 3 | fill | `[data-testid="login-password"]` | "Test123!" | — |
| 4 | click | `[data-testid="login-submit"]` | — | network idle |
| 5 | waitFor | URL | matches `/dashboard` | 5s |

**Verify:**
| # | Assertion | Target | Expected |
|---|-----------|--------|----------|
| 1 | URL | — | `/dashboard` |
| 2 | visible | `[data-testid="user-avatar"]` | — |
| 3 | textContent | `[data-testid="welcome-message"]` | contains "Welcome" |
| 4 | hidden | `[data-testid="login-error"]` | — |

**Selectors extracted from:** `src/components/auth/LoginForm.tsx:12-45`
**Code modified:** 2024-01-15
**Last verified:** pending
**Status:** 🆕 pending

---

### AUTH-03: Invalid Password Shows Error (Enriched)

**Validates:** `src/components/auth/LoginForm.tsx`
**Type:** Core | AI-verifiable

**Preconditions:**
- Route: `/login`
- Auth: logged out

**Steps:**
| # | Action | Target | Input | Wait |
|---|--------|--------|-------|------|
| 1 | navigate | `/login` | — | page load |
| 2 | fill | `[data-testid="login-email"]` | "test@example.com" | — |
| 3 | fill | `[data-testid="login-password"]` | "wrongpassword" | — |
| 4 | click | `[data-testid="login-submit"]` | — | network idle |

**Verify:**
| # | Assertion | Target | Expected |
|---|-----------|--------|----------|
| 1 | URL | — | `/login` (no redirect) |
| 2 | visible | `[data-testid="login-error"]` | — |
| 3 | textContent | `[data-testid="login-error"]` | contains "Invalid" |
| 4 | value | `[data-testid="login-password"]` | "" (cleared) |

**Code modified:** 2024-01-15
**Last verified:** pending
**Status:** 🆕 pending

---

## Edge

| ID | Scenario | Validates | Status |
|----|----------|-----------|--------|
| AUTH-E01 | Malformed email rejected | `login.ts` | 🆕 pending |
| AUTH-E02 | Empty password rejected | `login.ts` | 🆕 pending |
| AUTH-E03 | Rate limit after 5 attempts | `login.ts` | 🆕 pending |
```

---

**Remember**: Test cases define WHAT to verify. Keep them specific, AI-executable, and anchored to code. Execution happens via `test-relentlessly`.
