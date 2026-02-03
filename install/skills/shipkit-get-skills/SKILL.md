---
name: shipkit-get-skills
description: Discover and install skills from the open agent skills ecosystem (skills.sh)
argument-hint: "<search query>"
allowed-tools:
  - Bash
  - Read
---

# shipkit-get-skills - Skill Discovery & Installation

**Purpose**: Discover and install skills from the open agent skills ecosystem via conversational interface.

**Core value**: Discovery through conversation, not CLI memorization.

---

## Why This Skill Exists

**You don't naturally know what skills exist in the ecosystem.**

| Without Skill | With Skill |
|---------------|------------|
| User must know about skills.sh | User says "I need help with X" |
| User runs CLI commands manually | Claude searches and offers to install |
| User parses terminal output | Results presented conversationally |

---

## When to Invoke

**User says:**
- "Find skills for X"
- "Is there a skill for testing?"
- "I need help with commit messages"
- "Get skills", "Search skills"
- "Install a skill for API docs"

**Auto-suggest when:**
- User struggles with a task that likely has a community skill
- User asks "is there a better way to do X?"

---

## Prerequisites

**Required:**
- Node.js installed (for `npx skills` CLI)
- Internet connection

**If npx not available:**
- Offer manual install instructions
- Guide user to clone and copy skill folder

---

## Process

### Step 1: Understand Intent

When user mentions a need:

```
User: I'm struggling with writing good commit messages

Claude: I can search for skills that help with commit messages.
        Want me to look?
```

If user invokes directly with query:
```
User: /get-skills commit messages

→ Skip to Step 2
```

---

### Step 2: Search for Skills

**Run:**
```bash
npx skills find "<query>"
```

**Example:**
```bash
npx skills find "commit messages"
```

**If npx fails:**
```
⚠ npx not found (Node.js required)

Options:
  1. Install Node.js: https://nodejs.org

  2. Manual install:
     - Find skill at: https://skills.sh
     - Clone the repo
     - Copy skill folder to: .claude/skills/<name>/

Want me to search skills.sh in browser instead?
```

---

### Step 3: Present Results

Format search results conversationally:

```
Found 3 skills for "commit messages":

  [1] conventional-commits (vercel-labs/skills)
      Enforces conventional commit format with scopes

  [2] git-commit-helper (community/git-tools)
      Analyzes staged changes and suggests commit messages

  [3] semantic-commits (better-commits/skill)
      Semantic versioning aware commit messages

Install one? Enter number, or [s] to search again
```

---

### Step 4: Install Selected Skill

**Run:**
```bash
npx skills add <owner/repo>
```

**Example:**
```bash
npx skills add community/git-tools@git-commit-helper
```

**On success:**
```
✓ Installed git-commit-helper

Location: .claude/skills/git-commit-helper/
Try it: /git-commit-helper

Or just start using it — Claude will invoke automatically when relevant.
```

---

### Step 5: Handle Edge Cases

#### Skill uses shipkit- prefix

```
Note: This skill uses the "shipkit-" prefix, which is typically
reserved for Shipkit framework skills.

Installing anyway — this is your choice.
```

Non-blocking warning. User decides.

#### Skill already installed

```
git-commit-helper is already installed.

Location: .claude/skills/git-commit-helper/

[u] Update to latest  [r] Reinstall  [b] Back
```

#### No results found

```
No skills found for "quantum debugging".

Try:
  - Broader terms: "debugging", "testing"
  - Check skills.sh directly: https://skills.sh
  - Create your own skill for this use case
```

---

## Commands

| Command | Description |
|---------|-------------|
| `/get-skills` | Interactive discovery prompt |
| `/get-skills <query>` | Search by keyword |
| `/get-skills list` | Show installed skills |
| `/get-skills update` | Update all installed skills |

---

## CLI Mapping

| Skill Action | CLI Command |
|--------------|-------------|
| Search | `npx skills find <query>` |
| Install | `npx skills add <owner/repo>` |
| List installed | `npx skills list` |
| Update all | `npx skills update` |

---

## Design Decisions

1. **Naming** — `get-skills` (action-oriented, pairs with `get-mcps`)

2. **No proactive suggestions** — User invokes explicitly. Avoids Clippy problem.

3. **Namespace warning** — Light warning for `shipkit-` prefix, non-blocking

4. **Fallback without npx** — Graceful degradation with manual install option

---

## Context Files This Skill Reads

- `.claude/skills/` — Check what's already installed
- `package.json` — Verify Node.js project context (optional)

---

## Context Files This Skill Writes

**Write Strategy: NONE** (delegates to npx skills CLI)

The CLI handles all file operations:
- Creates `.claude/skills/<name>/` folder
- Writes SKILL.md and supporting files

---

## When This Skill Integrates with Others

### Relationship: Standalone Utility

This skill operates independently. It helps users extend their skill set.

**Complements:**
- `/shipkit-project-status` — Could suggest missing skills
- `/shipkit-claude-md` — Learnings about which skills work well

**Sibling:**
- `/shipkit-get-mcps` — Same pattern for MCP discovery

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

---

## Success Criteria

- [ ] User can discover skills through conversation
- [ ] Search results are clear and actionable
- [ ] Installation is one confirmation away
- [ ] Fallback works when npx unavailable
- [ ] Namespace warnings are informative but non-blocking

<!-- Shipkit v1.2.0 -->
