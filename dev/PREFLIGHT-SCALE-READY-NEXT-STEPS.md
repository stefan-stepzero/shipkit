# Preflight / Scale-Ready Split — Status & Next Steps

**Created**: 2024-02-06
**Purpose**: Track progress on splitting production readiness checks between MVP (preflight) and Growth/Enterprise (scale-ready)

---

## What We Did

### 1. Created `shipkit-scale-ready` skill ✅

New skill for Growth + Enterprise tier checks:

| File | Status |
|------|--------|
| `install/skills/shipkit-scale-ready/SKILL.md` | ✅ Created |
| `install/skills/shipkit-scale-ready/references/checklists/growth-checks.md` | ✅ Created |
| `install/skills/shipkit-scale-ready/references/checklists/enterprise-checks.md` | ✅ Created |
| `install/skills/shipkit-scale-ready/references/README.md` | ✅ Created |

**Categories covered:**
- Security Hardening (Growth + Enterprise)
- Database Optimization (Growth + Enterprise)
- Observability (Growth + Enterprise)
- Performance (Growth + Enterprise)
- Reliability (Growth + Enterprise)
- Operational Readiness (Growth + Enterprise)
- Code Maturity (Growth)
- Compliance (Enterprise)

### 2. Updated integration files ✅

| File | Change |
|------|--------|
| `install/profiles/shipkit.manifest.json` | Added scale-ready to Quality & Communication |
| `CLAUDE.md` | Updated count to 32, added to skill list |
| `README.md` | Updated counts, added skill description |
| `docs/generated/shipkit-overview.html` | Updated counts, added to cheat sheet |

### 3. Added pattern-based checks to preflight ✅

Added (without removing anything):
- **Brute force prevention** — Auth & Security section
- **Form abuse prevention** — Auth & Security section
- **Error visibility** — Error Handling section

All framed as patterns (code-based), not services.

### 4. Created decision document ✅

`dev/PREFLIGHT-SCALE-READY-SPLIT.html` — Visual comparison with:
- Full list of what stays vs moves
- Scoring rationale (L×I framework)
- 6 decision questions that need answers

---

## Decisions Made ✅

User reviewed and decided (conservative approach — keep more in MVP):

| Item | Decision | Reason |
|------|----------|--------|
| Session management | **KEEP** | Mobile phones lock, sessions need to handle this |
| Consistent API errors | **KEEP** | Conservative |
| Failed request retry | **KEEP** | Conservative |
| Graceful degradation | **KEEP** | Bad perception if features break |
| Environment parity | **KEEP** | Vercel handles it, low effort |
| Feature flags | **KEEP** | Debug mode needs this |
| Build without warnings | **KEEP** | Conservative |
| Subscription state synced | **KEEP** | Webhooks must update DB |
| Code Structure (entire) | **KEEP** | Maintenance matters, can blow out |
| AI Accessibility (entire) | **KEEP** | Testing important for AI dev |

## Items REMOVED from Preflight ✅

Applied to `install/skills/shipkit-preflight/SKILL.md`:

**Data & Database:**
- [x] Soft deletes for user data (GDPR)
- [x] Database indexes on query patterns
- [x] Data export capability (GDPR)
- [x] PII encryption at rest

**Deployment:**
- [x] Rollback plan documented

**UX Resilience:**
- [x] Offline handling

**Payments:**
- [x] Receipts/invoices sent

**Legal/Compliance:**
- [x] Data retention policy
- [x] GDPR compliance details (kept Privacy Policy)

## What's Pending

### Update reference checklists ✅

- [x] Update `universal-checks.md` — added MVP header, brute force pattern, form abuse pattern, error visibility pattern
- [x] Update `database-checks.md` — marked indexes, soft deletes, connection pooling as moved
- [x] Update `data-privacy-checks.md` — marked data export, encryption at rest, retention as moved
- [x] Update `deployment-checks.md` — marked rollback as moved
- [x] Update `payment-checks.md` — marked receipts/invoices as moved
- [x] Update `auth-checks.md` — added brute force and form abuse patterns

**All checklists updated with MVP focus and cross-references to scale-ready.**

---

## Files to Reference

| File | Purpose |
|------|---------|
| `dev/PREFLIGHT-SCALE-READY-SPLIT.html` | Visual decision document (open in browser) |
| `install/skills/shipkit-preflight/SKILL.md` | Current preflight skill |
| `install/skills/shipkit-scale-ready/SKILL.md` | New scale-ready skill |
| `install/skills/shipkit-preflight/references/checklists/universal-checks.md` | Preflight checklist details |
| `install/skills/shipkit-scale-ready/references/checklists/growth-checks.md` | Scale-ready checklist details |

---

## Summary

| Aspect | Status |
|--------|--------|
| Scale-ready skill created | ✅ Complete |
| Integration files updated | ✅ Complete |
| Pattern additions to preflight | ✅ Complete |
| Decision document created | ✅ Complete |
| Decision questions answered | ✅ Complete (conservative approach) |
| Items removed from preflight | ✅ Complete (10 items moved) |
| Checklist cleanup | ✅ Complete |

**Items moved to scale-ready:**
- Soft deletes, indexes, data export, PII encryption (database)
- Rollback plan (deployment)
- Offline handling (UX)
- Receipts/invoices (payments)
- Data retention, GDPR details (legal)

**Items KEPT in preflight (user decision):**
- Session management, graceful degradation, environment parity
- Feature flags, build warnings, subscription sync
- Code Structure & Reuse (entire category)
- AI Agent Accessibility (entire category)

**Status**: ✅ COMPLETE

The preflight/scale-ready split is done. Both skills are ready to use:
- `/shipkit-preflight` — MVP production readiness (security, data integrity, UX, legal basics)
- `/shipkit-scale-ready` — Growth & enterprise readiness (observability, performance, operations)
