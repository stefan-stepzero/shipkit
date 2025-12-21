# Project Instructions for Claude

This project uses the **shipkit** framework for structured product development and specification-driven implementation.

## Before Starting Any Significant Work

**Always read the project constitution first:**
- Location: `.claude/constitution.md`
- Contains: Project principles, tech stack, coding standards, and non-negotiable rules
- Purpose: Ensures consistency across all development work

**Load the appropriate agent persona:**
- Location: `.claude/agents/`
- Skills automatically specify which agent to load
- Adopt the persona's personality, approach, and constraints

---

## External Tools & MCPs

**Use external tools proactively during skills when they add value:**

| Skill | External Tool | Use For |
|-------|---------------|---------|
| `/market-analysis` | Web Search | Competitor info, pricing, features, reviews |
| `/strategic-thinking` | Web Search | Market trends, benchmarks, comparable companies |
| `/brainstorming` | Web Search | Existing solutions, prior art, inspiration |
| `/plan` | Web Search | Library docs, best practices |
| `/implement` | Web Search | API docs, error solutions |
| `/systematic-debugging` | Web Search | Error messages, Stack Overflow |

**Other MCPs:** GitHub (issues, PRs), Browser (visual inspection), Database (data queries)

**Rule:** Don't guess when you can search. Pause skill → research → resume with real data.

---

## Skill Routing - Match User Intent to Skills

When the user asks something, match their intent to the appropriate skill:

### Product Discovery Triggers

| User Says | Skill | Prerequisites |
|-----------|-------|---------------|
| "What should we build?", "Define our strategy", "Business model", "Value proposition" | `/strategic-thinking` | None (start here) |
| "Who are our users?", "Target customer", "Create personas" | `/personas` | Strategy exists (`.prodkit/strategy/business-canvas.md`) |
| "What problem do we solve?", "User workflows", "Current state" | `/jobs-to-be-done` | Personas exist (`.prodkit/discovery/personas.md`) |
| "Competition", "Market analysis", "Competitors" | `/market-analysis` | JTBD exists (`.prodkit/discovery/jobs-to-be-done.md`) |
| "Brand", "Visual direction", "Personality", "Tone" | `/brand-guidelines` | Market analysis exists |
| "User journey", "Future state", "Interaction design" | `/interaction-design` | Brand exists (`.prodkit/brand/`) |
| "User stories", "Requirements", "Features list" | `/user-stories` | Interaction design exists |
| "Risks", "Assumptions", "What could go wrong" | `/assumptions-and-risks` | User stories exist |
| "KPIs", "Success metrics", "How do we measure" | `/success-metrics` | Assumptions exist |
| "Should we build X?", "Prioritize features", "ROI", "Trade-offs" | `/trade-off-analysis` | Any time (async) |
| "Stakeholder update", "Investor deck", "Team summary" | `/communicator` | Any time (async) |

### Technical Specification Triggers

| User Says | Skill | Prerequisites |
|-----------|-------|---------------|
| "Project rules", "Update constitution", "What are our standards" | `/constitution` | None |
| "Build feature X", "I want to add...", "Create a spec for..." | `/specify` | Constitution customized recommended |
| "How should we implement?", "Technical plan", "Architecture" | `/plan` | Spec exists for feature |
| "Break this into tasks", "What are the steps?" | `/tasks` | Plan exists for feature |
| "Start implementing", "Execute the plan", "Build it" | `/implement` | Tasks exist for feature |
| "Clarify requirements", "I don't understand the spec" | `/clarify` | Spec exists |
| "Analyze this code", "Review this spec", "What does this do" | `/analyze` | Code or spec exists |
| "Create a checklist", "Validation checklist", "QA checklist" | `/checklist` | Spec or plan exists |
| "Create GitHub issues", "Push tasks to GitHub" | `/taskstoissues` | Tasks exist + GitHub configured |

### Development Workflow Triggers

