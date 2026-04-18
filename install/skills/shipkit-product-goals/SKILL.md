---
name: shipkit-product-goals
description: "Derive measurable user-outcome criteria from the product blueprint. Writes goals/product.json (completion rates, UX quality, satisfaction). Evaluate mode compares actuals to targets."
argument-hint: "[goal topic | --evaluate]"
agent: shipkit-product-owner-agent
effort: medium
---

# shipkit-product-goals — Product Success Criteria

**Purpose**: Derive measurable user-outcome criteria from the product blueprint. Each feature, UX pattern, and differentiator implies criteria for "how do we know this works?" — this skill makes those criteria explicit, measurable, and trackable.

**What it does**: Reads the product blueprint + discovery context + stage from strategic.json, proposes user-outcome criteria (P-*), lets user validate, appends P-* IDs to existing stage gates, then writes `goals/product.json`.

**Output**: One JSON file:
- `goals/product.json` — User-outcome criteria (PM owns)

> **Strategic goals** (stage, constraints, business metrics: S-*) are handled by `/shipkit-stage`, owned by the Visionary agent.
> **Engineering goals** (technical performance: E-*) are handled by `/shipkit-engineering-goals`, owned by the Architect agent.

---

## Modes

| Mode | Trigger | What It Does |
|------|---------|-------------|
| **Define** (default) | "Set goals", "success criteria", "product goals" | Derive P-* criteria from product blueprint, write product.json, append P-* to gates |
| **Evaluate** | `--evaluate`, "check metrics" | Read metrics/latest.json, compare product criteria to targets, output gap report |

---

## When to Invoke

**User triggers**:
- "Define success criteria", "How do we measure success?"
- "Set product goals", "What are our goals?"
- "Evaluate goals", "Check metrics"

**Workflow position**:
- After `/shipkit-product-definition` (reads the product blueprint)
- After `/shipkit-stage` (reads stage and constraints from strategic.json)
- Before `/shipkit-engineering-goals` (engineering reads product goals for alignment)
- Before `/shipkit-spec` — criteria inform feature specifications
- Before `/shipkit-review-shipping` — criteria become verification checks

---

## Prerequisites

| File | Required? | Mode | Provides | If Missing |
|------|-----------|------|----------|------------|
| `.shipkit/product-definition.json` | **Yes** | Define | Features, patterns, differentiators | Route to `/shipkit-product-definition` |
| `.shipkit/product-discovery.json` | Recommended | Define | Pain points for traceability | Proceed without traceability |
| `.shipkit/goals/strategic.json` | Recommended | Define | Stage, constraints for calibration | Proceed with defaults; suggest `/shipkit-stage` |
| `.shipkit/goals/product.json` | **Yes** | Evaluate | Current targets | Route to Define mode first |
| `.shipkit/metrics/latest.json` | **Yes** | Evaluate | Current actuals | Report "no metrics available" |

---

## Output File

| File | Owner Agent | Criteria Category | Contains |
|------|------------|-------------------|----------|
| `goals/product.json` | PM | `user-outcome` | Completion rates, UX quality, satisfaction, content quality |

---

## Process — Define Mode

### Completion Tracking (MANDATORY)

After loading context (Step 1), create tasks:

1. `TaskCreate`: "Load context (product-definition + strategic.json)"
2. `TaskCreate`: "Derive P-* criteria with rubrics from product blueprint"
3. `TaskCreate`: "Classify checkability + verificationTool for each criterion"
4. `TaskCreate`: "Map P-* criteria to existing gates in strategic.json"
5. `TaskCreate`: "Archive existing artifact (if replacing)"
6. `TaskCreate`: "Write goals/product.json"
7. `TaskCreate`: "Update strategic.json gates with P-* IDs"
8. `TaskCreate`: "Verify summary counts match actual array length"

**Rules:**
- Writing product.json (task 6) is NOT done — strategic.json gates must also be updated (task 7)
- `TaskUpdate` the gates task to `completed` only after reading strategic.json back and confirming P-* IDs appear in gate criteria arrays
- Every criterion must have a rubric (3-5 levels) — bare thresholds fail the criteria derivation task
- Do NOT present the final summary until ALL tasks show completed

### Step 0: Check for Existing Files

