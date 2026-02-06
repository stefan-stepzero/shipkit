# Skill Improvements Implementation Plan

**Created**: 2026-02-03
**Spec**: dev/SKILL-IMPROVEMENTS-SPEC.md
**Status**: In Progress

---

## Phase 1: Quick Wins (Frontmatter Only)

### 1.1 Add argument-hint to user-invocable skills

| Skill | Hint | Status |
|-------|------|--------|
| shipkit-spec | `<feature name or description>` | ✅ |
| shipkit-plan | `[spec name]` | ✅ |
| shipkit-verify | `[scope or feature]` | ✅ |
| shipkit-preflight | `[area to audit]` | ✅ |
| shipkit-prototyping | `<component or feature>` | ✅ |
| shipkit-architecture-memory | `<decision to log>` | ✅ |
| shipkit-work-memory | `[checkpoint name]` | ✅ |
| shipkit-project-status | _(no argument)_ | ✅ |
| shipkit-project-context | _(no argument)_ | ✅ |
| shipkit-get-skills | `<search query>` | ✅ |
| shipkit-get-mcps | `<search query>` | ✅ |
| shipkit-why-project | `[project name]` | ✅ |
| shipkit-product-discovery | `[persona or journey]` | ✅ |

### 1.2 Add model: haiku to scanning skills

| Skill | Status |
|-------|--------|
| shipkit-codebase-index | ✅ |
| shipkit-detect | ✅ |

### 1.3 Add allowed-tools to read-only skills

| Skill | Tools | Status |
|-------|-------|--------|
| shipkit-verify | Read, Glob, Grep, Bash | ✅ |
| shipkit-preflight | Read, Glob, Grep, Bash | ✅ |
| shipkit-project-status | Read, Glob, Grep, Bash | ✅ |
| shipkit-ux-audit | Read, Glob, Grep | ✅ |
| shipkit-codebase-index | Read, Glob, Grep, Bash, Write | ✅ |
| shipkit-detect | Read, Glob, Grep, Write | ✅ |

---

## Phase 2: AskUserQuestion Integration

### 2.1 shipkit-spec - Structured Questions
- Question 1: Feature type (UI/API/Integration/Infrastructure)
- Question 2: Complexity level (Simple/Medium/Complex)
- Question 3: Edge case focus (from 6 categories)

### 2.2 shipkit-plan - Structured Questions
- Question 1: Which spec to plan
- Question 2: Plan detail level (Quick POC/Detailed)

### 2.3 shipkit-product-discovery - Structured Questions
- Question 1: Discovery focus (Personas/Journeys/Stories)

---

## Phase 3: Context Isolation

### 3.1 Add context: fork to verification skills

| Skill | Status |
|-------|--------|
| shipkit-verify | ⬜ |
| shipkit-preflight | ⬜ |
| shipkit-codebase-index | ⬜ |

---

## Execution Checklist

- [x] Phase 1.1: argument-hint for all user-invocable skills
- [x] Phase 1.2: model: haiku for scanning skills
- [x] Phase 1.3: allowed-tools for read-only skills
- [x] Phase 2.1: AskUserQuestion in shipkit-spec
- [x] Phase 2.2: AskUserQuestion in shipkit-plan
- [x] Phase 2.3: AskUserQuestion in shipkit-product-discovery
- [ ] Phase 3.1: context: fork for verification skills (DEFERRED - significant behavioral change, needs testing)
- [ ] Update README with skill count if needed
- [ ] Update manifest if needed

---

## Notes

- Each change should be tested by invoking the skill
- Frontmatter changes are low-risk and can be done quickly
- AskUserQuestion changes require updating process steps
- context: fork changes affect skill behavior significantly
