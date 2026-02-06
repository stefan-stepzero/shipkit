---
name: shipkit-scale-ready
description: Audits production systems for scale readiness — observability, performance, reliability, and operational maturity. For teams with traction preparing to grow.
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

# shipkit-scale-ready - Scale Readiness Audit

**Purpose**: Ensure your production system can handle growth and be operated reliably.

**Who this is for**: Teams with traction — you've launched, you have users, now you need to harden for scale.

**Prerequisite**: Preflight passed. This skill assumes MVP-level production readiness already exists.

---

## When to Invoke

**User triggers**:
- "Ready to scale"
- "Scale readiness check"
- "Production hardening"
- "Post-MVP audit"
- "We have traction, what should we fix?"
- "Enterprise readiness"

**Workflow position**:
- After MVP launch and user traction
- Before scaling marketing/growth efforts
- Before enterprise customers
- When transitioning from "it works" to "it's robust"

---

## The Two Tiers

| Tier | When | Focus |
|------|------|-------|
| 🔶 **Growth** | Have traction, scaling up | Can handle 10x users, can debug prod issues |
| 🏢 **Enterprise** | Big customers, high stakes | Compliance, SLAs, operational maturity |

Default audit covers Growth tier. Enterprise tier on request or if context indicates enterprise customers.

---

## Process

### Step 0: Verify Prerequisites

```
1. Check if preflight passed recently
   - Read .shipkit/production-readiness.md
   - If blockers exist: "Fix preflight blockers first — run /preflight"

2. Load project context
   - .shipkit/stack.md — tech stack
   - .shipkit/why.md — scale expectations
   - .shipkit/architecture.md — key patterns
```

### Step 1: Determine Audit Scope

**Check for previous scale audit:**
```
1. Check if .shipkit/scale-readiness.md exists
2. If exists, get changes since last audit
3. Determine: FULL AUDIT vs INCREMENTAL
```

**Map stack to relevant categories:**

| Stack Includes | Check Categories |
|----------------|------------------|
| Database (any) | Database Optimization |
| External APIs | Reliability Patterns |
| Auth system | Security Hardening |
| Frontend | Performance |
| Any backend | Observability, Operational |

### Step 2: Run Checklist by Category

For each applicable category, run checks and classify as:
- ✅ **Pass** — Implemented correctly
- ⚠️ **Warning** — Partially implemented or could improve
- ❌ **Fail** — Missing or broken
- ⏭️ **N/A** — Not applicable to this stack
- 👤 **Human-Verify** — Claude cannot verify, human must check

**See**: `references/checklists/` for detailed check definitions.

**USE PARALLEL SUBAGENTS BY CATEGORY** - For full audits, spawn multiple Explore agents in parallel:

```
Launch these Task agents IN PARALLEL (single message, multiple tool calls):

1. SECURITY & DATABASE AGENT (subagent_type: "Explore")
   Prompt: "Audit security hardening and database optimization in this [stack] codebase.
   SECURITY: Check security headers (CSP, HSTS), session config, admin route protection,
   re-auth on sensitive actions, API key management.
   DATABASE: Check indexes on queries, N+1 patterns, connection pooling, slow query logging.
   Report Pass/Fail/Warning/Human-Verify with file:line evidence for each check."

2. OBSERVABILITY & PERFORMANCE AGENT (subagent_type: "Explore")
   Prompt: "Audit observability and performance in this [stack] codebase.
   OBSERVABILITY: Check structured logging vs console.log, log levels, request/correlation ID,
   error tracking context, health endpoint detail.
   PERFORMANCE: Check bundle size, code splitting, image optimization, caching headers,
   API response caching.
   Report Pass/Fail/Warning/Human-Verify with file:line evidence for each check."

3. RELIABILITY & OPERATIONS AGENT (subagent_type: "Explore")
   Prompt: "Audit reliability patterns and operational readiness in this [stack] codebase.
   RELIABILITY: Check timeouts on external calls, retry with backoff, graceful degradation,
   idempotency keys, retriable jobs.
   OPERATIONS: Check for runbooks, rollback docs, zero-downtime deploy config, feature flags.
   Report Pass/Fail/Warning/Human-Verify with file:line evidence for each check."

4. CODE MATURITY AGENT (subagent_type: "Explore")
   Prompt: "Audit code maturity and technical debt in this [stack] codebase.
   Check: test coverage on critical paths, duplicate components, shared component usage,
   centralized types, TODO/FIXME in core flows, dependency vulnerabilities (npm audit).
   Report Pass/Fail/Warning with file:line evidence for each check."

5. COMPLIANCE AGENT (Enterprise tier only) (subagent_type: "Explore")
   Prompt: "Audit compliance patterns in this [stack] codebase.
   Check: GDPR export endpoint, GDPR deletion flow, audit logging on sensitive actions,
   data retention cleanup jobs.
   Report Pass/Fail/Warning/Human-Verify with file:line evidence for each check."
```

