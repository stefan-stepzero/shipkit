---
name: shipkit-goals
description: "Capture structured project goals that bridge why.json vision to concrete specs. Triggers: 'set goals', 'project goals', 'objectives', 'priorities'."
argument-hint: "[goal topic]"
agent: shipkit-product-owner-agent
---

# shipkit-goals - Project Goals & Objectives

**Purpose**: Capture structured, trackable project goals that bridge `.shipkit/why.json` vision to concrete specs — with priorities, status, and success criteria.

**What it does**: Asks the user to define objectives, priorities, and success criteria. Generates `.shipkit/goals.json` with structured goals that persist across sessions and feed into mission control.

**Output format**: JSON — readable by Claude, renderable by mission control dashboard, and the single source of truth for project goals.

---

## When to Invoke

**User triggers**:
- "Set goals for this project"
- "What are our objectives?"
- "Define priorities"
- "What should we build toward?"
- "Goals for the MVP"

**Workflow position**:
- After `/shipkit-why-project` (vision exists) — goals make the vision actionable
- Before `/shipkit-spec` — goals inform which features to spec first

---

## Prerequisites

**Optional**:
- `.shipkit/why.json` (provides vision context — goals are more grounded with it)
- `.shipkit/stack.json` (helps frame technically feasible goals)

**If missing**: Skill still works — will ask user to describe vision inline instead.

---

## Process

### Step 0: Check for Existing File

```markdown
1. Check if `.shipkit/goals.json` exists

2. If exists AND modified < 5 minutes ago:
   - Show user: "Found recent goals (modified X ago)"
   - Ask: "Use these or regenerate?"
   - If "use these" → Exit early (save tokens)
   - If "regenerate" → Proceed to Step 1

3. If exists AND modified > 5 minutes ago:
   - Read and display current goals as a formatted summary
   - Ask: "View/Update/Replace/Cancel?"

4. If doesn't exist:
   - Skip to Step 1 (generate new)
```

**If Update:**
- Read existing goals.json
- Ask: "What should change? (new goals, reprioritize, mark achieved, etc.)"
- Regenerate incorporating updates

**If Replace:**
- Archive current: copy to `.shipkit/.archive/goals.YYYY-MM-DD.json`
- Proceed to Step 1

---

### Step 1: Gather Context

**Read these files if they exist** (skip missing ones silently):

```bash
# Vision context
.shipkit/why.json

# Technical context
.shipkit/stack.json

# Existing specs (to understand what's already planned)
.shipkit/specs/active/
```

**If why.json doesn't exist**: Ask user to briefly describe what the project is for (2-3 sentences).

---

### Step 2: Explore Current Codebase State

**Before asking about goals, understand what exists.**

Goals written without knowing what's already built miss partial implementations, existing momentum, and real constraints. This step grounds goal-setting in the project's actual state.

**Launch explore agents** — Use the Task tool with `subagent_type: Explore`:

```
Agent 1 - Project maturity: "Survey the codebase to understand current
project maturity. Look for: which features are implemented vs stubbed,
what areas have tests vs none, what's production-ready vs prototype.
Report: a brief summary of what exists, what's partial, and what's missing."

Agent 2 - Patterns and debt: "Scan the codebase for technical patterns,
TODO/FIXME/HACK comments, and areas of technical debt. Look for: recurring
patterns that indicate architectural direction, areas marked for improvement,
and partially implemented features. Report: key patterns in use, notable
debt areas, and any in-progress work."
```

**Launch both agents in parallel** — they are independent scans.

