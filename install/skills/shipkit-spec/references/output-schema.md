# Spec JSON Schema

This document defines the JSON schema for feature specifications output by `/shipkit-spec`.

---

## Overview

Feature specs are stored as JSON files following the Shipkit artifact convention. This enables:
- Dashboard visualization
- Structured queries across specs
- Programmatic access by other skills
- Consistent format for all feature documentation

---

## File Location

```
.shipkit/specs/
├── todo/        # Defined, ready to start
├── active/      # Being implemented
├── parked/      # On hold (blocked, deprioritized)
└── shipped/     # Delivered to users
```

**Naming**: Use kebab-case for feature names (e.g., `recipe-sharing.json`, `user-authentication.json`)

---

## Complete JSON Schema

```json
{
  "$schema": "shipkit-artifact",
  "type": "spec",
  "version": "1.0",
  "lastUpdated": "2025-01-15T10:00:00Z",
  "source": "shipkit-spec",

  "summary": {
    "name": "Recipe Sharing",
    "status": "active",
    "featureType": "user-facing-ui",
    "complexity": "medium",
    "scenarioCount": 3,
    "acceptanceCriteriaCount": 8,
    "edgeCasesApplied": ["loading", "error", "empty", "permission", "boundary", "consistency"]
  },

  "metadata": {
    "id": "spec-recipe-sharing",
    "created": "2025-01-15",
    "updated": "2025-01-15",
    "author": "shipkit-spec"
  },

  "problem": {
    "statement": "Users cannot share their recipes with others without requiring recipients to create an account",
    "userStory": {
      "as": "recipe author",
      "iWant": "share my recipes publicly via a unique link",
      "soThat": "others can view them without signing up"
    }
  },

  "scenarios": [
    {
      "id": "scenario-1",
      "name": "Generate shareable link",
      "type": "happy-path",
      "given": ["User is logged in", "User has created a recipe"],
      "when": "User clicks 'Share' button on their recipe",
      "then": [
        "System generates a unique shareable URL",
        "URL is copied to clipboard",
        "Toast notification confirms 'Link copied'",
        "Share modal displays the link with copy button"
      ]
    }
  ],

  "edgeCases": {
    "loading": [
      "Show spinner while generating share link",
      "Disable share button during link generation",
      "Handle timeout if link generation takes > 5 seconds"
    ],
    "error": [
      "Show error toast if link generation fails",
      "Provide retry option on network failure",
      "Log error details for debugging"
    ],
    "empty": [
      "Disable share for recipes with no content",
      "Show 'Add content to share' message for empty recipes"
    ],
    "permission": [
      "Only recipe owner can generate share links",
      "Public links are read-only (no editing)",
      "Owner can revoke share links"
    ],
    "boundary": [
      "Maximum 100 share links per recipe",
      "Share links expire after 30 days of inactivity",
      "Rate limit: 10 link generations per minute"
    ],
    "consistency": [
      "Update shared view when recipe is edited",
      "Show 'Recipe deleted' message if original is removed",
      "Handle concurrent share link generation"
    ]
  },

  "acceptanceCriteria": {
    "mustHave": [
      "Generate unique, unguessable share URL",
      "Copy link to clipboard with one click",
      "Allow viewing recipe without authentication",
      "Display recipe in read-only format"
    ],
    "shouldHave": [
      "Show share count/analytics",
      "Allow customizing link expiration",
      "Social media sharing buttons"
    ],
    "wontHave": [
      "Collaborative editing via share link",
      "Comments on shared recipes (this iteration)",
      "PDF export from share view"
    ]
  },

  "outOfScope": [
    "Recipe collections/folders sharing",
    "User profile sharing",
    "Embedding recipes on external sites"
  ],

  "dependencies": [
    "Authentication system must be in place",
    "Recipe CRUD operations must be complete",
    "URL shortener service (optional)"
  ],

  "technical": {
    "databaseChanges": [
      "Add share_links table (id, recipe_id, token, created_at, expires_at, view_count)",
      "Add index on share_links.token for fast lookups"
    ],
    "apiEndpoints": [
      { "method": "POST", "path": "/api/recipes/{id}/share", "purpose": "Generate share link" },
      { "method": "GET", "path": "/api/share/{token}", "purpose": "Get shared recipe" },
      { "method": "DELETE", "path": "/api/recipes/{id}/share/{linkId}", "purpose": "Revoke share link" }
    ],
    "notes": [
      "Use crypto.randomUUID() for token generation",
      "Consider CDN caching for popular shared recipes",
      "Implement rate limiting at API gateway level"
    ]
  },

  "functionalSurface": {
    "applications": [
      { "name": "web-ui", "kind": "frontend", "verdict": "COVERED", "evidence": "exists in architecture-map.json" },
      { "name": "api-backend", "kind": "service", "verdict": "COVERED", "evidence": "exists in architecture-map.json" }
    ],
    "datastores": [
      { "name": "share_links", "kind": "table", "verdict": "COVERED", "evidence": "technical.databaseChanges" }
    ],
    "contracts": [
      { "name": "GET /api/share/{token}", "kind": "rest-endpoint", "verdict": "COVERED", "evidence": "technical.apiEndpoints; surfaced by no-gaps gate (frontend-implies-backend)" }
    ],
    "integrations": [
      { "name": "Supabase Auth", "kind": "auth-provider", "verdict": "COVERED", "evidence": "dependencies" }
    ]
  },

  "gapReport": {
    "status": "clear",
    "dimensions": { "applications": "covered", "datastores": "covered", "contracts": "covered", "integrations": "covered" },
    "flagged": [],
    "sharedContracts": [
      { "field": "grade_band", "usedBy": ["student-view", "coach-dashboard"], "owner": "grade_band_v (view)", "status": "owned" }
    ],
    "unbackedSurfaces": [],
    "identityContract": { "key": "auth.uid()", "mapsTo": "profiles.id", "declaredBeforeSchema": true },
    "architectureMapUsed": true,
    "confidence": "high"
  },

  "deferred": [
    { "dimension": "datastores", "element": "share analytics store", "reason": "out of scope this iteration (acceptanceCriteria.wontHave)" }
  ],

  "testStrategy": {
    "callFlows": [
      "User -> ShareButton -> API -> Database -> Response -> Clipboard",
      "Visitor -> ShareURL -> API -> Database -> RecipeView",
      "Owner -> RevokeLink -> API -> Database -> LinkInvalidated"
    ],
    "coverage": [
      {
        "layer": "Business logic",
        "testType": "Unit",
        "whatToTest": "Token generation, expiration calculation, permission checks"
      },
      {
        "layer": "API endpoints",
        "testType": "Integration",
        "whatToTest": "Share link CRUD, auth checks, rate limiting"
      },
      {
        "layer": "UI components",
        "testType": "Component",
        "whatToTest": "Share modal, copy button, loading states"
      },
      {
        "layer": "Critical paths",
        "testType": "E2E",
        "whatToTest": "Full share flow: generate link -> visit link -> see recipe"
      }
    ],
    "mocking": {
      "mock": ["Clipboard API", "Analytics service"],
      "testDoubles": ["Database (in-memory)"],
      "real": ["Token generation", "URL validation"]
    },
    "keyTestCases": [
      {
        "scenario": "Generate shareable link",
        "testType": "Integration",
        "testName": "should generate unique token when owner shares recipe"
      },
      {
        "scenario": "View shared recipe",
        "testType": "Integration",
        "testName": "should return recipe data for valid share token"
      },
      {
        "scenario": "Permission denied",
        "testType": "Unit",
        "testName": "should reject share request from non-owner"
      },
      {
        "scenario": "Expired link",
        "testType": "Integration",
        "testName": "should return 404 for expired share token"
      }
    ]
  },

  "references": {
    "stack": ".shipkit/stack.json",
    "schema": ".shipkit/schema.json",
    "architecture": ".shipkit/architecture.json",
    "relatedSpecs": []
  },

  "nextSteps": [
    "/shipkit-plan to create implementation plan",
    "/shipkit-engineering-definition to log any architectural decisions"
  ]
}
```

