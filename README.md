# Shipkit - Complete Product Development Framework

A curated collection of **Claude Code skills** for end-to-end product development, from strategy to shipped code.

**24 core skills** organized in three categories:
- **Prod Skills** (12) - Product discovery & strategy
- **Dev Skills** (9) - Technical specs, orchestration & development workflow
- **Meta Skills** (3) - Enforcement, discussion & skill authoring

Plus **6 agent personas** that specialize behaviors for different workflow stages.

---

## What's Inside

### Product Skills (12 skills)
**Product discovery and strategy - research-driven, template-based**

**Sequential Workflow (10 skills):**
1. prod-strategic-thinking - Business strategy and value proposition
2. prod-constitution-builder - Product principles (POC/MVP/Established × B2C/B2B)
3. prod-personas - Target user definition with empathy mapping
4. prod-jobs-to-be-done - JTBD framework with forces diagram
5. prod-market-analysis - Competitive landscape (research-intensive)
6. prod-brand-guidelines - Visual direction and personality
7. prod-interaction-design - Future state user journeys
8. prod-user-stories - Actionable requirements
9. prod-assumptions-and-risks - Strategic risk identification
10. prod-success-metrics - KPIs and instrumentation

**Async Skills (2):**
- prod-discussion - Conversational trade-off analysis and decision facilitation
- prod-communicator - Stakeholder communications (5 templates)

### Development Skills (9 skills)
**Specification-driven development pipeline + multi-feature orchestration**

**Orchestration (2 skills):**
- dev-roadmap - Sequence specs from user stories (foundation first, optimal execution order)
- dev-progress - Track completion through roadmap (auto-updated after each merge)

**Core Pipeline (6 skills):**
- dev-constitution - Project standards and technical rules
- dev-specify - Feature specifications from descriptions
- dev-plan - Implementation plans with architecture decisions
- dev-tasks - Executable task breakdown with dependencies
- dev-implement - TDD execution with integrated verification
- dev-finish - Merge workflow with test validation + progress tracking

**Debugging (1 skill):**
- dev-systematic-debugging - Root cause investigation (invoked when bugs found)

**Key feature:** /dev-implement integrates TDD, verification, and debugging methodology through reference files (not separate skills). /dev-finish auto-calls /dev-progress after merge.

### Meta Skills (3)
**Enforcement, discussion, and extensibility**

- shipkit-master - Skill enforcement (auto-loaded at session start)
- dev-discussion - Technical clarification when ambiguity detected (can interrupt any dev workflow)
- dev-writing-skills - Skill authoring guide (TDD approach to creating custom skills)

### Agent Personas (6)
**Specialized behaviors for different workflow stages**

| Agent | Used For |
|-------|----------|
| prod-product-manager | Product discovery, strategic thinking |
| prod-product-designer | User research, interaction design |
| dev-architect | Technical planning, specs, architecture |
| dev-implementer | TDD-focused coding, minimal implementation |
| dev-reviewer | Two-stage code review (spec compliance + quality) |
| any-researcher | Deep research, competitive intel, web search |

---

## Architecture Overview

### Hybrid Structure

**Skill Definitions** → .claude/skills/[skill-name]/SKILL.md
- Instructions Claude reads
- <500 lines each (progressive disclosure)
- Reference implementation files

**Skill Implementation** → .shipkit/skills/[skill-name]/
- scripts/ - Automation (sources shared utilities)
- templates/ - Single adaptive template per skill
- references/ - Extended docs (reference.md, examples.md, user PDFs)
- outputs/ - Protected artifacts (read-only via settings.json)

**Shared Utilities** → .shipkit/scripts/bash/
- common.sh - Shared functions (sourced by all skills)
- check-prerequisites.sh - Validation (called by skills)

### File Protection

