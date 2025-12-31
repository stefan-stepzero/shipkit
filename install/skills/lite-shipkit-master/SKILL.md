---
name: lite-shipkit-master
description: Orchestrator that enforces skill usage, manages intelligent context loading at session start, and routes user requests to appropriate lite skills. Auto-loaded via session-start hook.
---

# shipkit-master-lite - Lightweight Orchestration & Routing

**Purpose**: Session orchestrator that checks file freshness, loads context efficiently, and routes user requests to appropriate lite skills based on keywords and project state.

**Role**: THE master orchestrator for Shipkit Lite. Loaded automatically at every session start via `.claude/hooks/session-start.sh`.

---

## When to Invoke

**Auto-invoked**:
- Every session start (via session-start.sh hook)
- Hook outputs this SKILL.md to Claude's context
- User never explicitly calls this skill

**What triggers auto-loading:**
- Opening Claude Code in a project with Shipkit Lite installed
- SessionStart hook detects `.claude/skills/lite-shipkit-master/` and loads it
- Becomes available in context for routing all subsequent user requests

**Manual reference** (rare):
- When user asks: "What should I do?", "Help me decide next steps", "What's available?"
- These questions trigger routing logic defined in this skill

---

## Prerequisites

**Installation requirements**:
- `.claude/hooks/session-start.sh` exists and executes this skill
- `.claude/skills/lite-shipkit-master/SKILL.md` exists (this file)
- Other lite skills installed in `.claude/skills/lite-*/`
- Settings configured to allow SessionStart hook

**Optional but recommended**:
- `.shipkit-lite/stack.md` - Enables freshness checking and context loading
- `.shipkit-lite/architecture.md` - Loaded at session start if exists
- Manifest and routing tables updated with all available skills

**First-time users**:
- If `.shipkit-lite/stack.md` missing → Skill suggests `/lite-project-context` to create it
- If no specs/plans exist → Skill suggests starting with `/lite-spec` or `/lite-project-status`

---

## Process

### Step 1: Session Start (Auto-Execution)

**When session starts:**
1. Hook runs and outputs this SKILL.md to context (~200 tokens)
2. Check file freshness (see `references/file-freshness-logic.md`)
3. Load fresh context files:
   - `.shipkit-lite/stack.md` (if fresh and exists)
   - `.shipkit-lite/architecture.md` (if exists, append-only)
4. Display session start message with freshness warnings

**See `references/session-start-behavior.md` for complete hook implementation**

---

### Step 2: Match User Intent to Skills

**When user sends message:**
1. Analyze message for keywords
2. Match to skill category (meta, decision, implementation, documentation, quality)
3. Route to appropriate skill
4. Load required context for that skill

**Routing hierarchy** (processed in order):
1. Meta keywords → Route to meta skills
2. Decision keywords → Route to decision skills
3. Implementation keywords → Route to implementation skills
4. Documentation keywords → Route to documentation skills
5. Quality keywords → Route to quality/process skills
6. Ambiguous → Ask clarifying question

**See `references/routing-patterns.md` for complete decision tree**

---

### Step 3: Load Context on Demand

**For each routed skill:**
1. Check context loading table (see below)
2. Load only required files (not everything)
3. Invoke skill with loaded context
4. Skill executes its logic

**Context loading strategy:**
- Session start: ~500 tokens (master + stack + architecture)
- Per skill: ~1500-2500 tokens (skill + specific context)
- **Never load all context upfront** (saves 85-90% tokens vs loading everything)

**See `references/context-loading-table.md` for complete table**

---

### Step 4: Suggest Next Skill

**After skill completes:**
1. Determine logical next step based on workflow
2. Suggest specific skill to user
3. Explain why that skill comes next
4. Wait for user confirmation

**Examples:**
- After `/lite-spec` → Suggest `/lite-plan`
- After `/lite-plan` → Suggest `/lite-implement`
- After `/lite-implement` → Suggest `/lite-quality-confidence` or `/lite-component-knowledge`

**See `references/routing-patterns.md` for complete suggestion table**

---

## Core Responsibilities

1. **File Freshness Checking** - Determine if cached context is stale (see `references/file-freshness-logic.md`)
2. **Lazy Context Loading** - Load only what's needed for current task (see `references/context-loading-table.md`)
3. **Request Routing** - Match user intent to appropriate lite skill (see routing tables below)
4. **Context Mapping** - Tell Claude which files to read for each skill (see Process Step 3)
5. **Next Step Suggestions** - Guide workflow progression (see `references/routing-patterns.md`)

