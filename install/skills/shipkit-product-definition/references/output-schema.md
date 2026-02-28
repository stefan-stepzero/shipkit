# Product Definition Output Schema

This document defines the JSON schema for `.shipkit/product-definition.json` (v2 — solution blueprint).

## Full JSON Schema

```json
{
  "$schema": "shipkit-artifact",
  "type": "product-definition",
  "version": "2.0",
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
    "primaryPersona": "persona-1"
  },

  "solutionApproach": "2-3 sentences on how the solution addresses needs",

  "mechanisms": [
    {
      "id": "M-001",
      "name": "Mechanism name",
      "description": "What this mechanism does and how",
      "addressesNeeds": ["pain-1"],
      "designChoices": [
        { "decision": "What was decided", "rationale": "Why", "alternatives": ["Rejected"] }
      ]
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
      "enabledBy": ["M-001", "P-001"]
    }
  ],

  "designDecisions": [
    {
      "decision": "Key choice",
      "rationale": "Why",
      "alternatives": ["Considered options"]
    }
  ],

  "stackDirection": {
    "recommended": { "frontend": "...", "backend": "...", "database": "...", "hosting": "..." },
    "rationale": "Why these choices",
    "constraints": ["Driving factors"],
    "note": "Only for greenfield"
  },

  "features": [
    {
      "id": "F-001",
      "name": "Feature name",
      "description": "What it does",
      "mechanisms": ["M-001"],
      "patterns": ["P-001"],
      "dependencies": []
    }
  ],

  "summary": {
    "totalMechanisms": 0,
    "totalPatterns": 0,
    "totalDifferentiators": 0,
    "totalFeatures": 0
  }
}
```

## Field Reference

### Top-Level Fields (Shipkit JSON Artifact Convention)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `$schema` | string | yes | Always `"shipkit-artifact"` |
| `type` | string | yes | Always `"product-definition"` |
| `version` | string | yes | `"2.0"` for solution blueprint format |
| `lastUpdated` | string | yes | ISO timestamp of last modification |
| `source` | string | yes | Always `"shipkit-product-definition"` |
| `product` | object | yes | Product identity |
| `problemSpace` | object | yes | Summary of discovered user needs |
| `solutionApproach` | string | yes | High-level solution description |
| `mechanisms` | array | yes | Core technical/product mechanisms |
| `uxPatterns` | array | yes | Key interaction patterns |
| `differentiators` | array | yes | What makes this unique |
| `designDecisions` | array | yes | Key choices with rationale |
| `stackDirection` | object | no | Technology recommendations (greenfield only) |
| `features` | array | yes | Feature list grounded in mechanisms/patterns |
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
| `personaIntents` | object | no | Map of persona ID → `primaryIntent` string. Include for multi-user apps (2+ personas with distinct intents). Enables downstream skills to map mechanisms/criteria to specific user types. |

### Mechanism Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Stable ID: `M-001`, `M-002`, etc. |
| `name` | string | yes | Concise mechanism name |
| `description` | string | yes | How this mechanism works at a conceptual level |
| `addressesNeeds` | string[] | yes | Pain point IDs from product-discovery.json |
| `designChoices` | object[] | no | Key decisions made for this mechanism |

### Design Choice Object (within Mechanism)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `decision` | string | yes | What was decided |
| `rationale` | string | yes | Why this choice |
| `alternatives` | string[] | no | Options that were considered but rejected |

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
| `enabledBy` | string[] | yes | Mechanism and/or pattern IDs that enable this |

### Design Decision Object (Top-Level)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `decision` | string | yes | What was decided |
| `rationale` | string | yes | Why this direction |
| `alternatives` | string[] | no | What was considered but rejected |

### Stack Direction Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `recommended` | object | yes | Technology choices by category |
| `recommended.frontend` | string | no | Frontend framework/library |
| `recommended.backend` | string | no | Backend framework/runtime |
| `recommended.database` | string | no | Database technology |
| `recommended.hosting` | string | no | Deployment platform |
| `rationale` | string | yes | Why these technologies |
| `constraints` | string[] | no | What drove the technology choices |
| `note` | string | no | Additional context (e.g., "greenfield only") |

**Note**: `stackDirection` is only populated for greenfield projects. If `.shipkit/stack.json` already exists, this section is omitted.

### Feature Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Stable ID: `F-001`, `F-002`, etc. |
| `name` | string | yes | Concise feature name |
| `description` | string | yes | What this feature does (1-2 sentences) |
| `mechanisms` | string[] | yes | Mechanism IDs this feature uses |
| `patterns` | string[] | yes | UX pattern IDs this feature follows |
| `dependencies` | string[] | yes | Feature IDs that must exist first (empty array if none) |

### Summary Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `totalMechanisms` | number | yes | Count of mechanisms array |
| `totalPatterns` | number | yes | Count of uxPatterns array |
| `totalDifferentiators` | number | yes | Count of differentiators array |
| `totalFeatures` | number | yes | Count of features array |

**Recompute summary every time the file is written.**

## Graph Relationships

The ID-based cross-references enable these traversals:

| From | To | Via |
|------|----|-----|
| Mechanism | Pain Points (discovery) | `mechanisms[].addressesNeeds` |
| UX Pattern | Features | `uxPatterns[].usedIn` |
| Feature | Mechanisms | `features[].mechanisms` |
| Feature | UX Patterns | `features[].patterns` |
| Differentiator | Mechanisms/Patterns | `differentiators[].enabledBy` |
| Problem Space | Pain Points (discovery) | `problemSpace.keyPainPoints` |
| Problem Space | Personas (discovery) | `problemSpace.primaryPersona` |

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