settings.json enforces read-only access to:
- .shipkit/skills/*/outputs/** - Only skill scripts can modify
- .shipkit/skills/*/templates/** - Protected templates
- .shipkit/skills/*/scripts/** - Protected automation

**This forces workflow discipline:** You can't bypass skills by editing outputs directly.

### Session Enforcement

**SessionStart hook** automatically loads shipkit-master meta-skill, which:
- Requires checking for skills before EVERY response
- Prevents rationalizing away from skill usage
- Enforces prerequisite checks
- Mandates TodoWrite for skill checklists

**Result:** Skills are non-optional. If a skill exists for the task, Claude uses it.

---

## Quick Start

Clone this repo next to your projects, then install:

```bash
cd your-project
bash ../shipkit/install.sh
```

This creates:
- .claude/skills/ - Skill definitions (Claude reads)
- .claude/agents/ - Agent personas
- .claude/hooks/ - Session enforcement
- .claude/settings.json - File protections + hooks
- .shipkit/skills/ - Skill implementations + outputs
- .shipkit/scripts/ - Shared utilities
- CLAUDE.md - Skill routing guide

---

## Repository Structure (Source)

```
shipkit/
├── install.sh                          # One-command installer
├── install/                            # Everything that gets installed
│   ├── CLAUDE.md                       # Skill routing template
│   ├── settings.json                   # Protections + SessionStart hook
│   ├── skills/                         # Skill SKILL.md files
│   │   ├── shipkit-master/SKILL.md
│   │   ├── prod-strategic-thinking/SKILL.md
│   │   └── [28 other skills...]
│   ├── workspace/                      # Skill implementations
│   │   ├── scripts/bash/common.sh
│   │   └── skills/
│   │       ├── prod-strategic-thinking/
│   │       │   ├── scripts/create-strategy.sh
│   │       │   ├── templates/business-canvas-template.md
│   │       │   ├── references/
│   │       │   │   ├── reference.md
│   │       │   │   ├── examples.md
│   │       │   │   └── README.md
│   │       │   └── outputs/
│   │       └── [other skills...]
│   ├── agents/
│   │   ├── prod-product-manager-agent.md
│   │   └── [5 other agents...]
│   └── hooks/
│       ├── session-start.sh
│       └── run-hook.cmd
│
├── CLAUDE.md                           # Development guide (this repo)
├── README.md                           # This file
├── RESTRUCTURING-PLAN.md               # Implementation tracker
└── help/
    ├── system-overview.html
    └── skills-summary.html
```

---

## What Gets Installed

After install.sh, your project structure:

```
your-project/
├── CLAUDE.md                           # Skill routing + workflow
├── .claude/
│   ├── settings.json                   # Protections + SessionStart
│   ├── skills/                         # Definitions
│   │   ├── shipkit-master/SKILL.md
│   │   └── [29 other skills...]
│   ├── agents/
│   │   └── [6 agent personas...]
│   └── hooks/
│       ├── session-start.sh
│       └── run-hook.cmd
│
└── .shipkit/                           # Implementations + outputs
    ├── scripts/bash/common.sh
    └── skills/
        ├── prod-strategic-thinking/
        │   ├── scripts/create-strategy.sh
        │   ├── templates/business-canvas-template.md
        │   ├── references/
        │   │   ├── reference.md
        │   │   ├── examples.md
        │   │   └── README.md
        │   └── outputs/
        │       └── business-canvas.md  # PROTECTED
        └── [other skills...]
```

**Everything under dot-folders** - no project root pollution!

---

## How It Works

### 1. Session Start Hook Enforces Skills

When Claude Code starts:
1. Runs .claude/hooks/session-start.sh
2. Loads shipkit-master/SKILL.md into Claude's context
3. This makes skill checking mandatory before EVERY response

The shipkit-master meta-skill tells Claude:
- "If there's even a 1% chance a skill applies, you MUST use it"
- Check prerequisites before invoking skills
- Use TodoWrite for skill checklists
- Never rationalize away from skill usage

**Result:** Skills are enforced, not optional.

### 2. Skills Reference Implementation Files

Each SKILL.md tells Claude to:
1. Run the skill's script (e.g., .shipkit/skills/prod-personas/scripts/create-persona.sh)
2. Use the skill's template
3. Read the skill's references for extended guidance

**Scripts ensure consistency:**
- Create files in correct locations
- Use templates (never freestyle)
- Validate inputs
- Handle updates/archiving

### 3. Outputs Are Protected

settings.json denies Claude write access to:
- .shipkit/skills/*/outputs/**
- .shipkit/skills/*/templates/**
- .shipkit/skills/*/scripts/**

**To update outputs, you MUST re-run the skill.** This prevents bypassing workflows.

### 4. Skills Chain Together

Skills have prerequisites (checked automatically):

```
/prod-strategic-thinking
  → checks: none (always first)
  → creates: .shipkit/skills/prod-strategic-thinking/outputs/business-canvas.md

/prod-personas
  → checks: business-canvas.md exists
  → creates: .shipkit/skills/prod-personas/outputs/personas.md
```

If prerequisites are missing, Claude suggests running them first.

### 5. Session Hooks Prompt Next Steps

After completing certain skills, hooks prompt:
- After /prod-strategic-thinking → "Next: /prod-constitution-builder"
- After any prod skill → "Create stakeholder communication? Run /prod-communicator"

These are prompts, not forced - user can decline.

---

## Complete Workflow

### Phase 1: Product Discovery

```
/prod-strategic-thinking                 # Business canvas
  → /prod-constitution-builder           # Product principles
  → /prod-personas                       # User personas
  → /prod-jobs-to-be-done                # JTBD framework
  → /prod-market-analysis                # Competitive research
  → /prod-brand-guidelines               # Visual direction
  → /prod-interaction-design             # User journeys
  → /prod-user-stories                   # Requirements
  → /prod-assumptions-and-risks          # Risk mitigation
  → /prod-success-metrics                # KPIs
```

**Async skills** (call anytime):
- /any-brainstorming - Can interrupt ANY skill when ambiguity detected
- /prod-discussion - Facilitate product decisions through trade-off analysis
- /prod-communicator - Generate stakeholder communications

**Output:** Complete product context in .shipkit/skills/prod-*/outputs/

