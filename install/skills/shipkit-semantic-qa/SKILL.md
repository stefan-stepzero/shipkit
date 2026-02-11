---
name: shipkit-semantic-qa
description: "Semantic QA — define inputs/criteria, generate test scripts, Claude judges API outputs or UI screenshots against quality criteria. Triggers: 'semantic qa', 'quality check', 'visual qa', 'judge outputs', 'QA suite'."
argument-hint: "[suite-name] [--setup|--run|--judge|--full]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task
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

### Step 0: Mode Detection

Determine mode from arguments and state:

**Explicit flag provided:**
- `--setup` → Setup mode
- `--run` → Run mode
- `--judge` → Judge mode
- `--full` → Setup (if needed) → Run → Judge

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
Launch Task agents IN PARALLEL:

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

## When This Skill Integrates with Others

### Before This Skill
- `/shipkit-spec` — Acceptance criteria can seed quality criteria
  - **When:** Feature has a spec with defined acceptance criteria
  - **Why:** Derives initial criteria from existing spec
- `/shipkit-project-context` — Provides stack.json for script generation
  - **When:** Need to determine API framework or test runner

### After This Skill
- `/shipkit-verify` — Can reference judgment findings during review
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

---

## What This Skill Does NOT Do

- Execute unit/integration tests (that's `test-relentlessly`)
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
<!-- /SECTION:success-criteria -->

---

<!-- SECTION:after-completion -->
## After Completion

**After Setup:** User can customize the generated script, add more inputs, then `--run`.
**After Run:** Outputs ready. Run `--judge` or let `--full` continue automatically.
**After Judge:** User reviews findings. Fix issues and re-run, or accept quality level.

No automatic follow-up. Natural capabilities handle fixing code based on findings.
<!-- /SECTION:after-completion -->

---

## References

- `references/output-schema.md` — JSON schema for judgment.json
- `references/criteria-guide.md` — How to write effective quality criteria
- `references/example.json` — Complete example judgment output
