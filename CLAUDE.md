# Shipkit - Framework Development Instructions

**You are developing Shipkit — a streamlined product development framework built on Claude Code.**

This repo contains the Shipkit framework: skills, agents, hooks, and templates that get installed into user projects. All development must align with official Claude Code documentation and patterns.

---

## Repo Model & Audience

**This is a public repo but not open-source-in-the-contributions-sense.** Stefan is the solo developer. The expected audience is **consumers** of the framework — people who install Shipkit into their own projects and use the skills — not contributors. Only a tiny fraction of visitors will ever read the source beyond the README.

**Implications:**
- The public-facing contents must be **consumer-polished**: `install/`, `cli/`, `README`, `CHANGELOG`, `VERSION`, `package.json`, `LICENSE`, `docs/generated/`.
- Dev tooling, drafts, audits, one-off scripts, framework-integrity checks — all **private**. They live in the private repo only. See `.gitignore` and "Branch Strategy" below.
- When deciding whether something belongs in the public repo, ask: *does a consumer benefit from this?* If no, it's private.
- **Not yet on npm**. Install is `npx github:stefan-stepzero/shipkit init -y` (the install command in `install/claude-md/shipkit.md` and README uses this form). Once published to npm, that command simplifies to `npx shipkit init` — update docs then.

---

## Branch Strategy (2 branches, 2 remotes)

**Single source of truth:**
- `origin` → `github.com/stefan-stepzero/shipkit.git` — **the public repo**. Only `origin/main` exists. `origin/main` = the latest consumer release.
- `private` → `github.com/stefan-stepzero/sg-shipkit-private.git` — **the private repo**. Only `private/dev` exists. `private/dev` = active work-in-progress.

**Local branches:**
- `dev` (tracks `private/dev`) — day-to-day work happens here.
- `main` (tracks `origin/main`) — release branch; only exists to fast-forward from `dev` when cutting a public release.

**Release flow:**
```
commit on local dev
    ↓
git push private dev            (in-progress push to private repo)
    ↓
git checkout main
git merge --ff-only dev
    ↓
git push origin main            (public release push)
    ↓
git checkout dev                (return to dev for next work)
```

**Never:**
- Never push anything to `origin` except `origin/main`. No `origin/dev`, no feature branches. If a feature branch shows up on origin, it's dirt — delete it.
- Never let any tool create `claude/*` prefix branches. The 8 `origin/claude/*` branches that existed until 2026-04-15 were residue from **Claude.ai's web app GitHub integration** (the web UI creates one branch per task). Current Claude Code terminal sessions commit directly to `dev` and don't auto-branch. **Do not use the Claude.ai GitHub integration on this repo** — use Claude Code terminal for all work.
- Never force-push to `origin/main` — it's the public release branch. Regular push only.
- Never `git filter-repo` or rewrite public history — breaks anyone's clones. If a sensitive file slips through, deal with it via key rotation / apology, not history rewriting.

**2026-04-15 cleanup** (for reference):
- Deleted `origin/dev`, `private/main`, and 8 `origin/claude/*` branches — all were merged into `origin/main`, all were residue from earlier workflows.
- Switched default branch on private repo from `main` to `dev` (required before deleting `private/main`).
- Before this cleanup, both remotes had a 2×2 grid (origin/main+dev, private/main+dev); after, each remote has exactly one branch.

---

## Public vs Private — What Goes Where

**`.gitignore` rule**: `.claude/` is fully ignored. Dev tooling under `.claude/skills/` (framework-integrity, dev-release, wiring-graph, validate-wiring, scout, analyst, ideator, documenter, smoketest, dev-plan, dev-spec, dev-review, dev-team, dev-team-status, cc-reference) lives on disk locally, is tracked in the **private** repo, but is **never** committed to `origin/main`.

| Path | Tracked in public (`origin/main`)? | Why |
|---|---|---|
| `install/skills/` | **YES** | These are the skills consumers install. |
| `install/agents/` | **YES** | Agent personas the installed skills use. |
| `install/shared/`, `install/settings/`, `install/claude-md/`, `install/profiles/`, `install/rules/` | **YES** | Installer-facing templates. |
| `cli/` | **YES** | The `shipkit init` and `shipkit update` CLI. |
| `README`, `CHANGELOG`, `VERSION`, `package.json`, `LICENSE` | **YES** | Consumer metadata. |
| `docs/generated/` | **YES** | User-facing overview HTML. |
| `.claude/skills/shipkit-*` (dev skills) | **NO** (was YES until 2026-04-15) | Framework-developer power tools. Consumers don't use them. |
| `.claude/specs/` | **NO** | Drafts and design specs for future framework work. |
| `.claude/plans/`, `.claude/agent-memory/`, `.claude/settings.local.json` | **NO** | Local dev state. |
| `docs/development/` | **NO** (via `.gitignore`) | Audit reports, scratch notes, one-off Python scripts. |

**If you're editing a file under `.claude/skills/shipkit-*`**, you can move fast and messy — it's private. If you're editing `install/skills/shipkit-*`, treat every edit as "about to ship to users" — it IS about to ship.

---

## Release Process (Learned Through 2.6.0)

