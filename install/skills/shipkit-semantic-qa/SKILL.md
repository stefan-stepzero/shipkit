---
name: shipkit-semantic-qa
description: "Semantic QA — define inputs/criteria, generate test scripts, Claude judges outputs or screenshots against criteria. Also scores a built app's fidelity (completeness + essence) against captured intent. Triggers: 'semantic qa', 'quality check', 'visual qa', 'judge outputs', 'QA suite', 'fidelity scorecard', 'score fidelity'."
argument-hint: "[suite-name] [--setup|--run|--judge|--full|--fidelity]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
effort: medium
---

# shipkit-semantic-qa - Semantic Quality Assurance

**Purpose**: Define test inputs and quality criteria, generate test scripts, run them, and let Claude semantically judge outputs (API responses or UI screenshots) against human-defined criteria.

**Pattern**: One skill, one loop — Setup → Run → Judge. Two suite types: backend (API/LLM pipeline) and frontend (visual components).

---

## When to Invoke

**User triggers:**
- "Semantic QA", "Set up QA", "Quality check"
- "Visual QA", "Screenshot QA", "Check my UI"
- "Judge outputs", "Run QA suite", "Check quality"
- "Set up quality criteria", "Define test inputs"

**Workflow position:**
- After features are implemented (something to test)
- Before verify/preflight (catches quality issues early)
- Can run standalone against any API or UI

---

## Prerequisites

**Required:** None (Setup mode creates everything)

**Helpful:**
- `.shipkit/stack.json` — Tech stack informs script generation
- `.shipkit/specs/` — Acceptance criteria can seed quality criteria
- Playwright installed (for frontend suites only)

---

## Process

### Completion Tracking

In `--full` mode (all 3 phases sequential), create tasks at the start:
- `TaskCreate`: "Setup: Define criteria + generate test script"
- `TaskCreate`: "Run: Execute tests + verify output count"
- `TaskCreate`: "Judge: Evaluate ALL outputs against ALL criteria"
- `TaskCreate`: "Write judgment.md + judgment.json"

`TaskUpdate` each task to `in_progress` when starting it, `completed` when done.

In Judge mode with 5+ outputs, create one task per output to prevent partial evaluation.
Do NOT present judgment summary until all output evaluations are complete and files are written.

### Step 0: Mode Detection

Determine mode from arguments and state:

**Explicit flag provided:**
- `--setup` → Setup mode
- `--run` → Run mode
- `--judge` → Judge mode
- `--full` → Setup (if needed) → Run → Judge
- `--fidelity` → **Fidelity mode** — score a built app against captured intent (completeness + essence),
  emit a fidelity scorecard. See [Step 5](#step-5-fidelity-mode---fidelity). Add a second suite/arm to
  compare two builds under one rubric.

**Suite name without flag — check state:**

| State | Mode |
|-------|------|
| Suite doesn't exist | → Setup |
| Suite exists, no outputs | → Run |
| Suite exists, outputs without judgment | → Judge |
| Suite exists, recent judgment (< 5 min) | → Quick Exit: View / Re-judge / Run again |

**No arguments:**
- If no suites exist → "No QA suites set up. Let's create one."
- If suites exist → List with status, ask which to run

---

### Step 1: Setup Mode

**Goal:** Capture human quality judgment, define test inputs, generate a test script.

#### Step 1.1: Suite Type

Ask: "What are we testing?"
- **Backend** — API endpoints, LLM pipelines, data processing
- **Frontend** — UI components, pages, visual states

#### Step 1.2: Define Run Strategy (Semantic)

Capture HOW to get outputs, in the user's words:

**Backend examples:**
- "POST each input to `/api/extract` and save the JSON response"
- "Run each input through the `processDocument()` function and capture return value"
- "Call the OpenAI-compatible endpoint at localhost:3000/v1/chat/completions"

**Frontend examples:**
- "Navigate to each component's Storybook page and screenshot it"
- "Load each route with mock data injected via context provider, screenshot at 3 viewports"
- "Use Playwright to visit each page, wait for data load, screenshot"

Store this as a semantic description in `suite.json`. Claude uses it to write and maintain the test script.

#### Step 1.3: Define Quality Criteria (THE HUMAN INPUT)

This is where the skill earns its existence — capturing what "good" means.

**For backend suites, ask:**
1. "What does good output look like for this pipeline?"
2. "What failure modes worry you?"
3. "Which criteria are must-pass vs nice-to-have?"

**For frontend suites, ask:**
1. "What visual quality standards matter?"
2. "What states need checking?" (empty, loaded, error, overflow)
3. "What viewports?" (desktop, tablet, mobile)

Write criteria to `suite.json` using this format per criterion:
```json
{
  "id": "SQ-001",
  "name": "Response Relevance",
  "description": "Output directly addresses the input query",
  "weight": "must-pass",
  "evaluationGuide": "Check if response answers what was asked. Off-topic = FAIL.",
  "passExample": "Input asks about pricing, output lists pricing tiers",
  "failExample": "Input asks about pricing, output gives company bio"
}
```

**Key fields:**
- `weight`: `must-pass` | `important` | `nice-to-have`
- `evaluationGuide`: Specific instructions for Claude on HOW to judge this criterion
- `passExample`/`failExample`: Optional anchors for ambiguous cases

See `references/criteria-guide.md` for detailed guidance.

**Criteria source — hand-authored vs the essence block.** By default criteria are captured from the user
here (that's the human input this skill earns its existence on). But when you're scoring a *built app's
fidelity to captured intent*, the criteria already exist as **checkable assertions** in the
product-definition essence block. In that case set `criteriaSource: "essence"` in `suite.json` and derive
criteria from `.shipkit/product-definition.json` instead of asking the user — see
[Step 5: Fidelity Mode](#step-5-fidelity-mode---fidelity).

#### Step 1.4: Define Input Library (Backend) or Component Inventory (Frontend)

**Backend:** Coach user through defining input variants:
- **Happy path** — typical usage, expected to pass everything
- **Edge cases** — boundaries, unusual but valid inputs
- **Adversarial** — malformed, injection attempts, empty/null

Write to `.shipkit/semantic-qa/suites/{suite}/inputs/*.json`

**Frontend:** Build component inventory:
- Component name, route or selector
- Mock data variants (empty, single item, many items, error state)
- Viewports to test

Write to `.shipkit/semantic-qa/suites/{suite}/components/inventory.json`

#### Step 1.5: Generate Test Script

**Based on the run strategy description**, write a project-specific script to `scripts/semantic-qa-{suite-name}.{ext}`.

This is Claude writing a real script tailored to the project — NOT a rigid template. The script should:
- Read inputs from `.shipkit/semantic-qa/suites/{suite}/inputs/`
- Execute the strategy (API calls, function invocations, Playwright screenshots)
- Save outputs to `.shipkit/semantic-qa/suites/{suite}/outputs/run-{timestamp}/`
  (already per-run via `run-{timestamp}`; under the orchestration engine these run
  outputs are transient and nest in the run root — see
  `install/shared/references/run-artifacts.md`. Suite definitions/inputs are durable.)
- Handle errors gracefully (save error info, don't crash on individual failures)

**The user owns this script after creation.** Claude can update it as the project evolves.

Record the script path in `suite.json` under `script`.

#### Step 1.6: Write Configuration

**`suite.json`** at `.shipkit/semantic-qa/suites/{suite-name}/suite.json`:
```json
{
  "$schema": "shipkit-artifact",
  "type": "semantic-qa-suite",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DD",
  "source": "shipkit-semantic-qa",
  "name": "{suite-name}",
  "suiteType": "backend|frontend",
  "description": "User's description of what this suite tests",
  "runStrategy": "Semantic description of how to get outputs",
  "script": "scripts/semantic-qa-{suite-name}.ts",
  "criteria": [/* ... */],
  "inputCategories": {
    "happy-path": { "description": "Typical usage", "files": ["inputs/happy-path.json"] }
  }
}
```

**`config.json`** at `.shipkit/semantic-qa/config.json` (if first suite):
```json
{
  "$schema": "shipkit-artifact",
  "type": "semantic-qa-config",
  "version": "1.0",
  "suites": ["{suite-name}"]
}
```

**Update `.gitignore`** — Add entries for `outputs/` and `screenshots/` directories.

---

### Step 2: Run Mode

**Goal:** Execute the test script and collect outputs.

#### Step 2.1: Validate Prerequisites

| Check | If missing |
|-------|-----------|
| `suite.json` exists | → "Suite not set up. Run `--setup` first." |
| Script exists at recorded path | → "Script not found. Regenerating from run strategy." |

If the script is missing, Claude regenerates it from the `runStrategy` description in `suite.json`.

#### Step 2.2: Execute Script

Run the script via Bash. The script reads inputs and produces outputs.

```
Running semantic-qa-api-pipeline.ts...
```

#### Step 2.3: Verify Outputs

Count output files, report status:

```
Run complete: run-2026-02-11T143022

Outputs collected: 8/10
  ✓ happy-path-001.json
  ✓ happy-path-002.json
  ...
  ✗ adversarial-003.json (timeout)
  ✗ adversarial-004.json (500 error)

Ready for judgment.
```

Update `suite.json` with `lastRun` metadata.

---

### Step 3: Judge Mode

**Goal:** Claude reads every output/screenshot and evaluates against stored criteria.

#### Step 3.1: Load Context

1. Read `suite.json` → get `criteria[]` and `lastRun`
2. Glob the most recent `outputs/run-{latest}/` or `screenshots/run-{latest}/`
3. Read previous judgment if it exists (for comparison)

#### Step 3.2: Evaluate

**For 5+ outputs, use parallel subagents (one per output):**

```
Launch Agent subagents IN PARALLEL:

For each output file:
  subagent_type: "general-purpose", model: "haiku"
  Prompt: "Evaluate this output against quality criteria.

  Input: {input data}
  Output: {output data or screenshot image}

  Criteria:
  1. {name}: {evaluationGuide} [weight: {weight}]
  2. ...

  For each criterion return: PASS/PARTIAL/FAIL, evidence, severity if fail."
```

**For screenshots:** Subagent reads the image file. Claude evaluates visual criteria (layout, overflow, data rendering, responsive behavior).

**For fewer than 5 outputs:** Evaluate inline without subagents.

#### Step 3.3: Aggregate and Compare

- Calculate per-criterion pass rates
- Identify patterns ("all adversarial inputs fail criterion X")
- Compare with previous run if available (score changes, new passes/failures)
- Generate actionable recommendations

#### Step 3.4: Write Judgment

**`judgment.md`** at `judgments/run-{timestamp}/judgment.md`:

```markdown
# Semantic QA Judgment: {suite-name}
**Run**: {timestamp}
**Suite type**: {backend|frontend}

## Summary: {passed}/{total} PASS

## Criteria Scorecard

| Criterion | Weight | Pass Rate | Notes |
|-----------|--------|-----------|-------|
| {name}    | must-pass | 8/10   | Edge cases weak |

## Detailed Findings

### {input-id} — PASS/PARTIAL/FAIL
| Criterion | Result | Evidence |
|-----------|--------|----------|
| ...       | ...    | ...      |

## Recommendations
- {Actionable items based on failure patterns}
```

**`judgment.json`** — Structured version following Shipkit Artifact Convention. See `references/output-schema.md`.

#### Step 3.5: Present Summary

```
✅ Semantic QA complete: api-pipeline

📊 Score: 85 (↑5 from last run)
  Must-pass: 9/10 ✓
  Important: 7/8
  Nice-to-have: 5/6

⚠️ Failures:
  • SQ-002 Factual Accuracy — adversarial-003 hallucinated a price
  • SQ-003 Format Compliance — edge-case-007 returned plain text, not JSON

📁 Full report: .shipkit/semantic-qa/suites/api-pipeline/judgments/run-{timestamp}/
```

---

### Step 4: Full Mode (`--full`)

Run Setup (if needed) → Run → Judge sequentially.

---

### Step 5: Fidelity Mode (`--fidelity`)

**Goal:** Score a *built* app against the *intent that was captured* — how faithfully what shipped matches
what the user envisioned. This is the evaluation half of Shipkit's outcome (**fidelity**). It produces a
**fidelity scorecard** (`.shipkit/fidelity-scorecard.json`) on two separate axes:

- **Completeness (deterministic, no LLM)** — declared surfaces (from the spec's no-gaps `gapReport`) vs
  built-and-backed (from review-shipping's `dataReality` mock-seam scan). A count/ratio.
- **Essence (LLM-judge)** — the shipped UI/behaviour scored against the product-definition **essence block**
  (each `nonNegotiable` differentiator assertion + each `qualityBar` assertion → pass / partial / fail with
  evidence). This is the normal Judge loop with the essence block as its criteria source.

The two axes are kept **separate** — never blended into one number that hides a failure. The full schema,
formulas, verdict rule, and worked examples live in `references/fidelity-scorecard-schema.md`. Read it before
running this mode.

#### Step 5.1: Locate the rubric (captured intent)

| Need | Read | Extract |
|------|------|---------|
| Declared surfaces | `.shipkit/specs/**/*.json` → `functionalSurface` (top-level, beside `gapReport`) | `functionalSurface.*[]` with `verdict: "COVERED"`; `gapReport.unbackedSurfaces[]` |
| Built-and-backed | `verification-report.json` (from `/shipkit-review-shipping`) | `dataReality.mockSeams[]` where `declaredLive: true` |
| Essence assertions | `.shipkit/product-definition.json` | `differentiators[]` where `nonNegotiable: true` (via `assertion`) + every `qualityBar[]` (via `assertion`) |

If `verification-report.json` is missing, run `/shipkit-review-shipping` first (its Data-Reality Gate
produces `dataReality`) — the completeness axis is more accurate with it. If the essence block is missing
(`qualityBar` absent or no `assertion` fields), run `/shipkit-product-definition` to capture it — this mode
scores against essence, it does not invent it.

#### Step 5.2: Completeness axis (run the tool — do not compute this by hand)

**The completeness axis is deterministic arithmetic, so it is a CLI, not a judgement.** `tools/fidelity/`
ships with this skill and emits `references/fidelity-scorecard-schema.md` verbatim. Run it. Do not
re-implement the formula in prose — a model re-deriving arithmetic is exactly how this axis drifts.

Resolve the tool path (it lives beside this SKILL.md, so it follows the install scope):

```bash
# Project-scope install first, then user-scope. Use whichever exists.
FID=".claude/skills/shipkit-semantic-qa/tools/fidelity"
[ -d "$FID" ] || FID="$HOME/.claude/skills/shipkit-semantic-qa/tools/fidelity"
```

Single arm:

```bash
python "$FID/fidelity-score.py" . \
  --spec .shipkit/specs/shipped/*.json \
  --verification-report .shipkit/verification-report.json \
  --product-definition .shipkit/product-definition.json \
  --out .shipkit/fidelity-scorecard.json \
  --stamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --report
```

- `--spec` is the **denominator's provenance** — the declared list, not a code re-scan. Required.
- `--verification-report` is preferred when present: review-shipping owns the Data-Reality Gate, so its
  `dataReality.mockSeams` is authoritative and the tool will not re-scan behind it. Omit it and the tool
  runs its own bundled `mock-seam-detector.py` instead.
- `--stamp` is the only source of `lastUpdated`; omit it and repeated runs stay byte-identical.

**Read these two fields before trusting the number:**

| Field | Why it matters |
|-------|----------------|
| `completeness.signals` | **Advisory only** — a heuristic code-scan blend that never moves `ratio` or the verdict. Leads for a human. Do not report `signals.blendedScore` as the completeness score. |
| `completeness.signals.declaredCoverage` | Declared surfaces with **no code evidence**. The contract's formula is optimistic (`builtAndBacked = declared − |notBacked|`), so a surface nobody built and nobody flagged still counts as **built** — an empty codebase scores `1.0`. If `unresolved > 0`, the ratio is an **upper bound**: say so, and check those surfaces by hand before calling the build complete. |

The tool leaves `essence: null` and `fidelityVerdict: null` — it has no judge, and it will not guess the
half it cannot prove. Step 5.3 fills essence; Step 5.4 derives the verdict.

#### Step 5.3: Essence axis (LLM-judge)

Set up a **frontend** suite with `criteriaSource: "essence"` and derive criteria from the essence block:

| Essence element | Criterion | Weight |
|-----------------|-----------|--------|
| `differentiators[]` with `nonNegotiable: true` | `id` = the `D-00x`, `evaluationGuide` = its `assertion`, `dimension: "differentiator"` | `must-pass` (essence **floor**) |
| every `qualityBar[]` item | `id` = the `Q-00x`, `evaluationGuide` = its `assertion`, `dimension` = the item's `dimension` | `important` |

Use `enabledBy` / `appliesTo` to route each assertion to the surface(s) to screenshot. Then run the normal
Run → Judge loop (Steps 2–3) to score each assertion `pass` / `partial` / `fail` with evidence. Compute:

```
per-criterion credit: pass = 1.0, partial = 0.5, fail = 0
essenceScore = weighted average in 0-100 (must-pass 3, important 2, nice-to-have 1)
floorHeld    = every nonNegotiable differentiator scored PASS (any partial/fail → floor broken)
```

`floorHeld: false` with a high `essenceScore` is still **taste-drift** — report both honestly.

**Write the result to `.shipkit/semantic-qa/essence.json`** — Step 5.4 reads it back to derive the verdict.
`score` and `floorHeld` are required (the tool rejects the file without them); `results[]` carries the
per-assertion detail through to the scorecard:

```json
{
  "score": 72,
  "floorHeld": false,
  "differentiators": { "pass": 2, "partial": 1, "fail": 0 },
  "qualityBar": { "pass": 2, "partial": 0, "fail": 1 },
  "results": [
    { "id": "D-003", "kind": "differentiator", "nonNegotiable": true,
      "assertion": "Preview streams first content within 2s of any parameter change.",
      "result": "partial",
      "evidence": "Preview streams, but first content measured at ~4.1s — over the 2s budget." }
  ]
}
```

#### Step 5.4: Compose the scorecard + verdict

**Re-run the tool with `--essence`** so the verdict is derived in code from both axes. The schema says
`fidelityVerdict` is derived and never entered by hand — that means the rule table below is documentation of
what the tool does, not a procedure for you to apply:

```bash
# .shipkit/semantic-qa/essence.json was written by Step 5.3.
python "$FID/fidelity-score.py" . \
  --spec .shipkit/specs/shipped/*.json \
  --verification-report .shipkit/verification-report.json \
  --product-definition .shipkit/product-definition.json \
  --essence .shipkit/semantic-qa/essence.json \
  --out .shipkit/fidelity-scorecard.json \
  --stamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)" --report
```

The scorecard lands at `.shipkit/fidelity-scorecard.json` (run-scoped under `<runDir>/` when the engine set
a run root — `install/shared/references/run-artifacts.md`; pass `--out <runDir>/fidelity-scorecard.json`).

The rule the tool applies (`--essence-threshold` sets the `80`, recorded as `essenceThreshold`):

| Verdict | Rule |
|---------|------|
| `FAITHFUL` | `ratio == 1.0` **and** `floorHeld` **and** `essenceScore >= 80` |
| `GAP-DRIFT` | `ratio < 1.0` (a declared surface missing or green-but-mock) |
| `TASTE-DRIFT` | `floorHeld == false` **or** `essenceScore < 80` |
| `GAP+TASTE-DRIFT` | both |

If you skip `--essence`, `fidelityVerdict` stays `null` on purpose: with completeness alone, `ratio < 1.0`
cannot distinguish `GAP-DRIFT` from `GAP+TASTE-DRIFT`, and `ratio == 1.0` cannot distinguish `FAITHFUL` from
`TASTE-DRIFT`. Report `completeness.verdict` (the provable half) rather than guessing the rest.

#### Step 5.5: Comparative mode (two arms, one rubric)

Same brief, two builds (e.g. **Shipkit-built** vs **raw-built**) scored against **one shared rubric**. The
rubric — declared-surface list + essence assertions — is fixed from a **single source of truth** (the
captured intent), and each arm is scored against it:

- **Completeness per arm:** one tool invocation scores every arm against the same `--spec`, so the shared
  rubric is enforced by construction rather than by care:

```bash
python "$FID/fidelity-score.py" \
  --arm shipkit=../arm-shipkit --arm raw=../arm-raw \
  --spec .shipkit/specs/shipped/*.json \
  --product-definition .shipkit/product-definition.json \
  --out .shipkit/fidelity-scorecard.json --report
```

- **Essence per arm:** run the essence judge against *each arm's shipped screens* with the identical criteria.

`mode`, `arms[]` and the `comparison` block (completeness / essence / floor deltas + winner) are emitted for
you; `rubricSource` records the rubric's provenance (see the schema reference's note on rubric provenance).
The **fidelity delta** is the deliverable Project A consumes.

> **Check `declaredCoverage` on every arm before quoting a winner.** Because the completeness formula is
> optimistic, an arm that simply *never built* a declared surface is not penalised for it — a near-empty arm
> scores `1.0`. The tool flags this in `comparison.notes` when any arm has unresolved surfaces, and the delta
> is only meaningful once both arms' declared surfaces are actually accounted for.

#### Step 5.6: Present

```
📐 Fidelity Scorecard — WorksheetForge (single)

Completeness  5/6  (0.83)   ⚠️ gap-drift
  • differentiated-sets-view — declared live, still on SAMPLE_SETS (mock seam)
Essence       72 · floor NOT held   ⚠️ taste-drift
  • D-003 streaming-preview PARTIAL — first content ~4.1s (budget 2s)
  • Q-003 error-recovery FAIL — raw stack trace on export failure

Verdict: GAP+TASTE-DRIFT
📁 .shipkit/fidelity-scorecard.json
```

---

## When This Skill Integrates with Others

### Before This Skill
- `/shipkit-spec` — Acceptance criteria can seed quality criteria; its `gapReport` (declared surfaces) is the completeness-axis rubric in fidelity mode
  - **When:** Feature has a spec with defined acceptance criteria
  - **Why:** Derives initial criteria from existing spec; fidelity mode reads the no-gaps `gapReport`
- `/shipkit-product-definition` — Produces the **essence block** (`nonNegotiable` differentiators + `qualityBar`) fidelity mode scores against
  - **When:** Running `--fidelity` — the essence axis needs captured, checkable assertions
- `/shipkit-review-shipping` — Its Data-Reality Gate produces `verification-report.json` `dataReality` (built-and-backed / mock seams)
  - **When:** Running `--fidelity` — the completeness axis reads this
- `/shipkit-project-context` — Provides stack.json for script generation
  - **When:** Need to determine API framework or test runner

### After This Skill
- `/shipkit-review-shipping` — Can reference judgment findings during review
  - **When:** Judgment reveals quality issues before commit
- No automatic follow-up. User decides next action.

### Related Skills
- `shipkit-test-cases` — Defines WHAT to test at unit/integration level (complementary)
- `shipkit-ux-audit` — Audits UX design patterns (complementary: design vs visual regression)
- `shipkit-prompt-audit` — Audits prompt architecture (complementary: structure vs output quality)

---

## Context Files This Skill Reads

| File | Purpose |
|------|---------|
| `.shipkit/semantic-qa/config.json` | Global config, suite list |
| `.shipkit/semantic-qa/suites/{suite}/suite.json` | Criteria, run strategy, script path |
| `.shipkit/semantic-qa/suites/{suite}/inputs/*.json` | Test inputs (backend) |
| `.shipkit/semantic-qa/suites/{suite}/components/inventory.json` | Component list (frontend) |
| `.shipkit/semantic-qa/suites/{suite}/outputs/run-{ts}/*` | Outputs to judge |
| `.shipkit/semantic-qa/suites/{suite}/screenshots/run-{ts}/*` | Screenshots to judge |
| `.shipkit/semantic-qa/suites/{suite}/judgments/` | Previous judgments for comparison |
| `.shipkit/stack.json` | Optional: tech stack for script generation |
| `.shipkit/specs/` | Optional: seed criteria from acceptance criteria |
| `.shipkit/product-definition.json` | **Fidelity mode:** essence block (`nonNegotiable` differentiators + `qualityBar`) = the essence-axis criteria |
| `.shipkit/specs/**/*.json` (`functionalSurface` + `gapReport`) | **Fidelity mode:** declared surfaces (the completeness denominator) + `unbackedSurfaces`. Passed to the tool as `--spec`. |
| `verification-report.json` (`dataReality`) | **Fidelity mode:** built-and-backed / mock-seam data for the completeness axis. Passed as `--verification-report`; authoritative when present. |

---

## Context Files This Skill Writes

**Write strategies:**
- `config.json` — OVERWRITE (single global config)
- `suite.json` — OVERWRITE (updated when criteria or strategy change)
- `inputs/*.json` — APPEND (add new inputs, preserve existing)
- `components/inventory.json` — OVERWRITE (regenerated on change)
- `outputs/`, `screenshots/` — CREATE per run (gitignored, ephemeral)
- `judgments/` — APPEND (one per run, kept permanently)
- `scripts/semantic-qa-{suite}.*` — CREATE on setup, user-owned after
- `semantic-qa/essence.json` — CREATE per fidelity run (Step 5.3): the essence axis (`score` + `floorHeld` + `results[]`). Read back by Step 5.4 as `--essence` so the verdict is derived, not hand-entered.
- `fidelity-scorecard.json` — CREATE per fidelity run (run-scoped under `<runDir>/` when the engine set a run root, else `.shipkit/`)

---

## What This Skill Does NOT Do

- Execute unit/integration tests (handled during team implementation)
- Auto-fix quality issues (reports only, user decides)
- Replace CI/CD test suites
- Judge prompt text quality (that's `prompt-audit`)
- Persist results to external systems

---

<!-- SECTION:success-criteria -->
## Success Criteria

**Setup complete when:**
- [ ] Suite type determined (backend or frontend)
- [ ] Quality criteria captured from user with weights and evaluation guides
- [ ] Input library or component inventory created
- [ ] Test script generated in `scripts/`
- [ ] `suite.json` written with criteria and run strategy
- [ ] `.gitignore` updated for outputs/screenshots

**Run complete when:**
- [ ] Script executed successfully
- [ ] Outputs collected and counted
- [ ] Any failures reported with error details

**Judge complete when:**
- [ ] All outputs/screenshots read and evaluated
- [ ] Each output scored against each criterion
- [ ] Judgment report written (markdown + JSON)
- [ ] Summary with score and comparison presented to user

**Fidelity complete when:**
- [ ] Rubric located: essence block (product-definition), declared surfaces (`functionalSurface`), `dataReality` (verification-report)
- [ ] Completeness axis produced by **running `tools/fidelity/fidelity-score.py`** with `--spec` — not computed by hand
- [ ] `signals.declaredCoverage` checked: any `unresolved > 0` reported as "ratio is an upper bound", not glossed
- [ ] Essence axis judged against every `nonNegotiable` differentiator + `qualityBar` assertion (`floorHeld` computed)
- [ ] `fidelity-scorecard.json` written with both axes separate + `fidelityVerdict` **derived by the tool** (`--essence`), never entered by hand
- [ ] Comparative runs: all arms scored in one invocation against one `--spec` + `comparison` deltas emitted
<!-- /SECTION:success-criteria -->

---

<!-- SECTION:after-completion -->
## After Completion

QA judgment written to `.shipkit/semantic-qa/suites/{suite-name}/judgments/run-{timestamp}/judgment.md` (and `judgment.json`).

**Next:**
- If **quality gaps found**: fix the underlying artifact (prompts, definitions, specs) and re-run this skill. For systemic pattern issues, log decisions in `/shipkit-engineering-definition`.
- If **judgment passes**: proceed to the next workflow step — typically `/shipkit-review-shipping` (if QAing implemented features before commit) or back to `/shipkit-spec` refinement (if QAing spec-derived criteria).

This skill is a judgment gate; it does not auto-dispatch fixes.
<!-- /SECTION:after-completion -->

---

## References

- `references/output-schema.md` — JSON schema for judgment.json
- `references/criteria-guide.md` — How to write effective quality criteria
- `references/example.json` — Complete example judgment output
- `references/fidelity-scorecard-schema.md` — **Fidelity mode:** scorecard schema (completeness + essence + comparative), formulas, verdict rule, two worked examples
- `tools/fidelity/` — **Fidelity mode:** the deterministic producer of the completeness axis. `fidelity-score.py` emits the scorecard schema; `mock-seam-detector.py` does the declared-live cross-check (also used by `shipkit-review-shipping`'s Data-Reality Gate). See `tools/fidelity/README.md` for the formula, the known limits, and the `_smoke/` fixture.
