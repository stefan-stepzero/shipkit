---
name: using-shipkit
description: Meta-skill injected at session start - enforces skill usage and workflow
priority: system
---

# Using shipkit

**THIS IS MANDATORY. NOT OPTIONAL. NOT NEGOTIABLE.**

This project uses the shipkit framework. Before responding to ANY user request, you MUST check if a skill applies.

## The Iron Rule

```
BEFORE ANY RESPONSE → CHECK FOR APPLICABLE SKILLS
Even 1% chance a skill applies → USE THE SKILL
```

Do NOT:
- Answer "simple" questions without checking skills first
- Gather information before checking skills
- Assume a skill is overkill
- Rationalize skipping skills "just this once"

## Constitution First

Before ANY significant work, read: `.devkit/memory/constitution.md`

This contains project principles, tech stack, and non-negotiable rules.

## Agent Personas

Agent personas in `.claude/agents/` define specialized behaviors for different workflow stages.

**WHEN TO LOAD AGENT PERSONAS:**

| Context | Load Persona | File |
|---------|--------------|------|
| Product discovery, brainstorming | Discovery Agent | `.claude/agents/discovery-agent.md` |
| Technical planning, specs, architecture | Architect Agent | `.claude/agents/architect-agent.md` |
| Implementation (direct or subagent) | Implementer Agent | `.claude/agents/implementer-agent.md` |
| Code review stages | Reviewer Agent | `.claude/agents/reviewer-agent.md` |
| Research tasks, deep dives | Researcher Agent | `.claude/agents/researcher-agent.md` |

**HOW TO USE:**

1. **At skill start** - Read the relevant persona file
2. **Adopt the personality** - Follow the approach, behaviors, constraints
3. **For subagents** - Include persona in the dispatch prompt

**Example - Starting /implement:**
```
1. Read `.claude/agents/implementer-agent.md`
2. Adopt TDD-focused, disciplined, test-first mindset
3. For each task, follow the persona's approach
```

**Example - Dispatching subagent:**
```
Task("Implement user authentication")
  Context: [Include implementer-agent.md persona]
  Task: [Task details]
  Files: [Relevant files]
```

---

## External Tools & MCPs

Some skills benefit from external tools. Use them proactively when relevant:

### When to Use Web Search

| Skill | Use Web Search For |
|-------|-------------------|
| `/market-analysis` | Competitor websites, pricing, features, reviews |
| `/strategic-thinking` | Market trends, industry benchmarks, comparable companies |
| `/brainstorming` | Existing solutions, prior art, inspiration |
| `/plan` | Library documentation, best practices, tutorials |
| `/implement` | API docs, error solutions, code examples |
| `/systematic-debugging` | Error messages, known issues, Stack Overflow |

### When to Use Other MCPs

| MCP | Use For |
|-----|---------|
| File system | Reading project files, checking what exists |
| GitHub | Checking issues, PRs, comparing with other repos |
| Database | Querying data for analysis skills |
| Browser | Visual inspection of competitor products |

### How to Integrate

**During a skill, if you need external info:**
1. Pause the skill workflow
2. Tell user: "I need to research X to complete this properly"
3. Use the appropriate tool (web search, MCP, etc.)
4. Resume the skill with the gathered info

**Example:**
```
Running /market-analysis...

I'll search for competitor information to complete the analysis.
[Uses web search for "Todoist pricing features 2024"]
[Uses web search for "Asana vs Todoist comparison"]

Now continuing with the analysis using this research...
```

**Don't guess when you can search.** External tools make skills more accurate.

## Skill Routing

Match user intent to skills:

### Product Discovery (ProdKit) - Do in Order

