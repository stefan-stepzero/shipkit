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

| Field | Type | Required | Scope | Description |
|-------|------|----------|-------|-------------|
| `vision` | string | yes | **Enduring** | The full-scale success state — what "done" looks like when the product is mature. Do NOT narrow this to current stage (e.g., "AI maths tutor for all primary students" not "AI tutor for AU Year 1-2 only"). |
| `problem` | string | yes | **Enduring** | The complete problem worth solving — the customer pain at full scale. Not the subset tackled in the current stage. |
| `targetUsers` | string | yes | **Enduring** | The broad audience the product ultimately serves. Stage-specific market narrowing (e.g., "AU only for POC") belongs in `stage.json` constraints. |
| `currentState` | string | yes | **Snapshot** | Where we are now — POC/MVP/Beta/Production/Starting. Brief maturity assessment only. |
| `approach` | string | yes | **Enduring** | High-level methodology and strategy. Not stage-specific tactics or current sprint focus. |

### Strategic Boundaries

| Field | Type | Required | Scope | Description |
|-------|------|----------|-------|-------------|
| `successCriteria` | array | yes | **Enduring** | Measurable outcomes at the vision level (can be empty). Stage-specific metrics belong in `stage.json` criteria. |
| `constraints` | array | yes | **Enduring** | Permanent project-level limitations (e.g., "must run on mobile", "no paid APIs"). Stage-specific constraints (e.g., "AU curriculum only", "Year 1-2 for POC") belong in `stage.json` `constraints.scope`. |
| `nonGoals` | array | yes | **Enduring** | What we're explicitly NOT building — ever, not just "not yet". Things deferred to later stages belong in `stage.json` `stageImplications.skip`. |

### Scope Boundary Rule

**why.json = enduring vision. stage.json = current scope.**

If a detail would change when the project moves from POC → MVP → Scale, it belongs in `stage.json`, not here. The why.json should read the same whether the project is in POC or at scale — only `currentState` changes.

## Shipkit Artifact Convention

This file follows the **Shipkit Artifact Convention** -- a standard envelope for structured data files produced by Shipkit skills. The convention enables:

- **Programmatic consumption** by other skills (e.g., `shipkit-spec`, `shipkit-review-shipping`)
- **Session auto-loading** for strategic context
- **Dashboard rendering**
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

### Timeline and Milestones

**Note:** Timeline and milestones are NOT captured in `why.json`. For trackable objectives with priorities and status, use `/shipkit-product-goals` which creates `goals.json`. This separation keeps `why.json` focused on strategic context while `goals.json` handles actionable tracking.
