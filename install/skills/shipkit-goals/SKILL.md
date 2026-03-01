---
name: shipkit-goals
description: "Derive measurable success criteria split across strategic, product, and engineering goal files. Evaluate goals against metrics. Triggers: 'success criteria', 'how do we measure', 'goals', 'stage gates', 'evaluate goals', 'check metrics'."
argument-hint: "[goal topic | --evaluate | set stage]"
context: fork
agent: shipkit-product-owner-agent
---

# shipkit-goals — Success Criteria & Stage Gates

**Purpose**: Derive measurable success criteria from the product and engineering blueprints, split across three goal files owned by different agents. Each feature, mechanism, UX pattern, and differentiator implies criteria for "how do we know this works?" — this skill makes those criteria explicit, measurable, and trackable.

**What it does**: Reads blueprints, proposes success criteria categorized by owner (strategic/product/engineering), lets user validate, then generates three goal files. Also supports evaluation mode that compares actuals from metrics to targets.

**Output**: Three JSON files in `.shipkit/goals/`:
- `goals/strategic.json` — Business-metric criteria + stage + constraints (Visionary owns)
- `goals/product.json` — User-outcome criteria (PM owns)
- `goals/engineering.json` — Technical-performance criteria (EM owns)

---

## Modes

| Mode | Trigger | What It Does |
|------|---------|-------------|
| **Define** (default) | "Set goals", "success criteria" | Derive criteria from blueprints, write 3 goal files |
| **Evaluate** | `--evaluate`, "check metrics" | Read metrics/latest.json, compare to targets, output gap report |
| **Set Stage** | "set stage" | Set project stage in goals/strategic.json |

---

## When to Invoke

**User triggers**:
- "Define success criteria", "How do we measure success?"
- "Set goals", "What are our goals?"
- "Stage gates", "Launch criteria"
- "When is this done?"
- "Evaluate goals", "Check metrics", "How are we doing?"
- "Set stage to MVP"

**Workflow position**:
- After `/shipkit-engineering-definition` (reads both product + engineering blueprints)
- Before `/shipkit-spec` — criteria inform feature specifications
- Before `/shipkit-verify` — criteria become verification checks
- During feedback loop — evaluation mode checks actuals vs targets

---

## Prerequisites

| File | Required? | Mode | Provides | If Missing |
|------|-----------|------|----------|------------|
| `.shipkit/product-definition.json` | **Yes** | Define | Features, patterns, differentiators | Route to `/shipkit-product-definition` |
| `.shipkit/engineering-definition.json` | **Yes** | Define | Mechanisms, components, design decisions | Route to `/shipkit-engineering-definition` |
| `.shipkit/product-discovery.json` | Recommended | Define | Pain points for traceability | Proceed without traceability |
| `.shipkit/why.json` | Recommended | Define | Stage context | Ask user for stage |
| `.shipkit/goals/*.json` | **Yes** | Evaluate | Current targets | Route to Define mode first |
| `.shipkit/metrics/latest.json` | **Yes** | Evaluate | Current actuals | Report "no metrics available" |

---

## Output Files

| File | Owner Agent | Criteria Category | Contains |
|------|------------|-------------------|----------|
| `goals/strategic.json` | Visionary | `business-metric` | Revenue, cost, DAU/MAU, retention, market metrics + **stage** + **constraints** |
| `goals/product.json` | PM | `user-outcome` | Completion rates, UX quality, satisfaction, content quality |
| `goals/engineering.json` | EM | `technical-performance` | Response times, uptime, test coverage, build health |

---

## Process — Define Mode

### Step 0: Check for Existing Files

1. Check if `.shipkit/goals/` directory exists with any of the 3 files
2. If exists AND modified < 5 minutes ago: Show user, ask "Use these or regenerate?"
3. If exists AND modified > 5 minutes ago: Read and display summary, ask "View/Update/Replace/Cancel?"
4. If doesn't exist: Check for legacy `.shipkit/goals.json` — offer migration (see Migration section)
5. If nothing exists: Skip to Step 1

**If Update:**
- Read existing goal files
- Ask: "What should change? (add criteria, adjust thresholds, mark achieved, etc.)"
- Regenerate incorporating updates