---

## Skill Routing Table

**Match user intent to appropriate lite skill:**

### Meta/Infrastructure Keywords

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "What's next?", "What should I do?", "Where do I start?", "What now?" | `/lite-whats-next` | All .shipkit-lite/ files (glob scan) |
| "Define vision", "Why this project?", "What's this about?", "Project goals" | `/lite-why-project` | .shipkit-lite/why.md (if exists) |
| "Who are our users?", "Create personas", "User research", "Product discovery", "User journey", "User stories" | `/lite-product-discovery` | .shipkit-lite/why.md, .shipkit-lite/stack.md |
| "Show status", "Project health" | `/lite-project-status` | All .shipkit-lite/ files (glob scan) |
| "Scan project", "Generate stack", "Refresh context", "What's my tech stack?" | `/lite-project-context` | package.json, .env.example, migrations/ |
| "Help", "What skills exist?", "What can you do?" | List all lite skills | None |

### Decision & Design Keywords

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "Log this decision", "Architecture choice", "Why did we choose X?" | `/lite-architecture-memory` | .shipkit-lite/architecture.md |
| "Audit UX", "Check UX patterns", "Missing UX features", "UX gaps" | `/lite-ux-audit` | .shipkit-lite/implementations.md |
| "Fetch integration docs", "Current API patterns", "Service integration help" | `/lite-integration-docs` | .shipkit-lite/stack.md (determine services) |
| "Validate data contracts", "Check type alignment", "Define data shapes" | `/lite-data-contracts` | .shipkit-lite/types.md, component-contracts.md |

### Implementation Workflow Keywords

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "Spec this feature", "Create specification", "Write requirements" | `/lite-spec` | .shipkit-lite/specs/active/ |
| "Prototype", "Mockup", "Rapid prototype", "UI mockup" | `/lite-prototyping` | specs/, why.md |
| "Extract prototype", "Prototype to spec", "Document prototype learnings", "Capture UI patterns" | `/lite-prototype-to-spec` | .shipkit-mockups/, specs/active/ |
| "Plan this", "How to implement?", "Create plan" | `/lite-plan` | specs/, stack.md, architecture.md |
| "Build this", "Start coding", "Implement" | `/lite-implement` | plans/, specs/, stack.md |

### Documentation Keywords

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "Document component", "How does X work?", "Component docs" | `/lite-component-knowledge` | .shipkit-lite/implementations.md |
| "Document route", "API endpoint docs", "Route docs" | `/lite-route-knowledge` | .shipkit-lite/implementations.md |
| "Create docs", "Write guide", "Documentation" | `/lite-document-artifact` | .shipkit-lite/docs/ |
| "Visualize", "HTML report", "Visual communication", "Create presentation" | `/lite-communications` | Relevant .shipkit-lite/ files based on request |

### Process & Quality Keywords

| User Says | Route To | Load Context |
|-----------|----------|--------------|
| "Bug", "Error", "Not working", "Broken", "Failing" | `/lite-debug-systematically` | specs/, implementations.md, architecture.md |
| "Pre-ship checklist", "Ready to ship?", "Quality check" | `/lite-quality-confidence` | implementations.md, specs/ |
| "Create task", "Track TODO", "User tasks" | `/lite-user-instructions` | .shipkit-lite/user-tasks/active.md |
| "Log progress", "Session summary", "What did we do?" | `/lite-work-memory` | .shipkit-lite/progress.md |

---

## Special Behaviors

### 1. Enforce Skill Usage

**shipkit-master-lite prevents manual file editing:**

If user tries to manually edit `.shipkit-lite/` files:
```
❌ "Don't edit .shipkit-lite/ files manually!"

Use the appropriate skill instead:
  • .shipkit-lite/stack.md → /lite-project-context
  • .shipkit-lite/specs/* → /lite-spec
  • .shipkit-lite/plans/* → /lite-plan
  • .shipkit-lite/implementations.md → /lite-component-knowledge or /lite-route-knowledge
  • .shipkit-lite/architecture.md → /lite-architecture-memory
```

**Exception**: User can read files manually anytime.

---

### 2. Progressive Disclosure

**Never load all context at once.**

**Good approach (Shipkit Lite way):**
```
Session start → Load master + stack + architecture (~400 tokens)
User asks to plan → Load relevant spec + stack (~1500 tokens)
User asks to implement → Load plan + stack (~1500 tokens)
```

