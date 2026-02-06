# Shipkit Skills Improvement Specification

**Created**: 2026-02-03
**Status**: Active
**Source**: Claude Code official documentation and CHANGELOG

---

## Overview

This spec documents Claude Code features that can improve Shipkit skills. Each feature includes:
- Official documentation reference
- Which Shipkit skills benefit
- Specific implementation guidance

---

## Feature 1: AskUserQuestion Tool

### Official Documentation

The `AskUserQuestion` tool allows Claude to present structured questions with selectable options to users during execution.

**Tool Parameters:**
```typescript
{
  questions: [{
    question: string,        // Clear question ending with "?"
    header: string,          // Short label (max 12 chars) for chip/tag
    options: [{
      label: string,         // Display text (1-5 words)
      description: string    // Explanation of option
    }],                      // 2-4 options, "Other" added automatically
    multiSelect: boolean     // Allow multiple selections (default: false)
  }],                        // 1-4 questions per call
  metadata?: {
    source?: string          // Optional analytics tracking
  }
}
```

**Key Rules:**
- Users can always select "Other" to provide custom text input
- Use `multiSelect: true` when choices aren't mutually exclusive
- Add "(Recommended)" to first option if you have a preference
- 2-4 options per question, 1-4 questions per call
- Max 12 chars for header

### Skills to Improve

| Skill | Current Behavior | Improvement |
|-------|------------------|-------------|
| `shipkit-spec` | Asks 2-3 clarifying questions as plain text | Use AskUserQuestion with structured options for common choices |
| `shipkit-plan` | Asks about complexity level as plain text | Use AskUserQuestion: "Quick POC plan or detailed plan?" |
| `shipkit-product-discovery` | Asks about persona types | Use AskUserQuestion for persona selection |
| `shipkit-why-project` | Asks about project type/goals | Use AskUserQuestion for strategic choices |
| `shipkit-architecture-memory` | Asks about decision category | Use AskUserQuestion for architecture patterns |
| `shipkit-prototyping` | Asks about prototype scope | Use AskUserQuestion for fidelity level |

### Implementation Example

**For `shipkit-spec` Step 1 (Understand the Feature):**

```markdown
### Step 1: Understand the Feature

Use AskUserQuestion tool to gather requirements:

**Question 1 - Feature Type:**
- header: "Type"
- question: "What type of feature are you specifying?"
- options:
  - label: "User-facing UI"
    description: "Forms, dashboards, navigation, visual components"
  - label: "API/Backend"
    description: "Endpoints, services, data processing"
  - label: "Integration"
    description: "Third-party services, webhooks, external APIs"
  - label: "Infrastructure"
    description: "Auth, caching, database changes"

**Question 2 - Complexity:**
- header: "Scope"
- question: "How complex is this feature?"
- options:
  - label: "Simple (Recommended)"
    description: "Single component/endpoint, minimal state"
  - label: "Medium"
    description: "Multiple components, some state management"
  - label: "Complex"
    description: "Cross-cutting concerns, significant architecture"
```

---

## Feature 2: Task System

### Official Documentation

Claude Code has a built-in task management system with these tools:

**TaskCreate:**
```typescript
{
  subject: string,      // Brief title in imperative form ("Fix auth bug")
  description: string,  // Detailed requirements
  activeForm?: string   // Present continuous for spinner ("Fixing auth bug")
}
```

**TaskUpdate:**
```typescript
{
  taskId: string,
  status?: "pending" | "in_progress" | "completed" | "deleted",
  addBlockedBy?: string[],  // Task IDs that must complete first
  addBlocks?: string[]      // Task IDs waiting on this one
}
```

**TaskList:** Returns all tasks with status, owner, blockedBy

**TaskGet:** Returns full task details by ID

**Key Rules:**
- Create tasks for complex multi-step tasks (3+ steps)
- Mark task as `in_progress` BEFORE starting work
- Mark `completed` only when FULLY done (not on errors)
- Prefer working on tasks in ID order (lower first)
- Tasks persist at `~/.claude/tasks/{sessionId}/*.json`

### Skills to Improve

| Skill | Current Behavior | Improvement |
|-------|------------------|-------------|
| `shipkit-plan` | Writes plan to file only | Also create Task items for each phase |
| `shipkit-work-memory` | Saves resume point to progress.md | Also surface pending Tasks in resume |
| `shipkit-project-status` | Reports health check | Include Task status in report |
| `shipkit-master` | Orchestrates workflow | Track skill execution as Tasks |

### Implementation Example

**For `shipkit-plan` Phase Generation:**

```markdown
### Step 3.5: Create Implementation Tasks

After generating the plan, create Task items for tracking:

**For each phase in the plan:**
1. Create a TaskCreate for the phase
2. Set dependencies with addBlockedBy
3. User can track progress via TaskList

Example:
- Task 1: "Set up database schema" (no blockers)
- Task 2: "Implement API endpoints" (blockedBy: Task 1)
- Task 3: "Build UI components" (blockedBy: Task 2)
- Task 4: "Add tests" (blockedBy: Task 2, Task 3)

**Why:** User can see implementation progress at a glance, Claude tracks what's done.
```

