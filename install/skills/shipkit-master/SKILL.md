---
name: shipkit-master
description: Orchestrator that manages context loading at session start and routes user requests to appropriate shipkit skills. Auto-loaded via session-start hook.
---

# shipkit-master - Lightweight Orchestration & Routing

**Purpose**: Session orchestrator that checks file freshness, loads context efficiently, and routes user requests to appropriate shipkit skills.

**Role**: THE master orchestrator for Shipkit. Loaded automatically at every session start.

---

## Why This Skill Exists

**You don't naturally know what skills are available.**

This skill provides:
1. **Discoverability** - Routing tables tell you what skills exist
2. **Context efficiency** - Load only what's needed, when needed
3. **Workflow guidance** - Match user intent to appropriate skills

---

## When to Invoke

**Auto-invoked**:
- Every session start (via session-start hook)
- Hook outputs this SKILL.md to Claude's context
- User never explicitly calls this skill

**What triggers auto-loading:**
- Opening Claude Code in a project with Shipkit installed
- SessionStart hook detects `.claude/skills/shipkit-master/` and loads it

---

## Prerequisites

**Installation requirements**:
- `.claude/hooks/shipkit-session-start.py` exists and loads this skill
- `.claude/skills/shipkit-master/SKILL.md` exists (this file)
- Other skills installed in `.claude/skills/shipkit-*/`

**First-time users**:
- If `.shipkit/stack.md` missing → Suggest `/shipkit-project-context` to create it
- If no specs/plans exist → Suggest starting with `/shipkit-spec` or `/shipkit-product-discovery`

---

## Process

### Step 1: Session Start (Auto-Execution)

**When session starts:**
1. Hook runs and outputs this SKILL.md to context
2. Check file freshness (see `references/file-freshness-logic.md`)
3. Load fresh context files:
   - `.shipkit/stack.md` (if fresh and exists)
   - `.shipkit/architecture.md` (if exists)
   - `.shipkit/why.md` (if exists)
4. Display session start message with freshness warnings

---

### Step 2: Match User Intent to Skills

**When user sends message:**
1. Analyze message for keywords
2. Match to skill category (see routing tables below)
3. Route to appropriate skill
4. Let that skill load its required context

**Routing hierarchy** (processed in order):
1. Vision/Discovery keywords → Route to vision skills
2. Context/Status keywords → Route to context skills
3. Specification keywords → Route to spec/plan skills
4. Knowledge keywords → Route to persistence skills
5. Quality keywords → Route to quality skills
6. Ambiguous → Ask clarifying question

---

### Step 3: Load Context on Demand

**Context loading strategy:**
- Session start: ~500 tokens (master + stack + architecture)
- Per skill: ~1500-2500 tokens (skill + specific context)
- **Never load all context upfront**

---

## Core Responsibilities

1. **File Freshness Checking** - Determine if cached context is stale
2. **Lazy Context Loading** - Load only what's needed for current task
3. **Request Routing** - Match user intent to appropriate shipkit skill
4. **Skill Discoverability** - Let Claude know what skills exist

---

## Skill Routing Table

### Vision & Discovery

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "Define vision", "Why this project?", "Project goals" | `/shipkit-why-project` | .shipkit/why.md |
| "Who are our users?", "Create personas", "User research", "User journey" | `/shipkit-product-discovery` | .shipkit/why.md, stack.md |

### Context & Status

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "Show status", "Project health", "What's missing?" | `/shipkit-project-status` | All .shipkit/ (glob scan) |
| "Scan project", "Generate stack", "What's my tech stack?" | `/shipkit-project-context` | package.json, .env.example |
| "Index codebase", "Map project", "Create index", "Update index" | `/shipkit-codebase-index` | None (generates from git) |
| "Log progress", "Session summary", "What did we do?", "Checkpoint", "Save state", "End session" | `/shipkit-work-memory` | .shipkit/progress.md |
| "Help", "What skills exist?", "What can you do?" | List all shipkit skills | None |
| "Find skills", "Get skills", "Is there a skill for?", "Install skill" | `/shipkit-get-skills` | None |
| "Find MCPs", "Get MCPs", "Is there an MCP for?", "Install MCP" | `/shipkit-get-mcps` | .mcp.json |

### Specification & Planning

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "Spec this feature", "Create specification", "Write requirements" | `/shipkit-spec` | .shipkit/specs/active/ |
| "Plan this", "How to implement?", "Create plan" | `/shipkit-plan` | specs/, stack.md, architecture.md |
| "Prototype", "Mockup", "Rapid prototype", "UI mockup" | `/shipkit-prototyping` | specs/, why.md |
| "Extract prototype", "Prototype to spec", "Capture UI patterns" | `/shipkit-prototype-to-spec` | .shipkit-mockups/, specs/active/ |

### Knowledge Persistence

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "Log this decision", "Architecture choice", "Why did we choose X?" | `/shipkit-architecture-memory` | .shipkit/architecture.md |
| "Define data shapes", "Type definitions", "Data contracts" | `/shipkit-data-contracts` | .shipkit/types.md |
| "Fetch integration docs", "API patterns", "Service integration" | `/shipkit-integration-docs` | .shipkit/stack.md |
| "Remember this", "Save this", "Update CLAUDE.md", "Add to CLAUDE.md" | `/shipkit-claude-md` | CLAUDE.md |

