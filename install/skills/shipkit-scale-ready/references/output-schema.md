# Scale Readiness Output Schema

This document defines the JSON schema for `.shipkit/scale-readiness.json` produced by the `shipkit-scale-ready` skill.

---

## Full JSON Schema

```json
{
  "$schema": "shipkit-artifact",
  "type": "scale-readiness",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DD",
  "source": "shipkit-scale-ready",

  "summary": {
    "overallStatus": "needs-work",
    "tier": "growth",
    "commit": "abc1234",
    "stack": "Next.js + Postgres",
    "counts": { "pass": 18, "warning": 8, "fail": 3, "na": 2, "human-verify": 5 },
    "categoryScores": {
      "security": { "pass": 3, "warning": 1, "fail": 1, "na": 0, "human-verify": 0 },
      "database": { "pass": 3, "warning": 1, "fail": 0, "na": 0, "human-verify": 1 },
      "observability": { "pass": 4, "warning": 1, "fail": 0, "na": 0, "human-verify": 1 },
      "performance": { "pass": 3, "warning": 2, "fail": 1, "na": 0, "human-verify": 0 },
      "reliability": { "pass": 2, "warning": 1, "fail": 1, "na": 1, "human-verify": 0 },
      "operations": { "pass": 1, "warning": 2, "fail": 0, "na": 0, "human-verify": 2 },
      "code-maturity": { "pass": 2, "warning": 0, "fail": 0, "na": 1, "human-verify": 1 },
      "compliance": { "pass": 0, "warning": 0, "fail": 0, "na": 0, "human-verify": 0 }
    }
  },

  "categories": [
    {
      "id": "security",
      "name": "Security Hardening",
      "tier": "growth",
      "checks": [
        {
          "id": "SEC-SCALE-001",
          "name": "Security headers configured (CSP, HSTS, X-Frame)",
          "status": "pass",
          "severity": "high",
          "details": "Helmet middleware configured with strict CSP policy",
          "evidence": "src/middleware.ts:14",
          "recommendation": null
        },
        {
          "id": "SEC-SCALE-002",
          "name": "Session expiry and refresh configured",
          "status": "warning",
          "severity": "medium",
          "details": "Session expiry set to 30 days - consider reducing for sensitive apps",
          "evidence": "src/auth/config.ts:8",
          "recommendation": "Reduce session expiry to 24h and implement refresh token rotation"
        }
      ]
    }
  ],

  "blockers": [
    {
      "checkId": "REL-SCALE-001",
      "category": "reliability",
      "name": "Timeouts on all external calls",
      "severity": "critical",
      "details": "No timeout configured on Stripe API calls - production outage risk",
      "evidence": "src/payments/stripe.ts:42",
      "recommendation": "Add 10s timeout to all Stripe SDK calls with graceful error handling"
    }
  ]
}
```

---

## Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `$schema` | string | yes | Always `"shipkit-artifact"` -- identifies this as a Shipkit-managed file |
| `type` | string | yes | Always `"scale-readiness"` -- artifact type for routing/rendering |
| `version` | string | yes | Schema version for forward compatibility |
| `lastUpdated` | string | yes | ISO date of last modification |
| `source` | string | yes | Always `"shipkit-scale-ready"` |
| `summary` | object | yes | Aggregated data for dashboard rendering |
| `summary.overallStatus` | enum | yes | `"scale-ready"` \| `"needs-work"` \| `"enterprise-ready"` |
| `summary.tier` | enum | yes | `"growth"` \| `"enterprise"` |
| `summary.commit` | string | yes | Git commit hash at time of audit |
| `summary.stack` | string | yes | Tech stack summary from stack.json |
| `summary.counts` | object | yes | Total pass/warning/fail/na/human-verify counts |
| `summary.categoryScores` | object | yes | Per-category breakdown of counts |
| `categories` | array | yes | Full audit results grouped by category |
| `categories[].id` | string | yes | Category slug (`"security"`, `"database"`, `"observability"`, `"performance"`, `"reliability"`, `"operations"`, `"code-maturity"`, `"compliance"`) |
| `categories[].name` | string | yes | Human-readable category name |
| `categories[].tier` | enum | yes | `"growth"` \| `"enterprise"` -- which tier this category belongs to |
| `categories[].checks` | array | yes | Individual checks within this category |
| `categories[].checks[].id` | string | yes | Check ID (e.g., `"SEC-SCALE-001"`) |
| `categories[].checks[].name` | string | yes | What is being checked |
| `categories[].checks[].status` | enum | yes | `"pass"` \| `"warning"` \| `"fail"` \| `"na"` \| `"human-verify"` |
| `categories[].checks[].severity` | enum | yes | `"critical"` \| `"high"` \| `"medium"` \| `"low"` |
| `categories[].checks[].details` | string | yes | What was found |
| `categories[].checks[].evidence` | string | no | File path and line number where finding was observed |
| `categories[].checks[].recommendation` | string | no | How to fix (null if status is `"pass"`) |
| `blockers` | array | yes | Subset of checks with `"fail"` status and `"critical"` or `"high"` severity -- items that block scale readiness |
| `blockers[].checkId` | string | yes | References `categories[].checks[].id` |
| `blockers[].category` | string | yes | Which category this blocker belongs to |
| `blockers[].name` | string | yes | What is being checked |
| `blockers[].severity` | enum | yes | `"critical"` \| `"high"` |
| `blockers[].details` | string | yes | What was found |
| `blockers[].evidence` | string | no | File path and line number |
| `blockers[].recommendation` | string | yes | How to fix |

---

## Summary Object

The `summary` field MUST be kept in sync with the `categories` array. It exists so the dashboard can render overview cards without iterating the full data. Recompute it every time the file is written.

---

## Status Classification

| Status | JSON Value | Meaning |
|--------|-----------|---------|
| Pass | `"pass"` | Implemented correctly |
| Warning | `"warning"` | Partially implemented or could improve |
| Fail | `"fail"` | Missing or broken |
| N/A | `"na"` | Not applicable to this stack |
| Human-Verify | `"human-verify"` | Claude cannot verify, human must check |

---

## Overall Status Logic

- `"scale-ready"` -- Zero `"fail"` checks, warnings are acceptable
- `"needs-work"` -- One or more `"fail"` checks exist
- `"enterprise-ready"` -- Enterprise tier audited, zero `"fail"` checks across all categories including compliance

---

## Severity Levels

| Severity | Meaning | Examples |
|----------|---------|----------|
| Critical | Production outage or security breach risk | No timeouts on external calls; missing auth on admin routes |
| High | Significant reliability or security concern | Missing rate limiting; no connection pooling |
| Medium | Should address before scaling further | Long session expiry; missing structured logging |
| Low | Nice to have for operational excellence | Could add more detailed health checks |

---

## Shipkit Artifact Convention

This skill follows the **Shipkit JSON artifact convention** -- a standard structure for all `.shipkit/*.json` files that enables dashboard visualization.

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

- `$schema` -- Always `"shipkit-artifact"`. Identifies Shipkit artifact files.
- `type` -- The artifact type (`"scale-readiness"`, `"goals"`, `"spec"`, etc.). Dashboard uses this for rendering.
- `version` -- Schema version. Bump when fields change.
- `lastUpdated` -- When this file was last written.
- `source` -- Which skill wrote this file.
- `summary` -- Aggregated data for dashboard cards. Structure varies by type.
