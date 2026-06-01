# Changelog

All notable changes to Shipkit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

---

## [2.8.0] - 2026-06-01

Hook-system release. Expands the installed hook set from 4 to 12 active hooks, **fixes a latent installer bug where `/shipkit-update` silently delivered only 4 of the 12 hooks**, and adds Windows shell parity. All hook output schemas were verified field-by-field against the CC 2.1.156 hooks reference and official docs before release.

### Fixed
- **`/shipkit-update` delivered only 4 of 12 hooks (latent install bug).** `cli/src/update.js` listed just the original four hooks (`session-start`, `track-skill-usage`, `task-completed`, `teammate-idle`), so existing users who ran `/shipkit-update` never received the other eight — `post-compact`, `session-end`, `subagent-context`, `diagnostics`, `prereq-check`, `pre-compact`, `task-created`, `permission-denied`. Updating to 2.8.0 now installs the full set. **Existing users gain eight previously-undelivered hooks.**
- **Windows: task-completed quality gate falsely blocked every shipping task.** The gate spawned `["npm", "run", "build"]` without a shell; on Windows the package-manager front-ends are `.cmd` shims that `CreateProcess` can't launch directly, so the subprocess raised `FileNotFoundError` and the hook scored it as a failed build — blocking completion of every shipping-agent task in team mode. `run_command` now resolves the executable via `shutil.which` and routes `.cmd`/`.bat` shims through the command processor. POSIX behaviour is unchanged.

### Added
- **Three new hooks:**
  - `shipkit-pre-compact.py` (PreCompact) — snapshots `.shipkit/orchestration.json` to a timestamped checkpoint before compaction so the pipeline can recover lost in-context state. Observability only; never blocks.
  - `shipkit-task-created-hook.py` (TaskCreated) — minimal legibility gate that rejects tasks with an empty title. Description is validated only when the event payload actually carries one (the standard TaskCreated event does not include a description).
  - `shipkit-permission-denied-hook.py` (PermissionDenied) — surfaces auto-mode tool denials with a remediation message (add the permission, or run `/shipkit-update`), and signals `retry: true` only for known-safe read-only denials.
- **Dynamic session title + skill reload on session start.** `shipkit-session-start.py` now emits `reloadSkills` (so hook-installed skills are live from the first prompt) and a `sessionTitle` of `Shipkit — {project} ({N} artifacts)`.
- **PowerShell permission surface.** `shipkit.settings.json` mirrors the Bash command allow-list with `PowerShell(...)` rules for Windows environments.
- **`skillOverrides` (`name-only`)** for the six orchestration/review skills (`shipkit-master`, `orch-direction/planning/shipping`, `review-direction/planning`) — they list by name without their full descriptions to conserve context budget.
- **`/reload-skills` step** in the `shipkit-update` post-install guidance (CC 2.1.152+), so newly installed skills activate without restarting the session.
- **Read-only tool locks** on `shipkit-ux-audit` (`disallowed-tools: Write, Edit, Bash, Agent, Task, WebFetch`) and `shipkit-thinking-partner` (`disallowed-tools: Write, Edit, Bash, Agent, Task`) — both are analysis/advisory skills that should never mutate the workspace.

### Changed
- **task-completed block mechanism: `exit 2` → `exit 0` + `{"decision":"block","reason":...}`.** TaskCompleted parses stdout JSON only at exit 0, so the top-level `decision:"block"` form guarantees the rejection reason is fed back to Claude rather than discarded.
- **Rules: `/code-review` guidance** added alongside `/simplify` in `install/rules/shipkit.md` — `/simplify` for cleanup, `/code-review` for correctness bugs, `/shipkit-review-shipping` for spec-aligned review.
- **Skill description trims** across eight skills (`design-system`, `engineering-definition`, `engineering-goals`, `qa-visual`, `semantic-qa`, `thinking-partner`, `update`, `ux-audit`) for context economy; behaviour unchanged.