### Quality & Communication

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "Verify", "Check my work", "Ready to commit?", "Review changes" | `/shipkit-verify` | Git diff, specs, architecture |
| "Preflight", "Production ready", "Ready to ship?", "Go live", "Launch check" | `/shipkit-preflight` | stack.md, why.md, architecture.md |
| "Audit UX", "Check UX patterns", "UX gaps" | `/shipkit-ux-audit` | implementations/ |
| "Create task", "Track TODO", "User tasks" | `/shipkit-user-instructions` | user-tasks/active.md |
| "Visualize", "HTML report", "Visual communication" | `/shipkit-communications` | Relevant files based on request |

---

## What Doesn't Need a Skill

| User Says | Just Do It |
|-----------|------------|
| "Build this", "Implement", "Start coding" | Implement using spec/plan |
| "Bug", "Error", "Not working", "Broken" | Debug systematically |
| "Write tests" | Write tests alongside code |
| "Document this code" | Add comments/docstrings |
| "Refactor this" | Refactor as requested |

**These are Claude's natural capabilities. No skill needed.**

---

## Special Behaviors

### 1. Enforce Skill Usage for Protected Files

**Prevent manual editing of `.shipkit/` context files:**

If user tries to manually edit:
```
Use the appropriate skill instead:
  • stack.md → /shipkit-project-context
  • specs/* → /shipkit-spec
  • plans/* → /shipkit-plan
  • architecture.md → /shipkit-architecture-memory
```

**Exception**: User can read files manually anytime.

---

### 2. Progressive Disclosure

**Never load all context at once.**

```
Session start → Load master + stack + architecture (~400 tokens)
User asks to plan → Load relevant spec + stack (~1500 tokens)
User asks about component → Load component docs (~1000 tokens)
```

---

## Context Files This Skill Reads

**At session start:**
- `.shipkit/stack.md` - Tech stack context
- `.shipkit/architecture.md` - Architecture decisions
- `.shipkit/why.md` - Project vision
- `package.json` - For freshness comparison

**During routing:**
- Routing relies on internal keyword tables (no file reads)
- Context files loaded AFTER routing, by the invoked skill

---

## Context Files This Skill Writes

**Write Strategy: READ-ONLY** (This skill does not write files)

- Master's role is orchestration, not execution
- Execution happens in routed skills
- Keeps master skill focused and lightweight

---

## When This Skill Integrates with Others

### Relationship: Orchestrator

This skill is the **central router** that connects all other skills.

**Loads at Session Start:**
- Auto-loaded via `shipkit-session-start.py` hook
- First skill loaded in every session
- Provides routing tables and context loading strategy

**Routes TO All Skills:**

| Category | Skills Routed To |
|----------|------------------|
| Vision/Discovery | `shipkit-why-project`, `shipkit-product-discovery` |
| Context/Status | `shipkit-project-status`, `shipkit-project-context`, `shipkit-work-memory` |
| Spec/Planning | `shipkit-spec`, `shipkit-plan`, `shipkit-prototyping`, `shipkit-prototype-to-spec` |
| Knowledge | `shipkit-architecture-memory`, `shipkit-data-contracts`, `shipkit-integration-docs`, `shipkit-claude-md` |
| Quality | `shipkit-verify`, `shipkit-ux-audit`, `shipkit-user-instructions`, `shipkit-communications` |

**Does NOT Route:**
- Natural capabilities (implement, debug, test, refactor) - Claude handles directly
- System skills (`shipkit-detect`) - triggered by hooks, not user requests

**Context Flow:**
1. Master loads lightweight context at session start (~400-500 tokens)
2. User request arrives
3. Master routes to appropriate skill
4. Target skill loads its specific context
5. Execution happens in target skill

---

<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Has important context been saved to `.shipkit/`?
2. **Prerequisites** - Does the next action need a spec or plan first?
3. **Session length** - Long session? Consider `/shipkit-work-memory` for continuity.

**Natural capabilities** (no skill needed): Implementation, debugging, testing, refactoring, code documentation.

**Suggest skill when:** User needs to make decisions, create persistence, or check project status.
<!-- /SECTION:after-completion -->

<!-- SECTION:success-criteria -->
## Success Criteria

- [ ] Session starts load ~400-500 tokens (not thousands)
- [ ] User requests route to correct skills based on keywords
- [ ] Context loads on demand (not upfront)
- [ ] Ambiguous requests trigger clarifying questions
- [ ] Skills are discoverable (user can ask "what skills exist?")
<!-- /SECTION:success-criteria -->
---

## Reference Documentation

- **File freshness logic** - `references/file-freshness-logic.md`
- **Session start behavior** - `references/session-start-behavior.md`
- **Routing patterns** - `references/routing-patterns.md`
- **Context loading table** - `references/context-loading-table.md`

---

**Remember:** This skill is the traffic controller. It routes efficiently, loads lazily, and makes skills discoverable. Every session starts here.

<!-- Shipkit v1.1.0 -->
