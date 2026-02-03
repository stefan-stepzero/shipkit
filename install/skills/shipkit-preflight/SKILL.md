---
name: shipkit-preflight
description: Aggregates project context and audits production readiness against a comprehensive SaaS checklist. Routes to prerequisite skills when context is missing.
invoke: user
---

# shipkit-preflight - Production Readiness Audit

**Purpose**: Ensure your project is actually ready for real users — not just working on localhost.

**What it does**: Aggregates context from existing skills, identifies gaps, runs a comprehensive SaaS production checklist, and generates a prioritized audit report.

---

## When to Invoke

**User triggers**:
- "Am I ready to ship?"
- "Production readiness check"
- "Preflight", "Go live check"
- "Is this ready for users?"
- "Launch checklist"

**Workflow position**:
- After features are implemented
- Before deploying to production
- When transitioning from "it works" to "it's shippable"

---

## Prerequisites

This skill aggregates context from other skills. It will route you to create missing context.

| Needed Context | Source Skill | File | Required? |
|----------------|--------------|------|-----------|
| Tech stack, deployment target | `/shipkit-project-context` | `stack.md` | Yes |
| Vision, constraints, scale | `/shipkit-why-project` | `why.md` | Yes |
| Architecture decisions, auth model | `/shipkit-architecture-memory` | `architecture.md` | Recommended |
| Data shapes, what's stored | `/shipkit-data-contracts` | `types.md` | Recommended |
| Feature specs | `/shipkit-spec` | `specs/active/*.md` | Helpful |

**If missing required context**: Skill will route you to the appropriate skill first.

---

## Process

### Step 0: Determine Audit Scope (Full vs Incremental)

**Check for previous audit:**

```
1. Check if .shipkit/production-readiness.md exists

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
1. Check .shipkit/stack.md
   - Missing? → "Run /shipkit-project-context first — I need to know your stack and deployment target"
   - Exists but no deployment target? → Ask: "Where are you deploying? (Vercel, AWS, Railway, Docker, etc.)"

2. Check .shipkit/why.md
   - Missing? → "Run /shipkit-why-project first — I need to understand scale and constraints"
   - Exists → Extract: expected users, data sensitivity, uptime requirements

3. Check .shipkit/architecture.md
   - Missing? → Note: "No architecture decisions documented — will use generic checks"
   - Exists → Extract: auth model, database choices, key patterns

4. Check .shipkit/types.md
   - Missing? → Note: "No data contracts — will infer from code"
   - Exists → Extract: what sensitive data is stored
```

**If required files missing**: Stop and route to prerequisite skill.

---

### Step 2: Gap Analysis (Minimal Intake)

**Only ask what's NOT captured in existing files:**

Possible questions (only if not already documented):

1. **Deployment target** (if not in stack.md):
   - "Where are you deploying? (Vercel, Railway, AWS, Docker, self-hosted)"

2. **Expected scale** (if not in why.md):
   - "Expected concurrent users at launch? (just me, <100, 100-1000, 1000+)"

3. **Data sensitivity** (if not in types.md):
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

**For FULL AUDIT:**
- Run all applicable checks
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

### Step 4: Generate Audit Report

**Create**: `.shipkit/production-readiness.md`

**Report structure (with tracking metadata):**

```markdown
# Production Readiness Audit

<!-- PREFLIGHT METADATA - DO NOT EDIT -->
<!-- last_run: 2024-01-15T14:32:00Z -->
<!-- commit: a1b2c3d4e5f6 -->
<!-- scope: full|incremental|quick-verify -->
<!-- files_checked: 47 -->
<!-- END METADATA -->

**Generated**: [date]
**Commit**: [short hash] ([X commits since last audit])
**Scope**: [Full Audit | Incremental (12 files changed) | Quick Verify]
**Project**: [from why.md]
**Stack**: [from stack.md]
**Deployment**: [target]

---

## Summary

| Category | Pass | Warn | Fail | N/A | Changed |
|----------|------|------|------|-----|---------|
| Auth & Security | X | X | X | X | ✓ |
| Data & Database | X | X | X | X | |
| Error Handling | X | X | X | X | ✓ |
| Environment | X | X | X | X | |
| Deployment | X | X | X | X | |
| UX Resilience | X | X | X | X | ✓ |
| Legal/Compliance | X | X | X | X | |

**Overall**: [READY / READY WITH WARNINGS / NOT READY]

---

## 🔴 Blockers (Must Fix)

[Critical issues that will cause problems in production]

### [Category]: [Issue Title]
- **File**: `path/to/file.ts:line`
- **Problem**: [What's wrong]
- **Impact**: [What happens if not fixed]
- **Fix**: [How to fix]
- **Status**: NEW | Still failing | Regression

---

## 🟡 Warnings (Should Fix)

[Issues that won't break production but create risk]

---

## 🔄 Status Changes (since last audit)

### ✅ Now Fixed
- [Check ID]: [Description] — was failing, now passes

### ❌ New Issues
- [Check ID]: [Description] — introduced since last audit

### ⚠️ Regressions
- [Check ID]: [Description] — was passing, now fails

---

## 🟢 Passed Checks

[Checklist items that passed — collapsed by default]

---

## ⏭️ Unchanged (carried forward)

[Categories not affected by changes since last audit]
- Auth & Security: 12 checks (last verified: [date])
- ...

---

## ⏭️ Not Applicable

[Checks skipped based on your stack/context]

---

## Audit History

| Date | Commit | Scope | Blockers | Warnings |
|------|--------|-------|----------|----------|
| 2024-01-15 | a1b2c3d | Full | 3 | 7 |
| 2024-01-12 | x9y8z7w | Incremental | 5 | 9 |

---

## Next Steps

1. [ ] Fix blockers before deploying
2. [ ] Review warnings and decide which to address
3. [ ] Re-run `/shipkit-preflight` after fixes to verify

---

**Previous audits**: .shipkit/audits/
```

