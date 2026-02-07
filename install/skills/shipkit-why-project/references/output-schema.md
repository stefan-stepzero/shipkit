# Why Project Schema Reference

This document defines the JSON schema for `.shipkit/why.json`.

## JSON Schema

```json
{
  "$schema": "shipkit-artifact",
  "type": "project-why",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DD",
  "createdAt": "YYYY-MM-DD",
  "source": "shipkit-why-project",
  "vision": "string",
  "problem": "string",
  "targetUsers": "string",
  "currentState": "string",
  "successCriteria": [
    "string"
  ],
  "constraints": [
    "string"
  ],
  "nonGoals": [
    "string"
  ],
  "timeline": {
    "target": "string | null",
    "milestones": [
      {
        "name": "string",
        "target": "string",
        "status": "planned | in-progress | completed"
      }
    ]
  },
  "approach": "string"
}
```

## Field Reference

### Envelope Fields (Shipkit Artifact Convention)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `$schema` | string | yes | Always `"shipkit-artifact"` |
| `type` | string | yes | Always `"project-why"` |
| `version` | string | yes | Schema version (`"1.0"`) |
| `lastUpdated` | string | yes | ISO date of last update |
| `createdAt` | string | yes | ISO date of initial creation (preserved on updates) |
| `source` | string | yes | Always `"shipkit-why-project"` |

### Core Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `vision` | string | yes | Where we need to be - the success state, what "done" looks like |
| `problem` | string | yes | Why this exists - the problem we're solving, value provided |
| `targetUsers` | string | yes | Who this is for - target users, audience, stakeholders |
| `currentState` | string | yes | Where we are now - POC/MVP/Beta/Production/Starting |
| `approach` | string | yes | How we're getting there - methodology, strategy |

### Strategic Boundaries

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `successCriteria` | array | yes | Measurable outcomes that define success (can be empty) |
| `constraints` | array | yes | Limitations, must-haves, non-negotiables (can be empty) |
| `nonGoals` | array | yes | What we're explicitly NOT building (can be empty) |

### Timeline Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `timeline.target` | string | no | Overall target date or timeframe, or `null` |
| `timeline.milestones` | array | no | Key milestones with targets (can be empty) |
| `timeline.milestones[].name` | string | yes | Milestone name |
| `timeline.milestones[].target` | string | yes | Target date or timeframe |
| `timeline.milestones[].status` | enum | yes | `"planned"`, `"in-progress"`, or `"completed"` |

## Shipkit Artifact Convention

This file follows the **Shipkit Artifact Convention** -- a standard envelope for structured data files produced by Shipkit skills. The convention enables:

- **Programmatic consumption** by other skills (e.g., `shipkit-spec`, `shipkit-verify`)
- **Session auto-loading** for strategic context
- **Dashboard rendering** in mission control
- **Consistency checks** across project artifacts

Required envelope fields for all Shipkit artifacts:
- `$schema`: Always `"shipkit-artifact"`
- `type`: Artifact type identifier
- `version`: Schema version for forward compatibility
- `lastUpdated`: ISO date of last generation
- `source`: Skill that produced the artifact

## Usage Notes

### Creating vs Updating

When updating an existing `why.json`:
- Preserve the `createdAt` date from the original
- Update `lastUpdated` to current date
- Prompt user if they want to view current values as defaults

### Array Fields

All array fields (`successCriteria`, `constraints`, `nonGoals`) can be empty arrays `[]` if user skips those questions. This is valid - not all projects need explicit constraints or non-goals early on.

### Timeline

The timeline is optional. If user doesn't specify dates or milestones:
- Set `timeline.target` to `null`
- Set `timeline.milestones` to empty array `[]`