**Synthesize into goal context** — Before asking the user about goals, note:
- Features already built (don't set goals for completed work)
- Partial implementations that need finishing (natural goal candidates)
- Technical debt that might block other goals
- Existing momentum (what direction is the code already heading?)

**If exploration reveals important findings**: Share with user during questioning. Example: *"I can see authentication is partially implemented and there are several TODO markers around payments — should these be explicit goals?"*

**Token budget**: Each explore agent should return a focused summary (~500 tokens).

**When to skip**: If the project is brand new (no source files beyond scaffolding), skip exploration and proceed directly to questions.

---

### Step 3: Ask Clarifying Questions

**Ask user 2-3 questions based on context:**

1. **What are the main objectives?**
   - "What are the 3-5 most important things this project needs to achieve?"
   - Listen for both strategic goals (market fit, revenue) and tactical goals (launch feature X, migrate to Y)

2. **What's the priority order?**
   - "If you could only accomplish ONE of these, which matters most?"
   - Helps establish P0/P1/P2 ranking

3. **What does success look like?** (if not obvious from answers)
   - "For each goal, how would you know it's achieved?"
   - Captures measurable success criteria

**Why ask first**: Goals must reflect human priorities — Claude can't decide what matters to the user.

---

### Step 4: Generate Goals JSON

**Create file using Write tool**: `.shipkit/goals.json`

The output MUST conform to the schema below. This is a strict contract — mission control and other skills depend on this structure.

---

## JSON Schema

**Full schema reference**: See `references/output-schema.md`
**Example output**: See `references/example.json`

### Quick Reference

```json
{
  "$schema": "shipkit-artifact",
  "type": "goals",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DD",
  "source": "shipkit-goals",
  "summary": { "total": N, "byPriority": {...}, "byStatus": {...} },
  "goals": [
    {
      "id": "goal-slug",
      "name": "Goal Name",
      "priority": "p0|p1|p2",
      "status": "not-started|in-progress|achieved|deferred",
      "objective": "What we're trying to achieve",
      "successCriteria": ["Criterion 1", "Criterion 2"],
      "linkedSpecs": ["specs/active/feature.json"],
      "notes": "Optional"
    }
  ]
}
```

**Key fields**: `id` (kebab-case slug), `priority` (p0/p1/p2), `status` (tracking), `successCriteria` (measurable).

**Summary**: Recompute `summary` counts every time the file is written.

---

### Step 5: Save and Suggest Next Step

**Use Write tool to create/overwrite**: `.shipkit/goals.json`

**Output to user** (formatted summary, not raw JSON):
```
Goals saved.

Location: .shipkit/goals.json

  P0 (must have): 2 goals
  P1 (should have): 2 goals
  P2 (nice to have): 1 goal

  Status: 2 not started, 2 in progress, 1 achieved

Next steps:
  1. /shipkit-spec - Create specs for your P0 goals
  2. /shipkit-plan - Plan implementation for an existing spec
  3. /shipkit-project-status - See overall project health

Ready to spec your top-priority goal?
```

---

---

## When This Skill Integrates with Others

### Before shipkit-goals
- `/shipkit-why-project` - Define vision first (optional but recommended)
- `/shipkit-project-context` - Know your stack (optional)

### After shipkit-goals
- `/shipkit-spec` - Create specs for P0 goals
- `/shipkit-plan` - Plan implementation for specs
- `/shipkit-project-status` - See how goals map to project health

### When shipkit-goals Runs Again
- File exists workflow activates
- User can view/update/replace existing goals
- Common update: mark goals as achieved, reprioritize, add new goals

---

## Context Files This Skill Reads

**Optional** (read if exist):
- `.shipkit/why.json` - Project vision context
- `.shipkit/stack.json` - Technical context
- `.shipkit/specs/active/*.json` - Existing specs to link

**If missing**: Asks user for inline context instead.

---

## Context Files This Skill Writes

**Write Strategy: OVERWRITE**

**Creates/Updates**:
- `.shipkit/goals.json` - Structured project goals (JSON artifact)

**Update Behavior**:
- File exists → File Exists Workflow (view/update/replace/cancel)
- Recent file (< 5 min) → Quick Exit Check (use or regenerate)
- Replace → Archive old version first
- Update → Read existing, incorporate changes
- Each write REPLACES entire file contents

**Archive location** (if replacing):
- `.shipkit/.archive/goals.YYYY-MM-DD.json`

---

## Success Criteria

- [ ] Codebase explored for current state, partial implementations, and debt
- [ ] Goals are structured with priority levels (P0/P1/P2)
- [ ] Each goal has measurable success criteria
- [ ] Goals connect to why.json vision
- [ ] Goals reflect actual codebase state (not duplicating completed work)
- [ ] Status tracking enables cross-session updates
- [ ] Output conforms to JSON schema above
- [ ] Summary field is accurate
- [ ] File saved to `.shipkit/goals.json`
- [ ] Old version archived (if replaced)

---

## Common Scenarios

### Scenario 1: New Project (First Time)

```
User: "Set goals for this project"

Claude:
1. Check .shipkit/goals.json (doesn't exist)
2. Read .shipkit/why.json for vision context
3. Ask: "What are the 3-5 most important objectives?"
   User: "Launch MVP, get 10 beta users, integrate payments"
4. Ask: "Which matters most if you could only do one?"
   User: "Launch MVP"
5. Ask: "How will you know the MVP is ready?"
   User: "Core flow works end-to-end, deployed to production"
6. Generate goals.json with priorities and criteria
7. Save to .shipkit/goals.json
8. Show formatted summary to user
```

### Scenario 2: Update Goals (File Exists)

```
User: "Update our goals"

Claude:
1. Check .shipkit/goals.json (exists, modified 2 days ago)
2. Read and display formatted summary
3. Ask: "View/Update/Replace/Cancel?"
   User: "Update"
4. Ask: "What should change?"
   User: "We achieved the MVP goal, and I want to add onboarding"
5. Read existing JSON, move MVP status to "achieved", add onboarding goal
6. Recompute summary counts
7. Overwrite .shipkit/goals.json
```

### Scenario 3: Quick Exit (Recent File)

```
User: "Show me our goals"

Claude:
1. Check .shipkit/goals.json (exists, modified 2 minutes ago)
2. Show: "Found recent goals (2 min ago). Use these or regenerate?"
   User: "Use these"
3. Read JSON, display formatted summary, exit
```

---

<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Has important context been saved to `.shipkit/`?
2. **Prerequisites** - Does the next action need a spec or plan first?
3. **Session length** - Long session? Consider `/shipkit-work-memory` for continuity.

**Natural capabilities** (no skill needed): Implementation, debugging, testing, refactoring, code documentation.

**Suggest skill when:** User needs to make decisions, create persistence, or check project status.
<!-- /SECTION:after-completion -->

---

**Remember**: Goals bridge vision to execution. They capture human priorities that Claude can't infer. Update them as the project evolves.
