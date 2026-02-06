# shipkit-teach Specification

**Purpose:** Capture corrections, preferences, and learnings by writing them to CLAUDE.md files (root or subfolder). Uses Claude Code's native hierarchy instead of custom files.

---

## Core Concept

When users correct Claude or share project knowledge, this skill persists it to the appropriate CLAUDE.md file so future sessions (and subagents) automatically pick it up.

### Why CLAUDE.md Instead of Custom Files

| Approach | Pros | Cons |
|----------|------|------|
| Custom `.shipkit/learnings.md` | Separate from main instructions | Requires explicit loading, subagents don't get it automatically |
| **Native CLAUDE.md** | Auto-loaded by Claude Code, subagents in subfolders get folder-specific context | Mixed with other instructions |

**Decision:** Use native CLAUDE.md with a dedicated `## Learnings` section.

---

## How It Works

### 1. User Triggers Teaching

```
User: /teach don't use moment.js, use date-fns
```

or without inline content:

```
User: /teach
Claude: What would you like me to remember?
User: Always use date-fns instead of moment.js
```

### 2. Claude Asks for Scope

```
Claude: Where should this apply?

  [1] Project-wide (root CLAUDE.md)
  [2] Frontend only (frontend/CLAUDE.md)
  [3] Backend only (backend/CLAUDE.md)
  [4] Custom path: ___
```