### Phase 2: Technical Specification

```
/dev-constitution-builder                # Technical standards
  → /dev-specify                         # Feature spec
  → /dev-plan                            # Implementation plan
  → /dev-tasks                           # Executable tasks
```

**Output:** Technical specs in .shipkit/skills/dev-*/outputs/

### Phase 3: Development

```
/dev-using-git-worktrees                 # Create isolated branch
  → /dev-implement                       # TDD + reviews + verification
  → /dev-finishing-a-development-branch  # Merge/PR workflow
```

/dev-implement automatically integrates TDD, reviews, and verification.

**Output:** Shipped feature

---

## Key Features

### Enforced Workflow Discipline

**Session hooks** load shipkit-master enforcement:
- Skills are non-optional (if skill exists, Claude uses it)
- Prerequisites are checked automatically
- TodoWrite is mandatory for checklists
- No rationalizing away from workflows

**File protections** prevent shortcuts:
- Outputs are read-only
- Must re-run skill to update
- Templates are protected
- Scripts are protected

### Research-Driven Product Discovery

**Product skills emphasize real data:**
- /prod-market-analysis requires WebSearch
- Competitor pricing must be specific ($X/mo, not "affordable")
- Customer reviews must be quoted
- Every claim needs a source

**Templates have "RESEARCH REQUIRED" callouts** to prevent guessing.

### Single Adaptive Templates

**No template explosion:**
- One template per skill (not lite/full variants)
- Templates adapt based on context (POC vs MVP vs Established, B2C vs B2B)
- Sections can be marked "Deferred" when not applicable

### Progressive Disclosure

**SKILL.md files are <500 lines:**
- Core instructions only
- Extended guidance in references/ folder
- Users can add their own references (PDFs, research, etc.)
- Claude reads all files in references/ when running skill

### No External Dependencies

- All skills work 100% locally
- Optional: WebSearch (for /prod-market-analysis)
- Optional: GitHub (for /dev-taskstoissues, /dev-finishing-branch)

### Cross-Platform

- Bash scripts (Mac, Linux, Git Bash on Windows)
- PowerShell versions (where applicable)

---

## Current Status

**✅ COMPLETE - Production Ready!**

**Core Skills: 24/24 (100%)** 🎉

**Product Skills:** 12/12 ✅
- Complete product discovery pipeline from strategy through metrics

**Development Skills:** 9/9 ✅
- Orchestration (2/2): roadmap, progress
- Core Pipeline (6/6): constitution, specify, plan, tasks, implement, finish
- Debugging (1/1): systematic-debugging

**Meta Skills:** 3/3 ✅
- shipkit-master (enforcement)
- dev-discussion (technical clarification)
- dev-writing-skills (custom skill authoring)

**Reference Files:** 3/3 ✅
- TDD, verification, and debugging methodologies

**The framework is production-ready with complete multi-feature project orchestration!**

See [Claude Working Documents/REMAINING-WORK.md](Claude Working Documents/REMAINING-WORK.md) for complete details.

---

## Advanced Usage

### Customize Agent Personas

Edit agents in .claude/agents/ for your team:

```markdown
# .claude/agents/dev-implementer-agent.md

## Constraints (customize these)
- Our team uses Vitest, not Jest
- We prefer functional components only
- All API calls go through our SDK
```

### Add Custom References

Drop PDFs, research, docs into any skill's references/ folder:

```
.shipkit/skills/prod-personas/references/
├── reference.md                  # Built-in
├── examples.md                   # Built-in
├── README.md                     # Built-in
├── our-user-interviews.pdf       # YOUR research
└── competitor-personas.pdf       # YOUR intel
```

Claude reads all files when running /prod-personas.

### Generate Stakeholder Communications

After product discovery:

```
User: "Create an investor one-pager"
Claude: [Runs /prod-communicator skill]
        [Reads prod-strategic-thinking, prod-personas, prod-jobs-to-be-done outputs]
        [Creates .shipkit/skills/prod-communicator/outputs/investor-one-pager-YYYYMMDD.md]
```

5 communication templates:
- Investor one-pager
- Executive summary
- Team update
- Customer announcement
- Board deck outline

---

## Skill Script Pattern

All skill scripts follow a consistent pattern for Claude Code automation:

### Script Structure

```bash
#!/usr/bin/env bash
# Script header with description

set -e

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
source "$REPO_ROOT/.shipkit/scripts/bash/common.sh"

# Parse flags (--update, --archive, --skip-prereqs, --cancel)
# ... flag parsing logic ...

# Check prerequisites (declarative, from common.sh)
check_skill_prerequisites "skill-name" "$SKIP_PREREQS"

# Check if output exists (handles --update, --archive flags)
check_output_exists "$OUTPUT_FILE" "Artifact Name" "$UPDATE" "$ARCHIVE"

# Create/update output file
# ... skill-specific logic ...
```

### Decision-Based Flow

Scripts use **structured output** for Claude Code to parse:

1. **Script runs** without flags
2. **Encounters decision point** (file exists, prereq missing)
3. **Exits with structured message**:
   ```
   DECISION_NEEDED: FILE_EXISTS
   MESSAGE: Strategy already exists at: .../business-canvas.md
   OPTIONS: --update (Update existing) | --archive (Create new version) | --cancel (Cancel)
   ```
4. **Claude reads output**, presents options to user
5. **User chooses** (e.g., "update")
6. **Claude reruns** with flag: `./create-strategy.sh --update`
7. **Script executes** chosen action

### Common Flags

All scripts support:
- `--update` - Update existing file
- `--archive` - Archive current, create new version
- `--skip-prereqs` - Skip prerequisite checks
- `--cancel` - Cancel operation
- `--help` - Show usage

### Prerequisite Chain

Managed declaratively in `common.sh`:

```bash
SKILL_PREREQUISITES=(
  ["prod-strategic-thinking"]=""                    # No prereq
  ["prod-personas"]="prod-strategic-thinking"      # Requires strategy
  ["prod-jobs-to-be-done"]="prod-personas"         # Requires personas
  # ... etc
)
```

One line in script:
```bash
check_skill_prerequisites "prod-personas" "$SKIP_PREREQS"
```

If prerequisite missing, exits with:
```
DECISION_NEEDED: PREREQUISITE_MISSING
MESSAGE: This skill works best after: /prod-strategic-thinking
OPTIONS: --skip-prereqs (Continue anyway)
```

### Why This Pattern?

1. **Non-interactive** - Works with Claude Code's Bash tool
2. **User control** - Claude presents decisions, user chooses
3. **Explicit** - Flags make behavior clear
4. **Maintainable** - Prerequisite chain in one place
5. **Consistent** - Same pattern for all 30 skills

---

## Maintenance

### Updating This Repo

When you improve a skill:
1. Edit files in install/
2. Test in a sample project
3. Commit changes
4. Re-install in your projects

### Updating Projects

Re-run installer to get latest skills:

```bash
cd your-project
bash ../shipkit/install.sh
```

**Preserves:**
- Existing outputs (.shipkit/skills/*/outputs/)
- User customizations
- Project-specific constitutions

**Updates:**
- Skill definitions (.claude/skills/)
- Templates (.shipkit/skills/*/templates/)
- Scripts (.shipkit/skills/*/scripts/)
- References (.shipkit/skills/*/references/)

---

## Future Development

The following 8 optional workflow tools have been identified for potential future development. **They are NOT required** - the core framework is complete without them:

### Potential Workflow Enhancements

1. **dev-clarify** - Resolve [NEEDS_CLARIFICATION] markers in specifications
2. **dev-analyze** - Cross-artifact consistency checking (spec/plan/tasks alignment)
3. **dev-using-git-worktrees** - Git worktree isolation for parallel feature development
4. **dev-dispatching-parallel-agents** - Parallel agent dispatch for concurrent task execution
5. **dev-requesting-code-review** - Best practices for PR preparation
6. **dev-receiving-code-review** - Workflow for processing review feedback
7. **dev-checklist** - Validation checklists for specs, plans, and implementations
8. **dev-taskstoissues** - GitHub issues integration for task tracking

These can be added as needed based on team requirements and usage patterns.

---

## Documentation

📖 **[System Overview](help/system-overview.html)** - **START HERE!**
- Visual workflow guide
- Shows how product → dev → implementation works

📖 **[Skills Summary](help/skills-summary.html)**
- Browse all skill prompts
- Implementation progress tracker

📖 **[Restructuring Plan](RESTRUCTURING-PLAN.md)**
- Detailed progress tracker
- Architecture decisions
- Remaining tasks

---

## License

MIT License

---

## Support

- **Quick Start**: help/system-overview.html
- **Progress**: RESTRUCTURING-PLAN.md
- **Development**: CLAUDE.md

---

**Ready to ship products faster?**

```bash
cd your-next-project
bash ../shipkit/install.sh
```

**From strategy to shipped code, all guided by AI.**
