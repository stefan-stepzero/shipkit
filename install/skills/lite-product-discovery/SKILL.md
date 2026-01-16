---
name: lite-product-discovery
description: "Use when defining users, personas, or user journeys. Triggers: 'who are users', 'create personas', 'user research', 'user stories'."
---

# lite-product-discovery - Lightweight Product Discovery

**Purpose**: Combines personas, user journey mapping, and user stories into a single lightweight workflow for POC/MVP projects

---

## When to Invoke

**User triggers**:
- "Who are our users?", "Create personas", "User research"
- "User journey", "Map user needs", "Product discovery"
- "User stories", "What features?", "Requirements"

**Workflow position**:
- Early Pillar 1 (Vision) or Pillar 3 (Co-design) - before specification
- First step in understanding users and their needs
- Replaces separate prod-personas + prod-jobs-to-be-done + prod-user-stories for POC/MVP projects

---

## Prerequisites

**Optional**:
- `.shipkit-lite/why.md` (Vision helps guide persona creation and feature prioritization)
- `.shipkit-lite/stack.md` (Technical constraints can inform feasibility of user needs)

**If missing**: Generate personas and stories based on user input alone (no blocking dependencies)

---

## Process

### Step 0: Check for Existing File (Quick Exit + File Exists Workflow)

**Quick Exit Check** (see SKILL-QUALITY-AND-PATTERNS.md Part 2.1):

```markdown
1. Check if `.shipkit-lite/product-discovery.md` exists

2. If exists AND modified < 5 minutes ago:
   - Show user: "Found recent Product Discovery Document (modified [time ago])"
   - Ask: "Use this or regenerate?"
   - If "use this" → Exit early (save tokens)
   - If "regenerate" → Proceed to Step 1

3. If exists AND modified > 5 minutes ago:
   - Proceed to File Exists Workflow (Step 0b)

4. If doesn't exist:
   - Skip to Step 1 (generate new)
```

**File Exists Workflow** (see SKILL-QUALITY-AND-PATTERNS.md Part 2.2):

```markdown
### Step 0b: File Already Exists

File exists: `.shipkit-lite/product-discovery.md`

**Options:**

1. **View** - Show current contents, then ask what to do
2. **Update** - Read existing, ask what to change, regenerate with updates
3. **Replace** - Archive old version, generate completely new
4. **Cancel** - Exit without changes

**User choice:**

**If View:**
- Display current file
- Ask: "Keep this, update it, or replace?"
- Go to Update/Replace/Cancel

**If Update:**
- Read existing file
- Ask: "What should change?" (e.g., "Add new persona", "Refine user story acceptance criteria")
- Regenerate incorporating updates
- Use Write tool to overwrite

**If Replace:**
- Archive current version (see Archive Before Overwrite pattern)
- Proceed to Step 1 (generate new)

**If Cancel:**
- Exit, no changes made
```

---

### Step 1: Gather Context About Users and Goals

**Ask user 3 clarifying questions**:

1. **Who are your primary users?**
   - Describe 1-3 types of users who will use this product
   - Examples: "Solo developers", "Enterprise team leads", "Non-technical founders"

2. **What are they trying to accomplish?**
   - What job or pain point brings them to your product?
   - What's their current workflow and where does it break down?

3. **What's your biggest assumption about their needs?**
   - What user need are you assuming but haven't validated?
   - This becomes a testable hypothesis in your user stories

**Why ask first**: Personas without context are fiction; we need real understanding of user goals to create actionable discovery artifacts.

---

### Step 2: Read Existing Context

**Read these files to understand project context**:

```bash
# Vision context
.shipkit-lite/why.md

# Technical constraints
.shipkit-lite/stack.md
```

**Token budget**: Keep context reading under 1000 tokens.

**If files don't exist**: Proceed with user input only (no dependency on other files)

---

### Step 3: Generate Product Discovery Document

**Create file using Write tool** (overwrites if exists):

**Location**: `.shipkit-lite/product-discovery.md`