**Total context across 3 interactions: ~3400 tokens** vs. loading everything upfront: ~5000 tokens

**Savings:** 32% fewer tokens, better focus.

**See `references/session-start-behavior.md` for token budget details**

---

## When This Skill Integrates with Others

### Before This Skill

**Installation & Setup:**
- `.claude/hooks/session-start.sh` must be configured to load this skill
  - **When**: During Shipkit Lite installation
  - **Why**: Enables auto-loading at session start
  - **Trigger**: User installs Shipkit Lite framework

### After This Skill

**All lite skills depend on this skill for routing:**

- **Every lite skill** - Receives routing and context loading from master
  - **When**: User sends any message after session start
  - **Why**: Master orchestrator routes all requests
  - **Trigger**: User intent matches skill keywords in routing table

**Specific examples:**

- `/lite-project-context` - Generates stack.md that master uses for freshness checking
  - **When**: First session or stale context detected
  - **Why**: Master needs stack.md to determine what context to load
  - **Trigger**: Master detects missing or stale stack.md at session start

- `/lite-spec` - Creates specs that master routes to from user requests
  - **When**: User says "spec this feature" or similar
  - **Why**: Master identifies "spec" keyword and routes appropriately
  - **Trigger**: Implementation workflow keywords matched

- `/lite-whats-next` - Gets routed from ambiguous "what should I do?" questions
  - **When**: User asks for guidance on next steps
  - **Why**: Master routes meta-questions to meta-skills
  - **Trigger**: Meta/infrastructure keywords matched

---

## Context Files This Skill Reads

**At session start (via hook):**
- `.shipkit-lite/stack.md` - Tech stack context (if fresh, ~100 tokens)
- `.shipkit-lite/architecture.md` - Architecture decisions (if exists, ~150 tokens)
- `package.json` - For freshness comparison (timestamp only)
- `.env.example` - For freshness comparison (timestamp only)

**During routing (for context loading decisions):**
- All routing relies on this skill's internal keyword tables (no file reads)
- Context files loaded AFTER routing, by the invoked skill (not by master)

**See `references/file-freshness-logic.md` for timestamp comparison logic**

---

## Context Files This Skill Writes

**Write Strategy: READ-ONLY** (This skill does not write files)

**This skill:**
- ❌ Does not create files
- ❌ Does not modify files
- ✅ Reads files at session start
- ✅ Routes to other skills that write files

**Why READ-ONLY:**
- Master's role is orchestration, not execution
- Execution happens in routed skills (spec, plan, implement, etc.)
- Keeps master skill focused and lightweight

**Files written by routed skills:**
- `.shipkit-lite/specs/` - Written by `/lite-spec`
- `.shipkit-lite/plans/` - Written by `/lite-plan`
- `.shipkit-lite/implementations.md` - Written by `/lite-component-knowledge`, `/lite-route-knowledge`
- `.shipkit-lite/architecture.md` - Written by `/lite-architecture-memory`
- `.shipkit-lite/progress.md` - Written by `/lite-work-memory`

---

## Success Criteria

shipkit-master-lite is working correctly when:

- [ ] Session starts load ~400-500 tokens (not thousands)
- [ ] File freshness is checked accurately at session start
- [ ] User requests route to correct skills based on keywords
- [ ] Context loads on demand (not upfront)
- [ ] Ambiguous requests trigger clarifying questions
- [ ] Manual edits to .shipkit-lite/ are discouraged
- [ ] Next skill suggestions are contextual and helpful
- [ ] Token budget stays under 3000 per session (start + 2-3 skill invocations)

---

## Reference Documentation

**For detailed implementation:**

- **File freshness logic** - `references/file-freshness-logic.md`
  - Timestamp comparison algorithm
  - Freshness warning examples
  - Token savings calculation

- **Session start behavior** - `references/session-start-behavior.md`
  - Hook implementation details
  - Loading strategy and token budget
  - Example session flows (fresh start, continuing work, stale context)

- **Routing patterns** - `references/routing-patterns.md`
  - Decision tree logic
  - Context loading instructions
  - Post-routing suggestions
  - Ambiguous intent handling

- **Context loading table** - `references/context-loading-table.md`
  - Which files to load for each skill
  - Token budget per skill invocation
  - Incremental loading strategy

---

**Remember:** shipkit-master-lite is the traffic controller. It routes efficiently, loads lazily, and keeps the workflow moving. Every session starts here. Every request flows through here.
