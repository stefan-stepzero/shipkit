---
name: shipkit-engineering-goals
description: "Derive technical performance criteria from the engineering blueprint. Writes goals/engineering.json with response times, reliability, test coverage thresholds. Evaluate mode checks actuals against targets."
argument-hint: "[goal topic | --evaluate]"
context: fork
agent: shipkit-architect-agent
---

# shipkit-engineering-goals — Technical Performance Criteria

**Purpose**: Derive measurable technical performance criteria from the engineering blueprint. Each mechanism, component, and design decision implies criteria for "how do we know this performs?" — this skill makes those criteria explicit, measurable, and trackable.

**What it does**: Reads the engineering blueprint + stage context, proposes technical criteria, lets user validate, then generates the engineering goal file. Adds engineering criteria to existing stage gates.

**Output**: One JSON file:
- `goals/engineering.json` — Technical-performance criteria (EM owns)

> **Strategic goals** (stage, constraints, business metrics: S-*) are handled by `/shipkit-stage`, owned by the Visionary agent. Run that skill first — it creates the stage gates that engineering criteria are added to.
> **Product goals** (user outcomes: P-*) are handled by `/shipkit-product-goals`, owned by the PM agent.

---

## Modes

| Mode | Trigger | What It Does |
|------|---------|-------------|
| **Define** (default) | "engineering goals", "technical criteria", "SLAs" | Derive criteria from engineering blueprint, write engineering.json |
| **Evaluate** | `--evaluate`, "check engineering metrics" | Compare actuals to targets, output technical gap report |

---

## When to Invoke

**User triggers**:
- "Define engineering goals", "Technical performance criteria"
- "SLAs", "Response time targets"
- "Engineering metrics", "Test coverage goals"
- "Evaluate engineering goals"

**Workflow position**:
- After `/shipkit-engineering-definition` (reads the engineering blueprint)
- After `/shipkit-stage` (reads stage and constraints from strategic.json)
- After `/shipkit-product-goals` (reads product goals for alignment, adds E-* criteria to existing gates)
- Before `/shipkit-plan` — criteria inform implementation priorities
- Before `/shipkit-review-shipping` — criteria become verification checks

---

## Prerequisites

| File | Required? | Mode | Provides | If Missing |
|------|-----------|------|----------|------------|
| `.shipkit/engineering-definition.json` | **Yes** | Define | Mechanisms, components, design decisions | Route to `/shipkit-engineering-definition` |
| `.shipkit/goals/strategic.json` | Recommended | Define | Stage context, existing gates | Ask user for stage; create gates locally |
| `.shipkit/goals/product.json` | Recommended | Define | User-outcome targets for alignment | Proceed without alignment check |
| `.shipkit/goals/engineering.json` | **Yes** | Evaluate | Current targets | Route to Define mode first |
| `.shipkit/metrics/latest.json` | **Yes** | Evaluate | Current actuals | Report "no metrics available" |

---

## Process — Define Mode

### Step 0: Check for Existing File

1. Check if `.shipkit/goals/engineering.json` exists
2. If exists AND modified < 5 minutes ago: Show user, ask "Use these or regenerate?"
3. If exists AND modified > 5 minutes ago: Read and display summary, ask "View/Update/Replace/Cancel?"
4. If nothing exists: Skip to Step 1

**If Update:**
- Read existing engineering goals
- Ask: "What should change? (add criteria, adjust thresholds, add SLAs, etc.)"
- Regenerate incorporating updates

**If Replace:**
- Archive current file to `.shipkit/.archive/goals-engineering.YYYY-MM-DD.json`
- Proceed to Step 1

---

### Step 1: Load Context

**Read these files:**

```
.shipkit/engineering-definition.json  → mechanisms, components, design decisions (REQUIRED)
.shipkit/goals/strategic.json         → stage + existing gates (RECOMMENDED)
.shipkit/goals/product.json           → user-outcome targets for alignment (RECOMMENDED)
```

**If engineering-definition.json missing**: Route to `/shipkit-engineering-definition` first.

---

### Step 2: Read Stage

Read stage from `goals/strategic.json` (if exists) or ask user:

| Stage | Engineering Criteria | Focus |
|-------|---------------------|-------|
| POC | "It compiles" — build passes, no tests required | Functional |
| Alpha | "It works" — happy path tests, basic perf | Reliability |
| MVP | "It performs" — response times, test coverage, CI/CD | Performance |
| Scale | "It scales" — SLAs, load testing, p99 latency | Scalability |

---

### Step 3: Derive Criteria from Engineering Blueprint

For each mechanism in `engineering-definition.json`, derive three types of criteria:

**Performance: How fast?**
- Generation/response time for pipelines
- Query response time for search/data operations
- Processing throughput for batch operations
- Sync latency for real-time features

**Quality: How good is the output?**
- Output accuracy/relevance for AI/ML pipelines
- Data accuracy for transformations
- Content appropriateness for generation

**Reliability: How often does it work?**
- Completion rate / error rate
- Uptime / availability
- Job success rate for background processing

