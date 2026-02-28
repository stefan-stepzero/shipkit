# Product Definition Output Schema

This document defines the JSON schema for `.shipkit/product-definition.json` (v3 — product blueprint).

## Full JSON Schema

```json
{
  "$schema": "shipkit-artifact",
  "type": "product-definition",
  "version": "3.0",
  "lastUpdated": "YYYY-MM-DDTHH:MM:SSZ",
  "source": "shipkit-product-definition",

  "product": {
    "name": "Product name",
    "vision": "One-line vision",
    "stage": "poc|mvp|production|scale"
  },

  "problemSpace": {
    "summary": "Brief summary of discovered user needs",
    "keyPainPoints": ["pain-1", "pain-2"],
    "primaryPersona": "persona-1",
    "personaIntents": {
      "persona-1": "Their primaryIntent (multi-user apps)"
    }
  },

  "solutionApproach": "2-3 sentences on how the product addresses needs",

  "features": [
    {
      "id": "F-001",
      "name": "Feature name",
      "description": "What it does from user's perspective",
      "addressesNeeds": ["pain-1"],
      "patterns": ["P-001"],
      "dependencies": []
    }
  ],

  "uxPatterns": [
    {
      "id": "P-001",
      "name": "Pattern name",
      "description": "How users interact with this",
      "usedIn": ["F-001"],
      "rationale": "Why this pattern"
    }
  ],

  "differentiators": [
    {
      "id": "D-001",
      "statement": "What makes this unique",
      "enabledBy": ["F-001", "P-001"]
    }
  ],

  "summary": {
    "totalFeatures": 0,
    "totalPatterns": 0,
    "totalDifferentiators": 0
  }
}
```

## Field Reference

### Top-Level Fields (Shipkit JSON Artifact Convention)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `$schema` | string | yes | Always `"shipkit-artifact"` |
| `type` | string | yes | Always `"product-definition"` |
| `version` | string | yes | `"3.0"` for product blueprint format |
| `lastUpdated` | string | yes | ISO timestamp of last modification |
| `source` | string | yes | Always `"shipkit-product-definition"` |
| `product` | object | yes | Product identity |
| `problemSpace` | object | yes | Summary of discovered user needs |
| `solutionApproach` | string | yes | High-level product approach description |
| `features` | array | yes | User-facing features |
| `uxPatterns` | array | yes | Key interaction patterns |
| `differentiators` | array | yes | What makes this unique |
| `summary` | object | yes | Aggregated counts |

### Product Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Product name |
| `vision` | string | yes | One-line vision (from why.json if available) |
| `stage` | enum | yes | `"poc"` \| `"mvp"` \| `"production"` \| `"scale"` |

### Problem Space Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `summary` | string | yes | Brief narrative of discovered user needs |
| `keyPainPoints` | string[] | yes | IDs from product-discovery.json `painPoints[].id` |
| `primaryPersona` | string | yes | ID from product-discovery.json `personas[].id` |
| `personaIntents` | object | no | Map of persona ID -> `primaryIntent` string. Include for multi-user apps (2+ personas with distinct intents). |

### Feature Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Stable ID: `F-001`, `F-002`, etc. |
| `name` | string | yes | Concise feature name |
| `description` | string | yes | What this feature does from the user's perspective (1-2 sentences) |
| `addressesNeeds` | string[] | yes | Pain point IDs from product-discovery.json |
| `patterns` | string[] | yes | UX pattern IDs this feature follows |
| `dependencies` | string[] | yes | Feature IDs that must exist first (empty array if none) |

### UX Pattern Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Stable ID: `P-001`, `P-002`, etc. |
| `name` | string | yes | Pattern name (e.g., "wizard flow", "live preview") |
| `description` | string | yes | How users experience this pattern |
| `usedIn` | string[] | yes | Feature IDs that use this pattern |
| `rationale` | string | yes | Why this pattern over alternatives |

### Differentiator Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Stable ID: `D-001`, `D-002`, etc. |
| `statement` | string | yes | What makes this unique — a clear differentiator claim |
| `enabledBy` | string[] | yes | Feature and/or pattern IDs that enable this |

### Summary Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `totalFeatures` | number | yes | Count of features array |
| `totalPatterns` | number | yes | Count of uxPatterns array |
| `totalDifferentiators` | number | yes | Count of differentiators array |

**Recompute summary every time the file is written.**

## Graph Relationships

The ID-based cross-references enable these traversals:

| From | To | Via |
|------|----|-----|
| Feature | Pain Points (discovery) | `features[].addressesNeeds` |
| Feature | UX Patterns | `features[].patterns` |
| UX Pattern | Features | `uxPatterns[].usedIn` |
| Differentiator | Features/Patterns | `differentiators[].enabledBy` |
| Problem Space | Pain Points (discovery) | `problemSpace.keyPainPoints` |
| Problem Space | Personas (discovery) | `problemSpace.primaryPersona` |

## Cross-File References

Product-definition.json is consumed by:
- `engineering-definition.json` — mechanisms reference `features[].id` via `implementsFeatures`
- `goals.json` — criteria derive from features and patterns

## Migration from v2

v3 removes fields that moved to engineering-definition.json:
- `mechanisms` -> now in `.shipkit/engineering-definition.json`
- `designDecisions` -> now in `.shipkit/engineering-definition.json`
- `stackDirection` -> now in `.shipkit/engineering-definition.json`
- `features[].mechanisms` -> removed (mechanisms now reference features, not vice versa)
- Features now have `addressesNeeds` (pain point traceability, previously on mechanisms)

## Shipkit Artifact Convention

Every JSON artifact MUST include these top-level fields:

```json
{
  "$schema": "shipkit-artifact",
  "type": "<artifact-type>",
  "version": "3.0",
  "lastUpdated": "YYYY-MM-DDTHH:MM:SSZ",
  "source": "<skill-name>",
  "summary": { ... }
}
```
