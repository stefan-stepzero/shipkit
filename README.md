# Shipkit - Streamlined Product Development Framework

A focused collection of **Claude Code skills** for efficient product development, from discovery to shipped code.

**<!-- sync:skill_count -->37<!-- /sync:skill_count --> skills** organized for streamlined workflow:
<!-- sync:readme_summary -->- **Vision & Discovery** (8) - why-project, product-discovery, project-context, ...
- **Spec & Planning** (4) - spec, feedback-bug, plan, ...
- **Knowledge & Memory** (5) - architecture-memory, data-contracts, integration-docs, ...
- **Execution** (7) - build-relentlessly, test-relentlessly, lint-relentlessly, ...
- **Quality & Communication** (9) - verify, preflight, scale-ready, ...
- **System** (3) - update, get-skills, get-mcps<!-- /sync:readme_summary -->

Plus **<!-- sync:agent_count -->10<!-- /sync:agent_count --> agent personas** that specialize behaviors for different workflow stages.

---

## What's Inside

### Skills (<!-- sync:skill_count -->37<!-- /sync:skill_count --> total)

All skills use the `shipkit-` prefix for clarity.

**Core Workflow (5 skills):**
- `shipkit-master` - Meta skill for workflow orchestration
- `shipkit-project-status` - Health check and gap analysis
- `shipkit-project-context` - Codebase scanning, stack detection
- `shipkit-codebase-index` - Semantic codebase indexing
- `shipkit-claude-md` - CLAUDE.md management

**Discovery & Planning (9 skills):**
- `shipkit-why-project` - Strategic vision definition
- `shipkit-product-discovery` - Personas, journeys, user needs
- `shipkit-product-definition` - Product blueprint (features, patterns, differentiators)
- `shipkit-engineering-definition` - Engineering blueprint (mechanisms, components, stack)
- `shipkit-goals` - Success criteria & stage gates
- `shipkit-spec` - Feature specification
- `shipkit-feedback-bug` - Process feedback into investigated bug specs (5 Whys root cause)
- `shipkit-plan` - Implementation planning
- `shipkit-thinking-partner` - Think through decisions with cognitive frameworks

**Implementation (3 skills):**
- `shipkit-architecture-memory` - Decision logging
- `shipkit-data-contracts` - Type definitions (Zod patterns)
- `shipkit-integration-docs` - Integration patterns

**Execution (7 skills):**
- `shipkit-test-cases` - Generate code-anchored test case specs
- `shipkit-build-relentlessly` - Build until compiles
- `shipkit-test-relentlessly` - Test until green
- `shipkit-lint-relentlessly` - Lint until clean
- `shipkit-implement-independently` - Parallel implementation in isolated worktree
- `shipkit-team` - Create agent team from implementation plan for parallel execution
- `shipkit-cleanup-worktrees` - Clean up stale implementation worktrees

**Quality & Documentation (10 skills):**
- `shipkit-verify` - QA and acceptance criteria
- `shipkit-preflight` - MVP production readiness audit
- `shipkit-scale-ready` - Scale & enterprise readiness audit
- `shipkit-prompt-audit` - LLM prompt architecture audit
- `shipkit-semantic-qa` - Semantic QA for API outputs and UI screenshots
- `shipkit-qa-visual` - Visual QA with Playwright: UI goals + autonomous test generation
- `shipkit-ux-audit` - UX analysis and patterns
- `shipkit-user-instructions` - User-facing documentation
- `shipkit-communications` - Communication and formatting
- `shipkit-work-memory` - Session memory and context

**System (3 skills):**
- `shipkit-update` - Install or update Shipkit from GitHub
- `shipkit-get-skills` - Discover and install Claude Code skills
- `shipkit-get-mcps` - Discover and install MCP servers

*System infrastructure (not counted — auto-triggered, not user-invocable):*
- `shipkit-detect` - Pattern detection and queue creation (hook infrastructure)

### Agent Personas (<!-- sync:agent_count -->10<!-- /sync:agent_count -->)

<!-- sync:readme_agent_table -->| Agent | Used For |
|-------|----------|
| `shipkit-project-manager-agent` | Coordination & context |
| `shipkit-product-owner-agent` | Vision & requirements |
| `shipkit-ux-designer-agent` | UI/UX design |
| `shipkit-architect-agent` | Technical decisions |
| `shipkit-implementer-agent` | Code implementation |
| `shipkit-implement-independently-agent` | Isolated parallel implementation |
| `shipkit-reviewer-agent` | Code review & quality |
| `shipkit-researcher-agent` | Research & analysis |
| `shipkit-thinking-partner-agent` | Cognitive discussion & thinking partner |<!-- /sync:readme_agent_table -->

---

## Quick Start

### Installation

```bash
cd your-project
npx shipkit-dev init
```

> **Pre-publish note:** Until the npm package is published, use:
> `npx github:stefan-stepzero/shipkit init`

Add `-y` for non-interactive mode (uses sensible defaults): `npx shipkit-dev init -y`

**Update an existing installation:**
```bash
npx shipkit-dev update
```

<details>
<summary>Alternative: Python installer</summary>

```bash
curl -O https://raw.githubusercontent.com/stefan-stepzero/shipkit/main/installers/install.py
python install.py --from-github
```
</details>

The installer will:
- Install all <!-- sync:skill_count -->37<!-- /sync:skill_count --> skills
- Set up <!-- sync:agent_count -->10<!-- /sync:agent_count --> agent personas
- Configure session hooks
- Create `.shipkit/` workspace

### After Installation

