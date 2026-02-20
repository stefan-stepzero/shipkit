---
name: shipkit-dev-review
description: Reviews framework changes for design quality, pattern consistency, CC compatibility, and Skill Value Test compliance. Goes beyond structural integrity to catch design issues. Use after implementing framework changes, before release.
argument-hint: "[--scope recent|branch|skill:<name>|all] [--strict]"
---

# shipkit-dev-review - Framework Design Review

**Purpose**: Catch design issues in framework changes that structural validation misses

**What it does**:
- Reviews recent changes or specific skills for design quality
- Validates Skill Value Test compliance
- Checks pattern consistency across the framework
- Verifies Claude Code compatibility
- Produces a review report with actionable findings

**How it differs from existing quality tools:**

| Tool | What it checks |
|------|---------------|
| `shipkit-framework-integrity` | Structural + consistency: frontmatter, 7-file integration, manifest sync, broken refs, installer |
| **`shipkit-dev-review`** | **Design: is this the RIGHT thing built the RIGHT way?** |

---

## When to Invoke

**User says:**
- "Review this change"
- "Is this skill well designed?"
- "Code review the framework changes"
- "Check quality before release"
- "Review what we just built"

**Automated trigger:**
- After implementing framework changes
- Before running `/shipkit-dev-release`
- As the reviewer role in a `/shipkit-dev-team`

---

## Prerequisites

**Required**:
- Changes to review (recent commits, a branch, or specific files)

**Helpful context**:
- `.claude/specs/{feature}.json` — spec the changes implement
- `CLAUDE.md` — Skill Value Test, framework rules
- `docs/development/SKILL-QUALITY-AND-PATTERNS.md` — quality standards

---

## Process

### Step 1: Identify Scope

Based on argument:
- `--scope recent` — Review uncommitted changes + last commit (default)
- `--scope branch` — Review all commits on current branch vs main
- `--scope skill:<name>` — Review a specific skill in depth
- `--scope all` — Review entire framework (expensive, use sparingly)

```bash
# For recent
git diff HEAD~1 --name-only
git diff --name-only

# For branch
git log main..HEAD --name-only --pretty=format:""
```

### Step 2: Categorize Changes

Group changed files by component type:
- **Skills** — `install/skills/shipkit-*/SKILL.md`
- **Local skills** — `.claude/skills/shipkit-*/SKILL.md`
- **Agents** — `install/agents/shipkit-*.md`
- **Hooks** — `install/shared/hooks/*.py`
- **Config** — `install/settings/`, `install/profiles/`
- **Docs** — `docs/generated/`, `README.md`
- **Rules** — `install/rules/`
- **Templates** — `install/claude-md/`

### Step 3: Design Review — Skills

For each changed/new skill, check:

**3.1 Value Test**
- [ ] Does this skill force explicit human decisions? Which ones?
- [ ] Does this skill create persistence Claude lacks? What persists?
- [ ] If neither → FLAG: "Skill may be redundant"

**3.2 Scope Discipline**
- [ ] Does the skill do ONE thing well?
- [ ] Is the process section < 10 steps? (More = over-engineered)
- [ ] Does it avoid implementing what Claude does naturally?
- [ ] Are there steps that could be removed without losing value?

**3.3 Context Awareness**
- [ ] Does it read relevant `.shipkit/` context before acting?
- [ ] Does it check for existing decisions instead of assuming defaults?
- [ ] Are context file paths correct and existing?

**3.4 Integration Quality**
- [ ] "Before/After" integrations make sense causally (not just lists)
- [ ] Cross-references are bidirectional
- [ ] No circular dependencies

**3.5 Output Quality**
- [ ] Outputs are structured (JSON for data, MD for narrative)
- [ ] JSON outputs follow artifact convention
- [ ] Outputs are consumed by a downstream skill (not dead-end data)

**3.6 Pattern Consistency**
- [ ] Follows same frontmatter pattern as peer skills
- [ ] Section structure matches framework conventions
- [ ] Naming matches conventions (CLAUDE.md naming table)

### Step 4: Design Review — Agents

For each changed/new agent:

- [ ] Role is distinct from existing agents (no overlap)
- [ ] Model selection matches role complexity (Haiku for simple, Sonnet for standard, Opus for reasoning-heavy)
- [ ] `permissionMode` is appropriate
- [ ] Agent prompt doesn't duplicate skill instructions
- [ ] If `memory` field used, scoping is appropriate

### Step 5: Design Review — Hooks

For each changed/new hook:

- [ ] Hook event is correct for the trigger
- [ ] Exit codes follow convention (0 = allow, 2 = block with feedback)
- [ ] Error handling uses silent failure pattern (never crashes)
- [ ] Timeout is appropriate for what the hook does
- [ ] State files use `.local.` naming (gitignored)
- [ ] Hook is idempotent (safe to fire multiple times)

### Step 6: Design Review — Cross-Cutting

Check framework-wide concerns:

- [ ] No duplicate functionality between skills
- [ ] Skill count in README/overview matches actual count
- [ ] Settings permissions cover all new skills
- [ ] Manifest entries match disk reality
- [ ] No secrets or credentials in committed files

### Step 7: CC Compatibility Check

Against current Claude Code version:
- [ ] All frontmatter fields are recognized
- [ ] No deprecated patterns used
- [ ] Hook events are valid
- [ ] Settings schema is current

### Step 8: Write Review Report

Present findings inline (not a JSON file — reviews are transient):

```
## Framework Design Review

**Scope**: {what was reviewed}
**Date**: {date}

### Findings

#### BLOCK: {title}
{description}
**File**: {path}:{line}
**Fix**: {concrete action}

#### WARN: {title}
{description}
**File**: {path}:{line}
**Suggestion**: {what to consider}

#### NOTE: {title}
{description}

### Summary
- Blockers: {N}
- Warnings: {N}
- Notes: {N}
- **Verdict**: {PASS / PASS WITH WARNINGS / BLOCK}
```

**If `--strict` mode**: Warnings are promoted to blockers.

---

## Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| **BLOCK** | Must fix before merge/release | Stop and fix |
| **WARN** | Should fix, but not blocking | Fix or document why not |
| **NOTE** | Observation, no action needed | Awareness only |

---

## When This Skill Integrates with Others

### Before This Skill
- Implementation — changes must exist to review
- `/shipkit-framework-integrity` — structural checks should pass first
  - **Why**: Don't waste design review time on structurally broken skills

### After This Skill
- `/shipkit-dev-release` — Release after review passes
  - **Trigger**: Review verdict is PASS
  - **Why**: Only release reviewed code
- Fix and re-review — if blockers found

---

## Context Files This Skill Reads

- `.claude/specs/{feature}.json` — Spec being implemented (if available)
- `CLAUDE.md` — Skill Value Test, framework rules
- `docs/development/SKILL-QUALITY-AND-PATTERNS.md` — Quality standards
- All changed files in scope

## Context Files This Skill Writes

- None — review output is presented inline, not persisted