---

## Field Reference

### Top-Level Envelope (Required for all Shipkit artifacts)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `$schema` | string | yes | Always `"shipkit-artifact"` |
| `type` | string | yes | Always `"spec"` for this artifact |
| `version` | string | yes | Schema version, currently `"1.0"` |
| `lastUpdated` | string | yes | ISO 8601 timestamp of last modification |
| `source` | string | yes | Always `"shipkit-spec"` |

### Summary (Dashboard display)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Human-readable feature name |
| `status` | enum | yes | `"todo"`, `"active"`, `"parked"`, or `"shipped"` |
| `featureType` | enum | yes | `"user-facing-ui"`, `"api-backend"`, `"integration"`, `"infrastructure"` |
| `complexity` | enum | yes | `"simple"`, `"medium"`, `"complex"` |
| `scenarioCount` | number | yes | Count of scenarios defined |
| `acceptanceCriteriaCount` | number | yes | Total count across all priority levels |
| `edgeCasesApplied` | string[] | yes | Which of the 6 categories were applied |

### Metadata

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique identifier (format: `spec-{feature-name}`) |
| `created` | string | yes | Date created (YYYY-MM-DD) |
| `updated` | string | yes | Date last updated (YYYY-MM-DD) |
| `author` | string | yes | Who/what created this spec |

