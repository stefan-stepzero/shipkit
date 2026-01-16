---
name: lite-why-project
description: "Use when defining project vision and strategic direction. Triggers: 'why this project', 'define vision', 'project goals', 'what are we building'."
---

# lite-why-project - Project Vision & Strategy

**Purpose**: Create a one-page strategic overview that answers: Who is this for? Why does it exist? Where are we? Where are we going? How are we getting there?

**What it does**: Asks 5 core questions, generates `.shipkit-lite/why.md`, provides strategic context for all future sessions.

---

## When to Invoke

**User triggers**:
- "Define the project vision"
- "Why are we building this?"
- "What's this project about?"
- "Create project overview"
- "Set the strategic direction"

**Auto-suggested**:
- Session start if `why.md` doesn't exist (via lite-session-start.py)

**Use cases**:
- Starting a new project (first skill after lite-project-context)
- Onboarding team members (share why.md)
- Before major architectural decisions (check alignment with vision)
- When project direction shifts (update the vision)

---

## Prerequisites

**None** - This can be the first skill you run (even before lite-project-context)

**Recommended order:**
1. `/lite-why-project` - Define strategic vision
2. `/lite-project-context` - Scan technical stack
3. Start building

---

## Process

### Step 1: Check if why.md Already Exists

**Before starting, check:**

```
If .shipkit-lite/why.md exists:
  → Ask user: "A project vision already exists. Would you like to:"
     1. View current vision
     2. Update vision (will overwrite)
     3. Cancel

  If user chooses "View":
    → Read and display why.md
    → Done

  If user chooses "Update":
    → Read old why.md (for context)
    → Proceed to Step 2 (show old answers as defaults)

  If user chooses "Cancel":
    → Exit

If .shipkit-lite/why.md does NOT exist:
  → Proceed directly to Step 2
```

---

### Step 2: Ask the 5 Core Questions

**Ask questions ONE AT A TIME** - Wait for user answer before asking next.

**Tone**: Conversational, helpful, not interrogative.

---

#### Question 1: Who Is This For?

**Ask**: "Who is this project for?" (target users, audience, stakeholders)

**Examples**: Solo developers, small teams, enterprise customers, myself (learning)

**Capture**: 1-3 sentences max

**If updating**: Show current answer, ask if changed

---

#### Question 2: Why Does This Exist?

**Ask**: "Why does this project exist?" (problem solving, value provided)

**Examples**: Solve wasted time, fill tooling gap, automate process, learn by building

**Capture**: 1-3 sentences max

**If updating**: Show current answer, ask if changed

---

#### Question 3: Where Are We Now?

**Ask**: "Where are we now?" (current state: POC/MVP/Beta/Production/Starting)

**Examples**: Early POC, MVP with users, production adding features, just started

**Capture**: 1-2 sentences max

**If updating**: Show current answer, ask if changed

---

#### Question 4: Where Do We Need To Be?

**Ask**: "Where do we need to be?" (vision, success state, what "done" looks like)

**Examples**: Stable with users, revenue target, feature complete, personal tool used daily

**Capture**: 1-3 sentences max

**If updating**: Show current answer, ask if changed

---

#### Question 5: How Are We Getting There?

**Ask**: "How are we getting there?" (approach, methodology, constraints, priorities)

**Examples**: Ship fast & iterate, TDD weekly deploys, learn by doing, agile sprints

**Capture**: 1-3 sentences max

**If updating**: Show current answer, ask if changed

---

### Step 3: Ask About Constraints & Priorities (Optional)

**After the 5 core questions, ask:**

```
Optional: Do you have specific constraints or priorities to note?

Examples:
  • Constraints: "Solo developer, limited time (5hrs/week)", "Must use Python"
  • Priorities: "Speed over perfection", "UX is #1 priority"

Enter constraints/priorities (or press Enter to skip):
```

**If user provides content:**
- Capture it
- Include in why.md

**If user skips:**
- Omit this section from why.md

---

### Step 4: Generate why.md

