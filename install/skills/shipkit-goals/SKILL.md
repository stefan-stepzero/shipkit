---
name: shipkit-goals
description: "Derive measurable success criteria from the solution blueprint. Triggers: 'success criteria', 'how do we measure', 'goals', 'stage gates'."
argument-hint: "[goal topic or criteria focus]"
agent: shipkit-product-owner-agent
---

# shipkit-goals — Success Criteria & Stage Gates

**Purpose**: Derive measurable success criteria from the solution blueprint (product-definition.json). Each mechanism, UX pattern, and differentiator implies criteria for "how do we know this works?" — this skill makes those criteria explicit, measurable, and trackable.

**What it does**: Reads the solution blueprint and discovered user needs, proposes success criteria with measurable thresholds and verification methods, lets user validate and customize, then generates `.shipkit/goals.json` with structured criteria that serve as stage gates for execution.

**Philosophy**: Success criteria are derivable from the solution design. Each mechanism implies performance and quality criteria. Each UX pattern implies usability criteria. Each differentiator implies validation criteria. This skill does the derivation — users validate thresholds and add business metrics.

**Output format**: JSON — readable by Claude, machine-readable by other tools, and the source of truth for what "done" means.

---

## When to Invoke

**User triggers**:
- "Define success criteria", "How do we measure success?"
- "Set goals", "What are our goals?"
- "Stage gates", "Launch criteria"
- "When is this done?"

**Workflow position**:
- After `/shipkit-product-definition` (reads the solution blueprint)
- Before `/shipkit-spec` — criteria inform feature specifications
- Before `/shipkit-verify` — criteria become verification checks

---

## Prerequisites

| File | Required? | Provides | If Missing |
|------|-----------|----------|------------|
| `.shipkit/product-definition.json` | **Yes** | Mechanisms, patterns, differentiators, MVP boundary | Route to `/shipkit-product-definition` |
| `.shipkit/product-discovery.json` | Recommended | Pain points for traceability | Proceed without traceability |
| `.shipkit/why.json` | Recommended | Stage context (POC/MVP/Production/Scale) | Ask user for stage |

---

## Process

### Step 0: Check for Existing File

1. Check if `.shipkit/goals.json` exists
2. If exists AND modified < 5 minutes ago: Show user, ask "Use these or regenerate?"
3. If exists AND modified > 5 minutes ago: Read and display summary, ask "View/Update/Replace/Cancel?"
4. If doesn't exist: Skip to Step 1

**If Update:**
- Read existing goals.json
- Ask: "What should change? (add criteria, adjust thresholds, mark achieved, etc.)"
- Regenerate incorporating updates

**If Replace:**
- Archive current: copy to `.shipkit/.archive/goals.YYYY-MM-DD.json`
- Proceed to Step 1

---

### Step 1: Load Context

**Read these files:**

```
.shipkit/product-definition.json  → mechanisms, patterns, differentiators, MVP boundary (REQUIRED)
.shipkit/product-discovery.json   → pain points for traceability (RECOMMENDED)
.shipkit/why.json                 → project stage (RECOMMENDED)
```

**If product-definition.json missing**: Route to `/shipkit-product-definition` first.

---

### Step 2: Determine Stage and Criteria Complexity

Read stage from `product-definition.json` (product.stage) or `why.json`:

| Stage | Criteria Complexity | Focus |
|-------|-------------------|-------|
| POC | Basic: "it works" checks | Functional completeness |
| MVP | Moderate: user outcome thresholds | Usability + core performance |
| Production | Full: performance + reliability gates | Reliability + scalability |
| Scale | Comprehensive: business metrics + SLAs | Growth + operational excellence |

---

### Step 3: Derive Criteria from Solution Blueprint

For each section of product-definition.json, derive criteria:

**From mechanisms:**
- Performance criteria (how fast?)
- Reliability criteria (how often does it work?)
- Quality criteria (how good is the output?)