**If Replace:**
- Archive current files to `.shipkit/.archive/goals-{type}.YYYY-MM-DD.json`
- Proceed to Step 1

---

### Step 1: Load Context

**Read these files:**

```
.shipkit/product-definition.json      → features, patterns, differentiators (REQUIRED)
.shipkit/engineering-definition.json  → mechanisms, components, design decisions (REQUIRED)
.shipkit/product-discovery.json       → pain points for traceability (RECOMMENDED)
.shipkit/why.json                     → project stage (RECOMMENDED)
```

**If product-definition.json missing**: Route to `/shipkit-product-definition` first.
**If engineering-definition.json missing**: Route to `/shipkit-engineering-definition` first.

---

### Step 2: Determine Stage and Constraints

Read stage from `product-definition.json` (product.stage) or `why.json`:

| Stage | Criteria Complexity | Focus | Quality Bar | Scope Limit | Cost Awareness |
|-------|-------------------|-------|-------------|-------------|----------------|
| POC | Basic: "it works" checks | Functional completeness | "Runs without crashing" | Single feature | Free tiers only |
| Alpha | Light: core path thresholds | Core usability + basic perf | "Works for testers" | Core + 1-2 features | Low budget |
| MVP | Moderate: user outcome thresholds | Usability + performance + reliability | "Works for customers" | Feature-complete for launch | Moderate budget |
| Scale | Comprehensive: business metrics + SLAs | Growth + operational excellence | "Works at load" | Full product + ops | Full budget |

---

### Step 3: Derive Criteria from Product + Engineering Blueprints

For each section of product-definition.json and engineering-definition.json, derive criteria and tag with the target file:

**From mechanisms** (engineering-definition.json) → `goals/engineering.json`:
- Performance criteria (how fast?)
- Reliability criteria (how often does it work?)
- Quality criteria (how good is the output?)

**From UX patterns** (product-definition.json) → `goals/product.json`:
- Usability criteria (can users complete the flow?)
- Completion rate criteria (what % finish?)
- Responsiveness criteria (how fast does it feel?)

**From differentiators** (product-definition.json) → `goals/product.json`:
- Validation criteria (does it actually differentiate?)
- User perception criteria (do users notice/value it?)

**From features** (product-definition.json) → `goals/product.json`:
- Completeness gate (are all gate-scoped features functional?)
- Integration gate (do features work together end-to-end?)

**Business metrics** (derived from vision + stage) → `goals/strategic.json`:
- Revenue/cost metrics
- User acquisition (DAU, MAU)
- Retention and churn
- Key business KPIs

See `references/derivation-patterns.md` for detailed derivation examples.

---

### Step 4: Propose Criteria for Validation

**Present proposed criteria grouped by owning agent:**

```
Based on your solution blueprint:

STRATEGIC (Visionary — goals/strategic.json):
  S-001: User acquisition: Active users reach threshold
    Threshold: 100 DAU within 30 days of launch
    Verify: analytics (DAU tracking)

  S-002: Return usage: Users come back
    Threshold: 40%+ 7-day return rate
    Verify: analytics (cohort tracking)

PRODUCT (PM — goals/product.json):
  P-001: Worksheet completion: Teacher creates worksheet quickly
    Threshold: 80% of users complete in < 2 min
    Verify: analytics (time-to-complete)
    Derived from: P-001 (Wizard Flow)

  P-002: Content quality: Generated questions are grade-appropriate
    Threshold: 90%+ accuracy on manual review
    Verify: manual-check (20 samples)
    Derived from: M-001 (LLM Generation Chain)

ENGINEERING (EM — goals/engineering.json):
  E-001: Generation speed: Worksheet generates fast
    Threshold: < 5 seconds for streaming first content
    Verify: automated-test (load test)
    Derived from: M-001 (LLM Generation Chain)

Accept these? Or:
  - Add: "I also want to track X"
  - Remove: "Skip the return rate metric"
  - Adjust: "Make generation speed < 3 seconds"
  - Move: "Move P-002 to engineering"
  - Custom: "Replace with my own criteria"
```

