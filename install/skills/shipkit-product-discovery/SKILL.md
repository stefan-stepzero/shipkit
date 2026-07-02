---
name: shipkit-product-discovery
description: "Use when defining users, personas, or user journeys. Triggers: 'who are users', 'create personas', 'user research', 'user stories'."
argument-hint: "[persona or journey]"
context: fork
agent: shipkit-product-owner-agent
effort: medium
---

# shipkit-product-discovery - Lightweight Product Discovery

**Purpose**: Combines personas, user journey mapping, and user stories into a single lightweight workflow for POC/MVP projects

**Protocol:** This skill follows the canonical elicitation protocol defined in `install/shared/references/elicitation-protocol.md` (the *mechanics* — marker, state files, resume). The steps below are this skill's specific application of that protocol.

**Calibration:** Apply `install/shared/references/ground-or-ask-calibration.md` (the *intelligence* — propose vs ask). **Ground first:** scan cited signals (the opening prompt, `why.json`, `README.md`, `package.json`, the codebase) before asking anything. Propose every field you can tie to a signal, tagged with its source; flag low-leverage guesses as `guessed`. **High-leverage for this skill:** who the PRIMARY personas are and their core journeys / top user needs — these define who the product is FOR and are hard to reverse. If ungrounded, ask. **Low-leverage:** secondary personas, edge-case journeys, ordering details — propose flagged defaults, don't ask. Target 2–3 questions maximum; if you're about to ask more, your grounding pass was too shallow. Never silently invent an ungrounded primary persona or core need.

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

> **Fork context — no user prompts.** You are dispatched in a fork and have no user channel. Skip the file-exists menu entirely.

1. Check if `.shipkit/product-discovery.json` exists
2. If exists: read `.shipkit/reviews/direction-assessment.json` if present. If the latest review lists a gap against this artifact, archive the existing file to `.shipkit/.archive/product-discovery.YYYY-MM-DD.json` and regenerate addressing the gap. Otherwise, read the existing file and exit early with a "no changes needed" report — the reviewer already accepted it.
3. If no file exists: proceed to Step 0b (propose mode).

---

### Step 0b: Grounding Pass (Context-Driven Propose)

**Grounding pass — run before generating any question or artifact:**

1. Read cited signals in order: `why.json` (`targetUsers`, `problem`, `vision`), `README.md` (audience, problem, value prop), `package.json` (name, description, keywords), the opening prompt / any argument provided.
2. For each field the artifact needs, classify:
   - **Grounded** → propose with `source: <signal>` tag (e.g. `"source": "why.json §targetUsers"`). Do not ask.
   - **Ungrounded + high-leverage** (who the primary personas are, their core journeys, their top needs) → add to candidate questions. These are hard to reverse.
   - **Ungrounded + low-leverage** (secondary persona details, edge journeys) → propose with `"guessed": true`. Do not ask.
3. **Decision gate:**
   - **Primary persona(s) grounded** (at least one persona and their core need are supported by a signal) → proceed to write the artifact (Step 3). Do not pause; propose secondary personas as `guessed` defaults. The orchestrator's review cycle catches gaps.
   - **Primary persona(s) ungrounded** (no signal identifies who the product is for) → you cannot safely proceed. Follow the **Elicitation Path** below.

---

### Elicitation Path (Fork + Ungrounded Primary Persona)

*Only reached when: (a) you are in a fork (check — is `AskUserQuestion` in your available tools? If not, you are in a fork), AND (b) the primary persona is ungrounded after the grounding pass.*

**Do not invent a persona. Do not write `product-discovery.json`. Follow this path exactly:**

**Write `.shipkit/elicitation/product-discovery/questions.md`** — overwrite with:
```
---
skill: shipkit-product-discovery
turn: 1
last_updated: <ISO 8601 UTC>
---

## Turn 1

1. Who are the primary users of this product? (roles, types, or a short description) (field: `personas[].name/role`)
2. What is the core thing each primary user is trying to accomplish — their main goal or job-to-be-done? (field: `personas[].primaryIntent`)
3. What is their biggest frustration or pain point with how they do this today? (field: `painPoints`)
```

Limit to 3 questions (the high-leverage set). Do not ask about secondary personas or edge journeys here.

**Write `.shipkit/elicitation/product-discovery/progress.json`** — create or update:
```json
{
  "skill": "shipkit-product-discovery",
  "status": "in_progress",
  "elicitation_turn": 1,
  "started_at": "<ISO 8601 UTC>",
  "last_updated_at": "<ISO 8601 UTC>",
  "completed_at": null,
  "last_elicited_at": "<ISO 8601 UTC>",
  "total_questions_planned": 3,
  "questions_answered": 0,
  "confidence": "low"
}
```

**Do NOT write `answers.md` if it already contains real answers.** Create an empty file with only the frontmatter header if the file does not yet exist.

