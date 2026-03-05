---
name: shipkit-validate-wiring
description: Validates wiring contracts between installed Shipkit components. Static mode checks dispatch chains, artifact flow, and tool conflicts against DOC-025. Walkthrough mode simulates orchestration loops step-by-step.
argument-hint: "[--static] [--walkthrough] [--refresh] [--loop N]"
---

# shipkit-validate-wiring - Wiring Contract Validator

**Purpose**: Validate that all wiring contracts between installed Shipkit skills and agents are correct — dispatch chains connect, artifact flows have upstream writers, and tool restrictions don't conflict.

**Two modes**:
- `--static` (default): Inline checks against DOC-025 JSON — fast, no agents needed
- `--walkthrough`: Dispatches 3 parallel agents to simulate each orchestration loop step-by-step

---

## When to Invoke

**User says:**
- "Validate wiring"
- "Check dispatch chains"
- "Are there wiring issues?"
- "Simulate orchestration flow"
- "Walkthrough the pipeline"

**Use when:**
- After modifying skill/agent frontmatter or body dispatch references
- After running `/shipkit-wiring-graph`
- Before release, as part of pre-flight validation
- When debugging unexpected dispatch failures

---

## Prerequisites

**Required**:
- Running from Shipkit framework repo root
- DOC-025 JSON exists at `docs/development/system-design/DOC-025-wiring-graph.json`
  - If missing, prompt user to run `/shipkit-wiring-graph` first
  - If `--refresh` flag present, run `/shipkit-wiring-graph` before validation

---

## Mode 1: Static Checks (`--static`, default)

Run all checks inline (no agents needed). Read DOC-025 JSON and apply the check catalog from `references/wiring-checks.md`.

### Process

1. Read `docs/development/system-design/DOC-025-wiring-graph.json`
2. Check staleness: compare DOC-025 `generatedAt` against latest modification time of any file in `install/skills/` or `install/agents/`. If DOC-025 is older, emit WARNING: "Wiring graph is stale — run /shipkit-wiring-graph --refresh"
3. For each check in the catalog (see `references/wiring-checks.md`), evaluate against the DOC-025 data
4. Collect results by severity: BLOCK, WARN, NOTE

### Report Format

```
============================================
WIRING VALIDATION REPORT (Static)
============================================
Timestamp: {now}
DOC-025 generated: {generatedAt}
Staleness: {fresh | STALE — install/ modified after DOC-025}

BLOCK ISSUES (must fix)
───────────────────────
{W-001: Agent binding exists — ...}
{W-003: Dispatch target exists — ...}
...or "None"

WARNINGS (should fix)
─────────────────────
{W-101: Model mismatch — ...}
...or "None"

NOTES (informational)
─────────────────────
{W-201: Shared agent — ...}
...or "None"

============================================
SUMMARY
============================================
BLOCK:    {N}
WARN:     {N}
NOTE:     {N}

RESULT: {PASS | FAIL (N blockers)}
============================================
```

---

## Mode 2: Walkthrough (`--walkthrough`)

Dispatches 3 parallel agents, each simulating one orchestration loop. Each agent traces through the dispatch order step-by-step, tracking artifact state and checking input availability.

### Process

Launch ALL 3 agents simultaneously using the Agent tool. Each agent is `subagent_type: "general-purpose"` with `model: "sonnet"`.

---

#### Agent W1: Direction Loop Walkthrough

**Prompt:**
```
Simulate the Direction loop of Shipkit's orchestration pipeline.

Read the wiring graph at P:\Projects2\sg-shipkit\docs\development\system-design\DOC-025-wiring-graph.json.

Starting state: No .shipkit/ artifacts exist (greenfield project). Only README and codebase exist.

Walk through the Direction loop's dispatch order:
1. /shipkit-why-project → produces what? Needs what inputs?
2. /shipkit-vision → produces what? Needs what inputs? Are they available now?
3. /shipkit-stage → produces what? Needs what inputs?
4. /shipkit-product-goals → produces what? Needs what inputs?
5. /shipkit-engineering-goals → produces what? Needs what inputs?
6. /shipkit-review-direction → reads what? Produces what assessment?

At each step:
- List the skill's reads (from DOC-025)
- Check if all reads are available in the cumulative artifact state
- List the skill's writes (from DOC-025)
- Add writes to cumulative state
- Flag any MISSING INPUT (read required but no upstream writer has produced it yet)

Then simulate a re-dispatch scenario:
- Assume reviewer-direction finds a gap (e.g., "vision doesn't align with updated why")
- Can the orchestrator re-dispatch /shipkit-vision? Are its inputs still available?
- Trace the re-dispatch through the DOC-025 data

Report format:
DIRECTION LOOP WALKTHROUGH
Step 1: /shipkit-why-project
  Inputs required: [list]
  Inputs available: [list]
  Missing: [list or "none"]
  Produces: [list]
  Cumulative state: [list of all artifacts now available]
...
RE-DISPATCH SIMULATION
  Trigger: {scenario}
  Re-dispatched skill: {name}
  Inputs available: {yes/no + details}
  Result: {success/blocked + reason}
ISSUES FOUND: [list or "none"]
```

---

#### Agent W2: Planning Loop Walkthrough