**Infrastructure criteria** (always included based on stage):
- Build compiles without errors (`verifiable` → `build`)
- Test suite passes (`verifiable` → `test`)
- Lint runs clean (`verifiable` → `lint`, if applicable)

**Every threshold MUST include a rubric.** A bare number like "< 500ms" is meaningless without defining what each level looks like. For each criterion, generate a rubric with 3-5 level descriptors:

```
Example rubric for "API response time (p95)":
  > 5s: Unusable — users perceive system as broken
  2-5s: Poor — noticeable delay, users may retry or abandon
  500ms-2s: Acceptable — slight lag but functional
  200-500ms: Good — feels responsive
  < 200ms: Excellent — feels instant
  Target: < 500ms (good — responsive)
```

The rubric anchors the threshold to observable reality and makes review assessments consistent.

See `references/derivation-patterns.md` for detailed derivation examples.

---

### Step 3b: Classify Checkability + Verification Tool

For each derived criterion, assign `checkability` and `verificationTool`:

| `verificationMethod` | Context | `checkability` | `verificationTool` |
|----------------------|---------|---------------|-------------------|
| `automated-test` | Tests backend pipeline/API | `verifiable` | `semantic-qa` |
| `automated-test` | Tests build/compile | `verifiable` | `build` |
| `automated-test` | Tests code quality/coverage | `verifiable` | `test` or `lint` |
| `automated-test` | Tests load/performance | `verifiable` | `semantic-qa` |
| `analytics` | Needs production traffic | `observable` | `none` |

**When uncertain**: default to `observable`.

**Key distinction**: "API responds in < 500ms in test" = `verifiable`. "p95 latency < 500ms under production load" = `observable`.

---

### Step 4: Propose Criteria for Validation

**Present proposed criteria:**

```
Based on your engineering blueprint:

ENGINEERING (EM — goals/engineering.json):
  E-001: Generation speed — < 5 seconds for first content
    Rubric:
      > 30s: Broken — users assume it failed
      10-30s: Poor — users wait but lose confidence
      5-10s: Marginal — noticeable delay
      2-5s: Good — acceptable wait
      < 2s: Excellent — feels responsive
    Verify: automated-test → semantic-qa
    Derived from: M-001 (LLM Generation Chain)

  E-002: Build passes — 0 errors
    Rubric:
      > 0 errors: Broken — cannot deploy
      0 errors: Pass — deployable
    Verify: automated-test → build

  E-003: Test suite passes — 0 failures
    Rubric:
      > 5 failures: Significant regression
      1-5 failures: Minor issues — investigate before deploy
      0 failures: Clean — ready to ship
    Verify: automated-test → test

  E-004: Generation reliability — > 99% success rate
    Rubric:
      < 90%: Unreliable — users encounter frequent errors
      90-95%: Flaky — occasional failures erode trust
      95-99%: Stable — rare failures, acceptable
      > 99%: Production-ready — reliable under sustained load
    Verify: analytics (needs production traffic)
    Checkability: observable

Accept these? Or:
  - Add: "I also want to track response time for search"
  - Remove: "Skip lint for now"
  - Adjust: "Make generation speed < 3 seconds"
```

**If user modifies**: Incorporate changes. Re-present if major changes.

---

### Step 5: Map to Existing Gates

Read gates from `goals/strategic.json` and assign engineering criteria to them:

```
ADDING ENGINEERING CRITERIA TO GATES:

MVP Launch Ready:
  Existing: S-001, P-001, P-002
  + E-001 (generation speed)
  + E-002 (build passes)
  + E-003 (tests pass)

Beta Ready:
  Existing: S-002, P-003
  + E-004 (reliability > 99%)
```

If `goals/strategic.json` doesn't exist, define gates locally in `engineering.json`.

Ask user to confirm gate assignment.

---

### Step 5.5: Archive Existing Artifact

**Artifact strategy: archive** — Before writing, if the target file already exists, move it to `.shipkit/archive/{filename}.{ISO-date}.json` (create the `archive/` directory if needed). Then write the new artifact fresh.

---

### Step 6: Generate Engineering Goal File

Write `.shipkit/goals/engineering.json`.

If `goals/strategic.json` exists, also update its gates array to include E-* criterion IDs.

---

### Step 7: Save and Suggest Next Steps

```
Engineering goals saved to .shipkit/goals/engineering.json

  Stage: {stage}
  Engineering criteria: {N}
  Gates updated: {N} (E-* criteria added)

  Status: {N} not-measured

Next:
  1. /shipkit-plan — Create implementation plans
  2. /shipkit-engineering-goals --evaluate — Check criteria after building
```

---

## Process — Evaluate Mode

When invoked with `--evaluate`:

### Step 1: Load Engineering Goals

Read `goals/engineering.json`.

### Step 2: Load Metrics

Read `.shipkit/metrics/latest.json`.

If missing: Report "No metrics file found."

### Step 3: Compare Actuals to Targets

For each criterion:
- Match metric key to criterion ID
- Compare actual value to threshold
- Update status

### Step 4: Output Technical Gap Report

Separate by checkability:

```
ENGINEERING GOAL EVALUATION — {date}

═══ VERIFIABLE GAPS (run these tools to close) ═══

  ✗ E-001: Generation speed — not measured [semantic-qa]
  ✗ E-002: Build passes — not measured [build]
  ✓ E-003: Tests pass [test]

═══ OBSERVABLE GAPS (need production data) ═══

  ◌ E-004: Reliability — needs sustained production traffic

RECOMMENDATION:
  Priority: E-002 (build) → E-001 (generation speed)
  Run: implement fixes, then /shipkit-semantic-qa
```

---

## Goal File Schema

### goals/engineering.json

```json
{
  "$schema": "shipkit-artifact",
  "type": "goals-engineering",
  "version": "4.0",
  "lastUpdated": "YYYY-MM-DDTHH:MM:SSZ",
  "source": "shipkit-engineering-goals",

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
      "rubric": [
        { "range": "> 5s", "meaning": "Unusable — users perceive system as broken" },
        { "range": "2-5s", "meaning": "Poor — noticeable delay, users may retry" },
        { "range": "500ms-2s", "meaning": "Acceptable — slight lag but functional" },
        { "range": "200-500ms", "meaning": "Good — feels responsive" },
        { "range": "< 200ms", "meaning": "Excellent — feels instant" }
      ],
      "currentValue": null,
      "verificationMethod": "automated-test",
      "checkability": "verifiable",
      "verificationTool": "test",
      "gate": "mvp-launch",
      "status": "not-measured",
      "derivedFrom": { "type": "mechanism", "id": "M-001" }
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

| Prefix | Owner | Category |
|--------|-------|----------|
| `E-` | EM | technical-performance |

---

## When This Skill Integrates with Others

### Before This Skill
- `/shipkit-engineering-definition` — Engineering blueprint (required)
- `/shipkit-stage` — Stage context + gates (recommended)
- `/shipkit-product-goals` — Product goals for alignment (recommended)

### After This Skill
- `/shipkit-plan` — Criteria inform implementation priorities
- `/shipkit-review-shipping` — Can reference criteria when checking quality
- `/shipkit-work-memory` — Session continuity and progress tracking

---

## Context Files This Skill Reads

| File | Purpose | If Missing |
|------|---------|------------|
| `.shipkit/engineering-definition.json` | Engineering blueprint | Route to `/shipkit-engineering-definition` |
| `.shipkit/goals/strategic.json` | Stage + existing gates | Ask user for stage |
| `.shipkit/goals/product.json` | User-outcome targets for alignment | Proceed without alignment |
| `.shipkit/stack.json` | Tech stack for calibrating criteria | Proceed with generic criteria |
| `.shipkit/metrics/latest.json` | Current actuals (Evaluate mode) | Report "no metrics" |

---

## Context Files This Skill Writes

**Write Strategy: OVERWRITE**

**Creates/Updates**:
- `.shipkit/goals/engineering.json` — Technical-performance criteria
- `.shipkit/goals/strategic.json` — Updates gate `criteria` arrays to include E-* IDs (if file exists)

**Archive location** (if replacing):
- `.shipkit/.archive/goals-engineering.YYYY-MM-DD.json`

---

<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Has important context been saved to `.shipkit/`?
2. **Prerequisites** - Does the next action need a spec or plan first?
3. **Session length** - Long session? Consider `/shipkit-work-memory` for continuity.

**Suggest skill when:** User needs plans (`/shipkit-plan`), specs (`/shipkit-spec`), or verification (`/shipkit-review-shipping`).
<!-- /SECTION:after-completion -->

<!-- SECTION:success-criteria -->
## Success Criteria

Engineering goals artifact is complete when:
- [ ] Engineering-definition.json read and mechanisms extracted
- [ ] Criteria derived from each mechanism (performance + quality + reliability)
- [ ] Infrastructure criteria included (build, test, lint as applicable)
- [ ] Each criterion has measurable threshold
- [ ] Each threshold has a rubric with 3-5 level descriptors explaining what each range looks like
- [ ] Each criterion has verification method
- [ ] Each criterion has checkability classification
- [ ] Each verifiable criterion has a verificationTool assigned
- [ ] Criteria mapped to existing stage gates (or new gates created)
- [ ] User confirmed criteria and thresholds
- [ ] Gate assignments confirmed
- [ ] derivedFrom traceability links are valid
- [ ] Summary counts match actual array length
- [ ] File saved to `.shipkit/goals/engineering.json`
- [ ] Strategic.json gates updated with E-* criteria (if file exists)
<!-- /SECTION:success-criteria -->

---

**Schema version**: 4.0. Split from unified `shipkit-goals` v3.1 — engineering goals are now owned by the Architect agent.

**Backward compatibility**: If reading goals files with `source: "shipkit-goals"`, these are from the unified skill. The criteria schema is compatible; only `source` field and version differ.

**Remember**: Engineering goals measure technical performance — speed, reliability, quality, and health. These are the EM's responsibility. Strategic goals (S-*) are owned by `/shipkit-stage`. Product outcomes (P-*) are owned by `/shipkit-product-goals`.