**Why parallel subagents**:
- Each category runs simultaneously → faster total execution
- Smaller scope per agent → more thorough checks within category
- Clear attribution → findings map directly to categories
- 8 categories × 5-6 checks each = 50+ checks parallelized efficiently

**When to use parallel subagents**:
- Full scale-ready audit
- Large codebase (50+ source files)

**When to scan manually (single thread)**:
- Incremental audit (few files changed)
- Single category focus (e.g., "just check security")

---

## The Categories

### 1. Security Hardening (🔶 Growth)

Beyond MVP auth — protection against targeted attacks.

| Check | What | How Claude Verifies |
|-------|------|---------------------|
| SEC-SCALE-001 | Security headers configured (CSP, HSTS, X-Frame) | Grep for helmet/headers config |
| SEC-SCALE-002 | Session expiry and refresh configured | Grep for session config |
| SEC-SCALE-003 | Admin routes extra-protected | Check admin routes for additional auth |
| SEC-SCALE-004 | Sensitive actions require re-auth | Grep for password confirm on critical ops |
| SEC-SCALE-005 | API keys scoped and rotatable | Check for key management patterns |

**🏢 Enterprise:**
| Check | What | How to Verify |
|-------|------|---------------|
| SEC-ENT-001 | Penetration testing done | 👤 Human-Verify: Report exists |
| SEC-ENT-002 | Security audit completed | 👤 Human-Verify: Report exists |
| SEC-ENT-003 | SOC2 compliance | 👤 Human-Verify: Certification |

---

### 2. Database Optimization (🔶 Growth)

Move from "works" to "works fast at scale."

| Check | What | How Claude Verifies |
|-------|------|---------------------|
| DB-SCALE-001 | Indexes on query patterns | Read migrations for CREATE INDEX |
| DB-SCALE-002 | No N+1 query patterns | Grep for fetch/query inside .map/.forEach |
| DB-SCALE-003 | Connection pooling configured | Grep for pool config |
| DB-SCALE-004 | Slow query logging enabled | Check DB config |
| DB-SCALE-005 | Backup tested (not just configured) | 👤 Human-Verify: Restore tested |

**🏢 Enterprise:**
| Check | What | How to Verify |
|-------|------|---------------|
| DB-ENT-001 | Read replicas for read-heavy loads | Check infra config |
| DB-ENT-002 | PII encrypted at rest | 👤 Human-Verify: Encryption config |
| DB-ENT-003 | Point-in-time recovery enabled | 👤 Human-Verify: DB settings |

---

### 3. Observability (🔶 Growth)

Can you see what's happening in production?

| Check | What | How Claude Verifies |
|-------|------|---------------------|
| OBS-SCALE-001 | Structured logging (not console.log) | Grep for logger import vs console.log |
| OBS-SCALE-002 | Log levels configured (debug off in prod) | Check logger config |
| OBS-SCALE-003 | Request ID / correlation ID | Grep for request-id, correlation |
| OBS-SCALE-004 | Error tracking captures context | Check Sentry/error config for extras |
| OBS-SCALE-005 | Alerting on error spike | 👤 Human-Verify: Alert rules exist |
| OBS-SCALE-006 | Health endpoint returns useful info | Read health endpoint, check for deps status |

