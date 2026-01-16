---
name: lite-prototype-to-spec
description: "Use when extracting learnings from a prototype into a spec. Triggers: 'prototype done', 'extract patterns', 'document prototype', 'capture UI patterns'."
---

# lite-prototype-to-spec - Prototype Learning Extractor

**Purpose**: Extract validated UI/UX decisions from prototypes into formal specifications

**What it does**: Reads prototype iterations.md and index.html, identifies key learnings, and appends UI/UX section to existing spec or creates new spec

---

## When to Invoke

**User triggers:**
- "Extract prototype to spec"
- "Update spec from prototype"
- "Capture prototype learnings"
- "Document prototype decisions"

**Suggested after:**
- `/lite-prototyping` - Prototype iteration complete
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
- `.shipkit-lite/specs/active/[feature].md` - Spec to update (will create if missing)

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
1. Update existing spec: [list specs from .shipkit-lite/specs/active/]
2. Create new spec for this feature
3. Cancel (keep learnings in prototype only)

→ [user choice]
```

**If "create new":**
- Ask for feature name
- Create new spec at `.shipkit-lite/specs/active/[feature].md`
- Use basic spec template

**If "update existing":**
- Read existing spec
- Prepare to append UI/UX section

---

### Step 4: Generate UI/UX Section

**Format learnings as appendable section:**

```markdown
---

## UI/UX Patterns (from prototype: [name])

### What Worked ✓
[Extract from iterations.md "What Worked" or successful changes]

**Validated interactions:**
- [Specific UI patterns that user confirmed]
- [Example: "Share button top-right with icon + text"]
- [Example: "Toast notification bottom-center, 2s duration"]

**User feedback:**
> "[Direct quotes from positive feedback]"

### What Didn't Work ✗
[Extract from iterations.md "What Didn't Work" or rejected approaches]

**Failed approaches:**
- [UI patterns that confused users]
- [Example: "Tabs felt cramped on mobile"]
- [Example: "Icon-only button wasn't obvious"]

**User feedback:**
> "[Direct quotes from negative feedback]"

### Design System Patterns

**Component structure:**
```jsx
[Extract key component pattern from index.html]
// Example: Share button component
<button className="absolute top-4 right-4 bg-blue-600 ...">
  Share
</button>
```

**State management:**
- [List state patterns used, e.g., "Toast visibility: useState boolean"]
- [Example: "Form validation: useState for errors object"]

**Tailwind utilities:**
- Layout: [e.g., "flex items-center justify-between"]
- Spacing: [e.g., "p-4, gap-2"]
- Colors: [e.g., "bg-blue-600, text-white"]
- Interactive: [e.g., "hover:bg-blue-700, transition-colors"]

### Surprises