**Use Write tool to create:**

**Location**: `.shipkit-lite/why.md`

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

{User-provided constraints/priorities formatted as bullets or paragraphs}
{END IF}
```

**Date handling:**
- **First time**: Set both Created and Last Updated to current date
- **Updating**: Keep original Created date, update Last Updated to current date

**Example output:**

```markdown
# Why This Project

**Created**: 2025-12-28
**Last Updated**: 2025-12-28

---

## Who Is This For?

Solo developers building side projects who need structure without complexity.

---

## Why Does This Exist?

Claude forgets context between sessions. Developers waste time re-explaining their stack, decisions, and goals every time. This solves that.

---

## Where Are We Now?

Early MVP with 17 core lite skills. Being tested by a handful of developers on POCs and side projects.

---

## Where Do We Need To Be?

Stable Lite edition with 20 skills used by 100+ developers. Full edition ready for teams working on complex projects.

---

## How Are We Getting There?

Prompt-driven skills (no bash complexity). Iterate quickly based on user feedback. Keep Lite simple and fast, Full comprehensive and powerful.

---

## Constraints & Priorities

**Constraints:**
- Solo maintainer, limited time
- Must work on Windows/Mac/Linux

**Priorities:**
1. Speed of execution (ship fast)
2. User experience (make it obvious)
3. Documentation (make it learnable)
```

---

### Step 5: Confirm to User

**After creating why.md:**

```
✅ Project vision defined

📁 Location: .shipkit-lite/why.md

📋 Summary:
  • Who: {Brief snippet from answer 1}
  • Why: {Brief snippet from answer 2}
  • Current: {Brief snippet from answer 3}

💡 This will auto-load at every session start to give me strategic context.
```

---

## Workspace Structure

Creates `.shipkit-lite/why.md` (auto-loaded by lite-session-start.py)

---

## Completion Checklist

Copy and track:
- [ ] Defined who the project serves
- [ ] Clarified why it matters
- [ ] Identified where it's going
- [ ] Saved to `.shipkit-lite/why.md`

---

## What Makes This "Lite"

**Lite approach**: 5 questions, 1 file, 2-5 minutes. Auto-loads at session start (~150 tokens).

**Full ShipKit approach**: 10 skills, 10+ files, 2-4 hours (personas, JTBD, market analysis, brand, stories, etc.).

**Philosophy**: Answer "why" in 5 minutes, not 5 hours. Enough strategic context without full product discovery.

**See `references/full-vs-lite.md` for detailed comparison.**

---

## Difference from Full ShipKit

**See `references/full-vs-lite.md` for detailed comparison.**

**Quick summary:**
- **Full ShipKit**: 2-4 hours, 10+ files, comprehensive product discovery
- **lite-why-project**: 2-5 minutes, 1 file, high-level strategic overview

Use lite-why-project for side projects, POCs, MVPs. Use full ShipKit for startups, market validation, enterprise products.

---

## When This Skill Integrates with Others

### Before This Skill

- None (can be first skill)
  - **When**: Starting a brand new project
  - **Why**: Vision provides strategic context before any other work
  - **Trigger**: User wants to define "why" before "what" or "how"

### After This Skill

- `/lite-project-context` - Scan technical stack
  - **When**: Vision defined, ready to document current state
  - **Why**: Stack info combined with vision enables better suggestions
  - **Trigger**: User runs "/lite-project-context" after defining vision

- `/lite-architecture-memory` - Log architectural decisions
  - **When**: Making technical decisions that need strategic alignment
  - **Why**: Decisions should align with vision (e.g., "ship fast" → simpler solutions)
  - **Trigger**: User logs decision like "using SQLite instead of Postgres"

- `/lite-spec` - Create feature specs
  - **When**: Building features for the project
  - **Why**: Specs can reference vision for alignment checks
  - **Trigger**: User says "build feature X" and spec references vision priorities

- Any other skill - Strategic context available
  - **When**: Any session after why.md created
  - **Why**: Auto-loads at session start, influences all Claude suggestions
  - **Trigger**: lite-session-start.py loads why.md automatically

### How Other Skills Use This

```
User: "Should we add OAuth or keep simple email auth?"

