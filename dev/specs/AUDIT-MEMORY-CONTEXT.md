# Memory & Context Patterns Audit

**Status:** Implemented
**Last Updated:** 2026-02-06
**Implementation:** Auto memory documented in CLAUDE.md. Remaining items moved to REMAINING-ENHANCEMENTS.md

## Purpose

Review new Claude Code memory and context features for potential adoption in Shipkit.

## New Capabilities to Audit

| Feature | Description | Release |
|---------|-------------|---------|
| `.claude/rules/` | Directory for rule files | v2.0.64 |
| CLAUDE.md imports | `@path/to/file.md` syntax | v0.2.107 |
| Auto memory | Claude records/recalls memories | v2.1.32 |
| `language` setting | Configure response language | v2.1.0 |
| `plansDirectory` setting | Customize plan file location | v2.1.9 |

## Current Shipkit Context Structure

```
.shipkit/
├── why.md              # Vision & constraints
├── stack.md            # Tech stack (auto-detected)
├── architecture.md     # Architecture decisions (append-only)
├── progress.md         # Session continuity
├── codebase-index.json # Navigation index
├── specs/
│   └── active/         # Feature specifications
├── plans/
│   └── active/         # Implementation plans
└── scripts/            # Helper scripts

.claude/
├── settings.json       # Settings & permissions
├── skills/             # Skill definitions
├── agents/             # Agent personas
└── hooks/              # Hook scripts

CLAUDE.md               # Project instructions (Shipkit template)
```

---

## Analysis

### 1. `.claude/rules/` Directory

**What it does:**
- Alternative to monolithic CLAUDE.md for project rules
- All `.md` files in `.claude/rules/` auto-loaded as project memory
- Supports **path-specific rules** via YAML frontmatter with `paths` field
- Loaded at same priority as `.claude/CLAUDE.md`
- Supports subdirectories for organization
- Supports symlinks for shared rules across projects

**Example structure:**
```
.claude/rules/
├── code-style.md       # General style guidelines
├── testing.md          # Testing conventions
├── security.md         # Security requirements
└── frontend/
    ├── react.md        # React-specific rules
    └── styles.md       # CSS/styling rules
```

**Path-specific rule example:**
```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API Development Rules
- All API endpoints must include input validation
- Use standard error response format
```

**Current Shipkit equivalent:**
- Shipkit uses a single CLAUDE.md template (`install/claude-md/shipkit.md`)
- Project-specific context goes in `.shipkit/` files (why.md, stack.md, architecture.md)
- No modular rules system currently

**Compatibility assessment:** HIGH
- Shipkit's current CLAUDE.md contains: Core Rules, Working Preferences, Quality Standards, Context Files reference, Skills Reference, Meta-Behavior, Project Learnings
- Many of these could be split into focused rule files

**Should adopt?** YES - Partial adoption recommended

**Rationale:**
1. **Separation of concerns** - Skills reference, quality standards, and meta-behavior could be separate files
2. **Path-specific rules** - Powerful for projects with mixed tech stacks (e.g., different rules for frontend vs backend)
3. **Symlinks enable sharing** - Could create reusable Shipkit rule files that projects link to
4. **Doesn't break existing** - CLAUDE.md still works, rules/ is additive

---

### 2. CLAUDE.md Imports (`@path/to/file.md`)

**What it does:**
- Import additional files into CLAUDE.md context
- Syntax: `@path/to/file.md` or `@README` (shorthand)
- Relative paths resolve from file containing the import
- Max depth: 5 recursive imports
- Requires one-time user approval per project for security
- Not evaluated inside code blocks (prevents accidental imports)

**Example:**
```markdown
See @README for project overview and @package.json for available npm commands.

# Additional Instructions
- git workflow @docs/git-instructions.md
```

**Current Shipkit usage:** None

