---
name: shipkit-why-project
description: "Use when defining project vision and strategic direction. Triggers: 'why this project', 'define vision', 'project goals', 'what are we building'."
argument-hint: "[project name]"
agent: shipkit-visionary-agent
effort: medium
---

# shipkit-why-project - Project Vision & Strategy

**Purpose**: Create a strategic overview that answers: Who is this for? What problem does it solve? Where are we? Where are we going? How are we getting there? What are we NOT building?

**What it does**: Collects core vision inputs, generates `.shipkit/why.json`, provides strategic context for all future sessions.

**Protocol:** This skill follows the canonical elicitation protocol defined in `install/shared/references/elicitation-protocol.md`. The steps below are this skill's specific application of that protocol.

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

### Step 0: Context Shortcut

Before checking elicitation state, attempt a context-based shortcut:

1. Read available context: `README.md`, `package.json` (name, description, keywords), existing source files, any `.shipkit/*.json` files.
2. **If sufficient context exists** (README or package.json with description, or >5 source files):
   - Generate a complete `why.json` proposal based on what you found.
   - **IMPORTANT: Keep it vision-level.** The why.json captures the enduring vision and customer problem — NOT stage-specific details like target markets, curriculum scope, timeline constraints, or POC boundaries. Those belong in `stage.json` (via `/shipkit-stage`).
   - Write `.shipkit/why.json` directly and skip to Step 6 (confirm to user).
   - Present a summary of what was written so the user can review.
3. **If insufficient context** (empty project, no README, no package.json): Fall through to Step 1.

---

### Step 1: Check if why.json Already Exists

1. Read `.shipkit/why.json` if it exists.
2. If it exists: read `.shipkit/reviews/direction-assessment.json` if present. If the latest review lists a gap against this artifact, archive the existing file to `.shipkit/.archive/why.YYYY-MM-DD.json` and regenerate addressing the gap. Otherwise, exit early with a "no changes needed" report — the reviewer already accepted it.
3. If no file exists: proceed to Step 2.

---

### Step 2: Check Elicitation State

Read `.shipkit/elicitation/why-project/answers.md`.

**Classify each `A:` line as real or placeholder:**
- Placeholder markers: `[awaiting answer]`, empty string, literal `A:` with nothing after.
- Real answer: any other non-empty content.

Then:

- **All 5 core fields have real answers** (Q1–Q5 → `targetUsers`, `problem`, `currentState`, `vision`, `approach`): synthesize `.shipkit/why.json` from those answers per the schema in Step 5. Update `progress.json` with `status: complete`, set `completed_at` and `last_elicited_at` to current ISO 8601 UTC timestamp. Skip to Step 6. Do NOT overwrite `answers.md` — the user's input is preserved as-is.
- **Some core fields have real answers, others are placeholders**: determine which questions still need answers. Proceed to Step 3 for those, but do NOT clobber `answers.md` — append a new turn header to the existing file for the unanswered questions only.
- **File absent, empty, or all placeholders**: proceed to Step 3 at turn 1. Safe to (over)write `answers.md` in Step 4 since no real content exists.

---

### Step 3: Generate Questions

Produce questions for the current turn. Two-turn split (recommended):

**Turn 1** — core foundation (Q1–Q3):
1. "Who is this project for?" (target users, audience, stakeholders) → `targetUsers`
2. "What problem does this solve? Why does it exist?" → `problem`
3. "Where are we now?" (current state: POC / MVP / Beta / Production / Starting) → `currentState`

**Turn 2** — direction + optional (Q4–Q5 + optional):
4. "What does success look like? What's the vision?" → `vision`
5. "What's the approach? How are we getting there?" → `approach`
6. *(Optional)* "What are the measurable success criteria? (or skip)" → `successCriteria`
7. *(Optional)* "Any enduring constraints? (e.g., must run on mobile, no paid APIs — or skip)" → `constraints`
8. *(Optional)* "What are we explicitly NOT building? (or skip)" → `nonGoals`

> **Note on constraints**: Capture only enduring project-level constraints here. Stage-specific constraints like "AU curriculum only for POC" belong in `stage.json`.

