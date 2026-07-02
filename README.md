# Shipkit - Streamlined Product Development Framework

A focused collection of **Claude Code skills** for efficient product development, from discovery to shipped code.

**<!-- sync:skill_count -->39<!-- /sync:skill_count --> skills** organized for streamlined workflow:
<!-- sync:readme_summary -->- **Vision & Discovery** (12) - why-project, product-discovery, project-context, ...
- **Spec & Planning** (6) - spec-roadmap, spec, feedback-bug, ...
- **Knowledge & Memory** (2) - claude-md, work-memory
- **Orchestration** (1) - direction
- **Execution** (2) - ship, test-cases
- **Quality & Communication** (12) - review-direction, review-planning, review-shipping, ...
- **System** (3) - update, get-skills, get-mcps<!-- /sync:readme_summary -->

Plus **<!-- sync:agent_count -->8<!-- /sync:agent_count --> agent personas** that specialize behaviors for different workflow stages.

---

## What's Inside

### Skills (<!-- sync:skill_count -->39<!-- /sync:skill_count --> total)

All skills use the `shipkit-` prefix for clarity.

**Core Workflow (4 skills):**
- `shipkit-project-context` - Codebase scanning, stack detection
- `shipkit-codebase-index` - Semantic codebase indexing
- `shipkit-architecture-map` - Code-derived current-state architecture map (apps, datastores, contracts, integrations)
- `shipkit-claude-md` - CLAUDE.md management

**Orchestration (2 skills):**
- `shipkit-orchestrate` - Core automation engine — delegate→reconcile→re-dispatch loop to a ground-truth bar (autonomous/steered); phase skills call it
- `shipkit-direction` - Direction entry point — drives the definitional foundation (why→goals) via the engine in autonomous-propose mode (ground-or-ask calibration)

**Discovery & Planning (15 skills):**
- `shipkit-why-project` - Strategic vision definition
- `shipkit-product-discovery` - Personas, journeys, user needs
- `shipkit-product-definition` - Product blueprint (features, patterns, differentiators)
- `shipkit-engineering-definition` - Engineering blueprint (mechanisms, components, stack)
- `shipkit-design-system` - Design system scaffold (principles, tokens, aesthetic direction)
- `shipkit-stage` - Project stage, constraints, and graduation criteria
- `shipkit-product-goals` - User-outcome success criteria (P-*)
- `shipkit-engineering-goals` - Technical performance criteria
- `shipkit-spec-roadmap` - Prioritize spec backlog from definitions + goals
- `shipkit-spec` - Feature specification
- `shipkit-feedback-bug` - Process feedback into investigated bug specs (5 Whys root cause)
- `shipkit-plan` - Implementation planning
- `shipkit-metrics` - Capture metric values for goal evaluation
- `shipkit-thinking-partner` - Think through decisions with cognitive frameworks (interactive + adversarial debate modes)
- `shipkit-resource-advocate` - Infrastructure: single-resource advocate dispatched by thinking-partner's adversarial debate (not user-invoked)

**Execution (2 skills):**
- `shipkit-ship` - Build a spec'd + planned feature to done (BUILD entry point; thin caller → `shipkit-orchestrate` autonomous over the plan)
- `shipkit-test-cases` - Generate code-anchored test case specs

**Quality & Documentation (13 skills):**
- `shipkit-review-direction` - Assess strategic artifact coherence
- `shipkit-review-planning` - Assess planning artifact alignment
- `shipkit-review-shipping` - QA and acceptance criteria
- `shipkit-preflight` - MVP production readiness audit
- `shipkit-scale-ready` - Scale & enterprise readiness audit
- `shipkit-prompt-audit` - LLM prompt architecture audit
- `shipkit-codebase-audit` - Dead code, orphans, unused deps & unwired seams (knip-class + intent↔code)
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


### Agent Personas (<!-- sync:agent_count -->8<!-- /sync:agent_count -->)

<!-- sync:readme_agent_table -->**Orchestrators:**
| Agent | Used For |
|-------|----------|