**🏢 Enterprise:**
| Check | What | How to Verify |
|-------|------|---------------|
| OBS-ENT-001 | Distributed tracing | Grep for tracing SDK |
| OBS-ENT-002 | Business metrics tracked | 👤 Human-Verify: Dashboard exists |
| OBS-ENT-003 | Log retention policy | 👤 Human-Verify: Config exists |

---

### 4. Performance (🔶 Growth)

Will it handle real traffic?

| Check | What | How Claude Verifies |
|-------|------|---------------------|
| PERF-SCALE-001 | Core Web Vitals passing | 👤 Human-Verify: Lighthouse/PageSpeed |
| PERF-SCALE-002 | Bundle size optimized | Check build output, look for bundle analyzer |
| PERF-SCALE-003 | Code splitting / lazy loading | Grep for dynamic import, React.lazy |
| PERF-SCALE-004 | Images optimized | Grep for next/image, srcset, webp |
| PERF-SCALE-005 | Caching headers on static assets | Check CDN/server config |
| PERF-SCALE-006 | API response caching where appropriate | Grep for cache-control, Redis usage |

**🏢 Enterprise:**
| Check | What | How to Verify |
|-------|------|---------------|
| PERF-ENT-001 | Load testing done | 👤 Human-Verify: Report exists |
| PERF-ENT-002 | Auto-scaling configured | 👤 Human-Verify: Infra config |
| PERF-ENT-003 | CDN for static assets | Check deployment config |
| PERF-ENT-004 | Database query performance baselined | 👤 Human-Verify: Metrics exist |

---

### 5. Reliability (🔶 Growth)

What happens when things fail?

| Check | What | How Claude Verifies |
|-------|------|---------------------|
| REL-SCALE-001 | Timeouts on all external calls | Grep for timeout config on fetch/axios |
| REL-SCALE-002 | Retry with exponential backoff | Grep for retry logic patterns |
| REL-SCALE-003 | Graceful degradation / fallbacks | Check for fallback UI, default values |
| REL-SCALE-004 | Idempotency on critical operations | Check for idempotency keys |
| REL-SCALE-005 | Queue jobs are retriable | Check job processor config |

**🏢 Enterprise:**
| Check | What | How to Verify |
|-------|------|---------------|
| REL-ENT-001 | Circuit breakers on external services | Grep for circuit breaker lib |
| REL-ENT-002 | Bulkhead pattern (isolation) | Check service architecture |
| REL-ENT-003 | Chaos testing done | 👤 Human-Verify: Tests run |

---

### 6. Operational Readiness (🔶 Growth)

Can you actually run and maintain this?

| Check | What | How Claude Verifies |
|-------|------|---------------------|
| OPS-SCALE-001 | Runbooks exist for common issues | Glob for docs/runbooks, RUNBOOK.md |
| OPS-SCALE-002 | Rollback procedure documented | Grep for rollback in docs |
| OPS-SCALE-003 | Zero-downtime deployment | Check CI/CD config for rolling deploy |
| OPS-SCALE-004 | Staging environment exists | 👤 Human-Verify: Environment exists |
| OPS-SCALE-005 | Feature flags for gradual rollout | Grep for feature flag library |

**🏢 Enterprise:**
| Check | What | How to Verify |
|-------|------|---------------|
| OPS-ENT-001 | Incident response process documented | Glob for INCIDENT.md, incident docs |
| OPS-ENT-002 | On-call rotation defined | 👤 Human-Verify: PagerDuty/similar |
| OPS-ENT-003 | Post-mortem process exists | Check for post-mortem template |
| OPS-ENT-004 | SLAs defined and monitored | 👤 Human-Verify: SLA doc exists |

---

### 7. Code Maturity (🔶 Growth)

Technical debt under control?