| User Says | Skill | Prerequisites |
|-----------|-------|---------------|
| "Create a branch", "Isolated development" | `/using-git-worktrees` | Git repo |
| "Start implementing", "Build it" | `/implement` | Tasks exist (integrates TDD, reviews, verification) |
| "Brainstorm", "Ideas for...", "What are options?" | `/brainstorming` | Any time (async - can interrupt any skill) |
| "Finish this branch", "Ready to merge", "Complete PR" | `/finishing-a-development-branch` | Work complete on branch |
| "Request review", "PR ready", "Need feedback on code" | `/requesting-code-review` | Code ready for review |
| "Got review feedback", "Address review comments" | `/receiving-code-review` | Review received |
| "Run agents in parallel", "Concurrent work" | `/dispatching-parallel-agents` | Multiple independent tasks |
| "Create a new skill", "Write a skill" | `/writing-skills` | Any time |

**Note:** `/implement` automatically uses TDD, verification, and systematic-debugging. You don't need to invoke these separately.

---

## Prerequisite Enforcement

**Before invoking a skill, check if prerequisites exist:**

1. If prerequisite file/folder is missing → Tell user and suggest the prerequisite skill first
2. If user insists on skipping → Warn about gaps but proceed

Example:
- User: "Who are our target users?"
- Check: Does `.prodkit/strategy/business-canvas.md` exist?
- If NO → "Before defining personas, we should define your product strategy. Would you like to run `/strategic-thinking` first?"
- If YES → Proceed with `/personas`

---

## ProdKit Sequential Workflow

These must be done in order for a complete product discovery:

```
1. /strategic-thinking           →  Creates: .prodkit/strategy/
         ↓
   /constitution-builder --product  →  Creates: .claude/constitution.md (product section)
         ↓
2. /personas                     →  Creates: .prodkit/discovery/personas.md
         ↓
3. /jobs-to-be-done              →  Creates: .prodkit/discovery/jobs-to-be-done.md
         ↓
4. /market-analysis              →  Creates: .prodkit/discovery/market-analysis.md
         ↓
5. /brand-guidelines             →  Creates: .prodkit/brand/
         ↓
6. /interaction-design           →  Creates: .prodkit/design/
         ↓
7. /user-stories                 →  Creates: .prodkit/requirements/
         ↓
8. /assumptions-risks            →  Creates: .prodkit/discovery/assumptions-risks.md
         ↓
9. /success-metrics              →  Creates: .prodkit/metrics/
```

**Async skill:** `/brainstorming` can interrupt ANY skill when ambiguity is detected.

---

## devkit Sequential Workflow

For implementing features:

```
/constitution-builder --technical  →  Adds technical section to .claude/constitution.md
    ↓
/specify  →  Creates: .devkit/specs/NNN-feature/spec.md
    ↓
/plan     →  Creates: .devkit/specs/NNN-feature/plan.md (reads constitution!)
    ↓
/tasks    →  Creates: .devkit/specs/NNN-feature/tasks.md
    ↓
/implement →  Executes tasks with TDD + two-stage review
```

**/implement** automatically integrates:
- TDD (RED → GREEN → REFACTOR for each task)
- Spec Compliance Review (matches requirements?)
- Code Quality Review (clean code?)
- Verification before marking complete

---

## ProdKit → devkit Integration

**When running devkit skills, reference ProdKit outputs as context:**

| devkit Skill | Read These ProdKit Artifacts |
|----------------|------------------------------|
| `/specify` | `requirements/user-stories.md`, `brand/personality.md`, `brand/visual-direction.md`, `design/future-state-journeys.md`, `design/interaction-patterns.md` |
| `/plan` | `design/interaction-patterns.md` (navigation, feedback patterns) |
| `/tasks` | `requirements/user-stories.md` (acceptance criteria) |
| `/implement` | `metrics/success-definition.md` (what to instrument) |

**Before writing a spec:**
1. Check if `.prodkit/` has relevant artifacts
2. If YES → Read them and reference in the spec
3. If NO → Ask user if they want to run product discovery first, or proceed without

**Example spec introduction referencing ProdKit:**
```markdown
## Overview
This feature implements [User Story US-003] from `.prodkit/requirements/user-stories.md`.

Brand voice follows `.prodkit/brand/personality.md` (professional, efficient).
```

---

## Available Skills

### Product Discovery (ProdKit)
Sequential workflow - complete in order for new products/features:
1. `/strategic-thinking` - Define business strategy and value proposition
2. `/constitution-builder --product` - Define product principles (after strategy)
3. `/personas` - Identify and document target users
4. `/jobs-to-be-done` - Map current state workflows
5. `/market-analysis` - Analyze competitive landscape
6. `/brand-guidelines` - Define visual direction and personality
7. `/interaction-design` - Design future state user journeys
8. `/user-stories` - Write actionable requirements
9. `/assumptions-and-risks` - Identify strategic risks
10. `/success-metrics` - Define KPIs and success criteria

