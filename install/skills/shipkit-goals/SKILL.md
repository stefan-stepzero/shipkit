---
name: shipkit-goals
description: "Capture structured project goals that bridge why.md vision to concrete specs. Triggers: 'set goals', 'project goals', 'objectives', 'priorities'."
argument-hint: "[goal topic]"
agent: shipkit-product-owner-agent
---

# shipkit-goals - Project Goals & Objectives

**Purpose**: Capture structured, trackable project goals that bridge `.shipkit/why.md` vision to concrete specs — with priorities, status, and success criteria.

**What it does**: Asks the user to define objectives, priorities, and success criteria. Generates `.shipkit/goals.md` with structured goals that persist across sessions.

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
- `.shipkit/why.md` (provides vision context — goals are more grounded with it)
- `.shipkit/stack.md` (helps frame technically feasible goals)

**If missing**: Skill still works — will ask user to describe vision inline instead.

---

## Process

### Step 0: Check for Existing File (Quick Exit + File Exists Workflow)

**Quick Exit Check**:

```markdown
1. Check if `.shipkit/goals.md` exists

2. If exists AND modified < 5 minutes ago:
   - Show user: "Found recent goals (modified X ago)"
   - Ask: "Use these or regenerate?"
   - If "use these" → Exit early (save tokens)
   - If "regenerate" → Proceed to Step 1

3. If exists AND modified > 5 minutes ago:
   - Proceed to File Exists Workflow (Step 0b)

4. If doesn't exist:
   - Skip to Step 1 (generate new)
```

**File Exists Workflow**:

```markdown
### Step 0b: File Already Exists

File exists: `.shipkit/goals.md`

**Options:**

1. **View** - Show current goals, then ask what to do
2. **Update** - Read existing, ask what to change, regenerate
3. **Replace** - Archive old version, generate completely new
4. **Cancel** - Exit without changes

**If View:**
- Display current goals
- Ask: "Keep these, update, or replace?"

**If Update:**
- Read existing goals
- Ask: "What should change? (new goals, reprioritize, mark achieved, etc.)"
- Regenerate incorporating updates
- Use Write tool to overwrite

**If Replace:**
- Archive current version
- Proceed to Step 1 (generate new)

**If Cancel:**
- Exit, no changes made
```

---

### Step 1: Gather Context

**Read these files if they exist** (skip missing ones silently):

```bash
# Vision context
.shipkit/why.md

# Technical context
.shipkit/stack.md

# Existing specs (to understand what's already planned)
.shipkit/specs/active/
```

**If why.md doesn't exist**: Ask user to briefly describe what the project is for (2-3 sentences).

---

### Step 2: Ask Clarifying Questions

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

### Step 3: Generate Goals Document

**Create file using Write tool**: `.shipkit/goals.md`

---

## Goals Template Structure

**The goals document MUST follow this template**:

```markdown
# Project Goals

**Last Updated**: [YYYY-MM-DD]
**Source**: .shipkit/why.md vision

---

## Active Goals

### P0 - Must Have (blocks everything else)

#### [Goal Name]
- **Objective**: [What we're trying to achieve]
- **Success Criteria**: [How we know it's done]
- **Status**: [not-started | in-progress | achieved | deferred]
- **Linked Specs**: [specs/active/feature-x.md, or "none yet"]

### P1 - Should Have (important but not blocking)

#### [Goal Name]
- **Objective**: [What we're trying to achieve]
- **Success Criteria**: [How we know it's done]
- **Status**: [not-started | in-progress | achieved | deferred]
- **Linked Specs**: [specs/active/feature-y.md, or "none yet"]

### P2 - Nice to Have (if time permits)

#### [Goal Name]
- **Objective**: [What we're trying to achieve]
- **Success Criteria**: [How we know it's done]
- **Status**: [not-started | in-progress | achieved | deferred]
- **Linked Specs**: [none yet]

---

## Achieved Goals

*(Move goals here when success criteria are met)*

---

## Deferred Goals

*(Move goals here when consciously deprioritized — include reason)*

---

## Quality Checklist

**Validate goals meet standards:**

### Clarity
- [ ] Each goal has a clear, specific objective
- [ ] Success criteria are measurable or observable
- [ ] No vague goals ("make it better", "improve performance")

### Alignment
- [ ] Goals connect to why.md vision
- [ ] Priority order reflects user's stated priorities
- [ ] No contradicting goals

### Actionability
- [ ] Each goal can be broken into specs
- [ ] Status tracking enables session-to-session continuity
- [ ] Linked specs show progress toward goals
```