**Content includes**:
1. **Personas** (1-3 lightweight personas)
2. **User Journeys** (current state, pain points, jobs-to-be-done)
3. **User Stories** (feature requirements with acceptance criteria)

---

## Product Discovery Document Template Structure

**The Product Discovery Document MUST follow this template**:

```markdown
# Product Discovery

**Last Updated**: [YYYY-MM-DD]

---

## Personas

**Persona 1: [Name/Role]**

- **Who**: [Role, context, background]
- **Goals**: [What they're trying to achieve]
- **Pain Points**: [Current frustrations and blockers]
- **Context**: [When/where they use the product, constraints they face]

**Persona 2: [Name/Role]** (if applicable)

[Same structure as Persona 1]

**Persona 3: [Name/Role]** (if applicable)

[Same structure as Persona 1]

---

## User Journeys

**Journey 1: [Persona Name] - [Job to be Done]**

**Current State**:
- Step 1: [What they do now]
- Step 2: [Next action]
- **Pain Point**: [Where it breaks down]

**Jobs-to-be-Done**:
- **Functional Job**: [Task they need to complete]
- **Emotional Job**: [How they want to feel]
- **Social Job**: [How they want to be perceived]

**Future State** (after using your product):
- Step 1: [Improved workflow]
- Step 2: [Reduced friction]
- **Benefit**: [Outcome achieved]

**Journey 2: [Persona Name] - [Job to be Done]** (if applicable)

[Same structure as Journey 1]

---

## User Stories

**Story 1: [Feature Name]**

**As a** [Persona],
**I want** [goal/capability],
**So that** [benefit/outcome].

**Acceptance Criteria**:
- [ ] Given [context], When [action], Then [expected result]
- [ ] Given [context], When [action], Then [expected result]
- [ ] Edge case: [scenario and expected behavior]

**Priority**: High/Medium/Low

**Story 2: [Feature Name]** (continue for all core features)

[Same structure as Story 1]

---

## Quality Checklist

**Validate Product Discovery Document meets standards:**

### Personas
- [ ] Each persona has clear goals and context (not generic)
- [ ] Personas are distinct (not overlapping)
- [ ] Based on real user research or founder insight (not assumptions)

### User Journeys
- [ ] Current state pain points identified
- [ ] Jobs-to-be-done are specific and actionable
- [ ] Future state shows measurable improvement

### User Stories
- [ ] Stories follow "As a [persona], I want [goal], so that [benefit]" format
- [ ] Acceptance criteria are testable (Given/When/Then)
- [ ] Each story has clear priority
- [ ] Stories trace back to specific persona needs

---

**⚠️ Review this checklist before using Product Discovery Document for specification or implementation**
```

---

### Step 4: Archive Old Version (If Replacing)

**Archive Before Overwrite Pattern** (see SKILL-QUALITY-AND-PATTERNS.md Part 2.5):

```markdown
**If user chose "Replace" in Step 0:**

1. Create archive directory: `.shipkit-lite/archive/product-discovery`

2. Copy existing file with timestamp:
   ```bash
   mkdir -p .shipkit-lite/archive/product-discovery
   cp .shipkit-lite/product-discovery.md .shipkit-lite/archive/product-discovery/product-discovery.[TIMESTAMP].md
   ```

3. Add archive note to new file:
   ```markdown
   **Previous version**: See `.shipkit-lite/archive/product-discovery/product-discovery.[timestamp].md`
   ```

4. Write new file (overwrites current)
```

**Why archive**: Preserve previous discovery learnings when regenerating with new insights; product understanding evolves as you validate assumptions.

---

### Step 5: Save and Suggest Next Step

**Use Write tool to create/overwrite**: `.shipkit-lite/product-discovery.md`

**Output to user**:
```
✅ Product Discovery Document created/updated

📁 Location: .shipkit-lite/product-discovery.md

📋 Summary:
  • X personas defined
  • User journeys mapped with pain points identified
  • Y user stories with acceptance criteria

📦 Previous version archived: .shipkit-lite/archive/product-discovery/[filename]
(if replaced)
```

