# Shipkit Lite - Framework Development Instructions

**You are developing Shipkit Lite — a streamlined product development framework built on Claude Code.**

This repo contains the Shipkit Lite framework: skills, agents, hooks, and constitutions that get installed into user projects. All development must align with official Claude Code documentation and patterns.

---

## 1. What is Shipkit Lite?

**Shipkit Lite = Claude Code + Structured Product Workflow**

| Claude Code Provides | Shipkit Lite Adds |
|---------------------|-------------------|
| Skills system (slash commands) | 19 pre-built lite skills |
| Agent personas (subagent contexts) | 6 specialized lite agents |
| MCP servers | Constitution templates |
| Hooks system | Session & routing hooks |
| Settings & Permissions | Unified workspace structure (`.shipkit-lite/`) |

### The Layer Principle
- ✅ Create skills that work **with** Claude Code primitives
- ✅ Provide agent personas Claude Code loads
- ❌ Never modify Claude Code itself or bypass its features
- ❌ Never create parallel systems

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

**This principle is non-negotiable. Every skill in Shipkit Lite must pass this test.**

---

## 3. Framework Development Approach

**These are the explicit decisions about how we build Shipkit Lite itself.**

### Technical Approach
- **Skill format:** Follow Claude Code skill spec exactly — check `claude-code-best-practices/` before assuming syntax
- **File structure:** All lite skills in `install/skills/`, agents in `install/agents/`
- **Naming:** All skills use `lite-` prefix
- **Integration:** 7-file system (manifest, hooks, routing, etc.) — see `BUILDING-LITE-SKILLS.md`

### Quality Trade-offs
- **Correctness over speed:** Verify against Claude Code docs before implementing
- **Clarity over cleverness:** Skills should be readable and maintainable
- **Coverage assurance:** Every development action maps to a skill OR a declared natural capability (MECE)

### Dependency Philosophy
- **Minimal external deps:** Skills should work with Claude Code primitives only
- **No parallel systems:** Don't recreate what Claude Code already provides

### When to Update This Approach
- When Claude Code updates its skill/agent spec
- When a pattern emerges that should be standardized
- When you find yourself repeatedly correcting Claude's assumptions about how to build skills

---

## 4. Development Workflow

### Before Implementing ANY Feature

1. **Check official Claude Code docs:** `https://docs.anthropic.com/claude/docs/claude-code`
2. **Check local best practices:** `claude-code-best-practices/`
3. **Primary reference:** `claude-code-best-practices/REFERENCES-BEST-PRACTICES.md` — read this FIRST
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
- `claude-code-best-practices/LITE-7-FILE-INTEGRATION.md` — 7-file integration system
- `claude-code-best-practices/SKILL-QUALITY-AND-PATTERNS.md` — Quality standards

Production-ready = Integration (7 files) + Quality. DO NOT skip quality standards.

---

## 5. Skill Authoring Guidelines

### The Specificity-Flexibility Trade-off

| More Specific | More Flexible |
|---------------|---------------|
| Better format consistency | Better edge case handling |
| More predictable output | More adaptable to context |

### Principles

1. **Be specific about structure, flexible about content**
   - ✅ "Output as markdown table with columns: X, Y, Z"
   - ❌ "Output like this example: [detailed example]"

2. **Constraints should enable, not restrict**
   - ✅ "Ask 2-3 clarifying questions before generating"
   - ❌ "Ask these exact questions: [list]"

3. **Prefer principles over prescriptions**
   - ✅ "Ensure the spec is implementation-agnostic"
   - ❌ "Never mention React, Vue, or Angular in specs"

4. **Test edge cases** — Does the skill work for CLI, mobile, API?

5. **Context over defaults** — Claude has implicit defaults that may conflict with project context

**Warning:** Examples bias output toward their format AND content. Use them sparingly, for format only.

### Context Over Defaults

Claude has **implicit defaults** for how to do things — preferences baked in from training. These aren't wrong, but they're **context-blind**.