Options are generated dynamically based on:
- Existing CLAUDE.md files in subfolders
- Common directory patterns (src/, lib/, packages/*)

### 3. Claude Writes to CLAUDE.md

Appends to the `## Learnings` section (creates if missing):

```markdown
## Learnings

- Use date-fns instead of moment.js for date handling
- Always use TypeScript strict mode
- Prefer named exports over default exports
```

---

## Triggers

| Trigger | Context |
|---------|---------|
| `/teach <learning>` | Explicit command with inline content |
| `/teach` | Opens dialog (prompts for learning) |
| "Remember this" | Natural language trigger |
| "Save this for next time" | Natural language trigger |
| "Add this to CLAUDE.md" | Natural language trigger |
| "Don't forget this" | Natural language trigger |

### No Auto-Suggest (Important)

Claude does **not** ask "Should I remember this?" after corrections. User must explicitly request persistence.

| ❌ Don't Do | ✅ Do |
|-------------|-------|
| User corrects → Claude asks "Remember this?" | User says "remember this" → Claude triggers teach flow |

**Removing learnings:** No separate skill needed. User says "remove the learning about X" and Claude edits CLAUDE.md directly.

---

## CLAUDE.md Structure (Shipkit Standard)

The installed CLAUDE.md follows this structure:

```markdown
# Shipkit

Brief project description.

---

## Core Rules
<!-- Fundamental project rules — rarely changed -->

---

## Working Preferences
<!-- User's style/behavior preferences. shipkit-teach appends here. -->

- Verbosity: Concise
- Code style: Match existing codebase
- (learnings about HOW Claude should work go here)

---

## Context Files
<!-- Reference to .shipkit/ files -->

---

## Codebase Navigation
<!-- How to use codebase-index.json -->

---

## Skills Reference
<!-- When to use which skill -->

---

## Meta-Behavior
<!-- Instructions for shipkit-teach behavior -->

---

## Project Learnings
<!-- Mistakes corrected, patterns discovered. shipkit-teach appends here. -->

- (learnings about WHAT to do/avoid go here)
```

### Two Target Sections

| Learning Type | Target Section | Example |
|---------------|----------------|---------|
| **Style/Behavior** | `## Working Preferences` | "Be more concise", "Don't explain unless asked" |
| **Technical/Pattern** | `## Project Learnings` | "Use date-fns not moment", "API returns {data:[]}" |

### Location Decision Tree

```
What type of learning?
├── Style/Behavior → ## Working Preferences
└── Technical/Pattern → ## Project Learnings

Which CLAUDE.md?
├── Global → Root CLAUDE.md
└── Folder-specific
    ├── Folder has CLAUDE.md → Append to it
    └── Folder lacks CLAUDE.md → Create it (with minimal structure)
```

### Subfolder CLAUDE.md Template

When creating a new subfolder CLAUDE.md:

```markdown
# Frontend

Frontend-specific context and learnings.

---

## Working Preferences

<!-- Style preferences for frontend work -->

---

## Project Learnings

<!-- Frontend-specific patterns and corrections -->

```

---

## Categories of Learnings

| Category | Example | Scope |
|----------|---------|-------|
| **Library choice** | "Use date-fns not moment" | Usually global |
| **Code style** | "Prefer named exports" | Usually global |
| **API patterns** | "Responses wrap in { data }" | Often folder-specific |
| **Framework conventions** | "Use Tailwind, not CSS modules" | Often folder-specific |
| **Avoid patterns** | "Don't use any type" | Usually global |
| **Testing** | "Use vitest not jest" | Usually global |
| **Domain knowledge** | "Users have multiple orgs" | Global |

---

## Skill Definition

```yaml
---
name: shipkit-teach
description: Persist learnings and corrections to CLAUDE.md
invoke: user
model: haiku
tools:
  - Read
  - Write
  - Glob
---
```

---

## Workflow

### Step 1: Receive Learning

Either from:
- Explicit `/teach` command
- User correction in conversation
- User says "remember this"

### Step 2: Classify Learning Type

| If learning is about... | Type | Target Section |
|-------------------------|------|----------------|
| How Claude should behave | Style | `## Working Preferences` |
| What code patterns to use | Technical | `## Project Learnings` |

Examples:
- "Be more concise" → Style → Working Preferences
- "Don't use moment.js" → Technical → Project Learnings
- "Always confirm before deleting" → Style → Working Preferences
- "API returns {data:[]} not {items:[]}" → Technical → Project Learnings

### Step 3: Identify Scope

```
Claude: Should this apply project-wide or to a specific folder?

  [1] Project-wide (root CLAUDE.md)
  [2] Frontend (frontend/CLAUDE.md)
  [3] Other path: ___
```

Options generated from: `Glob("**/CLAUDE.md")` + common directories.

### Step 4: Read Target CLAUDE.md

```
Read(<selected-path>/CLAUDE.md)
```

Parse to find:
- `## Working Preferences` section
- `## Project Learnings` section

### Step 5: Append to Correct Section

**For Style learning:**
```markdown
## Working Preferences

- Verbosity: Concise
- Code style: Match existing codebase
+ - Always confirm before file deletions    ← NEW
```

**For Technical learning:**
```markdown
## Project Learnings

- Use date-fns instead of moment.js
+ - API responses wrap data in { data: [] }    ← NEW
```

### Step 6: Confirm

```
Claude: Added to CLAUDE.md → Project Learnings:
  - API responses wrap data in { data: [] }

This will apply to all future sessions.
```

---

## Edge Cases

### No CLAUDE.md Exists

```
Claude: No CLAUDE.md found at frontend/. Should I create one?
  [1] Yes, create frontend/CLAUDE.md
  [2] Add to root CLAUDE.md instead
```

### Learning Already Exists

Check for duplicates before adding. If similar learning exists:

```
Claude: Similar learning already exists:
  - "Prefer date-fns over moment"

Should I:
  [1] Skip (already covered)
  [2] Add anyway (more specific)
  [3] Replace existing
```

### Conflicting Learning

If new learning contradicts existing:

```
Claude: This seems to conflict with existing learning:
  Existing: "Use moment.js for dates"
  New: "Use date-fns for dates"

Should I:
  [1] Replace old with new
  [2] Keep both (maybe context-specific)
  [3] Cancel
```

---

## Integration with Subagents

### How It Works Automatically

1. User teaches: "In frontend, use Tailwind"
2. Skill writes to `frontend/CLAUDE.md`
3. Later, subagent spawned to work in `frontend/`
4. Claude Code lazy-loads `frontend/CLAUDE.md`
5. Subagent knows to use Tailwind — no extra prompting needed

### Why This Matters

Traditional approach:
```
spawn subagent → manually pass context → hope it remembers
```

With shipkit-teach:
```
spawn subagent → CLAUDE.md auto-loaded → context is there
```

---

## Success Metrics

1. **Learnings persist** — New sessions pick up teachings automatically
2. **Subagents inherit context** — Folder-specific learnings apply to subagents
3. **No duplicates** — Skill detects and handles duplicate/conflicting learnings
4. **User stays in control** — Always confirms before writing

---

## Design Decisions

1. **No auto-suggest** — Claude never asks "Should I remember this?" User must explicitly invoke `/teach`. Avoids annoyance.

2. **Flat list** — Simple bullets in each section. Users can organize manually if desired.

3. **No `/forget` skill** — User says "remove the learning about X" and Claude edits CLAUDE.md directly. Just a line deletion.

---

## Relationship to Existing Skills

| Skill | Relationship |
|-------|--------------|
| `shipkit-project-context` | Reads CLAUDE.md; `teach` writes to it |
| `shipkit-codebase-index` | Different purpose (structure vs. learnings) |
| `shipkit-detect` | Could trigger "should I remember this?" prompt |

---

## Replaces

This skill replaces two previously proposed skills:

- ~~`shipkit-preferences`~~ — Folded into teach (preferences are learnings)
- ~~`shipkit-learnings`~~ — This is the implementation

---

## Files Modified by This Skill

| File | Action |
|------|--------|
| `CLAUDE.md` (root) | Append to `## Learnings` section |
| `<folder>/CLAUDE.md` | Append to `## Learnings` section |

No custom `.shipkit/` files created.
