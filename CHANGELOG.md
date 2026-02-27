# Changelog

All notable changes to Shipkit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

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
- `context: fork` for `shipkit-verify` and `shipkit-codebase-index` (context isolation)
- AskUserQuestion structured guidance in `shipkit-spec`, `shipkit-plan`, `shipkit-product-discovery`
- `scripts/update-version.py` — Automate version updates across all files

### Changed
- Model optimization: `haiku` only for bulk scanning (`shipkit-detect`, `shipkit-codebase-index`)
- Removed `haiku` from `shipkit-claude-md`, `shipkit-get-skills`, `shipkit-get-mcps` (inherit best model)
- Removed `sonnet` from `shipkit-verify`, `shipkit-preflight` (inherit best model)
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
- `shipkit-verify` — Quality verification across 12 dimensions
- `shipkit-preflight` — Production readiness audit
- `shipkit-codebase-index` — Semantic codebase indexing for navigation
- Version watermarking on all installed files (`<!-- Shipkit v1.1.0 -->`)
- `install/VERSION` file for version tracking
- Archive-based update system (never deletes, always preserves)

### Removed
- `shipkit-component-knowledge` — Replaced by natural capability (documentation)
- `shipkit-route-knowledge` — Replaced by natural capability (documentation)
- `shipkit-implement` — Replaced by natural capability (implementation)
- `shipkit-quality-confidence` — Replaced by `shipkit-verify`
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
