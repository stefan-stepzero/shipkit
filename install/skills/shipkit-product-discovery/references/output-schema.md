# Product Discovery Output Schema

This document defines the JSON schema for `.shipkit/product-discovery.json` produced by the `shipkit-product-discovery` skill.

---

## Full JSON Schema

```json
{
  "$schema": "shipkit-artifact",
  "type": "product-discovery",
  "version": "1.0",
  "lastUpdated": "2025-01-15T10:00:00Z",
  "source": "shipkit-product-discovery",
  "summary": {
    "totalPersonas": 3,
    "totalJourneys": 4,
    "totalPainPoints": 8,
    "totalOpportunities": 2,
    "primaryPersona": "Solo Developer",
    "topPainPoint": "Context loss between sessions"
  },
  "personas": [
    {
      "id": "persona-1",
      "name": "Solo Developer",
      "role": "Full-stack developer",
      "primaryIntent": "Ship side projects to production quickly",
      "goals": ["Ship MVP fast", "Avoid context loss"],
      "frustrations": ["Starting over each session", "Forgetting decisions"],
      "techComfort": "high",
      "context": "Works alone on side projects, evenings and weekends",
      "isPrimary": true
    }
  ],
  "painPoints": [
    {
      "id": "pain-1",
      "description": "Context loss between sessions",
      "severity": "critical",
      "affectedPersonas": ["persona-1"],
      "currentWorkaround": "Manual notes in README",
      "frequency": "every session"
    }
  ],
  "journeys": [
    {
      "id": "journey-1",
      "name": "New Project Setup",
      "persona": "persona-1",
      "steps": [
        {
          "id": "step-1",
          "action": "Initialize project",
          "emotion": "excited",
          "painPoints": [],
          "touchpoints": ["CLI"]
        },
        {
          "id": "step-2",
          "action": "Configure stack",
          "emotion": "neutral",
          "painPoints": ["pain-1"],
          "touchpoints": ["CLI", ".shipkit/"]
        }
      ]
    }
  ],
  "opportunities": [
    {
      "id": "opp-1",
      "description": "Auto-detect project context on session start",
      "addressesPainPoints": ["pain-1"],
      "impactedPersonas": ["persona-1"],
      "effort": "medium",
      "impact": "high"
    }
  ]
}
```

---

## Field Reference

### Envelope Fields (Required)

| Field | Type | Description |
|-------|------|-------------|
| `$schema` | string | Always `"shipkit-artifact"` |
| `type` | string | `"product-discovery"` for this skill |
| `version` | string | Schema version, currently `"1.0"` |
| `lastUpdated` | string | ISO 8601 timestamp |
| `source` | string | `"shipkit-product-discovery"` |
| `summary` | object | Aggregated counts for dashboard cards |

### Summary Object

| Field | Type | Description |
|-------|------|-------------|
| `totalPersonas` | number | Count of personas |
| `totalJourneys` | number | Count of journeys |
| `totalPainPoints` | number | Count of pain points |
| `totalOpportunities` | number | Count of opportunities |
| `primaryPersona` | string | Name of the primary persona |
| `topPainPoint` | string | Most critical pain point description |

### Personas Array

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Stable ID: `persona-{n}` |
| `name` | string | Persona name or archetype |
| `role` | string | Role or job title |
| `primaryIntent` | string | Core motivation for using the product (e.g., "Create worksheets efficiently"). For multi-user apps, each persona should have a distinct intent. |
| `goals` | string[] | What they want to achieve |
| `frustrations` | string[] | Current pain points (human-readable) |
| `techComfort` | string | `"high"`, `"medium"`, or `"low"` |
| `context` | string | When/where they use the product |
| `isPrimary` | boolean | `true` for the primary persona |

### Pain Points Array

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Stable ID: `pain-{n}` |
| `description` | string | Pain point description |
| `severity` | string | `"critical"`, `"high"`, `"medium"`, or `"low"` |
| `affectedPersonas` | string[] | Array of persona IDs |
| `currentWorkaround` | string | How users cope today |
| `frequency` | string | How often this occurs |

### Journeys Array

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Stable ID: `journey-{n}` |
| `name` | string | Journey name |
| `persona` | string | Persona ID this journey belongs to |
| `steps` | object[] | Ordered steps in the journey |

### Journey Steps

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Stable ID: `step-{n}` (unique within journey) |
| `action` | string | What the user does |
| `emotion` | string | `"excited"`, `"neutral"`, `"frustrated"`, `"confused"`, `"satisfied"` |
| `painPoints` | string[] | Array of pain point IDs encountered at this step |
| `touchpoints` | string[] | Interfaces/channels involved |

### Opportunities Array

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Stable ID: `opp-{n}` |
| `description` | string | Opportunity description |
| `addressesPainPoints` | string[] | Array of pain point IDs this addresses |
| `impactedPersonas` | string[] | Array of persona IDs who benefit |
| `effort` | string | `"low"`, `"medium"`, or `"high"` |
| `impact` | string | `"low"`, `"medium"`, or `"high"` |

---

## Graph Relationships

The ID-based cross-references enable these graph traversals:

- **Persona -> Pain Points**: `painPoints[].affectedPersonas` references `personas[].id`
- **Journey -> Persona**: `journeys[].persona` references `personas[].id`
- **Journey Step -> Pain Points**: `journeys[].steps[].painPoints` references `painPoints[].id`
- **Opportunity -> Pain Points**: `opportunities[].addressesPainPoints` references `painPoints[].id`
- **Opportunity -> Personas**: `opportunities[].impactedPersonas` references `personas[].id`

---

## Shipkit Artifact Convention

This skill follows the **Shipkit JSON artifact convention** - a standard structure for all `.shipkit/*.json` files that enables dashboard visualization.

**Every JSON artifact MUST include these top-level fields:**

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

- `$schema` - Always `"shipkit-artifact"`. Identifies Shipkit artifact files.
- `type` - The artifact type (`"product-discovery"`, `"preflight"`, `"spec"`, etc.). Dashboard uses this for rendering.
- `version` - Schema version. Bump when fields change.
- `lastUpdated` - When this file was last written.
- `source` - Which skill wrote this file.
- `summary` - Aggregated data for dashboard cards. Structure varies by type.
