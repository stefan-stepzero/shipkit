---
name: shipkit-stage
description: "Define project stage, scope constraints, and graduation criteria. Set mode configures the stage; evaluate mode assesses readiness for human approval."
argument-hint: "[set | --evaluate]"
context: fork
agent: shipkit-visionary-agent
---

# shipkit-stage — Project Stage & Graduation Criteria

**Purpose**: Define the project stage (POC/Alpha/MVP/Scale), derive scope constraints and quality bars from that stage, set business-metric criteria (S-*), and define stage gates. Evaluate mode assesses gate readiness for human-approved graduation.

**What it does**: Reads the project vision, asks the human to confirm stage, derives constraints and business metrics, defines gates with S-* criteria, and writes `goals/strategic.json`. Evaluate mode cross-references ALL goal files to build a graduation evidence table.

**Output**: One JSON file:
- `goals/strategic.json` — Stage, constraints, stageImplications, business-metric criteria, gates

> **Product goals** (user outcomes: P-*) are handled by `/shipkit-product-goals`. **Engineering goals** (technical performance: E-*) are handled by `/shipkit-engineering-goals`. Both skills append their criteria IDs to the gates defined here.

---

## Modes

| Mode | Trigger | What It Does |
|------|---------|-------------|
| **Set** (default) | "Set stage", "stage", "constraints" | Set stage, derive constraints + business metrics, define gates |
| **Evaluate** | `--evaluate`, "graduation", "ready to advance?" | Cross-check all criteria across all goal files, build evidence table, recommend graduation |

---

## When to Invoke

**User triggers**:
- "Set project stage", "What stage are we at?"
- "Define constraints", "Quality bar"
- "Stage gates", "Graduation criteria"
- "Ready to graduate?", "Evaluate stage readiness"

**Workflow position**:
- After `/shipkit-why-project` (reads why.json for vision context)
- Before `/shipkit-product-goals` (strategic.json provides stage context for PM)
- Before `/shipkit-engineering-goals` (strategic.json provides stage context for EM)
- Before `/shipkit-spec` — stage constraints inform feature scoping

---

## Prerequisites

| File | Required? | Mode | Provides | If Missing |
|------|-----------|------|----------|------------|
| `.shipkit/why.json` | **Yes** | Set | Vision, purpose, approach | Route to `/shipkit-why-project` |
| `.shipkit/goals/strategic.json` | **Yes** | Evaluate | Current stage + criteria | Route to Set mode first |
| `.shipkit/goals/product.json` | Recommended | Evaluate | P-* criteria for gate check | Report "product goals not yet defined" |
| `.shipkit/goals/engineering.json` | Recommended | Evaluate | E-* criteria for gate check | Report "engineering goals not yet defined" |
| `.shipkit/specs/active/*.json` | Recommended | Evaluate | Spec coverage evidence | Report "no specs found" |
| `.shipkit/plans/active/*.json` | Recommended | Evaluate | Plan coverage evidence | Report "no plans found" |
| `.shipkit/progress.json` | Recommended | Evaluate | Implementation status | Report "no progress data" |

---

## Process — Set Mode

### Completion Tracking

Create tasks for each major output:
- `TaskCreate`: "Confirm stage with user"
- `TaskCreate`: "Derive constraints + stageImplications"
- `TaskCreate`: "Derive S-* criteria with rubrics"
- `TaskCreate`: "Define stage gates"
- `TaskCreate`: "Write goals/strategic.json"

In Evaluate mode, create tasks:
- `TaskCreate`: "Build evidence table across all goal files"
- `TaskCreate`: "Produce graduation recommendation"

Each S-* criterion must include a rubric — bare thresholds are incomplete.

### Step 0: Check for Existing File

1. Check if `.shipkit/goals/strategic.json` exists
2. If exists AND modified < 5 minutes ago: Show user, ask "Use this or regenerate?"
3. If exists AND modified > 5 minutes ago: Read and display summary, ask "View/Update/Replace/Cancel?"
4. If nothing exists: Skip to Step 1