1. Check if `.shipkit/goals/product.json` exists
2. If exists: archive current file to `.shipkit/.archive/goals-product.YYYY-MM-DD.json` and regenerate (fork context — no user prompt; let the reviewer catch over-eager rewrites)
3. If legacy `.shipkit/goals.json` exists: migrate (see Migration section)
4. If nothing exists: Skip to Step 1

---

### Step 1: Load Context

**Read these files:**

```
.shipkit/product-definition.json      → features, patterns, differentiators (REQUIRED)
.shipkit/product-discovery.json       → pain points for traceability (RECOMMENDED)
.shipkit/goals/strategic.json         → stage, constraints for calibration (RECOMMENDED)
```

**If product-definition.json missing**: Route to `/shipkit-product-definition` first.
**If strategic.json missing**: Suggest running `/shipkit-stage` first. Proceed with defaults if user declines.

---

### Step 2: Read Stage Context

Read stage and constraints from `goals/strategic.json` (set by `/shipkit-stage`):

| Stage | Product Criteria Depth | Focus |
|-------|----------------------|-------|
| POC | Basic: "core flow completable" (2-3 criteria) | Functional completeness |
| Alpha | Light: core path usability (3-5 criteria) | Core usability |
| MVP | Moderate: user outcome thresholds (5-10 criteria) | Usability + satisfaction |
| Scale | Comprehensive: full UX quality (10-15 criteria) | Growth + user delight |

If `goals/strategic.json` is missing, default to MVP stage (fork context — no user prompt; dispatch `/shipkit-stage` first if stage needs to be set explicitly).

---

### Step 3: Derive Criteria from Product Blueprint

For each section of product-definition.json, derive user-outcome criteria (P-*):

**From UX patterns**:
- Usability criteria (can users complete the flow?)
- Completion rate criteria (what % finish?)
- Responsiveness criteria (how fast does it feel?)

**From differentiators**:
- Validation criteria (does it actually differentiate?)
- User perception criteria (do users notice/value it?)

**From features**:
- Completeness gate (are all gate-scoped features functional?)
- Integration gate (do features work together end-to-end?)

> **Business metrics** (S-* criteria) are defined by `/shipkit-stage`, not this skill.

**Every threshold MUST include a rubric.** A bare number like "> 80%" is meaningless without defining what each level looks like. For each criterion, generate a rubric with 3-5 level descriptors:

```
Example rubric for "Wizard completion rate":
  0-20%: Users abandon immediately — flow is broken or confusing
  20-50%: Users attempt but hit blockers — missing guidance or errors
  50-80%: Users complete with effort — friction points remain
  80-95%: Users complete smoothly — minor polish needed
  95-100%: Users complete effortlessly — flow is intuitive
  Target: > 80% (smooth completion)
```

The rubric makes the threshold defensible — reviewers can assess where the product actually falls and what gap to close.

See `references/derivation-patterns.md` for detailed derivation examples.

---

### Step 3b: Classify Checkability + Verification Tool

For each derived criterion, assign `checkability` and `verificationTool`:

| `verificationMethod` | Context | `checkability` | `verificationTool` |
|----------------------|---------|---------------|-------------------|
| `automated-test` | Tests UI flow/rendering | `verifiable` | `visual-qa` |
| `automated-test` | Tests code quality/coverage | `verifiable` | `test` or `lint` |
| `manual-check` | Checks app behavior | `verifiable` | `visual-qa` or `semantic-qa` |
| `manual-check` | Needs domain expert review | `observable` | `none` |
| `analytics` | Any | `observable` | `none` |
| `user-feedback` | Any | `observable` | `none` |

**When uncertain**: default to `observable`.

**Key distinction**: "E2E flow passes" = `verifiable` (Playwright can simulate). "80% of real users complete flow" = `observable` (needs real funnel data).

---

### Step 4: Finalize Criteria

> **Forked producer — do not prompt.** You are dispatched inside a fork and have no user channel. Finalize the P-* criteria from your derivation pass (Step 3) directly, write them in Step 6, and let the direction reviewer catch any miscalibration via the loop's feedback cycle. If context is genuinely insufficient (missing product-definition.json, no stage set), return a `gaps_found` signal in the artifact instead of asking the user.

---

### Step 5: Map P-* to Existing Gates

Read gates from `goals/strategic.json` (defined by `/shipkit-stage`) and assign P-* criteria to them:

```
ADDING PRODUCT CRITERIA TO GATES:

MVP Launch Ready:
  Existing: S-001
  + P-001 (wizard completion time)
  + P-002 (wizard flow E2E)
  + P-003 (preview responsiveness)

Beta Ready:
  Existing: S-002, S-003
  + P-004 (teachers perceive speed advantage)
  + P-005 (teachers trust standards alignment)
```

If `goals/strategic.json` doesn't exist or has no gates, define gates locally in `product.json` and note they should be merged when `/shipkit-stage` runs.

Assign gates directly — no user prompt (fork context). The reviewer will flag misalignments in the loop's review cycle.

---

### Step 5.5: Archive Existing Artifact

**Artifact strategy: archive** — Before writing, if the target file already exists, move it to `.shipkit/archive/{filename}.{ISO-date}.json` (create the `archive/` directory if needed). Then write the new artifact fresh.

---

### Step 6: Generate Product Goal File

After confirmation:

1. Write `.shipkit/goals/product.json` — user-outcome criteria
2. If `goals/strategic.json` exists, update its gates `criteria` arrays to include P-* IDs

See `references/output-schema.md` for full schema.

---

### Step 7: Save and Suggest Next Steps

```
Product goals saved to .shipkit/goals/product.json

  Stage: {stage} (from strategic.json)
  Product criteria: {N}
  Gates updated: {N} (P-* criteria appended)

  Status: {N} not-measured

Next:
  1. /shipkit-engineering-goals — Add technical performance criteria (E-*)
  2. /shipkit-spec — Create specs for features (criteria inform acceptance tests)
  3. /shipkit-product-goals --evaluate — Check product criteria status after building
```

---

## Process — Evaluate Mode

When invoked with `--evaluate` or "check metrics":

### Step 1: Load Goal File

Read `goals/product.json` from `.shipkit/goals/`.

### Step 2: Load Metrics

Read `.shipkit/metrics/latest.json` for current actuals.

If missing: Report "No metrics file found. Create `.shipkit/metrics/latest.json` with current measurements to enable evaluation."

### Step 3: Compare Actuals to Targets

For each criterion in `goals/product.json`:
- Match metric key from `metrics/latest.json` to criterion ID
- Compare actual value to threshold
- Update status: `not-measured`, `below-threshold`, `at-threshold`, `exceeded`

### Step 5: Output Gap Report

Separate gaps into "Verifiable" (can be closed with tools) and "Observable" (needs real data):

```
PRODUCT GOAL EVALUATION — {date}

Stage: {stage}

═══ VERIFIABLE GAPS (run these tools to close) ═══

  ✗ P-003: Wizard flow E2E — not measured [visual-qa]
  ✓ P-004: Export works [visual-qa]

═══ OBSERVABLE GAPS (need real data) ═══

  ◌ P-001: Completion rate — needs real user funnel
  ◌ P-005: Teachers perceive speed advantage — needs user feedback

SUMMARY:
  Product criteria: {N}/{M} passing
  Verifiable: {V} passing, {V_gap} gaps
  Observable: {O} awaiting data

Note: Run /shipkit-stage --evaluate for full gate status across all goal files.
Note: Run /shipkit-engineering-goals --evaluate for technical criteria status.
```

---

## Migration from Legacy Format

When `.shipkit/goals.json` (single file) exists or files have `"source": "shipkit-goals"` (old unified skill):

1. Detect legacy format
2. Offer migration
3. Split criteria by `category`:
   - `business-metric` → strategic.json
   - `user-outcome` → product.json
   - `technical-performance` → leave for `/shipkit-engineering-goals` to handle
4. Archive original: `.shipkit/.archive/goals.YYYY-MM-DD.json`

---

## Goal File Schema

### goals/product.json

```json
{
  "$schema": "shipkit-artifact",
  "type": "goals-product",
  "version": "4.0",
  "lastUpdated": "YYYY-MM-DDTHH:MM:SSZ",
  "source": "shipkit-product-goals",

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
      "rubric": [
        { "range": "0-20%", "meaning": "Flow broken — users abandon immediately" },
        { "range": "20-50%", "meaning": "Major friction — users attempt but hit blockers" },
        { "range": "50-80%", "meaning": "Workable — most complete with effort" },
        { "range": "80-95%", "meaning": "Smooth — users complete without confusion" },
        { "range": "95-100%", "meaning": "Effortless — intuitive, no hesitation" }
      ],
      "currentValue": null,
      "verificationMethod": "analytics",
      "checkability": "observable",
      "verificationTool": "none",
      "gate": "mvp-launch",
      "status": "not-measured",
      "derivedFrom": { "type": "pattern", "id": "P-001" },
      "painPointAddressed": "pain-1"
    }
  ],

  "summary": {
    "totalCriteria": 0,
    "byStatus": {},
    "byCheckability": {}
  }
}
```