| Claude's Default | But Context Might Say |
|------------------|----------------------|
| Modular architecture | Monolithic for MVP speed |
| TypeScript strict mode | JavaScript for quick prototype |
| Comprehensive error handling | Happy path only for POC |
| Full test coverage | No tests for throwaway code |
| Component-based UI | Simple HTML for internal tool |

**The Problem:** Claude applies defaults even when project context suggests otherwise.

**The Solution:**
1. **Skills capture context** — `.shipkit-lite/` files record explicit decisions (why.md, architecture.md, stack.md)
2. **Skills check context first** — Before assuming an approach, read what's been decided
3. **Decisions override defaults** — If architecture.md says "monolithic for MVP", that wins

**Skills should:**
- ✅ Read context files before making architectural assumptions
- ✅ Ask clarifying questions if context is missing
- ✅ Respect explicit decisions even if they differ from "best practice"
- ❌ Never assume "industry standard" when project context exists
- ❌ Never override user decisions with training defaults

**Example in Practice:**
```
User: "Let's build the dashboard"

Claude WITHOUT context: "I'll create separate components for each widget,
with a shared state management layer using Context API..."

Claude WITH context (reads why.md: "MVP in 2 weeks, solo developer"):
"Given your MVP timeline and solo dev context, I'll keep this simple —
one Dashboard component with inline state. We can modularize later."
```

This is why `.shipkit-lite/` files exist — they're not documentation, they're **decision persistence** that overrides Claude's defaults.

---

## 6. Tactical Rules

### File Operations

Use the simplest available tool:
1. **Read** the file
2. **Write** the file with new content
3. Done.

❌ Don't use complex bash heredocs, Python scripts, or temp files for simple edits.
✅ Bash IS appropriate for git, tests, builds, system operations.

**If you catch yourself writing complex bash for a simple file edit, STOP and use Read + Write instead.**

### Working Documents

**Location:** Always create in `claude-working-documents/`

**Naming:** UPPERCASE-WITH-HYPHENS.md (e.g., `MIGRATION-STATUS.md`, `SKILL-RESTRUCTURE-PLAN.md`)

**Use for:** Implementation progress, migration plans, architecture decisions, task breakdowns

**Don't use for:** Scratch notes, single-session todos, user-facing docs, code files, product artifacts (those go in `.shipkit-lite/`)

**Always check `claude-working-documents/` FIRST when:**
- User references a "plan" or "status document"
- Resuming work from a previous session
- User asks "what's the status of X"

---

## Appendix: Active Components

### Lite Skills (19 total)
Location: `install/skills/`

**Core Workflow:** `lite-shipkit-master`, `lite-project-status`, `lite-project-context`

**Discovery & Planning:** `lite-product-discovery`, `lite-why-project`, `lite-spec`, `lite-plan`, `lite-prototyping`, `lite-prototype-to-spec`

**Implementation:** `lite-architecture-memory`, `lite-data-contracts`, `lite-component-knowledge`, `lite-route-knowledge`, `lite-integration-docs`

**Quality & Documentation:** `lite-ux-audit`, `lite-user-instructions`, `lite-communications`, `lite-work-memory`

**System:** `lite-detect` (auto-triggered)

### Lite Agents (6 total)
Location: `install/agents/`

`lite-product-owner-agent`, `lite-ux-designer-agent`, `lite-architect-agent`, `lite-implementer-agent`, `lite-reviewer-agent`, `lite-researcher-agent`

### Configuration Files
- `install/profiles/lite.manifest.json` — Skill/agent manifest
- `install/settings/lite.settings.json` — Permissions and configuration
- `install/claude-md/lite.md` — Project instructions (installed into user projects)
- `install/shared/hooks/lite-session-start.py` — Session initialization
- `install/shared/hooks/lite-after-skill-router.py` — Auto-detection routing

### Reference Materials
- `claude-code-best-practices/REFERENCES-BEST-PRACTICES.md` — PRIMARY REFERENCE
- `claude-code-best-practices/SKILL-QUALITY-AND-PATTERNS.md` — Quality standards
- `claude-code-best-practices/LITE-7-FILE-INTEGRATION.md` — Integration system
- `claude-code-best-practices/LITE-DESIGN-PHILOSOPHY.md` — Lite philosophy
