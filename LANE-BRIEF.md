# Lane: context-diet

**Branch:** `context-diet` · **Base:** `dev@18ab39c` · **Claimed:** 2026-07-17
**Theme:** Context-efficiency root-cause fixes for always-loaded artifact bloat. Target: next release after 2.13.0 (success-harness has 2.13.0 staged).

## Work items

### E1 — Size budgets on always-loaded artifacts (root-cause fix 1)
`install/shared/hooks/shipkit-session-start.py` already measures artifact **ages**; extend it to measure **sizes** and emit a loud over-budget warning when an always-loaded artifact exceeds its budget. Enforcement lives in the hook, at session start, where the cost is actually paid.

### E2 — `shipkit-adr` skill: land decisions atomically (root-cause fix 2)
New skill that performs the full decision-landing transaction in one move:
1. update the invariant (with a **hard length cap**),
2. append to the lean index,
3. mirror to archive.
Enforcement at the moment of temptation — the moment a decision is being recorded is when bloat gets appended. Full 7-file integration (manifest, README count/list, HTML overview, claude-md table if user-invocable).

### E3 — Deduplicate `install/rules/shipkit.md`
- Delete the Skills Reference tables — skill frontmatter descriptions are the **single routing surface**.
- Cut generic-hygiene boilerplate.
- Make the Auto Memory section conditional.
Goal: roughly halve the file for every consumer project.

### E4 — Session-start hook injects a pointer, not a body
Replace the full shipkit-master body injection with a 3-line pointer. Principle: **hooks inject state, not instructions.**

### E5 — Hide worker/reviewer skills from the main listing *(unverified — gated)*
Check the CC authoring playbook (`~/.claude/cc-authoring-playbook.md` + `~/.claude/cc-authoring-reference.md`, and `docs/development/cc-reference/synthesized/skills-reference.md` on the bench) for a supported mechanism to hide skills from the main listing. **If no mechanism exists, this item dies** — do not invent a parallel system.

## Integration constraints
- **Land AFTER `success-harness`, rebase over it.** That lane already modified `install/shared/hooks/shipkit-session-start.py`, `install/claude-md/shipkit.md`, and the release metadata (VERSION/package.json/README/CHANGELOG). E1/E4 edit the same hook — do the hook work against success-harness's version at rebase time, or expect conflicts.
- `fidelity-measure` is disjoint (tools/fidelity/) — no coordination needed.
- Bench integrates; this lane never merges to dev itself. Ledger: `~/.claude-integration/sg-shipkit.md`, append with `>>` only.

## Repo-local gotchas
- `.claude/` and `docs/development/` are gitignored → this worktree does **not** have the dev skills or DOC-015/DOC-025. Read those from the bench checkout (`P:/Projects2/sg-shipkit/...`) read-only.
- Read `docs/development/cc-reference/synthesized/hooks-reference.md` (bench) before touching the session-start hook; `skills-reference.md` before authoring shipkit-adr.
- Every `install/` edit ships to consumers — consumer-polish bar applies.
- Commit-per-item to this branch (recoverable partials; bench reconciles against `git log dev..context-diet`).