**Producers:**
| Agent | Used For |
|-------|----------|
| `shipkit-visionary-agent` | Strategic visionary — sets stage, vision, constraints, business goals |
| `shipkit-product-owner-agent` | Product manager — definitions, specs, feedback, product goals |
| `shipkit-architect-agent` | Engineering manager — architecture, plans, engineering goals |
| `shipkit-thinking-partner-agent` | Cognitive discussion & thinking partner |
| `shipkit-resource-advocate-agent` | Single-resource debate advocate — champions one resource in the adversarial debate |

**Reviewers:**
| Agent | Used For |
|-------|----------|
| `shipkit-reviewer-direction-agent` | Direction judgment — strategic coherence assessment |
| `shipkit-reviewer-planning-agent` | Planning judgment — definition/spec alignment assessment |
| `shipkit-reviewer-shipping-agent` | Shipping judgment — implementation quality + QA dispatch |<!-- /sync:readme_agent_table -->

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
- Install all <!-- sync:skill_count -->39<!-- /sync:skill_count --> skills
- Set up <!-- sync:agent_count -->8<!-- /sync:agent_count --> agent personas
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
│   ├── skills/                  # 39 skill definitions
│   ├── agents/                  # 8 agent personas
│   └── hooks/                   # Session hooks
└── .shipkit/                    # Your workspace
    ├── specs/                   # Feature specifications
    ├── plans/                   # Implementation plans
    └── [context files...]       # Stack, architecture, etc.
```

### Basic Workflow

```mermaid
flowchart LR
    SKL_WHY["/why-project"] --> SKL_DISCOVERY["/product-discovery"]
    SKL_DISCOVERY --> SKL_PRODDEF["/product-definition"]
    SKL_PRODDEF --> SKL_ENGDEF["/engineering-definition"]
    SKL_ENGDEF --> SKL_GOALS["/goals"]
    SKL_GOALS --> SKL_ROADMAP["/spec-roadmap"]
    SKL_ROADMAP --> SKL_SPEC["/spec"]
    SKL_SPEC --> SKL_PLAN["/plan"]
    SKL_PLAN --> IMPL["implement"]
    IMPL --> SKL_VERIFY["/review-shipping"]
    SKL_VERIFY --> SKL_WORKMEM["/work-memory"]
```

> **Shortcut:** If you already know what to build, skip straight to `/shipkit-spec`. The discovery chain (why → discovery → product-definition → engineering-definition → goals) is most valuable for new products or when exploring problem space.

---

## How It Works

### 1. Session Hooks Enforce Skills

When Claude Code starts:
1. Runs session-start hook
2. Loads the `shipkit-orchestrate` engine + project context into context
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
└── engineering-definition.json  # Technical mechanisms & data contracts
```

### 3. Skills Chain Together

Skills naturally flow from one to another. Each produces an artifact the next step reads:

```mermaid
flowchart LR
    SKL_WHY["why-project"] --> SKL_DISCOVERY["product-discovery"]
    SKL_DISCOVERY --> SKL_PRODDEF["product-definition"]
    SKL_PRODDEF --> SKL_ENGDEF["engineering-definition"]
    SKL_ENGDEF --> SKL_GOALS["goals"]
    SKL_GOALS --> SKL_ROADMAP["spec-roadmap"]
    SKL_ROADMAP --> SKL_SPECPLAN["spec / plan"]
    SKL_SPECPLAN --> IMPL["implement"]
    IMPL --> SKL_VERIFY["verify"]
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
│   ├── skills/                      # <!-- sync:skill_count -->39<!-- /sync:skill_count --> shipkit-* skill definitions
│   ├── agents/                      # <!-- sync:agent_count -->8<!-- /sync:agent_count --> shipkit-*-agent personas
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
│   ├── creating-skills.md           # Contributor guide
│   └── generated/                   # Interactive HTML docs
│       ├── shipkit-overview.html
│       └── orchestration-pipeline.html
│
├── package.json                     # npm package config
└── README.md                        # This file
```

---

## Key Features

### Streamlined Workflow
- <!-- sync:skill_count -->39<!-- /sync:skill_count --> focused skills
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
/shipkit-review-shipping
```

### Explore Codebase
```bash
/shipkit-project-context
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

MIT — See [LICENSE](LICENSE) for details.

---

**Ready to ship faster?**

```bash
npx shipkit-dev init
```

**Streamlined product development, guided by AI.**
