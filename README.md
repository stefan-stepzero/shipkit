# Shipkit - Streamlined Product Development Framework

A focused collection of **Claude Code skills** for efficient product development, from discovery to shipped code.

**24 skills** organized for streamlined workflow:
- **Core Workflow** (5) - Orchestration, status, and context management
- **Discovery & Planning** (6) - Product discovery and specification
- **Implementation** (3) - Architecture, contracts, and integrations
- **Quality & Documentation** (6) - Testing, UX, and documentation
- **Ecosystem** (2) - Get skills and MCPs
- **System** (2) - Auto-triggered detection and updates

Plus **6 agent personas** that specialize behaviors for different workflow stages.

---

## What's Inside

### Skills (24 total)

All skills use the `shipkit-` prefix for clarity.

**Core Workflow (5 skills):**
- `shipkit-master` - Meta skill for workflow orchestration
- `shipkit-project-status` - Health check and gap analysis
- `shipkit-project-context` - Codebase scanning, stack detection
- `shipkit-codebase-index` - Semantic codebase indexing
- `shipkit-claude-md` - CLAUDE.md management

**Discovery & Planning (6 skills):**
- `shipkit-product-discovery` - Personas, journeys, user stories
- `shipkit-why-project` - Strategic vision definition
- `shipkit-spec` - Feature specification
- `shipkit-plan` - Implementation planning
- `shipkit-prototyping` - Rapid UI mockups
- `shipkit-prototype-to-spec` - Extract learnings from prototypes

**Implementation (3 skills):**
- `shipkit-architecture-memory` - Decision logging
- `shipkit-data-contracts` - Type definitions (Zod patterns)
- `shipkit-integration-docs` - Integration patterns

**Quality & Documentation (6 skills):**
- `shipkit-ux-audit` - UX analysis and patterns
- `shipkit-verify` - QA and acceptance criteria
- `shipkit-preflight` - Production readiness audit
- `shipkit-user-instructions` - User-facing documentation
- `shipkit-communications` - Communication and formatting
- `shipkit-work-memory` - Session memory and context

**Ecosystem (2 skills):**
- `shipkit-get-skills` - Discover and install Claude Code skills
- `shipkit-get-mcps` - Discover and install MCP servers

**System Skills (2 skills):**
- `shipkit-detect` - Pattern detection and queue creation (auto-triggered)
- `shipkit-update` - Install or update Shipkit from GitHub

### Agent Personas (6)

| Agent | Used For |
|-------|----------|
| `shipkit-product-owner-agent` | Product/vision focus |
| `shipkit-ux-designer-agent` | UX/design perspective |
| `shipkit-architect-agent` | Technical architecture |
| `shipkit-implementer-agent` | Implementation focus |
| `shipkit-reviewer-agent` | Code review/quality |
| `shipkit-researcher-agent` | Research/discovery |

---

## Quick Start

### Installation

**Option 1: Ask Claude (Recommended)**

In any project with Claude Code, just ask:
> "Install Shipkit from https://github.com/stefan-stepzero/sg-shipkit"

Claude will fetch and run the `shipkit-update` skill to bootstrap the installation.

**Option 2: Python Installer**
```bash
cd your-project
curl -O https://raw.githubusercontent.com/stefan-stepzero/sg-shipkit/main/installers/install.py
python install.py
```

The installer will:
- Install all 24 skills
- Set up 6 agent personas
- Configure session hooks
- Create `.shipkit/` workspace

### After Installation

Your project will have:
```
your-project/
├── CLAUDE.md                    # Workflow guide
├── .claude/
│   ├── settings.json            # Permissions + hooks
│   ├── skills/                  # 24 skill definitions
│   ├── agents/                  # 6 agent personas
│   └── hooks/                   # Session hooks
└── .shipkit/                    # Your workspace
    ├── specs/                   # Feature specifications
    ├── plans/                   # Implementation plans
    └── [context files...]       # Stack, architecture, etc.
```

### Basic Workflow

```
/shipkit-project-context   → Scan and understand codebase
    ↓
/shipkit-spec              → Create feature specification
    ↓
/shipkit-plan              → Generate implementation plan
    ↓
(implement)                → Build the feature (natural capability)
    ↓
/shipkit-verify            → Verify quality
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
├── architecture.md      # Architecture decisions
├── stack.md             # Technology stack
├── implementations.md   # What's been built
└── types.md             # Data contracts
```

### 3. Skills Chain Together

Skills naturally flow from one to another:

```
/shipkit-project-context → Detects your stack
    → /shipkit-spec → Creates feature spec
    → /shipkit-plan → Generates implementation plan
    → (implement) → Builds the feature
```

---

## Repository Structure

```
sg-shipkit/
├── installers/
│   ├── install.py                # Python installer (cross-platform)
│   ├── uninstall.py              # Uninstaller
│   └── README.md                 # Installer documentation
│
├── install/                      # Everything that gets installed
│   ├── skills/                   # 24 shipkit-* skill definitions
│   ├── agents/                   # 6 shipkit-*-agent personas
│   ├── profiles/
│   │   └── shipkit.manifest.json # Skill manifest
│   ├── settings/
│   │   └── shipkit.settings.json # Permissions + hooks
│   ├── claude-md/
│   │   └── shipkit.md            # CLAUDE.md template
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
- 24 focused skills
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
curl -O https://raw.githubusercontent.com/stefan-stepzero/sg-shipkit/main/installers/install.py
python install.py -y
```

This preserves your `.shipkit/` context files while updating skill definitions.

---

## License

MIT License

---

**Ready to ship faster?**

Ask Claude: *"Install Shipkit from https://github.com/stefan-stepzero/sg-shipkit"*

**Streamlined product development, guided by AI.**