---

### Step 5: Save and Present

**Archive previous** (if exists and doing full audit):
```bash
# Move existing to archive with date
.shipkit/production-readiness.md → .shipkit/audits/production-readiness-2024-01-15.md
```

**Write new**: `.shipkit/production-readiness.md` (with metadata header)

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

📁 Full report: .shipkit/production-readiness.md

Ready to review blockers? I can help fix them.
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

📁 Full report: .shipkit/production-readiness.md

Ready to review the new issue? I can help fix it.
```

**Output to user (Quick Verify - no changes):**
```
✅ Quick verify complete

📊 No changes since last audit (a1b2c3d, 2 hours ago)

🔴 Previous blockers re-checked:
   ❌ 2 still failing
   ✅ 1 now fixed

📁 Full report: .shipkit/production-readiness.md

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

### 2. Data & Database
- RLS policies on all user tables (Supabase)
- Soft deletes for user data (GDPR)
- Cascade deletes configured correctly
- Database indexes on query patterns
- Backup strategy documented
- Data export capability (GDPR)
- PII encryption at rest

### 3. Error Handling
- Try/catch on all async operations
- API error responses are consistent
- Error boundaries in UI (React)
- Failed request retry logic
- Graceful degradation for non-critical features
- User-friendly error messages (not stack traces)

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
- Rollback plan documented
- SSL/HTTPS enforced
- Domain configured correctly

### 6. UX Resilience
- Loading states on all async operations
- Empty states handled
- Offline handling (or clear error)
- Confirmation on destructive actions
- Form validation with clear errors
- Mobile responsive (if applicable)

### 7. Payments (if applicable)
- Webhook signature verification
- Idempotency on payment operations
- Failed payment handling
- Subscription state synced with provider
- Receipts/invoices sent
- Test mode disabled in prod

### 8. Legal/Compliance
- Terms of Service link
- Privacy Policy link
- Cookie consent (if required)
- Data retention policy
- GDPR compliance (if EU users)

---

## Context Files This Skill Reads

**For incremental audit**:
- `.shipkit/production-readiness.md` — Previous audit with metadata (commit hash, findings)
- Git history — `git diff <last-commit>..HEAD --name-only`

**Required (full audit)**:
- `.shipkit/stack.md` — Tech stack, deployment target
- `.shipkit/why.md` — Vision, constraints, scale expectations

**Recommended**:
- `.shipkit/architecture.md` — Auth model, key decisions
- `.shipkit/types.md` — Data shapes, sensitive fields
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
- `.shipkit/production-readiness.md` — Current audit report with metadata header:
  ```
  <!-- PREFLIGHT METADATA -->
  <!-- last_run: ISO timestamp -->
  <!-- commit: git commit hash -->
  <!-- scope: full|incremental|quick-verify -->
  <!-- END METADATA -->
  ```

**Archives** (full audit only):
- `.shipkit/audits/production-readiness-[YYYY-MM-DD].md` — Previous audits

**Why track metadata**:
- Enable incremental audits (know what changed since last run)
- Track progress over time ("last audit had 12 blockers, now 3")
- Identify regressions (was passing, now fails)
- See what was flagged before

---

## When This Skill Integrates with Others

### Routes TO (when prerequisites missing)

| Missing | Routes To |
|---------|-----------|
| stack.md | `/shipkit-project-context` |
| why.md | `/shipkit-why-project` |
| architecture.md | `/shipkit-architecture-memory` (suggests, doesn't require) |
| types.md | `/shipkit-data-contracts` (suggests, doesn't require) |

### After This Skill

- User fixes blockers (natural capability — no skill needed)
- Re-run `/shipkit-preflight` to verify fixes
- Proceed with deployment

### Differs From

- `/shipkit-verify` — Code quality on recent changes (pre-commit)
- `/shipkit-preflight` — Production readiness (pre-launch)

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
- [ ] Metadata header written for future incremental runs
- [ ] Previous audit archived if full audit
- [ ] Report saved to `.shipkit/production-readiness.md`
- [ ] Clear delta summary for incremental audits
<!-- /SECTION:success-criteria -->

---

## References

See `references/checklists/` for detailed checklist items:
- `universal-checks.md` — Applies to all projects
- `auth-checks.md` — Authentication & authorization
- `payment-checks.md` — Stripe, Lemon Squeezy, etc.
- `database-checks.md` — Supabase, Postgres, etc.
- `deployment-checks.md` — Vercel, AWS, Railway, Docker
- `data-privacy-checks.md` — GDPR, PII handling

<!-- Shipkit v1.1.0 -->
