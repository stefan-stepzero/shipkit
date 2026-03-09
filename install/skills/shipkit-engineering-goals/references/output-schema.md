# Engineering Goals Output Schema

This document defines the JSON schema for `.shipkit/goals/engineering.json` (v4.0).

## goals/engineering.json

```json
{
  "$schema": "shipkit-artifact",
  "type": "goals-engineering",
  "version": "4.0",
  "lastUpdated": "YYYY-MM-DDTHH:MM:SSZ",
  "source": "shipkit-engineering-goals",

  "derivedFrom": {
    "engineeringDefinition": ".shipkit/engineering-definition.json"
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
  "id": "E-001",
  "name": "Human-readable name",
  "category": "technical-performance",
  "metric": "What to measure",
  "threshold": "Target value (e.g., '< 500ms', '> 99%')",
  "rubric": [
    { "range": "Level range", "meaning": "What this level looks like in practice" }
  ],
  "currentValue": null,
  "verificationMethod": "automated-test|analytics",
  "checkability": "verifiable|observable",
  "verificationTool": "build|test|lint|semantic-qa|none",
  "gate": "gate-slug",
  "status": "not-measured|below-threshold|at-threshold|exceeded",
  "derivedFrom": { "type": "mechanism", "id": "M-001" },
  "notes": "Optional context"
}
```

## ID Convention

| Prefix | Owner | Category |
|--------|-------|----------|
| `E-` | EM | technical-performance |

## Gate Integration

Engineering criteria reference gates defined in `goals/strategic.json`. When this skill runs, it adds E-* IDs to existing gate `criteria` arrays. If strategic.json doesn't exist, gates can be defined locally.

## Shipkit Artifact Convention

Every JSON artifact MUST include: `$schema`, `type`, `version`, `lastUpdated`, `source`, `summary`.
