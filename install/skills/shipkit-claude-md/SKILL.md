---
name: shipkit-claude-md
description: Update CLAUDE.md with learnings, preferences, or project context. Use when user says "update claude.md", "add to claude.md", or wants to persist something.
allowed-tools:
  - Read
  - Write
  - Glob
---

# shipkit-claude-md

Update CLAUDE.md so future sessions and subagents automatically inherit learnings and context.

---

## When to Invoke

**Explicit triggers:**
- `/claude-md <content>` — with inline content
- `/claude-md` — prompts for what to add
- `/shipkit-claude-md`

**Natural language triggers:**
- "Update CLAUDE.md"
- "Add to CLAUDE.md"
- "Update my claude md"
- "Remember this"
- "Save this for next time"

**Important:** Never auto-suggest. Only act when user explicitly requests persistence.

---

## Prerequisites

**Required:**
- Root `CLAUDE.md` exists (installed by Shipkit)
- CLAUDE.md has `## Working Preferences` and `## Project Learnings` sections

**Optional:**
- Subfolder `CLAUDE.md` files for folder-specific learnings

**Important distinction:**
- `CLAUDE.md` → User-editable (preferences, learnings) — THIS skill edits this file
- `.claude/rules/shipkit.md` → Framework-managed (skills reference, core rules) — DO NOT edit

---

## Process

### Step 1: Get the Learning

If invoked with content:
```
/teach use date-fns instead of moment.js
```
→ Learning = "use date-fns instead of moment.js"

If invoked without content:
```
/teach
```
→ Ask: "What would you like me to remember?"

### Step 2: Classify Type

| Learning About... | Type | Target Section |
|-------------------|------|----------------|
| How Claude behaves | Style | `## Working Preferences` |
| Code patterns/libraries | Technical | `## Project Learnings` |

Examples:
- "Be more concise" → Style → Working Preferences
- "Use date-fns not moment" → Technical → Project Learnings
- "Always confirm before deleting" → Style → Working Preferences
- "API returns {data:[]} wrapper" → Technical → Project Learnings

### Step 3: Determine Scope

Check for existing CLAUDE.md files:
```
Glob("**/CLAUDE.md")
```

Present options:
```
Where should this apply?

  [1] Project-wide (root CLAUDE.md)
  [2] frontend/ (frontend/CLAUDE.md)
  [3] Other path: ___
```

If user picks a folder without CLAUDE.md, offer to create one.

### Step 4: Read Target File

```
Read(<path>/CLAUDE.md)
```

Find the target section:
- For Style → find `## Working Preferences`
- For Technical → find `## Project Learnings`

### Step 5: Check for Duplicates

Scan existing learnings in the section. If similar exists:
```
Similar learning already exists:
  - "Prefer date-fns over moment"

  [1] Skip (already covered)
  [2] Add anyway (more specific)
  [3] Replace existing
```

### Step 6: Append Learning

Add new bullet to the end of the target section.

**Before:**
```markdown
## Project Learnings

- Use date-fns instead of moment.js
```

**After:**
```markdown
## Project Learnings

- Use date-fns instead of moment.js
- API responses wrap data in { data: [] }
```

### Step 7: Confirm

```
Added to CLAUDE.md → Project Learnings:
  - API responses wrap data in { data: [] }

This will apply to all future sessions.
```

If folder-specific:
```
Added to frontend/CLAUDE.md → Project Learnings:
  - Use Tailwind instead of CSS modules

This will apply when working in frontend/.
```

---

## Creating Subfolder CLAUDE.md

If user wants folder-specific learning but no CLAUDE.md exists:

```
No CLAUDE.md found in frontend/. Create one?

  [1] Yes, create frontend/CLAUDE.md
  [2] Add to root CLAUDE.md instead
```

If yes, create minimal structure:

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

Then append the learning.

---

## Important Rules

1. **Never auto-suggest** — Don't ask "Should I remember this?" Only act when user explicitly requests
2. **Always confirm** — Show what was added and where
3. **Respect structure** — Append to existing sections, don't reorganize
4. **Check duplicates** — Avoid redundant entries
5. **Never edit `.claude/rules/`** — Framework rules are managed by `/shipkit-update`, not this skill

---

## Removing Learnings

No special handling needed. User says:
```
Remove the learning about moment.js
```

Claude reads CLAUDE.md, finds the line, removes it, confirms.

---

## When This Skill Integrates with Others

### Before This Skill

| Skill | Relationship |
|-------|--------------|
| Any skill | User may want to persist a learning discovered during any workflow |

### After This Skill

| Skill | Relationship |
|-------|--------------|
| All future sessions | Learnings auto-loaded via CLAUDE.md |
| Subagents in subfolders | Folder-specific learnings auto-loaded via lazy loading |

### Related Skills

| Skill | Relationship |
|-------|--------------|
| `/shipkit-project-context` | Reads CLAUDE.md; teach writes to it |
| `/shipkit-codebase-index` | Different purpose (structure vs. learnings) |

---

## Context Files This Skill Reads

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Root project instructions (find target section) |
| `<folder>/CLAUDE.md` | Subfolder instructions (if folder-specific) |
| `**/CLAUDE.md` | Glob to find existing CLAUDE.md files for scope options |

---

## Context Files This Skill Writes

| File | Action |
|------|--------|
| `CLAUDE.md` | Append to `## Working Preferences` or `## Project Learnings` |
| `<folder>/CLAUDE.md` | Create if needed, append learning |

**Write Strategy:** APPEND-ONLY to existing sections. Never reorganize or overwrite.

---

<!-- SECTION:after-completion -->
## After Completion

**Confirm to user:**
- What learning was added
- Which section (Working Preferences or Project Learnings)
- Which file (root or subfolder CLAUDE.md)
- When it takes effect (all future sessions, or when working in folder)

**No follow-up skill needed** — learnings are immediately active for current session and persist to future sessions.
<!-- /SECTION:after-completion -->

---

<!-- SECTION:success-criteria -->
## Success Criteria

- [ ] Learning captured from user
- [ ] Type classified (Style vs Technical)
- [ ] Scope determined (root vs folder)
- [ ] Duplicates checked
- [ ] Learning appended to correct section
- [ ] User confirmed what was added and where
<!-- /SECTION:success-criteria -->