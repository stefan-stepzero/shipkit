# Project Instructions for Claude

This project uses the **Shipkit** framework for structured product development and specification-driven implementation.

**24 core skills** organized in three categories:
- **12 Product Skills** - Product discovery & strategy (prod-*)
- **9 Development Skills** - Technical specs, orchestration & workflow (dev-*)
- **3 Meta Skills** - Enforcement, discussion & skill authoring

Plus **6 agent personas** that specialize behaviors for different workflow stages.

---

## Before Starting Any Significant Work

**Always read the product constitution first (if it exists):**
- Location: `.shipkit/skills/prod-constitution-builder/outputs/product-constitution.md`
- Contains: Project type (POC/MVP/Greenfield/etc), scope boundaries, quality standards
- Purpose: Right-sizes product discovery and development based on project type

**Load the appropriate agent persona:**
- Location: `.claude/agents/`
- Skills automatically specify which agent to load
- Adopt the persona's personality, approach, and constraints

---

## External Tools & MCPs

**Use external tools proactively during skills when they add value:**

| Skill | External Tool | Use For |
|-------|---------------|---------|
| `/prod-market-analysis` | Web Search | Competitor info, pricing, features, reviews |
| `/prod-strategic-thinking` | Web Search | Market trends, benchmarks, comparable companies |
| `/prod-discussion` | Web Search | Research for decision-making |
| `/dev-plan` | Web Search | Library docs, best practices |
| `/dev-implement` | Web Search | API docs, error solutions |
| `/dev-systematic-debugging` | Web Search | Error messages, Stack Overflow |

**Other MCPs:** GitHub (issues, PRs), Browser (visual inspection), Database (data queries)

**Rule:** Don't guess when you can search. Pause skill → research → resume with real data.

---

## Skill Routing - Match User Intent to Skills

When the user asks something, match their intent to the appropriate skill:

### Product Discovery Triggers

| User Says | Skill | Prerequisites |
|-----------|-------|---------------|
| "What should we build?", "Define our strategy", "Business model", "Value proposition" | `/prod-strategic-thinking` | None (start here) |
| "Set product principles", "Define project scope", "POC or MVP?" | `/prod-constitution-builder` | Strategic thinking recommended |
| "Who are our users?", "Target customer", "Create personas" | `/prod-personas` | Constitution exists (optional but recommended) |
| "What problem do we solve?", "User workflows", "Current state" | `/prod-jobs-to-be-done` | Personas exist |
| "Competition", "Market analysis", "Competitors" | `/prod-market-analysis` | JTBD exists |
| "Brand", "Visual direction", "Personality", "Tone" | `/prod-brand-guidelines` | Market analysis exists |
| "User journey", "Future state", "Interaction design" | `/prod-interaction-design` | Brand exists |
| "User stories", "Requirements", "Features list" | `/prod-user-stories` | Interaction design exists |
| "Risks", "Assumptions", "What could go wrong" | `/prod-assumptions-and-risks` | User stories exist |
| "KPIs", "Success metrics", "How do we measure" | `/prod-success-metrics` | Assumptions exist |
| "Should we build X?", "Prioritize features", "Trade-offs" | `/prod-discussion` | Any time (async) |
| "Stakeholder update", "Investor deck", "Team summary" | `/prod-communicator` | Any time (async) |

### Technical Specification Triggers

| User Says | Skill | Prerequisites |
|-----------|-------|---------------|
| "Reference project rules", "What are our standards" | `/dev-constitution` | Constitution exists |
| "Build feature X", "I want to add...", "Create a spec for..." | `/dev-specify` | Constitution customized recommended |
| "How should we implement?", "Technical plan", "Architecture" | `/dev-plan` | Spec exists for feature |
| "Break this into tasks", "What are the steps?" | `/dev-tasks` | Plan exists for feature |
| "Start implementing", "Execute the plan", "Build it" | `/dev-implement` | Tasks exist for feature |
| "Technical clarification needed", "Ambiguous requirement" | `/dev-discussion` | Any time (can interrupt workflows) |
| "Create a new skill", "Write a skill" | `/dev-writing-skills` | Any time |