| User Intent | Skill | Prerequisite |
|-------------|-------|--------------|
| Strategy, business model, value prop | `/strategic-thinking` | None (start here) |
| Target users, personas, customers | `/personas` | `.prodkit/strategy/` exists |
| Problems, workflows, current state | `/jobs-to-be-done` | `.prodkit/discovery/personas.md` exists |
| Competition, market, competitors | `/market-analysis` | JTBD exists |
| Brand, visual, personality, tone | `/brand-guidelines` | Market analysis exists |
| User journey, future state, UX | `/interaction-design` | Brand exists |
| User stories, requirements, features | `/user-stories` | Interaction design exists |
| Risks, assumptions, what could fail | `/assumptions-and-risks` | User stories exist |
| KPIs, metrics, success measurement | `/success-metrics` | Assumptions exist |
| Prioritization, trade-offs, ROI | `/trade-off-analysis` | Any time |
| Stakeholder comms, decks, updates | `/communicator` | Any time |

### Technical Specification (devkit)

**Sequential Workflow:**

| User Intent | Skill | Prerequisite |
|-------------|-------|--------------|
| Project rules, standards, update constitution | `/constitution` | None |
| Build feature, add capability, spec | `/specify` | Constitution read |
| Implementation plan, architecture | `/plan` | Spec exists |
| Break into tasks, steps | `/tasks` | Plan exists |
| Implement, execute, build | `/implement` | Tasks exist |
| Clarify requirements | `/clarify` | Spec exists |
| Analyze code, review spec, what does this do | `/analyze` | Code or spec exists |
| Create checklist, validation, QA | `/checklist` | Spec or plan exists |
| Create GitHub issues, push tasks | `/taskstoissues` | Tasks exist + GitHub configured |

**Async (call anytime):**

| User Intent | Skill | When to Trigger |
|-------------|-------|-----------------|
| Ambiguity detected, unclear requirement | `/brainstorming` | Vague requirements, multiple approaches, user uncertainty |

**Note:** `/implement` automatically integrates devkit skills (TDD, verification, debugging, subagent execution). You don't need to call them separately during implementation.

**Note:** `/brainstorming` can interrupt ANY skill when ambiguity is detected. Pause, clarify, resume.

### Development (devkit) - Integrated into devkit

These skills are **automatically used by `/implement`**:

| Skill | Used By /implement For |
|-------|------------------------|
| `/test-driven-development` | Every task: RED → GREEN → REFACTOR |
| `/verification-before-completion` | Before marking any task done |
| `/systematic-debugging` | When tests fail during implementation |
| `/finishing-a-development-branch` | After all tasks complete |
| Subagent execution | Optional mode for large plans (6+ tasks) |

### Development (devkit) - Standalone Use

| User Intent | Skill | When to Use |
|-------------|-------|-------------|
| Create branch, isolated work | `/using-git-worktrees` | Before starting any implementation |
| Request review, PR ready | `/requesting-code-review` | After implementation, before merge |
| Got review feedback | `/receiving-code-review` | When addressing PR comments |
| Run agents in parallel | `/dispatching-parallel-agents` | Multiple independent problems |
| Create new skill | `/writing-skills` | Extending the framework |

### The Complete Workflow

```
/specify → /plan → /tasks → /implement
    ↑         ↑        ↑          ↑
 Formal    Technical  Task     Execution
 spec      plan       breakdown (TDD + reviews)
    │         │        │          │
    └─────────┴────────┴──────────┘
                  ↑
          /brainstorming
          (async - interrupts when
           ambiguity detected)
```

**`/brainstorming` triggers automatically when:**
- Vague requirements detected ("add authentication" - what kind?)
- Multiple valid approaches (REST vs GraphQL)
- User says "I'm not sure" or "what do you think?"
- Missing information (no error handling specified)
- Ambiguous scope ("make it fast" - how fast?)

**Detection happens during any skill** - pause, clarify, resume.

## Prerequisite Enforcement

**ALWAYS check prerequisites before invoking a skill:**

1. Check if required file/folder exists
2. If MISSING → Suggest the prerequisite skill first
3. If user insists → Warn about gaps, then proceed

Example flow:
```
User: "Who are our target users?"
You: Check .prodkit/strategy/business-canvas.md exists?
  → If NO: "Before defining personas, let's define your strategy. Run /strategic-thinking first?"
  → If YES: Proceed with /personas
```

## ProdKit → devkit Integration

**When running devkit, read and reference ProdKit outputs:**

