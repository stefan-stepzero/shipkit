# UX Decisions Schema Reference

This document defines the JSON schema for `.shipkit/ux-decisions.json`.

## JSON Schema

```json
{
  "$schema": "shipkit-artifact",
  "type": "ux-decisions",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DD",
  "source": "shipkit-ux-audit",
  "summary": {
    "totalDecisions": 0,
    "totalGaps": 0,
    "byCategory": {
      "form": 0,
      "modal": 0,
      "toggle": 0,
      "list": 0,
      "button": 0,
      "navigation": 0,
      "feedback": 0,
      "other": 0
    },
    "byPersona": {
      "general": 0,
      "adhd-friendly": 0,
      "elderly": 0,
      "mobile-first": 0,
      "low-bandwidth": 0,
      "accessibility-first": 0
    }
  },
  "decisions": [
    {
      "id": "string",
      "component": "string",
      "category": "form | modal | toggle | list | button | navigation | feedback | other",
      "pattern": "string",
      "decision": "string",
      "rationale": "string",
      "accessibility": ["string"],
      "existingMatch": "string | null",
      "persona": "general | adhd-friendly | elderly | mobile-first | low-bandwidth | accessibility-first",
      "checklist": ["string"],
      "date": "YYYY-MM-DD"
    }
  ],
  "gaps": [
    {
      "id": "string",
      "component": "string",
      "missingPatterns": ["string"],
      "priority": "high | medium | low",
      "notes": "string | null",
      "identifiedDate": "YYYY-MM-DD"
    }
  ]
}
```

## Field Reference

### Envelope Fields (Shipkit Artifact Convention)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `$schema` | string | yes | Always `"shipkit-artifact"` |
| `type` | string | yes | Always `"ux-decisions"` |
| `version` | string | yes | Schema version (`"1.0"`) |
| `lastUpdated` | string | yes | ISO date of last update |
| `source` | string | yes | Always `"shipkit-ux-audit"` |

### Summary Object

| Field | Type | Description |
|-------|------|-------------|
| `summary.totalDecisions` | number | Total UX decisions logged |
| `summary.totalGaps` | number | Total identified UX gaps |
| `summary.byCategory.*` | number | Count of decisions by component category |
| `summary.byPersona.*` | number | Count of decisions by target persona |

### Decisions Array

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique decision ID (e.g., `"UX-001"`, `"UX-002"`) |
| `component` | string | yes | Component name (e.g., `"LoginForm"`, `"ConfirmModal"`) |
| `category` | enum | yes | Component type category |
| `pattern` | string | yes | Specific UX pattern applied (e.g., `"inline validation"`) |
| `decision` | string | yes | Brief description of what was decided |
| `rationale` | string | yes | Why this pattern was chosen (1-2 sentences) |
| `accessibility` | array | yes | Key WCAG/a11y requirements applied |
| `existingMatch` | string | no | Reference to similar component, or `null` |
| `persona` | enum | yes | Target user persona for this decision |
| `checklist` | array | yes | Implementation requirements |
| `date` | string | yes | ISO date when decision was made |

### Gaps Array

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique gap ID (e.g., `"GAP-001"`) |
| `component` | string | yes | Component or area with missing patterns |
| `missingPatterns` | array | yes | List of patterns that should be added |
| `priority` | enum | yes | `"high"`, `"medium"`, or `"low"` |
| `notes` | string | no | Additional context about the gap |
| `identifiedDate` | string | yes | ISO date when gap was identified |

## Category Values

| Category | Description |
|----------|-------------|
| `form` | Forms, inputs, validation, submission |
| `modal` | Modals, dialogs, popups |
| `toggle` | Switches, toggles, checkboxes |
| `list` | Lists, tables, grids, collections |
| `button` | Buttons, CTAs, clickable actions |
| `navigation` | Navigation, menus, breadcrumbs |
| `feedback` | Toasts, alerts, notifications, loading |
| `other` | Components not fitting other categories |

## Persona Values

| Persona | Description |
|---------|-------------|
| `general` | No specific persona adaptation |
| `adhd-friendly` | Minimize options, auto-save, clear feedback |
| `elderly` | Large targets, high contrast, confirmations |
| `mobile-first` | Touch-friendly, thumb zones, responsive |
| `low-bandwidth` | Minimize media, offline support |
| `accessibility-first` | Beyond WCAG AA, excellent screen reader support |

## Shipkit Artifact Convention

This file follows the **Shipkit Artifact Convention** -- a standard envelope for structured data files produced by Shipkit skills. The convention enables:

- **Programmatic consumption** by other skills (e.g., `shipkit-verify`, `shipkit-preflight`)
- **Pattern consistency checking** across components
- **Dashboard rendering** in mission control
- **Historical tracking** of UX decisions

Required envelope fields for all Shipkit artifacts:
- `$schema`: Always `"shipkit-artifact"`
- `type`: Artifact type identifier
- `version`: Schema version for forward compatibility
- `lastUpdated`: ISO date of last generation
- `source`: Skill that produced the artifact

## Usage Notes

### Adding Decisions

When adding a new UX decision:
1. Generate next sequential ID (e.g., if last is `UX-005`, next is `UX-006`)
2. Append to `decisions` array
3. Update `summary` counts
4. Update `lastUpdated` to current date

### Adding Gaps

When identifying a UX gap:
1. Generate next sequential gap ID (e.g., `GAP-001`)
2. Append to `gaps` array
3. Update `summary.totalGaps`
4. Update `lastUpdated`

### Resolving Gaps

When a gap is addressed:
1. Remove from `gaps` array
2. Add corresponding decision to `decisions` array
3. Update summary counts

### ID Generation

- Decision IDs: `UX-001`, `UX-002`, etc. (zero-padded 3 digits)
- Gap IDs: `GAP-001`, `GAP-002`, etc. (zero-padded 3 digits)