### Multi-Feature Orchestration Triggers

| User Says | Skill | Prerequisites |
|-----------|-------|---------------|
| "Sequence multiple features", "Create roadmap", "What order?" | `/dev-roadmap` | User stories exist |
| "Track progress", "What's done?", "Update status" | `/dev-progress` | Roadmap exists |
| "Finish this feature", "Ready to merge", "Complete branch" | `/dev-finish` | Work complete on branch |

**Note:** `/dev-implement` automatically integrates TDD, two-stage review, and verification. You don't need to invoke these separately.

---

## Prerequisite Enforcement

**Before invoking a skill, check if prerequisites exist:**

1. If prerequisite file/folder is missing → Tell user and suggest the prerequisite skill first
2. If user insists on skipping → Warn about gaps but proceed

Example:
- User: "Who are our target users?"
- Check: Does `.shipkit/skills/prod-constitution-builder/outputs/product-constitution.md` exist?
- If YES → Check project type, adjust persona count accordingly
- Check: Does `.shipkit/skills/prod-strategic-thinking/outputs/business-canvas.md` exist?
- If NO → "Before defining personas, we should define your product strategy. Would you like to run `/prod-strategic-thinking` first?"
- If YES → Proceed with `/prod-personas`

---

## Product Discovery Sequential Workflow

These must be done in order for a complete product discovery:

```
1. /prod-strategic-thinking           →  Creates: .shipkit/skills/prod-strategic-thinking/outputs/business-canvas.md
         ↓
2. /prod-constitution-builder         →  Creates: .shipkit/skills/prod-constitution-builder/outputs/product-constitution.md
         ↓                                        (6 templates: B2B/B2C Greenfield, Experimental, Side MVP/POC, Existing Project)
3. /prod-personas                     →  Creates: .shipkit/skills/prod-personas/outputs/personas.md
         ↓                                        (Count varies: POC=1, Greenfield=3-5)
4. /prod-jobs-to-be-done              →  Creates: .shipkit/skills/prod-jobs-to-be-done/outputs/jobs-to-be-done.md
         ↓                                        (Depth varies by project type)
5. /prod-market-analysis              →  Creates: .shipkit/skills/prod-market-analysis/outputs/market-analysis.md
         ↓
6. /prod-brand-guidelines             →  Creates: .shipkit/skills/prod-brand-guidelines/outputs/brand-guidelines.md
         ↓
7. /prod-interaction-design           →  Creates: .shipkit/skills/prod-interaction-design/outputs/interaction-design.md
         ↓
8. /prod-user-stories                 →  Creates: .shipkit/skills/prod-user-stories/outputs/user-stories.md
         ↓                                        (AC rigor varies by project type)
9. /prod-assumptions-and-risks        →  Creates: .shipkit/skills/prod-assumptions-and-risks/outputs/assumptions-and-risks.md
         ↓
10. /prod-success-metrics             →  Creates: .shipkit/skills/prod-success-metrics/outputs/success-metrics.md
```

**Async skills (can interrupt any workflow):**
- `/prod-discussion` - Conversational trade-off analysis when ambiguity detected
- `/prod-communicator` - Generate stakeholder communications at any time

**Output:** Complete product context in `.shipkit/skills/prod-*/outputs/`

---

## Development Sequential Workflow

For implementing features:

### Option 1: Single Feature (Simple)
```
/dev-constitution  →  Reference: .shipkit/skills/dev-constitution-builder/outputs/technical-constitution.md
    ↓
/dev-specify  →  Creates: .shipkit/skills/dev-specify/outputs/001-feature-name/spec.md
    ↓
/dev-plan     →  Creates: .shipkit/skills/dev-specify/outputs/001-feature-name/plan.md (reads constitution!)
    ↓
/dev-tasks    →  Creates: .shipkit/skills/dev-specify/outputs/001-feature-name/tasks.md
    ↓
/dev-implement →  Executes tasks with TDD + two-stage review
    ↓
/dev-finish   →  Merge/PR workflow with test validation
```

