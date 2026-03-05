# Product Goals Output Schema

This document defines the JSON schema for `.shipkit/goals/product.json` (v4.0).

> **Strategic goals schema** (`goals/strategic.json`) is documented in `/shipkit-stage/references/output-schema.md`.

## goals/product.json

```json
{
  "$schema": "shipkit-artifact",
  "type": "goals-product",
  "version": "4.0",
  "lastUpdated": "YYYY-MM-DDTHH:MM:SSZ",
  "source": "shipkit-product-goals",

  "derivedFrom": {
    "productDefinition": ".shipkit/product-definition.json",
    "productDiscovery": ".shipkit/product-discovery.json"
  },

  "criteria": [ "...criterion objects..." ],

  "summary": {
    "totalCriteria": 0,
    "byStatus": { "not-measured": 0, "below-threshold": 0, "at-threshold": 0, "exceeded": 0 },
    "byCheckability": { "verifiable": 0, "observable": 0 }
  }
}
```

## Criterion Object

```json
{
  "id": "P-001",
  "name": "Human-readable name",
  "category": "user-outcome",
  "metric": "What to measure",
  "threshold": "Target value (e.g., '> 80%', '< 3 seconds')",
  "currentValue": null,
  "verificationMethod": "manual-check|analytics|automated-test|user-feedback",
  "checkability": "verifiable|observable",
  "verificationTool": "build|test|lint|semantic-qa|visual-qa|manual|none",
  "gate": "gate-slug",
  "status": "not-measured|below-threshold|at-threshold|exceeded",
  "derivedFrom": { "type": "pattern|differentiator|feature", "id": "P-001" },
  "painPointAddressed": "pain-1",
  "notes": "Optional context"
}
```

## ID Convention

| Prefix | Owner | Category | Defined By |
|--------|-------|----------|------------|
| `P-` | PM | user-outcome | `/shipkit-product-goals` |
| `S-` | Visionary | business-metric | `/shipkit-stage` |
| `E-` | EM | technical-performance | `/shipkit-engineering-goals` |

## Gate Notes

Gates are defined in `strategic.json` by `/shipkit-stage` with S-* criteria. This skill appends P-* IDs to existing gates. Engineering criteria (E-*) are added by `/shipkit-engineering-goals`.

## Shipkit Artifact Convention

Every JSON artifact MUST include: `$schema`, `type`, `version`, `lastUpdated`, `source`, `summary`.
