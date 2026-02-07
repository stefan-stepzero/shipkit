# Preflight Output Schema

This document defines the JSON schema for `.shipkit/preflight.json` produced by the `shipkit-preflight` skill.

---

## Full JSON Schema

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
      "evidence": "src/middleware/auth.ts:15 - requireAuth applied to all /api/protected/* routes",
      "file": "src/middleware/auth.ts",
      "line": 15,
      "statusChange": null,
      "details": "All 12 protected routes have auth middleware"
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
    }
  ],

  "context": {
    "project": "From why.json",
    "stack": "From stack.json",
    "deployment": "Target platform"
  }
}
```

---

## Field Reference

### Envelope Fields (Required)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `$schema` | string | yes | Always `"shipkit-artifact"` - identifies this as a Shipkit-managed file |
| `type` | string | yes | Always `"preflight"` - artifact type for routing/rendering |
| `version` | string | yes | Schema version for forward compatibility |
| `lastUpdated` | string | yes | ISO date of last modification |
| `source` | string | yes | Always `"shipkit-preflight"` |

### Summary Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `summary` | object | yes | Aggregated counts for dashboard rendering |
| `summary.overallStatus` | enum | yes | `"ready"` \| `"ready-with-warnings"` \| `"not-ready"` |
| `summary.readinessScore` | number | yes | 0-100 percentage (pass / (pass + fail + warning) * 100) |
| `summary.scope` | enum | yes | `"full"` \| `"incremental"` \| `"quick-verify"` |
| `summary.commit` | string | yes | Git commit hash at time of audit |
| `summary.filesChecked` | number | yes | Number of source files scanned |
| `summary.previousAuditCommit` | string | no | Commit hash of last audit (for incremental) |
| `summary.counts` | object | yes | Total pass/fail/warning/notApplicable/unchanged |
| `summary.byCategory` | object | yes | Per-category breakdown with `changed` flag for incremental |

The `summary` field MUST be kept in sync with the `checks` array. It exists so the dashboard can render overview cards without iterating the full array. Recompute it every time the file is written.

### Checks Array

| Field | Type | Required | Description |
|-------|------|----------|-------------|
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

### Blockers Array

| Field | Type | Required | Description |
|-------|------|----------|-------------|
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

### Recommendations Array

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `recommendations` | array | yes | Non-critical issues extracted from checks where status is `"warning"` |
| `recommendations[].checkId` | string | yes | References `checks[].id` |
| `recommendations[].category` | string | yes | Category slug |
| `recommendations[].name` | string | yes | Issue title |
| `recommendations[].severity` | string | yes | Always `"warning"` |
| `recommendations[].suggestion` | string | yes | What to do about it |
| `recommendations[].effort` | enum | no | `"low"` \| `"medium"` \| `"high"` |

### Status Changes Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `statusChanges` | object | yes | Delta from previous audit |
| `statusChanges.fixed` | array | yes | Checks that were failing but now pass |
| `statusChanges.newIssues` | array | yes | Checks that are new failures |
| `statusChanges.regressions` | array | yes | Checks that were passing but now fail |

### Audit History Array

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `auditHistory` | array | yes | Previous audit summaries (append on each full audit) |

### Context Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `context` | object | yes | Project context used for this audit |

---

## Determining Overall Status

- `"not-ready"` - Any blockers exist (checks with status `"fail"`)
- `"ready-with-warnings"` - No blockers, but recommendations exist (checks with status `"warning"`)
- `"ready"` - All checks pass or are not-applicable

---

## Shipkit Artifact Convention

This skill follows the **Shipkit JSON artifact convention** - a standard structure for all `.shipkit/*.json` files that enables mission control visualization.

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

- `$schema` - Always `"shipkit-artifact"`. Lets the reporter hook identify files to ship to mission control.
- `type` - The artifact type (`"preflight"`, `"goals"`, `"spec"`, etc.). Dashboard uses this for rendering.
- `version` - Schema version. Bump when fields change.
- `lastUpdated` - When this file was last written.
- `source` - Which skill wrote this file.
- `summary` - Aggregated data for dashboard cards. Structure varies by type.