### Option 2: Multi-Feature (Orchestrated)
```
/dev-constitution  →  Reference project standards
    ↓
[Create specs for all features using /dev-specify]
    ↓
/dev-roadmap  →  Creates: .shipkit/skills/dev-roadmap/outputs/roadmap.md
    ↓          (Sequences specs: foundation first, optimal order)
[For each spec in roadmap order:]
    ↓
/dev-plan → /dev-tasks → /dev-implement → /dev-finish
    ↓
/dev-progress  →  Auto-updated after each /dev-finish
```

**/dev-implement** automatically integrates:
- TDD (RED → GREEN → REFACTOR for each task)
- Spec Compliance Review (matches requirements?)
- Code Quality Review (clean code?)
- Verification before marking complete
- Systematic debugging (when bugs found)

---

## Product → Development Integration

**When running development skills, reference product outputs as context:**

| Dev Skill | Read These Product Artifacts (if they exist) |
|----------------|------------------------------|
| `/dev-specify` | `prod-user-stories/outputs/user-stories.md`, `prod-brand-guidelines/outputs/*`, `prod-interaction-design/outputs/*` |
| `/dev-plan` | `prod-interaction-design/outputs/interaction-design.md` (navigation, feedback patterns) |
| `/dev-tasks` | `prod-user-stories/outputs/user-stories.md` (acceptance criteria) |
| `/dev-implement` | `prod-success-metrics/outputs/success-metrics.md` (what to instrument) |

**Before writing a spec:**
1. Check if `.shipkit/skills/prod-*/outputs/` has relevant artifacts
2. If YES → Read them and reference in the spec
3. If NO → Ask user if they want to run product discovery first, or proceed without

**Example spec introduction referencing product outputs:**
```markdown
## Overview
This feature implements [User Story US-003] from `prod-user-stories/outputs/user-stories.md`.

Brand voice follows `prod-brand-guidelines/outputs/personality.md` (professional, efficient).
```

---

## Available Skills

### Product Skills (12 skills)

**Sequential Workflow (10 skills):**
1. `/prod-strategic-thinking` - Define business strategy and value proposition
2. `/prod-constitution-builder` - Create product constitution (6 project types: POC/MVP/Greenfield/Experimental/Existing)
3. `/prod-personas` - Identify and document target users
4. `/prod-jobs-to-be-done` - Map current state workflows and pain points
5. `/prod-market-analysis` - Analyze competitive landscape
6. `/prod-brand-guidelines` - Define visual direction and personality
7. `/prod-interaction-design` - Design future state user journeys
8. `/prod-user-stories` - Write actionable requirements with acceptance criteria
9. `/prod-assumptions-and-risks` - Identify strategic risks
10. `/prod-success-metrics` - Define KPIs and instrumentation

**Async Skills (2 skills):**
- `/prod-discussion` - Conversational trade-off analysis and decision facilitation
- `/prod-communicator` - Generate stakeholder communications (5 templates)

### Development Skills (9 skills)

**Orchestration (2 skills):**
- `/dev-roadmap` - Sequence specs from user stories (foundation first, optimal order)
- `/dev-progress` - Track completion through roadmap (auto-updated after each merge)

**Core Pipeline (6 skills):**
- `/dev-constitution` - Reference existing project constitution and technical rules
- `/dev-specify` - Create feature specifications from descriptions
- `/dev-plan` - Generate implementation plans (reads constitution)
- `/dev-tasks` - Break plans into executable tasks
- `/dev-implement` - Execute tasks with integrated TDD + reviews + verification
- `/dev-finish` - Merge workflow with test validation + auto progress tracking

**Debugging (1 skill):**
- `/dev-systematic-debugging` - 4-phase root cause investigation (auto-invoked by /dev-implement when bugs found)

### Meta Skills (3 skills)
- `/shipkit-master` - Enforcement meta-skill (auto-loaded at session start via SessionStart hook)
- `/dev-discussion` - Technical clarification when ambiguity detected (can interrupt any dev workflow)
- `/dev-writing-skills` - Skill authoring guide (TDD approach to creating custom skills)

