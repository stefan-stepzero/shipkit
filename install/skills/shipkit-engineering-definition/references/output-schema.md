# Engineering Definition Output Schema

This document defines the JSON schema for `.shipkit/engineering-definition.json` (v1 — technical approach).

## Full JSON Schema

```json
{
  "$schema": "shipkit-artifact",
  "type": "engineering-definition",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DDTHH:MM:SSZ",
  "source": "shipkit-engineering-definition",

  "product": {
    "name": "Product name",
    "stage": "poc|mvp|production|scale"
  },

  "mechanisms": [
    {
      "id": "M-001",
      "name": "Mechanism name",
      "description": "How this works technically",
      "implementsFeatures": ["F-001"],
      "designChoices": [
        { "decision": "What was decided", "rationale": "Why", "alternatives": ["Rejected"] }
      ]
    }
  ],

  "components": [
    {
      "id": "C-001",
      "name": "Component name",
      "responsibility": "What this component owns",
      "mechanisms": ["M-001"],
      "interfaces": ["REST API to C-002"]
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

  "summary": {
    "totalMechanisms": 0,
    "totalComponents": 0,
    "totalDesignDecisions": 0
  }
}
```

## Field Reference

### Top-Level Fields (Shipkit JSON Artifact Convention)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `$schema` | string | yes | Always `"shipkit-artifact"` |
| `type` | string | yes | Always `"engineering-definition"` |
| `version` | string | yes | `"1.0"` for initial format |
| `lastUpdated` | string | yes | ISO timestamp of last modification |
| `source` | string | yes | Always `"shipkit-engineering-definition"` |
| `product` | object | yes | Product identity (mirrored from product-definition) |
| `mechanisms` | array | yes | Core technical mechanisms |
| `components` | array | yes | System component structure |
| `designDecisions` | array | yes | Cross-cutting technical choices |
| `stackDirection` | object | no | Technology recommendations (greenfield only) |
| `summary` | object | yes | Aggregated counts |

### Product Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Product name (from product-definition.json) |
| `stage` | enum | yes | `"poc"` \| `"mvp"` \| `"production"` \| `"scale"` |

### Mechanism Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Stable ID: `M-001`, `M-002`, etc. |
| `name` | string | yes | Concise mechanism name |
| `description` | string | yes | How this mechanism works at a technical level |
| `implementsFeatures` | string[] | yes | Feature IDs from product-definition.json `features[].id` |
| `designChoices` | object[] | no | Key decisions made for this mechanism |

### Design Choice Object (within Mechanism)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `decision` | string | yes | What was decided |
| `rationale` | string | yes | Why this choice |
| `alternatives` | string[] | no | Options that were considered but rejected |

### Component Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Stable ID: `C-001`, `C-002`, etc. |
| `name` | string | yes | Component/module/service name |
| `responsibility` | string | yes | What this component owns (single responsibility) |
| `mechanisms` | string[] | yes | Mechanism IDs this component implements |
| `interfaces` | string[] | yes | How it communicates with other components (empty array if standalone) |

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

### Summary Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `totalMechanisms` | number | yes | Count of mechanisms array |
| `totalComponents` | number | yes | Count of components array |
| `totalDesignDecisions` | number | yes | Count of designDecisions array |

**Recompute summary every time the file is written.**

## Graph Relationships

The ID-based cross-references enable these traversals:

| From | To | Via |
|------|----|-----|
| Mechanism | Features (product-definition) | `mechanisms[].implementsFeatures` |
| Component | Mechanisms | `components[].mechanisms` |
| Feature (product-definition) | Mechanisms | Reverse lookup: mechanisms where `implementsFeatures` contains feature ID |

## Cross-File References

Engineering-definition.json references product-definition.json:
- `mechanisms[].implementsFeatures` → `features[].id` in product-definition.json
- `product.name` mirrored from product-definition.json

## Shipkit Artifact Convention

Every JSON artifact MUST include these top-level fields:

```json
{
  "$schema": "shipkit-artifact",
  "type": "<artifact-type>",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DDTHH:MM:SSZ",
  "source": "<skill-name>",
  "summary": { ... }
}
```
