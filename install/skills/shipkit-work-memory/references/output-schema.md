# Work Memory Output Schema

This document defines the JSON schema for `.shipkit/progress.json` produced by the `shipkit-work-memory` skill.

---

## Full JSON Schema

```json
{
  "$schema": "shipkit-artifact",
  "type": "work-memory",
  "version": "1.0",
  "lastUpdated": "2025-01-15T10:00:00Z",
  "source": "shipkit-work-memory",
  "summary": {
    "totalSessions": 12,
    "currentPhase": "implementation",
    "lastSessionDate": "2025-01-15",
    "activeWorkstream": "Authentication flow",
    "blockers": 1,
    "momentum": "high"
  },
  "sessions": [
    {
      "id": "session-12",
      "date": "2025-01-15",
      "duration": "2h",
      "workstream": "Authentication flow",
      "phase": "implementation",
      "accomplished": [
        "Implemented JWT token refresh",
        "Added middleware for protected routes"
      ],
      "filesModified": [
        "src/middleware/auth.ts",
        "src/routes/api/auth.ts"
      ],
      "decisions": [
        {
          "decision": "Use HTTP-only cookies for token storage",
          "rationale": "More secure than localStorage"
        }
      ],
      "gotchas": [
        "Prisma must import from @/lib/prisma"
      ],
      "blockers": [],
      "nextSteps": [
        "Add rate limiting to auth endpoints",
        "Write integration tests for auth flow"
      ],
      "status": "in-progress"
    }
  ],
  "workstreams": [
    {
      "id": "ws-1",
      "name": "Authentication flow",
      "status": "in-progress",
      "startDate": "2025-01-10",
      "sessions": ["session-10", "session-11", "session-12"],
      "completionEstimate": "80%"
    }
  ],
  "resumePoint": {
    "lastSession": "session-12",
    "immediateNextStep": "Add rate limiting to auth endpoints",
    "context": "JWT auth is working, need to harden before deployment",
    "openFiles": ["src/middleware/auth.ts", "src/routes/api/auth.ts"],
    "relatedArtifacts": ["architecture.json", "contracts.json"]
  },
  "timeline": [
    {
      "date": "2025-01-10",
      "event": "Started authentication workstream",
      "type": "milestone"
    },
    {
      "date": "2025-01-12",
      "event": "Decided on JWT over session-based auth",
      "type": "decision"
    },
    {
      "date": "2025-01-15",
      "event": "Core auth flow working end-to-end",
      "type": "milestone"
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
| `type` | string | Always `"work-memory"` |
| `version` | string | Schema version, currently `"1.0"` |
| `lastUpdated` | string | ISO 8601 datetime of last update |
| `source` | string | Always `"shipkit-work-memory"` |

### Summary Object

| Field | Type | Description |
|-------|------|-------------|
| `summary` | object | Aggregated data for dashboard cards |
| `summary.totalSessions` | number | Count of all sessions logged |
| `summary.currentPhase` | string | Current project phase (discovery, planning, implementation, testing, deployment) |
| `summary.lastSessionDate` | string | ISO date of most recent session |
| `summary.activeWorkstream` | string | Name of the currently active workstream |
| `summary.blockers` | number | Count of active blockers across all sessions |
| `summary.momentum` | string | `"high"`, `"medium"`, or `"low"` based on recent session frequency and progress |

### Sessions Array

| Field | Type | Description |
|-------|------|-------------|
| `sessions` | array | Ordered list of session entries (most recent last) |
| `sessions[].id` | string | Unique session ID (`session-N`) |
| `sessions[].date` | string | ISO date of the session |
| `sessions[].duration` | string | Approximate session duration |
| `sessions[].workstream` | string | Which workstream this session contributed to |
| `sessions[].phase` | string | Phase during this session |
| `sessions[].accomplished` | array | List of completed items |
| `sessions[].filesModified` | array | Files changed (from git status) |
| `sessions[].decisions` | array | Objects with `decision` and `rationale` |
| `sessions[].gotchas` | array | Surprises, errors, workarounds discovered |
| `sessions[].blockers` | array | Active blockers preventing progress |
| `sessions[].nextSteps` | array | What to do next |
| `sessions[].status` | string | `"in-progress"`, `"complete"`, or `"blocked"` |

### Workstreams Array

| Field | Type | Description |
|-------|------|-------------|
| `workstreams` | array | Tracked workstreams grouping related sessions |
| `workstreams[].id` | string | Unique workstream ID (`ws-N`) |
| `workstreams[].name` | string | Workstream name |
| `workstreams[].status` | string | `"in-progress"`, `"complete"`, or `"blocked"` |
| `workstreams[].startDate` | string | ISO date when workstream began |
| `workstreams[].sessions` | array | Session IDs belonging to this workstream |
| `workstreams[].completionEstimate` | string | Estimated completion percentage |

### Resume Point Object

| Field | Type | Description |
|-------|------|-------------|
| `resumePoint` | object | Quick-resume context for next session |
| `resumePoint.lastSession` | string | ID of the most recent session |
| `resumePoint.immediateNextStep` | string | Single most important next action |
| `resumePoint.context` | string | Brief context for resuming |
| `resumePoint.openFiles` | array | Files that were being worked on |
| `resumePoint.relatedArtifacts` | array | Other `.shipkit/*.json` files relevant to current work |

### Timeline Array

| Field | Type | Description |
|-------|------|-------------|
| `timeline` | array | Ordered events for timeline visualization |
| `timeline[].date` | string | ISO date of the event |
| `timeline[].event` | string | Description of what happened |
| `timeline[].type` | string | `"milestone"`, `"decision"`, `"blocker"`, or `"session"` |

---

## Archive Schema

Sessions older than 48 hours are archived to `.shipkit/archives/progress-archive-YYYY-MM.json`:

```json
{
  "$schema": "shipkit-artifact",
  "type": "work-memory-archive",
  "version": "1.0",
  "lastUpdated": "<archive date>",
  "source": "shipkit-work-memory",
  "summary": {
    "totalSessions": 3,
    "dateRange": "2025-01-01 to 2025-01-13"
  },
  "sessions": [ "<archived session objects>" ]
}
```

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
- `type` - The artifact type (`"work-memory"`, `"preflight"`, `"spec"`, etc.). Dashboard uses this for rendering.
- `version` - Schema version. Bump when fields change.
- `lastUpdated` - When this file was last written.
- `source` - Which skill wrote this file.
- `summary` - Aggregated data for dashboard cards. Structure varies by type.
