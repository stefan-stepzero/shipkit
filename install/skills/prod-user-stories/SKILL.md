---
name: prod-user-stories
description: "Use when converting interaction design into actionable user stories with acceptance criteria"
---

# User Stories

## Agent Persona

**Load:** `.claude/agents/discovery-agent.md`

Adopt: Requirements-focused, writes testable acceptance criteria, breaks large features into small deliverable stories.

## Purpose

Convert interaction design journeys and product requirements into actionable user stories that guide development. Each story describes specific value from the user's perspective with clear, testable acceptance criteria.

## When to Trigger

User says:
- "Write user stories"
- "Create requirements"
- "Convert the design into stories"
- "What stories do we need?"
- "Break this down into dev tasks"

Or when:
- Interaction design is complete
- Ready to plan development
- Need to communicate requirements to engineering
- Preparing for sprint planning

## Prerequisites

**Required:**
- Interaction design defined (`.shipkit/skills/prod-interaction-design/outputs/interaction-design.md`)
  - Need user journeys to convert into stories
  - Interaction patterns inform acceptance criteria

**Recommended (provides context):**
- Personas (understand who stories are for)
- Jobs-to-be-done (understand user goals)
- Product stage (POC/MVP/Established affects story scope)

## Inputs

- **Interaction Design:** User journeys, screen flows, patterns
- **Personas:** Who are we building for?
- **Product Stage:** POC / MVP / Established (affects story detail)
- **Priority Guidance:** Must-have vs should-have vs nice-to-have

## Process

### Step 1: Read References

Read all files in the skill's references directory:
```bash
.shipkit/skills/prod-user-stories/references/
```

**If >2 files exist:** Ask the user which files are most relevant for this task.

This includes built-in guidance (reference.md, examples.md) and any user-added files (PDFs, research, notes).

---

### Step 2: Check Product Constitution (Recommended)

**If product constitution exists:**
- Read `.shipkit/skills/prod-constitution-builder/outputs/product-constitution.md`
- Project type determines acceptance criteria rigor:
  - **POC:** Minimal ACs (happy path only, skip edge cases/errors)
  - **Side Project MVP:** Basic ACs (happy path + obvious errors only)
  - **B2C/B2B Greenfield:** Comprehensive ACs (all scenarios, full edge case coverage)
  - **Experimental:** ACs focused on experiment validation metrics
  - **Existing Project:** Match existing story format and AC standards

**If constitution doesn't exist:** Default to medium rigor (happy path + key errors)

---

### Step 3: Run the Script

```bash
.shipkit/skills/prod-user-stories/scripts/create-user-stories.sh
```

This initializes the user stories document from template.

### Step 4: Organize Into Epics

Group related stories into epics (large features):

**Epic Examples:**
- User Onboarding
- Core Workflow
- Account Management
- Reporting & Analytics
- Mobile Experience

**For each epic, identify:**
- Goal: What does this epic accomplish?
- Success metric: How do we measure success?
- User journey stage: Which stage from interaction-design.md?

### Step 5: Write Stories Using Standard Format

**Template:**
```
As a [specific persona]
I want to [action/capability]
So that [clear benefit/outcome]

Acceptance Criteria:
- [ ] Given [context], when [action], then [result]
- [ ] [Additional criteria]

Priority: Must Have / Should Have / Nice to Have
Estimated Effort: S / M / L / XL
```

**Story Checklist (INVEST):**
- **Independent:** Can be delivered standalone
- **Negotiable:** Details flexible, not prescriptive
- **Valuable:** Delivers user or business value
- **Estimable:** Team can estimate effort
- **Small:** Completable in one iteration
- **Testable:** Has clear pass/fail criteria

### Step 6: Convert Journeys to Stories

**From Interaction Design → User Stories:**

**Journey Stage: First Use / Onboarding**
- "Aha!" moment: User completes first task in <5 minutes

**Becomes Stories:**
```
Story 1: "As a new user, I want to sign up with Google,
         so that I can get started in seconds"

Story 2: "As a new user, I want guided setup,
         so that I reach value quickly without getting lost"
```

**Screen Flow: Sign Up → Onboarding → First Value**

**Becomes Stories:**
```
Story 1: Sign up page with social auth
Story 2: 3-step onboarding wizard
Story 3: First value screen (user achieves something)
```

### Step 7: Write Acceptance Criteria

**Use Given-When-Then Format:**
```
Given [context/precondition]
When [user action]
Then [expected outcome]
```

**Cover Multiple Scenarios:**
- **Happy path:** Everything works ideally
- **Alternative paths:** Valid but less common
- **Error conditions:** Invalid input, failures
- **Edge cases:** Boundary conditions

**Make Criteria Specific:**
- ❌ "Search is fast"
- ✅ "Search returns results in <500ms for 95% of queries"

**Example:**
```
As a user
I want to search for products
So that I can find what I need quickly

Acceptance Criteria:
- [ ] Given I type in search box, when I pause typing (300ms),
      then results update automatically
- [ ] Given search results, when they load, then most relevant
      items appear first
- [ ] Given no matches, when I search, then I see "No results
      for '[query]'" with suggestions
- [ ] Given I want to filter, when I select category, then
      results narrow immediately
- [ ] Search includes: product name, description, tags
- [ ] Results load in <500ms for 95% of queries
```

