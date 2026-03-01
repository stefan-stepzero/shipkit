---
name: shipkit-master
description: Autonomous orchestrator that assesses project state, decides what to do next, and routes user requests to appropriate shipkit skills. Auto-loaded via session-start hook.
agent: shipkit-master
disable-model-invocation: true
---

# shipkit-master - Autonomous Orchestration & Routing

**Purpose**: Autonomous orchestrator that assesses project state, decides what to do next, invokes skills dynamically, and routes explicit requests via keyword matching.

**Role**: THE master orchestrator for Shipkit. Loaded automatically at every session start.

## Autonomous Mode — Goal-Driven Agent Hierarchy

When the `agent:` persona is loaded, the master operates in **autonomous mode** using a 4-agent hierarchy:

```
Master (orchestrator — checks goals, spawns responsible agent)
  ├── Visionary (WHY — stage, vision, strategic goals)
  ├── PM / Product Owner (WHAT — product definition, specs, product goals)
  ├── EM / Architect (HOW — architecture, plans, engineering goals)
  └── Execution Lead / Project Manager (DO — team implementation, verification)
```

**Decision loop:**
1. Read `.shipkit/goals/strategic.json`, `goals/product.json`, `goals/engineering.json`
2. Identify unmet criteria (priority: strategic > product > engineering)
3. Spawn the agent responsible for closing the gap
4. Evaluate results, re-check goals
5. Gate check with user at key transitions

**Examples:**
- No goals exist → spawn Visionary to bootstrap
- Strategic metrics unmet → spawn Visionary to adjust stage/strategy
- Product outcomes unmet → spawn PM to revise specs/definitions
- Engineering performance unmet → spawn EM to revise architecture
- All goals set, implementation pending → spawn Execution Lead

**The routing tables below remain as fallback** for explicit keyword-matched requests (e.g., "spec this feature" → `/shipkit-spec`). Both paths coexist — the agent handles ambiguous/open-ended requests, routing tables handle explicit ones.

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
- If `.shipkit/stack.json` missing → Suggest `/shipkit-project-context` to create it
- If no specs/plans exist → Suggest starting with `/shipkit-spec` or `/shipkit-product-discovery`

---

## Process

### Step 1: Session Start (Auto-Execution)

**When session starts:**
1. Hook runs and outputs this SKILL.md to context
2. Check file freshness (see `references/file-freshness-logic.md`)
3. Load fresh context files:
   - `.shipkit/stack.json` (if fresh and exists)
   - `.shipkit/architecture.json` (if exists)
   - `.shipkit/why.json` (if exists)
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
| "Define vision", "Why this project?", "Project goals" | `/shipkit-why-project` | .shipkit/why.json |
| "Who are our users?", "Create personas", "User research", "User journey" | `/shipkit-product-discovery` | .shipkit/why.json, stack.json |
| "Define solution", "Product definition", "What to build", "Features", "Differentiators" | `/shipkit-product-definition` | .shipkit/product-discovery.json, why.json |
| "Technical approach", "Engineering design", "How to build", "Mechanisms", "Components" | `/shipkit-engineering-definition` | .shipkit/product-definition.json, stack.json |
| "Success criteria", "Measure success", "Goals", "Stage gates", "How do we know it works" | `/shipkit-goals` | .shipkit/product-definition.json, engineering-definition.json |

### Context & Status

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "Show status", "Project health", "What's missing?" | `/shipkit-project-status` | All .shipkit/ (glob scan) |
| "Scan project", "Generate stack", "What's my tech stack?" | `/shipkit-project-context` | package.json, .env.example |
| "Index codebase", "Map project", "Create index", "Update index" | `/shipkit-codebase-index` | None (generates from git) |
| "Log progress", "Session summary", "What did we do?", "Checkpoint", "Save state", "End session" | `/shipkit-work-memory` | .shipkit/progress.json |
| "Help", "What skills exist?", "What can you do?" | List all shipkit skills | None |
| "Find skills", "Get skills", "Is there a skill for?", "Install skill" | `/shipkit-get-skills` | None |
| "Find MCPs", "Get MCPs", "Is there an MCP for?", "Install MCP" | `/shipkit-get-mcps` | .mcp.json |
| "Install Shipkit", "Update Shipkit", "Upgrade Shipkit", "Reinstall Shipkit" | `/shipkit-update` | None |


### Specification & Planning

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "Spec this feature", "Create specification", "Write requirements" | `/shipkit-spec` | .shipkit/specs/todo/ |
| "Triage feedback", "Process bug reports", "User testing feedback" | `/shipkit-feedback-bug` | .shipkit/specs/{todo,active}/, codebase-index |
| "Plan this", "How to implement?", "Create plan" | `/shipkit-plan` | specs/{todo,active}/, stack.json, architecture.json |
| "Help me think through", "Think with me", "Let's discuss", "What am I missing?" | `/shipkit-thinking-partner` | .shipkit/why.json, architecture.json |
| "Devil's advocate", "Pre-mortem", "Trade-offs", "I'm torn between" | `/shipkit-thinking-partner` | .shipkit/why.json, architecture.json |