Claude (WITH why.md loaded):
"Given this is for solo developers (from why.md) with priority
 'ship fast' (from why.md), simple email auth aligns better.
 OAuth adds complexity that doesn't serve your vision of speed."

Claude (WITHOUT why.md):
"Both are valid. OAuth is more flexible but complex.
 Email auth is simpler but less feature-rich. What do you prefer?"
```

---

## Context Files This Skill Reads

**On update (if why.md exists)**:
- `.shipkit-lite/why.md` - Read old answers as defaults

**Never reads other files** - This is the starting point

---

## Context Files This Skill Writes

**Creates/Updates**:
- `.shipkit-lite/why.md` - OVERWRITE AND REPLACE
  - **Write Strategy**: OVERWRITE AND REPLACE
  - **Behavior**: Entire file regenerated when vision changes
  - **Why**: Represents current state, not history (like stack.md)
  - **Created date**: Preserved from original when updating
  - **Updated date**: Changed to current date

**Never modifies other files**

---

## Session Start Behavior

**lite-session-start.py auto-loads why.md** (~150 tokens)

**Result**: Claude starts every session knowing who/why/where (current/future)/how, enabling better aligned suggestions.

---

<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Has important context been saved to `.shipkit-lite/`?
2. **Prerequisites** - Does the next action need a spec or plan first?
3. **Session length** - Long session? Consider `/lite-work-memory` for continuity.

**Natural capabilities** (no skill needed): Implementation, debugging, testing, refactoring, code documentation.

**Suggest skill when:** User needs to make decisions, create persistence, or check project status.
<!-- /SECTION:after-completion -->

<!-- SECTION:success-criteria -->
## Success Criteria

Vision is defined when:
- [ ] User answered all 5 core questions
- [ ] Answers are high-level (1-3 sentences each)
- [ ] why.md created in `.shipkit-lite/`
- [ ] File follows template structure
- [ ] Dates are correct (Created preserved if updating)
- [ ] User knows vision will auto-load at session start
- [ ] Constraints/priorities included (if provided)
<!-- /SECTION:success-criteria -->
---

## Common Scenarios

**See `references/common-scenarios.md` for detailed examples:**
- Scenario 1: Brand New Project
- Scenario 2: Updating Existing Vision
- Scenario 3: Mid-Session Suggestion

---

## Tips for Effective Vision Definition

**See `references/tips.md` for detailed guidance on:**
- Keeping it concise (1-3 sentences per question)
- Being honest about project scope
- Understanding how vision influences Claude's decisions
- When to update the vision
- Sharing vision with team
- When NOT to use this skill (vs full ShipKit)

**Quick tips:**
- High-level, not detailed
- Strategic, not tactical
- Update when direction changes
- Share why.md for team alignment

---

## Example Output

**See `references/example-output.md` for a complete example of why.md.**

**Structure:**
- Created/Last Updated dates
- 5 core sections (Who/Why/Where Now/Where To Be/How)
- Optional Constraints & Priorities section

**Remember**: This is strategic context, not requirements. Keep it high-level. Answer "why" not "how". Think vision, not spec.

---

## Reference Documentation

**This skill provides detailed guidance in reference files:**

**Process Examples:**
- `references/common-scenarios.md` - 3 scenarios (brand new project, updating vision, mid-session suggestion)

**Best Practices:**
- `references/tips.md` - Tips for effective vision definition, when NOT to use this skill

**Templates & Examples:**
- `references/example-output.md` - Complete example of why.md file
- `references/full-vs-lite.md` - Comparison between lite-why-project and full ShipKit prod-* skills

**How to use references:**
- Main SKILL.md provides the 5-question process
- Reference files provide examples and best practices
- Keep answers concise (1-3 sentences each)
- Update vision when direction changes