---

## Feature 3: context: fork (Subagent Isolation)

### Official Documentation

Skills can run in isolated subagent context using `context: fork` frontmatter:

```yaml
---
name: my-skill
description: Does something
context: fork
allowed-tools:
  - Read
  - Grep
  - Glob
model: haiku
---
```

**Key Properties:**
- Runs skill in separate context window
- Preserves main conversation context
- Can restrict tools with `allowed-tools`
- Can specify model (`sonnet`, `opus`, `haiku`, `inherit`)
- Subagent receives only skill system prompt + basic environment
- Results return summary to main conversation
- **Subagents cannot spawn other subagents**

**When to Use:**
- High-volume output operations (test runs, large scans)
- Read-only verification that shouldn't pollute main context
- Tasks that produce verbose output but only need summary

### Skills to Improve

| Skill | Current Behavior | Improvement |
|-------|------------------|-------------|
| `shipkit-verify` | Runs in main context | Use `context: fork` with read-only tools |
| `shipkit-preflight` | Runs in main context | Use `context: fork` for production audit |
| `shipkit-codebase-index` | Scans entire codebase | Use `context: fork` with `model: haiku` |
| `shipkit-project-context` | Scans codebase for stack | Use `context: fork` for initial scan |

### Implementation Example

**For `shipkit-verify`:**

```yaml
---
name: shipkit-verify
description: Review recent changes across 12 quality dimensions
context: fork
model: sonnet
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---
```

**Benefits:**
- Verification output doesn't consume main context
- Can scan many files without impacting conversation
- Summary returns to main conversation
- Model can be cheaper for bulk operations

---

## Feature 4: Memory @imports Syntax

### Official Documentation

CLAUDE.md files can import other files using `@path/to/file` syntax:

```markdown
See @README for project overview and @package.json for available commands.

# Additional Instructions
- Git workflow @docs/git-instructions.md
```

**Key Rules:**
- Relative paths resolve from file containing the import
- Absolute paths supported
- First-time imports show approval dialog
- Max depth: 5 hops for recursive imports
- Not evaluated inside code spans/blocks
- Use `CLAUDE.local.md` for private per-project preferences
- For worktrees: `@~/.claude/my-project-instructions.md`

### Skills to Improve

| Skill | Current Behavior | Improvement |
|-------|------------------|-------------|
| `shipkit-claude-md` | Manages CLAUDE.md directly | Support @imports for modular instructions |
| `shipkit-master` | Loads full master prompt | Use @imports for skill references |

### Implementation Example

**For installed CLAUDE.md (shipkit.md template):**

```markdown
# Project Instructions

## Core Context
@.shipkit/stack.md
@.shipkit/architecture.md

## Active Work
@.shipkit/progress.md

## Workflow
See SKILL.md files in .claude/skills/ for available commands.
```

**Benefits:**
- CLAUDE.md stays concise
- Context files loaded on demand
- User can see exactly what's imported via `/memory`

---

## Feature 5: argument-hint Frontmatter

### Official Documentation

Skills can provide argument hints displayed in slash command menu:

```yaml
---
name: shipkit-spec
description: Create feature specification
argument-hint: "<feature name or description>"
---
```

**Display:** `/shipkit-spec <feature name or description>`

**Key Rules:**
- Shows in command palette/autocomplete
- Helps users understand expected input
- Keep hints concise and helpful

### Skills to Improve

**All user-invocable skills should add argument-hint:**

| Skill | Suggested Hint |
|-------|----------------|
| `shipkit-spec` | `<feature name or description>` |
| `shipkit-plan` | `[spec name]` |
| `shipkit-verify` | `[scope or feature]` |
| `shipkit-prototyping` | `<component or feature>` |
| `shipkit-architecture-memory` | `<decision to log>` |
| `shipkit-work-memory` | `[checkpoint name]` |
| `shipkit-project-status` | _(no argument needed)_ |
| `shipkit-get-skills` | `<search query>` |
| `shipkit-get-mcps` | `<search query>` |

### Implementation Example

**For `shipkit-spec`:**

```yaml
---
name: shipkit-spec
description: "Use when user describes a feature to build."
argument-hint: "<feature name or description>"
---
```

---

## Feature 6: allowed-tools Restrictions

### Official Documentation

Skills can restrict available tools with `allowed-tools`:

```yaml
---
name: read-only-skill
description: Analyzes code without modifications
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---
```

**Available Tools:**
- Read, Write, Edit
- Glob, Grep
- Bash
- Task (subagent spawning)
- WebFetch, WebSearch
- MCP tools (mcp__server__tool)
- AskUserQuestion
- TaskCreate, TaskUpdate, TaskList, TaskGet

