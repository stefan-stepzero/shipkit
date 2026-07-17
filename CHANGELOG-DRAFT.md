# context-diet lane — CHANGELOG entry draft

For the bench to fold into `CHANGELOG.md` under the next release version (after 2.13.0 / success-harness) at rebase+land time, then delete this file.

### Added
- **`shipkit-adr` skill** (39 → 40 skills) — lands one architecture decision atomically at the moment it's made: full entry appended to `architecture-archive.json` first, then a hard-capped lean projection into the `@`-imported `architecture.json` (decision ≤ 120 chars, one-line rationale ≤ 160 chars, superseded entries collapse to one-line stubs). Handles new / supersede / amend per the canonical dual-write convention; ID allocation scans both files so an interrupted write self-heals.
- **Size budgets on always-loaded artifacts** — the session-start hook now measures sizes alongside ages: per-file byte budgets for `CLAUDE.md` and the three `@`-imported `.shipkit` artifacts, a loud over-budget warning with per-file remediation (silent when within budget), and a Size column in the Available Context table.

### Changed
- **Session-start hook injects a 3-line engine pointer instead of the full `shipkit-orchestrate` body** (~1700 tokens saved per session in every activated project). Hooks inject state, not instructions — the engine's protocol loads on invocation.
- **`install/rules/shipkit.md` roughly halved** (276 → 131 lines) for every consumer project: Skills Reference tables deleted (skill frontmatter descriptions are the single routing surface), generic-hygiene boilerplate cut (Working Smart, Model Budget, session-continuity/enterprise notes), Auto Memory collapsed to a conditional two-liner under Meta-Behavior.

### Notes (not for changelog)
- E5 (hide worker/reviewer skills) closed as **verified, no change**: all three internal-only skills (`shipkit-resource-advocate`, `shipkit-review-direction`, `shipkit-review-planning`) already carry `user-invocable: false`. Optional deepening (settings `skillOverrides: "name-only"` to drop their descriptions from the model listing) is documented in CC but untested in DOC-023 — deferred.
- Bench follow-ups: DOC-025's frontmatter layer is stale (`userInvocable: true` for all 39 incl. the three hidden ones) — regen at release gate; the "31 user-invocable + 8 infrastructure" count in the repo CLAUDE.md appendix doesn't match ground truth (36 + 3, now 37 + 3); `architecture-log-schema.md`'s referrer list should gain `shipkit-adr` after success-harness lands (file is success-harness-owned right now, so deferred to rebase).
- Rebase caution: E1/E4 touch `install/shared/hooks/shipkit-session-start.py` and release metadata also modified by success-harness — land this lane after it.