---

## [2.7.1] - 2026-05-27

Patch release. Removes the buggy `context-check` UserPromptSubmit hook, and adds intellectual-posture + structured-artifact guidance to the installed CLAUDE.md template and framework rules.

### Removed
- **`shipkit-context-check.py` UserPromptSubmit hook** — Misfired with false positives ("missing key context: why.json, stack.json, ...") on projects where those files were present and populated. Root cause: the hook resolved `project_root` by walking up from `hook_input['cwd']` and short-circuiting on the first dir with either `.claude/` or `.shipkit/`, which under cwd-drift conditions resolved to the wrong root. The functionality was also redundant with the SessionStart hook's "Available Context" table, which already surfaces missing-file status without per-prompt nagging. Removed the script, the `UserPromptSubmit` entry in `shipkit.settings.json`, and the corresponding entry in `cli/src/init.js`. A stale comment in `shipkit-prereq-check.py` referencing the deleted hook was updated.

### Added
- **`install/claude-md/shipkit.md` — "How to engage with me" section** — Five intellectual-posture rules (communication style, disagreement posture, confidence calibration, use-the-method-not-the-eyeball, always-consider-the-alternate) plus a Challenge Calibration block for when to steelman vs execute. Installs into the user CLAUDE.md template so new Shipkit projects start with these defaults.
- **`install/rules/shipkit.md` — "Structured Artifact Updates" guidance** — Directs Claude to use targeted Edit calls (not Python/Node heredocs) when modifying `.shipkit/progress.json`, spec/plan files, and other structured JSON artifacts. Closes a recurring failure mode where agents reached for inline-Python and tripped over quoting.

---

## [2.7.0] - 2026-04-18

Interim reliability release. Fixes silent hallucination in forked elicitive skills by flipping them to inline execution, and sharpens the "After Completion" guidance across 8 skills so it reflects the actual orchestration flow instead of the older user-facing "decide next steps" prose.

