# Spec Roadmap Output Schema

This document defines the JSON schema for `.shipkit/spec-roadmap.json` (v1.0 — prioritized spec backlog from definitions + goals).

## Full JSON Schema

```json
{
  "$schema": "shipkit-artifact",
  "type": "spec-roadmap",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DDTHH:MM:SSZ",
  "source": "shipkit-spec-roadmap",

  "product": {
    "name": "Product Name",
    "stage": "mvp"
  },

  "phases": [
    {
      "id": "phase-1",
      "name": "MVP Launch Ready",
      "gateId": "gate-mvp-launch",
      "items": [
        {
          "priority": 1,
          "featureId": "F-001",
          "featureName": "Worksheet Creator",
          "effort": "L",
          "effortDays": 8,
          "mechanisms": ["M-001", "M-003"],
          "dependencies": [],
          "dependedUponBy": ["F-003", "F-004"],
          "addressesNeeds": ["pain-time-creating", "pain-generic-content"],
          "specStatus": "none",
          "scoring": {
            "foundationValue": 8,
            "painCoverage": 3,
            "dependencyDepth": 0
          }
        }
      ]
    }
  ],

  "completed": [
    {
      "featureId": "F-006",
      "featureName": "User Authentication",
      "specPath": "specs/active/user-auth.json",
      "specStatus": "active"
    }
  ],

  "dependencyGraph": {
    "edges": [
      { "from": "F-003", "to": "F-001" }
    ],
    "warnings": [
      "F-005 depends on F-003 → F-001 (chain of 2)"
    ]
  },

  "summary": {
    "totalFeatures": 10,
    "specced": 2,
    "unspecced": 8,
    "phases": 2,
    "effortBreakdown": {
      "XS": 1,
      "S": 2,
      "M": 3,
      "L": 1,
      "XL": 1
    },
    "estimatedTotalDays": 45
  }
}
```

## Field Reference

### Top-Level Fields (Shipkit JSON Artifact Convention)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `$schema` | string | yes | Always `"shipkit-artifact"` |
| `type` | string | yes | Always `"spec-roadmap"` |
| `version` | string | yes | `"1.0"` for spec roadmap format |
| `lastUpdated` | string | yes | ISO timestamp of last modification |
| `source` | string | yes | Always `"shipkit-spec-roadmap"` |
| `product` | object | yes | Product metadata |
| `phases` | array | yes | Ordered phases with prioritized items |
| `completed` | array | yes | Features that already have specs |
| `dependencyGraph` | object | yes | Dependency edges and warnings |
| `summary` | object | yes | Aggregated counts |

### Product Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Product name from product-definition.json |
| `stage` | string | yes | Current stage: `"poc"` \| `"mvp"` \| `"production"` \| `"scale"` |

### Phase Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Phase identifier (e.g., `"phase-1"`) |
| `name` | string | yes | Human-readable phase name (e.g., "MVP Launch Ready") |
| `gateId` | string\|null | yes | ID of the goal gate this phase maps to, or `null` if no goals defined |
| `items` | array | yes | Prioritized features in this phase |

### Phase Item Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `priority` | number | yes | Priority rank within the phase (1 = highest) |
| `featureId` | string | yes | Feature ID from product-definition.json (e.g., `"F-001"`) |
| `featureName` | string | yes | Human-readable feature name |
| `effort` | enum | yes | T-shirt size: `"XS"` \| `"S"` \| `"M"` \| `"L"` \| `"XL"` |
| `effortDays` | number | yes | Rough midpoint estimate in days (for summary math only) |
| `mechanisms` | string[] | yes | Mechanism IDs from engineering-definition.json |
| `dependencies` | string[] | yes | Feature IDs that must be specced before this one |
| `dependedUponBy` | string[] | yes | Feature IDs that depend on this one |
| `addressesNeeds` | string[] | yes | Pain point IDs from product-discovery.json |
| `specStatus` | enum | yes | `"none"` \| `"todo"` \| `"active"` \| `"shipped"` |
| `scoring` | object | yes | Transparent scoring breakdown |

### Scoring Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `foundationValue` | number | yes | 0-10 scale — how many features depend on this one |
| `painCoverage` | number | yes | 0-10 scale — how many user pain points addressed |
| `dependencyDepth` | number | yes | 0-N — depth in dependency chain (0 = no prerequisites) |

### Effort Sizes

| Size | Mechanisms | Design Choices | Midpoint Days |
|------|-----------|----------------|--------------|
| XS | 0 | 0 | 0.5 |
| S | 1 | 0-1 | 1.5 |
| M | 1-2 | 2-3 | 4 |
| L | 2-3 | 4-6 | 8 |
| XL | 3+ | 7+ | 15 |

### Completed Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `featureId` | string | yes | Feature ID from product-definition.json |
| `featureName` | string | yes | Human-readable feature name |
| `specPath` | string | yes | Relative path to existing spec file |
| `specStatus` | enum | yes | `"todo"` \| `"active"` \| `"shipped"` |

### Dependency Graph Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `edges` | array | yes | Directed dependency edges |
| `warnings` | string[] | yes | Human-readable warnings about dependency chains |

### Dependency Edge Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `from` | string | yes | Feature ID that depends on another |
| `to` | string | yes | Feature ID that is depended upon |

### Summary Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `totalFeatures` | number | yes | Total features in product-definition.json |
| `specced` | number | yes | Features that already have specs |
| `unspecced` | number | yes | Features still needing specs |
| `phases` | number | yes | Number of phases in roadmap |
| `effortBreakdown` | object | yes | Count of features per effort size |
| `estimatedTotalDays` | number | yes | Sum of effortDays for all unspecced features |

**Recompute summary every time the file is written.**

## Graph Relationships

The ID-based cross-references enable these traversals:

| From | To | Via |
|------|----|-----|
| Phase | Goal Gate | `phases[].gateId` |
| Item | Feature (definition) | `phases[].items[].featureId` |
| Item | Mechanisms (engineering) | `phases[].items[].mechanisms` |
| Item | Pain Points (discovery) | `phases[].items[].addressesNeeds` |
| Item | Dependencies | `phases[].items[].dependencies` |
| Item | Dependents | `phases[].items[].dependedUponBy` |
| Dependency Graph | Features | `dependencyGraph.edges[].from/to` |

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
