---
name: shipkit-prototype-to-spec
description: "Use when extracting learnings from a prototype into a spec. Triggers: 'prototype done', 'extract patterns', 'document prototype', 'capture UI patterns'."
---

# shipkit-prototype-to-spec - Prototype Learning Extractor

**Purpose**: Extract validated UI/UX decisions from prototypes into formal JSON specifications

**What it does**: Reads prototype iterations.md and index.html, identifies key learnings, and updates the `uiux` field in existing JSON spec or creates new spec

---

## When to Invoke

**User triggers:**
- "Extract prototype to spec"
- "Update spec from prototype"
- "Capture prototype learnings"
- "Document prototype decisions"

**Suggested after:**
- `/shipkit-prototyping` - Prototype iteration complete
- User says "done prototyping" or "ready to document"

**Use cases:**
- Preserve validated UI patterns before implementation
- Document "what worked" and "what didn't" from prototyping
- Update spec with concrete interaction patterns
- Capture user feedback before deleting prototype

---

## Prerequisites

**Required:**
- `.shipkit-mockups/[name]/iterations.md` - Prototype change log must exist
- `.shipkit-mockups/[name]/index.html` - Prototype file

**Recommended:**
- `.shipkit/specs/active/[feature].json` - Spec to update (will create if missing)

**This skill can create new spec** if none exists, but prefer updating existing spec.

---

## Process

### Step 1: Identify Prototype to Extract

**Ask user:**
```
Which prototype should I extract learnings from?

Options:
1. Specify prototype name (e.g., "recipe-share-v1")
2. List available prototypes

→ [user choice]
```

**If user chooses "list":**
```bash
ls -d .shipkit-mockups/*/ 2>/dev/null | sed 's|.shipkit-mockups/||' | sed 's|/||'
```

**Store:** `prototype_name`

**Verify prototype exists:**
```bash
[ -f .shipkit-mockups/${prototype_name}/iterations.md ] || ERROR
```

---

### Step 2: Read Prototype Artifacts

**Read these files:**
1. `.shipkit-mockups/[name]/iterations.md` - Change log with user feedback
2. `.shipkit-mockups/[name]/README.md` - What prototype explored
3. `.shipkit-mockups/[name]/index.html` - Final prototype state

**Extract key information:**

**From iterations.md:**
- User feedback on each iteration
- What changes were made
- User responses ("better", "perfect", "confusing")
- Final "Key Learnings" section (if exists)

**From README.md:**
- Core interaction being tested
- What UI/UX question prototype answered

**From index.html:**
- Component structure (React components used)
- State management patterns
- Tailwind classes (design system patterns)
- Interaction handlers (onClick, etc.)

---

### Step 3: Determine Target Spec

**Ask user:**
```
Which spec should I update with these learnings?

Options:
1. Update existing spec: [list specs from .shipkit/specs/active/*.json]
2. Create new spec for this feature
3. Cancel (keep learnings in prototype only)

→ [user choice]
```

**If "create new":**
- Ask for feature name
- Create new spec at `.shipkit/specs/active/[feature].json`
- Use basic spec template with `uiux` field

**If "update existing":**
- Read existing JSON spec
- Prepare to add/update `uiux` field

---

### Step 4: Generate UI/UX Object

**Structure the learnings as a JSON object:**