**Opportunities:**
1. **Import `.shipkit/` context files** directly into CLAUDE.md:
   ```markdown
   # Project Vision
   @.shipkit/why.md

   # Tech Stack
   @.shipkit/stack.md
   ```
2. **User customization** - Let users import their own rule files
3. **Modular Shipkit sections** - Split CLAUDE.md into importable chunks

**Compatibility assessment:** HIGH
- Works alongside existing session-start hook
- Could reduce hook complexity (no need to manually output context)

**Should adopt?** YES - Strong adoption recommended

**Rationale:**
1. **Native feature** - Uses Claude Code's built-in import system vs custom hooks
2. **Cleaner session start** - Context loads via imports, hook just shows status summary
3. **User flexibility** - Users can easily add/remove imports
4. **Recursive imports** - Can chain context files naturally

---

### 3. Auto Memory

**What it does:**
- Claude automatically records and recalls learnings during sessions
- No explicit user action required
- Memory editable via `/memory` command
- Uses CLAUDE.md for persistent storage

**Impact on Shipkit:**
- Shipkit already has explicit memory capture patterns:
  - `/shipkit-work-memory` - End-of-session progress logging
  - `/shipkit-architecture-memory` - Architecture decision logging
  - `/shipkit-claude-md` - Update CLAUDE.md with learnings
  - "Project Learnings" section in CLAUDE.md

**Compatibility assessment:** MODERATE - Potential overlap

**Potential conflicts:**
1. **Duplicate memories** - Auto memory might record what Shipkit skills already capture
2. **Memory location** - Auto memory goes to CLAUDE.md; Shipkit spreads context across multiple files
3. **Control** - Auto memory is implicit; Shipkit's approach is explicit ("ask before generating")

**Should adopt?** MONITOR - Understand before integrating

**Rationale:**
1. Shipkit's philosophy is "explicit over implicit" - skills force human decisions
2. Auto memory might be too aggressive for solo dev workflow
3. Need to test how auto memory interacts with Shipkit's structured context files
4. May want to document how to disable/configure auto memory in Shipkit docs

**Recommendation:**
- Add a section to CLAUDE.md about auto memory interaction
- Test how auto memory behaves with Shipkit's existing "Meta-Behavior" section
- Consider whether to embrace or limit auto memory in Shipkit workflows

---

### 4. `language` Setting

**What it does:**
- Configure Claude's response language
- Set in `settings.json`: `"language": "japanese"`
- Affects all responses in configured scope

**Current Shipkit usage:** Not exposed

**Should Shipkit expose this?** YES - Optional, in installer

**Rationale:**
1. **Global dev teams** - Non-English speakers benefit
2. **Simple to add** - Just a settings.json field
3. **Non-invasive** - Default to no setting (English)

**Implementation:**
- Add optional prompt in installer: "Preferred response language? (press Enter for English)"
- If set, add to generated `settings.json`
- Document in CLAUDE.md as a customizable setting

---

### 5. `plansDirectory` Setting

**What it does:**
- Customize where plan files are stored
- Set in `settings.json`: `"plansDirectory": "./plans"`
- Default: `~/.claude/plans`
- Supports relative (to project root) and absolute paths

**Current Shipkit default:** `.shipkit/plans`

**Alignment assessment:** MISALIGNED

**Issue:**
- Claude Code's default: `~/.claude/plans` (user-level, cross-project)
- Shipkit's default: `.shipkit/plans` (project-level, version-controlled)
- Shipkit's `workspace.plansPath` in settings.json is custom, not the official `plansDirectory`

**Should align?** YES

**Rationale:**
1. **Use official setting** - `plansDirectory` is the Claude Code standard
2. **Keep project-level storage** - `.shipkit/plans` is better for Shipkit's philosophy (project context stays with project)
3. **Settings interoperability** - Future Claude Code features may use `plansDirectory`

**Implementation:**
- Add `"plansDirectory": ".shipkit/plans"` to settings.json template
- Keep `workspace.plansPath` for backward compatibility (or migrate)
- Verify Claude Code respects this setting for `/plan` command output