| devkit Skill | Read These ProdKit Files |
|----------------|--------------------------|
| `/specify` | `requirements/user-stories.md`, `brand/personality.md`, `brand/visual-direction.md`, `design/future-state-journeys.md`, `design/interaction-patterns.md` |
| `/plan` | `design/interaction-patterns.md` (navigation, feedback patterns) |
| `/tasks` | `requirements/user-stories.md` (acceptance criteria) |
| `/implement` | `metrics/success-definition.md` (what to instrument) |

## Ambiguity Detection

**During ANY skill, watch for these triggers:**

| Trigger | Action |
|---------|--------|
| Vague requirement | Pause → `/brainstorming` → Resume |
| Multiple valid approaches | Pause → `/brainstorming` → Resume |
| User says "I'm not sure" | Pause → `/brainstorming` → Resume |
| Missing critical info | Pause → `/brainstorming` → Resume |
| "etc.", "as needed", "appropriate" | Pause → `/brainstorming` → Resume |

**Format when pausing:**
```
I'm pausing /[current skill] - I've detected ambiguity:

[State the specific unclear point]

Let me clarify before continuing...
```

**Don't pause for:**
- Minor details with reasonable defaults
- Low-impact choices
- Things inferable from context

## Red Flags - You Are Rationalizing

If you think any of these, STOP:
- "This is just a simple question"
- "I'll check skills after understanding what they need"
- "No skill applies to this"
- "Using a skill would be overkill"
- "Let me just quickly..."

These are rationalizations. Check skills FIRST.

## Workflow Summary

```
1. User request arrives
2. CHECK: Does any skill apply? (even 1% chance = yes)
3. CHECK: Prerequisites exist?
4. If missing prerequisites → Suggest prerequisite skill
5. READ: Constitution (for implementation work)
6. READ: Relevant .prodkit/ artifacts (for devkit work)
7. INVOKE: The appropriate skill
8. FOLLOW: Skill instructions exactly
9. SUGGEST: Next skill in the workflow
```

**Skills use scripts. Scripts use templates. This ensures consistency.**

DO NOT freestyle file creation. DO NOT skip the workflow.

---

## Always Suggest Next Skill

**MANDATORY: After completing ANY skill, suggest the next logical skill.**

### devkit Workflow (always suggest next):
```
/specify   → "Spec complete. Next: /plan to create implementation plan"
/plan      → "Plan complete. Next: /tasks to break into executable tasks"
/tasks     → "Tasks complete. Next: /implement to start building"
/implement → "Implementation complete. /finishing-a-development-branch triggered for merge/PR"
```

**Note:** `/implement` automatically runs TDD, reviews, and verification for each task. For 6+ tasks, it offers subagent execution mode for fresh context per task.

**Note:** `/brainstorming` is async - it can interrupt any skill when ambiguity is detected, then resume the original skill.

### ProdKit Workflow (always suggest next):
```
/strategic-thinking → "Strategy complete. Next: /constitution-builder --product to define product principles"
/constitution-builder --product → "Product constitution created. Next: /personas to define target users"
/personas          → "Personas complete. Next: /jobs-to-be-done to map current workflows"
/jobs-to-be-done   → "JTBD complete. Next: /market-analysis to analyze competition"
/market-analysis   → "Analysis complete. Next: /brand-guidelines to define visual direction"
/brand-guidelines  → "Brand complete. Next: /interaction-design to design user journeys"
/interaction-design → "Design complete. Next: /user-stories to write requirements"
/user-stories      → "Stories complete. Next: /assumptions-and-risks to identify risks"
/assumptions-and-risks → "Risks complete. Next: /success-metrics to define KPIs"
/success-metrics   → "Metrics complete. Product discovery done! Next: /constitution-builder --technical"
/constitution-builder --technical → "Technical constitution complete. Next: /specify to write technical specs"
```

### Format for Next Skill Suggestion:
```
✅ [Skill name] complete.

📁 Created: [list of files created]

👉 **Next step:** `/[next-skill]` - [one line description]

Would you like to proceed with `/[next-skill]`?
```

**Never end a skill without suggesting what comes next.**
