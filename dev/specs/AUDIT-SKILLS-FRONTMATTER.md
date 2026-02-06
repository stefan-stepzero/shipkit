# Skills Frontmatter Audit

**Status:** Implemented
**Last Updated:** 2026-02-06
**Implementation:** Phases 1-3 complete (model specs, context:fork, agent assignment). Remaining items moved to REMAINING-ENHANCEMENTS.md

## Purpose

Audit all 29 Shipkit skills against new Claude Code frontmatter capabilities to identify improvement opportunities.

## New Capabilities to Audit

| Capability | Description | Use Case |
|------------|-------------|----------|
| `context: fork` | Run skill in forked sub-agent context | Skills that do research/exploration without polluting main context |
| `agent` | Specify agent type for execution | Skills that should run with a specific persona |
| `hooks` | Define PreToolUse/PostToolUse/Stop hooks scoped to skill | Skills needing validation, cleanup, or enforcement |
| `skills` | Auto-load other skills for subagents | Skills that spawn subagents needing specific capabilities |
| `model` | Specify model per skill | Skills needing specific model capabilities (e.g., Opus for planning) |
| `allowed-tools` (YAML) | YAML-style list syntax | Cleaner multi-tool declarations |
| `once: true` | Hook runs only once | One-time setup or validation |

## Skills Inventory

### Core Workflow (5 skills)
- [x] shipkit-master
- [x] shipkit-project-status
- [x] shipkit-project-context
- [x] shipkit-codebase-index
- [x] shipkit-claude-md

### Discovery & Planning (7 skills)
- [x] shipkit-product-discovery
- [x] shipkit-why-project
- [x] shipkit-spec
- [x] shipkit-feedback-bug
- [x] shipkit-plan
- [x] shipkit-prototyping
- [x] shipkit-prototype-to-spec

### Implementation (3 skills)
- [x] shipkit-architecture-memory
- [x] shipkit-data-contracts
- [x] shipkit-integration-docs

### Execution (4 skills)
- [x] shipkit-build-relentlessly
- [x] shipkit-test-relentlessly
- [x] shipkit-lint-relentlessly
- [x] shipkit-test-cases

### Quality & Documentation (6 skills)
- [x] shipkit-verify
- [x] shipkit-preflight
- [x] shipkit-ux-audit
- [x] shipkit-user-instructions
- [x] shipkit-communications
- [x] shipkit-work-memory

### Ecosystem (2 skills)
- [x] shipkit-get-skills
- [x] shipkit-get-mcps

### System (2 skills)
- [x] shipkit-detect
- [x] shipkit-update

## Findings

### Skills that should use `context: fork`

**Already using:**
- `shipkit-codebase-index` - Already has `context: fork` and `model: haiku`
- `shipkit-verify` - Already has `context: fork`

**Recommended additions:**

| Skill | Rationale |
|-------|-----------|
| `shipkit-preflight` | Heavy codebase scanning, exploratory analysis, shouldn't pollute main context |
| `shipkit-test-cases` | Code analysis and test case generation is exploratory |
| `shipkit-ux-audit` | Scans implementations for UX patterns, exploratory work |
| `shipkit-feedback-bug` | Bug investigation with codebase exploration |
| `shipkit-project-status` | Scans entire .shipkit/ directory, generates report |
| `shipkit-project-context` | Tech stack detection is exploratory scanning |

**Pattern:** Skills that scan/explore codebase without making decisions that need to persist in main context.

### Skills that should specify `agent`

**Recommended additions:**

| Skill | Agent | Rationale |
|-------|-------|-----------|
| `shipkit-spec` | `shipkit-product-owner-agent` | Specs require product owner perspective for requirements |
| `shipkit-product-discovery` | `shipkit-product-owner-agent` | User personas and journeys need product owner mindset |
| `shipkit-why-project` | `shipkit-product-owner-agent` | Vision definition is product owner work |
| `shipkit-plan` | `shipkit-architect-agent` | Implementation planning needs architect perspective |
| `shipkit-architecture-memory` | `shipkit-architect-agent` | Logging architecture decisions |
| `shipkit-ux-audit` | `shipkit-ux-designer-agent` | UX review needs designer perspective |
| `shipkit-verify` | `shipkit-reviewer-agent` | Code review should use reviewer persona |
| `shipkit-preflight` | `shipkit-reviewer-agent` | Production readiness audit is review work |
| `shipkit-feedback-bug` | `shipkit-researcher-agent` | Bug investigation needs research mindset |
| `shipkit-integration-docs` | `shipkit-researcher-agent` | Fetching docs is research |

