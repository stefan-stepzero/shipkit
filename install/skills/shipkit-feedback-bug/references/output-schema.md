# Bug Spec JSON Schema

This document defines the JSON schema for bug specifications output by `/shipkit-feedback-bug`.

---

## Overview

Bug specs are stored as JSON files following the Shipkit artifact convention. They share the same base structure as feature specs (from `/shipkit-spec`) with additional bug-specific fields. This enables:
- Dashboard visualization in mission control
- Structured queries across specs and bugs
- Programmatic access by other skills
- Consistent format for all specification documentation

---

## File Location

**Active bugs**: `.shipkit/specs/active/bug-{name}.json`
**Resolved bugs**: `.shipkit/specs/implemented/bug-{name}.json`

**Naming**: Use kebab-case for bug names, prefixed with `bug-` (e.g., `bug-save-button-race-condition.json`, `bug-login-timeout.json`)

---

## Complete JSON Schema

```json
{
  "$schema": "shipkit-artifact",
  "type": "bug-spec",
  "version": "1.0",
  "lastUpdated": "2025-01-15T10:00:00Z",
  "source": "shipkit-feedback-bug",

  "summary": {
    "name": "Save Button Race Condition",
    "status": "active",
    "severity": "high",
    "feedbackSource": "user-testing",
    "rootCauseType": "race-condition",
    "affectedComponentCount": 3,
    "hasBlastRadius": true
  },

  "metadata": {
    "id": "bug-save-button-race-condition",
    "created": "2025-01-15",
    "updated": "2025-01-15",
    "author": "shipkit-feedback-bug",
    "feedbackDate": "2025-01-14"
  },

  "originalFeedback": {
    "quote": "When I click save really fast, sometimes my changes don't save and I lose everything",
    "source": "user-testing",
    "reporter": "Beta Tester #3"
  },

  "problem": {
    "statement": "Rapid clicks on save button can cause data loss due to race condition between async operations",
    "expectedBehavior": "All changes are saved regardless of click timing",
    "actualBehavior": "Sometimes changes are lost when save is clicked quickly after previous save"
  },

  "reproduction": {
    "confirmed": "2025-01-15",
    "steps": [
      "Open any document for editing",
      "Make a change to the content",
      "Click save button",
      "Immediately make another change",
      "Click save button again within 500ms",
      "Observe that second change may be lost"
    ],
    "environment": {
      "browser": "Chrome 120+",
      "os": "Any",
      "prerequisites": ["Logged in", "Document with edit permissions"]
    },
    "minimumRepro": "Two rapid saves within 500ms window"
  },

  "investigation": {
    "codePath": {
      "entry": "SaveButton.onClick()",
      "failurePoint": "useSave hook state reset",
      "relevantFiles": [
        "src/components/SaveButton.tsx:45",
        "src/hooks/useSave.ts:23-67",
        "src/api/documents.ts:89"
      ]
    },
    "rootCause": {
      "fiveWhys": [
        {
          "level": 1,
          "symptom": "Second save loses data",
          "because": "First save's cleanup runs during second save"
        },
        {
          "level": 2,
          "symptom": "First save's cleanup runs during second save",
          "because": "useEffect cleanup triggers on re-render"
        },
        {
          "level": 3,
          "symptom": "Component re-renders during save",
          "because": "Loading state change causes parent re-render"
        },
        {
          "level": 4,
          "symptom": "Loading state change causes parent re-render",
          "because": "No request deduplication or debouncing"
        }
      ],
      "conclusion": "Race condition: useEffect cleanup resets state before async response arrives when rapid saves trigger re-renders",
      "type": "race-condition"
    },
    "blastRadius": {
      "description": "Same pattern exists in other async hooks",
      "affectedComponents": [
        {
          "file": "src/hooks/useDelete.ts",
          "risk": "high",
          "samePattern": true
        },
        {
          "file": "src/hooks/useUpdate.ts",
          "risk": "high",
          "samePattern": true
        },
        {
          "file": "src/hooks/useCreate.ts",
          "risk": "medium",
          "samePattern": true
        }
      ]
    }
  },

  "fix": {
    "approach": "Implement request deduplication with AbortController and add debouncing to save action",
    "acceptanceCriteria": [
      "Rapid clicks are debounced (300ms)",
      "Pending requests are cancelled when new request starts",
      "No data loss under any click timing",
      "Loading indicator shows during save",
      "Same fix applied to useDelete and useUpdate hooks"
    ]
  },

  "learnings": {
    "patternToAvoid": "Using useEffect cleanup for async state management without request cancellation",
    "patternToUse": "AbortController for request cancellation + debouncing for rapid user actions",
    "architectureMemoryWorthy": true
  },

  "resolution": {
    "status": "open",
    "fixedIn": null,
    "verifiedBy": null,
    "verifiedDate": null
  },

  "references": {
    "stack": ".shipkit/stack.json",
    "codebaseIndex": ".shipkit/codebase-index.json",
    "relatedSpecs": [],
    "relatedBugs": []
  },

  "nextSteps": [
    "Fix the useSave hook with debouncing and AbortController",
    "Apply same pattern to useDelete and useUpdate (blast radius)",
    "/shipkit-verify after implementation",
    "/shipkit-architecture-memory to document async hook pattern"
  ]
}
```