**If Update:**
- Read existing strategic goals
- Ask: "What should change? (stage, constraints, add criteria, adjust thresholds, etc.)"
- Regenerate incorporating updates

**If Replace:**
- Archive current file to `.shipkit/.archive/goals-strategic.YYYY-MM-DD.json`
- Proceed to Step 1

---

### Step 1: Load Context

**Read these files:**

```
.shipkit/why.json      → vision, purpose, approach (REQUIRED)
```

**If why.json missing**: Route to `/shipkit-why-project` first.

---

### Step 2: Ask Human for Stage

Present stage options and ask the human to choose:

```
What stage is this project at?

  1. POC   — Prove the core mechanism works
  2. Alpha — Core flow works E2E for testers
  3. MVP   — Production-ready for launch segment
  4. Scale — Enterprise-ready, optimized for growth

Current stage: [detected from goals/strategic.json or "not set"]
Target stage: [ask user]
```

---

### Step 3: Derive Constraints and Stage Implications

Based on stage choice, derive constraints and `stageImplications`:

| Stage | Quality | Scope | Skip | Focus |
|-------|---------|-------|------|-------|
| **POC** | "It works" | Core mechanism only | Tests, lint, docs, error handling | Functional proof |
| **Alpha** | "Reliable" | Core flow E2E | Load testing, security audit | Core usability |
| **MVP** | "Production-ready" | Feature-complete for launch | Scale testing, enterprise features | Launch readiness |
| **Scale** | "Enterprise-ready" | Full product | Nothing | Growth + operational excellence |

Present constraints and let user adjust:

```
Stage: MVP

Constraints:
  Quality: production-ready — CI/CD, monitoring, error handling
  Scope: feature-complete for launch segment
  Cost: moderate — dedicated resources acceptable

Stage Implications (cascaded to all agents):
  Skip: scale testing, enterprise features
  Focus: launch readiness, user experience, reliability
  Quality bar: "works for customers"

Accept these? Or adjust:
  - "Make quality bar higher"
  - "Tighten scope to just core flow"
  - "Custom constraint"
```

---

### Step 4: Derive Business-Metric Criteria (S-*)

Based on vision + stage, derive business-metric criteria:

| Stage | Typical Business Metrics |
|-------|------------------------|
| POC | None — just "it works" |
| Alpha | Initial user count, basic engagement |
| MVP | DAU/MAU, retention (7-day return), user satisfaction |
| Scale | Revenue, conversion, NPS, churn, CAC, LTV |

**Every threshold MUST include a rubric.** A bare number like "> 100 DAU" is meaningless without defining what each level indicates. For each criterion, generate a rubric with 3-5 level descriptors explaining what the number means in practice.

Present proposed criteria with rubrics for validation:

```
Based on your vision and stage (MVP):

STRATEGIC CRITERIA (Visionary — goals/strategic.json):
  S-001: User acquisition
    Threshold: > 100 DAU within 30 days of launch
    Rubric:
      < 10 DAU: No traction — revisit distribution or value prop
      10-50 DAU: Early signal — some interest but not enough to validate
      50-100 DAU: Growing — close to validation threshold
      100-500 DAU: Validated — enough users to measure retention
      500+ DAU: Strong traction — ready for growth investment
    Verify: analytics
    Checkability: observable — needs real user data

  S-002: Return usage
    Threshold: > 40% 7-day return rate
    Rubric:
      < 10%: No retention — users try once and leave
      10-25%: Weak — product doesn't compel return visits
      25-40%: Moderate — some value but not habit-forming
      40-60%: Good — users find ongoing value
      60%+: Excellent — strong product-market fit signal
    Verify: analytics
    Checkability: observable — needs cohort data

  S-003: User satisfaction
    Threshold: > 4.0/5.0 average rating
    Rubric:
      < 2.0: Users actively dislike the product
      2.0-3.0: Below expectations — significant gaps
      3.0-4.0: Acceptable — meets basic needs but uninspiring
      4.0-4.5: Good — users are satisfied and would recommend
      4.5-5.0: Exceptional — strong advocacy potential
    Verify: user-feedback
    Checkability: observable — needs survey data

Accept these? Or:
  - Add: "I also want to track revenue"
  - Remove: "Skip satisfaction for now"
  - Adjust: "Make DAU threshold 50"
```