**Pattern:** Match skill purpose to appropriate specialist agent persona.

### Skills that should define `hooks`

**Recommended additions:**

| Skill | Hook Type | Purpose |
|-------|-----------|---------|
| `shipkit-spec` | `PostToolUse` on Write | Validate spec file has all required sections before saving |
| `shipkit-plan` | `PostToolUse` on Write | Validate plan has all validation checks passed |
| `shipkit-architecture-memory` | `PostToolUse` on Write | Check for contradictions before appending |
| `shipkit-verify` | `PreToolUse` on Edit/Write | Prevent verify from making changes (read-only enforcement) |
| `shipkit-preflight` | `PreToolUse` on Edit/Write | Prevent preflight from making changes (report-only) |

**Relentless skills already have Stop hooks defined externally** - keep as-is via `shipkit-relentless-stop-hook.py`.

### Skills that should use `model`

**Already using:**
- `shipkit-codebase-index` - Already has `model: haiku`
- `shipkit-detect` - Already has `model: haiku`

**Recommended additions:**

| Skill | Model | Rationale |
|-------|-------|-----------|
| `shipkit-plan` | `model: opus` | Complex multi-phase planning with validation requires deep reasoning |
| `shipkit-spec` | `model: opus` | Feature specification with edge cases needs thorough analysis |
| `shipkit-preflight` | `model: opus` | Production readiness audit requires comprehensive judgment |
| `shipkit-project-status` | `model: haiku` | Fast scanning, no deep reasoning needed |
| `shipkit-project-context` | `model: haiku` | File scanning and extraction, mechanical work |
| `shipkit-test-cases` | `model: haiku` | Test case generation is pattern-based |

**Pattern:**
- `opus` for skills requiring judgment, planning, complex reasoning
- `haiku` for scanning, detection, mechanical extraction

### Skills that should use `skills` (auto-load other skills)

**Recommended additions:**

| Skill | Auto-load Skills | Rationale |
|-------|-----------------|-----------|
| `shipkit-preflight` | `shipkit-verify` | Preflight may use verify patterns |
| `shipkit-plan` | `shipkit-spec` | Plans reference specs |
| `shipkit-prototyping` | `shipkit-spec` | May need to create spec if missing |

**Note:** This capability is most useful for skills that spawn subagents. Most Shipkit skills reference other skills in documentation but don't programmatically spawn them.

### Other improvements identified

**1. YAML-style `allowed-tools` cleanup (all skills with tool restrictions):**

Skills already using YAML list format correctly:
- `shipkit-project-status`, `shipkit-codebase-index`, `shipkit-claude-md`
- `shipkit-build/test/lint-relentlessly`
- `shipkit-verify`, `shipkit-preflight`, `shipkit-ux-audit`
- `shipkit-get-skills`, `shipkit-get-mcps`, `shipkit-detect`

Skills that could benefit from adding explicit `allowed-tools`:
- `shipkit-spec` - Add Read, Write, Glob, Grep
- `shipkit-plan` - Add Read, Write, Glob, Grep, Bash, Task
- `shipkit-feedback-bug` - Add Read, Write, Glob, Grep, Task
- `shipkit-work-memory` - Add Read, Write, Bash
- `shipkit-communications` - Add Read, Write, Glob

**2. Missing `argument-hint` for better discoverability:**

Skills missing hints that would benefit:
- `shipkit-project-status` - `"[scope or feature]"`
- `shipkit-verify` - Already has it
- `shipkit-preflight` - Already has it
- `shipkit-work-memory` - Already has it

**3. Missing `triggers` for natural language routing:**