---

## Project Structure

```
.claude/
  settings.json     # Permissions, hooks, file protections
  agents/           # Agent persona definitions (6 agents)
  skills/           # Skill definitions (24 SKILL.md files)
  hooks/            # SessionStart hook (loads shipkit-master)

.shipkit/
  scripts/bash/
    common.sh       # Shared utilities (sourced by all skill scripts)
  skills/
    prod-strategic-thinking/
      scripts/       # create-strategy.sh
      templates/     # business-canvas-template.md
      references/    # reference.md, examples.md, user PDFs
      outputs/       # business-canvas.md (PROTECTED - read-only)
    prod-constitution-builder/
      scripts/       # build-constitution.sh
      templates/     # 6 constitution templates (b2b-saas-greenfield.md, etc.)
      outputs/       # product-constitution.md (PROTECTED)
    [... other prod-* skills ...]
    dev-specify/
      outputs/       # 001-feature-name/spec.md (PROTECTED)
    dev-roadmap/
      outputs/       # roadmap.md (PROTECTED)
    dev-progress/
      outputs/       # progress.md (PROTECTED - auto-updated)
    [... other dev-* skills ...]
```

**File Protection:** `.claude/settings.json` enforces read-only access to:
- `.shipkit/skills/*/outputs/**` - Only skill scripts can modify
- `.shipkit/skills/*/templates/**` - Protected templates
- `.shipkit/skills/*/scripts/**` - Protected automation

**This forces workflow discipline:** You can't bypass skills by editing outputs directly.

---

## Key Behaviors

1. **Match intent to skills** - When user asks something, check the routing tables above
2. **Load agent personas** - Each skill specifies which agent persona to adopt
3. **Check prerequisites** - Before invoking a skill, verify required artifacts exist
4. **Suggest prerequisites** - If missing, offer to run the prerequisite skill first
5. **Read constitution** - Before product/dev work, check if product constitution exists
6. **Constitution-driven behavior** - Adjust skill depth/rigor based on project type (POC vs Greenfield)
7. **Use scripts** - Skills call scripts; never create files manually outside the workflow
8. **Follow the chain** - Product discovery 1→10, then dev pipeline specify→plan→tasks→implement→finish
9. **Watch for ambiguity** - `/prod-discussion` or `/dev-discussion` can interrupt any workflow when uncertainty detected
10. **Always suggest next skill** - After completing any skill, tell user what comes next

**Don't freestyle.** The skills ensure consistency, use templates, and respect the constitution.

---

## Always Suggest Next Skill

**After completing ANY skill, suggest the next logical skill.**

### Product Discovery Chain:
```
/prod-strategic-thinking         → Next: /prod-constitution-builder
/prod-constitution-builder       → Next: /prod-personas
/prod-personas                   → Next: /prod-jobs-to-be-done
/prod-jobs-to-be-done            → Next: /prod-market-analysis
/prod-market-analysis            → Next: /prod-brand-guidelines
/prod-brand-guidelines           → Next: /prod-interaction-design
/prod-interaction-design         → Next: /prod-user-stories
/prod-user-stories               → Next: /prod-assumptions-and-risks
/prod-assumptions-and-risks      → Next: /prod-success-metrics
/prod-success-metrics            → Next: /dev-constitution (if starting development)
```

### Development Chain (Single Feature):
```
/dev-constitution  → Next: /dev-specify
/dev-specify       → Next: /dev-plan
/dev-plan          → Next: /dev-tasks
/dev-tasks         → Next: /dev-implement
/dev-implement     → Next: /dev-finish
/dev-finish        → Feature complete!
```

### Development Chain (Multi-Feature):
```
/dev-constitution  → Next: Create all specs with /dev-specify
[After all specs]  → Next: /dev-roadmap
/dev-roadmap       → Next: Implement first spec in roadmap order
[After each /dev-finish] → /dev-progress auto-updates
```