**Key Rules:**
- Omit to inherit all tools
- Use `disallowed-tools` for denylist approach
- Tool restrictions apply for skill duration

### Skills to Improve

| Skill | Recommended Tools |
|-------|-------------------|
| `shipkit-verify` | Read, Glob, Grep, Bash (no Write/Edit) |
| `shipkit-preflight` | Read, Glob, Grep, Bash (no Write/Edit) |
| `shipkit-project-status` | Read, Glob, Grep, Bash (no Write/Edit) |
| `shipkit-codebase-index` | Read, Glob, Grep, Write (index output only) |

---

## Feature 7: Model Selection

### Official Documentation

Skills can specify which model to use:

```yaml
---
name: my-skill
model: haiku
---
```

**Options:**
- `sonnet` - Balanced capability and speed
- `opus` - Most capable
- `haiku` - Fastest, cheapest
- `inherit` - Use conversation model (default)

**When to Use:**
- `haiku` for high-volume scanning, simple lookups
- `sonnet` for balanced analysis
- `opus` for complex reasoning (rarely needed)

### Skills to Improve

| Skill | Recommended Model | Reason |
|-------|-------------------|--------|
| `shipkit-codebase-index` | haiku | High-volume file scanning |
| `shipkit-verify` | sonnet | Balanced analysis |
| `shipkit-preflight` | sonnet | Production audit needs good reasoning |
| `shipkit-detect` | haiku | Pattern matching only |

---

## Feature 8: Hooks in Skill Frontmatter

### Official Documentation

Skills can define lifecycle hooks in frontmatter:

```yaml
---
name: my-skill
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
  Stop:
    - hooks:
        - type: prompt
          prompt: "Verify skill completed all requirements: $ARGUMENTS"
---
```

**Supported Events:**
- PreToolUse, PostToolUse, PostToolUseFailure
- PermissionRequest
- Stop (converted to SubagentStop for subagents)
- All standard hook events

**Hook Types:**
- `command` - Run shell script
- `prompt` - LLM evaluation (returns {ok: true/false})
- `agent` - Multi-turn subagent with tool access

### Skills to Improve

| Skill | Hook Opportunity |
|-------|------------------|
| `shipkit-verify` | Stop hook: verify all dimensions reviewed |
| `shipkit-spec` | Stop hook: verify spec completeness |
| `shipkit-plan` | Stop hook: verify all phases defined |

---

## Feature 9: once Flag for Single-Fire Hooks

### Official Documentation

Skills can define hooks that run only once per session:

```yaml
---
name: my-skill
hooks:
  SessionStart:
    - hooks:
        - type: command
          command: "./setup.sh"
          once: true
---
```

**Use Case:** Initialization that shouldn't repeat on session resume.

---

## Implementation Priority

### Phase 1: Quick Wins (Frontmatter Only)
1. Add `argument-hint` to all user-invocable skills
2. Add `model: haiku` to scanning skills
3. Add `allowed-tools` restrictions to read-only skills

### Phase 2: AskUserQuestion Integration
4. Update `shipkit-spec` with structured questions
5. Update `shipkit-plan` with structured questions
6. Update `shipkit-product-discovery` with structured questions

### Phase 3: Context Isolation
7. Add `context: fork` to `shipkit-verify`
8. Add `context: fork` to `shipkit-preflight`
9. Add `context: fork` to `shipkit-codebase-index`

### Phase 4: Task System Integration
10. Update `shipkit-plan` to create Tasks
11. Update `shipkit-work-memory` to surface Tasks
12. Update `shipkit-project-status` to show Tasks

### Phase 5: Advanced Features
13. Add Stop hooks for completion verification
14. Update CLAUDE.md template with @imports
15. Update `shipkit-master` to leverage @imports

---

## Acceptance Criteria

### Must Have
- [x] All user-invocable skills have `argument-hint`
- [x] Read-only skills use `allowed-tools`
- [x] Scanning skills use `model: haiku`
- [x] `shipkit-spec` uses AskUserQuestion guidance
- [x] `shipkit-plan` uses AskUserQuestion guidance
- [x] `shipkit-product-discovery` uses AskUserQuestion guidance

### Should Have (Deferred)
- [ ] Verification skills use `context: fork` (needs testing)
- [ ] `shipkit-plan` creates Tasks
- [ ] CLAUDE.md template uses @imports

### Won't Have (this iteration)
- [ ] Agent-based hooks (complex, needs validation)
- [ ] MCP tool restrictions (no MCPs yet)

---

## Reference Documentation

- **Skills:** https://code.claude.com/docs/en/skills
- **Subagents:** https://code.claude.com/docs/en/sub-agents
- **Hooks:** https://code.claude.com/docs/en/hooks
- **Memory:** https://code.claude.com/docs/en/memory
- **CHANGELOG:** https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md

---

<!-- Shipkit v1.1.0 -->