---

## Field Reference

### Top-Level Envelope (Required for all Shipkit artifacts)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `$schema` | string | yes | Always `"shipkit-artifact"` |
| `type` | string | yes | Always `"bug-spec"` for this artifact |
| `version` | string | yes | Schema version, currently `"1.0"` |
| `lastUpdated` | string | yes | ISO 8601 timestamp of last modification |
| `source` | string | yes | Always `"shipkit-feedback-bug"` |

### Summary (Dashboard display)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Human-readable bug name |
| `status` | enum | yes | `"active"` or `"resolved"` |
| `severity` | enum | yes | `"critical"`, `"high"`, `"medium"`, `"low"` |
| `feedbackSource` | enum | yes | `"user-testing"`, `"beta"`, `"bug-report"`, `"general"` |
| `rootCauseType` | enum | yes | `"logic-error"`, `"race-condition"`, `"missing-validation"`, `"state-management"`, `"integration"`, `"environment"` |
| `affectedComponentCount` | number | yes | Count of components in blast radius |
| `hasBlastRadius` | boolean | yes | Whether bug affects multiple components |

### Metadata

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique identifier (format: `bug-{name}`) |
| `created` | string | yes | Date created (YYYY-MM-DD) |
| `updated` | string | yes | Date last updated (YYYY-MM-DD) |
| `author` | string | yes | Who/what created this spec |
| `feedbackDate` | string | yes | Date original feedback was received |

### Original Feedback

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `quote` | string | yes | Original user quote/report |
| `source` | enum | yes | Same as `summary.feedbackSource` |
| `reporter` | string | no | Who reported it (anonymized if needed) |

### Problem

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `statement` | string | yes | Clear problem statement |
| `expectedBehavior` | string | yes | What should happen |
| `actualBehavior` | string | yes | What happens instead |

### Reproduction

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `confirmed` | string | yes | Date bug was confirmed (YYYY-MM-DD) |
| `steps` | string[] | yes | Ordered reproduction steps |
| `environment` | object | no | Environment details |
| `environment.browser` | string | no | Browser requirements |
| `environment.os` | string | no | OS requirements |
| `environment.prerequisites` | string[] | no | Required preconditions |
| `minimumRepro` | string | yes | Simplest case that triggers bug |