### Fixed
- **Silent hallucination in 5 elicitive skills** — `shipkit-why-project`, `shipkit-stage`, `shipkit-product-goals`, `shipkit-engineering-goals`, and `shipkit-feedback-bug` previously ran with `context: fork`. Because CC strips `AskUserQuestion` from forks ([issues #12890](https://github.com/anthropics/claude-code/issues/12890), [#18721](https://github.com/anthropics/claude-code/issues/18721)), these skills were inventing strategic visions, project stages, goals, and bug root causes with no confidence flags and writing them to `.shipkit/` artifacts as if the user had provided them. Frontmatter flipped to inline so they ask the user directly via `AskUserQuestion`. Empirically validated pilot (T4/T5/T6) in `P:/Projects2/shipkit-testing/`.
- **Body copy corrected** in `shipkit-stage` and `shipkit-engineering-goals` — removed "Dispatched in fork context — proceeds without user prompts" language that described the hallucination pattern in broad daylight.

### Changed
- **Direction loop is no longer fully autonomous** — elicitive skills now halt orchestration for user input instead of running silently. Planning and shipping loops unaffected. Walk-away mode still possible by pre-populating `.shipkit/elicitation/<skill-slug>/answers.md` before invocation.
- **"After Completion" sections rewritten** in 8 skills (`shipkit-codebase-index`, `shipkit-plan`, `shipkit-preflight`, `shipkit-review-direction`, `shipkit-review-planning`, `shipkit-review-shipping`, `shipkit-semantic-qa`, `shipkit-test-cases`) — now point at the correct next orchestrator/skill in the pipeline instead of older "user decides next steps" prose that treated every skill as a user-invoked terminal. Clarifies that reviewer skills are orchestrator-dispatched, and that plan/test-cases hand off to the shipping loop.

### Added
- **`install/shared/references/elicitation-protocol.md`** — Canonical reference for the return-prompt-resume pattern (fork emits marker, main session resumes). Currently dormant pending T7/T8/T9 orchestrator-bubble integration tests; kept on disk so the pilot skill body and future rollout can reference it without re-deriving the protocol.
- **`shipkit-why-project` pilot refactor** — Entry protocol implements context shortcut → artifact check → answers-file check → question generation → state-file writes, with runtime `AskUserQuestion` detection so the skill works correctly in both inline and (future) fork modes.

### Known Interim State
- Spec `.claude/specs/return-prompt-resume.json` (local only) tracks the paused rollout. The orchestrator-bubble design (rec #2 in the spec) was never validated end-to-end; T7/T8/T9 test plan is drafted but not yet run. Until those tests pass, all elicitive skills run inline — the cost is that direction-loop orchestration pauses for answers instead of running walk-away.

---

## [2.6.0] - 2026-04-15

Architectural cleanup release. Retired a vestigial gateway skill, fixed a runtime bug where 4 producer skills were silently running inline instead of forking with their personas, swept the framework for fork-prompt anti-patterns, and added 3 new architectural rules + 2 new wiring validation checks to catch this class of drift on every release.

### Removed
- **`shipkit-vision` skill** — Retired. Was a 2-tier-era routing gateway that became structurally redundant when the 3-loop orchestrator tier was added. The `vision.json` artifact it was supposed to produce never had a real writer — it was a phantom contract referenced in 11 places. `why.json` already contains vision/purpose/stage; the direction loop now routes to `/shipkit-why-project` or `/shipkit-stage` directly. Skill count: 38 → 37. See KI-001 in DOC-025 for history.

### Fixed
- **Producer skills now actually load their personas** (W-006) — `shipkit-product-definition`, `shipkit-engineering-definition`, `shipkit-design-system`, and `shipkit-spec` had decorative `agent:` fields without `context: fork`. Per DOC-023, this meant the producer persona never loaded at runtime — they ran as whatever the caller's context was (sonnet with orchestrator tools) instead of as product-owner/architect with opus and acceptEdits. All four now fork correctly with their personas.
- **`shipkit-stage` broken on every dispatch** — Had no propose mode at all. Every run prompted for stage/constraints/criteria/gates. In fork context those prompts hung or hallucinated. Rewritten with full propose mode: infers stage from `why.json` + codebase signals, derives constraints directly, writes the artifact without user prompts.
- **`shipkit-reviewer-shipping-agent` Bash contradiction** (W-005) — Agent declared `Bash` in `disallowedTools` but three skills using it (preflight, scale-ready, review-shipping) need Bash for build/test commands. Removed Bash from disallowedTools, added to tools. Kept `Edit, NotebookEdit` denied.
- **Fork-prompt anti-pattern swept from 15 skills** (W-009) — Removed every `Accept these?`, `Ask user to confirm`, `View/Update/Replace/Cancel`, `Use this or regenerate`, and similar prompt in any fork-dispatched producer. Also fixed residual soft-prose "ask user for stage" instructions in prerequisite tables. Fork-dispatched skills now propose-and-write-and-exit; user feedback enters through the reviewer loop at loop boundaries.
- **Step 0 ordering bug across 6 skills** — `shipkit-product-definition`, `shipkit-engineering-definition`, `shipkit-design-system`, `shipkit-product-discovery`, `shipkit-spec-roadmap`, `shipkit-why-project` had their file-exists menu running before their propose-mode check, intercepting on reviewer re-dispatch. Reordered to read `reviews/*-assessment.json` on re-dispatch and regenerate-on-gap or exit-early, with no user prompt.
- **`shipkit-spec` Agent tool → Skill dispatch** — Step 3c was instructing `Agent(subagent_type: "Explore")` for code exploration, which fails in fork context (subagents cannot spawn sub-subagents via Agent). Replaced with inline Read/Grep/Glob exploration.
- **`shipkit-thinking-partner` decorative agent field** — Removed the `agent:` field (it was never loaded because the skill intentionally runs inline for Socratic dialogue). Annotated the agent `.md` file as documentation-only.

### Added
- **Three architectural rules in DOC-015:**
  - **AR-001**: *No routing skills — routing is an orchestrator's job.* Shipkit has exactly 3 orchestration tiers (master → loop orch → producer). Router skills that conditionally dispatch one of N producers are forbidden; that logic belongs in the enclosing loop orchestrator.
  - **AR-002**: *Fork skills dispatched by an orchestrator must not prompt the user.* Gates on reachability (`orchestrated`) rather than agent type, so it covers both producer forks and utility forks.
  - **AR-003**: *When adding an orchestration tier, audit gateway skills for redundancy.* Future tier changes must include a "retired skills" section. Captures the lesson from why shipkit-vision sat as architectural debt for a year.
- **Two new validation checks in `shipkit-validate-wiring`:**
  - **W-008**: Orchestrator roster output match — every orch roster row's declared artifact must appear in the dispatched skill's `writes` set. Catches the vision.json-style contract drift.
  - **W-009**: Fork-skill prompt scan — scans every `context: fork` + `reachability: orchestrated` skill body for interactive prompt patterns. Exception allowlist gates on reachability.

### Changed
- **`cli/src/settings.js` refactor** — Settings generator no longer hardcodes permissions in JS. It loads `install/settings/shipkit.settings.json` as the single source of truth, strips the editorial `_notes` block, and replaces the `Skill()` allow-list with the caller's selected set. Eliminates a real drift risk and removes `cli/src/hooks.js` entirely. Net: -176 lines.
- **DOC-015 skill taxonomy**: Renamed the "Gateway" skill type to "Producer" (the term "gateway" was overloaded — meant both "fork + worker" and colloquially "router"). All 4 KI entries documented.
- **DOC-025 wiring graph regenerated** — now correctly captures `architecture.json` with 3 writers and 15 readers (previous regen had missed both). Contains `knownIssues` entries KI-001 through KI-004.
- **`shipkit-architect-agent` skills preload list** — Added `shipkit-design-system` (was missing; blocker for the W-006 fork fix).
- **Utility fork skills** — `shipkit-project-context` and `shipkit-codebase-index` stopped prompting during rescan/skip-folder decisions. Both now use sensible defaults in fork context.

### Internal
- Archived `.claude/specs/orchestration-artifact.md` — the unimplemented draft spec that seeded the phantom `vision.json` contract. Annotated as superseded.
- 5 audit reports added under `docs/development/` documenting the pre/post state at each fix round.
- `package.json` description corrected from 38 to 37 skills.

---

## [1.12.0] - 2026-02-28

### Added
- **`shipkit-engineering-definition` skill** — New skill (37th) that owns the technical approach: mechanisms, components, design decisions, and stack direction. Mechanisms map to features via `implementsFeatures` cross-references.
- **Component structure** in engineering-definition — `components[]` with `id`, `name`, `responsibility`, `mechanisms[]`, and `interfaces[]` for system decomposition.

### Changed
- **`shipkit-product-definition` v3** — Slimmed to pure product concerns: features, UX patterns, and differentiators. Features gain `addressesNeeds` for pain point traceability. Mechanisms, designDecisions, and stackDirection moved to engineering-definition.
- **Discovery chain extended** — `why → discovery → product-definition → engineering-definition → goals → spec → plan`. Separation of concerns: product-definition owns WHAT to build, engineering-definition owns HOW to build it.
- **`shipkit-goals` updated** — Now reads both product-definition.json and engineering-definition.json. Derives criteria from both blueprints (mechanisms from engineering, patterns from product).
- Updated 8 downstream skills to read engineering-definition.json: goals, spec, plan, architecture-memory, project-status, product-discovery, team
- Added `shipkit-scale-ready` to master routing table (was missing)
- Updated all 7-file integration: manifest, settings, master routing, overview HTML, README, CLAUDE.md, rules

### Fixed
- `shipkit-scale-ready` missing from master routing table
- `package.json` description showed 36 skills instead of 37

---

## [1.11.0] - 2026-02-27

### Added
- **`primaryIntent` field on personas** — Product discovery personas now include a `primaryIntent` field for multi-user app support. Enables downstream skills to map mechanisms and criteria to specific user types (e.g., teachers vs students, buyers vs sellers).
- **`personaIntents` map in product-definition** — Solution blueprints now include a `personaIntents` object mapping persona IDs to their intents for multi-user products.
- **Derivation patterns reference** — New `references/derivation-patterns.md` for goals skill documenting mechanism→criteria, pattern→criteria, differentiator→criteria, and MVP boundary→gate derivation patterns.

### Changed
- **Discovery chain reordered** — `why → discovery → definition → goals → spec → plan` (was: `why → goals → discovery → definition`). Goals now derive from the solution blueprint instead of being defined before it exists.
- **`shipkit-product-definition` rewritten as solution blueprint** — Captures mechanisms, UX patterns, differentiators, design decisions, stack direction, and MVP scope boundary. Replaces the previous feature portfolio mapper approach. New v2 schema with ID-based graph (`M-001`, `P-001`, `D-001`, `F-001`).
- **`shipkit-goals` rewritten as success criteria** — Produces measurable criteria with thresholds and verification methods, organized into stage gates. Replaces the previous strategic objectives approach. New v2 schema with criteria + gates model.
- Updated 10 dependent skills for chain consistency: master routing, why-project, spec, plan, architecture-memory, team, project-status, product-discovery, and team templates
- Updated manifests, rules, README, getting-started, skill-reference, and overview HTML
- Pipeline template phases renamed: Phase 1 = Discovery (why + discovery), Phase 2 = Solution Design (definition + goals)

### Removed
- `references/goal-templates.md` — replaced by `references/derivation-patterns.md`

---

## [1.10.0] - 2026-02-25

### Added
- **npx CLI for one-command install and update** — `npx github:stefan-stepzero/shipkit init` (zero dependencies, Node 18+). Full interactive and non-interactive modes with profile selection, skill/agent toggles, and CLAUDE.md merge strategies. Package name: `shipkit-dev` (pending npm publish).
- **`sync-docs` command** — `node cli/bin/shipkit.js sync-docs` regenerates skill/agent counts across README.md, installers/README.md, and shipkit-overview.html from the manifest using `<!-- sync:* -->` markers. Eliminates manual count tracking.
- **Artifact-aware pipeline startup** — `/shipkit-team --template pipeline` now scans `.shipkit/` on startup, maps existing artifacts to phases, and skips completed phases automatically.

### Changed
- Pipeline template updated with artifact-to-phase mapping, partial completion detection, and status display
- `shipkit-update` skill now uses npx CLI as primary method (Python installer as fallback)
- `shipkit-dev-release` Step 4 uses `sync-docs` instead of manual count audit
- `shipkit-framework-integrity` validates both npx CLI and Python installer (dual-installer coverage)
- All docs and skills updated to reference `npx shipkit-dev` (with `github:` pre-publish notes)
- Bash installer marked as deprecated
- CLAUDE.md Configuration Files section now lists all 6 hook files

### Fixed
- Stale `install/VERSION` path references (VERSION is at repo root)
- Skill count inconsistencies across README, CLAUDE.md, installers/README.md, and overview HTML
- CLI completion messages use working `github:` form pre-publish

---

## [1.8.1] - 2026-02-08

### Changed
- **Goals skill enhanced with template-based proposals** — Proposes stage-appropriate goals instead of asking open-ended questions. 80% of goals predictable from project stage + detected capabilities
- Goals organized across 4 lenses: Technical, Product/UX, Growth, Operational
- Added `lens` and `stage` fields to goals.json schema
- New `references/goal-templates.md` with stage definitions and concept modifiers

### Fixed
- Removed timeline/milestones from why-project (goals.json handles tracking now)
- Cleaner separation: why.json = strategic context, goals.json = actionable tracking

---

## [1.8.0] - 2026-02-08

### Added
- **React + Vite dashboard for Mission Control** — Replaces vanilla HTML with React Flow graph visualization
- **shipkit-goals skill** — Capture structured project goals with priorities (P0/P1/P2) and status tracking
- **JSON artifact convention** — Standard envelope for all `.shipkit/*.json` files (`$schema`, `type`, `version`, `lastUpdated`, `source`, `summary`)
- L-I-E (Likelihood · Impact · Effort) assessment added to verify findings

### Changed
- Migrated 11 skills to JSON artifact output (architecture, contracts, preflight, scale-ready, prompt-audit, ux-audit, progress, product-discovery, spec, plan, goals)
- Skills now reference `codebase-index.json` for accelerated exploration (goals, project-context, preflight)
- Mission Control hooks properly wired in installer

### Fixed
- Installer gaps: Mission Control files, permissions, version consolidation
- Standby command delivery: active polling replaces hook injection
- MC hooks wiring gap in installer and update skill

---

## [1.7.0] - 2026-02-07

### Added
- **Mission Control** — Real-time project dashboard with artifact visualization
- **Changelog sync system** — Auto-fetch Claude Code changelog for compatibility checks
- `shipkit-standby` skill — Wait for Mission Control commands
- `shipkit-mission-control` skill — Launch and manage dashboard
- PostToolUse hook for skill usage tracking and MC reporter
- PreToolUse hook for MC command receiver
- Contextual skill nudges in session-start hook

### Changed
- Skill count: 29 → 37
- Added `.claude/skills/` for cross-session skill access
- Moved get-skills/get-mcps to System category

---

## [1.6.0] - 2026-02-06

### Added
- `shipkit-thinking-partner` — Rubber duck debugging and ideation partner
- `shipkit-prompt-audit` — Analyze and improve AI prompts
- `shipkit-scale-ready` — Enterprise/growth readiness audit (post-traction)
- Parallel execution guidance added to remaining skills

### Changed
- Fix-and-recheck loop added to verify skill with user dismissals
- Write permissions for updater to run without interruptions

---

## [1.5.0] - 2026-02-06

### Added
- **Modular rules structure** — Framework rules in `.claude/rules/shipkit.md`
- **PreCompact hook** — Context preservation before compaction
- `shipkit-implement-independently` — Parallel implementation across git worktrees
- `shipkit-cleanup-worktrees` — Clean up finished worktrees

### Changed
- Relentless skills refactored to semantic approach (ralph-wiggum pattern)
- Added `--max` and `--cmd` arguments to relentless skills
- Installation simplified with single VERSION file

---

## [1.4.0] - 2026-02-05

### Added
- **New agent: shipkit-project-manager** — Coordination, status tracking, context management
- Hybrid mode documentation — Use skills directly (`/shipkit-plan`) OR natural language ("plan the auth feature")
- Agents now have preloaded skills via `skills:` frontmatter field

### Changed
- **Agent format updated to Claude Code subagent spec** — Proper YAML frontmatter with:
  - `tools` — Tool access control
  - `model` — All agents use `opus` for quality
  - `permissionMode` — `acceptEdits` for doc-writers, `default` for code-writers
  - `memory: project` — Project-scoped memory
  - `skills` — Preloaded skill knowledge
- **Skill reassignments for better role fit:**
  - `test-cases`: implementer → reviewer (quality planning)
  - `user-instructions`: researcher → project-manager (task coordination)
  - `communications`: researcher → project-manager (reporting)
- Agent count: 6 → 7 (all documentation updated)

### Technical
- 25/29 skills now covered by agents (4 system skills remain direct-invoke only)
- Permission optimization: `acceptEdits` for project-manager, product-owner, ux-designer, architect
- Agents now auto-delegate based on `description` field matching task

---

## [1.3.0] - 2026-02-04

### Added
- `shipkit-test-cases` — Generate code-anchored test case specifications
- Test case enrichment stage for AI-executable UI tests
- AI Agent Accessibility standards to quality checks

### Changed
- Skill count: 24 → 29

---

## [1.2.0] - 2026-02-03

### Added
- `argument-hint` frontmatter for 13 user-invocable skills (shows in slash command menu)
- `allowed-tools` restrictions for 8 read-only/focused skills
- `context: fork` for `shipkit-review-shipping` and `shipkit-codebase-index` (context isolation)
- AskUserQuestion structured guidance in `shipkit-spec`, `shipkit-plan`, `shipkit-product-discovery`
- `scripts/update-version.py` — Automate version updates across all files

### Changed
- Model optimization: `haiku` only for bulk scanning (`shipkit-detect`, `shipkit-codebase-index`)
- Removed `haiku` from `shipkit-claude-md`, `shipkit-get-skills`, `shipkit-get-mcps` (inherit best model)
- Removed `sonnet` from `shipkit-review-shipping`, `shipkit-preflight` (inherit best model)
- Skills now leverage Claude Code frontmatter features for better UX and performance

### Technical
- Integrated Claude Code features: `argument-hint`, `allowed-tools`, `context: fork`
- Skills documentation now includes AskUserQuestion patterns for structured user input
- Version watermarking updated to v1.2.0 across 35 files

---

## [1.1.0] - 2026-02-03

### Added
- `shipkit-update` — Install or update Shipkit from GitHub with intelligent merge
- `shipkit-get-skills` — Discover and install community Claude Code skills
- `shipkit-get-mcps` — Discover and install MCP servers
- `shipkit-claude-md` — Manage and update CLAUDE.md with learnings
- `shipkit-review-shipping` — Quality verification across 12 dimensions
- `shipkit-preflight` — Production readiness audit
- `shipkit-codebase-index` — Semantic codebase indexing for navigation
- Version watermarking on all installed files (`<!-- Shipkit v1.1.0 -->`)
- `install/VERSION` file for version tracking
- Archive-based update system (never deletes, always preserves)

### Removed
- `shipkit-component-knowledge` — Replaced by natural capability (documentation)
- `shipkit-route-knowledge` — Replaced by natural capability (documentation)
- `shipkit-implement` — Replaced by natural capability (implementation)
- `shipkit-quality-confidence` — Replaced by `shipkit-review-shipping`
- `shipkit-teach` — Renamed to `shipkit-claude-md`

### Changed
- Renamed all `lite-*` files to `shipkit-*` for consistency
- Updated skill count to 24 skills
- CLAUDE.md now uses BEGIN/END markers for Shipkit sections
- Settings.json includes `_shipkit` version key
- Clarified that implementation, debugging, testing are natural capabilities

### Fixed
- Removed stale references to deleted skills in detect mode
- Cleaned up template files referencing old skill names

---

## [0.1.0] - 2026-01-16

### Added
- Initial Shipkit release
- 22 skills organized into 6 categories
- 7 agent personas
- Python cross-platform installer
- Session hooks for workflow enforcement
- `.shipkit/` workspace structure

### Categories
- **Core Workflow**: master, project-status, project-context, codebase-index, claude-md
- **Discovery & Planning**: product-discovery, why-project, spec, plan, prototyping, prototype-to-spec
- **Implementation**: architecture-memory, data-contracts, integration-docs
- **Quality & Documentation**: verify, ux-audit, user-instructions, communications, work-memory
- **Ecosystem**: get-skills, get-mcps
- **System**: detect

---

## Archive

The full Shipkit framework (dev-*, prod-* skills) was archived on January 16, 2026.
See `archive/base-shipkit/` for historical reference.