Async skills (use anytime):
- `/brainstorming` - Can interrupt ANY skill when ambiguity detected
- `/trade-off-analysis` - Prioritize features by ROI
- `/communicator` - Generate stakeholder communications

### Technical Specification (devkit)
- `/constitution-builder --technical` - Define technical standards (before specs)
- `/specify` - Create feature specifications from descriptions
- `/plan` - Generate implementation plans (reads constitution)
- `/tasks` - Break plans into executable tasks
- `/implement` - Execute tasks with integrated TDD + reviews
- `/clarify` - Clarify specification requirements
- `/analyze` - Analyze existing code or specs
- `/checklist` - Create validation checklists
- `/taskstoissues` - Push tasks to GitHub issues

### Development Workflow (devkit)
**Integrated into /implement:**
- TDD, verification, systematic-debugging (automatic)

**Standalone skills:**
- `/using-git-worktrees` - Isolated branch development
- `/finishing-a-development-branch` - Complete and merge branches
- `/requesting-code-review` - Prepare for code review
- `/receiving-code-review` - Process review feedback
- `/dispatching-parallel-agents` - Run agents concurrently
- `/writing-skills` - Create new skills

## Recommended Workflow

### For New Features
1. Read `.devkit/memory/constitution.md`
2. Use `/specify` to create the spec
3. Use `/plan` to create implementation plan
4. Use `/tasks` to break into tasks
5. Use `/implement` to execute

### For Product Discovery
1. Read `.devkit/memory/constitution.md`
2. Follow ProdKit skills 1-9 in sequence
3. Use `/specify` to translate discoveries into specs

## Project Structure

```
.claude/
  constitution.md   # Project rules (created by /constitution-builder)
  agents/           # Agent persona definitions
  skills/           # Skill definitions (auto-discovered)
  hooks/            # Session start hooks
.devkit/
  specs/            # Feature specifications
  scripts/          # Automation scripts
  templates/        # Document templates
.prodkit/
  inputs/           # Research files and user data
  strategy/         # Business strategy artifacts
  discovery/        # Personas, JTBD, market analysis
  requirements/     # User stories
  comms/            # Generated communications
```

## Key Behaviors

1. **Match intent to skills** - When user asks something, check the routing tables above
2. **Load agent personas** - Each skill specifies which agent persona to adopt
3. **Check prerequisites** - Before invoking a skill, verify required artifacts exist
4. **Suggest prerequisites** - If missing, offer to run the prerequisite skill first
5. **Read constitution** - Before any significant implementation work (`.claude/constitution.md`)
6. **Reference ProdKit in devkit** - When writing specs/plans, read and cite relevant `.prodkit/` artifacts
7. **Use scripts** - Skills call scripts; never create files manually outside the workflow
8. **Follow the chain** - ProdKit 1→9, then devkit specify→plan→tasks→implement
9. **Watch for ambiguity** - `/brainstorming` can interrupt any skill when uncertainty detected
10. **Always suggest next skill** - After completing any skill, tell user what comes next

**Don't freestyle.** The skills ensure consistency, use templates, and respect the constitution.

---

## Always Suggest Next Skill

**After completing ANY skill, suggest the next logical skill.**

### ProdKit Chain:
```
/strategic-thinking         → Next: /constitution-builder --product
/constitution-builder --product → Next: /personas
/personas                   → Next: /jobs-to-be-done
/jobs-to-be-done            → Next: /market-analysis
/market-analysis            → Next: /brand-guidelines
/brand-guidelines           → Next: /interaction-design
/interaction-design         → Next: /user-stories
/user-stories               → Next: /assumptions-and-risks
/assumptions-and-risks      → Next: /success-metrics
/success-metrics            → Next: /constitution-builder --technical
```

### devkit Chain:
```
/constitution-builder --technical → Next: /specify
/specify                    → Next: /plan
/plan                       → Next: /tasks
/tasks                      → Next: /implement
/implement                  → Next: /finishing-a-development-branch
```

### Output Format:
```
✅ [Skill] complete.
📁 Created: [files]
👉 Next: /[next-skill] - [description]

Proceed with /[next-skill]?
```
