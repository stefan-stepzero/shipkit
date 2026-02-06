---
name: shipkit-preflight
description: Aggregates project context and audits production readiness against a comprehensive SaaS checklist. Routes to prerequisite skills when context is missing.
argument-hint: "[area to audit]"
model: opus
context: fork
agent: shipkit-reviewer-agent
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# shipkit-preflight - MVP Production Readiness Audit

**Purpose**: Ensure your project is ready for first users — the essentials that can't wait.

**What it does**: Runs an MVP-focused production checklist covering security, data integrity, error handling, UX basics, and legal compliance. Generates `.shipkit/preflight.json` with structured results. For scale/enterprise readiness (observability, performance, operational maturity), use `/shipkit-scale-ready` after you have traction.

**Output format**: JSON — readable by Claude, renderable by mission control dashboard, and the single source of truth for production readiness status.

**Philosophy**: With AI dev, building is cheap — but security, data integrity, and user trust aren't. This checklist keeps what matters for MVP while deferring optimization concerns.

---

## When to Invoke

**User triggers**:
- "Am I ready to ship?"
- "Production readiness check"
- "Preflight", "Go live check"
- "Is this ready for users?"
- "Launch checklist"

**For thorough mode** (deep code review per partition):
- "Thorough preflight", "Deep preflight"
- "Really scrutinize before launch"
- → See [Thorough Mode](#thorough-mode-deep-code-review) section

**Workflow position**:
- After features are implemented
- Before deploying to production
- When transitioning from "it works" to "it's shippable"

---

## Prerequisites

This skill aggregates context from other skills. It will route you to create missing context.

| Needed Context | Source Skill | File | Required? |
|----------------|--------------|------|-----------|
| Tech stack, deployment target | `/shipkit-project-context` | `stack.json` | Yes |
| Vision, constraints, scale | `/shipkit-why-project` | `why.md` | Yes |
| Architecture decisions, auth model | `/shipkit-architecture-memory` | `architecture.json` | Recommended |
| Data shapes, what's stored | `/shipkit-data-contracts` | `contracts.json` | Recommended |
| Feature specs | `/shipkit-spec` | `specs/active/*.md` | Helpful |

**If missing required context**: Skill will route you to the appropriate skill first.

---

## Process

### Step 0: Determine Audit Scope (Full vs Incremental)

**Check for previous audit:**

```
1. Check if .shipkit/preflight.json exists

2. If exists, extract metadata:
   - Last run timestamp
   - Commit hash at last run
   - Previous findings (passed/failed/warned)

3. Get changes since last audit:
   git diff <last-commit>..HEAD --name-only

4. Determine scope:
   - No previous audit → FULL AUDIT
   - No changes since last audit → QUICK VERIFY (re-check failures only)
   - Changes detected → INCREMENTAL AUDIT (focus on changed areas)
```

**Map changed files to checklist categories:**

| Files Changed | Re-check Categories |
|---------------|---------------------|
| `**/auth/**`, `**/middleware/**`, `**/login/**` | Auth & Security |
| `**/api/**`, `**/routes/**` | API, Error Handling |
| `**/*.sql`, `**/migrations/**`, `**/prisma/**` | Database |
| `**/components/**`, `**/pages/**`, `**/app/**` | UX Resilience |
| `.env*`, `**/config/**` | Environment |
| `Dockerfile`, `vercel.json`, `railway.*` | Deployment |
| `**/payment/**`, `**/billing/**`, `**/webhook/**` | Payments |
| `**/shared/**`, `**/common/**`, `**/features/**/components/**` | Code Structure & Reuse |

**Communicate scope to user:**
```
Since last preflight (a1b2c3d, 3 days ago):
- 12 files changed
- Categories affected: Auth, Database, Error Handling
- Running incremental audit...
```

---

### Step 1: Check Prerequisites (if Full Audit)

**Skip to Step 3 if incremental audit with all prerequisites already met.**

**Read existing context files:**

```
1. Check .shipkit/stack.json
   - Missing? → "Run /shipkit-project-context first — I need to know your stack and deployment target"
   - Exists but no deployment target? → Ask: "Where are you deploying? (Vercel, AWS, Railway, Docker, etc.)"

2. Check .shipkit/why.md
   - Missing? → "Run /shipkit-why-project first — I need to understand scale and constraints"
   - Exists → Extract: expected users, data sensitivity, uptime requirements

3. Check .shipkit/architecture.json
   - Missing? → Note: "No architecture decisions documented — will use generic checks"
   - Exists → Extract: auth model, database choices, key patterns

4. Check .shipkit/contracts.json
   - Missing? → Note: "No data contracts — will infer from code"
   - Exists → Extract: what sensitive data is stored
```

**If required files missing**: Stop and route to prerequisite skill.

---

### Step 2: Gap Analysis (Minimal Intake)

**Only ask what's NOT captured in existing files:**

Possible questions (only if not already documented):

1. **Deployment target** (if not in stack.json):
   - "Where are you deploying? (Vercel, Railway, AWS, Docker, self-hosted)"

2. **Expected scale** (if not in why.md):
   - "Expected concurrent users at launch? (just me, <100, 100-1000, 1000+)"

3. **Data sensitivity** (if not in contracts.json):
   - "What's the most sensitive data you store? (none, emails, PII, payments, healthcare)"

4. **Current state**:
   - "Is this a fresh launch or adding features to a live product?"

**Store answers in audit context** (not persisted separately — these inform THIS audit).

---

### Step 3: Run Audit Against Checklist

**Load checklist sections based on context AND scope:**

| If Context Shows | Load Checklist Sections |
|------------------|------------------------|
| Auth in stack | `auth-checks.md` |
| Payments (Stripe, Lemon Squeezy) | `payment-checks.md` |
| Database (Supabase, Postgres) | `database-checks.md` |
| Deployment target known | `deployment-checks.md` (target-specific) |
| PII or sensitive data | `data-privacy-checks.md` |
| All projects | `universal-checks.md` |

**See**: `references/checklists/` for full checklist content.

**USE PARALLEL SUBAGENTS BY CATEGORY** - For full audits, spawn multiple Explore agents in parallel:

```
Launch these Task agents IN PARALLEL (single message, multiple tool calls):

1. AUTH & SECURITY AGENT (subagent_type: "Explore")
   Prompt: "Audit authentication and security patterns in this [stack] codebase.
   Check: auth on protected routes, session expiry, CSRF protection, rate limiting,
   secrets in env vars, input validation, brute force prevention, form abuse prevention.
   Report Pass/Fail/Warning with file:line evidence for each check."

2. DATA & ERROR HANDLING AGENT (subagent_type: "Explore")
   Prompt: "Audit data integrity and error handling in this [stack] codebase.
   Check: RLS policies (Supabase), cascade deletes, backup docs, try/catch on async,
   error boundaries, consistent API errors, retry logic, graceful degradation, error logging.
   Report Pass/Fail/Warning with file:line evidence for each check."

3. UX & DEPLOYMENT AGENT (subagent_type: "Explore")
   Prompt: "Audit UX resilience and deployment readiness in this [stack] codebase.
   Check: loading states, empty states, confirmation dialogs, form validation,
   mobile responsive, build passes, health endpoint, migrations, SSL, domain config.
   Report Pass/Fail/Warning with file:line evidence for each check."

4. CODE QUALITY & COMPLIANCE AGENT (subagent_type: "Explore")
   Prompt: "Audit code structure, accessibility, and compliance in this [stack] codebase.
   Check: no duplicate components, shared components used, consistent naming,
   utils consolidated, types centralized, data-testid attributes, ARIA roles,
   Terms of Service link, Privacy Policy link, cookie consent.
   Report Pass/Fail/Warning with file:line evidence for each check."

5. PAYMENTS AGENT (if applicable) (subagent_type: "Explore")
   Prompt: "Audit payment integration in this [stack] codebase.
   Check: webhook signature verification, idempotency, failed payment handling,
   subscription state sync, test mode disabled in prod.
   Report Pass/Fail/Warning with file:line evidence for each check."
```

**Why parallel subagents**:
- Each category runs simultaneously → faster total execution
- Smaller scope per agent → more thorough checks within category
- Better context management → agent stays focused on related patterns
- Clearer attribution → know which category each finding came from

**When to use parallel subagents**:
- Full audit with 3+ checklist categories
- Large codebase (50+ source files)
- Need thorough coverage

**When to scan manually (single thread)**:
- Quick verify (re-check failures only)
- Incremental audit (few files changed)
- Single category focus

**For FULL AUDIT:**
- Run all applicable checks (via subagent for efficiency)
- Scan entire codebase for evidence
- Mark as: ✅ Pass | ⚠️ Warning | ❌ Fail | ⏭️ N/A

**For INCREMENTAL AUDIT:**
```
1. Re-check categories affected by changed files
   - Full scan of changed files
   - Mark as: ✅ Pass | ⚠️ Warning | ❌ Fail

2. Re-verify previous failures
   - Check if previously failed items now pass
   - Mark as: ✅ NOW FIXED | ❌ Still failing

3. Skip unchanged categories
   - Note as: ⏭️ Unchanged since last audit
   - Carry forward previous status

4. Quick spot-check unchanged passing items (optional)
   - Verify critical items haven't regressed
   - Only if explicitly requested
```

**For QUICK VERIFY (no changes):**
- Only re-check previously failed/warned items
- Report if issues still exist or now fixed

---

### Step 3.5: Verification Protocol for Each Check

**Critical: Execute tools before marking Pass/Fail.**

Each checklist item describes what to "Scan for" — translate these to actual tool calls:

| Checklist Description | Tool Call | Pass Condition |
|----------------------|-----------|----------------|
| "Auth on protected routes" | `Grep: pattern="getSession\|requireAuth" path="src/app/api/**"` | All route files have auth |
| "Secrets in env vars" | `Grep: pattern="(secret\|key)[:=]['\"]" glob="**/*.{ts,tsx}"` | 0 matches in source |
| "Try/catch on async" | `Grep: pattern="await " -A=5` then check for try | All awaits wrapped |
| "Error boundaries" | `Grep: pattern="ErrorBoundary\|error\\.tsx" path="src/app"` | Found in layout/root |
| "Loading states" | `Grep: pattern="loading\|isLoading\|Skeleton" path="[component]"` | Found in async components |
| "Input validation" | `Grep: pattern="zod\|yup\|schema\\.parse" path="[form file]"` | Found in form handlers |

**Verification sequence for each check:**
1. **Execute** the appropriate Glob/Grep/Read
2. **Read** the output completely
3. **Classify** as Pass/Fail based on evidence
4. **Record** evidence in finding (file:line or "0 matches")

**Never mark a check without tool evidence.** If a checklist says "Scan for X" and you didn't actually scan, the check is incomplete.

---

### Step 4: Generate Audit Report

**Create**: `.shipkit/preflight.json`

**The output MUST conform to the schema below.** This is a strict contract — mission control and other skills depend on this structure.

---

## JSON Schema

```json
{
  "$schema": "shipkit-artifact",
  "type": "preflight",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DD",
  "source": "shipkit-preflight",

  "summary": {
    "overallStatus": "ready | ready-with-warnings | not-ready",
    "readinessScore": 85,
    "scope": "full | incremental | quick-verify",
    "commit": "a1b2c3d",
    "filesChecked": 47,
    "previousAuditCommit": "x9y8z7w",
    "counts": {
      "pass": 22,
      "fail": 3,
      "warning": 5,
      "notApplicable": 4,
      "unchanged": 0
    },
    "byCategory": {
      "auth-security": { "pass": 5, "fail": 1, "warning": 1, "notApplicable": 0, "changed": true },
      "data-database": { "pass": 3, "fail": 0, "warning": 1, "notApplicable": 0, "changed": false },
      "error-handling": { "pass": 4, "fail": 1, "warning": 0, "notApplicable": 0, "changed": true },
      "environment": { "pass": 3, "fail": 0, "warning": 1, "notApplicable": 1, "changed": false },
      "deployment": { "pass": 3, "fail": 1, "warning": 0, "notApplicable": 1, "changed": false },
      "ux-resilience": { "pass": 3, "fail": 0, "warning": 1, "notApplicable": 1, "changed": true },
      "code-structure": { "pass": 3, "fail": 0, "warning": 1, "notApplicable": 0, "changed": false },
      "legal-compliance": { "pass": 2, "fail": 0, "warning": 0, "notApplicable": 1, "changed": false },
      "payments": { "pass": 0, "fail": 0, "warning": 0, "notApplicable": 0, "changed": false },
      "ai-accessibility": { "pass": 1, "fail": 0, "warning": 0, "notApplicable": 0, "changed": false }
    }
  },

  "checks": [
    {
      "id": "auth-protected-routes",
      "category": "auth-security",
      "name": "Authentication on protected routes",
      "status": "pass | fail | warning | not-applicable | unchanged",
      "evidence": "src/middleware/auth.ts:15 — requireAuth applied to all /api/protected/* routes",
      "file": "src/middleware/auth.ts",
      "line": 15,
      "statusChange": null,
      "details": "All 12 protected routes have auth middleware"
    },
    {
      "id": "secrets-in-env",
      "category": "auth-security",
      "name": "Secrets in environment variables",
      "status": "fail",
      "evidence": "src/config/api.ts:8 — hardcoded API key found",
      "file": "src/config/api.ts",
      "line": 8,
      "statusChange": "new",
      "details": "API key hardcoded in source instead of environment variable"
    }
  ],

  "blockers": [
    {
      "checkId": "secrets-in-env",
      "category": "auth-security",
      "name": "Hardcoded API key in source",
      "file": "src/config/api.ts",
      "line": 8,
      "problem": "API key is hardcoded in source code",
      "impact": "Key exposed in git history, anyone with repo access can use it",
      "fix": "Move to environment variable, add to .env.example, rotate the key",
      "statusChange": "new | still-failing | regression"
    }
  ],

  "recommendations": [
    {
      "checkId": "rate-limiting",
      "category": "auth-security",
      "name": "Rate limiting on auth endpoints",
      "severity": "warning",
      "suggestion": "Add rate limiting middleware to /api/auth/* routes to prevent brute force attacks",
      "effort": "low | medium | high"
    }
  ],

  "statusChanges": {
    "fixed": [
      { "checkId": "error-boundaries", "description": "Error boundaries now present in root layout" }
    ],
    "newIssues": [
      { "checkId": "secrets-in-env", "description": "Hardcoded API key introduced in recent commit" }
    ],
    "regressions": []
  },

  "auditHistory": [
    {
      "date": "2024-01-15",
      "commit": "a1b2c3d",
      "scope": "full",
      "blockers": 3,
      "warnings": 7
    },
    {
      "date": "2024-01-12",
      "commit": "x9y8z7w",
      "scope": "incremental",
      "blockers": 5,
      "warnings": 9
    }
  ],

  "context": {
    "project": "From why.md",
    "stack": "From stack.json",
    "deployment": "Target platform"
  }
}
```

### Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `$schema` | string | yes | Always `"shipkit-artifact"` — identifies this as a Shipkit-managed file |
| `type` | string | yes | Always `"preflight"` — artifact type for routing/rendering |
| `version` | string | yes | Schema version for forward compatibility |
| `lastUpdated` | string | yes | ISO date of last modification |
| `source` | string | yes | Always `"shipkit-preflight"` |
| `summary` | object | yes | Aggregated counts for dashboard rendering |
| `summary.overallStatus` | enum | yes | `"ready"` \| `"ready-with-warnings"` \| `"not-ready"` |
| `summary.readinessScore` | number | yes | 0-100 percentage (pass / (pass + fail + warning) * 100) |
| `summary.scope` | enum | yes | `"full"` \| `"incremental"` \| `"quick-verify"` |
| `summary.commit` | string | yes | Git commit hash at time of audit |
| `summary.filesChecked` | number | yes | Number of source files scanned |
| `summary.previousAuditCommit` | string | no | Commit hash of last audit (for incremental) |
| `summary.counts` | object | yes | Total pass/fail/warning/notApplicable/unchanged |
| `summary.byCategory` | object | yes | Per-category breakdown with `changed` flag for incremental |
| `checks` | array | yes | All individual checks with status and evidence |
| `checks[].id` | string | yes | Slug identifier (kebab-case) |
| `checks[].category` | string | yes | Category slug matching `summary.byCategory` keys |
| `checks[].name` | string | yes | Human-readable check name |
| `checks[].status` | enum | yes | `"pass"` \| `"fail"` \| `"warning"` \| `"not-applicable"` \| `"unchanged"` |
| `checks[].evidence` | string | yes | Tool output evidence (file:line or "0 matches") |
| `checks[].file` | string | no | File path where evidence was found |
| `checks[].line` | number | no | Line number in file |
| `checks[].statusChange` | enum | no | `"new"` \| `"fixed"` \| `"regression"` \| `null` |
| `checks[].details` | string | no | Additional context |
| `blockers` | array | yes | Critical issues extracted from checks where status is `"fail"` |
| `blockers[].checkId` | string | yes | References `checks[].id` |
| `blockers[].category` | string | yes | Category slug |
| `blockers[].name` | string | yes | Issue title |
| `blockers[].file` | string | no | File path |
| `blockers[].line` | number | no | Line number |
| `blockers[].problem` | string | yes | What is wrong |
| `blockers[].impact` | string | yes | What happens if not fixed |
| `blockers[].fix` | string | yes | How to fix it |
| `blockers[].statusChange` | enum | no | `"new"` \| `"still-failing"` \| `"regression"` |
| `recommendations` | array | yes | Non-critical issues extracted from checks where status is `"warning"` |
| `recommendations[].checkId` | string | yes | References `checks[].id` |
| `recommendations[].category` | string | yes | Category slug |
| `recommendations[].name` | string | yes | Issue title |
| `recommendations[].severity` | string | yes | Always `"warning"` |
| `recommendations[].suggestion` | string | yes | What to do about it |
| `recommendations[].effort` | enum | no | `"low"` \| `"medium"` \| `"high"` |
| `statusChanges` | object | yes | Delta from previous audit |
| `statusChanges.fixed` | array | yes | Checks that were failing but now pass |
| `statusChanges.newIssues` | array | yes | Checks that are new failures |
| `statusChanges.regressions` | array | yes | Checks that were passing but now fail |
| `auditHistory` | array | yes | Previous audit summaries (append on each full audit) |
| `context` | object | yes | Project context used for this audit |

### Summary Object

The `summary` field MUST be kept in sync with the `checks` array. It exists so the dashboard can render overview cards without iterating the full array. Recompute it every time the file is written.

### Determining Overall Status

- `"not-ready"` — Any blockers exist (checks with status `"fail"`)
- `"ready-with-warnings"` — No blockers, but recommendations exist (checks with status `"warning"`)
- `"ready"` — All checks pass or are not-applicable

---

### Step 5: Save and Present

**Archive previous** (if exists and doing full audit):
```bash
# Move existing to archive with date
.shipkit/preflight.json → .shipkit/audits/preflight-2024-01-15.json
```

**Write new**: `.shipkit/preflight.json` (conforming to JSON schema above)

**Output to user (Full Audit):**
```
✅ Preflight audit complete (full)

📊 Results: X passed | X warnings | X blockers

🔴 Blockers (must fix before launch):
  1. [Brief description]
  2. [Brief description]

🟡 Top warnings:
  1. [Brief description]
  2. [Brief description]

📁 Full report: .shipkit/preflight.json

Ready to review blockers? I can help fix them.

💡 For deep code review: "thorough preflight" (requires pr-review-toolkit plugin)
```

**Output to user (Incremental Audit):**
```
✅ Preflight audit complete (incremental)

📊 Since last audit (a1b2c3d, 3 days ago):
   12 files changed → 3 categories re-checked

🔄 Status changes:
   ✅ 2 issues now fixed
   ❌ 1 new issue found
   ⚠️ 0 regressions

🔴 Current blockers: 2 (was 3)
🟡 Current warnings: 5 (was 7)

📁 Full report: .shipkit/preflight.json

Ready to review the new issue? I can help fix it.
```

**Output to user (Quick Verify - no changes):**
```
✅ Quick verify complete

📊 No changes since last audit (a1b2c3d, 2 hours ago)

🔴 Previous blockers re-checked:
   ❌ 2 still failing
   ✅ 1 now fixed

📁 Full report: .shipkit/preflight.json

Ready to fix the remaining blockers?
```

---

## The Checklist Categories

### 1. Auth & Security
- Authentication on all protected routes
- Session management (expiry, refresh)
- Password requirements (if applicable)
- OAuth state parameter (if applicable)
- CSRF protection
- Rate limiting on auth endpoints
- Secrets in environment variables (not code)
- Input sanitization
- **Brute force prevention** — lockout or delay after N failed login attempts (pattern: counter in DB, exponential backoff)
- **Form abuse prevention** — honeypot field + timing check on public forms (pattern: hidden field bots fill, reject < 2s submissions)

### 2. Data & Database
- RLS policies on all user tables (Supabase)
- Cascade deletes configured correctly
- Backup strategy documented

*Moved to scale-ready: soft deletes, indexes, data export, PII encryption*

### 3. Error Handling
- Try/catch on all async operations
- API error responses are consistent
- Error boundaries in UI (React)
- Failed request retry logic
- Graceful degradation for non-critical features
- User-friendly error messages (not stack traces)
- **Error visibility** — errors logged with context for debugging (pattern: structured error logging with user/request context; optional: error tracking service like Sentry free tier)

### 4. Environment & Config
- All env vars documented in .env.example
- No hardcoded URLs/endpoints
- Environment parity (dev ≈ prod)
- Feature flags for WIP features
- Secrets not in git history

### 5. Deployment
- Build passes without warnings
- Health check endpoint exists
- Migrations run automatically or documented
- SSL/HTTPS enforced
- Domain configured correctly

*Moved to scale-ready: rollback plan documented*

### 6. UX Resilience
- Loading states on all async operations
- Empty states handled
- Confirmation on destructive actions
- Form validation with clear errors
- Mobile responsive

*Moved to scale-ready: offline handling*

### 7. Payments (if applicable)
- Webhook signature verification
- Idempotency on payment operations
- Failed payment handling
- Subscription state synced with provider
- Test mode disabled in prod

*Moved to scale-ready: receipts/invoices*

### 8. Legal/Compliance
- Terms of Service link
- Privacy Policy link
- Cookie consent (if required)

*Moved to scale-ready: data retention policy, GDPR data export/deletion*

### 9. Code Structure & Reuse
- **No duplicate components** (same component name in multiple feature directories)
- **Shared components used** (features import from shared/common/ui, not local copies)
- **Consistent naming** (no Modal vs Dialog vs Popup for same purpose)
- **Utils consolidated** (no duplicate hooks/helpers across features)
- **Types centralized** (shared types in one location, not scattered)

**Why critical**: Duplication creates maintenance burden, inconsistent UX, and makes global updates (like design system changes) painful. Ships technical debt.

### 10. AI Agent Accessibility
- Interactive elements have `data-testid` attributes
- Custom widgets have ARIA roles (`combobox`, `dialog`, `menu`, `tablist`)
- State exposed via attributes (`aria-expanded`, `aria-checked`, `data-state`)
- Form inputs have associated labels (explicit or `aria-label`)
- Dynamic content changes announced to screen readers

**Why critical**: Without these, AI-driven QA (Claude in Chrome, Playwright) cannot reliably interact with or verify UI. This blocks automated testing and accessibility compliance.

---

## Context Files This Skill Reads

**For incremental audit**:
- `.shipkit/preflight.json` — Previous audit with metadata (commit hash, findings)
- Git history — `git diff <last-commit>..HEAD --name-only`

**Required (full audit)**:
- `.shipkit/stack.json` — Tech stack, deployment target
- `.shipkit/why.md` — Vision, constraints, scale expectations

**Recommended**:
- `.shipkit/architecture.json` — Auth model, key decisions
- `.shipkit/contracts.json` — Data shapes, sensitive fields
- `.shipkit/specs/active/*.md` — Feature requirements

**Scans**:
- Source code files based on stack (or just changed files for incremental)
- `package.json` / `requirements.txt` — Dependencies
- `.env.example` — Environment documentation
- Config files based on deployment target

---

## Context Files This Skill Writes

**Write Strategy**: OVERWRITE with ARCHIVE (full audit) or UPDATE-IN-PLACE (incremental)

**Creates/Updates**:
- `.shipkit/preflight.json` — Current audit report (JSON artifact with `$schema`, `type`, `version`, `lastUpdated`, `source`, `summary` fields)

**Archives** (full audit only):
- `.shipkit/audits/preflight-[YYYY-MM-DD].json` — Previous audits

**Why track metadata**:
- Enable incremental audits (know what changed since last run)
- Track progress over time ("last audit had 12 blockers, now 3")
- Identify regressions (was passing, now fails)
- See what was flagged before

---

## Shipkit Artifact Convention

This skill follows the **Shipkit JSON artifact convention** — a standard structure for all `.shipkit/*.json` files that enables mission control visualization.

**Every JSON artifact MUST include these top-level fields:**

```json
{
  "$schema": "shipkit-artifact",
  "type": "<artifact-type>",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DD",
  "source": "<skill-name>",
  "summary": { ... }
}
```

- `$schema` — Always `"shipkit-artifact"`. Lets the reporter hook identify files to ship to mission control.
- `type` — The artifact type (`"preflight"`, `"goals"`, `"spec"`, etc.). Dashboard uses this for rendering.
- `version` — Schema version. Bump when fields change.
- `lastUpdated` — When this file was last written.
- `source` — Which skill wrote this file.
- `summary` — Aggregated data for dashboard cards. Structure varies by type.

Skills that haven't migrated to JSON yet continue writing markdown. The reporter hook ships both: JSON artifacts get structured dashboard rendering, markdown files fall back to metadata-only (exists, date, size).

---

## When This Skill Integrates with Others

### Routes TO (when prerequisites missing)

| Missing | Routes To |
|---------|-----------|
| stack.json | `/shipkit-project-context` |
| why.md | `/shipkit-why-project` |
| architecture.json | `/shipkit-architecture-memory` (suggests, doesn't require) |
| contracts.json | `/shipkit-data-contracts` (suggests, doesn't require) |

### After This Skill

- User fixes blockers (natural capability — no skill needed)
- Re-run `/shipkit-preflight` to verify fixes
- Proceed with deployment

### Differs From

- `/shipkit-verify` — Code quality on recent changes (pre-commit)
- `/shipkit-preflight` — MVP production readiness (pre-launch)
- `/shipkit-scale-ready` — Growth & enterprise readiness (post-traction)

### Progression

```
/shipkit-preflight  →  Launch MVP  →  Get traction  →  /shipkit-scale-ready
     (MVP)                                              (Growth/Enterprise)
```

---

<!-- SECTION:after-completion -->
## After Completion

**Audit delivered. User decides next steps:**

1. **Fix blockers** — Ask Claude to help fix specific issues
2. **Review warnings** — Decide which to address now vs later
3. **Re-run audit** — Verify fixes resolved the issues
4. **Proceed with launch** — If no blockers remain

**Natural capabilities** (no skill needed): Implementing fixes for identified issues.

**Suggest re-running** when significant fixes have been made.
<!-- /SECTION:after-completion -->

---

<!-- SECTION:success-criteria -->
## Success Criteria

- [ ] Audit scope determined (full/incremental/quick-verify)
- [ ] Prerequisites checked on full audit, routed to skills if missing
- [ ] Changed files mapped to affected categories (incremental)
- [ ] Gap questions asked only for undocumented context
- [ ] Checklist filtered to relevant sections based on stack + scope
- [ ] Each finding has specific file/line reference
- [ ] Findings prioritized (blocker/warning/pass)
- [ ] Status changes tracked (fixed/new/regression)
- [ ] JSON artifact fields populated (`$schema`, `type`, `version`, `lastUpdated`, `source`, `summary`)
- [ ] Previous audit archived if full audit
- [ ] Output conforms to JSON schema above
- [ ] Summary field is accurate (counts match checks array)
- [ ] Report saved to `.shipkit/preflight.json`
- [ ] Clear delta summary for incremental audits
<!-- /SECTION:success-criteria -->

---

## Thorough Mode (Deep Code Review)

The standard preflight is a **checklist-based audit** — fast, broad coverage.

For **maximum scrutiny**, use the `pr-review-toolkit` plugin to deep-review the entire codebase:

### Process

1. **Partition codebase into MECE chunks** using codebase-index concepts:
   ```
   Read .shipkit/codebase-index.json

   Example partitions:
   - auth (src/auth/**, src/middleware/auth*)
   - api (src/api/**)
   - database (src/db/**, src/models/**)
   - ui (src/components/**, src/pages/**)
   - config (src/config/**, *.config.*)
   ```

2. **Run pr-review-toolkit on each partition** with project context:
   ```
   For each partition:
   - Provide: partition files + codebase-index summary + architecture.json
   - Run: /pr-review-toolkit:review-pr
   - Collect: findings
   ```

3. **Aggregate findings** into preflight report by category

### When to Use

- Pre-launch of critical product
- After major refactor
- Security audit
- When standard preflight flags multiple concerns

### Trade-off

| Mode | Coverage | Depth | Cost |
|------|----------|-------|------|
| Standard | Entire project | Checklist scan | ~1 call |
| Thorough | Entire project | Deep per-partition | ~6 calls × N partitions |

### Installation

```bash
/plugin install pr-review-toolkit@claude-code-plugins
```

Then ask: "Run thorough preflight with deep code review"

---

## References

See `references/checklists/` for detailed checklist items:
- `universal-checks.md` — Applies to all projects
- `auth-checks.md` — Authentication & authorization
- `payment-checks.md` — Stripe, Lemon Squeezy, etc.
- `database-checks.md` — Supabase, Postgres, etc.
- `deployment-checks.md` — Vercel, AWS, Railway, Docker
- `data-privacy-checks.md` — GDPR, PII handling