### Problem

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `statement` | string | yes | Clear problem statement (1-2 sentences) |
| `userStory.as` | string | yes | User type/persona |
| `userStory.iWant` | string | yes | What the user wants to do |
| `userStory.soThat` | string | yes | The benefit/outcome |

### Scenarios (Array)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique identifier (format: `scenario-N`) |
| `name` | string | yes | Short descriptive name |
| `type` | enum | yes | `"happy-path"`, `"alternative"`, `"reversal"`, `"error"` |
| `given` | string[] | yes | Initial conditions (array of statements) |
| `when` | string | yes | User action or trigger |
| `then` | string[] | yes | Expected outcomes (array of statements) |

### Edge Cases

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `loading` | string[] | yes | Loading state considerations |
| `error` | string[] | yes | Error handling considerations |
| `empty` | string[] | yes | Empty/missing state considerations |
| `permission` | string[] | yes | Permission/auth considerations |
| `boundary` | string[] | yes | Boundary condition considerations |
| `consistency` | string[] | yes | Data consistency considerations |

### Acceptance Criteria

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `mustHave` | string[] | yes | Critical requirements (MVP) |
| `shouldHave` | string[] | yes | Important but not blocking |
| `wontHave` | string[] | yes | Explicitly excluded (this iteration) |

### Out of Scope

Array of strings explicitly listing what is NOT included in this feature.

### Dependencies

Array of strings listing what must be in place before this feature.

### Technical

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `databaseChanges` | string[] | no | Tables, columns, indexes to add |
| `apiEndpoints` | object[] | no | New/modified endpoints |
| `apiEndpoints[].method` | string | yes | HTTP method |
| `apiEndpoints[].path` | string | yes | Endpoint path |
| `apiEndpoints[].purpose` | string | yes | What the endpoint does |
| `notes` | string[] | no | Implementation hints and considerations |

### Functional Surface (No-Gaps Gate)

Produced by the no-gaps completeness gate (see `no-gaps-checklist.md`). Enumerates what the feature **implies** across four dimensions so nothing is silently missing. Each dimension is an array of element objects.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `applications` | object[] | yes | Runnable surfaces implied (UI, service, worker, CLI, mobile) |
| `datastores` | object[] | yes | Persistent stores read/written (tables, collections, buckets, caches) |
| `contracts` | object[] | yes | APIs / function signatures / events connecting surfaces (the frontend-implies-backend dimension) |
| `integrations` | object[] | yes | External services / providers / infra depended on |
| `*[].name` | string | yes | The element (e.g. `GET /api/share/{token}`, `share_links`) |
| `*[].kind` | string | yes | Sub-type (e.g. `rest-endpoint`, `table`, `auth-provider`) |
| `*[].verdict` | enum | yes | `COVERED`, `FLAGGED`, or `EXPLICITLY-DEFERRED` |
| `*[].evidence` | string | yes | Where it's covered (spec field / architecture-map) or why flagged |

