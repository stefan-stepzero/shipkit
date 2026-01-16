# Shipkit Light - Streamlined Product Development Framework

A focused collection of **Claude Code skills** for efficient product development, from discovery to shipped code.

**28 lite skills** organized for streamlined workflow:
- **Core Workflow** (4) - Orchestration and status
- **Discovery & Planning** (6) - Product discovery and specification
- **Implementation** (7) - Building and documentation
- **Quality** (6) - Testing and user documentation
- **System** (5) - Auto-triggered validation skills

Plus **6 agent personas** that specialize behaviors for different workflow stages.

> **Note:** This repo now exclusively supports Shipkit Light. The full Shipkit framework has been archived to `archive/base-shipkit/`.

---

## What's Inside

### Lite Skills (28 total)

All skills use the `lite-` prefix for clarity.

**Core Workflow (4 skills):**
- `lite-shipkit-master` - Meta skill for workflow orchestration
- `lite-project-status` - Health check and gap analysis
- `lite-project-context` - Codebase scanning, stack detection
- `lite-whats-next` - Workflow routing and next steps

**Discovery & Planning (6 skills):**
- `lite-product-discovery` - Personas, journeys, user stories
- `lite-why-project` - Strategic vision definition
- `lite-spec` - Feature specification
- `lite-plan` - Implementation planning
- `lite-prototyping` - Rapid UI mockups
- `lite-prototype-to-spec` - Extract learnings from prototypes

**Implementation (7 skills):**
- `lite-implement` - Feature building
- `lite-architecture-memory` - Decision logging
- `lite-data-contracts` - Type definitions (Zod patterns)
- `lite-component-knowledge` - Component documentation
- `lite-route-knowledge` - Route documentation
- `lite-integration-docs` - Integration patterns
- `lite-debug-systematically` - Debugging methodology

**Quality & Documentation (6 skills):**
- `lite-ux-audit` - UX analysis and patterns
- `lite-quality-confidence` - QA and acceptance criteria
- `lite-document-artifact` - Documentation templates
- `lite-user-instructions` - User-facing documentation
- `lite-communications` - Communication and formatting
- `lite-work-memory` - Session memory and context

**System Skills (5 skills, auto-triggered):**
- `lite-milestone-detector` - Feature completion detection
- `lite-post-spec-check` - Post-spec validation
- `lite-post-plan-check` - Post-plan validation
- `lite-post-implement-check` - Post-implement validation
- `lite-pre-ship-check` - Pre-release validation

### Agent Personas (6)

| Agent | Used For |
|-------|----------|
| `lite-product-owner-agent` | Product/vision focus |
| `lite-ux-designer-agent` | UX/design perspective |
| `lite-architect-agent` | Technical architecture |
| `lite-implementer-agent` | Implementation focus |
| `lite-reviewer-agent` | Code review/quality |
| `lite-researcher-agent` | Research/discovery |

---

## Quick Start

### Installation

**Python (All Platforms - Recommended):**
```bash
cd your-project
python ../sg-shipkit/installers/install.py
```

The installer will:
- Install all 28 lite skills
- Set up 6 agent personas
- Configure session hooks
- Create `.shipkit-lite/` workspace

### After Installation

Your project will have:
```
your-project/
├── CLAUDE.md                    # Workflow guide
├── .claude/
│   ├── settings.json            # Permissions + hooks
│   ├── skills/                  # 28 lite skill definitions
│   ├── agents/                  # 6 agent personas
│   └── hooks/                   # Session hooks
└── .shipkit-lite/               # Your workspace
    ├── scripts/                 # Shared utilities
    ├── specs/                   # Feature specifications
    ├── plans/                   # Implementation plans
    └── [context files...]       # Stack, architecture, etc.
```

### Basic Workflow

```
/lite-project-context   → Scan and understand codebase
    ↓
/lite-spec              → Create feature specification
    ↓
/lite-plan              → Generate implementation plan
    ↓
/lite-implement         → Build the feature
    ↓
/lite-quality-confidence → Verify quality
```

---

## How It Works

### 1. Session Hooks Enforce Skills

When Claude Code starts:
1. Runs session-start hook
2. Loads `lite-shipkit-master` into context
3. Skills become the primary workflow method

### 2. Context Lives in `.shipkit-lite/`

Your project context is stored in:
```
.shipkit-lite/
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
/lite-project-context → Detects your stack
    → /lite-spec → Creates feature spec
    → /lite-plan → Generates implementation plan
    → /lite-implement → Builds the feature
```

After each skill, `/lite-whats-next` suggests the logical next step.

---

## Repository Structure

```
sg-shipkit/
├── installers/
│   ├── install.py                # Python installer (cross-platform)
│   └── README.md                 # Installer documentation
│
├── install/                      # Everything that gets installed
│   ├── skills/                   # 28 lite-* skill definitions
│   ├── agents/                   # 6 lite-*-agent personas
│   ├── profiles/
│   │   └── lite.manifest.json    # Skill manifest
│   ├── settings/
│   │   └── lite.settings.json    # Permissions + hooks
│   ├── claude-md/
│   │   └── lite.md               # CLAUDE.md template
│   ├── shared/
│   │   ├── hooks/                # Session hooks
│   │   └── scripts/              # Shared utilities
│   └── templates/                # Queue templates
│
├── archive/
│   └── base-shipkit/             # Archived full framework
│
├── claude-code-best-practices/   # Reference documentation
├── CLAUDE.md                     # Development guide (this repo)
└── README.md                     # This file
```

---

## Key Features

### Streamlined Workflow
- 28 focused skills (vs 37+ in full framework)
- All skills use `lite-` prefix for clarity
- Context stored in single `.shipkit-lite/` folder
- No complex workspace structure

### Specification-Driven
- Features start with `/lite-spec`
- Plans reference specs
- Implementation follows plans
- Quality checks verify alignment

### Session Persistence
- `/lite-work-memory` maintains context
- `/lite-project-context` detects your stack
- Context files persist between sessions

### Automatic Validation
- System skills trigger automatically
- Post-spec, post-plan, post-implement checks
- Pre-ship validation before release

---

## Common Workflows

### New Feature
```bash
/lite-spec "Add user authentication"
/lite-plan
/lite-implement
/lite-quality-confidence
```

### Explore Codebase
```bash
/lite-project-context
/lite-project-status
```

### Debug Issue
```bash
/lite-debug-systematically
```

### Document Component
```bash
/lite-component-knowledge "UserProfile"
/lite-user-instructions
```

---

## Updating

Re-run the installer to get the latest skills:

```bash
cd your-project
python ../sg-shipkit/installers/install.py -y
```

This preserves your `.shipkit-lite/` context files while updating skill definitions.

---

## Archived: Full Shipkit

The full Shipkit framework (dev-*, prod-* skills) has been archived to `archive/base-shipkit/`.

If you need the full framework, see `archive/base-shipkit/README.md` for restoration instructions.

---

## License

MIT License

---

**Ready to ship faster?**

```bash
cd your-next-project
python ../sg-shipkit/installers/install.py
```

**Streamlined product development, guided by AI.**