**Emit the marker as the FINAL line of your output:**
```
NEEDS_ELICITATION:shipkit-product-discovery
status=paused
turn=1
questions_file=.shipkit/elicitation/product-discovery/questions.md
reason=primary persona ungrounded — awaiting user answers for turn 1
```

Return immediately. Do not synthesize anything. Do not continue past this point.

---

### Step 1: Gather Context About Users and Goals (Inline Mode Only)

**Only run this step when `AskUserQuestion` IS in your available tools** (you are running inline in the main session, not in a fork). If you are in a fork and the primary persona is ungrounded, use the Elicitation Path above instead.

**Check for pre-populated answers first.** Read `.shipkit/elicitation/product-discovery/answers.md`. If it contains real answers for the primary persona fields, skip the questions below and proceed to Step 3 using those answers.

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

**Question 2 - User Type:** (if not provided in argument or signals)
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
1. **Personas** (1-3 lightweight personas with IDs, primary intent, and cross-referencing)
2. **Pain Points** (extracted from personas, linked by ID)
3. **User Journeys** (step-by-step with emotion tracking and pain point references)
4. **Opportunities** (linked to pain points and personas)

**Multi-user apps**: When the product serves distinct user types (e.g., teachers + students, buyers + sellers), each persona MUST have a distinct `primaryIntent` that captures their core motivation. This ensures downstream skills (product-definition, engineering-definition, goals, spec) can map features, mechanisms, and criteria to specific user intents.

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
  "personas": [{ "id", "name", "role", "primaryIntent", "goals", "frustrations", "techComfort", "context", "isPrimary" }],
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

## When This Skill Integrates with Others

### Before shipkit-product-discovery
- `/shipkit-why-project` - Defines vision context (optional but recommended)
- `/shipkit-project-context` - Scans technical stack (optional)

### After shipkit-product-discovery
- `/shipkit-spec` - Creates detailed specifications from user stories
- `/shipkit-plan` - Creates implementation plan

---

## Context Files This Skill Reads

**Optional** (read if exist):
- `.shipkit/why.json` - Understand project vision
- `.shipkit/stack.json` - Understand technical constraints

---

## Context Files This Skill Writes

**Artifact strategy: replace** — Overwrites the existing artifact file. Previous content is not preserved.

**Write Strategy: OVERWRITE**

**Creates/Updates**:
- `.shipkit/product-discovery.json` - Graph-ready JSON artifact with personas, pain points, journeys, and opportunities

**Archive location** (if replacing):
- `.shipkit/archive/product-discovery/product-discovery.[timestamp].json`

**Elicitation state** (persists as audit trail; run-scoped when under the orchestration engine):
- `.shipkit/elicitation/product-discovery/questions.md` — current turn's questions
- `.shipkit/elicitation/product-discovery/answers.md` — accumulated Q&A across turns
- `.shipkit/elicitation/product-discovery/progress.json` — turn state + timestamps

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

**If `NEEDS_ELICITATION:shipkit-product-discovery` was emitted:** The skill paused without writing `product-discovery.json`. The main session should run `/shipkit-product-discovery` inline (where `AskUserQuestion` is available), answer the questions in `.shipkit/elicitation/product-discovery/questions.md`, then re-invoke the original skill or orchestrator to resume. See `install/shared/references/elicitation-protocol.md` for full handling instructions.

**Natural capabilities** (no skill needed): Implementation, debugging, testing, refactoring, code documentation.

**Suggest skill when:** User needs to make decisions, create persistence, or check project status.
<!-- /SECTION:after-completion -->

<!-- SECTION:success-criteria -->
## Success Criteria

Product Discovery JSON artifact is complete when:
- [ ] 1-3 personas with stable IDs, clear goals, and context
- [ ] Each persona has distinct characteristics (`isPrimary` set on exactly one)
- [ ] Every proposed value is tagged with `source: <signal>` (grounded) or `guessed: true` (low-leverage default) — no silent untagged guesses
- [ ] Pain points extracted with severity levels and persona cross-references
- [ ] User journeys include emotion tracking at each step
- [ ] Journey steps reference pain point IDs where friction occurs
- [ ] Opportunities link to both pain points and personas they address
- [ ] Summary counts match actual array lengths
- [ ] All ID cross-references are valid (no dangling references)
- [ ] File saved to `.shipkit/product-discovery.json`
- [ ] If marker emitted: `NEEDS_ELICITATION:shipkit-product-discovery` is the final output line; `product-discovery.json` was NOT written; primary persona was genuinely ungrounded
<!-- /SECTION:success-criteria -->
---

**Remember**: This file is your single source of truth for user understanding. Update it as you learn more about users. Product discovery is iterative; refine as insights emerge. The JSON format with stable IDs enables other skills and dashboards to traverse persona-pain-journey-opportunity relationships as a graph.