A dimension array may be empty only if the feature genuinely implies nothing in it (state why in `gapReport`, don't leave it unconsidered).

### Gap Report (No-Gaps Gate)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | enum | yes | `"clear"` (FLAGGED = 0, no `recomputed` shared contracts, no `unbackedSurfaces`, identity contract satisfied for auth apps) or `"flagged"` — **must be `clear` to save** |
| `dimensions` | object | yes | Per-dimension roll-up: `covered` / `flagged` / `deferred` / `n-a` |
| `flagged` | object[] | yes | Open gaps: `{ dimension, element, impliedBy, proposedResolution }` (empty when clear) |
| `sharedContracts` | object[] | yes | SSOT map for fields/metrics/entities read by ≥2 surfaces: `{ field, usedBy[], owner, status: "owned" \| "recomputed" }`. Any `recomputed` → `status: "flagged"` (a shared field computed independently on multiple surfaces is a violation). Empty if nothing is shared across surfaces. |
| `unbackedSurfaces` | object[] | yes | Surfaces reading a shared field with no declared owner: `{ surface, field, reason }` (empty when clear) |
| `identityContract` | object | conditional | Present when the app has auth: `{ key, mapsTo, declaredBeforeSchema: boolean }`. `declaredBeforeSchema: false` → `status: "flagged"` (identity row-key must be locked before any schema/RLS). Omit for apps with no auth. |
| `architectureMapUsed` | boolean | yes | `false` in greenfield (no `architecture-map.json`) |
| `confidence` | enum | yes | `"high"` or `"reduced"` (greenfield / thin map) |

### Deferred (No-Gaps Gate)

Array of explicitly-deferred implied elements — each `{ dimension, element, reason }`. These are out of scope this iteration **on purpose, with a reason** (typically traced to `acceptanceCriteria.wontHave` or `outOfScope`); they do not block "done".

### Test Strategy

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `callFlows` | string[] | yes | Data/control flows affected |
| `coverage` | object[] | yes | Test coverage by layer |
| `coverage[].layer` | string | yes | Layer name (e.g., "Business logic") |
| `coverage[].testType` | string | yes | Test type (Unit, Integration, Component, E2E) |
| `coverage[].whatToTest` | string | yes | What to test at this layer |
| `mocking` | object | yes | Mocking strategy |
| `mocking.mock` | string[] | yes | What to mock |
| `mocking.testDoubles` | string[] | yes | Test doubles to use |
| `mocking.real` | string[] | yes | What to test with real implementations |
| `keyTestCases` | object[] | yes | Key test cases derived from scenarios |

### References

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `stack` | string | yes | Path to stack.json |
| `schema` | string | yes | Path to schema.json |
| `architecture` | string | yes | Path to architecture.json |
| `relatedSpecs` | string[] | no | Paths to related spec files |

### Next Steps

Array of strings suggesting what to do after spec is complete.

---

## Validation Rules

1. **Unique IDs**: Each scenario must have a unique `id` within the spec
2. **Edge Cases Coverage**: All 6 edge case categories must be present (can be empty arrays)
3. **At Least One Scenario**: The `scenarios` array must have at least one entry
4. **Must Have Criteria**: The `mustHave` array must have at least one entry
5. **Summary Sync**: Summary counts must match actual array lengths
6. **No-Gaps Gate**: `gapReport.status` must be `"clear"` before a spec is saved to `todo/`. This requires: zero FLAGGED elements (every implied application, datastore, contract, and integration is COVERED or EXPLICITLY-DEFERRED with a reason); no `recomputed` entries in `sharedContracts` (every field/metric/entity read by ≥2 surfaces has a single owning SSOT); empty `unbackedSurfaces`; and — if the app has auth — `identityContract.declaredBeforeSchema: true` (see `no-gaps-checklist.md`).

---

## Status Lifecycle

| Status | Location | Description |
|--------|----------|-------------|
| `todo` | `.shipkit/specs/todo/` | Spec defined, ready to start when capacity available |
| `active` | `.shipkit/specs/active/` | Currently being implemented |
| `parked` | `.shipkit/specs/parked/` | On hold (blocked, deprioritized, waiting) |
| `shipped` | `.shipkit/specs/shipped/` | Delivered to users |

### Transitions

```
[spec created] → todo/ → active/ → shipped/
                   ↓        ↓
                parked/ ←──┘
                   ↓
                 (back to todo/ when unblocked)
```

| Transition | When | Action |
|------------|------|--------|
| `todo` → `active` | Work starts | Move file, update status |
| `active` → `shipped` | Feature delivered | Move file, update status, add completion metadata |
| `active` → `parked` | Blocked or deprioritized | Move file, update status, add reason in metadata |
| `parked` → `todo` | Unblocked, ready again | Move file, update status |

---

## Compatibility Notes

- **Version 1.0**: Initial schema release
- Future versions will maintain backward compatibility where possible
- Breaking changes will increment major version