**If user modifies**: Incorporate changes. Re-present if major changes.

---

### Step 5: Define Stage Gates

Group confirmed criteria into named gates. Gates can reference criteria across files:

```
STAGE GATES:

MVP Launch Ready (all must pass):
  - E-001 (engineering) — generation speed
  - P-001 (product) — completion rate
  - P-002 (product) — content quality
  - S-001 (strategic) — minimum users

Beta Ready (MVP Launch + these):
  - S-002 (strategic) — return usage
  - P-003 (product) — differentiation validated
```

Ask user to confirm gate composition.

---

### Step 6: Generate Goal Files

After confirmation, write three files:

1. `.shipkit/goals/strategic.json` — business-metric criteria + stage + constraints
2. `.shipkit/goals/product.json` — user-outcome criteria
3. `.shipkit/goals/engineering.json` — technical-performance criteria

Each file contains only the criteria owned by that agent, plus shared metadata (gates reference criteria across files by ID).

See [Goal File Schemas](#goal-file-schemas) below.

---

### Step 7: Save and Suggest Next Steps

```
Success criteria saved to .shipkit/goals/

  Stage: {stage}

  Strategic (Visionary):  {N} criteria
  Product (PM):           {N} criteria
  Engineering (EM):       {N} criteria
  Total:                  {N} criteria

  Gates: {N}
    MVP Launch Ready: {N} criteria
    {Other gates}: {N} criteria each

  Status: {N} not-measured

Next:
  1. /shipkit-spec — Create specs for features (criteria inform acceptance tests)
  2. /shipkit-plan — Plan implementation
  3. /shipkit-goals --evaluate — Check criteria status after building
```

---

## Process — Evaluate Mode

When invoked with `--evaluate` or "check metrics":

### Step 1: Load Goal Files

Read all three goal files from `.shipkit/goals/`.

### Step 2: Load Metrics

Read `.shipkit/metrics/latest.json` for current actuals.

If missing: Report "No metrics file found. Create `.shipkit/metrics/latest.json` with current measurements to enable evaluation."

### Step 3: Compare Actuals to Targets

For each criterion across all 3 files:
- Match metric key from `metrics/latest.json` to criterion ID
- Compare actual value to threshold
- Update status: `not-measured`, `below-threshold`, `at-threshold`, `exceeded`

### Step 4: Recalculate Gate Status

For each gate:
- Check all referenced criteria (may span multiple files)
- Gate status: `blocked` (any below), `partial` (mixed), `passed` (all at/exceeded)

### Step 5: Output Gap Report

```
GOAL EVALUATION — {date}

Stage: {stage}

STRATEGIC GAPS (→ Visionary):
  ⚠ S-002: Return usage — 25% actual vs 40% target
  ✓ S-001: User acquisition — 150 DAU vs 100 target

PRODUCT GAPS (→ PM):
  ✗ P-001: Completion rate — 60% actual vs 80% target
  ✓ P-002: Content quality — 92% actual vs 90% target

ENGINEERING GAPS (→ EM):
  ✓ E-001: Generation speed — 3.2s actual vs 5s target

GATES:
  MVP Launch Ready: BLOCKED (P-001 below threshold)

RECOMMENDATION:
  Priority gap: P-001 (completion rate) — route to PM for UX revision
```

---

## Process — Set Stage Mode

When invoked with "set stage":

### Step 1: Present Stage Options

Show the stage calibration table and ask user to pick.

### Step 2: Set Constraints

Based on stage, propose quality/scope/cost constraints. Let user adjust.

### Step 3: Write to Strategic Goals

Update `.shipkit/goals/strategic.json` with new stage and constraints.

---

## Migration from Legacy Format

When `.shipkit/goals.json` (single file) exists but `.shipkit/goals/` directory doesn't:

1. Detect legacy format
2. Offer: "Found legacy goals.json. Migrate to 3-file format? (Y/n)"
3. If yes:
   - Read existing criteria
   - Split by `category` field: `business-metric` → strategic, `user-outcome` → product, `technical-performance` → engineering
   - Add stage and constraints to strategic.json (ask user or infer from `why.json`)
   - Write 3 files to `.shipkit/goals/`
   - Archive original: `.shipkit/.archive/goals.YYYY-MM-DD.json`
4. If no: Continue reading legacy format (all criteria in one file)

---

## Goal File Schemas

### goals/strategic.json

```json
{
  "$schema": "shipkit-artifact",
  "type": "goals-strategic",
  "version": "3.0",
  "lastUpdated": "YYYY-MM-DDTHH:MM:SSZ",
  "source": "shipkit-goals",

  "stage": {
    "current": "mvp",
    "target": "scale"
  },

  "constraints": {
    "quality": "production-ready — CI/CD, monitoring, error handling",
    "scope": "feature-complete for launch segment",
    "cost_budget": "moderate — dedicated resources acceptable"
  },

  "derivedFrom": {
    "why": ".shipkit/why.json",
    "productDiscovery": ".shipkit/product-discovery.json"
  },

  "criteria": [
    {
      "id": "S-001",
      "name": "User acquisition",
      "category": "business-metric",
      "metric": "Daily active users",
      "threshold": "> 100 DAU",
      "currentValue": null,
      "verificationMethod": "analytics",
      "gate": "mvp-launch",
      "status": "not-measured",
      "notes": "Track from launch day"
    }
  ],

  "gates": [
    {
      "id": "mvp-launch",
      "name": "MVP Launch Ready",
      "description": "Minimum criteria for public launch",
      "criteria": ["S-001", "P-001", "P-002", "E-001"],
      "status": "blocked",
      "passedAt": null
    }
  ],

  "summary": {
    "totalCriteria": 0,
    "byStatus": { "not-measured": 0, "below-threshold": 0, "at-threshold": 0, "exceeded": 0 }
  }
}
```

### goals/product.json

```json
{
  "$schema": "shipkit-artifact",
  "type": "goals-product",
  "version": "3.0",
  "lastUpdated": "YYYY-MM-DDTHH:MM:SSZ",
  "source": "shipkit-goals",

  "derivedFrom": {
    "productDefinition": ".shipkit/product-definition.json",
    "productDiscovery": ".shipkit/product-discovery.json"
  },

  "criteria": [
    {
      "id": "P-001",
      "name": "Feature completion rate",
      "category": "user-outcome",
      "metric": "% of users completing core flow",
      "threshold": "> 80%",
      "currentValue": null,
      "verificationMethod": "analytics",
      "gate": "mvp-launch",
      "status": "not-measured",
      "derivedFrom": { "type": "pattern", "id": "P-001" },
      "painPointAddressed": "pain-1"
    }
  ],

  "summary": {
    "totalCriteria": 0,
    "byStatus": { "not-measured": 0, "below-threshold": 0, "at-threshold": 0, "exceeded": 0 }
  }
}
```

### goals/engineering.json

```json
{
  "$schema": "shipkit-artifact",
  "type": "goals-engineering",
  "version": "3.0",
  "lastUpdated": "YYYY-MM-DDTHH:MM:SSZ",
  "source": "shipkit-goals",

  "derivedFrom": {
    "engineeringDefinition": ".shipkit/engineering-definition.json"
  },

  "criteria": [
    {
      "id": "E-001",
      "name": "API response time",
      "category": "technical-performance",
      "metric": "p95 response time",
      "threshold": "< 500ms",
      "currentValue": null,
      "verificationMethod": "automated-test",
      "gate": "mvp-launch",
      "status": "not-measured",
      "derivedFrom": { "type": "mechanism", "id": "M-001" }
    }
  ],

  "summary": {
    "totalCriteria": 0,
    "byStatus": { "not-measured": 0, "below-threshold": 0, "at-threshold": 0, "exceeded": 0 }
  }
}
```

### Criterion ID Convention

| Prefix | Owner | Category |
|--------|-------|----------|
| `S-` | Visionary | business-metric |
| `P-` | PM | user-outcome |
| `E-` | EM | technical-performance |

### Metrics Schema (metrics/latest.json)

```json
{
  "$schema": "shipkit-artifact",
  "type": "metrics-snapshot",
  "version": "1.0",
  "collectedAt": "YYYY-MM-DDTHH:MM:SSZ",
  "source": "manual|analytics|automated-test",
  "measurements": {
    "S-001": { "value": 150, "unit": "DAU", "measuredAt": "..." },
    "P-001": { "value": 0.82, "unit": "ratio", "measuredAt": "..." },
    "E-001": { "value": 320, "unit": "ms", "measuredAt": "..." }
  }
}
```

Snapshots can be saved to `.shipkit/metrics/snapshots/YYYY-MM-DD.json` for history.

---

## When This Skill Integrates with Others

### Before This Skill
- `/shipkit-product-definition` — Produces the product blueprint: features, patterns, differentiators (required for Define)
- `/shipkit-engineering-definition` — Produces the engineering blueprint: mechanisms, components (required for Define)
- `/shipkit-product-discovery` — Produces user needs for traceability (recommended)
- `/shipkit-why-project` — Provides stage context (recommended)

### After This Skill
- `/shipkit-spec` — Criteria inform acceptance tests within feature specs
- `/shipkit-plan` — Plans can reference criteria for verification steps
- `/shipkit-verify` — Can reference criteria when checking implementation quality
- `/shipkit-project-status` — Displays criteria and gate status

### When This Skill Runs Again
- **Define mode**: File exists workflow activates — view/update/replace existing criteria
- **Evaluate mode**: Compare metrics to targets, output gap report with routing recommendations
- **Set Stage mode**: Update stage and constraints in strategic.json

---

## Context Files This Skill Reads

| File | Purpose | If Missing |
|------|---------|------------|
| `.shipkit/product-definition.json` | Product blueprint — features, patterns, differentiators | Route to `/shipkit-product-definition` |
| `.shipkit/engineering-definition.json` | Engineering blueprint — mechanisms, components | Route to `/shipkit-engineering-definition` |
| `.shipkit/product-discovery.json` | Pain points for traceability | Proceed without traceability |
| `.shipkit/why.json` | Project stage for criteria complexity | Ask user for stage |
| `.shipkit/goals.json` | Legacy single-file goals (migration) | No action |
| `.shipkit/metrics/latest.json` | Current metric actuals (Evaluate mode) | Report "no metrics" |

---

## Context Files This Skill Writes

**Write Strategy: OVERWRITE**

**Creates/Updates**:
- `.shipkit/goals/strategic.json` — Business-metric criteria + stage + constraints
- `.shipkit/goals/product.json` — User-outcome criteria
- `.shipkit/goals/engineering.json` — Technical-performance criteria

**Archive location** (if replacing):
- `.shipkit/.archive/goals-strategic.YYYY-MM-DD.json`
- `.shipkit/.archive/goals-product.YYYY-MM-DD.json`
- `.shipkit/.archive/goals-engineering.YYYY-MM-DD.json`

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
- [ ] Product-definition.json read and features/patterns/differentiators extracted
- [ ] Engineering-definition.json read and mechanisms extracted
- [ ] Criteria derived from each mechanism (performance + quality + reliability)
- [ ] Criteria derived from each UX pattern (usability + completion rate)
- [ ] Criteria derived from differentiators (validation)
- [ ] Each criterion has measurable threshold (not vague)
- [ ] Each criterion has verification method (how to measure)
- [ ] Criteria split into 3 files by category (strategic/product/engineering)
- [ ] Stage and constraints set in strategic.json
- [ ] Criteria grouped into stage gates
- [ ] User confirmed criteria and thresholds
- [ ] Gate composition confirmed
- [ ] derivedFrom traceability links are valid
- [ ] Summary counts match actual array lengths per file
- [ ] All 3 files saved to `.shipkit/goals/`
- [ ] Legacy migration offered if old goals.json exists
<!-- /SECTION:success-criteria -->

---

**Remember**: Success criteria are the acceptance tests for your product, owned by three agents: Visionary (business metrics), PM (user outcomes), EM (technical performance). Goals become the orchestration contract — the master agent checks these files to decide which agent to spawn. Keep targets realistic for the current stage. Update them as the solution evolves. Use `--evaluate` to check progress against actuals.