---

## Recommendations Summary

| Feature | Adopt? | Priority | Effort |
|---------|--------|----------|--------|
| `.claude/rules/` | Partial | Medium | Medium |
| CLAUDE.md imports | Yes | High | Low |
| Auto memory | Monitor | Low | None |
| `language` setting | Yes | Low | Low |
| `plansDirectory` setting | Yes | High | Low |

### Priority Order

1. **`plansDirectory` setting** - Quick fix, ensures alignment with Claude Code
2. **CLAUDE.md imports** - High value, reduces hook complexity
3. **`language` setting** - Easy win, improves accessibility
4. **`.claude/rules/`** - Valuable but requires CLAUDE.md restructuring
5. **Auto memory** - Monitor and document, don't actively integrate yet

---

## Implementation Plan

### Phase 1: Settings Alignment (Immediate)

**File:** `install/settings/shipkit.settings.json`

Add official `plansDirectory` setting:
```json
{
  "plansDirectory": ".shipkit/plans",
  // ... existing settings
}
```

**File:** `installers/install.py`

Add optional language prompt:
```python
def prompt_for_language_setting():
    """Prompt user for response language preference"""
    print("Preferred response language? (press Enter for default/English)")
    lang = input("  Language: ").strip()
    return lang if lang else None
```

Add to `generate_settings()` if language is set:
```python
if language_setting:
    settings["language"] = language_setting
```

### Phase 2: CLAUDE.md Imports (Short-term)

**File:** `install/claude-md/shipkit.md`

Replace inline context loading with imports:
```markdown
# Shipkit

Solo dev framework for shipping MVPs.

---

## Project Context

@.shipkit/why.md
@.shipkit/stack.md
@.shipkit/architecture.md

---

## Core Rules
... (keep existing)
```

**File:** `install/shared/hooks/shipkit-session-start.py`

Simplify to only output:
1. Update check
2. Quick status summary
3. Smart recommendation

Remove context file output (now handled by imports).

### Phase 3: Modular Rules (Medium-term)

**New files:**
```
install/rules/
├── shipkit-core-rules.md       # Core behavior rules
├── shipkit-quality-standards.md # AI agent accessibility, etc.
├── shipkit-skills-reference.md  # Skills table
└── shipkit-meta-behavior.md     # Memory handling behavior
```

**Updated CLAUDE.md:**
```markdown
# Shipkit

Solo dev framework for shipping MVPs.

## Context
@.shipkit/why.md
@.shipkit/stack.md

## Rules
See `.claude/rules/` for:
- Core workflow rules
- Quality standards
- Skills reference
```

**Installer changes:**
- Copy rules to `.claude/rules/`
- Update directory structure diagram

### Phase 4: Auto Memory Documentation (Ongoing)

**Add to CLAUDE.md:**
```markdown
## Auto Memory Interaction

Claude Code's auto memory feature may record learnings automatically.
Shipkit's explicit memory skills (/shipkit-work-memory, /shipkit-architecture-memory)
are preferred for structured context.

If auto memory duplicates Shipkit context:
- Use /memory command to review and clean up
- Prefer .shipkit/ files for project-critical context
```

---

## Testing Checklist

- [ ] Verify `plansDirectory` is respected by Claude Code `/plan` command
- [ ] Test CLAUDE.md imports with `.shipkit/` files
- [ ] Verify one-time approval dialog works for imports
- [ ] Test `language` setting with non-English value
- [ ] Verify `.claude/rules/` files load correctly with path-specific frontmatter
- [ ] Test auto memory interaction with Shipkit's existing meta-behavior section
- [ ] Verify session-start hook still works after import changes

---

## References

- Claude Code Memory Docs: https://code.claude.com/docs/en/memory
- Claude Code Settings Docs: https://code.claude.com/docs/en/settings
- Claude Code CHANGELOG: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