---

### Step 5: Define Stage Gates

Group confirmed S-* criteria into named gates. Gates start with S-* only — P-* and E-* are appended by other skills:

```
STAGE GATES:

mvp-launch (all must pass):
  - S-001 (user acquisition)
  Note: P-* criteria added by /shipkit-product-goals
  Note: E-* criteria added by /shipkit-engineering-goals

beta-ready (mvp-launch + these):
  - S-002 (return usage)
  - S-003 (user satisfaction)
```

> **Note**: Gates are defined here with S-* criteria only. `/shipkit-product-goals` appends P-* IDs, `/shipkit-engineering-goals` appends E-* IDs. Gates grow as other skills add their criteria.

Ask user to confirm gate composition.

---

### Step 6: Generate Strategic Goals File

After confirmation, write:

`.shipkit/goals/strategic.json` — stage, constraints, stageImplications, S-* criteria, gates

See `references/output-schema.md` for full schema.

---

### Step 7: Save and Suggest Next Steps

```
Strategic goals saved to .shipkit/goals/strategic.json

  Stage: {current} → {target}
  Constraints: {quality}, {scope}
  Strategic criteria: {N} (all observable — need real data after launch)
  Gates: {N} (S-* only — P-*/E-* added by downstream skills)

Next:
  1. /shipkit-product-goals — Define user-outcome criteria (P-*), append to gates
  2. /shipkit-engineering-goals — Define technical criteria (E-*), append to gates
  3. /shipkit-stage --evaluate — Check graduation readiness after building
```

---

## Process — Evaluate Mode

When invoked with `--evaluate` or "graduation readiness":

### Step 1: Load ALL Artifacts

Read everything relevant:

```
.shipkit/goals/strategic.json     → S-* criteria + gates
.shipkit/goals/product.json       → P-* criteria
.shipkit/goals/engineering.json   → E-* criteria
.shipkit/specs/active/*.json      → spec coverage
.shipkit/plans/active/*.json      → plan coverage
.shipkit/progress.json            → implementation status
```

### Step 2: Build Evidence Table

For each gate, check ALL referenced criteria (S-*, P-*, E-*) across all goal files:

| Criterion | Status | Evidence |
|-----------|--------|----------|
| S-001 | AWAITING DATA | Observable — needs analytics post-launch |
| P-001 | MET | Playwright E2E passes (visual-qa) |
| P-002 | NOT MET | Completion rate below threshold |
| E-001 | MET | Build passes, tests green |
| E-002 | MET | Response time < 500ms (semantic-qa) |

### Step 3: Gate Readiness Assessment

For each gate:

```
GATE: mvp-launch
  Status: PARTIAL

  Verifiable criteria:  3/4 passing
  Observable criteria:  0/2 measured (awaiting data)

  Passing:
    ✓ P-001: Wizard flow E2E [visual-qa]
    ✓ E-001: Build passes [build]
    ✓ E-002: Tests pass [test]

  Failing:
    ✗ P-002: Preview responsiveness — 800ms (threshold: < 500ms) [visual-qa]

  Awaiting data:
    ◌ S-001: User acquisition — needs analytics after launch
    ◌ S-002: Return usage — needs cohort tracking
```

### Step 4: Graduation Recommendation

Present recommendation to human — **stage advancement is always a human checkpoint**:

```
GRADUATION ASSESSMENT — {date}

Current stage: MVP
Target stage: Scale

RECOMMENDATION: NOT READY

Verifiable gaps: 1 remaining
  ✗ P-002: Preview responsiveness needs optimization

Observable gaps: 2 awaiting data (expected — need real users)

When ready:
  1. Fix P-002 (preview responsiveness)
  2. Deploy to production
  3. Collect analytics data for S-001, S-002
  4. Re-run /shipkit-stage --evaluate

Proceed with graduation anyway? (human decision)
```

