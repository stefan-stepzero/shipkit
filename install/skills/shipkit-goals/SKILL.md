---
name: shipkit-goals
description: "Capture structured project goals that bridge why.json vision to concrete specs. Triggers: 'set goals', 'project goals', 'objectives', 'priorities'."
argument-hint: "[goal topic]"
agent: shipkit-product-owner-agent
---

# shipkit-goals - Project Goals & Objectives

**Purpose**: Capture structured, trackable project goals that bridge `.shipkit/why.json` vision to concrete specs — with priorities, status, and success criteria.

**What it does**: Proposes stage-appropriate goals based on project context, lets user validate and customize, then generates `.shipkit/goals.json` with structured goals that persist across sessions and feed into mission control.

**Philosophy**: Goals are 80% predictable from project stage and type. This skill does the grunt work — proposing smart defaults across Technical, Product/UX, Growth, and Operational lenses — so users validate rather than create from scratch.

**Output format**: JSON — readable by Claude, renderable by mission control dashboard, and the single source of truth for project goals.

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

| File | Required? | Provides | If Missing |
|------|-----------|----------|------------|
| `.shipkit/why.json` | **Yes** | `currentState` (stage), vision, problem | Route to `/shipkit-why-project` |
| `.shipkit/codebase-index.json` | Recommended | `concepts`, `recentlyActive`, framework | Suggest `/shipkit-codebase-index` or proceed with generic stage goals |
| `.shipkit/stack.json` | Optional | Tech context for feasibility | Use framework from codebase-index |

**Why these matter**: Goals are proposed based on current stage (from why.json) and detected capabilities (from codebase-index). Without context, goals are generic.

---

## Process

### Step 0: Check for Existing File

```markdown
1. Check if `.shipkit/goals.json` exists

2. If exists AND modified < 5 minutes ago:
   - Show user: "Found recent goals (modified X ago)"
   - Ask: "Use these or regenerate?"
   - If "use these" → Exit early (save tokens)
   - If "regenerate" → Proceed to Step 1

3. If exists AND modified > 5 minutes ago:
   - Read and display current goals as a formatted summary
   - Ask: "View/Update/Replace/Cancel?"

4. If doesn't exist:
   - Skip to Step 1 (generate new)
```

**If Update:**
- Read existing goals.json
- Ask: "What should change? (new goals, reprioritize, mark achieved, etc.)"
- Regenerate incorporating updates

**If Replace:**
- Archive current: copy to `.shipkit/.archive/goals.YYYY-MM-DD.json`
- Proceed to Step 1

---

### Step 1: Gather Context

**Read these files:**

```
.shipkit/why.json           → currentState, vision, problem (REQUIRED)
.shipkit/codebase-index.json → concepts, framework, recentlyActive (RECOMMENDED)
.shipkit/stack.json          → tech context (OPTIONAL)
```

**If why.json missing**: Route to `/shipkit-why-project` first.

**If codebase-index.json missing**:
- Suggest: "For better goal proposals, run `/shipkit-codebase-index` first. Or continue with stage-based goals?"
- If user continues → use generic stage goals without concept modifiers

---

### Step 2: Determine Stage and Select Templates

**Map currentState to stage** (see `references/goal-templates.md`):

| why.json `currentState` | Stage | Next Stage |
|------------------------|-------|------------|
| "starting", "idea", "POC" | POC | → MVP |
| "MVP", "alpha", "prototype" | MVP | → Production |
| "beta", "production", "live" | Production | → Scale |
| "growth", "scale", "enterprise" | Scale | → Enterprise |

**Select goal templates** from `references/goal-templates.md`:
1. Pull goals for current → next stage transition
2. Apply concept modifiers based on `codebase-index.json`:
   - If `concepts.auth` → add auth-hardening goals
   - If `concepts.payments` → add payment-readiness goals
   - If `concepts.database` → add data integrity goals
3. Adjust lens weights based on project type (SaaS, CLI, library, API)

---

### Step 3: Propose Goals for Validation

**Present proposed goals organized by lens:**

```
Based on your project:
  Stage: MVP → Production
  Vision: "{from why.json}"
  Detected: auth, payments, database

Proposed goals:

TECHNICAL (P0):
  □ Auth hardened (session expiry, rate limiting)
  □ Error recovery exists (retry logic, graceful degradation)
  □ CI/CD pipeline operational

PRODUCT/UX (P0):
  □ Onboarding flow complete
  □ Error messages are actionable

PAYMENTS (P1 - detected):
  □ Webhook signature verification
  □ Failed payment handling

OPERATIONAL (P1):
  □ User-facing documentation
  □ Error logging with context

Accept these? Or:
  - Add: "I also need X"
  - Remove: "Skip the payments goals"
  - Reprioritize: "Make onboarding P0"
  - Custom: "Replace with my own list"
```

**Why propose first**: 80% of goals are predictable from stage + concepts. User validates rather than creates from scratch. This captures human priorities while reducing cognitive load.

**If user modifies**: Incorporate changes. Re-present if major changes.

**If user wants fully custom**: Fall back to asking open-ended questions (legacy mode).

---

### Step 4: Generate Goals JSON

**Create file using Write tool**: `.shipkit/goals.json`

The output MUST conform to the schema below. This is a strict contract — mission control and other skills depend on this structure.

---

## JSON Schema

**Full schema reference**: See `references/output-schema.md`
**Example output**: See `references/example.json`

### Quick Reference

