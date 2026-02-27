# Goals Output Schema

This document defines the JSON schema for `.shipkit/goals.json` (v2 — success criteria & stage gates).

## Full JSON Schema

```json
{
  "$schema": "shipkit-artifact",
  "type": "goals",
  "version": "2.0",
  "lastUpdated": "YYYY-MM-DDTHH:MM:SSZ",
  "source": "shipkit-goals",

  "stage": {
    "current": "mvp",
    "target": "production"
  },

  "derivedFrom": {
    "productDefinition": ".shipkit/product-definition.json",
    "productDiscovery": ".shipkit/product-discovery.json"
  },

  "criteria": [
    {
      "id": "criterion-slug",
      "name": "Human-readable name",
      "category": "user-outcome|technical-performance|business-metric",
      "metric": "What to measure",
      "threshold": "Target value (e.g., '> 80%', '< 3 seconds')",
      "currentValue": null,
      "verificationMethod": "manual-check|analytics|automated-test|user-feedback",
      "gate": "gate-slug",
      "status": "not-measured|below-threshold|at-threshold|exceeded",
      "derivedFrom": {
        "type": "mechanism|pattern|differentiator|mvpBoundary",
        "id": "M-001"
      },
      "painPointAddressed": "pain-1",
      "notes": "Optional context"
    }
  ],

  "gates": [
    {
      "id": "gate-slug",
      "name": "Gate name",
      "description": "What passing this gate means",
      "criteria": ["criterion-slug-1", "criterion-slug-2"],
      "status": "blocked|partial|passed",
      "passedAt": null
    }
  ],

  "summary": {
    "totalCriteria": 0,
    "byCategory": { "user-outcome": 0, "technical-performance": 0, "business-metric": 0 },
    "byStatus": { "not-measured": 0, "below-threshold": 0, "at-threshold": 0, "exceeded": 0 },
    "totalGates": 0,
    "gatesPassed": 0
  }
}
```

## Field Reference

### Top-Level Fields (Shipkit JSON Artifact Convention)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `$schema` | string | yes | Always `"shipkit-artifact"` |
| `type` | string | yes | Always `"goals"` |
| `version` | string | yes | `"2.0"` for success criteria format |
| `lastUpdated` | string | yes | ISO timestamp of last modification |
| `source` | string | yes | Always `"shipkit-goals"` |
| `stage` | object | yes | Current and target project stage |
| `derivedFrom` | object | yes | Source artifacts for traceability |
| `criteria` | array | yes | Measurable success criteria |
| `gates` | array | yes | Named stage gates composed of criteria |
| `summary` | object | yes | Aggregated counts |

### Stage Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `current` | string | yes | Current stage: `"poc"` \| `"mvp"` \| `"production"` \| `"scale"` |
| `target` | string | yes | Target stage for this criteria set |

### Derived From Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `productDefinition` | string | yes | Path to product-definition.json |
| `productDiscovery` | string | no | Path to product-discovery.json (if used for traceability) |

### Criterion Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Slug identifier (kebab-case, prefixed with `criterion-`) |
| `name` | string | yes | Human-readable name |
| `category` | enum | yes | `"user-outcome"` \| `"technical-performance"` \| `"business-metric"` |
| `metric` | string | yes | What specifically to measure (e.g., "wizard completion rate") |
| `threshold` | string | yes | Target value with comparator (e.g., "> 80%", "< 3 seconds", "= 0 critical bugs") |
| `currentValue` | string\|null | yes | Latest measurement, or `null` if not yet measured |
| `verificationMethod` | enum | yes | `"manual-check"` \| `"analytics"` \| `"automated-test"` \| `"user-feedback"` |
| `gate` | string | yes | ID of the stage gate this criterion belongs to |
| `status` | enum | yes | `"not-measured"` \| `"below-threshold"` \| `"at-threshold"` \| `"exceeded"` |
| `derivedFrom` | object | yes | Traceability to solution blueprint |
| `painPointAddressed` | string | no | Pain point ID from product-discovery.json |
| `notes` | string | no | Additional context |

### Derived From Object (within Criterion)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | enum | yes | `"mechanism"` \| `"pattern"` \| `"differentiator"` \| `"mvpBoundary"` |
| `id` | string | yes | ID from product-definition.json (e.g., "M-001", "P-001", "D-001") |

### Category Values

| Category | Focus | Derived From |
|----------|-------|-------------|
| `user-outcome` | Can users accomplish their goals? Task completion, satisfaction, time-to-value | UX patterns, differentiators |
| `technical-performance` | Does the system perform? Speed, reliability, quality, scalability | Mechanisms |
| `business-metric` | Does it drive the business? Retention, conversion, engagement | Differentiators, MVP boundary |

### Verification Methods

| Method | When to Use | Example |
|--------|------------|---------|
| `manual-check` | Human review required | "Review 20 generated worksheets for accuracy" |
| `analytics` | Track in product analytics | "Measure wizard completion rate in Mixpanel" |
| `automated-test` | Programmatic verification | "Load test: 95th percentile response < 3s" |
| `user-feedback` | Ask users directly | "Survey: 'Did the worksheet match your needs?'" |

### Status Values

| Status | Meaning |
|--------|---------|
| `not-measured` | Criterion defined but no measurement taken yet |
| `below-threshold` | Measured but not meeting the threshold |
| `at-threshold` | Meeting the threshold value |
| `exceeded` | Exceeding the threshold value |

### Gate Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Slug identifier (kebab-case) |
| `name` | string | yes | Human-readable gate name (e.g., "MVP Launch Ready") |
| `description` | string | yes | What passing this gate means for the project |
| `criteria` | string[] | yes | Array of criterion IDs that must pass for this gate |
| `status` | enum | yes | `"blocked"` \| `"partial"` \| `"passed"` |
| `passedAt` | string\|null | yes | ISO timestamp when gate passed, or `null` |

### Gate Status Values

| Status | Meaning |
|--------|---------|
| `blocked` | No criteria in this gate have been measured or met |
| `partial` | Some criteria met, others still below threshold or not measured |
| `passed` | All criteria in this gate are at-threshold or exceeded |

### Summary Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `totalCriteria` | number | yes | Count of criteria array |
| `byCategory` | object | yes | Counts per category |
| `byStatus` | object | yes | Counts per status |
| `totalGates` | number | yes | Count of gates array |
| `gatesPassed` | number | yes | Count of gates with status "passed" |

**Recompute summary every time the file is written.**

## Graph Relationships

The ID-based cross-references enable these traversals:

| From | To | Via |
|------|----|-----|
| Criterion | Mechanism/Pattern/Differentiator (definition) | `criteria[].derivedFrom` |
| Criterion | Pain Point (discovery) | `criteria[].painPointAddressed` |
| Criterion | Gate | `criteria[].gate` |
| Gate | Criteria | `gates[].criteria` |
| Goals artifact | Product Definition | `derivedFrom.productDefinition` |
| Goals artifact | Product Discovery | `derivedFrom.productDiscovery` |

## Shipkit Artifact Convention

Every JSON artifact MUST include these top-level fields:

```json
{
  "$schema": "shipkit-artifact",
  "type": "<artifact-type>",
  "version": "2.0",
  "lastUpdated": "YYYY-MM-DDTHH:MM:SSZ",
  "source": "<skill-name>",
  "summary": { ... }
}
```
