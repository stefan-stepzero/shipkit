# Agents Frontmatter Audit

**Status:** Implemented
**Last Updated:** 2026-02-06
**Implementation:** disallowedTools added to all 6 agents

## Purpose

Audit all 7 Shipkit agents against new Claude Code agent frontmatter capabilities.

## New Capabilities to Audit

| Capability | Description | Use Case |
|------------|-------------|----------|
| `permissionMode` | Set permission mode for agent | Restrict agent to specific permission level |
| `disallowedTools` | Explicitly block tools | Prevent agents from using certain tools |
| `hooks` | Define hooks scoped to agent lifecycle | Validation, logging, enforcement during agent work |
| `model` | Specify model for agent | Use appropriate model for agent's role |

## Agents Inventory

- [x] shipkit-product-owner-agent
- [x] shipkit-ux-designer-agent
- [x] shipkit-architect-agent
- [x] shipkit-implementer-agent
- [x] shipkit-reviewer-agent
- [x] shipkit-researcher-agent
- [x] shipkit-project-manager-agent

---

## Current State Analysis

### shipkit-product-owner-agent
**Current frontmatter:**
```yaml
name: shipkit-product-owner
description: Product owner for requirements, feature specs, user research, and product discovery.
tools: Read, Glob, Grep, Write, Edit
model: opus
permissionMode: acceptEdits
memory: project
skills: shipkit-why-project, shipkit-product-discovery, shipkit-spec, shipkit-feedback-bug
```

**Analysis:**
- Already uses `model: opus` - appropriate for strategic product thinking
- Uses `permissionMode: acceptEdits` - reasonable for a role that creates specs/artifacts
- Has Bash excluded from tools - good, PO shouldn't be running commands
- No `disallowedTools` or `hooks` defined

**Recommendations:**
| Capability | Current | Recommendation | Rationale |
|------------|---------|----------------|-----------|
| `permissionMode` | `acceptEdits` | Keep as-is | PO needs to write specs/context files |
| `disallowedTools` | None | Add `Bash, NotebookEdit` | Explicitly document the exclusion; PO should never run commands |
| `hooks` | None | Consider `afterAgent` | Could validate that outputs went to `.shipkit/` |
| `model` | `opus` | Keep as-is | Strategic thinking benefits from opus |

### shipkit-ux-designer-agent
**Current frontmatter:**
```yaml
name: shipkit-ux-designer
description: UX designer for UI patterns, prototyping, and design decisions.
tools: Read, Glob, Grep, Write, Edit
model: opus
permissionMode: acceptEdits
memory: project
skills: shipkit-ux-audit, shipkit-prototyping, shipkit-prototype-to-spec
```

**Analysis:**
- Uses `model: opus` - appropriate for design decisions
- Uses `permissionMode: acceptEdits` - reasonable for creating prototypes
- Has Bash excluded from tools - good, designer shouldn't run commands
- Similar profile to product-owner

**Recommendations:**
| Capability | Current | Recommendation | Rationale |
|------------|---------|----------------|-----------|
| `permissionMode` | `acceptEdits` | Keep as-is | UX needs to write component code/prototypes |
| `disallowedTools` | None | Add `Bash, NotebookEdit` | Explicitly prevent command execution |
| `hooks` | None | Optional | Less critical than other agents |
| `model` | `opus` | Consider `sonnet` | Design work may not need opus-level reasoning; cost savings |

### shipkit-architect-agent
**Current frontmatter:**
```yaml
name: shipkit-architect
description: Technical architect for system design, implementation planning, and architectural decisions.
tools: Read, Glob, Grep, Write, Edit, Bash
model: opus
permissionMode: acceptEdits
memory: project
skills: shipkit-plan, shipkit-architecture-memory, shipkit-data-contracts
```

**Analysis:**
- Uses `model: opus` - **critical** for complex architectural reasoning
- Uses `permissionMode: acceptEdits` - appropriate
- Has Bash access - needed for exploring codebase, running analysis commands
- Most tooling-heavy of the non-implementation agents