---

### Step 4: Archive Old Version (If Replacing)

```markdown
**If user chose "Replace" in Step 0:**

1. Create archive directory: `.shipkit/.archive/`

2. Copy existing file with timestamp:
   cp .shipkit/goals.md .shipkit/.archive/goals.YYYY-MM-DD.md

3. Write new file (overwrites current)
```

---

### Step 5: Save and Suggest Next Step

**Use Write tool to create/overwrite**: `.shipkit/goals.md`

**Output to user**:
```
Goals document created.

Location: .shipkit/goals.md

Summary:
  - X goals defined (P0: N, P1: N, P2: N)
  - Success criteria captured for each
  - Linked to existing specs where applicable

Next steps:
  1. /shipkit-spec - Create specs for your P0 goals
  2. /shipkit-plan - Plan implementation for an existing spec
  3. /shipkit-project-status - See overall project health

Ready to spec your top-priority goal?
```

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
- `.shipkit/why.md` - Project vision context
- `.shipkit/stack.md` - Technical context
- `.shipkit/specs/active/*.md` - Existing specs to link

**If missing**: Asks user for inline context instead.

---

## Context Files This Skill Writes

**Write Strategy: OVERWRITE**

**Creates/Updates**:
- `.shipkit/goals.md` - Structured project goals with priorities and status

**Update Behavior**:
- File exists → File Exists Workflow (view/update/replace/cancel)
- Recent file (< 5 min) → Quick Exit Check (use or regenerate)
- Replace → Archive old version first
- Update → Read existing, incorporate changes
- Each write REPLACES entire file contents

**Archive location** (if replacing):
- `.shipkit/.archive/goals.YYYY-MM-DD.md`

**Why OVERWRITE:**
- Goals are a single coherent document (not entries)
- Priority order matters — can't just append
- Whole-file updates ensure consistency

---

## Success Criteria

- [ ] Goals are structured with priority levels (P0/P1/P2)
- [ ] Each goal has measurable success criteria
- [ ] Goals connect to why.md vision
- [ ] Status tracking enables cross-session updates
- [ ] Quality checklist embedded
- [ ] File saved to `.shipkit/goals.md`
- [ ] Old version archived (if replaced)

---

## Common Scenarios

### Scenario 1: New Project (First Time)

```
User: "Set goals for this project"

Claude:
1. Check .shipkit/goals.md (doesn't exist)
2. Read .shipkit/why.md for vision context
3. Ask: "What are the 3-5 most important objectives?"
   User: "Launch MVP, get 10 beta users, integrate payments"
4. Ask: "Which matters most if you could only do one?"
   User: "Launch MVP"
5. Ask: "How will you know the MVP is ready?"
   User: "Core flow works end-to-end, deployed to production"
6. Generate goals.md with priorities and criteria
7. Save to .shipkit/goals.md
```

### Scenario 2: Update Goals (File Exists)

```
User: "Update our goals"

Claude:
1. Check .shipkit/goals.md (exists, modified 2 days ago)
2. Show: "Goals exist. Options: View/Update/Replace/Cancel"
   User: "Update"
3. Read existing goals
4. Ask: "What should change?"
   User: "We achieved the MVP goal, and I want to add onboarding"
5. Move MVP to Achieved, add onboarding goal
6. Overwrite .shipkit/goals.md
```

### Scenario 3: Quick Exit (Recent File)

```
User: "Show me our goals"

Claude:
1. Check .shipkit/goals.md (exists, modified 2 minutes ago)
2. Show: "Found recent goals (2 min ago). Use these or regenerate?"
   User: "Use these"
3. Display current goals, exit
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
