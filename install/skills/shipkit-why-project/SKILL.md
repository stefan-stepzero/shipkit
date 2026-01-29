---
name: shipkit-why-project
description: "Use when defining project vision and strategic direction. Triggers: 'why this project', 'define vision', 'project goals', 'what are we building'."
---

# shipkit-why-project - Project Vision & Strategy

**Purpose**: Create a one-page strategic overview that answers: Who is this for? Why does it exist? Where are we? Where are we going? How are we getting there?

**What it does**: Asks 5 core questions, generates `.shipkit/why.md`, provides strategic context for all future sessions.

---

## When to Invoke

**User triggers**:
- "Define the project vision"
- "Why are we building this?"
- "What's this project about?"
- "Create project overview"

**Auto-suggested**: Session start if `why.md` doesn't exist (via shipkit-session-start.py)

---

## Prerequisites

**None** - This can be the first skill you run (even before shipkit-project-context)

**Recommended order:**
1. `/shipkit-why-project` - Define strategic vision
2. `/shipkit-project-context` - Scan technical stack
3. Start building

---

## Process

### Step 1: Check if why.md Already Exists

```
If .shipkit/why.md exists:
  → Ask user: "A project vision already exists. Would you like to:"
     1. View current vision
     2. Update vision (will overwrite)
     3. Cancel

If .shipkit/why.md does NOT exist:
  → Proceed directly to Step 2
```

---

### Step 2: Ask the 5 Core Questions

**Ask questions ONE AT A TIME** - Wait for user answer before asking next.

#### Question 1: Who Is This For?
**Ask**: "Who is this project for?" (target users, audience, stakeholders)
**Capture**: 1-3 sentences max

#### Question 2: Why Does This Exist?
**Ask**: "Why does this project exist?" (problem solving, value provided)
**Capture**: 1-3 sentences max

#### Question 3: Where Are We Now?
**Ask**: "Where are we now?" (current state: POC/MVP/Beta/Production/Starting)
**Capture**: 1-2 sentences max

#### Question 4: Where Do We Need To Be?
**Ask**: "Where do we need to be?" (vision, success state, what "done" looks like)
**Capture**: 1-3 sentences max

#### Question 5: How Are We Getting There?
**Ask**: "How are we getting there?" (approach, methodology, constraints, priorities)
**Capture**: 1-3 sentences max

---

### Step 3: Ask About Constraints & Priorities (Optional)

**Ask**: "Do you have specific constraints or priorities to note? (or press Enter to skip)"

**If user provides content**: Include in why.md
**If user skips**: Omit this section

---

### Step 4: Generate why.md

**Location**: `.shipkit/why.md`

**Template:**

```markdown
# Why This Project

**Created**: {First creation date - preserve if updating}
**Last Updated**: {Current date}

---

## Who Is This For?

{Answer to Question 1}

---

## Why Does This Exist?

{Answer to Question 2}

---

## Where Are We Now?

{Answer to Question 3}

---

## Where Do We Need To Be?

{Answer to Question 4}

---

## How Are We Getting There?

{Answer to Question 5}

{IF CONSTRAINTS/PRIORITIES PROVIDED:}
---

## Constraints & Priorities

{User-provided constraints/priorities}
{END IF}
```

---

### Step 5: Confirm to User

**Output**: Summary of who/why/current state, location of file, note about auto-loading at session start.

---

## Workspace Structure

Creates `.shipkit/why.md` (auto-loaded by shipkit-session-start.py)

---

## Completion Checklist

Copy and track:
- [ ] Defined who the project serves
- [ ] Clarified why it matters
- [ ] Identified where it's going
- [ ] Saved to `.shipkit/why.md`

---

## What Makes This "Lite"

**Lite approach**: 5 questions, 1 file, 2-5 minutes. Auto-loads at session start (~150 tokens).

**Full ShipKit approach**: 10 skills, 10+ files, 2-4 hours (personas, JTBD, market analysis, etc.).

**Philosophy**: Answer "why" in 5 minutes, not 5 hours. Enough strategic context without full product discovery.

---

## When This Skill Integrates with Others

### Before This Skill
- None (can be first skill)

### After This Skill
- `/shipkit-project-context` - Scan technical stack
- `/shipkit-architecture-memory` - Log architectural decisions
- `/shipkit-spec` - Create feature specs (can reference vision for alignment)
- Any other skill - Strategic context available via auto-load

---

## Context Files This Skill Reads

**On update (if why.md exists)**: `.shipkit/why.md` - Read old answers as defaults

**Never reads other files** - This is the starting point

---

## Context Files This Skill Writes

**Creates/Updates**: `.shipkit/why.md` - OVERWRITE AND REPLACE

**Write Strategy**: OVERWRITE AND REPLACE
- Entire file regenerated when vision changes
- Represents current state, not history
- Created date preserved from original when updating

---

## Session Start Behavior

**shipkit-session-start.py auto-loads why.md** (~150 tokens)

**Result**: Claude starts every session knowing who/why/where/how, enabling better aligned suggestions.

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

<!-- SECTION:success-criteria -->
## Success Criteria

Vision is defined when:
- [ ] User answered all 5 core questions
- [ ] Answers are high-level (1-3 sentences each)
- [ ] why.md created in `.shipkit/`
- [ ] File follows template structure
- [ ] Dates are correct (Created preserved if updating)
- [ ] User knows vision will auto-load at session start
<!-- /SECTION:success-criteria -->
---

**Remember**: This is strategic context, not requirements. Keep it high-level. Answer "why" not "how". Think vision, not spec.

**Detailed guidance**: See `references/` folder for common scenarios, tips, and examples.