**Recommendations:**
| Capability | Current | Recommendation | Rationale |
|------------|---------|----------------|-----------|
| `permissionMode` | `acceptEdits` | Consider `plan` | Architect should plan, not implement; restricts to read + planning |
| `disallowedTools` | None | Add `NotebookEdit` | Architect doesn't need notebook editing |
| `hooks` | None | Add `afterAgent` | Validate architecture decisions are documented |
| `model` | `opus` | **Keep as-is** | Architectural reasoning is exactly where opus shines |

**Important Note:** If `permissionMode: plan` is added, verify it still allows writing to `.shipkit/` context files. If not, keep `acceptEdits`.

### shipkit-implementer-agent
**Current frontmatter:**
```yaml
name: shipkit-implementer
description: Implementation specialist for coding features, fixing bugs, and writing tests.
tools: Read, Glob, Grep, Write, Edit, Bash, NotebookEdit
model: opus
permissionMode: default
memory: project
skills: shipkit-build-relentlessly, shipkit-test-relentlessly, shipkit-lint-relentlessly
```

**Analysis:**
- Uses `model: opus` - may be overkill for straightforward implementation
- Uses `permissionMode: default` - full permissions, appropriate for implementation
- Has full tool access including NotebookEdit and Bash - correct for implementation
- Most permissive agent, as expected

**Recommendations:**
| Capability | Current | Recommendation | Rationale |
|------------|---------|----------------|-----------|
| `permissionMode` | `default` | Keep as-is | Implementation requires full file/command access |
| `disallowedTools` | None | None needed | Implementer needs all tools |
| `hooks` | None | Add `afterAgent` | Validate tests pass, linting clean before completing |
| `model` | `opus` | Consider `sonnet` | Implementation is more mechanical; sonnet is faster/cheaper |

**Cost-benefit:** Sonnet for implementer could significantly reduce costs for long implementation sessions while maintaining quality.

### shipkit-reviewer-agent
**Current frontmatter:**
```yaml
name: shipkit-reviewer
description: Code reviewer for quality verification, security checks, and acceptance criteria validation.
tools: Read, Glob, Grep
model: opus
permissionMode: default
memory: project
skills: shipkit-verify, shipkit-preflight, shipkit-test-cases
```

**Analysis:**
- Uses `model: opus` - good for nuanced security/quality analysis
- Uses `permissionMode: default` but only has read tools - **inconsistent**
- **Already restricts tools** via `tools` field - only Read, Glob, Grep
- Cannot write/edit - appropriate for a reviewer who should flag, not fix

**Recommendations:**
| Capability | Current | Recommendation | Rationale |
|------------|---------|----------------|-----------|
| `permissionMode` | `default` | Change to `plan` or `bypassPermissions` | Should be read-only; current tools already restrict |
| `disallowedTools` | None | Add `Write, Edit, Bash, NotebookEdit` | Explicitly enforce read-only behavior |
| `hooks` | None | Add `afterAgent` | Ensure review findings are documented |
| `model` | `opus` | Keep as-is | Security review benefits from sophisticated reasoning |

**Critical Finding:** Reviewer should be explicitly read-only. Using `disallowedTools` makes this intent clearer than relying solely on `tools` field.

### shipkit-researcher-agent
**Current frontmatter:**
```yaml
name: shipkit-researcher
description: Research specialist for documentation lookup, integration research, and troubleshooting.
tools: Read, Glob, Grep, WebFetch, WebSearch
model: opus
permissionMode: default
memory: project
skills: shipkit-integration-docs
```

**Analysis:**
- Uses `model: opus` - may be overkill for research/lookup
- Uses `permissionMode: default` but only has read + web tools
- Has web access (WebFetch, WebSearch) - unique among agents
- Cannot write/edit files - appropriate for research role

