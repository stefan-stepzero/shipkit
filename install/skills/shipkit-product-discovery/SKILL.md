---
name: shipkit-product-discovery
description: "Use when defining users, personas, or user journeys. Triggers: 'who are users', 'create personas', 'user research', 'user stories'."
argument-hint: "[persona or journey]"
agent: shipkit-product-owner-agent
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
- `.shipkit/why.json` (Vision helps guide persona creation)
- `.shipkit/stack.json` (Technical constraints inform feasibility)

**If missing**: Generate personas and stories based on user input alone

---

## Process

### Step 0: Check for Existing File

**Quick Exit Check**:
1. Check if `.shipkit/product-discovery.json` exists
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

**Use AskUserQuestion tool to gather requirements:**

**Question 1 - Discovery Focus:**
```
header: "Focus"
question: "What aspect of product discovery do you need?"
options:
  - label: "Full Discovery (Recommended)"
    description: "Personas + journeys + user stories"
  - label: "Personas Only"
    description: "Define who your users are"
  - label: "User Journeys"
    description: "Map how users accomplish goals"
  - label: "User Stories"
    description: "Generate feature requirements"
```

**Question 2 - User Type:** (if not provided in argument)
```
header: "Users"
question: "Who are your primary users?"
options:
  - label: "Consumers (B2C)"
    description: "End users, general public"
  - label: "Businesses (B2B)"
    description: "Companies, teams, professionals"
  - label: "Internal Users"
    description: "Your team, employees, admins"
  - label: "Developers"
    description: "API consumers, integrators"
```

**If user selects "Other"**: Follow up with clarifying questions about their specific user types and goals.

---

### Step 2: Read Existing Context

**Read these files** (if exist):
- `.shipkit/why.json` - Vision context
- `.shipkit/stack.json` - Technical constraints

**Token budget**: Keep context reading under 1000 tokens.

---

### Step 3: Generate Product Discovery JSON Artifact

**Create file using Write tool**: `.shipkit/product-discovery.json`

**Content includes**:
1. **Personas** (1-3 lightweight personas with IDs for cross-referencing)
2. **Pain Points** (extracted from personas, linked by ID)
3. **User Journeys** (step-by-step with emotion tracking and pain point references)
4. **Opportunities** (linked to pain points and personas)

**All entities use stable IDs** (`persona-1`, `pain-1`, `journey-1`, `opp-1`) to enable graph traversal and relationship mapping across the artifact.

---

## Product Discovery JSON Schema (Quick Reference)

The output MUST conform to the Shipkit JSON Artifact Convention.

```json
{
  "$schema": "shipkit-artifact",
  "type": "product-discovery",
  "version": "1.0",
  "lastUpdated": "2025-01-15T10:00:00Z",
  "source": "shipkit-product-discovery",
  "summary": { "totalPersonas", "totalJourneys", "totalPainPoints", "totalOpportunities", "primaryPersona", "topPainPoint" },
  "personas": [{ "id", "name", "role", "goals", "frustrations", "techComfort", "context", "isPrimary" }],
  "painPoints": [{ "id", "description", "severity", "affectedPersonas", "currentWorkaround", "frequency" }],
  "journeys": [{ "id", "name", "persona", "steps": [{ "id", "action", "emotion", "painPoints", "touchpoints" }] }],
  "opportunities": [{ "id", "description", "addressesPainPoints", "impactedPersonas", "effort", "impact" }]
}
```

**Full schema and field reference**: See `references/output-schema.md`

**Realistic example**: See `references/example.json`

### Graph Relationships

The ID-based cross-references enable these graph traversals:

- **Persona -> Pain Points**: `painPoints[].affectedPersonas` references `personas[].id`
- **Journey -> Persona**: `journeys[].persona` references `personas[].id`
- **Journey Step -> Pain Points**: `journeys[].steps[].painPoints` references `painPoints[].id`
- **Opportunity -> Pain Points**: `opportunities[].addressesPainPoints` references `painPoints[].id`
- **Opportunity -> Personas**: `opportunities[].impactedPersonas` references `personas[].id`

---

### Step 4: Archive Old Version (If Replacing)

If user chose "Replace" in Step 0:
1. Create archive: `.shipkit/archive/product-discovery/`
2. Copy existing with timestamp: `product-discovery.[timestamp].json`
3. Write new file

---

### Step 5: Save and Suggest Next Step

**Output to user**: Summary of personas defined, journeys mapped, user stories created.

---

## Completion Checklist

Copy and track:
- [ ] Defined target personas with stable IDs
- [ ] Extracted pain points with severity and persona links
- [ ] Created user journeys with emotion tracking and pain point references
- [ ] Identified opportunities linked to pain points and personas
- [ ] Summary fields populated with correct counts
- [ ] All cross-references use valid IDs
- [ ] Saved to `.shipkit/product-discovery.json`

---

## What Makes This "Lite"

**Included**:
- 1-3 personas (not 5-7 like full prod-personas)
- Combined workflow (personas -> pain points -> journeys -> opportunities in one skill)
- Quick exit check (avoid regenerating recent files)
- Graph-ready JSON with stable IDs for cross-referencing
- Summary block for dashboard integration

**Not included** (vs full prod-personas + prod-jobs-to-be-done + prod-user-stories):
- Separate skills for each phase
- Deep competitive persona analysis
- Extensive journey mapping workshops
- Comprehensive edge case scenarios

**Philosophy**: Capture enough to start building, not exhaustive research. The JSON format ensures data is machine-readable and graph-traversable from day one.

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
- `.shipkit/why.json` - Understand project vision
- `.shipkit/stack.json` - Understand technical constraints

---

## Context Files This Skill Writes

**Write Strategy: OVERWRITE**

**Creates/Updates**:
- `.shipkit/product-discovery.json` - Graph-ready JSON artifact with personas, pain points, journeys, and opportunities

**Archive location** (if replacing):
- `.shipkit/archive/product-discovery/product-discovery.[timestamp].json`

---

## Lazy Loading Behavior

**This skill loads context ON DEMAND**:

1. User invokes `/shipkit-product-discovery`
2. Check if file exists (Quick Exit Check)
3. If regenerating: Ask 2 questions
4. Read why.json, stack.json (~1000 tokens)
5. Generate Product Discovery JSON artifact
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

Product Discovery JSON artifact is complete when:
- [ ] 1-3 personas with stable IDs, clear goals, and context
- [ ] Each persona has distinct characteristics (`isPrimary` set on exactly one)
- [ ] Pain points extracted with severity levels and persona cross-references
- [ ] User journeys include emotion tracking at each step
- [ ] Journey steps reference pain point IDs where friction occurs
- [ ] Opportunities link to both pain points and personas they address
- [ ] Summary counts match actual array lengths
- [ ] All ID cross-references are valid (no dangling references)
- [ ] File saved to `.shipkit/product-discovery.json`
<!-- /SECTION:success-criteria -->
---

**Remember**: This file is your single source of truth for user understanding. Update it as you learn more about users. Product discovery is iterative; refine as insights emerge. The JSON format with stable IDs enables other skills and dashboards to traverse persona-pain-journey-opportunity relationships as a graph.