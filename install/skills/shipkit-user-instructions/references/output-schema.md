# User Tasks Schema Reference

This document defines the JSON schema for `.shipkit/user-tasks.json`.

## JSON Schema

```json
{
  "$schema": "shipkit-artifact",
  "type": "user-tasks",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DD",
  "source": "shipkit-user-instructions",

  "summary": {
    "total": 0,
    "byStatus": {
      "active": 0,
      "in-progress": 0,
      "completed": 0,
      "deferred": 0
    },
    "byPriority": {
      "high": 0,
      "medium": 0,
      "low": 0
    }
  },

  "tasks": [
    {
      "id": "task-slug",
      "title": "Human-readable task name",
      "description": "Why this task is necessary",
      "status": "active | in-progress | completed | deferred",
      "priority": "high | medium | low",
      "steps": ["Specific action 1", "Specific action 2"],
      "verification": ["How to verify task is complete"],
      "relatedFeature": "Feature name or null",
      "triggeredBy": "skill-name or manual",
      "createdAt": "YYYY-MM-DD",
      "completedAt": "YYYY-MM-DD or null"
    }
  ]
}
```

## Field Reference

### Envelope Fields (Shipkit Artifact Convention)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `$schema` | string | yes | Always `"shipkit-artifact"` -- identifies this as a Shipkit-managed file |
| `type` | string | yes | Always `"user-tasks"` -- artifact type for routing/rendering |
| `version` | string | yes | Schema version for forward compatibility |
| `lastUpdated` | string | yes | ISO date of last modification |
| `source` | string | yes | Always `"shipkit-user-instructions"` |

### Summary Object

The `summary` field MUST be kept in sync with the `tasks` array. It exists so the dashboard can render overview cards without iterating the full array. Recompute it every time the file is written.

| Field | Type | Description |
|-------|------|-------------|
| `summary.total` | number | Total number of tasks |
| `summary.byStatus.active` | number | Tasks awaiting action |
| `summary.byStatus.in-progress` | number | Tasks currently being worked on |
| `summary.byStatus.completed` | number | Finished tasks |
| `summary.byStatus.deferred` | number | Tasks postponed for later |
| `summary.byPriority.high` | number | Blocking or urgent tasks |
| `summary.byPriority.medium` | number | Important but not blocking |
| `summary.byPriority.low` | number | Nice-to-have tasks |

### Tasks Array

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Slug identifier (kebab-case, e.g., `"configure-webhook"`) |
| `title` | string | yes | Display name for the task |
| `description` | string | yes | Why this task is necessary (1-2 sentences) |
| `status` | enum | yes | `"active"`, `"in-progress"`, `"completed"`, or `"deferred"` |
| `priority` | enum | yes | `"high"`, `"medium"`, or `"low"` |
| `steps` | string[] | yes | Specific actions the user must take |
| `verification` | string[] | yes | How to confirm the task is done |
| `relatedFeature` | string | no | Feature name or `null` |
| `triggeredBy` | string | no | Skill that created this task or `"manual"` |
| `createdAt` | string | yes | ISO date when task was created |
| `completedAt` | string | no | ISO date when task was completed, or `null` |

## Shipkit Artifact Convention

This file follows the **Shipkit Artifact Convention** -- a standard structure for all `.shipkit/*.json` files that enables dashboard visualization.

Every JSON artifact MUST include these top-level fields:

- `$schema` -- Always `"shipkit-artifact"`. Identifies Shipkit artifact files.
- `type` -- The artifact type (`"user-tasks"`, `"goals"`, `"spec"`, etc.). Dashboard uses this for rendering.
- `version` -- Schema version. Bump when fields change.
- `lastUpdated` -- When this file was last written.
- `source` -- Which skill wrote this file.
- `summary` -- Aggregated data for dashboard cards. Structure varies by type.

Skills that haven't migrated to JSON yet continue writing markdown. The reporter hook ships both: JSON artifacts get structured dashboard rendering, markdown files fall back to metadata-only (exists, date, size).
