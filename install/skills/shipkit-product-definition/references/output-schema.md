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
      "assertion": "The testable form — a checkable claim about the built product",
      "nonNegotiable": true,
      "enabledBy": ["F-001", "P-001"]
    }
  ],

  "qualityBar": [
    {
      "id": "Q-001",
      "dimension": "interaction|feedback|empty-state|error|performance|accessibility|content",
      "assertion": "Testable interaction/quality standard the build is scored against",
      "appliesTo": ["F-001"]
    }
  ],

  "summary": {
    "totalFeatures": 0,
    "totalPatterns": 0,
    "totalDifferentiators": 0,
    "totalQualityBar": 0
  }
}
```

## The Essence Block (Phase-3 fidelity target)

`differentiators` + `qualityBar` together capture the app's **essence** — what makes it *this* app and
the quality bar it holds itself to — as **checkable criteria**, so a downstream eval can score a built
app for fidelity rather than judging prose.

- **Essence scored by an eval** = `differentiators[]` items where `nonNegotiable: true` (via each
  `assertion`) **+** every `qualityBar[]` assertion.
- Every `assertion` must be **observable and binary-checkable** (yes / no / partially) against a built
  screen or behaviour — not a feeling. Avoid "clean", "modern", "intuitive", "seamless" unless paired
  with a measurable spec.
- The `qualityBar` is the behavioural/interaction standard. It **references** the design system for
  aesthetic direction (tokens/principles) rather than duplicating it.

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
| `differentiators` | array | yes | What makes this unique (essence — with testable assertions) |
| `qualityBar` | array | yes | Interaction/product quality bar as testable assertions (essence) |
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
| `assertion` | string | yes | The differentiator restated as a **testable assertion** — an observable, binary-checkable claim about the built product that an eval can score |
| `nonNegotiable` | boolean | no | `true` for the essence-floor differentiators that must ship faithfully. Defaults to `true` when omitted (differentiators are non-negotiable by intent). |
| `enabledBy` | string[] | yes | Feature and/or pattern IDs that enable this |

### Quality Bar Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Stable ID: `Q-001`, `Q-002`, etc. |
| `dimension` | string | yes | Which quality dimension: `interaction`, `feedback`, `empty-state`, `error`, `performance`, `accessibility`, `content` (extend as needed) |
| `assertion` | string | yes | The interaction/quality standard as a **testable assertion** — observable and binary-checkable against a built screen/behaviour |
| `appliesTo` | string[] | yes | Feature IDs this bar holds (empty array = app-wide) |

### Summary Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `totalFeatures` | number | yes | Count of features array |
| `totalPatterns` | number | yes | Count of uxPatterns array |
| `totalDifferentiators` | number | yes | Count of differentiators array |
| `totalQualityBar` | number | yes | Count of qualityBar array |

**Recompute summary every time the file is written.**

## Graph Relationships

The ID-based cross-references enable these traversals:

| From | To | Via |
|------|----|-----|
| Feature | Pain Points (discovery) | `features[].addressesNeeds` |
| Feature | UX Patterns | `features[].patterns` |
| UX Pattern | Features | `uxPatterns[].usedIn` |
| Differentiator | Features/Patterns | `differentiators[].enabledBy` |
| Quality Bar | Features | `qualityBar[].appliesTo` |
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