Only relentless skills have explicit triggers. Consider adding for:
- `shipkit-verify` - triggers: ["check my work", "review changes", "ready to commit"]
- `shipkit-preflight` - triggers: ["ready to ship", "production check", "go live"]
- `shipkit-work-memory` - triggers: ["save progress", "end session", "checkpoint"]

## Recommendations

### Priority 1: High-Value Model Specifications

These changes ensure expensive/complex skills use appropriate model power:

1. **Add `model: opus`** to:
   - `shipkit-plan` - Complex validation and planning
   - `shipkit-spec` - Thorough edge case analysis
   - `shipkit-preflight` - Production readiness judgment

2. **Add `model: haiku`** to:
   - `shipkit-project-status` - Fast scanning
   - `shipkit-project-context` - Mechanical extraction
   - `shipkit-test-cases` - Pattern-based generation

### Priority 2: Context Isolation via Fork

Prevent exploratory work from polluting main conversation:

1. **Add `context: fork`** to:
   - `shipkit-preflight`
   - `shipkit-test-cases`
   - `shipkit-ux-audit`
   - `shipkit-feedback-bug`
   - `shipkit-project-status`
   - `shipkit-project-context`

### Priority 3: Agent Persona Assignment

Match skills to specialist perspectives:

1. **Product Owner perspective:**
   - `shipkit-spec` - `agent: shipkit-product-owner-agent`
   - `shipkit-product-discovery` - `agent: shipkit-product-owner-agent`
   - `shipkit-why-project` - `agent: shipkit-product-owner-agent`

2. **Architect perspective:**
   - `shipkit-plan` - `agent: shipkit-architect-agent`
   - `shipkit-architecture-memory` - `agent: shipkit-architect-agent`

3. **Reviewer perspective:**
   - `shipkit-verify` - `agent: shipkit-reviewer-agent`
   - `shipkit-preflight` - `agent: shipkit-reviewer-agent`

4. **UX Designer perspective:**
   - `shipkit-ux-audit` - `agent: shipkit-ux-designer-agent`

5. **Researcher perspective:**
   - `shipkit-feedback-bug` - `agent: shipkit-researcher-agent`
   - `shipkit-integration-docs` - `agent: shipkit-researcher-agent`

### Priority 4: Validation Hooks (Lower Priority)

Add skill-scoped hooks for quality enforcement:

1. `shipkit-verify` - PreToolUse hook to block Edit/Write (read-only enforcement)
2. `shipkit-preflight` - PreToolUse hook to block Edit/Write (report-only)

### Priority 5: Explicit Tool Restrictions (Lower Priority)

Add `allowed-tools` to skills that don't have them for clarity and safety.

## Implementation Plan

### Phase 1: Model Optimization (High Impact, Low Risk)

```yaml
# shipkit-plan
model: opus

# shipkit-spec
model: opus

# shipkit-preflight
model: opus

# shipkit-project-status
model: haiku

# shipkit-project-context
model: haiku

# shipkit-test-cases
model: haiku
```

### Phase 2: Context Isolation (Medium Impact, Low Risk)

```yaml
# Add to these skills:
context: fork

# Skills: preflight, test-cases, ux-audit, feedback-bug, project-status, project-context
```

### Phase 3: Agent Assignment (Medium Impact, Medium Risk)

Test thoroughly as agent personas may change skill behavior.

```yaml
# shipkit-spec
agent: shipkit-product-owner-agent

# shipkit-plan
agent: shipkit-architect-agent

# etc.
```

### Phase 4: Validation Hooks (Low Priority)

Requires testing hook behavior. Implement after core changes stabilize.

## Summary

| Capability | Skills to Update | Priority |
|------------|-----------------|----------|
| `model: opus` | 3 skills | P1 |
| `model: haiku` | 3 skills | P1 |
| `context: fork` | 6 skills | P2 |
| `agent` | 10 skills | P3 |
| `hooks` | 2-5 skills | P4 |
| `allowed-tools` | 5 skills | P5 |

**Total high-value changes:** ~22 skill frontmatter updates

**Already optimal (no changes needed):**
- `shipkit-codebase-index` - Has fork + haiku
- `shipkit-detect` - Has haiku (system skill)
- `shipkit-verify` - Has fork
- All relentless skills - Have external Stop hook
