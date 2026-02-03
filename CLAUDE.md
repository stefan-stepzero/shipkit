# Shipkit - Framework Development Instructions

**You are developing Shipkit — a streamlined product development framework built on Claude Code.**

This repo contains the Shipkit framework: skills, agents, hooks, and templates that get installed into user projects. All development must align with official Claude Code documentation and patterns.

---

## Naming Conventions

**Use these names consistently throughout the codebase:**

| Concept | Name | Notes |
|---------|------|-------|
| Framework name | **Shipkit** | One word, capital S and K |
| Context folder | **`.shipkit/`** | Lowercase |
| Skills prefix | **`shipkit-`** | Namespaced to avoid conflicts |
| Installed CLAUDE.md | `install/claude-md/shipkit.md` | Template for user projects |

---

## 1. What is Shipkit?

**Shipkit = Claude Code + Structured Product Workflow**

| Claude Code Provides | Shipkit Adds |
|---------------------|---------------|
| Skills system (slash commands) | Pre-built shipkit skills |
| Agent personas (subagent contexts) | Specialized shipkit agents |
| MCP servers | Context file templates |
| Hooks system | Session & routing hooks |
| Settings & Permissions | Unified workspace structure (`.shipkit/`) |

### The Layer Principle
- Create skills that work **with** Claude Code primitives
- Provide agent personas Claude Code loads
- Never modify Claude Code itself or bypass its features
- Never create parallel systems

**We build ON TOP of Claude Code, not alongside it.**

---

## 2. Why Skills Exist (The Fundamental Rule)

**Claude is trained on human coding patterns but lacks memory and session continuity.**

| Human Coder | Claude |
|-------------|--------|
| Remembers yesterday | Each session starts fresh |
| Knows project history | Only sees what's loaded |
| Picks up where they left off | Requires explicit handoff artifacts |

### The Skill Value Test

A skill is **valuable** if it does one of these:
1. **Forces human decisions to be explicit** — Vision, trade-offs, priorities, domain knowledge
2. **Creates persistence Claude lacks** — Institutional memory that survives sessions

A skill is **redundant** if Claude does it well without instruction (debugging, implementing, documenting code, writing tests).

**Litmus test:** *"If I just asked Claude to do this without a skill, would it work?"*
- YES → Don't create the skill
- NO (requires human input or persistence) → Create the skill

### Quick Reference

| Needs a Skill | No Skill Needed |
|---------------|-----------------|
| Define user personas | Debug this error |
| Document architecture decisions | Implement the login feature |
| Define technology stack | Write unit tests |
| Create feature specification | Refactor this code |
| Capture project approach | Communicating with user |

**This principle is non-negotiable. Every skill in Shipkit must pass this test.**

---

## 3. Framework Development Approach

### Technical Approach
- **Skill format:** Follow Claude Code skill spec exactly — check `claude-code-best-practices/` before assuming syntax
- **File structure:** All skills in `install/skills/`, agents in `install/agents/`
- **Naming:** All skills use `shipkit-` prefix
- **Integration:** 7-file system (manifest, hooks, routing, etc.) — see `BUILDING-LITE-SKILLS.md`

### Quality Trade-offs
- **Correctness over speed:** Verify against Claude Code docs before implementing
- **Clarity over cleverness:** Skills should be readable and maintainable
- **Coverage assurance:** Every development action maps to a skill OR a declared natural capability (MECE)

### Dependency Philosophy
- **Minimal external deps:** Skills should work with Claude Code primitives only
- **No parallel systems:** Don't recreate what Claude Code already provides

---

## 4. Development Workflow

### Before Implementing ANY Feature

1. **Check official Claude Code docs:** `https://docs.anthropic.com/claude/docs/claude-code`
2. **Check local best practices:** `docs/development/`
3. **Primary reference:** `docs/development/REFERENCES-BEST-PRACTICES.md` — read this FIRST
4. Verify skills syntax matches current spec
5. Ensure agent persona format is correct
6. Validate hook patterns are supported

**When uncertain about Claude Code features:**
- Don't guess or assume
- Check the documentation
- Test in a real Claude Code environment
- Ask the user if documentation is unclear

### When Creating or Editing Lite Skills