**From UX patterns:**
- Usability criteria (can users complete the flow?)
- Completion rate criteria (what % finish?)
- Responsiveness criteria (how fast does it feel?)

**From differentiators:**
- Validation criteria (does it actually differentiate?)
- User perception criteria (do users notice/value it?)

**From MVP boundary:**
- Completeness gate (are all MVP items functional?)
- Integration gate (do MVP features work together?)

See `references/derivation-patterns.md` for detailed derivation examples.

---

### Step 4: Propose Criteria for Validation

**Present proposed criteria grouped by category:**

```
Based on your solution blueprint:

USER OUTCOMES:
  □ Worksheet completion: Teacher creates worksheet in < 2 minutes
    Threshold: 80% of users complete in < 2 min
    Verify: analytics (time-to-complete tracking)
    Derived from: P-001 (Wizard Flow)

  □ Content quality: Generated questions are grade-appropriate
    Threshold: 90%+ accuracy on manual review sample
    Verify: manual-check (teacher review of 20 samples)
    Derived from: M-001 (LLM Generation Chain)

TECHNICAL PERFORMANCE:
  □ Generation speed: Worksheet generates within acceptable time
    Threshold: < 5 seconds for streaming first content
    Verify: automated-test (load test with timer)
    Derived from: M-001 (LLM Generation Chain)

BUSINESS METRICS:
  □ Return usage: Teachers come back to create more
    Threshold: 40%+ 7-day return rate
    Verify: analytics (cohort tracking)
    Derived from: D-003 (Real-time preview)

Accept these? Or:
  - Add: "I also want to track X"
  - Remove: "Skip the return rate metric for now"
  - Adjust threshold: "Make generation speed < 3 seconds"
  - Custom: "Replace with my own criteria"
```

**If user modifies**: Incorporate changes. Re-present if major changes.

---

### Step 5: Define Stage Gates

Group confirmed criteria into named gates:

```
STAGE GATES:

MVP Launch Ready (all must pass):
  - criterion-worksheet-completion
  - criterion-generation-speed
  - criterion-content-quality
  - criterion-mvp-completeness

Beta Ready (MVP Launch + these):
  - criterion-return-usage
  - criterion-differentiation-validation
```

Ask user to confirm gate composition.

---

### Step 6: Generate Goals JSON

After confirmation, write `.shipkit/goals.json`.

