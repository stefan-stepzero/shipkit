---
name: shipkit-why-project
description: "Use when defining project vision and strategic direction. Triggers: 'why this project', 'define vision', 'project goals', 'what are we building'."
argument-hint: "[project name]"
context: fork
agent: shipkit-visionary-agent
effort: medium
---

# shipkit-why-project - Project Vision & Strategy

**Purpose**: Create a strategic overview that answers: Who is this for? What problem does it solve? Where are we? Where are we going? How are we getting there? What are we NOT building?

**What it does**: Asks core questions, generates `.shipkit/why.json`, provides strategic context for all future sessions.

---

## When to Invoke

**User triggers**:
- "Define the project vision"
- "Why are we building this?"
- "What's this project about?"
- "Create project overview"

**Auto-suggested**: Session start if `why.json` doesn't exist (via shipkit-session-start.py)

---

## Prerequisites

**None** - This can be the first skill you run (even before shipkit-project-context)

**Recommended order:**
1. `/shipkit-why-project` - Define strategic vision
2. `/shipkit-stage` - Set project stage, constraints, and business metrics
3. `/shipkit-product-discovery` - Define personas & user needs
4. `/shipkit-product-definition` - Design solution blueprint
5. `/shipkit-product-goals` - Define user-outcome success criteria (P-*)

---

## Process

### Step 0: Context Check + Propose Mode

Before asking questions, check if the project already has enough context to propose a vision:

1. Read available context: `README.md`, `package.json` (name, description, keywords), existing source files, any `.shipkit/*.json` files
2. **If sufficient context exists** (README or package.json with description, or >5 source files):
   - Generate a complete `why.json` proposal based on what you found
   - **IMPORTANT: Keep it vision-level.** The why.json captures the enduring vision and customer problem — NOT stage-specific details like target markets, curriculum scope, timeline constraints, or POC boundaries. Those belong in `stage.json` (via `/shipkit-stage`).
   - Present the proposal as a formatted summary:
     ```
     Based on your project files, here's a proposed vision:

     Who: [broad target audience — not narrowed by current stage]
     Problem: [the full problem worth solving]
     Current State: [brief maturity assessment]
     Vision: [the big picture — what success looks like at scale]
     Approach: [high-level methodology, not stage-specific tactics]

     ```
   - Write `why.json` directly and skip to Step 7 (suggest next steps)
   - Present a summary of what was written so the user can review
3. **If insufficient context** (empty project, no README, no package.json): Fall through to Step 1

---

### Step 1: Check if why.json Already Exists

> **Fork context — no user prompts.** You are dispatched in a fork and have no user channel. Skip the file-exists menu entirely.

1. Check if `.shipkit/why.json` exists
2. If exists: read `.shipkit/reviews/direction-assessment.json` if present. If the latest review lists a gap against this artifact, archive the existing file to `.shipkit/.archive/why.YYYY-MM-DD.json` and regenerate addressing the gap. Otherwise, read the existing file and exit early with a "no changes needed" report — the reviewer already accepted it.
3. If no file exists: proceed to Step 2.

---

### Step 2: Ask Core Questions

**Ask questions ONE AT A TIME** - Wait for user answer before asking next.

#### Question 1: Who Is This For?
**Ask**: "Who is this project for?" (target users, audience, stakeholders)
**Capture as**: `targetUsers` - 1-3 sentences max

#### Question 2: What Problem Are We Solving?
**Ask**: "What problem does this solve? Why does it exist?"
**Capture as**: `problem` - 1-3 sentences max

#### Question 3: Where Are We Now?
**Ask**: "Where are we now?" (current state: POC/MVP/Beta/Production/Starting)
**Capture as**: `currentState` - 1-2 sentences max

#### Question 4: Where Do We Need To Be?
**Ask**: "What does success look like? What's the vision?"
**Capture as**: `vision` - 1-3 sentences max

#### Question 5: How Are We Getting There?
**Ask**: "What's the approach? How are we getting there?"
**Capture as**: `approach` - 1-3 sentences max

---

### Step 3: Ask About Success Criteria (Optional)

**Ask**: "What are the measurable success criteria? (or press Enter to skip)"

**If user provides content**: Parse into array for `successCriteria`
**If user skips**: Set `successCriteria` to empty array `[]`

---

### Step 4: Ask About Constraints (Optional)

**Ask**: "Any constraints or must-haves? (budget, timeline, tech requirements - or Enter to skip)"

**Note**: Capture only enduring project-level constraints here (e.g., "must run on mobile", "no paid APIs"). Stage-specific constraints like "AU curriculum only for POC" or "Year 1-2 only" belong in `stage.json`.