### Criterion ID Convention

| Prefix | Owner | Category | Defined By |
|--------|-------|----------|------------|
| `P-` | PM | user-outcome | `/shipkit-product-goals` |
| `S-` | Visionary | business-metric | `/shipkit-stage` |
| `E-` | EM | technical-performance | `/shipkit-engineering-goals` |

---

## When This Skill Integrates with Others

### Before This Skill
- `/shipkit-product-definition` — Product blueprint (required)
- `/shipkit-product-discovery` — User needs for traceability (recommended)
- `/shipkit-stage` — Stage context and gates (recommended)

### After This Skill
- `/shipkit-engineering-goals` — Reads product goals for alignment, adds E-* to gates
- `/shipkit-spec` — Criteria inform acceptance tests
- `/shipkit-plan` — Plans can reference criteria for verification steps
- `/shipkit-review-shipping` — Can reference criteria when checking quality

---

## Context Files This Skill Reads

| File | Purpose | If Missing |
|------|---------|------------|
| `.shipkit/product-definition.json` | Product blueprint | Route to `/shipkit-product-definition` |
| `.shipkit/product-discovery.json` | Pain points for traceability | Proceed without traceability |
| `.shipkit/goals/strategic.json` | Stage, constraints for calibration | Suggest `/shipkit-stage`; proceed with defaults |
| `.shipkit/metrics/latest.json` | Current actuals (Evaluate mode) | Report "no metrics" |

---

## Context Files This Skill Writes

**Write Strategy: OVERWRITE**

**Creates/Updates**:
- `.shipkit/goals/product.json` — User-outcome criteria
- `.shipkit/goals/strategic.json` — Updates gate `criteria` arrays to include P-* IDs (if file exists)

**Archive location** (if replacing):
- `.shipkit/.archive/goals-product.YYYY-MM-DD.json`

---

<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Has important context been saved to `.shipkit/`?
2. **Prerequisites** - Does the next action need a spec or plan first?
3. **Session length** - Long session? Consider `/shipkit-work-memory` for continuity.

**Natural capabilities** (no skill needed): Implementation, debugging, testing, refactoring, code documentation.

**Suggest skill when:** User needs engineering goals (`/shipkit-engineering-goals`), specs (`/shipkit-spec`), or verification (`/shipkit-review-shipping`).
<!-- /SECTION:after-completion -->

<!-- SECTION:success-criteria -->
## Success Criteria

Product goals artifact is complete when:
- [ ] Product-definition.json read and features/patterns/differentiators extracted
- [ ] Stage context read from strategic.json (or defaults used)
- [ ] P-* criteria derived from each UX pattern (usability + completion rate)
- [ ] P-* criteria derived from differentiators (validation)
- [ ] Each criterion has measurable threshold (not vague)
- [ ] Each threshold has a rubric with 3-5 level descriptors explaining what each range looks like
- [ ] Each criterion has verification method (how to measure)
- [ ] Each criterion has checkability classification (verifiable or observable)
- [ ] Each verifiable criterion has a verificationTool assigned
- [ ] P-* criteria mapped to existing gates in strategic.json (or local gates created)
- [ ] derivedFrom traceability links are valid
- [ ] Summary counts match actual array length
- [ ] File saved to `.shipkit/goals/product.json`
- [ ] Strategic.json gates updated with P-* criteria (if file exists)
<!-- /SECTION:success-criteria -->

---

**Schema version**: 4.0. Split from unified `shipkit-goals` v3.1 — product goals are now separate from strategic and engineering goals.

**Backward compatibility**: If reading goals files with `source: "shipkit-goals"`, these are from the unified skill. The criteria and schemas are compatible; only `source` field and version differ.

**Remember**: Product goals measure user outcomes — completion rates, UX quality, satisfaction. Strategic goals (S-*) are owned by `/shipkit-stage`. Engineering goals (E-*) are owned by `/shipkit-engineering-goals`. This skill appends P-* criteria to the gates defined by `/shipkit-stage`.
