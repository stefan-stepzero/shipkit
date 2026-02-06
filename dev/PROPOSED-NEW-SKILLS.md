# Proposed New Skills

Consolidated list of new skills to add to Shipkit.

---

## Summary

| Skill | Purpose | Priority | Spec Status |
|-------|---------|----------|-------------|
| **shipkit-teach** | Persist learnings to CLAUDE.md (replaces preferences + learnings) | 🔴 High | ✅ Built |
| **shipkit-codebase-index** | Generate project map to avoid exploration waste | 🔴 High | ✅ Built |
| **shipkit-get-skills** | Discover and install skills from skills.sh | 🔴 High | ✅ Built |
| **shipkit-get-mcps** | Discover and install MCP servers | 🔴 High | ✅ Built |
| **shipkit-standards** | Define and enforce project quality standards | 🟡 Medium | ✅ `SHIPKIT-STANDARDS-SPEC.md` |
| ~~shipkit-checkpoint~~ | ~~Save state before context overflow~~ | — | Merged into work-memory |
| **shipkit-verify** | Enforce verification after implementation | 🟢 Low | ✅ `SHIPKIT-VERIFY-SPEC.md` |

---

## Tier 1: True Memory Gaps (High Priority)

These address actual capability gaps — Claude cannot do these without file persistence.

### shipkit-teach

**Purpose:** Persist learnings and corrections to CLAUDE.md files (root or subfolder). Replaces both preferences and learnings with a unified approach using native CLAUDE.md hierarchy.

**Output:** Appends to `## Working Preferences` or `## Project Learnings` sections in CLAUDE.md

**Triggers:**
- `/teach <learning>` — Explicit teaching
- After user correction — "Should I remember this?"
- "Remember this for next time"

**What it captures:**
- **Style/Behavior** → Working Preferences section
  - Communication style (verbose vs concise)
  - Confirmation preferences
  - Code style preferences
- **Technical/Patterns** → Project Learnings section
  - Library choices ("Use date-fns not moment")
  - API patterns ("Returns {data:[]} wrapper")
  - Avoid patterns ("Don't use any type")

**Key Design:**
- Uses native CLAUDE.md hierarchy (not custom .shipkit/ files)
- Subfolder CLAUDE.md files auto-load for subagents (lazy loading)
- Two target sections based on learning type

**Spec:** `SHIPKIT-TEACH-SPEC.md`

---

### shipkit-codebase-index

**Purpose:** Generate project map to eliminate exploration token waste.

**Output:** `.shipkit/codebase-index.md`

**Triggers:**
- `/codebase-index` or `/shipkit-codebase-index`
- Session start suggestion if missing
- After major structure changes

**What it captures:**
- npm scripts with descriptions
- Key files and their exports
- Directory structure with purpose annotations
- Architecture notes

**Spec:** `PERSISTENCE-SKILLS-SPEC.md`, `CODEBASE-INDEX-DESIGN.md`

---

## Tier 2: Ecosystem & Workflow (Medium Priority)

### shipkit-extensions

**Purpose:** Post-install manager for MCPs and skills. Browse, compare installed vs available, and install from manifest.

**Output:** Updates to `.mcp.json` and `.claude/skills/`

**Triggers:**
- `/extensions` — Interactive menu
- `/extensions mcps` — Browse MCPs only
- `/extensions skills` — Browse skills only
- `/extensions install <name>` — Install specific extension
- `/extensions budget` — Show token usage

**What it does:**
- Show installed vs available extensions
- Display token cost for MCPs (context budget awareness)
- Install MCPs (update `.mcp.json`)
- Install skills (copy to `.claude/skills/`)
- Check prerequisites before install
- Show post-install instructions

**Key Design:**
- Unified "extensions" concept for both MCPs and skills
- Token budget display helps manage context overhead
- Reads from `shipkit.manifest.json` as source of truth
- Shares manifest with installer (consistent data)

**Spec:** `SHIPKIT-EXTENSIONS-SPEC.md`

---

### shipkit-standards

**Purpose:** Define project-specific quality standards Claude should follow.

**Output:** `.shipkit/standards.md`

**Triggers:**
- `/standards` or `/shipkit-standards`
- When user says "always do X" or "never do Y"

**What it captures:**
- Code quality requirements
- Testing requirements
- Accessibility standards
- Security requirements
- Review checklist

