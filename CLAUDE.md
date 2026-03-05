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
| Framework rules | `install/rules/shipkit.md` | Auto-loaded, managed by /shipkit-update |
| User CLAUDE.md | `install/claude-md/shipkit.md` | User-editable template (preferences, learnings) |

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
- **Skill format:** Follow Claude Code skill spec exactly — check GitHub repo before assuming syntax
- **File structure:** All skills in `install/skills/`, agents in `install/agents/`
- **Naming:** All skills use `shipkit-` prefix
- **Integration:** 7-file system (manifest, hooks, routing, etc.) — see `docs/development/integration/7-file-integration.md`

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

**Primary sources of truth (in order):**

1. **Claude Code GitHub repo** — `https://github.com/anthropics/claude-code`
   - `CHANGELOG.md` — Latest features, tools, and breaking changes
   - Issues — Real-world usage patterns and edge cases
   - Source code — Actual tool definitions and behavior
2. **Official Claude Code docs** — `https://code.claude.com/docs`
3. **CC Primitives Test Report** — `docs/development/cc-reference/DOC-023-pipeline-test-report.md`
   - Empirically confirmed behaviors (15 confirmed facts + 7 architecture rules)
   - Test repo: `P:/Projects2/shipkit-testing/`
   - Don't retest confirmed behaviors unless CC version changes significantly
4. **Local best practices** — `docs/development/`

**Why GitHub first?** Claude Code evolves rapidly. The CHANGELOG and source code are always current. Third-party articles and even official docs can lag behind. When researching a feature (like Tasks, subagents, hooks), check the repo first.

**Example workflow for understanding a new feature:**
```
1. Search CHANGELOG.md for feature introduction
2. Search GitHub Issues for usage patterns and gotchas
3. Check official docs for conceptual overview
4. Test in a real Claude Code environment
```

**When uncertain about Claude Code features:**
- Don't guess or assume from training data
- Check the GitHub repo CHANGELOG first
- Verify with official docs
- Test in a real Claude Code environment
- Ask the user if documentation is unclear

### When Creating or Editing Skills

**Required reading:**
- `docs/development/integration/7-file-integration.md` — 7-file integration system
- `docs/development/quality-standards/skill-quality-and-patterns.md` — Quality standards

Production-ready = Integration (7 files) + Quality. DO NOT skip quality standards.

**When adding a new skill, update:**
1. `install/profiles/shipkit.manifest.json` — Add skill entry
2. `README.md` — Update skill count and list
3. `docs/generated/shipkit-overview.html` — Update skill count and add to list
4. `install/claude-md/shipkit.md` — Add to skill reference table if user-invocable

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
3. **Decisions override defaults** — If architecture.json says "monolithic for MVP", that wins

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

**Location:** `docs/development/` — managed by the documentation manifest (`docs/development/manifest.json`)

**Use `shipkit-documenter`** to create and register new documents in the appropriate category (system-design, cc-reference, quality-standards, integration, dev-progress, inspiration, archive).

**Don't use for:** Scratch notes, single-session todos, user-facing docs, code files, product artifacts (those go in `.shipkit/`)

### Subagent Models

When using the Task tool, default to `model: haiku` for Explore agents and straightforward search/audit tasks. Only use sonnet or opus for subagents that require deeper reasoning or complex analysis.

### Using Claude Code's Task System

For complex multi-step framework development (migrations, multi-file refactors, release prep), use Claude Code's native Task tools:

- **TaskCreate** — Create tasks with subject, description, activeForm (spinner text)
- **TaskUpdate** — Update status, set dependencies with `addBlockedBy`
- **TaskList** — View all tasks with status
- **TaskGet** — Get full task details

Tasks persist across context compaction and can be shared across sessions with `CLAUDE_CODE_TASK_LIST_ID` env var.

### Release Checklist

Before publishing changes to GitHub:

1. **Update `VERSION` + `package.json`** — Bump version in both (must match)
2. **Update .gitignore** — Ensure internal files are excluded
3. **Remove deprecated files** — `git rm --cached` for files that should no longer be tracked
4. **Update skill counts** — README.md, HTML help, manifest
5. **Update repo URLs** — Check skills reference correct GitHub repo
6. **Verify no secrets** — Search for API keys, tokens, credentials
7. **Test installation** — Run `node cli/bin/shipkit.js init -y --target /tmp/test` in a fresh directory

---

## Appendix: Active Components

**Read DOC-015 (`docs/development/system-design/DOC-015-orchestration-pipeline.json`) before modifying agents, skills, or the orchestration pipeline.** It is the single source of truth for the 3-loop architecture, agent taxonomy, skill types, naming conventions, and artifact flow.

### Quick Reference
- **37 skills** (27 user-invocable + 10 infrastructure) — see `install/profiles/shipkit.manifest.json`
- **12 agents** (4 orchestrators, 5 producers, 3 reviewers) — see `install/agents/`
- **DOC-025 Wiring Graph** — machine-readable dispatch chains, artifact flow, tool restrictions

### Dev Skills (local only, not distributed)
Location: `.claude/skills/`
- Framework integrity, scout, analyst, ideator (intelligence & QA)
- Dev-spec, dev-plan, dev-review, dev-team, dev-release (development workflow)
- Wiring-graph, validate-wiring (contract validation)
- Documenter, smoketest (administration & testing)

### Configuration Files
- `install/settings/shipkit.settings.json` — Permissions and configuration
- `install/claude-md/shipkit.md` — Project instructions (installed into user projects)
- `install/shared/hooks/shipkit-session-start.py` — Context loader (progress resume, available files, version check)
- `install/shared/hooks/shipkit-track-skill-usage.py` — Skill usage tracking
- `install/shared/hooks/shipkit-task-completed-hook.py` — Task completion quality gate
- `install/shared/hooks/shipkit-teammate-idle-hook.py` — Teammate idle quality gate

### Reference Materials (Local Only - Gitignored)
- `docs/development/system-design/DOC-015-orchestration-pipeline.json` — **ORCHESTRATION PIPELINE** (3-loop architecture, 12-agent taxonomy, skill types, naming conventions, artifact flow, verification checklist — the single source of truth. Absorbs former DOC-024.)
- `docs/development/cc-reference/DOC-023-pipeline-test-report.md` — **CC PRIMITIVES TEST REPORT** (15 confirmed behaviors, 7 architecture rules — read before designing agent/skill interactions)
- `docs/development/quality-standards/references-best-practices.md` — PRIMARY REFERENCE
- `docs/development/quality-standards/skill-quality-and-patterns.md` — Quality standards
- `docs/development/integration/7-file-integration.md` — Integration system
- `docs/development/system-design/design-philosophy.md` — Design philosophy
- `docs/development/cc-reference/agent-teams-best-practices.md` — Agent teams patterns
- `docs/development/cc-reference/agent-teams-primitives.md` — Agent teams tool reference
- `docs/development/inspiration/obra-repo/` — Reference patterns from obra
- `docs/development/inspiration/speckit/` — Reference patterns from speckit

**Note:** These files are gitignored and only available locally for framework development. They are not distributed with the public repo.