**Prompt:**
```
Simulate the Planning loop of Shipkit's orchestration pipeline.

Read the wiring graph at P:\Projects2\sg-shipkit\docs\development\system-design\DOC-025-wiring-graph.json.

Starting state: Direction loop has completed. These artifacts exist:
- .shipkit/why.json
- .shipkit/vision.json
- .shipkit/goals/strategic.json
- .shipkit/goals/product.json (draft)
- .shipkit/goals/engineering.json (draft)
- .shipkit/reviews/direction-assessment.json

Walk through the Planning loop's dispatch order:
1. /shipkit-product-discovery
2. /shipkit-product-definition
3. /shipkit-engineering-definition
4. /shipkit-product-goals (refined)
5. /shipkit-engineering-goals (refined)
6. /shipkit-spec-roadmap
7. /shipkit-spec
8. /shipkit-user-instructions
9. /shipkit-review-planning

At each step:
- List reads, check availability, list writes, update cumulative state
- Flag MISSING INPUT or IMPLICIT DEPENDENCY (input available but not explicitly in DOC-025 reads)

Then simulate re-dispatch:
- Assume reviewer-planning finds: "spec doesn't cover a product requirement"
- Can orch-planning re-dispatch /shipkit-product-definition then /shipkit-spec?

Report format: Same as Direction agent (step-by-step + re-dispatch simulation + issues).
```

---

#### Agent W3: Shipping Loop Walkthrough

**Prompt:**
```
Simulate the Shipping loop of Shipkit's orchestration pipeline.

Read the wiring graph at P:\Projects2\sg-shipkit\docs\development\system-design\DOC-025-wiring-graph.json.

Starting state: Direction + Planning loops complete. All direction and planning artifacts exist:
- .shipkit/why.json, vision.json, goals/strategic.json, goals/product.json, goals/engineering.json
- .shipkit/product-discovery.json, product-definition.json, engineering-definition.json
- .shipkit/spec-roadmap.json, specs/todo/*.json, user-instructions.json
- .shipkit/reviews/direction-assessment.json, planning-assessment.json

Walk through the Shipping loop's dispatch order:
1. /shipkit-plan
2. /shipkit-test-cases
3. /shipkit-team (creates Agent Team for parallel implementation)
4. /shipkit-verify (reviewer-shipping runs QA, may dispatch sub-skills)
5. /shipkit-preflight

At each step:
- List reads, check availability, list writes, update cumulative state
- For /shipkit-verify: trace which QA sub-skills it can dispatch (ux-audit, semantic-qa, qa-visual, prompt-audit) and what they need

Then simulate re-dispatch:
- Assume verify finds failing tests + UX gap
- Can orch-shipping re-dispatch /shipkit-team? Are inputs available?
- After re-implementation, can verify run again?

Report format: Same as Direction agent (step-by-step + re-dispatch simulation + issues).
```

---

### Aggregate Walkthrough Results

After all 3 agents return:

1. Collect all MISSING INPUT and IMPLICIT DEPENDENCY issues
2. Collect all re-dispatch simulation results
3. Report in combined format:

```
============================================
WIRING WALKTHROUGH REPORT
============================================
Timestamp: {now}

DIRECTION LOOP
──────────────
{Agent W1 summary — steps with issues highlighted}

PLANNING LOOP
─────────────
{Agent W2 summary — steps with issues highlighted}

SHIPPING LOOP
─────────────
{Agent W3 summary — steps with issues highlighted}

============================================
CROSS-LOOP ISSUES
============================================
{Issues that span loops — e.g., planning reads an artifact direction doesn't produce}

============================================
SUMMARY
============================================
Steps traced: {N}
Missing inputs: {N}
Implicit dependencies: {N}
Re-dispatch simulations: {N passed}/{N total}

RESULT: {PASS | ISSUES FOUND (N)}
============================================
```

---

## Loop Mode

When invoked with `--loop N`, the skill runs iteratively — checking, fixing, and re-checking.

**State file**: `.shipkit/validate-wiring-loop.local.md`

**Default completion promise**: "Wiring validation reports zero BLOCK issues"

**How it works**:
1. Parse `--loop N` from arguments (default N=3 if omitted)
2. Create state file with frontmatter (skill, iteration, max_iterations, completion_promise)
3. Run the validation (static or walkthrough based on flags)
4. Update the Progress section in the state file with findings
5. If zero BLOCK issues → delete state file, report success, stop
6. If BLOCK issues remain → end response; the relentless stop hook blocks exit and re-prompts

**Shared reference**: See `.claude/skills/_shared/loop-mode-reference.md` for state file format and protocol details.

---

## Output

- Console report (always)
- State file (only in `--loop` mode): `.shipkit/validate-wiring-loop.local.md`

---

## When This Skill Integrates with Others

### Before This Skill
- Run `/shipkit-wiring-graph` to generate/refresh DOC-025
- Or use `--refresh` flag to auto-trigger wiring graph generation

### After This Skill
- Fix any BLOCK issues found
- Re-run to verify fixes (or use `--loop N` for iterative fix-validate)

### Related Skills
- `shipkit-wiring-graph` — Generates the DOC-025 wiring graph this skill validates
- `shipkit-framework-integrity` — Validates structural integrity (manifest, references, hooks)
- `shipkit-dev-review` — Reviews framework changes for design quality
