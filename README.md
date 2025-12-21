# ShipKit - Complete Product Development Framework

A curated collection of **Claude Code skills** combining **DevKit** (technical specs + development workflow) and **ProdKit** (product discovery) for end-to-end product development.

## What's Inside

### 🎯 DevKit (23 skills)
**Specification-driven development pipeline + quality workflow**

**Core Pipeline:**
- constitution, constitution-builder, specify, plan, tasks, implement
- analyze, clarify, checklist, taskstoissues

**Quality & Testing:**
- test-driven-development, verification-before-completion, systematic-debugging

**Workflow & Collaboration:**
- using-git-worktrees, brainstorming (async - can interrupt any skill)
- finishing-a-development-branch, requesting-code-review, receiving-code-review
- dispatching-parallel-agents, subagent-driven-development, writing-plans

**Meta:**
- writing-skills, using-devkit

**Key feature:** `/implement` integrates TDD, verification, debugging, and two-stage code review automatically.

Inspired by: [GitHub's Spec-Kit](https://github.com/github/spec-kit) | [obra's Superpowers](https://github.com/anthropics/claude-code-superpowers)

### 🏭 ProdKit (11 skills)
**Product discovery and strategy**

**Sequential Workflow (9 skills)**:
1. strategic-thinking - Business strategy and value proposition
2. personas - Target user definition
3. jobs-to-be-done - Current state analysis
4. market-analysis - Competitive landscape (Porter's Five Forces)
5. brand-guidelines - Visual direction and personality
6. interaction-design - Future state user journeys
7. user-stories - Actionable requirements
8. assumptions-and-risks - Strategic risk identification
9. success-metrics - KPIs and instrumentation

**Async (2 skills)**:
- trade-off-analysis - Feature prioritization and ROI
- communicator - Stakeholder communications (HTML generation)

### 🤖 Agent Personas (5 agents)
**Specialized behaviors for different workflow stages**

| Agent | Used For |
|-------|----------|
| Discovery | Product discovery, brainstorming, user research |
| Architect | Technical planning, specs, architecture |
| Implementer | TDD-focused coding, minimal implementation |
| Reviewer | Two-stage code review (spec compliance + quality) |
| Researcher | Deep research, competitive intel, cross-referencing |

Skills automatically load the appropriate agent persona.

---

## Quick Start

### Installation

**Two installation modes available:**

#### Option 1: Local Installation (Recommended for Development)

Structure your projects like this:
```
Projects/
├── shipkit/          # This repo (clone once)
└── your-project/          # Your project
```

Then install:
```bash
cd Projects/your-project
bash ../shipkit/install.sh --preset solo
```

#### Option 2: GitHub Installation (One-Command Setup)

Install directly from GitHub (public or private repo):

```bash
# Public repository
cd your-project
bash install.sh --github https://github.com/user/shipkit.git --preset solo

# Private repository (requires SSH access)
bash install.sh --github git@github.com:user/shipkit.git --preset solo

# One-liner (requires curl)
curl -fsSL https://raw.githubusercontent.com/user/shipkit/main/install.sh | bash -s -- --github https://github.com/user/shipkit.git --preset solo
```

### Installation Options

```bash
# Everything (34 skills + full infrastructure)
bash ../shipkit/install.sh --all

# Solo preset (all 34 skills - recommended)
bash ../shipkit/install.sh --preset solo

# Just DevKit (23 skills)
bash ../shipkit/install.sh --devkit-only

# Just ProdKit (11 skills)
bash ../shipkit/install.sh --prodkit-only

# From GitHub with specific branch
bash install.sh --github https://github.com/user/shipkit.git --branch dev --all

# Help
bash ../shipkit/install.sh --help
```

---

## Repository Structure

```
shipkit/
├── install.sh                      # One-command installer
├── README.md                       # This file
├── CLAUDE.md                       # Project instructions template (copied to projects)
│
├── agents/                         # Agent persona definitions
│   ├── discovery-agent.md          # Product discovery specialist
│   ├── architect-agent.md          # Technical planning specialist
│   ├── implementer-agent.md        # TDD implementation specialist
│   ├── reviewer-agent.md           # Code review specialist
│   ├── researcher-agent.md         # Research specialist
│   └── README.md                   # Agent documentation
│
├── hooks/                          # Session start hooks (enforcement layer)
│   ├── hooks.json                  # Hook configuration
│   ├── session-start.sh            # Injects meta-skill at session start
│   └── run-hook.cmd                # Windows wrapper
│
├── help/                           # Documentation & tools
│   ├── generate-reference.py       # Generate skills reference HTML
│   ├── system-overview.html        # Visual workflow guide (start here!)
│   └── skills-overview.html        # Detailed prompt reference (maintainers)
│
├── skills/                         # Source: Claude Code skill definitions
│   ├── meta/                       # Meta-skill (enforcement - injected at session start)
│   │   └── using-shipkit.md
│   ├── devkit/                     # 23 skills (flat structure)
│   └── prodkit/
│       ├── sequential/             # 9 numbered skills (1-9)
│       └── async/                  # 2 anytime skills
│
├── devkit-files/                   # DevKit infrastructure
│   ├── scripts/
│   │   ├── bash/                   # Automation scripts
│   │   └── powershell/             # Automation scripts
│   └── templates/                  # Document templates + constitution
│
└── prodkit-files/                  # ProdKit infrastructure
    ├── scripts/
    │   └── bash/                   # Automation scripts
    └── templates/
        ├── structure/              # Markdown templates
        └── communication/          # HTML templates
```

---

## What Gets Installed

After running `install.sh --preset solo`, your project structure:

```
your-project/
│
├── CLAUDE.md                       # Project instructions (Claude reads at session start)
├── .claude/
│   ├── settings.json               # Hook configuration (auto-injects at session start)
│   ├── constitution.md             # Project rules (created by /constitution-builder)
│   ├── agents/                     # Agent persona definitions
│   │   ├── discovery-agent.md
│   │   ├── architect-agent.md
│   │   ├── implementer-agent.md
│   │   ├── reviewer-agent.md
│   │   └── researcher-agent.md
│   ├── hooks/                      # Session start scripts
│   │   ├── hooks.json
│   │   ├── session-start.sh
│   │   └── run-hook.cmd
│   └── skills/                     # Skill definitions
│       ├── meta/                   # Meta-skill (enforcement layer)
│       ├── devkit/                 # 23 DevKit skills
│       └── prodkit/
│           ├── sequential/         # 9 skills
│           └── async/              # 2 skills
│
├── .devkit/                        # DevKit workspace
│   ├── scripts/                    # Automation scripts
│   ├── templates/                  # Document templates
│   └── specs/                      # Feature specifications
│       └── 001-feature-name/
│           ├── spec.md
│           ├── plan.md
│           └── tasks.md
│
└── .prodkit/                       # ProdKit workspace
    ├── scripts/                    # Automation scripts
    ├── templates/                  # Markdown + HTML templates
    ├── inputs/                     # Drop research files here
    ├── strategy/                   # Generated artifacts
    ├── discovery/
    ├── brand/
    ├── design/
    ├── requirements/
    ├── metrics/
    └── comms/                      # Generated HTML communications
```

**Everything stays hidden** under dot-folders - no pollution of your project root!

---

## How It Works

### 1. This is Your Source Repo
`shipkit` is your **source of truth** - maintain and update it over time.

### 2. Install Into Projects
When starting a new project, choose your installation method:

**Local installation** (faster, no network needed):
```bash
cd my-new-project/
bash ../shipkit/install.sh --preset solo
```

**GitHub installation** (works from anywhere):
```bash
cd my-new-project/
bash install.sh --github https://github.com/user/shipkit.git --preset solo
```

Both create:
- `.claude/skills/` - 30+ skill definitions (including meta-skill)
- `.claude/hooks/` - Session start hooks (enforcement layer)
- `.devkit/` - devkit workspace with scripts/templates
- `.prodkit/` - ProdKit workspace with scripts/templates

### 3. Session Start Hook Injects Enforcement
When Claude Code starts, the session hook:
- Runs `.claude/hooks/session-start.sh`
- Injects the meta-skill (`using-shipkit.md`) into Claude's context
- This makes skill checking **mandatory before any response**

The meta-skill tells Claude:
- Check for applicable skills before ANY response
- Even 1% chance = use the skill
- Check prerequisites before invoking skills
- Read constitution before implementation work

### 4. Claude Also Reads CLAUDE.md
Claude Code reads `CLAUDE.md` at session start as backup, which:
- Contains routing tables (user intent → skill)
- Lists prerequisites for each skill
- Documents the ProdKit → devkit integration

### 5. Claude Code Discovers Skills
Claude Code automatically reads skills from:
- `.claude/skills/` (project-specific)
- `~/.claude/skills/` (global)

### 6. Skills Call Scripts
Skills are **instructions** that tell Claude:
- When to trigger
- What questions to ask
- **Which script to call** (enforces consistency)

Example: `/strategic-thinking` skill tells Claude to:
1. Ask Playing to Win questions
2. Call `.prodkit/scripts/bash/create-strategy.sh`
3. Never create files manually

**Scripts ensure:**
- Consistent file structure
- Template usage
- Validation
- No freestyle file creation

---

## Complete Workflow

For a new product/feature:

### Phase 1: Product Discovery (ProdKit)

```
/strategic-thinking
        ↓
/constitution-builder --product    ← Define product principles
        ↓
/personas → /jobs-to-be-done → /market-analysis
        ↓
/brand-guidelines → /interaction-design
        ↓
/user-stories → /assumptions-and-risks → /success-metrics
```

**Async skills** (call anytime):
- **/brainstorming** - Can interrupt ANY skill when ambiguity detected
- **/trade-off-analysis** - Prioritize features by ROI
- **/communicator** - Generate stakeholder HTML docs

**Output**: Complete product context in `.prodkit/`

### Phase 2: Technical Specification (devkit)

```
/constitution-builder --technical  ← Define technical standards
        ↓
/specify → /plan → /tasks
```

**Output**: Technical specs in `.devkit/specs/001-feature-name/`

### Phase 3: Development

```
/using-git-worktrees              ← Create isolated branch
        ↓
/implement                        ← Executes with:
  ├── TDD (RED → GREEN → REFACTOR)
  ├── Spec Compliance Review
  ├── Code Quality Review
  └── Verification before completion
        ↓
/finishing-a-development-branch   ← Merge/PR workflow
```

**/implement** automatically integrates TDD, reviews, and verification. For 6+ tasks, it offers subagent execution mode.

**Output**: Shipped feature

---

## Presets Explained

### `--preset solo` (Default - Recommended)
**Installs:** DevKit + ProdKit + Agent Personas
**Total:** 34 skills + 5 agents
**Best for:** Solo developers, full-stack SaaS
**Includes:** Complete product-to-code workflow

### `--all` (Everything)
**Installs:** All 34 skills + all infrastructure
**Best for:** Teams, maximum flexibility
**Includes:** Full subagent capabilities, advanced review workflows

### `--devkit-only`
**Installs:** Just DevKit
**Total:** 23 skills + 5 agents
**Best for:** Already have product specs, just need development workflow

### `--prodkit-only`
**Installs:** Just ProdKit
**Total:** 11 skills
**Best for:** Product discovery only, no technical specs

---

## Key Features

### ✅ No External Dependencies
- All 34 skills work 100% locally
- No APIs required (except optional WebSearch for market research)
- Optional GitHub integration for `taskstoissues` and PR creation

### ✅ Script-Enforced Consistency
- Claude never creates files manually
- Scripts use templates
- Validate inputs
- Ensure file structure

### ✅ Separation of Concerns
- `.claude/` - Skills only (what Claude reads)
- `.devkit/` - DevKit workspace (technical specs)
- `.prodkit/` - ProdKit workspace (product discovery)

### ✅ Cross-Platform
- Bash scripts (Mac, Linux, Git Bash on Windows)
- PowerShell scripts coming soon

### ✅ Hidden by Default
- Everything under dot-folders
- No project root pollution
- Git-friendly

---

## Advanced Usage

### Set Up Project Constitution

Use the two-phase constitution builder for comprehensive project rules:

```bash
# After /strategic-thinking - define product principles
/constitution-builder --product

# Before /specify - define technical standards
/constitution-builder --technical
```

This creates `.claude/constitution.md` with:
- **Product phase**: Brand voice, UX principles, accessibility requirements
- **Technical phase**: Tech stack, architecture patterns, code standards

Claude reads this during all devkit skills.

### Customize Agent Personas

Agent personas in `.claude/agents/` define specialized behaviors. Customize them for your team:

```markdown
# .claude/agents/implementer-agent.md

## Constraints (customize these)
- Our team uses Vitest, not Jest
- We prefer functional components only
- All API calls go through our SDK
```

Skills automatically load the appropriate persona.

### Generate Stakeholder Communications

After product discovery:

```
User: "Create an investor one-pager"
Claude: [Reads .prodkit/ artifacts, uses /communicator skill]
        [Calls generate-communication.sh]
        [Creates .prodkit/comms/2024-12-20-investors-onepager.html]
```

Output: Print-ready HTML with strategy, market, traction.

### Run Trade-off Analysis

After devkit generates `tasks.md`:

```
User: "Should we build real-time collaboration?"
Claude: [Uses /trade-off-analysis skill]
        [Reads user stories, strategy, effort estimates]
        [Calls calculate-tradeoffs.sh]
        [Recommends BUILD/DEFER/CUT based on ROI]
```

---

## Maintenance

### Updating This Repo
When upstream repos update:
1. Pull latest from devkit and devkit
2. Update files in `skills/`
3. Update HTML overview
4. Commit changes
5. Push to GitHub (if using GitHub installation mode)

### Updating Projects
When you update shipkit, re-run the installer:

**Local installation:**
```bash
cd your-project
bash ../shipkit/install.sh --preset solo
```

**GitHub installation:**
```bash
cd your-project
bash install.sh --github https://github.com/user/shipkit.git --preset solo
```

The installer preserves existing files (won't overwrite customized constitution or project artifacts).

---

## Integration Requirements

### Works 100% Locally
- ✅ All 9 devkit skills (except `taskstoissues`)
- ✅ All 13 devkit skills
- ✅ All 11 prodkit skills

### Optional Integrations
- ⚠️ **GitHub**: `taskstoissues`, `finishing-branch` (can push/PR)
- ⚠️ **WebSearch**: `/market-analysis` uses WebSearch for competitive research (optional)

**For solo development, everything works without external dependencies.**

---

## Documentation

### User Documentation

📖 **[System Overview](help/system-overview.html)** - **START HERE!**
- Visual workflow guide for end users
- Shows how ProdKit → devkit → Development works together
- Installation presets explained
- Complete workflow walkthrough

### Maintainer References

📖 **[Skills Overview](help/skills-overview.html)** (For prompt editing)
- Browse all 11 ProdKit prompts in detail
- View raw prompt files for editing
- Scripts shown as visual pseudocode
- **Generate**: `python help/generate-reference.py`

---

## Sources & Credits

This framework combines:
- **[devkit](https://github.com/github/devkit)** by GitHub - Technical specification framework
- **[devkit](https://github.com/obra/devkit)** by Jesse Vincent - Development workflow enhancements
- **prodkit** - Product discovery framework (new, built for this repo)

---

## License

- **devkit skills**: Retain original license from GitHub
- **devkit skills**: Retain original license from obra
- **ProdKit skills and infrastructure**: MIT License
- **Collection structure**: MIT License

---

## Support

- **Quick Start Guide**: `help/system-overview.html`
- **Prompt Reference**: `help/skills-overview.html`
- **devkit Docs**: https://github.com/github/devkit
- **devkit Docs**: https://github.com/obra/devkit
- **Issues**: [Your issue tracker]

---

**Ready to ship products faster?**

**Local installation:**
```bash
cd your-next-project
bash ../shipkit/install.sh --preset solo
```

**GitHub installation (one-liner):**
```bash
curl -fsSL https://raw.githubusercontent.com/user/shipkit/main/install.sh | bash -s -- --github https://github.com/user/shipkit.git --preset solo
```

**From strategy to shipped code, all guided by AI.**