**Required reading:**
- `docs/development/SHIPKIT-7-FILE-INTEGRATION.md` — 7-file integration system
- `docs/development/SKILL-QUALITY-AND-PATTERNS.md` — Quality standards

Production-ready = Integration (7 files) + Quality. DO NOT skip quality standards.

---

## 5. Skill Authoring Guidelines

### Principles

1. **Be specific about structure, flexible about content**
   - "Output as markdown table with columns: X, Y, Z"
   - Not: "Output like this example: [detailed example]"

2. **Constraints should enable, not restrict**
   - "Ask 2-3 clarifying questions before generating"
   - Not: "Ask these exact questions: [list]"

3. **Prefer principles over prescriptions**
   - "Ensure the spec is implementation-agnostic"
   - Not: "Never mention React, Vue, or Angular in specs"

4. **Test edge cases** — Does the skill work for CLI, mobile, API?

5. **Context over defaults** — Claude has implicit defaults that may conflict with project context

**Warning:** Examples bias output toward their format AND content. Use them sparingly, for format only.

### Context Over Defaults

Claude has **implicit defaults** from training. These aren't wrong, but they're **context-blind**.

| Claude's Default | But Context Might Say |
|------------------|----------------------|
| Modular architecture | Monolithic for MVP speed |
| TypeScript strict mode | JavaScript for quick prototype |
| Comprehensive error handling | Happy path only for POC |
| Full test coverage | No tests for throwaway code |

**The Solution:**
1. **Skills capture context** — `.shipkit/` files record explicit decisions
2. **Skills check context first** — Before assuming, read what's been decided
3. **Decisions override defaults** — If architecture.md says "monolithic for MVP", that wins

---

## 6. Tactical Rules

### File Operations

Use the simplest available tool:
1. **Read** the file
2. **Write** the file with new content
3. Done.

Don't use complex bash heredocs, Python scripts, or temp files for simple edits.
Bash IS appropriate for git, tests, builds, system operations.

### Working Documents

**Location:** Always create in `dev/`

**Naming:** UPPERCASE-WITH-HYPHENS.md (e.g., `MIGRATION-STATUS.md`, `SKILL-RESTRUCTURE-PLAN.md`)

**Use for:** Implementation progress, migration plans, architecture decisions, task breakdowns

**Don't use for:** Scratch notes, single-session todos, user-facing docs, code files, product artifacts (those go in `.shipkit/`)

---

## Appendix: Active Components

### Skills
Location: `install/skills/`

**Core Workflow:** `shipkit-master`, `shipkit-project-status`, `shipkit-project-context`, `shipkit-codebase-index`, `shipkit-claude-md`

**Discovery & Planning:** `shipkit-product-discovery`, `shipkit-why-project`, `shipkit-spec`, `shipkit-plan`, `shipkit-prototyping`, `shipkit-prototype-to-spec`

**Implementation:** `shipkit-architecture-memory`, `shipkit-data-contracts`, `shipkit-integration-docs`

**Quality & Documentation:** `shipkit-verify`, `shipkit-preflight`, `shipkit-ux-audit`, `shipkit-user-instructions`, `shipkit-communications`, `shipkit-work-memory`

**Ecosystem:** `shipkit-get-skills`, `shipkit-get-mcps`

**System:** `shipkit-detect` (auto-triggered), `shipkit-update`

**Total:** 24 skills

### Agents
Location: `install/agents/`

`shipkit-product-owner-agent`, `shipkit-ux-designer-agent`, `shipkit-architect-agent`, `shipkit-implementer-agent`, `shipkit-reviewer-agent`, `shipkit-researcher-agent`

### Configuration Files
- `install/settings/shipkit.settings.json` — Permissions and configuration
- `install/claude-md/shipkit.md` — Project instructions (installed into user projects)
- `install/shared/hooks/shipkit-session-start.py` — Session initialization
- `install/shared/hooks/shipkit-after-skill-router.py` — Auto-detection routing

### Reference Materials
- `docs/development/REFERENCES-BEST-PRACTICES.md` — PRIMARY REFERENCE
- `docs/development/SKILL-QUALITY-AND-PATTERNS.md` — Quality standards
- `docs/development/SHIPKIT-7-FILE-INTEGRATION.md` — Integration system
- `docs/development/SHIPKIT-DESIGN-PHILOSOPHY.md` — Design philosophy