### Step 8: Prioritize Stories

**Use MoSCoW Method:**

**Must Have:**
- Critical to core value
- Product fails without it
- Blocks other features
- Legal/regulatory requirement

**Should Have:**
- Important but not critical
- Has workaround if missing
- High value, reasonable effort

**Could Have:**
- Nice improvements
- Low priority
- Easy to defer

**Won't Have (This Release):**
- Out of scope
- Future consideration

**Alternative: Value vs Effort Matrix**
```
High Value, Low Effort → Do First (Quick Wins)
High Value, High Effort → Plan Carefully (Major Features)
Low Value, Low Effort → Do Later (Fill Gaps)
Low Value, High Effort → Don't Do (Money Pit)
```

### Step 9: Size Stories

**Estimate effort:**

**S (Small):** <1 day
- Simple UI change, validation rule, copy update

**M (Medium):** 1-3 days
- New screen with standard components, simple integration

**L (Large):** 3-5 days
- Complex workflow, new integration, multiple systems

**XL (Extra Large):** 5-10 days
- **Action:** Break into smaller stories

### Step 10: Identify Dependencies

**Note which stories depend on others:**
- "Story 2.3 depends on Story 2.1 (authentication)"
- "Story 3.1 requires API integration (Story 1.5)"

**Types of Dependencies:**
- Sequential: B can't start until A completes
- Data: B needs data created by A
- Technical: B needs infrastructure from A

### Step 11: Adapt to Product Stage

**For POC:**
- Must-have only (prove core hypothesis)
- Happy path acceptance criteria
- Manual workarounds acceptable
- Speed over polish

**For MVP:**
- Must-have + some should-haves
- Happy path + common errors
- Basic automation
- Professional quality

**For Established:**
- Full feature set
- All paths covered
- Performance optimized
- Accessibility compliant

## Outputs

- `.shipkit/skills/prod-user-stories/outputs/user-stories.md`

This document includes:
- Stories organized by epics
- Clear acceptance criteria for each story
- Priority and effort estimates
- Dependencies mapped
- Context-specific scope (POC/MVP/Established)

## Constraints

- **DO NOT** create user-stories.md manually
- **ALWAYS** use the create-user-stories.sh script
- **MUST** have interaction design completed first (need journeys to convert)
- **WRITE** stories from user perspective (not technical tasks)
- **MAKE** acceptance criteria specific and testable
- **KEEP** stories small (1-5 days of work)

## Quality Checks

Before marking complete, verify:
- [ ] Stories organized into logical epics
- [ ] Each story follows "As a/I want/So that" format
- [ ] Acceptance criteria use Given-When-Then
- [ ] Stories cover happy path + errors + edge cases
- [ ] Each story is INVEST-compliant (Independent, Negotiable, Valuable, Estimable, Small, Testable)
- [ ] Priorities assigned (Must/Should/Could/Won't)
- [ ] Effort estimated (S/M/L/XL)
- [ ] Dependencies identified
- [ ] Stories are sized appropriately (not too large)
- [ ] Traced to interaction design journeys

## Next Steps

After user stories are complete:
- **→ /prod-assumptions-and-risks** - Identify assumptions behind stories and delivery risks
- **→ /prod-success-metrics** - Define how to measure success of these features

## Context

This is **Step 8 of 12** in the Product Discovery sequential workflow.

## Tips

**Focus on Value, Not Features:**
- ❌ "As a user, I want a dashboard with graphs"
- ✅ "As a manager, I want to see team progress at a glance, so I know where to help"

**Be Specific in Acceptance Criteria:**
- Avoid "works well", "looks good", "is fast"
- Use measurable outcomes: "<2 seconds", ">90% completion", "handles 10,000 items"

**Break Large Stories:**
- If story takes >5 days, split it
- Vertical slicing: deliver end-to-end thin features
- Horizontal slicing by journey stage, CRUD operation, or user role

**Write Testable Criteria:**
- Each criterion should have clear pass/fail
- Enables automated testing
- Prevents scope creep

**Link to Design:**
- Reference screens from interaction design
- Attach wireframes or prototypes
- Note interaction patterns used

**Collaborate:**
- Write stories with PM, designer, engineers together
- Review as team before starting development
- Refine based on feedback

## Common Mistakes to Avoid

❌ **Technical stories without user value**
- "As a developer, I want to refactor the database"
- Fix: Frame as user benefit ("pages load in <2 seconds")

❌ **Solution-first instead of problem-first**
- "I want a carousel with 5 slides"
- Fix: Describe outcome ("understand product quickly")

❌ **Vague acceptance criteria**
- "Feature works correctly", "Looks good"
- Fix: Be specific and measurable

❌ **Epics disguised as stories**
- "I want a complete analytics dashboard"
- Fix: Break into smaller stories (view metrics, filter data, export reports)

❌ **Missing the "So That"**
- "I want to export data" (why?)
- Fix: Add benefit ("so I can analyze in Excel")