**Now invoke `/lite-whats-next`** for intelligent workflow guidance.

---

## Completion Checklist

Copy and track:
- [ ] Defined target personas
- [ ] Created user journeys
- [ ] Documented user stories
- [ ] Saved to `.shipkit-lite/product-discovery.md`
- [ ] Invoke `/lite-whats-next` for workflow guidance

**REQUIRED FINAL STEP:** After completing this skill, you MUST invoke `/lite-whats-next` for workflow guidance. This is mandatory per lite.md meta-rules.

---

## What Makes This "Lite"

**Included**:
- ✅ 1-3 personas (not 5-7 like full prod-personas)
- ✅ Combined workflow (personas → journeys → stories in one skill)
- ✅ Quick exit check (avoid regenerating recent files)
- ✅ File exists workflow (view/update/replace/cancel)
- ✅ Lightweight acceptance criteria (happy path focus)

**Not included** (vs full prod-personas + prod-jobs-to-be-done + prod-user-stories):
- ❌ Separate skills for each phase
- ❌ Deep competitive persona analysis
- ❌ Extensive journey mapping workshops
- ❌ Comprehensive edge case scenarios in acceptance criteria
- ❌ Stakeholder validation rounds

**Philosophy**: Capture enough to start building, not exhaustive research. Product discovery is iterative; you'll learn more by shipping and validating assumptions.

---

## When This Skill Integrates with Others

### Before lite-product-discovery
- `/lite-why-project` - Defines vision context (optional but recommended)
  - **When**: User wants to ground product discovery in strategic vision
  - **Why**: Vision guides persona prioritization and feature selection
  - **Trigger**: User asks "What's the project vision?" or wants strategic alignment

- `/lite-project-context` - Scans technical stack (optional)
  - **When**: User has existing codebase
  - **Why**: Technical constraints inform feasibility of user needs
  - **Trigger**: User wants to understand what's already built

### After lite-product-discovery
- `/lite-spec` - Creates detailed specifications from user stories
  - **When**: User wants to start building first feature
  - **Why**: Detailed specification ensures implementation matches user needs
  - **Trigger**: User ready to implement specific user story

- `/lite-architecture-memory` - Documents key product decisions (optional)
  - **When**: User made important product trade-offs during discovery
  - **Why**: Preserve "why" behind decisions before they're forgotten
  - **Trigger**: User asks to log product decisions

- `/lite-plan` - Creates implementation plan
  - **When**: User has specification and ready to plan implementation
  - **Why**: Break down specification into concrete tasks
  - **Trigger**: User asks "How do we build this?"

### When lite-product-discovery Runs Again
- File exists workflow activates
- User can view/update/replace existing discovery document
- Common updates: Add new persona, refine user stories, update acceptance criteria based on user feedback

---

## Context Files This Skill Reads

**Optional** (read if exist):
- `.shipkit-lite/why.md` - Understand project vision and goals
- `.shipkit-lite/stack.md` - Understand technical constraints

**If missing**: Proceed with user input (no blocking dependencies)

---

## Context Files This Skill Writes

**Write Strategy: OVERWRITE** (see SKILL-QUALITY-AND-PATTERNS.md Part 2.2 - File Exists Workflow)

**Creates/Updates**:
- `.shipkit-lite/product-discovery.md` - Combined personas, user journeys, and user stories

**Update Behavior**:
- File exists → File Exists Workflow (view/update/replace/cancel)
- Recent file (< 5 min) → Quick Exit Check (use or regenerate)
- Replace → Archive old version first
- Update → Read existing, incorporate changes
- Each write REPLACES entire file contents

**Archive location** (if replacing):
- `.shipkit-lite/archive/product-discovery/product-discovery.[timestamp].md`

**Why OVERWRITE:**
- Product discovery evolves as you learn about users
- Single source of truth for current user understanding
- Archive preserves historical versions for reference

---

## Lazy Loading Behavior

**This skill loads context ON DEMAND**:

1. User invokes `/lite-product-discovery`
2. Master tells Claude to read this SKILL.md
3. Claude checks if file exists (Quick Exit Check)
4. If regenerating: Ask 3 questions
5. Read why.md, stack.md (~1000 tokens)
6. Generate Product Discovery Document
7. Total context loaded: ~1500 tokens

**Not loaded unless needed**:
- Implementation details
- Other product discovery artifacts (unless referenced)
- Source code
- Full project specifications

---

## Success Criteria

Product Discovery Document is complete when:
- [ ] 1-3 personas with clear goals and context
- [ ] Each persona has distinct characteristics (not overlapping)
- [ ] User journeys identify current state pain points
- [ ] Jobs-to-be-done are specific and actionable
- [ ] User stories have testable acceptance criteria (Given/When/Then)
- [ ] Stories trace back to specific persona needs
- [ ] Quality checklist embedded
- [ ] File saved to `.shipkit-lite/product-discovery.md`
- [ ] Old version archived (if replaced)

---

## Common Scenarios

### Scenario 1: First Product Discovery (First Time)

```
User: "Who should use this product?"

Claude:
1. Check .shipkit-lite/product-discovery.md (doesn't exist)
2. Ask: "Who are your primary users and what are they trying to accomplish?"
   User: "Solo developers who want to quickly validate ideas without writing full specs"
3. Ask: "What are their pain points with current tools?"
   User: "Existing tools require too much ceremony; they just want to start coding"
4. Ask: "What's your biggest assumption about their needs?"
   User: "They prefer interactive guidance over reading documentation"
5. Read why.md (if exists)
6. Generate Product Discovery Document with:
   - Persona: "Sam - Solo Developer"
   - Journey: Current state (too much process) → Future state (interactive guidance)
   - User Stories: "As Sam, I want interactive feature creation..."
7. Save to .shipkit-lite/product-discovery.md
```

### Scenario 2: Update Personas (File Exists)

```
User: "Add a new persona type"

Claude:
1. Check .shipkit-lite/product-discovery.md (exists, modified 3 days ago)
2. Show: "File exists. Options: View/Update/Replace/Cancel"
   User: "Update"
3. Read existing file (1 persona: Solo Developer)
4. Ask: "What should change?"
   User: "Add enterprise team leads as a persona"
5. Ask clarifying questions about enterprise team leads
6. Regenerate with both personas:
   - Persona 1: Sam - Solo Developer (keep existing)
   - Persona 2: Taylor - Enterprise Team Lead (new)
7. Overwrite .shipkit-lite/product-discovery.md
```

### Scenario 3: Quick Exit (Recent File)

```
User: "Show me our personas"

Claude:
1. Check .shipkit-lite/product-discovery.md (exists, modified 2 minutes ago)
2. Show: "Found recent Product Discovery Document (2 min ago). Use this or regenerate?"
   User: "Use this"
3. Display contents of product-discovery.md
4. Exit (saved ~1500 tokens, no regeneration)
```

---

## Tips for Effective Product Discovery

**Persona Creation**:
- Based on real user research or founder insight (not generic "busy professional")
- Include specific context (e.g., "Uses Python for data science, limited frontend experience")
- Keep to 1-3 personas for POC/MVP (focus over breadth)

**User Journey Mapping**:
- Identify ONE critical pain point per journey (not 10 minor annoyances)
- Focus on jobs-to-be-done, not feature requests
- Map current state honestly (where workflows break down)

**User Story Writing**:
- Start with happy path scenarios (edge cases can wait)
- Acceptance criteria should be testable (Given/When/Then format)
- Trace each story back to specific persona need (avoid feature creep)

**When to upgrade to full /prod-personas + /prod-jobs-to-be-done + /prod-user-stories**:
- Need deep competitive persona analysis with quantitative research
- Multiple product stakeholders requiring separate workshops and alignment
- Enterprise product requiring compliance and extensive edge case coverage
- Team size > 5 where separate discovery phases add clarity

---

**Remember**: This file is your single source of truth for user understanding. Update it as you learn more about users through validation and user feedback. Product discovery is iterative; refine as insights emerge.
