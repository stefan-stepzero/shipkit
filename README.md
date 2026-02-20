# Shipkit - Streamlined Product Development Framework

A focused collection of **Claude Code skills** for efficient product development, from discovery to shipped code.

**38 skills** organized for streamlined workflow:
- **Core Workflow** (5) - Orchestration, status, and context management
- **Discovery & Planning** (8) - Product discovery, goals, product definition, specification, and bug triage
- **Implementation** (3) - Architecture, contracts, and integrations
- **Execution** (6) - Test case generation, relentless build/test/lint, parallel implementation
- **Quality & Documentation** (10) - Testing, UX, production readiness, prompt architecture, semantic QA, visual QA, and documentation
- **Ecosystem** (2) - Get skills and MCPs
- **System** (3) - Detection, updates, and standby mode

Plus **9 agent personas** that specialize behaviors for different workflow stages.

---

## What's Inside

### Skills (38 total)

All skills use the `shipkit-` prefix for clarity.

**Core Workflow (5 skills):**
- `shipkit-master` - Meta skill for workflow orchestration
- `shipkit-project-status` - Health check and gap analysis
- `shipkit-project-context` - Codebase scanning, stack detection
- `shipkit-codebase-index` - Semantic codebase indexing
- `shipkit-claude-md` - CLAUDE.md management

**Discovery & Planning (8 skills):**
- `shipkit-product-discovery` - Personas, journeys, user stories
- `shipkit-why-project` - Strategic vision definition
- `shipkit-goals` - Project goals, priorities, and success criteria
- `shipkit-product-definition` - Map goals to features with coverage analysis
- `shipkit-spec` - Feature specification
- `shipkit-feedback-bug` - Process feedback into investigated bug specs (5 Whys root cause)
- `shipkit-plan` - Implementation planning
- `shipkit-thinking-partner` - Think through decisions with cognitive frameworks

**Implementation (3 skills):**
- `shipkit-architecture-memory` - Decision logging
- `shipkit-data-contracts` - Type definitions (Zod patterns)
- `shipkit-integration-docs` - Integration patterns

**Execution (6 skills):**
- `shipkit-test-cases` - Generate code-anchored test case specs
- `shipkit-build-relentlessly` - Build until compiles
- `shipkit-test-relentlessly` - Test until green
- `shipkit-lint-relentlessly` - Lint until clean
- `shipkit-implement-independently` - Parallel implementation in isolated worktree
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

**System Skills (5 skills):**
- `shipkit-detect` - Pattern detection and queue creation (auto-triggered)
- `shipkit-update` - Install or update Shipkit from GitHub
- `shipkit-standby` - AFK daemon mode with command polling and backoff
- `shipkit-get-skills` - Discover and install Claude Code skills
- `shipkit-get-mcps` - Discover and install MCP servers

### Agent Personas (9)

| Agent | Used For |
|-------|----------|
| `shipkit-project-manager-agent` | Coordination & context |
| `shipkit-product-owner-agent` | Product/vision focus |
| `shipkit-ux-designer-agent` | UX/design perspective |
| `shipkit-architect-agent` | Technical architecture |
| `shipkit-implementer-agent` | Implementation focus |
| `shipkit-implement-independently-agent` | Isolated parallel implementation |
| `shipkit-reviewer-agent` | Code review/quality |
| `shipkit-researcher-agent` | Research/discovery |
| `shipkit-thinking-partner-agent` | Cognitive thinking partner |

---

## Quick Start

### Installation

**Download and run the Python installer:**
```bash
cd your-project
curl -O https://raw.githubusercontent.com/stefan-stepzero/shipkit/main/installers/install.py
python install.py --from-github
```

Add `-y` for non-interactive mode (uses sensible defaults).

**Already have Shipkit?** Update with `/shipkit-update`

The installer will:
- Install all 38 skills
- Set up 9 agent personas
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
│   ├── skills/                  # 35 skill definitions
│   ├── agents/                  # 9 agent personas
│   └── hooks/                   # Session hooks
└── .shipkit/                    # Your workspace
    ├── specs/                   # Feature specifications
    ├── plans/                   # Implementation plans
    └── [context files...]       # Stack, architecture, etc.
```

### Basic Workflow

```
/shipkit-why-project       → Define vision & goals (new projects)
    ↓
/shipkit-project-context   → Scan codebase, detect stack
    ↓
/shipkit-spec              → Create feature specification
    ↓
/shipkit-plan              → Generate implementation plan
    ↓
(implement)                → Build the feature (natural capability)
    ↓
/shipkit-verify            → Verify quality before commit
    ↓
/shipkit-work-memory       → Checkpoint progress for next session
```

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
/shipkit-project-context → Detects your stack
    → /shipkit-spec → Creates feature spec
    → /shipkit-plan → Generates implementation plan
    → (implement) → Builds the feature
    → /shipkit-verify → Checks quality
    → /shipkit-work-memory → Saves progress
```

---

## Repository Structure

```
shipkit/
├── installers/
│   ├── install.py                # Python installer (cross-platform)
│   ├── uninstall.py              # Uninstaller
│   └── README.md                 # Installer documentation
│
├── install/                      # Everything that gets installed
│   ├── skills/                   # 34 shipkit-* skill definitions
│   ├── agents/                   # 9 shipkit-*-agent personas
│   ├── rules/
│   │   └── shipkit.md            # Framework rules (auto-loaded)
│   ├── profiles/
│   │   └── shipkit.manifest.json # Skill manifest
│   ├── settings/
│   │   └── shipkit.settings.json # Permissions + hooks
│   ├── claude-md/
│   │   └── shipkit.md            # CLAUDE.md template (user-editable)
│   ├── shared/
│   │   ├── hooks/                # Session hooks
│   │   └── scripts/              # Shared utilities
│   └── templates/                # Queue templates
│
├── docs/                         # Documentation
│   ├── getting-started.md
│   ├── architecture.md
│   ├── skill-reference.md
│   └── creating-skills.md
│
└── README.md                     # This file
```

---

## Key Features

### Streamlined Workflow
- 35 focused skills
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

Use the `shipkit-update` skill:
```bash
/shipkit-update
```

Or re-run the installer:
```bash
curl -O https://raw.githubusercontent.com/stefan-stepzero/shipkit/main/installers/install.py
python install.py -y
```

This preserves your `.shipkit/` context files while updating skill definitions.

---

## License

MIT License

---

**Ready to ship faster?**

Ask Claude: *"Use /shipkit-update to install Shipkit from https://github.com/stefan-stepzero/shipkit"*

**Streamlined product development, guided by AI.**
