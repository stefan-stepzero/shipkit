# Goals Output Schema

This document defines the JSON schema for `.shipkit/goals.json`.

## Full JSON Schema

```json
{
  "$schema": "shipkit-artifact",
  "type": "goals",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DD",
  "source": "shipkit-goals",

  "summary": {
    "total": 5,
    "byPriority": { "p0": 2, "p1": 2, "p2": 1 },
    "byStatus": { "not-started": 2, "in-progress": 2, "achieved": 1, "deferred": 0 }
  },

  "goals": [
    {
      "id": "goal-slug",
      "name": "Human-readable goal name",
      "priority": "p0",
      "status": "in-progress",
      "objective": "What we're trying to achieve",
      "successCriteria": [
        "Measurable criterion 1",
        "Measurable criterion 2"
      ],
      "linkedSpecs": ["specs/active/feature-x.json"],
      "notes": "Optional context"
    }
  ]
}
```

## Field Reference

### Top-Level Fields (Shipkit JSON Artifact Convention)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `$schema` | string | yes | Always `"shipkit-artifact"` - identifies this as a Shipkit-managed file |
| `type` | string | yes | Always `"goals"` - artifact type for routing/rendering |
| `version` | string | yes | Schema version for forward compatibility |
| `lastUpdated` | string | yes | ISO date of last modification |
| `source` | string | yes | Skill that created/updated this file |
| `summary` | object | yes | Aggregated counts for dashboard rendering |
| `goals` | array | yes | The actual goals |

### Goal Object Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Slug identifier (kebab-case) |
| `name` | string | yes | Display name |
| `priority` | enum | yes | `"p0"` \| `"p1"` \| `"p2"` |
| `status` | enum | yes | `"not-started"` \| `"in-progress"` \| `"achieved"` \| `"deferred"` |
| `objective` | string | yes | What we're trying to achieve |
| `successCriteria` | string[] | yes | How we know it's done |
| `linkedSpecs` | string[] | no | Paths to related spec files |
| `notes` | string | no | Additional context |

### Priority Levels

| Priority | Meaning |
|----------|---------|
| `p0` | Must have - critical for launch/success |
| `p1` | Should have - important but not blocking |
| `p2` | Nice to have - future consideration |

### Status Values

| Status | Meaning |
|--------|---------|
| `not-started` | Goal defined but work hasn't begun |
| `in-progress` | Actively working toward this goal |
| `achieved` | Goal completed successfully |
| `deferred` | Postponed to future milestone |

## Summary Object

The `summary` field MUST be kept in sync with the `goals` array. It exists so the dashboard can render overview cards without iterating the full array.

```json
{
  "total": 5,
  "byPriority": { "p0": 2, "p1": 2, "p2": 1 },
  "byStatus": { "not-started": 2, "in-progress": 2, "achieved": 1, "deferred": 0 }
}
```

**Recompute summary every time the file is written.**

## Shipkit Artifact Convention

This skill follows the **Shipkit JSON artifact convention** - a standard structure for all `.shipkit/*.json` files that enables mission control visualization.

**Every JSON artifact MUST include these top-level fields:**

```json
{
  "$schema": "shipkit-artifact",
  "type": "<artifact-type>",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DD",
  "source": "<skill-name>",
  "summary": { ... }
}
```

- `$schema` - Always `"shipkit-artifact"`. Lets the reporter hook identify files to ship to mission control.
- `type` - The artifact type (`"goals"`, `"spec"`, `"plan"`, etc.). Dashboard uses this for rendering.
- `version` - Schema version. Bump when fields change.
- `lastUpdated` - When this file was last written.
- `source` - Which skill wrote this file.
- `summary` - Aggregated data for dashboard cards. Structure varies by type.