**Before any release:**
1. Run `/shipkit-validate-wiring --static` (dogfoods W-008/W-009 against fresh DOC-025).
2. Run `/shipkit-framework-integrity --quick` (5-parallel-agent audit + installer smoke test).
3. Regenerate DOC-025 if any `install/` file was edited after the last regen: `/shipkit-wiring-graph`.
4. Bump `VERSION` AND `package.json` together (prepublishOnly hook checks they match).
5. Run `node cli/bin/shipkit.js sync-docs` to regenerate skill-count sync markers in README and HTML.
6. Write a CHANGELOG entry under a new version heading with Removed/Fixed/Added/Changed sections.

**Commit and push:**
7. `git add -u` stages all modifications + deletions of tracked files (doesn't pull in gitignored cruft).
8. Explicit `git add` for any new files that aren't gitignored.
9. Commit with a multi-line HEREDOC message that summarizes the release.
10. `git push private dev` → `git checkout main && git merge --ff-only dev` → `git push origin main` → `git checkout dev`.

**Gotcha: `git rm --cached` + `git checkout branch` = local file loss.**
Discovered 2026-04-15: `git rm --cached -r .claude/` removes files from the index but leaves the working tree. However, if you then commit the deletion and **switch branches** (even to a fast-forwarded descendant), git applies the deletion to the working tree. Files go away locally.
**Recovery**: `git checkout {pre-deletion-commit} -- .claude/` restores files to working tree (but re-adds them to the index), then `git reset HEAD -- .claude/` unstages them. Net: files back on disk, still untracked.
**Prevention**: Before switching branches after a `git rm --cached` + commit, back up the affected paths to a temp location outside the repo.

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

1. **Synthesized CC References** — `docs/development/cc-reference/synthesized/`
   - `skills-reference.md`, `agents-reference.md`, `hooks-reference.md`, `settings-reference.md`
   - Merges official docs + DOC-023 empirical tests into practical coding guides
   - **Read the relevant reference file before creating or modifying any skill, agent, or hook**
   - Refresh with `/shipkit-cc-reference` when stale or after CC upgrades
2. **Claude Code GitHub repo** — `https://github.com/anthropics/claude-code`
   - `CHANGELOG.md` — Latest features, tools, and breaking changes
   - Issues — Real-world usage patterns and edge cases
   - Source code — Actual tool definitions and behavior
3. **Official Claude Code docs** — `https://code.claude.com/docs`
4. **CC Primitives Test Report** — `docs/development/cc-reference/DOC-023-pipeline-test-report.md`
   - Empirically confirmed behaviors (15 confirmed facts + 7 architecture rules)
   - Test repo: `P:/Projects2/shipkit-testing/`
   - Don't retest confirmed behaviors unless CC version changes significantly
5. **Local best practices** — `docs/development/`

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
- **11 agents** (4 orchestrators, 4 producers, 3 reviewers) — see `install/agents/`
- **DOC-025 Wiring Graph** — machine-readable dispatch chains, artifact flow, tool restrictions

### Dev Skills (local only, not distributed)
Location: `.claude/skills/`
- Framework integrity, scout, analyst, ideator (intelligence & QA)
- Dev-spec, dev-plan, dev-review, dev-team, dev-release (development workflow)
- Wiring-graph, validate-wiring (contract validation)
- Documenter, smoketest (administration & testing)

### Specs (local only, not distributed)
Location: `.claude/specs/`
- Design specs for new or proposed skills/agents before implementation
- Created by `shipkit-dev-spec` or manually
- Read these before implementing any specced feature

**Pending specs (not yet implemented):**
- `thinking-partner-adversarial.json` — Adversarial debate mode for thinking-partner: 3-5 resource advocate agents debate autonomously, produce tension map + decision matrix
- `ux-pattern-researcher.json` — UX pattern research skill: identify pattern from taxonomy → find orgs with best implementations → browser research with screenshots → analyze UX flow + UI component structure → design recommendations. Taxonomy: `P:/Projects2/sg-dendrite/trees/ux-pattern-taxonomy/tree.json` (177 patterns, 9 cognitive-task categories)
- `gtm-strategy.json` — Go-to-market strategy skill: positioning, segments, pricing model, content strategy, trust signals, channels, launch plan → outputs `.shipkit/gtm-strategy.json` for downstream skills
- `website-blueprint.json` — Website blueprint skill: page inventory, section-by-section specs with UX patterns, conversion flows, SEO map, trust architecture, content requirements → outputs `.shipkit/website-blueprint.json`. Consumes GTM strategy
- `engineering-definition-ecosystem-defaults.json` — Add ecosystem-aware defaults to engineering-definition: Step 2b (Ecosystem Audit), stack-specific reference files (python-llm, python-api, nextjs-fullstack, react-spa), mechanism-standards.md mapping common mechanisms to standard solutions. Prevents reinventing the wheel.

**Known interim state (2026-04-18):**
- `return-prompt-resume.json` — rollout paused pending orchestrator-bubble integration tests (T7/T8/T9). Interim: 5 elicitive skills (why-project, stage, product-goals, engineering-goals, feedback-bug) flipped from `context: fork` to inline to prevent silent hallucination. Direction loop now halts for user input instead of running fully autonomous. Planning and shipping loops unaffected.

### Testing & Feedback (external repos)
- **Crypto test harness**: `P:/Projects2/shipkit-testing/` — 23 skills, 10 agents, SHA-256 hash chain tests
- **Lite test project**: `P:/Projects2/sg-shipkit-testing/` — Shipkit Lite installation for integration testing
- **Feedback channel**: `P:/Projects2/sg-shipkit-testing/feedback/` — test-results.md, issues.md, suggestions.md
  - Read feedback after test runs to identify skill/agent bugs and prioritize fixes

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