**Spec:** `SHIPKIT-STANDARDS-SPEC.md`

---

### shipkit-checkpoint

**Purpose:** Save state before context overflow for multi-session continuity.

**Output:** `.shipkit/checkpoint.md`

**Triggers:**
- `/checkpoint`
- When context is getting full (if detectable)
- Before ending a long session

**What it captures:**
- Current task and progress
- Completed steps
- Pending steps
- Key decisions made
- Context needed to resume

**Spec:** `SHIPKIT-CHECKPOINT-SPEC.md`

---

## Tier 3: Discipline Enforcement (Lower Priority)

### shipkit-verify

**Purpose:** Enforce verification discipline after implementation.

**Output:** Verification report (no persistent file)

**Triggers:**
- After completing implementation work
- `/verify`
- Phase transition prompts

**What it does:**
- Run tests if they exist
- Check types compile
- Verify build succeeds
- Check against spec if exists
- Report confidence level

**Spec:** `SHIPKIT-VERIFY-SPEC.md`

**Note:** This might be better as instructions added to existing skills rather than a standalone skill. The capability exists (Claude can run tests), it's just discipline.

---

## Not Creating (Discipline Gaps Handled Differently)

These were identified as gaps but don't need dedicated skills:

| Gap | Why No Skill | Solution Instead |
|-----|--------------|------------------|
| Quality checks | Discipline, not capability | Add to existing skill instructions |
| Communication style | Covered by shipkit-preferences | — |
| Verification habit | Discipline | Add phase gates to workflow |
| Efficiency | Covered by shipkit-codebase-index | — |

---

## Implementation Order

### Phase 1: Persistence (Immediate)
1. **shipkit-codebase-index** — ✅ Built
2. **shipkit-teach** — ✅ Built

### Phase 2: Ecosystem (Next)
3. **shipkit-extensions** — Post-install MCP and skill manager
4. **shipkit-standards** — Captures human decisions on quality

### Phase 3: Continuity (Later)
5. **shipkit-checkpoint** — Multi-session task handling
6. **shipkit-verify** — Or fold into existing skills

---

## Relationship to Existing Skills

| New Skill | Complements | Why |
|-----------|-------------|-----|
| shipkit-teach | All skills | Learnings apply everywhere via CLAUDE.md |
| shipkit-codebase-index | shipkit-project-context | Extends context loading |
| shipkit-extensions | shipkit-project-status | Status can recommend extensions |
| shipkit-standards | shipkit-plan, shipkit-spec | Plans/specs should reference standards |
| shipkit-checkpoint | shipkit-work-memory | More detailed session state |
| shipkit-verify | shipkit-plan | Verification after plan execution |

---

## Context Files Summary

Files created/modified by these skills:

| File | Modified By | Purpose |
|------|-------------|---------|
| `CLAUDE.md` | shipkit-teach | Appends to Working Preferences / Project Learnings |
| `<folder>/CLAUDE.md` | shipkit-teach | Folder-specific learnings |
| `.shipkit/codebase-index.json` | shipkit-codebase-index | Project structure map |
| `.shipkit/standards.md` | shipkit-standards | Quality requirements |
| `.shipkit/checkpoint.md` | shipkit-checkpoint | Session state for resume |

---

## Related Documents

### Spec Files (All in `claude-working-documents/`)

| File | Skills Covered |
|------|----------------|
| `SHIPKIT-TEACH-SPEC.md` | shipkit-teach |
| `SHIPKIT-EXTENSIONS-SPEC.md` | shipkit-extensions |
| `SHIPKIT-STANDARDS-SPEC.md` | shipkit-standards |
| `SHIPKIT-CHECKPOINT-SPEC.md` | shipkit-checkpoint |
| `SHIPKIT-VERIFY-SPEC.md` | shipkit-verify |

*Note: `PERSISTENCE-SKILLS-SPEC.md` is deprecated — shipkit-teach replaces preferences + learnings.*

### Analysis & Design

- `CONTEXT-GAPS-INVENTORY.md` — Analysis that identified these gaps
- `CODEBASE-INDEX-DESIGN.md` — Detailed codebase index design
- `CLAUDE-CODE-SKILLS-INTEGRATION.md` — Plugin/marketplace integration
