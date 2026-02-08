# Changelog

All notable changes to Shipkit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

*No unreleased changes*

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
