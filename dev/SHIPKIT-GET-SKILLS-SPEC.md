# shipkit-get-skills Specification

**Purpose:** Discover and install skills from the open agent skills ecosystem (skills.sh).

---

## Core Concept

When a user needs a capability that might exist as a skill, this skill helps them find and install it. Wraps the `npx skills` CLI with a conversational interface.

---

## Why This Skill Exists

| Without Skill | With Skill |
|---------------|------------|
| User must know about skills.sh | User says "I need help with X" |
| User runs CLI commands manually | Claude searches and offers to install |
| User parses terminal output | Results presented conversationally |

The value is **discovery through conversation**, not just CLI wrapping.

---

## Triggers

| Trigger | Action |
|---------|--------|
| `/get-skills` | Interactive search prompt |
| `/get-skills <query>` | Search for specific capability |
| "Is there a skill for X?" | Search and present options |
| "I need help with API docs" | Suggest searching for skills |
| "Find skills for testing" | Search and present options |

---

## Workflow

### Step 1: Understand Intent

```
User: I'm struggling with writing good commit messages

Claude: I can search for skills that help with commit messages.
        Want me to look?
```

### Step 2: Search

```bash
npx skills find "commit messages"
```

### Step 3: Present Results

```
Found 3 skills for "commit messages":

  [1] conventional-commits (vercel-labs/skills)
      Enforces conventional commit format with scopes

  [2] git-commit-helper (community/git-tools)
      Analyzes staged changes and suggests commit messages

  [3] semantic-commits (better-commits/skill)
      Semantic versioning aware commit messages

Install one? Enter number or [s] to search again
```

### Step 4: Install

```
User: 2

Claude: Installing git-commit-helper...

→ npx skills add community/git-tools@git-commit-helper

✓ Installed to .claude/skills/git-commit-helper/

Try it with: /git-commit-helper
Or just write code and it'll suggest commit messages automatically.
```

---

## Commands

| Command | Description |
|---------|-------------|
| `/get-skills` | Interactive discovery |
| `/get-skills <query>` | Search by keyword |
| `/get-skills list` | Show installed skills |
| `/get-skills update` | Update all skills |

---

## CLI Mapping

| Skill Action | CLI Command |
|--------------|-------------|
| Search | `npx skills find <query>` |
| Install | `npx skills add <owner/repo>` |
| List | `npx skills list` |
| Update | `npx skills update` |

---

## Skill Definition

```yaml
---
name: shipkit-get-skills
description: Discover and install skills from skills.sh
invoke: user
model: haiku
tools:
  - Bash
  - Read
---
```

---

## Edge Cases

### No Results Found

```
No skills found for "quantum computing debugging".

Try:
  - Broader terms: "debugging", "physics"
  - Check skills.sh directly: https://skills.sh
  - Create your own skill for this niche use case
```

### Skill Already Installed

```
conventional-commits is already installed.

Location: .claude/skills/conventional-commits/
Version: 1.2.0

[u] Update to latest  [r] Reinstall  [b] Back
```

### npx Not Available

```
⚠ npx not found.

The skills CLI requires Node.js.
Install Node.js from: https://nodejs.org

Or install skills manually by copying SKILL.md files to:
  .claude/skills/<skill-name>/
```

---

## What This Skill Does NOT Do

- **Manage MCPs** → Use `/get-mcps` instead
- **Create skills** → Use `/create-skill` instead
- **Validate skills** → Use `/validate-skill` instead

---

## Success Metrics

1. **Easy discovery** — User describes need, skill finds matches
2. **Low friction install** — One confirmation, done
3. **Conversational** — Natural language, not CLI memorization

---

## Design Decisions

1. **Naming** — `get-skills` (not `find-skills` or `skills`)
   - Action-oriented: implies find → choose → install
   - Pairs with `get-mcps`

2. **No proactive suggestions** — User invokes explicitly
   - Avoids Clippy problem
   - If added later: opt-in, very conservative (3+ patterns)

3. **Namespace warning** — Light warning, don't block
   - If skill uses `shipkit-` prefix, show note:
     "This uses the shipkit- prefix, typically reserved for Shipkit framework skills."
   - Non-blocking. User's choice.

4. **Fallback without npx** — Graceful degradation
   - Detect if npx works
   - If not: explain Node.js requirement + offer manual clone/copy alternative

---

## Relationship to Other Skills

| Skill | Relationship |
|-------|--------------|
| `shipkit-get-mcps` | Sibling — MCPs are separate ecosystem |
| `shipkit-project-status` | Could suggest missing skills |
| `shipkit-teach` | Learnings about which skills work well |