See [Goals JSON Schema](#goals-json-schema) below.

---

### Step 7: Save and Suggest Next Steps

```
Success criteria saved to .shipkit/goals.json

  Criteria: {N} total
    User outcomes: {N}
    Technical performance: {N}
    Business metrics: {N}

  Gates: {N}
    MVP Launch Ready: {N} criteria
    {Other gates}: {N} criteria each

  Status: {N} not-measured

Next:
  1. /shipkit-spec — Create specs for MVP features (criteria inform acceptance tests)
  2. /shipkit-plan — Plan implementation
  3. /shipkit-verify — Check criteria status after building

Ready to start speccing?
```

---

## Goals JSON Schema (Quick Reference)

```json
{
  "$schema": "shipkit-artifact",
  "type": "goals",
  "version": "2.0",
  "lastUpdated": "YYYY-MM-DDTHH:MM:SSZ",
  "source": "shipkit-goals",

  "stage": {
    "current": "mvp",
    "target": "production"
  },

  "derivedFrom": {
    "productDefinition": ".shipkit/product-definition.json",
    "productDiscovery": ".shipkit/product-discovery.json"
  },

  "criteria": [
    {
      "id": "criterion-slug",
      "name": "Human-readable name",
      "category": "user-outcome|technical-performance|business-metric",
      "metric": "What to measure",
      "threshold": "Target value (e.g., '> 80%', '< 3 seconds')",
      "currentValue": null,
      "verificationMethod": "manual-check|analytics|automated-test|user-feedback",
      "gate": "gate-slug",
      "status": "not-measured|below-threshold|at-threshold|exceeded",
      "derivedFrom": {
        "type": "mechanism|pattern|differentiator|mvpBoundary",
        "id": "M-001"
      },
      "painPointAddressed": "pain-1",
      "notes": "Optional context"
    }
  ],

  "gates": [
    {
      "id": "gate-slug",
      "name": "Gate name",
      "description": "What passing this gate means",
      "criteria": ["criterion-slug-1", "criterion-slug-2"],
      "status": "blocked|partial|passed",
      "passedAt": null
    }
  ],

  "summary": {
    "totalCriteria": 0,
    "byCategory": { "user-outcome": 0, "technical-performance": 0, "business-metric": 0 },
    "byStatus": { "not-measured": 0, "below-threshold": 0, "at-threshold": 0, "exceeded": 0 },
    "totalGates": 0,
    "gatesPassed": 0
  }
}
```

**Full schema reference**: See `references/output-schema.md`
**Derivation patterns**: See `references/derivation-patterns.md`
**Realistic example**: See `references/example.json`

---

## When This Skill Integrates with Others

### Before This Skill
- `/shipkit-product-definition` — Produces the solution blueprint (required)
- `/shipkit-product-discovery` — Produces user needs for traceability (recommended)
- `/shipkit-why-project` — Provides stage context (recommended)

### After This Skill
- `/shipkit-spec` — Criteria inform acceptance tests within feature specs
- `/shipkit-plan` — Plans can reference criteria for verification steps (future integration)
- `/shipkit-verify` — Can reference criteria when checking implementation quality (future integration)
- `/shipkit-project-status` — Displays criteria and gate status

### When This Skill Runs Again
- File exists workflow activates
- User can view/update/replace existing criteria
- Common updates: adjust thresholds, mark criteria as measured, add new criteria

---

## Context Files This Skill Reads

| File | Purpose | If Missing |
|------|---------|------------|
| `.shipkit/product-definition.json` | Solution blueprint — derive criteria from | Route to `/shipkit-product-definition` |
| `.shipkit/product-discovery.json` | Pain points for traceability | Proceed without traceability |
| `.shipkit/why.json` | Project stage for criteria complexity | Ask user for stage |

---

## Context Files This Skill Writes

**Write Strategy: OVERWRITE**

**Creates/Updates**:
- `.shipkit/goals.json` — Structured success criteria (JSON artifact)

**Archive location** (if replacing):
- `.shipkit/.archive/goals.YYYY-MM-DD.json`

---

<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Has important context been saved to `.shipkit/`?
2. **Prerequisites** - Does the next action need a spec or plan first?
3. **Session length** - Long session? Consider `/shipkit-work-memory` for continuity.

**Natural capabilities** (no skill needed): Implementation, debugging, testing, refactoring, code documentation.

**Suggest skill when:** User needs to create specs (`/shipkit-spec`), plan implementation (`/shipkit-plan`), or verify criteria (`/shipkit-verify`).
<!-- /SECTION:after-completion -->

<!-- SECTION:success-criteria -->
## Success Criteria

Goals artifact is complete when:
- [ ] Product-definition.json read and mechanisms/patterns/differentiators extracted
- [ ] Criteria derived from each mechanism (performance + quality + reliability)
- [ ] Criteria derived from each UX pattern (usability + completion rate)
- [ ] Criteria derived from differentiators (validation)
- [ ] Each criterion has measurable threshold (not vague)
- [ ] Each criterion has verification method (how to measure)
- [ ] Criteria grouped into stage gates
- [ ] User confirmed criteria and thresholds
- [ ] Gate composition confirmed
- [ ] derivedFrom traceability links are valid
- [ ] Summary counts match actual array lengths
- [ ] File saved to `.shipkit/goals.json`
<!-- /SECTION:success-criteria -->

---

**Remember**: Success criteria are the acceptance tests for your product. They answer "how do we know this works?" for every mechanism, pattern, and differentiator in the solution blueprint. Update them as the solution evolves. Gate status drives execution — keep building until gates pass.
