# Strategic Goals Output Schema

This document defines the JSON schema for `.shipkit/goals/strategic.json` (v5.0).

## goals/strategic.json

```json
{
  "$schema": "shipkit-artifact",
  "type": "goals-strategic",
  "version": "5.0",
  "lastUpdated": "YYYY-MM-DDTHH:MM:SSZ",
  "source": "shipkit-stage",

  "stage": {
    "current": "mvp",
    "target": "scale"
  },

  "constraints": {
    "quality": "Description of quality bar",
    "scope": "Description of scope limit",
    "cost_budget": "Description of cost allowance"
  },

  "stageImplications": {
    "skip": ["scale testing", "enterprise features"],
    "focus": ["launch readiness", "user experience", "reliability"],
    "qualityBar": "works for customers"
  },

  "derivedFrom": {
    "why": ".shipkit/why.json"
  },

  "criteria": [ "...criterion objects..." ],

  "gates": [
    {
      "id": "gate-slug",
      "name": "Gate name",
      "description": "What passing this gate means",
      "criteria": ["S-001", "P-001", "E-001"],
      "status": "blocked|partial|passed",
      "passedAt": null,
      "verifiableStatus": "blocked|partial|passed",
      "verifiablePassedAt": null
    }
  ],

  "summary": {
    "totalCriteria": 0,
    "byStatus": { "not-measured": 0, "below-threshold": 0, "at-threshold": 0, "exceeded": 0 },
    "byCheckability": { "verifiable": 0, "observable": 0 }
  }
}
```

## New in v5.0

### `stageImplications` (new field)

Cascades stage-aware behavior to all agents:

| Stage | skip | focus | qualityBar |
|-------|------|-------|------------|
| POC | tests, lint, docs, error handling | functional proof | "it works" |
| Alpha | load testing, security audit | core usability | "reliable" |
| MVP | scale testing, enterprise features | launch readiness | "production-ready" |
| Scale | nothing | growth + operational excellence | "enterprise-ready" |

Agents read `stageImplications` to calibrate their output:
- PM: scope specs to current-stage features
- EM: skip/include patterns based on `skip` array
- Execution Lead: calibrate verification depth

### `source` field

Changed from `"shipkit-product-goals"` to `"shipkit-stage"`.

### `derivedFrom` field

References only `why.json` (no longer includes `productDiscovery`).

## Criterion Object

```json
{
  "id": "S-001",
  "name": "Human-readable name",
  "category": "business-metric",
  "metric": "What to measure",
  "threshold": "Target value (e.g., '> 100 DAU', '> 40% retention')",
  "currentValue": null,
  "verificationMethod": "analytics|user-feedback",
  "checkability": "observable",
  "verificationTool": "none",
  "gate": "gate-slug",
  "status": "not-measured|below-threshold|at-threshold|exceeded",
  "notes": "Optional context"
}
```

## ID Convention

| Prefix | Owner | Category | Defined By |
|--------|-------|----------|------------|
| `S-` | Visionary | business-metric | `/shipkit-stage` |
| `P-` | PM | user-outcome | `/shipkit-product-goals` |
| `E-` | EM | technical-performance | `/shipkit-engineering-goals` |

## Gate Notes

Gates are defined in `strategic.json` by `/shipkit-stage` with S-* criteria only. Other skills append their criteria:
- `/shipkit-product-goals` appends P-* IDs
- `/shipkit-engineering-goals` appends E-* IDs

Gates reference criteria across all three goal files. Evaluate mode in `/shipkit-stage` cross-checks all of them.

## Shipkit Artifact Convention

Every JSON artifact MUST include: `$schema`, `type`, `version`, `lastUpdated`, `source`, `summary`.