### Investigation

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `codePath` | object | yes | Code path analysis |
| `codePath.entry` | string | yes | Entry point |
| `codePath.failurePoint` | string | yes | Where it goes wrong |
| `codePath.relevantFiles` | string[] | yes | File:line references |
| `rootCause` | object | yes | Root cause analysis |
| `rootCause.fiveWhys` | object[] | yes | 5 Whys analysis |
| `rootCause.fiveWhys[].level` | number | yes | Why level (1-5) |
| `rootCause.fiveWhys[].symptom` | string | yes | What happened |
| `rootCause.fiveWhys[].because` | string | yes | Why it happened |
| `rootCause.conclusion` | string | yes | Final root cause statement |
| `rootCause.type` | enum | yes | Same as `summary.rootCauseType` |
| `blastRadius` | object | yes | Blast radius assessment |
| `blastRadius.description` | string | yes | Summary of impact |
| `blastRadius.affectedComponents` | object[] | yes | List of affected components |
| `blastRadius.affectedComponents[].file` | string | yes | File path |
| `blastRadius.affectedComponents[].risk` | enum | yes | `"high"`, `"medium"`, `"low"` |
| `blastRadius.affectedComponents[].samePattern` | boolean | yes | Uses same problematic pattern |

### Fix

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `approach` | string | yes | How to fix it |
| `acceptanceCriteria` | string[] | yes | Specific criteria for fix |

### Learnings

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `patternToAvoid` | string | yes | What caused this bug |
| `patternToUse` | string | yes | Better approach |
| `architectureMemoryWorthy` | boolean | yes | Should log to `/shipkit-architecture-memory` |

### Resolution

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | enum | yes | `"open"`, `"in-progress"`, `"resolved"`, `"wont-fix"` |
| `fixedIn` | string | no | Version/commit when fixed |
| `verifiedBy` | string | no | How it was verified |
| `verifiedDate` | string | no | Date verified (YYYY-MM-DD) |

### References

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `stack` | string | yes | Path to stack.json |
| `codebaseIndex` | string | yes | Path to codebase-index.json |
| `relatedSpecs` | string[] | no | Paths to related feature specs |
| `relatedBugs` | string[] | no | Paths to related bug specs |

### Next Steps

Array of strings suggesting what to do after bug spec is complete.

---

## Severity Definitions

| Severity | Definition | Examples |
|----------|------------|----------|
| `critical` | Blocks core functionality, data loss, security issue | Data corruption, auth bypass, app crash |
| `high` | Major feature broken, difficult workaround | Can't save, can't load, broken workflow |
| `medium` | Feature impaired, workaround exists | Slow performance, UI glitch, minor data issue |
| `low` | Minor issue, cosmetic, edge case | Typo, alignment, rare edge case |

---

## Root Cause Types

| Type | Description |
|------|-------------|
| `logic-error` | Wrong condition, off-by-one, incorrect calculation |
| `race-condition` | Timing issue, async problems, state synchronization |
| `missing-validation` | Null check, type check, bounds check missing |
| `state-management` | Stale state, wrong scope, improper updates |
| `integration` | API contract, external service, third-party issue |
| `environment` | Browser-specific, config issue, deployment problem |

---

## Status Lifecycle

| Status | Location | Description |
|--------|----------|-------------|
| `open` | `.shipkit/specs/active/` | Bug confirmed, awaiting fix |
| `in-progress` | `.shipkit/specs/active/` | Fix in development |
| `resolved` | `.shipkit/specs/implemented/` | Bug fixed and verified |
| `wont-fix` | `.shipkit/specs/implemented/` | Decision not to fix |

When a bug is resolved:
1. Update `status` to `"resolved"` or `"wont-fix"`
2. Fill in `resolution` fields
3. Move file from `active/` to `implemented/`

---

## Validation Rules

1. **Unique IDs**: Each bug spec must have a unique `id`
2. **At Least 2 Whys**: The `fiveWhys` array must have at least 2 entries
3. **At Least 1 Acceptance Criterion**: The `acceptanceCriteria` array must have at least one entry
4. **At Least 2 Reproduction Steps**: The `steps` array must have at least 2 entries
5. **Summary Sync**: Summary counts must match actual array lengths

---

## Compatibility Notes

- **Version 1.0**: Initial schema release
- Shares base envelope structure with feature specs for consistency
- Future versions will maintain backward compatibility where possible