### Output Format:
```
✅ [Skill] complete.
📁 Created: [files]
👉 Next: /[next-skill] - [description]

Proceed with /[next-skill]?
```

---

## Constitution-Driven Development

Shipkit adapts to your project type via the **product constitution**:

**6 Project Types:**
1. **B2B SaaS Greenfield** - Enterprise products (comprehensive discovery)
2. **B2C SaaS Greenfield** - Consumer products (UX-focused discovery)
3. **Experimental** - Technology exploration (learning-focused, minimal product work)
4. **Side Project MVP** - 1-4 week builds (medium depth)
5. **Side Project POC** - Days to 1 week (minimal depth, prove concept only)
6. **Existing Project** - Adding Shipkit to established codebase (document current state)

**How Constitution Affects Skills:**

| Skill | POC Behavior | Greenfield Behavior |
|-------|-------------|---------------------|
| `/prod-personas` | 1 persona only | 3-5 personas (B2B), 2-3 (B2C) |
| `/prod-jobs-to-be-done` | 1 job, shallow analysis | 2-4 jobs per persona, deep analysis |
| `/prod-user-stories` | Minimal ACs (happy path only) | Comprehensive ACs (all edge cases) |
| `/prod-brand-guidelines` | Skip entirely | Full brand system |

**Result:** POC projects move fast with minimal ceremony. Greenfield projects get comprehensive discovery.

---

## Agent Personas (6 agents)

Skills automatically load specialized agent personas:

| Agent | Used For | Location |
|-------|----------|----------|
| **prod-product-manager** | Strategy, personas, JTBD, market analysis, user stories, metrics | `.claude/agents/prod-product-manager-agent.md` |
| **prod-product-designer** | Brand, interaction design, communicator | `.claude/agents/prod-product-designer-agent.md` |
| **dev-architect** | Specs, plans, tasks, roadmap | `.claude/agents/dev-architect-agent.md` |
| **dev-implementer** | TDD-focused coding, minimal implementation | `.claude/agents/dev-implementer-agent.md` |
| **dev-reviewer** | Two-stage review (spec compliance + quality) | `.claude/agents/dev-reviewer-agent.md` |
| **any-researcher** | Deep research, market analysis, web search | `.claude/agents/any-researcher-agent.md` |

---

## Common Workflows

### Full Product Development (Greenfield)
```bash
/prod-strategic-thinking         # Define strategy
/prod-constitution-builder       # Choose project type (B2B/B2C Greenfield)
/prod-personas                   # 3-5 personas
/prod-jobs-to-be-done            # Deep JTBD analysis
/prod-market-analysis            # Full competitive landscape
/prod-brand-guidelines           # Complete brand system
/prod-interaction-design         # User journeys
/prod-user-stories               # Comprehensive ACs
/prod-assumptions-and-risks      # Risk mitigation
/prod-success-metrics            # KPIs
/dev-constitution                # Technical standards
/dev-specify                     # Feature specs
/dev-roadmap                     # Sequence all features
/dev-plan                        # First feature plan
/dev-tasks                       # Break into tasks
/dev-implement                   # Execute with TDD
/dev-finish                      # Merge + auto-update progress
```

### Quick POC (Fast Validation)
```bash
/prod-strategic-thinking         # Core hypothesis
/prod-constitution-builder       # Choose "Side Project POC"
/prod-personas                   # 1 persona only
/prod-jobs-to-be-done            # 1 job, shallow
/prod-user-stories               # Happy path only
/dev-constitution                # Minimal standards
/dev-specify                     # One spec
/dev-plan                        # Quick plan
/dev-tasks                       # Essential tasks
/dev-implement                   # Build fast
```

### Existing Codebase (Add One Feature)
```bash
/dev-constitution                # Reference existing standards
/dev-specify                     # New feature spec
/dev-plan                        # Implementation plan
/dev-tasks                       # Task breakdown
/dev-implement                   # Execute
/dev-finish                      # Merge
```

---

**Ready to build? Start with `/prod-strategic-thinking` or `/dev-constitution` depending on whether you need product discovery or just want to start coding.**
