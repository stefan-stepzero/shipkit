# Shipkit Repository Improvements

**Created:** 2026-02-03
**Purpose:** Track improvements to make Shipkit a great open source tool

---

## Overview

33 tasks organized into 6 tranches to improve repo structure, documentation, and open source readiness.

---

## Tranche 1: Open Source Readiness ✅

| # | Task | Status |
|---|------|--------|
| 1 | Add CONTRIBUTING.md — How to contribute skills, agents, bug fixes | Done |
| 2 | Add CODE_OF_CONDUCT.md — Standard code of conduct | Done |
| 3 | Add LICENSE file — MIT mentioned in README but no actual file | Done |
| 4 | Add CHANGELOG.md — Track version changes | Done |
| 5 | Add .github/ISSUE_TEMPLATE/bug_report.md | Done |
| 6 | Add .github/ISSUE_TEMPLATE/feature_request.md | Done |
| 7 | Add .github/ISSUE_TEMPLATE/new_skill_proposal.md | Done |
| 8 | Add .github/PULL_REQUEST_TEMPLATE.md | Done |
| 9 | Add .github/workflows/validate-skills.yml — CI to validate skill structure | Done |

---

## Tranche 2: Documentation Consolidation ✅

| # | Task | Status |
|---|------|--------|
| 10 | Create docs/getting-started.md — Tutorial for first-time users | Done |
| 11 | Create docs/skill-reference.md — All 23 skills documented | Done |
| 12 | Create docs/creating-skills.md — How to create new skills | Done |
| 13 | Create docs/architecture.md — Framework design philosophy | Done |
| 14 | Create docs/examples/new-project.md — Example workflow starting fresh | Done |
| 15 | Create docs/examples/existing-project.md — Example adding to existing codebase | Done |
| 16 | Merge claude-code-best-practices/ into docs/development/ | Done |
| 17 | Move help/ to docs/generated/ | Done |

---

## Tranche 3: Root Directory Cleanup ✅

| # | Task | Status |
|---|------|--------|
| 18 | Delete exported/ — Moved script to scripts/, deleted folder | Done |
| 19 | Rename claude-working-documents/ to dev/ | Done |
| 20 | Verify .gitignore covers build artifacts | Done |

---

## Tranche 4: Installer Improvements ✅

| # | Task | Status |
|---|------|--------|
| 21 | Add installers/uninstall.py — Clean removal of Shipkit | Done |
| 22 | Add list-skills.py (installed to .shipkit/scripts/) | Done |
| 23 | Add skill profiles — minimal, discovery, shipkit (full) | Done |
| 24 | Add npx shipkit init — npm package | Skipped (future) |
| 25 | Add curl installer — Single command install | Skipped (future) |

---

## Tranche 5: Skill System Improvements

| # | Task | Status |
|---|------|--------|
| 26 | Standardize skill metadata — Add version, category, requires, creates, reads | Pending |
| 27 | Add skill versioning — Track versions in manifest | Pending |
| 28 | Document unique value of each skill — Clarify overlaps | Pending |
| 29 | Review shipkit-work-memory vs shipkit-project-status overlap | Pending |
| 30 | Review shipkit-claude-md necessity | Pending |

---

## Tranche 6: Testing & CI

| # | Task | Status |
|---|------|--------|
| 31 | Revive tests/ folder — Create working test suite | Pending |
| 32 | Create tests/validate-skills.py — Automated validation | Pending |
| 33 | Add CI workflow — Run validation on PRs | Pending |

---

## Priority Matrix

| Priority | Tranches | Rationale |
|----------|----------|-----------|
| **Immediate** | Tranche 1 | Required for open source credibility |
| **High** | Tranche 2, 3 | Improves discoverability and cleanliness |
| **Medium** | Tranche 4, 6 | Improves developer experience |
| **Lower** | Tranche 5 | Nice-to-have refinements |

---

## Progress Log

| Date | Tranche | Tasks Completed | Notes |
|------|---------|-----------------|-------|
| 2026-02-03 | - | 0 | Document created |
| 2026-02-03 | 1 | 9 | Open source readiness complete |
| 2026-02-03 | 2 | 8 | Documentation consolidation complete |
| 2026-02-03 | 3 | 3 | Root directory cleanup complete |
| 2026-02-03 | 4 | 3 | Installer improvements (skipped future items) |

---

## Notes

- Tranche 1 should be completed before any public announcement
- Tranches can be done in parallel if resources allow
- Tasks 24-25 (npm/curl installers) are future enhancements, not blockers