**Recommendations:**
| Capability | Current | Recommendation | Rationale |
|------------|---------|----------------|-----------|
| `permissionMode` | `default` | Consider `plan` | Research should inform, not modify |
| `disallowedTools` | None | Add `Write, Edit, Bash, NotebookEdit` | Explicitly prevent modifications |
| `hooks` | None | Optional | Less critical |
| `model` | `opus` | Consider `sonnet` | Research is mostly lookup; sonnet is sufficient |

### shipkit-project-manager-agent
**Current frontmatter:**
```yaml
name: shipkit-project-manager
description: Project manager for coordination, status tracking, and context management.
tools: Read, Glob, Grep, Write, Edit, Bash
model: opus
permissionMode: acceptEdits
memory: project
skills: shipkit-master, shipkit-project-status, shipkit-project-context, shipkit-codebase-index, shipkit-claude-md, shipkit-work-memory, shipkit-user-instructions, shipkit-communications
```

**Analysis:**
- Uses `model: opus` - appropriate for orchestration/coordination
- Uses `permissionMode: acceptEdits` - reasonable for maintaining context
- Has Bash access - useful for git status, project exploration
- Most skills of any agent (8 skills)

**Recommendations:**
| Capability | Current | Recommendation | Rationale |
|------------|---------|----------------|-----------|
| `permissionMode` | `acceptEdits` | Keep as-is | PM needs to update context files |
| `disallowedTools` | None | Add `NotebookEdit` | PM doesn't need notebook editing |
| `hooks` | None | Add `beforeAgent` | Load current project status before work |
| `model` | `opus` | Keep as-is | Coordination benefits from sophisticated reasoning |

---

## Findings

### Agents that should set `permissionMode`

| Agent | Current | Recommended | Rationale |
|-------|---------|-------------|-----------|
| `shipkit-architect-agent` | `acceptEdits` | `plan` (if allows .shipkit writes) | Should plan, not implement |
| `shipkit-reviewer-agent` | `default` | `plan` | Should be read-only |
| `shipkit-researcher-agent` | `default` | `plan` | Should inform, not modify |

**Note:** Need to verify what `permissionMode: plan` allows. If it blocks all file writes, then `acceptEdits` with `disallowedTools` is better.

### Agents that should use `disallowedTools`

| Agent | Recommended `disallowedTools` | Rationale |
|-------|-------------------------------|-----------|
| `shipkit-product-owner-agent` | `Bash, NotebookEdit` | PO shouldn't run commands |
| `shipkit-ux-designer-agent` | `Bash, NotebookEdit` | Designer shouldn't run commands |
| `shipkit-architect-agent` | `NotebookEdit` | Architect doesn't need notebooks |
| `shipkit-reviewer-agent` | `Write, Edit, Bash, NotebookEdit` | **Must be read-only** |
| `shipkit-researcher-agent` | `Write, Edit, Bash, NotebookEdit` | **Must be read-only** |
| `shipkit-project-manager-agent` | `NotebookEdit` | PM doesn't need notebooks |

**Priority:** Reviewer and Researcher are highest priority - they should be explicitly read-only.

### Agents that should define `hooks`

| Agent | Hook Type | Purpose |
|-------|-----------|---------|
| `shipkit-architect-agent` | `afterAgent` | Validate architecture decisions documented in `.shipkit/` |
| `shipkit-implementer-agent` | `afterAgent` | Validate tests pass, linting clean |
| `shipkit-reviewer-agent` | `afterAgent` | Ensure review findings documented |
| `shipkit-project-manager-agent` | `beforeAgent` | Load current project status |

**Consideration:** Hooks add complexity. Start with `disallowedTools` which is simpler.

### Agents that should specify `model`

All agents currently use `model: opus`. Recommendations for cost optimization:

| Agent | Current | Recommended | Rationale |
|-------|---------|-------------|-----------|
| `shipkit-product-owner-agent` | `opus` | Keep `opus` | Strategic decisions need best reasoning |
| `shipkit-ux-designer-agent` | `opus` | Consider `sonnet` | Design work is more pattern-matching |
| `shipkit-architect-agent` | `opus` | **Keep `opus`** | Architectural complexity needs opus |
| `shipkit-implementer-agent` | `opus` | Consider `sonnet` | Implementation is more mechanical |
| `shipkit-reviewer-agent` | `opus` | Keep `opus` | Security review needs sophisticated reasoning |
| `shipkit-researcher-agent` | `opus` | Consider `sonnet` | Research is mostly lookup |
| `shipkit-project-manager-agent` | `opus` | Keep `opus` | Orchestration benefits from opus |

**Cost Optimization Candidates:** UX Designer, Implementer, Researcher could use Sonnet to reduce costs without significant quality loss.

---

## Recommendations

### Priority 1: Enforce Read-Only for Review/Research Agents (HIGH IMPACT)
Add `disallowedTools` to Reviewer and Researcher to make their read-only nature explicit and enforced.

### Priority 2: Add `disallowedTools` to All Agents (MEDIUM IMPACT)
Document and enforce tool restrictions for all agents, even if already restricted via `tools` field.

### Priority 3: Consider Model Optimization (COST SAVINGS)
Test Sonnet for UX Designer, Implementer, and Researcher. Measure quality vs. cost.

### Priority 4: Add Hooks for Quality Gates (FUTURE ENHANCEMENT)
Add `afterAgent` hooks for validation, starting with Implementer and Reviewer.

---

## Implementation Plan

### Phase 1: Enforce Read-Only (Immediate)

**shipkit-reviewer-agent.md** - Add to frontmatter:
```yaml
disallowedTools: Write, Edit, Bash, NotebookEdit
```

**shipkit-researcher-agent.md** - Add to frontmatter:
```yaml
disallowedTools: Write, Edit, Bash, NotebookEdit
```

### Phase 2: Explicit Tool Restrictions (Short-term)

**shipkit-product-owner-agent.md** - Add:
```yaml
disallowedTools: Bash, NotebookEdit
```

**shipkit-ux-designer-agent.md** - Add:
```yaml
disallowedTools: Bash, NotebookEdit
```

**shipkit-architect-agent.md** - Add:
```yaml
disallowedTools: NotebookEdit
```

**shipkit-project-manager-agent.md** - Add:
```yaml
disallowedTools: NotebookEdit
```

### Phase 3: Model Optimization Testing (Medium-term)

1. Create test scenarios for each agent
2. Run UX Designer, Implementer, Researcher with `model: sonnet`
3. Compare output quality and cost
4. Update model settings based on results

### Phase 4: Hooks Implementation (Future)

1. Verify hook syntax in Claude Code documentation
2. Add `afterAgent` hook to Implementer (test/lint validation)
3. Add `beforeAgent` hook to Project Manager (status loading)
4. Monitor for performance impact

---

## Summary Table

| Agent | `permissionMode` | `disallowedTools` | `hooks` | `model` |
|-------|-----------------|-------------------|---------|---------|
| product-owner | `acceptEdits` (keep) | Add: `Bash, NotebookEdit` | Optional | `opus` (keep) |
| ux-designer | `acceptEdits` (keep) | Add: `Bash, NotebookEdit` | Optional | Test `sonnet` |
| architect | `acceptEdits` (keep) | Add: `NotebookEdit` | `afterAgent` | `opus` (keep) |
| implementer | `default` (keep) | None | `afterAgent` | Test `sonnet` |
| reviewer | `default` (keep) | Add: `Write, Edit, Bash, NotebookEdit` | `afterAgent` | `opus` (keep) |
| researcher | `default` (keep) | Add: `Write, Edit, Bash, NotebookEdit` | Optional | Test `sonnet` |
| project-manager | `acceptEdits` (keep) | Add: `NotebookEdit` | `beforeAgent` | `opus` (keep) |
