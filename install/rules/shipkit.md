# Shipkit Framework Rules

<!-- Framework-managed file. Updated via /shipkit-update. Do not edit manually. -->

## Core Rules

1. **Context over defaults** — Check `.shipkit/` before assuming. Project decisions override training defaults.
2. **MVP quality** — Core paths bulletproof, everything else minimal. Ship > perfect.
3. **Stay focused** — Do what's asked. No unsolicited refactoring or "improvements."
4. **Ask before generating** — 2-3 clarifying questions, then build.
5. **Skills for persistence only** — Use skills to capture decisions or create memory. Everything else (implementing, debugging, testing, refactoring), just do it. Skills route by their descriptions — no lookup table needed.
6. **Solo patterns** — No PR workflows, no "future developer" docs, no unnecessary abstraction.
7. **Save before compact** — When you see the PreCompact warning, run `/shipkit-work-memory` to save progress.

---

## Structured Artifact Updates

For updates to structured JSON artifacts (`.shipkit/progress.json`, spec/plan files, any skill-produced JSON, config files), use **targeted Edit calls — never a Python/Node script**. Each field you need to change is one Edit: one for summary fields, one to splice the new entry into an array, one to overwrite a sub-object, etc. The Edit tool handles large JSON files fine.

- **Don't reach for bash heredocs with inline Python** — a classic quoting trap when the Python contains apostrophes in strings. The retreat to "write it as a script file instead" is a sign you started in the wrong place.
- **Only write a script when you need programmatic computation across many files or values** — e.g. batch renames, bulk schema migrations, data aggregation. Splicing one value into one location is not that.
- **Read + Write (overwrite the whole file) is the acceptable fallback** when many fields change at once, but prefer Edit first — it keeps diffs reviewable and doesn't pull the whole file into context.
- Rule of thumb: if you can describe the change as "replace block A with block B," it's an Edit.

---

## Quality Standards

### AI Agent Accessibility
All interactive UI elements must include:
- `data-testid` attribute (naming: `{component}-{action}`, e.g., `login-submit-btn`, `sidebar-nav-link`)
- ARIA roles for custom widgets (`combobox`, `dialog`, `menu`, `tablist`)
- State attributes (`aria-expanded`, `aria-checked`, `aria-selected`, `data-state`)

**Why:** Enables AI-driven QA (Claude in Chrome, Playwright), E2E testing, and accessibility compliance. Without these, AI agents cannot reliably interact with or verify UI elements.

---

## Context Files

All project context lives in `.shipkit/`:

| File | Purpose |
|------|---------|
| `why.json` | Vision, constraints, approach |
| `product-discovery.json` | User needs, personas, journeys |
| `product-definition.json` | Product blueprint (features, patterns, differentiators) |
| `engineering-definition.json` | Engineering blueprint (mechanisms, components) |
| `goals/strategic.json` | Stage, stage implications & gates (S-* criteria) |
| `goals/product.json` | User-outcome success criteria (P-*) |
| `goals/engineering.json` | Technical-performance criteria (E-*) |
| `stack.json` | Tech choices (auto-scanned) |
| `architecture.json` | Decisions log — *why* (**lean** active-decisions index: capped active ADRs + one-line superseded stubs; `@`-imported) |
| `architecture-archive.json` | Full ADR history — complete rationale, alternatives, supersession chains (append-only; **not** `@`-imported; read on demand) |
| `architecture-map.json` | Current-state map — *what-is* (apps, datastores, contracts, integrations; code-derived, refreshable) |
| `progress.json` | Session continuity |
| `codebase-index.json` | Navigation index (concept → files) |
| `specs/active/*.json` | Feature specs |
| `plans/active/*.json` | Implementation plans |

**Always check context before making architectural decisions.**

### When to read what (read-on-demand triggers)

The lean slices below — current **stage + gates** and the **codebase map** — are injected at session start (see Codebase Navigation). The large artefacts are *referenced*: know they exist and read them at the moment of need.

| Before you... | Read |
|---|---|
| implement/modify a feature | its `specs/active/*.json` + `engineering-definition.json` (mechanisms + data contracts — the frontend→backend gap lives here) |
| decide what to build next | `spec-roadmap.json` |
| make a product / UX / scope call | `product-definition.json` (+ `product-discovery.json` for personas/journeys) |
| need an ADR's full rationale, rejected alternatives, or the chain behind a superseded stub | `architecture-archive.json` (the lean `architecture.json` carries only the capped entry / stub) |
| judge whether something is "done" | `goals/strategic.json` gates (lean slice injected at session start) + the spec's acceptance criteria |
| navigate the codebase | the injected Codebase Map digest; `Read .shipkit/codebase-index.json` for per-file detail |

---

## Codebase Navigation

When `.shipkit/codebase-index.json` exists, the session-start hook injects a **lean Codebase Map digest** (concepts → files, entry points, skip globs, with the index's age). Use it before reaching for glob/grep:

1. Use the injected `concepts` map to find feature-related files
2. Use `entryPoints` to find starting points
3. Check `skip` to avoid wasting context on irrelevant files
4. Don't glob or explore if the digest answers the question
5. `Read .shipkit/codebase-index.json` for per-file detail the digest omits (on a large repo the digest is the top concepts + a pointer)

**The Codebase Map digest is injected at session start** (size-capped — not the full file). If the shown index age is stale, re-run `/shipkit-codebase-index`.

---

## Meta-Behavior

**When user asks to remember something** (e.g., "remember this", "save this for next time", "add to CLAUDE.md"):
- Determine type: style/behavior → Working Preferences, technical/pattern → Project Learnings
- Ask scope: project-wide (root) or folder-specific
- Append to appropriate section in CLAUDE.md
- Confirm what was added

**Do NOT auto-suggest** — Don't ask "Should I remember this?" after corrections. Only persist when user explicitly requests it.

**To remove a learning:** User says "remove the learning about X" — edit CLAUDE.md directly.

**If Claude Code auto memory is active** (`~/.claude/projects/<project-hash>/memory/`): keep `MEMORY.md` concise (<200 lines); use it for session-to-session learnings only — project artifacts (specs, plans, architecture) belong in `.shipkit/`.

---

## Sandbox Mode

If sandbox mode is enabled, `.claude/skills/` is write-protected. Shipkit install/update requires either:
- Sandbox disabled during install, or
- `.claude/` added to `sandbox.filesystem.allowWrite`

---

## Parallel sessions & the integration bench (opt-in)

**Skip this entire section unless you run multiple Claude Code sessions concurrently across git worktrees of one repo.** Single-session work: your checkout is your normal workspace — commit, branch, and merge in it freely; none of the below applies.

When you *do* fan out into parallel worktree sessions, designate the **primary checkout as the integration bench**: the one tree where branches get merged and integrated, never worked on directly by a spawned session. A session must first determine whether it is the bench or a linked worktree before running any git command:

```
git rev-parse --git-common-dir    # the shared .git
git rev-parse --git-dir           # this tree's git dir
```
If the two differ (or `git worktree list` shows this directory as a **linked** entry), you are a worktree session, not the bench.

- **Worktree sessions** keep all git work inside their own worktree and branch — commit, rebase, push your own branch freely. **Do not** run git commands that target the bench (no `checkout`/`switch`, `merge`, `reset`, `commit`, branch create/delete, or stash against the primary tree). Concurrent git operations on a shared tree corrupt each other's state.
- **The bench session** (or you, manually) owns integration: pulling and merging the worktree branches together. Spawned sessions hand off finished branches; they don't integrate.
- If you can't tell which you are, **stop and ask** rather than running git against an unknown tree.
