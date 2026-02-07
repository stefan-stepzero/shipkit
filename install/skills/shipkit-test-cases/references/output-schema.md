# Test Coverage Schema Reference

This document defines the JSON schema for `.shipkit/test-cases/coverage.json`.

## JSON Schema

```json
{
  "$schema": "shipkit-artifact",
  "type": "test-coverage",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DD",
  "source": "shipkit-test-cases",
  "summary": {
    "totalCases": 0,
    "filesWithCases": 0,
    "totalSourceFiles": 0,
    "coverageScore": 0,
    "byPriority": {
      "core": 0,
      "edge": 0,
      "regression": 0
    },
    "byStatus": {
      "verified": 0,
      "pending": 0,
      "stale": 0,
      "orphaned": 0
    }
  },
  "cases": [
    {
      "id": "string",
      "name": "string",
      "priority": "core | edge | regression",
      "status": "verified | pending | stale | orphaned",
      "sourceFile": "string",
      "linkedSpec": "string | null",
      "codeModified": "YYYY-MM-DD",
      "lastVerified": "YYYY-MM-DD | null"
    }
  ],
  "gaps": [
    {
      "file": "string",
      "reason": "string",
      "priority": "core | edge | regression"
    }
  ],
  "staleCases": [
    {
      "caseId": "string",
      "sourceFile": "string",
      "codeModified": "YYYY-MM-DD",
      "lastVerified": "YYYY-MM-DD"
    }
  ],
  "orphanedCases": [
    {
      "caseId": "string",
      "originalFile": "string"
    }
  ]
}
```

## Field Reference

### Envelope Fields (Shipkit Artifact Convention)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `$schema` | string | yes | Always `"shipkit-artifact"` |
| `type` | string | yes | Always `"test-coverage"` |
| `version` | string | yes | Schema version (`"1.0"`) |
| `lastUpdated` | string | yes | ISO date of generation |
| `source` | string | yes | Always `"shipkit-test-cases"` |

### Summary Object

| Field | Type | Description |
|-------|------|-------------|
| `summary.totalCases` | number | Total test cases across all files |
| `summary.filesWithCases` | number | Source files with at least one test case |
| `summary.totalSourceFiles` | number | Total source files analyzed |
| `summary.coverageScore` | number | Percentage (0-100) of files with cases |
| `summary.byPriority.core` | number | Count of core priority cases |
| `summary.byPriority.edge` | number | Count of edge priority cases |
| `summary.byPriority.regression` | number | Count of regression cases |
| `summary.byStatus.verified` | number | Cases verified against current code |
| `summary.byStatus.pending` | number | Cases not yet verified |
| `summary.byStatus.stale` | number | Cases where code changed since verification |
| `summary.byStatus.orphaned` | number | Cases whose source file was deleted |

### Cases Array

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique case identifier (e.g., `"AUTH-01"`) |
| `name` | string | yes | Human-readable test name |
| `priority` | enum | yes | `"core"`, `"edge"`, or `"regression"` |
| `status` | enum | yes | `"verified"`, `"pending"`, `"stale"`, or `"orphaned"` |
| `sourceFile` | string | yes | Path to validated source file |
| `linkedSpec` | string | no | Path to related spec, or `null` |
| `codeModified` | string | yes | ISO date of last source file modification |
| `lastVerified` | string | no | ISO date of last verification, or `null` if pending |

### Gaps Array

| Field | Type | Description |
|-------|------|-------------|
| `file` | string | Path to source file without test cases |
| `reason` | string | Why this is a gap (e.g., `"no coverage"`) |
| `priority` | enum | Inferred priority: `"core"`, `"edge"`, or `"regression"` |

### Stale Cases Array

| Field | Type | Description |
|-------|------|-------------|
| `caseId` | string | ID of the stale test case |
| `sourceFile` | string | Path to the modified source file |
| `codeModified` | string | ISO date when code was modified |
| `lastVerified` | string | ISO date of last verification |

### Orphaned Cases Array

| Field | Type | Description |
|-------|------|-------------|
| `caseId` | string | ID of the orphaned test case |
| `originalFile` | string | Path to the deleted source file |

## Shipkit Artifact Convention

This file follows the **Shipkit Artifact Convention** -- a standard envelope for structured data files produced by Shipkit skills. The convention enables:

- **Programmatic consumption** by other skills (e.g., `shipkit-verify`, `shipkit-preflight`)
- **Dashboard rendering** in mission control
- **Threshold checks** (e.g., "coverageScore >= 80")

Required envelope fields for all Shipkit artifacts:
- `$schema`: Always `"shipkit-artifact"`
- `type`: Artifact type identifier
- `version`: Schema version for forward compatibility
- `lastUpdated`: ISO date of last generation
- `source`: Skill that produced the artifact
