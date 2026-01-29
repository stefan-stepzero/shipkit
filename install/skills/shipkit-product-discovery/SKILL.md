---
name: shipkit-product-discovery
description: "Use when defining users, personas, or user journeys. Triggers: 'who are users', 'create personas', 'user research', 'user stories'."
---

# shipkit-product-discovery - Lightweight Product Discovery

**Purpose**: Combines personas, user journey mapping, and user stories into a single lightweight workflow for POC/MVP projects

---

## When to Invoke

**User triggers**:
- "Who are our users?", "Create personas", "User research"
- "User journey", "Map user needs", "Product discovery"
- "User stories", "What features?", "Requirements"

**Workflow position**:
- Early Pillar 1 (Vision) or Pillar 3 (Co-design) - before specification
- Replaces separate prod-personas + prod-jobs-to-be-done + prod-user-stories for POC/MVP

---

## Prerequisites

**Optional**:
- `.shipkit/why.md` (Vision helps guide persona creation)
- `.shipkit/stack.md` (Technical constraints inform feasibility)

**If missing**: Generate personas and stories based on user input alone

---

## Process

### Step 0: Check for Existing File

**Quick Exit Check**:
1. Check if `.shipkit/product-discovery.md` exists
2. If exists AND modified < 5 minutes ago: Show user, ask "Use this or regenerate?"
3. If exists AND modified > 5 minutes ago: Proceed to File Exists Workflow (Step 0b)
4. If doesn't exist: Skip to Step 1 (generate new)

**File Exists Workflow (Step 0b)**:
- Options: View / Update / Replace / Cancel
- View: Display current file, then ask what to do
- Update: Read existing, ask what to change, regenerate with updates
- Replace: Archive old version, generate completely new
- Cancel: Exit without changes

---

### Step 1: Gather Context About Users and Goals

**Ask user 3 clarifying questions**:

1. **Who are your primary users?** (1-3 types)
2. **What are they trying to accomplish?** (job/pain point, current workflow)
3. **What's your biggest assumption about their needs?** (becomes testable hypothesis)

---

### Step 2: Read Existing Context

**Read these files** (if exist):
- `.shipkit/why.md` - Vision context
- `.shipkit/stack.md` - Technical constraints

**Token budget**: Keep context reading under 1000 tokens.

---

### Step 3: Generate Product Discovery Document

**Create file using Write tool**: `.shipkit/product-discovery.md`

**Content includes**:
1. **Personas** (1-3 lightweight personas)
2. **User Journeys** (current state, pain points, jobs-to-be-done)
3. **User Stories** (feature requirements with acceptance criteria)

---

## Product Discovery Document Template Structure

```markdown
# Product Discovery

**Last Updated**: [YYYY-MM-DD]

---

## Personas

**Persona 1: [Name/Role]**
- **Who**: [Role, context, background]
- **Goals**: [What they're trying to achieve]
- **Pain Points**: [Current frustrations]
- **Context**: [When/where they use the product]

---

## User Journeys

**Journey 1: [Persona Name] - [Job to be Done]**

**Current State**: [Steps, Pain Point]
**Jobs-to-be-Done**: Functional, Emotional, Social
**Future State**: [Improved workflow, Benefit]

---

## User Stories

**Story 1: [Feature Name]**

**As a** [Persona], **I want** [goal], **So that** [benefit].

**Acceptance Criteria**:
- [ ] Given [context], When [action], Then [result]

**Priority**: High/Medium/Low

---

## Quality Checklist

- [ ] Each persona has clear goals (not generic)
- [ ] Personas are distinct (not overlapping)
- [ ] Jobs-to-be-done are specific and actionable
- [ ] User stories have testable acceptance criteria
- [ ] Stories trace back to specific persona needs
```

---

### Step 4: Archive Old Version (If Replacing)

If user chose "Replace" in Step 0:
1. Create archive: `.shipkit/archive/product-discovery/`
2. Copy existing with timestamp
3. Write new file

---

### Step 5: Save and Suggest Next Step

**Output to user**: Summary of personas defined, journeys mapped, user stories created.

---

## Completion Checklist

Copy and track:
- [ ] Defined target personas
- [ ] Created user journeys
- [ ] Documented user stories
- [ ] Saved to `.shipkit/product-discovery.md`

---

## What Makes This "Lite"

**Included**:
- 1-3 personas (not 5-7 like full prod-personas)
- Combined workflow (personas → journeys → stories in one skill)
- Quick exit check (avoid regenerating recent files)
- Lightweight acceptance criteria (happy path focus)

**Not included** (vs full prod-personas + prod-jobs-to-be-done + prod-user-stories):
- Separate skills for each phase
- Deep competitive persona analysis
- Extensive journey mapping workshops
- Comprehensive edge case scenarios

**Philosophy**: Capture enough to start building, not exhaustive research.

---

## When This Skill Integrates with Others

### Before shipkit-product-discovery
- `/shipkit-why-project` - Defines vision context (optional but recommended)
- `/shipkit-project-context` - Scans technical stack (optional)

### After shipkit-product-discovery
- `/shipkit-spec` - Creates detailed specifications from user stories
- `/shipkit-architecture-memory` - Documents key product decisions (optional)
- `/shipkit-plan` - Creates implementation plan

---

## Context Files This Skill Reads

**Optional** (read if exist):
- `.shipkit/why.md` - Understand project vision
- `.shipkit/stack.md` - Understand technical constraints

---

## Context Files This Skill Writes

**Write Strategy: OVERWRITE**

**Creates/Updates**:
- `.shipkit/product-discovery.md` - Combined personas, user journeys, user stories

**Archive location** (if replacing):
- `.shipkit/archive/product-discovery/product-discovery.[timestamp].md`

---

## Lazy Loading Behavior

**This skill loads context ON DEMAND**:

1. User invokes `/shipkit-product-discovery`
2. Check if file exists (Quick Exit Check)
3. If regenerating: Ask 3 questions
4. Read why.md, stack.md (~1000 tokens)
5. Generate Product Discovery Document
6. Total context loaded: ~1500 tokens

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

Product Discovery Document is complete when:
- [ ] 1-3 personas with clear goals and context
- [ ] Each persona has distinct characteristics
- [ ] User journeys identify current state pain points
- [ ] Jobs-to-be-done are specific and actionable
- [ ] User stories have testable acceptance criteria
- [ ] Stories trace back to specific persona needs
- [ ] Quality checklist embedded
- [ ] File saved to `.shipkit/product-discovery.md`
<!-- /SECTION:success-criteria -->
---

**Remember**: This file is your single source of truth for user understanding. Update it as you learn more about users. Product discovery is iterative; refine as insights emerge.