Your project will have:
```
your-project/
├── CLAUDE.md                    # User preferences & learnings (editable)
├── .claude/
│   ├── settings.json            # Permissions + hooks
│   ├── rules/
│   │   └── shipkit.md           # Framework rules (managed by /shipkit-update)
│   ├── skills/                  # 37 skill definitions
│   ├── agents/                  # 10 agent personas
│   └── hooks/                   # Session hooks
└── .shipkit/                    # Your workspace
    ├── specs/                   # Feature specifications
    ├── plans/                   # Implementation plans
    └── [context files...]       # Stack, architecture, etc.
```

### Basic Workflow

```
/shipkit-why-project         → Define vision & purpose (new projects)
    ↓
/shipkit-product-discovery   → Personas, pain points, journeys
    ↓
/shipkit-product-definition  → Product blueprint (features, patterns, differentiators)
    ↓
/shipkit-engineering-definition → Engineering blueprint (mechanisms, components)
    ↓
/shipkit-goals               → Success criteria & stage gates (feature phasing)
    ↓
/shipkit-spec                → Create feature specification
    ↓
/shipkit-plan                → Generate implementation plan
    ↓
(implement)                  → Build the feature (natural capability)
    ↓
/shipkit-verify              → Verify quality before commit
    ↓
/shipkit-work-memory         → Checkpoint progress for next session
```

> **Shortcut:** If you already know what to build, skip straight to `/shipkit-spec`. The discovery chain (why → discovery → product-definition → engineering-definition → goals) is most valuable for new products or when exploring problem space.

---

## How It Works

### 1. Session Hooks Enforce Skills

When Claude Code starts:
1. Runs session-start hook
2. Loads `shipkit-master` into context
3. Skills become the primary workflow method

### 2. Context Lives in `.shipkit/`

Your project context is stored in:
```
.shipkit/
├── specs/               # Feature specifications
├── plans/               # Implementation plans
├── architecture.json    # Architecture decisions
├── stack.json           # Technology stack
├── implementations.json   # What's been built
└── contracts.json       # Data contracts
```

### 3. Skills Chain Together

Skills naturally flow from one to another:

```
/shipkit-why-project → Defines vision
    → /shipkit-product-discovery → Understands users
    → /shipkit-product-definition → Defines what to build
    → /shipkit-engineering-definition → Designs how to build it
    → /shipkit-goals → Defines success criteria & phasing
    → /shipkit-spec → Creates feature spec
    → /shipkit-plan → Generates implementation plan
    → (implement) → Builds the feature
    → /shipkit-verify → Checks quality
```

---

## Repository Structure

```
shipkit/
├── cli/                             # npx CLI (zero dependencies)
│   ├── bin/shipkit.js               # Entry point
│   └── src/                         # Commands, prompts, utilities
│
├── install/                         # Everything that gets installed
│   ├── skills/                      # <!-- sync:skill_count -->37<!-- /sync:skill_count --> shipkit-* skill definitions
│   ├── agents/                      # <!-- sync:agent_count -->10<!-- /sync:agent_count --> shipkit-*-agent personas
│   ├── rules/
│   │   └── shipkit.md               # Framework rules (auto-loaded)
│   ├── profiles/
│   │   └── shipkit.manifest.json    # Skill manifest
│   ├── settings/
│   │   └── shipkit.settings.json    # Permissions + hooks
│   ├── claude-md/
│   │   └── shipkit.md               # CLAUDE.md template (user-editable)
│   ├── shared/
│   │   ├── hooks/                   # Session hooks
│   │   └── scripts/                 # Shared utilities
│   └── templates/                   # Queue templates
│
├── installers/                      # Alternative installers
│   ├── install.py                   # Python installer (legacy)
│   └── uninstall.py                 # Uninstaller
│
├── docs/                            # Documentation
│   ├── getting-started.md
│   ├── architecture.md
│   ├── skill-reference.md
│   └── creating-skills.md
│
├── package.json                     # npm package config
└── README.md                        # This file
```

---

## Key Features

### Streamlined Workflow
- <!-- sync:skill_count -->37<!-- /sync:skill_count --> focused skills
- All skills use `shipkit-` prefix for clarity
- Context stored in single `.shipkit/` folder
- No complex workspace structure

### Specification-Driven
- Features start with `/shipkit-spec`
- Plans reference specs
- Implementation follows plans
- Quality checks verify alignment

### Session Persistence
- `/shipkit-work-memory` maintains context
- `/shipkit-project-context` detects your stack
- Context files persist between sessions

### Natural Capabilities
Implementation, debugging, testing, refactoring, and code documentation are **natural Claude capabilities** that don't need skills. Skills focus on:
- Human decisions that must be explicit
- Persistence that survives sessions

---

## Common Workflows

### New Feature
```bash
/shipkit-spec "Add user authentication"
/shipkit-plan
# implement the feature
/shipkit-verify
```

### Explore Codebase
```bash
/shipkit-project-context
/shipkit-project-status
```

### Document Architecture
```bash
/shipkit-architecture-memory
```

### Get External Resources
```bash
/shipkit-get-skills     # Find Claude Code skills
/shipkit-get-mcps       # Find MCP servers
```

---

## Updating

```bash
npx shipkit-dev update
```

Or use the `shipkit-update` skill from within Claude Code:
```bash
/shipkit-update
```

This preserves your `.shipkit/` context files and custom settings while updating skill definitions.

---

## License

MIT License

---

**Ready to ship faster?**

```bash
npx shipkit-dev init
```

**Streamlined product development, guided by AI.**