For optional fields (Q6–Q8): if the user skips, set the corresponding field to an empty array `[]`.

One-turn mode is also acceptable for pilot: ask all 8 questions in a single turn if context suggests the user prefers a direct Q&A session.

---

### Step 4: Write State Files

Write the following files. All timestamps ISO 8601 UTC.

**`.shipkit/elicitation/why-project/questions.md`** — overwrite with current turn's questions using the schema from `install/shared/references/elicitation-protocol.md`:
```
---
skill: shipkit-why-project
turn: <n>
last_updated: <ISO 8601 UTC>
---

## Turn <n>

1. Question text (field: `targetUsers`)
2. ...
```

**`.shipkit/elicitation/why-project/answers.md`** — **DO NOT write this file from the fork.** The main session creates and maintains this file when it collects answers via AskUserQuestion. Writing placeholders here from the fork clobbers any real user answers (pre-populated or from prior turns). The fork's job is to emit the marker and signal which questions need answering — `questions.md` carries that information.

If you want to leave a clear breadcrumb, you may create an empty `answers.md` with only the frontmatter header **only if the file does not already exist**. Never overwrite an existing `answers.md`.

**`.shipkit/elicitation/why-project/progress.json`** — create or update:
```json
{
  "skill": "shipkit-why-project",
  "status": "in_progress",
  "elicitation_turn": <n>,
  "started_at": "<ISO 8601 UTC>",
  "last_updated_at": "<ISO 8601 UTC>",
  "completed_at": null,
  "last_elicited_at": "<ISO 8601 UTC>",
  "total_questions_planned": 5,
  "questions_answered": <count from prior turns>,
  "confidence": "medium"
}
```

---

### Step 5: Emit Marker and Return

Emit the following as the **final line** of your output:

```
NEEDS_ELICITATION:shipkit-why-project
status=paused
turn=<n>
questions_file=.shipkit/elicitation/why-project/questions.md
reason=awaiting user answers for turn <n>
```

Do **not** synthesize `why.json`. Do **not** invent answers. Return immediately after emitting the marker.

---

### Step 5 (synthesis): Generate why.json

*Only reached when real answers are available — from the context shortcut (Step 0), a pre-populated answers.md (Step 2), or completed elicitation.*

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
  "vision": "{answer to Q4}",
  "problem": "{answer to Q2}",
  "targetUsers": "{answer to Q1}",
  "currentState": "{answer to Q3}",
  "successCriteria": ["{parsed from Q6, or []}"],
  "constraints": ["{parsed from Q7, or []}"],
  "nonGoals": ["{parsed from Q8, or []}"],
  "approach": "{answer to Q5}"
}
```

Update `progress.json`: set `status: complete`, `completed_at` and `last_elicited_at` to current ISO 8601 UTC timestamp.

---

### Step 6: Confirm to User

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

Elicitation state (persists as audit trail):
- `.shipkit/elicitation/why-project/questions.md`
- `.shipkit/elicitation/why-project/answers.md`
- `.shipkit/elicitation/why-project/progress.json`

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
- [ ] Elicitation state written to `.shipkit/elicitation/why-project/`
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

**If `NEEDS_ELICITATION:shipkit-why-project` was emitted:** The skill paused without writing `why.json`. The main session should run `/shipkit-why-project` inline (where `AskUserQuestion` is available), answer the questions in `.shipkit/elicitation/why-project/questions.md`, then re-invoke the original skill or orchestrator to resume. See `install/shared/references/elicitation-protocol.md` for full handling instructions.

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
- [ ] If elicitation ran: state files present in `.shipkit/elicitation/why-project/` with ISO 8601 UTC timestamps
- [ ] If marker emitted: `NEEDS_ELICITATION:shipkit-why-project` is the final output line; why.json was NOT written
<!-- /SECTION:success-criteria -->
---

**Remember**: This is strategic context, not requirements. Keep it high-level. Answer "why" not "how". Think vision, not spec.

**Schema reference**: See `references/output-schema.md` for complete JSON schema.
**Example**: See `references/example.json` for a sample output.