```json
{
  "uiux": {
    "extractedFrom": ".shipkit-mockups/[prototype-name]/",
    "extractedAt": "2025-01-15T14:30:00Z",

    "patterns": [
      {
        "name": "Share button placement",
        "description": "Top-right corner with icon + text",
        "validated": true,
        "feedback": "Users looked there first"
      }
    ],

    "components": [
      {
        "name": "ShareButton",
        "structure": "button with icon + label",
        "tailwind": "absolute top-4 right-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2",
        "state": ["isSharing: boolean"]
      },
      {
        "name": "Toast",
        "structure": "fixed bottom notification",
        "tailwind": "fixed bottom-4 left-1/2 -translate-x-1/2 bg-gray-900 text-white px-4 py-2 rounded-lg",
        "state": ["isVisible: boolean", "message: string"]
      }
    ],

    "interactions": [
      {
        "action": "Click share button",
        "result": "Copy link to clipboard, show toast",
        "duration": "Toast visible for 2s"
      }
    ],

    "accessibility": [
      "Share button has aria-label with recipe name",
      "Toast announced via aria-live region",
      "Focus returns to share button after toast dismisses"
    ],

    "validated": {
      "whatWorked": [
        "Share button top-right because users looked there first",
        "Icon + text more discoverable than icon-only",
        "Toast at bottom-center, 2s duration felt right"
      ],
      "whatFailed": [
        "Tabs felt cramped on mobile - switched to dropdown",
        "Icon-only button wasn't obvious enough"
      ],
      "userFeedback": [
        "\"This feels right\" - on final placement",
        "\"I see it immediately\" - on button visibility"
      ]
    },

    "implementationNotes": {
      "ensure": [
        "Share button always visible (sticky positioning)",
        "Toast disappears automatically after 2s",
        "Copy to clipboard with fallback for older browsers"
      ],
      "avoid": [
        "Icon-only buttons for primary actions",
        "Tabs on mobile viewports"
      ]
    }
  }
}
```

---

### Step 5: Update JSON Spec

**Read existing spec:**
```javascript
const spec = JSON.parse(readFile('.shipkit/specs/active/[feature].json'));
```

**Add or update `uiux` field:**
```javascript
spec.uiux = generatedUiuxObject;
spec.lastUpdated = new Date().toISOString();
```

**Write updated spec:**
```javascript
writeFile('.shipkit/specs/active/[feature].json', JSON.stringify(spec, null, 2));
```

**If creating new spec, use this minimal template:**
```json
{
  "$schema": "shipkit-artifact",
  "type": "spec",
  "version": "1.0",
  "lastUpdated": "2025-01-15T14:30:00Z",
  "source": "shipkit-prototype-to-spec",

  "summary": {
    "name": "[Feature Name]",
    "status": "draft",
    "featureType": "user-facing-ui"
  },

  "metadata": {
    "id": "spec-[feature-name]",
    "created": "2025-01-15",
    "updated": "2025-01-15",
    "author": "shipkit-prototype-to-spec"
  },

  "problem": {
    "statement": "[To be defined]",
    "userStory": {
      "as": "[user type]",
      "iWant": "[capability]",
      "soThat": "[benefit]"
    }
  },

  "uiux": {
    // Generated UI/UX object from Step 4
  },

  "nextSteps": [
    "/shipkit-spec to complete full specification",
    "/shipkit-plan to create implementation plan"
  ]
}
```

---

### Step 6: Confirm and Archive

**Show user:**
```
Updated spec: .shipkit/specs/active/[feature].json

Added/updated uiux field with:
- 3 validated patterns
- 2 component definitions
- 4 interaction patterns
- 3 accessibility considerations
- Implementation notes (ensure/avoid)

Prototype learnings preserved in JSON format!

Next steps:
1. Review updated spec
2. Archive or delete prototype:
   - Keep: .shipkit-mockups/[name]/ (for reference during implementation)
   - Delete: rm -rf .shipkit-mockups/[name]/ (after implementation complete)

3. Ready to plan implementation:
   Run: /shipkit-plan [feature]

Delete prototype now? (y/n)
```

**If yes:** Delete `.shipkit-mockups/[name]/` folder
**If no:** Leave prototype as reference

---

## Completion Checklist

Copy and track:
- [ ] Reviewed prototype in `.shipkit-mockups/`
- [ ] Extracted key patterns and learnings
- [ ] Updated JSON spec with `uiux` field

---

## When This Skill Integrates with Others

### Before This Skill

**shipkit-prototyping** - Creates prototypes to extract from
- **When**: Prototype iteration complete, user validated core interaction
- **Why**: Prototyping generates the iterations.md and learnings to extract
- **Trigger**: User says "done prototyping" or "extract to spec"

**shipkit-spec** - May have created initial spec (optional)
- **When**: JSON spec exists before prototyping started
- **Why**: Prototyping refines initial spec with validated UI patterns
- **Trigger**: Spec exists and needs `uiux` field added

### After This Skill

**shipkit-plan** - Creates implementation plan from updated spec
- **When**: Spec now includes validated UI/UX patterns in `uiux` field
- **Why**: Plan can reference specific patterns from prototype
- **Trigger**: User ready to plan implementation