**Unexpected user behavior:**
- [Things users did that weren't anticipated]

**Wrong assumptions:**
- [Design assumptions proven wrong by testing]

### Implementation Notes

**When implementing, ensure:**
- [ ] [Checklist item from validated pattern]
- [ ] [Example: "Share button always visible (sticky positioning)"]
- [ ] [Example: "Toast disappears automatically after 2s"]

**Avoid:**
- [ ] [Checklist of rejected patterns]

---

**Prototype archived at:** `.shipkit-mockups/[name]/`
**Prototype can be deleted after implementation complete.**
```

---

### Step 5: Append to Spec

**If spec exists:**
```markdown
[Existing spec content]

---

[Generated UI/UX section from Step 4]
```

**If creating new spec:**
```markdown
# [Feature Name] Specification

## Overview
[User provides brief description]

## Functional Requirements
[User provides or defer to later]

---

[Generated UI/UX section from Step 4]
```

**Write to:** `.shipkit-lite/specs/active/[feature].md`

---

### Step 6: Confirm and Archive

**Show user:**
```
✅ Updated spec: .shipkit-lite/specs/active/[feature].md

Added UI/UX section with:
- 3 validated patterns
- 2 rejected approaches
- Component structure examples
- Implementation checklist

Prototype learnings preserved!

Next steps:
1. Review updated spec
2. Archive or delete prototype:
   - Keep: .shipkit-mockups/[name]/ (for reference during implementation)
   - Delete: rm -rf .shipkit-mockups/[name]/ (after implementation complete)

3. Ready to plan implementation:
   Run: /lite-plan [feature]

Delete prototype now? (y/n)
```

**If yes:** Delete `.shipkit-mockups/[name]/` folder
**If no:** Leave prototype as reference

---

## Completion Checklist

Copy and track:
- [ ] Reviewed prototype in `.shipkit-mockups/`
- [ ] Extracted key patterns and learnings
- [ ] Updated or created spec with insights

---

## When This Skill Integrates with Others

### Before This Skill

**lite-prototyping** - Creates prototypes to extract from
- **When**: Prototype iteration complete, user validated core interaction
- **Why**: Prototyping generates the iterations.md and learnings to extract
- **Trigger**: User says "done prototyping" or "extract to spec"

**lite-spec** - May have created initial spec (optional)
- **When**: Spec exists before prototyping started
- **Why**: Prototyping refines initial spec with validated UI patterns
- **Trigger**: Spec exists and needs UI/UX section added

### After This Skill

**lite-plan** - Creates implementation plan from updated spec
- **When**: Spec now includes validated UI/UX patterns
- **Why**: Plan can reference specific patterns from prototype
- **Trigger**: User ready to plan implementation

**lite-implement** - Implements features using validated patterns
- **When**: Implementation starts after planning
- **Why**: Spec's UI/UX section guides implementation decisions
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
- `.shipkit-lite/specs/active/[feature].md` - Existing spec to update

---

## Context Files This Skill Writes

**Updates (APPEND):**
- `.shipkit-lite/specs/active/[feature].md` - Appends UI/UX section
  - **Write Strategy**: APPEND (adds UI/UX section to existing spec)
  - **Behavior**: If spec exists, appends section. If not, creates new spec with section.
  - **Why**: Preserve existing spec content while adding prototype learnings

**May delete (if user confirms):**
- `.shipkit-mockups/[name]/` - Prototype folder after extraction

---

<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Has important context been saved to `.shipkit-lite/`?
2. **Prerequisites** - Does the next action need a spec or plan first?
3. **Session length** - Long session? Consider `/lite-work-memory` for continuity.

**Natural capabilities** (no skill needed): Implementation, debugging, testing, refactoring, code documentation.

**Suggest skill when:** User needs to make decisions, create persistence, or check project status.
<!-- /SECTION:after-completion -->

<!-- SECTION:success-criteria -->
## Success Criteria

Extraction successful when:
- [ ] Read all prototype artifacts (iterations.md, README.md, index.html)
- [ ] Identified validated patterns (what worked)
- [ ] Identified rejected approaches (what didn't work)
- [ ] Generated UI/UX section with implementation checklist
- [ ] Updated or created spec with learnings
- [ ] User knows next step (plan or implement)

**Not required:**
- Prototype doesn't need to be deleted (user choice)
- Spec doesn't need to be "complete" (UI/UX section is one part)

**Goal:** Preserve knowledge before prototype is deleted.
<!-- /SECTION:success-criteria -->
---

## Tips for Effective Extraction

**Focus on actionable patterns:**
- Don't just copy "button is blue"
- Capture "Share button top-right because users looked there first"
- Include the "why" from user feedback

**Preserve concrete examples:**
- Copy actual Tailwind classes (design system)
- Include React state patterns (implementation guidance)
- Show component structure (not full code, just key patterns)

**Create implementation checklists:**
- "Ensure X" based on what worked
- "Avoid Y" based on what failed
- Binary checks for validated patterns

**Quote user feedback:**
- Direct quotes are more valuable than summaries
- "This feels right" vs "User approved design"
- Shows real validation, not assumptions

---

**Remember:** Prototypes are disposable, but learnings are permanent. Extract before deleting.