```json
{
  "$schema": "shipkit-artifact",
  "type": "goals",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DD",
  "source": "shipkit-goals",
  "summary": { "total": N, "byPriority": {...}, "byStatus": {...} },
  "goals": [
    {
      "id": "goal-slug",
      "name": "Goal Name",
      "priority": "p0|p1|p2",
      "status": "not-started|in-progress|achieved|deferred",
      "objective": "What we're trying to achieve",
      "successCriteria": ["Criterion 1", "Criterion 2"],
      "linkedSpecs": ["specs/active/feature.json"],
      "notes": "Optional"
    }
  ]
}
```

**Key fields**: `id` (kebab-case slug), `priority` (p0/p1/p2), `status` (tracking), `successCriteria` (measurable).

**Summary**: Recompute `summary` counts every time the file is written.

---

### Step 5: Save and Suggest Next Step

**Use Write tool to create/overwrite**: `.shipkit/goals.json`

**Output to user** (formatted summary, not raw JSON):
```
Goals saved.

Location: .shipkit/goals.json

  P0 (must have): 2 goals
  P1 (should have): 2 goals
  P2 (nice to have): 1 goal

  Status: 2 not started, 2 in progress, 1 achieved

Next steps:
  1. /shipkit-spec - Create specs for your P0 goals
  2. /shipkit-plan - Plan implementation for an existing spec
  3. /shipkit-project-status - See overall project health

Ready to spec your top-priority goal?
```

---

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

| File | Purpose | If Missing |
|------|---------|------------|
| `.shipkit/why.json` | `currentState` determines stage, vision grounds proposals | Route to `/shipkit-why-project` |
| `.shipkit/codebase-index.json` | `concepts` trigger domain-specific goals | Suggest running it, or use generic goals |
| `.shipkit/stack.json` | Tech context for feasibility | Use framework from codebase-index |
| `.shipkit/specs/active/*.json` | Link goals to existing specs | Goals stand alone |

**Template reference**: `references/goal-templates.md` — stage definitions, goal templates by lens, concept modifiers.

---

## Context Files This Skill Writes

**Write Strategy: OVERWRITE**

**Creates/Updates**:
- `.shipkit/goals.json` - Structured project goals (JSON artifact)

**Update Behavior**:
- File exists → File Exists Workflow (view/update/replace/cancel)
- Recent file (< 5 min) → Quick Exit Check (use or regenerate)
- Replace → Archive old version first
- Update → Read existing, incorporate changes
- Each write REPLACES entire file contents

**Archive location** (if replacing):
- `.shipkit/.archive/goals.YYYY-MM-DD.json`

---

## Success Criteria

- [ ] Stage determined from why.json `currentState`
- [ ] Goal templates selected from `references/goal-templates.md`
- [ ] Concept modifiers applied based on codebase-index (if available)
- [ ] Goals proposed to user across relevant lenses (Technical, Product/UX, Growth, Operational)
- [ ] User validated/customized proposed goals
- [ ] Goals are structured with priority levels (P0/P1/P2)
- [ ] Each goal has measurable success criteria
- [ ] Output conforms to JSON schema
- [ ] Summary field is accurate
- [ ] File saved to `.shipkit/goals.json`
- [ ] Old version archived (if replaced)

---

## Common Scenarios

### Scenario 1: New Project with Context

```
User: "Set goals for this project"

Claude:
1. Check .shipkit/goals.json (doesn't exist)
2. Read .shipkit/why.json → currentState: "MVP"
3. Read .shipkit/codebase-index.json → concepts: auth, payments, database
4. Determine: MVP → Production transition
5. Select templates from goal-templates.md, apply concept modifiers
6. Propose:
   "Based on MVP → Production with auth, payments, database detected:

   TECHNICAL (P0): Auth hardened, Error recovery, CI/CD
   PRODUCT/UX (P0): Onboarding flow, Actionable errors
   PAYMENTS (P1): Webhook verification, Failed payment handling
   OPERATIONAL (P1): User docs, Error logging

   Accept these? Or add/remove/reprioritize?"

7. User: "Accept, but make onboarding P0"
8. Adjust, generate goals.json, save
```

### Scenario 2: New Project without Codebase Index

```
User: "Set goals"

Claude:
1. Read .shipkit/why.json → currentState: "POC"
2. Check .shipkit/codebase-index.json (doesn't exist)
3. Suggest: "For better goal proposals, run /shipkit-codebase-index first.
   Or continue with stage-based goals?"
   User: "Continue"
4. Use generic POC → MVP templates (no concept modifiers)
5. Propose goals, user validates
```

### Scenario 3: Update Goals (File Exists)

```
User: "Update our goals"

Claude:
1. Check .shipkit/goals.json (exists, modified 2 days ago)
2. Read and display formatted summary
3. Ask: "View/Update/Replace/Cancel?"
   User: "Update"
4. Ask: "What should change?"
   User: "We achieved the MVP goal, and I want to add onboarding"
5. Move MVP status to "achieved", add onboarding goal from templates
6. Recompute summary counts
7. Overwrite .shipkit/goals.json
```

### Scenario 4: Quick Exit (Recent File)

```
User: "Show me our goals"

Claude:
1. Check .shipkit/goals.json (exists, modified 2 minutes ago)
2. Show: "Found recent goals (2 min ago). Use these or regenerate?"
   User: "Use these"
3. Read JSON, display formatted summary, exit
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

**Remember**: Goals are 80% predictable from stage + detected capabilities. Propose smart defaults, let users validate. The skill does the grunt work — users make the final call on priorities. Update goals as the project evolves.
