# Project Status Output Schema

This document defines the JSON schema for `.shipkit/status.json` produced by the `shipkit-project-status` skill.

---

## Full JSON Schema

```json
{
  "$schema": "shipkit-artifact",
  "type": "project-status",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DD",
  "source": "shipkit-project-status",

  "summary": {
    "healthScore": 72,
    "totalSpecs": 2,
    "totalPlans": 0,
    "totalTasks": 5,
    "gapsFound": 4,
    "coreFilesPresent": 3,
    "coreFilesTotal": 4
  },

  "coreContext": [
    {
      "file": "stack.json",
      "exists": true,
      "freshness": "aging",
      "lastModified": "2025-12-26",
      "sizeBytes": 1240,
      "notes": "package.json modified more recently"
    },
    {
      "file": "architecture.json",
      "exists": true,
      "freshness": "fresh",
      "lastModified": "2025-12-27",
      "sizeBytes": 3420,
      "itemCount": 12,
      "notes": "12 decisions logged"
    },
    {
      "file": "implementations.json",
      "exists": true,
      "freshness": "fresh",
      "lastModified": "2025-12-28",
      "sizeBytes": 5100,
      "itemCount": 23,
      "notes": "23 components documented"
    },
    {
      "file": "progress.json",
      "exists": true,
      "freshness": "fresh",
      "lastModified": "2025-12-28",
      "sizeBytes": 2800,
      "itemCount": 8,
      "notes": "8 sessions logged"
    }
  ],

  "workflow": {
    "specs": {
      "activeCount": 2,
      "files": ["specs/active/recipe-sharing.json", "specs/active/user-profile.json"]
    },
    "plans": {
      "count": 0,
      "files": []
    },
    "tasks": {
      "activeCount": 5,
      "completedCount": 0
    }
  },

  "gaps": [
    {
      "id": "stale-stack",
      "severity": "warning",
      "category": "freshness",
      "description": "stack.json is stale (2 days old, package.json modified since)",
      "suggestedAction": "/shipkit-project-context"
    },
    {
      "id": "undocumented-auth",
      "severity": "warning",
      "category": "undocumented",
      "description": "src/lib/auth.ts (347 lines) not documented in implementations.json",
      "file": "src/lib/auth.ts",
      "lineCount": 347,
      "suggestedAction": "Document component manually"
    },
    {
      "id": "undocumented-datatable",
      "severity": "warning",
      "category": "undocumented",
      "description": "src/components/DataTable.tsx (215 lines) not documented in implementations.json",
      "file": "src/components/DataTable.tsx",
      "lineCount": 215,
      "suggestedAction": "Document component manually"
    },
    {
      "id": "specs-without-plans",
      "severity": "critical",
      "category": "workflow-gap",
      "description": "2 active specs have no corresponding plans",
      "suggestedAction": "/shipkit-plan"
    }
  ],

  "skillUsage": {
    "totalInvocations": 47,
    "mostUsed": [
      { "skill": "shipkit-spec", "count": 12 },
      { "skill": "shipkit-plan", "count": 8 },
      { "skill": "shipkit-project-context", "count": 6 }
    ],
    "neverUsed": ["shipkit-ux-audit", "shipkit-data-contracts"],
    "stale": [
      { "skill": "shipkit-verify", "daysSinceUse": 21, "count": 2 },
      { "skill": "shipkit-preflight", "daysSinceUse": 18, "count": 1 }
    ]
  },

  "recommendations": [
    {
      "priority": 1,
      "action": "/shipkit-project-context",
      "reason": "Stack context is stale — package.json modified more recently"
    },
    {
      "priority": 2,
      "action": "/shipkit-plan",
      "reason": "Active specs (recipe-sharing, user-profile) have no plans"
    },
    {
      "priority": 3,
      "action": "Document components manually",
      "reason": "2 large files (>200 LOC) are undocumented"
    }
  ]
}
```

---

## Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `$schema` | string | yes | Always `"shipkit-artifact"` -- identifies as Shipkit-managed file |
| `type` | string | yes | Always `"project-status"` -- artifact type for routing/rendering |
| `version` | string | yes | Schema version for forward compatibility |
| `lastUpdated` | string | yes | ISO date of last status check |
| `source` | string | yes | Always `"shipkit-project-status"` |
| `summary` | object | yes | Aggregated counts for dashboard rendering |
| `summary.healthScore` | number | yes | 0-100 score based on freshness, gaps, and workflow state |
| `summary.totalSpecs` | number | yes | Count of active specs |
| `summary.totalPlans` | number | yes | Count of plans |
| `summary.totalTasks` | number | yes | Count of active user tasks |
| `summary.gapsFound` | number | yes | Total number of detected gaps |
| `summary.coreFilesPresent` | number | yes | How many of 4 core context files exist |
| `summary.coreFilesTotal` | number | yes | Always 4 (stack, architecture, implementations, progress) |
| `coreContext` | array | yes | Status of each core `.shipkit/` context file |
| `coreContext[].file` | string | yes | Filename (relative to `.shipkit/`) |
| `coreContext[].exists` | boolean | yes | Whether the file exists |
| `coreContext[].freshness` | enum | yes | `"fresh"` (<24h) \| `"aging"` (1-7d) \| `"stale"` (>7d) \| `"missing"` |
| `coreContext[].lastModified` | string | no | ISO date of last modification (omit if missing) |
| `coreContext[].sizeBytes` | number | no | File size in bytes (omit if missing) |
| `coreContext[].itemCount` | number | no | Count of documented items (decisions, components, sessions) |
| `coreContext[].notes` | string | no | Human-readable summary of file state |
| `workflow` | object | yes | Status of specs, plans, and tasks |
| `workflow.specs.activeCount` | number | yes | Number of active spec files |
| `workflow.specs.files` | string[] | yes | Paths to active spec files |
| `workflow.plans.count` | number | yes | Number of plan files |
| `workflow.plans.files` | string[] | yes | Paths to plan files |
| `workflow.tasks.activeCount` | number | yes | Number of active (unchecked) tasks |
| `workflow.tasks.completedCount` | number | yes | Number of completed tasks |
| `gaps` | array | yes | Detected documentation and workflow gaps |
| `gaps[].id` | string | yes | Slug identifier for the gap |
| `gaps[].severity` | enum | yes | `"critical"` \| `"warning"` \| `"info"` |
| `gaps[].category` | enum | yes | `"freshness"` \| `"undocumented"` \| `"workflow-gap"` \| `"missing"` |
| `gaps[].description` | string | yes | Human-readable description of the gap |
| `gaps[].file` | string | no | File path associated with gap (if applicable) |
| `gaps[].lineCount` | number | no | Line count for undocumented file gaps |
| `gaps[].suggestedAction` | string | yes | Skill or action to resolve the gap |
| `skillUsage` | object | no | Skill usage analytics (omit if no tracking data) |
| `skillUsage.totalInvocations` | number | yes | Total tracked invocations |
| `skillUsage.mostUsed` | array | yes | Top skills by usage count |
| `skillUsage.neverUsed` | string[] | yes | Skills with 0 invocations |
| `skillUsage.stale` | array | yes | Skills not used in 14+ days |
| `recommendations` | array | yes | Prioritized next actions |
| `recommendations[].priority` | number | yes | Priority rank (1 = highest) |
| `recommendations[].action` | string | yes | Skill command or action to take |
| `recommendations[].reason` | string | yes | Why this action is recommended |

---

## Summary Object

The `summary` field MUST be kept in sync with the scan results. It exists so the dashboard can render overview cards without traversing the full structure. Recompute it every time the file is written.

---

## Health Score Calculation

Compute `healthScore` (0-100) based on weighted factors:

| Factor | Weight | Scoring |
|--------|--------|---------|
| Core files present | 30 | 0 pts per missing, 7.5 pts per existing |
| Core files freshness | 25 | 0 pts stale, 12.5 pts aging, 25 pts all fresh |
| Workflow completeness | 25 | Specs+plans+tasks scored proportionally |
| Documentation coverage | 20 | Based on ratio of documented vs undocumented large files |

---

## Shipkit Artifact Convention

This skill follows the **Shipkit JSON artifact convention** -- a standard structure for all `.shipkit/*.json` files that enables mission control visualization.

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

- `$schema` -- Always `"shipkit-artifact"`. Lets the reporter hook identify files to ship to mission control.
- `type` -- The artifact type (`"project-status"`, `"goals"`, `"spec"`, etc.). Dashboard uses this for rendering.
- `version` -- Schema version. Bump when fields change.
- `lastUpdated` -- When this file was last written.
- `source` -- Which skill wrote this file.
- `summary` -- Aggregated data for dashboard cards. Structure varies by type.