### Knowledge Persistence

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "Log this decision", "Architecture choice", "Why did we choose X?" | `/shipkit-architecture-memory` | .shipkit/architecture.json |
| "Define data shapes", "Type definitions", "Data contracts" | `/shipkit-data-contracts` | .shipkit/contracts.json |
| "Fetch integration docs", "API patterns", "Service integration" | `/shipkit-integration-docs` | .shipkit/stack.json |
| "Remember this", "Save this", "Update CLAUDE.md", "Add to CLAUDE.md" | `/shipkit-claude-md` | CLAUDE.md |

### Quality & Communication

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "Verify", "Check my work", "Ready to commit?", "Review changes" | `/shipkit-verify` | Git diff, specs, architecture |
| "Preflight", "Production ready", "Ready to ship?", "Go live", "Launch check" | `/shipkit-preflight` | stack.json, why.json, architecture.json |
| "Scale ready", "Enterprise ready", "Scale audit", "Observability", "Reliability" | `/shipkit-scale-ready` | stack.json, architecture.json |
| "Audit UX", "Check UX patterns", "UX gaps" | `/shipkit-ux-audit` | implementations/ |
| "Create task", "Track TODO", "User tasks" | `/shipkit-user-instructions` | user-tasks/active.md |
| "Visualize", "HTML report", "Visual communication" | `/shipkit-communications` | Relevant files based on request |
| "Audit prompts", "Prompt architecture", "LLM pipeline review", "Check my prompts" | `/shipkit-prompt-audit` | stack.json, architecture.json |
| "Semantic QA", "Quality check", "Judge outputs", "QA suite", "Run QA" | `/shipkit-semantic-qa` | .shipkit/semantic-qa/config.json |
| "Visual QA", "UI testing", "Screenshot test", "Check the UI", "Playwright", "Test UI goals" | `/shipkit-qa-visual` | .shipkit/ui-goals.json |

### Execution

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "Test cases", "Generate tests", "What to test", "Test coverage", "Test specification" | `/shipkit-test-cases` | Source files, specs, existing test cases |
| "Build until", "Compile until success", "Fix build errors" | `/shipkit-build-relentlessly` | Build output |
| "Test until", "Run tests until green", "Fix test failures" | `/shipkit-test-relentlessly` | Test output, test-cases |
| "Lint until", "Fix lint errors", "Clean up lint" | `/shipkit-lint-relentlessly` | Lint output |
| "Implement independently", "Parallel implementation", "Work on this separately" | `/shipkit-implement-independently` | Spec, stack.json, architecture.json |
| "Create a team", "Team implement", "Build with a team", "Parallel team" | `/shipkit-team` | Plan, spec, stack.json, architecture.json |
| "Build this product", "Full pipeline", "End to end", "YOLO build" | `/shipkit-team --template pipeline` | All .shipkit/ |
| "Cleanup worktrees", "Clean up worktrees", "Remove old worktrees" | `/shipkit-cleanup-worktrees` | .shipkit/worktrees/ |

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
  • stack.json → /shipkit-project-context
  • specs/* → /shipkit-spec
  • plans/* → /shipkit-plan
  • architecture.json → /shipkit-architecture-memory
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
- `.shipkit/stack.json` - Tech stack context
- `.shipkit/architecture.json` - Architecture decisions
- `.shipkit/why.json` - Project vision
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
| Vision/Discovery | `shipkit-why-project`, `shipkit-product-discovery`, `shipkit-product-definition`, `shipkit-engineering-definition`, `shipkit-goals` |
| Context/Status | `shipkit-project-status`, `shipkit-project-context`, `shipkit-work-memory` |
| Spec/Planning | `shipkit-spec`, `shipkit-feedback-bug`, `shipkit-plan`, `shipkit-thinking-partner` |
| Knowledge | `shipkit-architecture-memory`, `shipkit-data-contracts`, `shipkit-integration-docs`, `shipkit-claude-md` |
| Quality | `shipkit-verify`, `shipkit-preflight`, `shipkit-scale-ready`, `shipkit-ux-audit`, `shipkit-prompt-audit`, `shipkit-semantic-qa`, `shipkit-qa-visual`, `shipkit-user-instructions`, `shipkit-communications` |

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
  - Freshness thresholds per file type
  - Staleness detection algorithm
  - Comparison logic (e.g., stack.json vs package.json)

---

**Remember:** This skill is the traffic controller. It routes efficiently, loads lazily, and makes skills discoverable. Every session starts here.