| Check | What | How Claude Verifies |
|-------|------|---------------------|
| CODE-SCALE-001 | Test coverage on critical paths | Run coverage, check critical files |
| CODE-SCALE-002 | No duplicate components | Glob for duplicate basenames |
| CODE-SCALE-003 | Shared components used | Grep for imports from shared |
| CODE-SCALE-004 | Types centralized | Check for scattered type definitions |
| CODE-SCALE-005 | No TODO/FIXME on core flows | Grep for TODO/FIXME in critical paths |
| CODE-SCALE-006 | Dependencies vulnerability-free | Run npm audit / pip audit |

---

### 8. Compliance (🏢 Enterprise)

For enterprise customers and regulated industries.

| Check | What | How to Verify |
|-------|------|---------------|
| COMP-ENT-001 | GDPR data export works | Test export endpoint |
| COMP-ENT-002 | GDPR deletion works | Test deletion flow |
| COMP-ENT-003 | Audit logging on sensitive actions | Grep for audit log calls |
| COMP-ENT-004 | Data retention policy enforced | Check cleanup jobs |
| COMP-ENT-005 | SOC2 Type II | 👤 Human-Verify: Certification |
| COMP-ENT-006 | HIPAA (if health data) | 👤 Human-Verify: Compliance audit |

---

## Output Format

```markdown
# Scale Readiness Audit

**Generated**: [date]
**Commit**: [hash]
**Tier**: Growth / Enterprise
**Stack**: [from stack.md]

---

## Summary

| Category | Pass | Warn | Fail | Human-Verify |
|----------|------|------|------|--------------|
| Security Hardening | X | X | X | X |
| Database Optimization | X | X | X | X |
| Observability | X | X | X | X |
| Performance | X | X | X | X |
| Reliability | X | X | X | X |
| Operational Readiness | X | X | X | X |
| Code Maturity | X | X | X | X |
| Compliance (Enterprise) | X | X | X | X |

**Overall**: [SCALE-READY / NEEDS WORK / ENTERPRISE-READY]

---

## 🔴 Critical Issues

[Issues that will cause problems at scale]

## 🟡 Improvements Needed

[Should fix before significant growth]

## 👤 Human Verification Required

[Items Claude cannot verify — requires human action]

### To Verify:
- [ ] OBS-SCALE-005: Check alerting rules in [monitoring tool]
- [ ] PERF-ENT-001: Run load test with k6/Artillery
- [ ] DB-SCALE-005: Test backup restore procedure

## ✅ Passed

[What's already good]

---

## Next Steps

1. [ ] Address critical issues
2. [ ] Complete human verification items
3. [ ] Re-run `/scale-ready` to confirm

---

**Preflight status**: [Last run date, blockers count]
```

---

## Context Files This Skill Reads

**Required**:
- `.shipkit/production-readiness.md` — Preflight must have passed
- `.shipkit/stack.md` — Tech stack

**Recommended**:
- `.shipkit/why.md` — Scale expectations
- `.shipkit/architecture.md` — Patterns and decisions
- `.shipkit/scale-readiness.md` — Previous audit (for incremental)

**Scans**:
- Source code for patterns
- Config files (CI/CD, Docker, etc.)
- Documentation (runbooks, etc.)

---

## Context Files This Skill Writes

**Creates/Updates**:
- `.shipkit/scale-readiness.md` — Current audit report with metadata

**Archives** (on full audit):
- `.shipkit/audits/scale-readiness-[YYYY-MM-DD].md`

---

## Relationship to Other Skills

| Skill | Relationship |
|-------|--------------|
| `/preflight` | Prerequisite — MVP readiness must pass first |
| `/verify` | Complements — verify is per-change, scale-ready is system-wide |
| `/architecture-memory` | Reads — understands system patterns |

---

## Success Criteria

- [ ] Preflight status verified (passed)
- [ ] Stack context loaded
- [ ] Tier determined (Growth vs Enterprise)
- [ ] All applicable categories checked
- [ ] Human-verify items clearly listed
- [ ] Evidence provided for each finding
- [ ] Prioritized output (critical → improvements → passed)
- [ ] Report saved to `.shipkit/scale-readiness.md`