**If user provides content**: Parse into array for `constraints`
**If user skips**: Set `constraints` to empty array `[]`

---

### Step 5: Ask About Non-Goals (Optional)

**Ask**: "What are we explicitly NOT building? (helps prevent scope creep - or Enter to skip)"

**If user provides content**: Parse into array for `nonGoals`
**If user skips**: Set `nonGoals` to empty array `[]`

---

### Step 6: Generate why.json

**Location**: `.shipkit/why.json`

**Output format**: See `references/output-schema.md` for complete schema.

**Key fields**:
```json
{
  "$schema": "shipkit-artifact",
  "type": "project-why",
  "version": "1.0",
  "lastUpdated": "{Current date YYYY-MM-DD}",
  "createdAt": "{First creation date - preserve if updating}",
  "source": "shipkit-why-project",
  "vision": "{Answer to Question 4}",
  "problem": "{Answer to Question 2}",
  "targetUsers": "{Answer to Question 1}",
  "currentState": "{Answer to Question 3}",
  "successCriteria": ["{parsed from Step 3}"],
  "constraints": ["{parsed from Step 4}"],
  "nonGoals": ["{parsed from Step 5}"],
  "approach": "{Answer to Question 5}"
}
```

---

### Step 7: Confirm to User

**Output**:
- Summary of vision, problem, target users
- Location of file (`.shipkit/why.json`)
- Note about auto-loading at session start
- Counts of success criteria, constraints, non-goals captured
- Suggest `/shipkit-stage` to set project stage and business metrics
- Suggest `/shipkit-product-discovery` to define user needs and personas

---

## Workspace Structure

Creates `.shipkit/why.json` (auto-loaded by shipkit-session-start.py)

---

## Completion Checklist

Copy and track:
- [ ] Defined who the project serves (`targetUsers`)
- [ ] Clarified what problem it solves (`problem`)
- [ ] Identified current state and vision
- [ ] Captured success criteria (or explicitly skipped)
- [ ] Captured constraints (or explicitly skipped)
- [ ] Captured non-goals (or explicitly skipped)
- [ ] Saved to `.shipkit/why.json`
- [ ] Suggested `/shipkit-stage` for project stage and business metrics
- [ ] Suggested `/shipkit-product-discovery` for user needs

---

## When This Skill Integrates with Others

### Before This Skill
- None (can be first skill)

### After This Skill
- `/shipkit-stage` - **Recommended next step** — Set project stage, constraints, and business metrics
- `/shipkit-product-discovery` - Define personas, user needs, and journeys
- `/shipkit-project-context` - Scan technical stack (can run in parallel with discovery)
- `/shipkit-engineering-definition` - Engineering blueprint and architecture decisions
- `/shipkit-spec` - Create feature specs (can reference vision for alignment)

---

## Context Files This Skill Reads

**On update (if why.json exists)**: `.shipkit/why.json` - Read old values as defaults

**Never reads other files** - This is the starting point

---

## Context Files This Skill Writes

**Artifact strategy: replace** — Overwrites the existing artifact file. Previous content is not preserved.

**Creates/Updates**: `.shipkit/why.json` - OVERWRITE AND REPLACE

**Write Strategy**: OVERWRITE AND REPLACE
- Entire file regenerated when vision changes
- Represents current state, not history
- `createdAt` date preserved from original when updating

---

## Session Start Behavior

**shipkit-session-start.py auto-loads why.json** (~200 tokens)

**Result**: Claude starts every session knowing who/why/where/how, enabling better aligned suggestions.

---

<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Has important context been saved to `.shipkit/`?
2. **Prerequisites** - Does the next action need a spec or plan first?
3. **Session length** - Long session? Consider `/shipkit-work-memory` for continuity.

**Natural capabilities** (no skill needed): Implementation, debugging, testing, refactoring, code documentation.

**Suggest skill when:** User needs to set project stage (`/shipkit-stage`), define user needs (`/shipkit-product-discovery`), or check project status.
<!-- /SECTION:after-completion -->

<!-- SECTION:success-criteria -->
## Success Criteria

Vision is defined when:
- [ ] All 5 core vision fields populated (targetUsers, problem, currentState, vision, approach)
- [ ] Answers are high-level (1-3 sentences each)
- [ ] why.json created in `.shipkit/`
- [ ] File follows Shipkit artifact envelope schema
- [ ] Dates are correct (`createdAt` preserved if updating)
- [ ] Session-start auto-load confirmed
<!-- /SECTION:success-criteria -->
---

**Remember**: This is strategic context, not requirements. Keep it high-level. Answer "why" not "how". Think vision, not spec.

**Schema reference**: See `references/output-schema.md` for complete JSON schema.
**Example**: See `references/example.json` for a sample output.