**Implementation** (natural capability)
- **When**: Implementation starts after planning
- **Why**: Spec's `uiux` field guides implementation decisions
- **Trigger**: Development phase begins

### Special Relationships

**Bridges prototyping and implementation** - Prevents lost knowledge
- **When**: Between exploration (prototyping) and execution (implementation)
- **Why**: Prototypes are disposable, but learnings must be preserved
- **Trigger**: Natural workflow step after validation

**Can run multiple times** - Extract from variants
- **When**: Multiple prototype variants tested (v1, v2, v3)
- **Why**: Each variant may have unique learnings to capture
- **Trigger**: User created multiple prototypes for same feature

---

## Context Files This Skill Reads

**Prototype artifacts (required):**
- `.shipkit-mockups/[name]/iterations.md` - Change log with feedback
- `.shipkit-mockups/[name]/README.md` - What prototype explored
- `.shipkit-mockups/[name]/index.html` - Final prototype implementation

**Spec files (optional):**
- `.shipkit/specs/active/[feature].json` - Existing spec to update

---

## Context Files This Skill Writes

**Updates (MERGE):**
- `.shipkit/specs/active/[feature].json` - Adds/updates `uiux` field
  - **Write Strategy**: MERGE (reads existing JSON, adds `uiux` field, writes back)
  - **Behavior**: If spec exists, adds `uiux` field. If not, creates new spec with `uiux` field.
  - **Why**: Preserve existing spec content while adding prototype learnings as structured JSON

**May delete (if user confirms):**
- `.shipkit-mockups/[name]/` - Prototype folder after extraction

---

<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Has important context been saved to `.shipkit/`?
2. **Prerequisites** - Does the next action need a spec or plan first?
3. **Session length** - Long session? Consider `/shipkit-work-memory` for continuity.

**Natural capabilities** (no skill needed): Implementation, debugging, testing, refactoring, code documentation.

**Suggest skill when:** User needs to make decisions, create persistence, or check project status.
<!-- /SECTION:after-completion -->

<!-- SECTION:success-criteria -->
## Success Criteria

Extraction successful when:
- [ ] Read all prototype artifacts (iterations.md, README.md, index.html)
- [ ] Identified validated patterns (what worked)
- [ ] Identified rejected approaches (what didn't work)
- [ ] Generated `uiux` JSON object with structured learnings
- [ ] Updated or created JSON spec with `uiux` field
- [ ] User knows next step (plan or implement)

**Not required:**
- Prototype doesn't need to be deleted (user choice)
- Spec doesn't need to be "complete" (`uiux` is one field among many)

**Goal:** Preserve knowledge before prototype is deleted.
<!-- /SECTION:success-criteria -->
---

## Tips for Effective Extraction

**Focus on actionable patterns:**
- Don't just capture "button is blue"
- Capture "Share button top-right because users looked there first"
- Include the "why" from user feedback

**Preserve concrete examples:**
- Copy actual Tailwind classes (design system)
- Include React state patterns (implementation guidance)
- Show component structure (not full code, just key patterns)

**Structure for implementation:**
- `ensure` list: binary checks for validated patterns
- `avoid` list: patterns that failed
- `components`: ready-to-implement structures

**Quote user feedback:**
- Direct quotes are more valuable than summaries
- "This feels right" vs "User approved design"
- Shows real validation, not assumptions

---

## UI/UX Object Field Reference

| Field | Type | Purpose |
|-------|------|---------|
| `extractedFrom` | string | Path to source prototype |
| `extractedAt` | string (ISO) | When extraction occurred |
| `patterns` | array | Named UI patterns with validation status |
| `components` | array | Component definitions with Tailwind + state |
| `interactions` | array | User interaction flows |
| `accessibility` | array | A11y considerations discovered |
| `validated.whatWorked` | array | Patterns confirmed by user |
| `validated.whatFailed` | array | Rejected approaches |
| `validated.userFeedback` | array | Direct user quotes |
| `implementationNotes.ensure` | array | Must-have implementation details |
| `implementationNotes.avoid` | array | Anti-patterns to avoid |

---

**Remember:** Prototypes are disposable, but learnings are permanent. Extract before deleting.