### Step 5: If Approved

If human approves graduation:
1. Update `stage.current` to new stage
2. Recalculate constraints and stageImplications for new stage
3. Write updated `goals/strategic.json`
4. Report stage change — all agents will read new stageImplications

---

## Migration from Legacy Format

When `.shipkit/goals/strategic.json` exists with `"source": "shipkit-product-goals"` (old owner):

1. Detect legacy source field
2. Update `source` to `"shipkit-stage"`
3. Add `stageImplications` if missing (derive from stage)
4. Update `derivedFrom` to reference only `why.json`
5. Keep all existing criteria and gates intact

---

## Context Files This Skill Reads

| File | Purpose | If Missing |
|------|---------|------------|
| `.shipkit/why.json` | Vision, purpose, approach | Route to `/shipkit-why-project` |
| `.shipkit/goals/strategic.json` | Existing stage + criteria (Evaluate mode) | Route to Set mode |
| `.shipkit/goals/product.json` | P-* criteria for gate evaluation | Report "not yet defined" |
| `.shipkit/goals/engineering.json` | E-* criteria for gate evaluation | Report "not yet defined" |
| `.shipkit/metrics/latest.json` | Measured progress data (Evaluate mode) | Report "no metrics" |
| `.shipkit/spec-roadmap.json` | Roadmap completion evidence (Evaluate mode) | Report "no roadmap" |
| `.shipkit/specs/active/*.json` | Spec coverage evidence (Evaluate mode) | Report "no specs" |
| `.shipkit/plans/active/*.json` | Plan coverage evidence (Evaluate mode) | Report "no plans" |
| `.shipkit/progress.json` | Implementation status (Evaluate mode) | Report "no progress data" |

---

## Context Files This Skill Writes

**Write Strategy: OVERWRITE**

**Creates/Updates**:
- `.shipkit/goals/strategic.json` — Stage, constraints, stageImplications, S-* criteria, gates

**Archive location** (if replacing):
- `.shipkit/.archive/goals-strategic.YYYY-MM-DD.json`

---

<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Has important context been saved to `.shipkit/`?
2. **Prerequisites** - Does the next action need a spec or plan first?
3. **Session length** - Long session? Consider `/shipkit-work-memory` for continuity.

**Natural capabilities** (no skill needed): Implementation, debugging, testing, refactoring, code documentation.

**Suggest skill when:** User needs product goals (`/shipkit-product-goals`), engineering goals (`/shipkit-engineering-goals`), or specs (`/shipkit-spec`).
<!-- /SECTION:after-completion -->

<!-- SECTION:success-criteria -->
## Success Criteria

Stage artifact is complete when:
- [ ] why.json read and vision context extracted
- [ ] Human confirmed current stage and target stage
- [ ] Constraints derived from stage and confirmed by human
- [ ] stageImplications derived (skip, focus, qualityBar)
- [ ] S-* business-metric criteria derived from vision + stage
- [ ] Each criterion has measurable threshold
- [ ] Each criterion has verification method and checkability classification
- [ ] Criteria grouped into named stage gates
- [ ] Gates contain only S-* criteria (P-*/E-* added by downstream skills)
- [ ] User confirmed criteria, thresholds, and gate composition
- [ ] derivedFrom references only why.json
- [ ] Summary counts match actual array length
- [ ] File saved to `.shipkit/goals/strategic.json`
<!-- /SECTION:success-criteria -->

---

**Schema version**: 5.0. Split from `shipkit-product-goals` v4.0 — strategic goals now have their own lifecycle owned by the Visionary agent.

**Backward compatibility**: Files with `source: "shipkit-product-goals"` are from the previous owner. The criteria and gate schemas are compatible; only `source`, `version`, `stageImplications`, and `derivedFrom` differ. Migration is automatic on first run.

**Remember**: This skill defines the strategic frame — stage, constraints, and business metrics. Stage advancement is always a human checkpoint. Other skills (product-goals, engineering-goals) append their criteria to the gates defined here.
