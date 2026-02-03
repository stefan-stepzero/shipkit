# Changelog

All notable changes to Shipkit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### Added
- `shipkit-get-skills` — Discover and install community Claude Code skills
- `shipkit-get-mcps` — Discover and install MCP servers
- `shipkit-claude-md` — Manage and update CLAUDE.md with learnings
- `shipkit-verify` — Quality verification across 12 dimensions
- `shipkit-codebase-index` — Semantic codebase indexing for navigation

### Removed
- `shipkit-component-knowledge` — Replaced by natural capability (documentation)
- `shipkit-route-knowledge` — Replaced by natural capability (documentation)
- `shipkit-implement` — Replaced by natural capability (implementation)
- `shipkit-quality-confidence` — Replaced by `shipkit-verify`
- `shipkit-teach` — Renamed to `shipkit-claude-md`

### Changed
- Renamed all `lite-*` files to `shipkit-*` for consistency
- Updated skill count from 28 to 22 (removed redundant skills)
- Clarified that implementation, debugging, testing are natural capabilities

### Fixed
- Removed stale references to deleted skills in detect mode
- Cleaned up template files referencing old skill names

---

## [0.1.0] - 2026-01-16

### Added
- Initial Shipkit release
- 22 skills organized into 6 categories
- 6 agent personas
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
