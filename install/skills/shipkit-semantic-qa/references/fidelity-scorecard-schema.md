# Fidelity Scorecard Schema

The **fidelity scorecard** scores a *built* app against the *intent that was captured* — how faithfully
what shipped matches what the user envisioned. It is the evaluation half of Shipkit's outcome
(**fidelity**), and it is produced by `shipkit-semantic-qa` in **fidelity mode** (`--fidelity`).

Two axes, deliberately kept **separate** (never blended into one number that hides a failure):

| Axis | How scored | Source of truth |
|------|-----------|-----------------|
| **Completeness** | Deterministic count/ratio — no LLM | spec `gapReport` (declared surfaces) vs review-shipping `dataReality` (built-and-backed) |
| **Essence** | LLM-judge (pass / partial / fail per assertion, with evidence) | product-definition **essence block** (`nonNegotiable` differentiators + `qualityBar`) |

The enemy is **drift**: *gap-drift* (incomplete — the completeness axis) or *taste-drift* (generic — the
essence axis). The scorecard makes both visible at once so neither hides behind a healthy average.

Artefact path: `.shipkit/fidelity-scorecard.json` (run-scoped under `<runDir>/` when the engine set a run
root — see `install/shared/references/run-artifacts.md`; `.shipkit/` otherwise).

---

## Axis 1 — Completeness (deterministic)

**Declared surfaces** come from the spec's `functionalSurface`. **Built-and-backed** comes from
review-shipping's `dataReality` mock-seam scan (the build-time counterpart of the spec-time no-gaps gate).
No model judgement — this is arithmetic over two JSON artefacts.

> **This axis has a producer: `tools/fidelity/fidelity-score.py`, which ships with this skill.** It emits this
> schema. Run it rather than re-deriving the arithmetic in prose — see SKILL.md Step 5.2.

### Inputs

| Input | From | Field |
|-------|------|-------|
| Declared surfaces | `.shipkit/specs/**/*.json` → `functionalSurface` (**top-level**, a sibling of `gapReport`) | `functionalSurface.{applications,datastores,contracts,integrations}[]` with `verdict: "COVERED"` |
| Unbacked shared surfaces | same spec | `gapReport.unbackedSurfaces[]` — note this is **normally empty by construction**: a spec cannot be saved unless `gapReport.status` is `clear`, which requires it. It is read anyway, to cover hand-edited / in-flight / legacy specs. |
| Mock seams on built code | `verification-report.json` (review-shipping) | `dataReality.mockSeams[]` where `declaredLive: true` |

### Formula

```
D  = count of functionalSurface elements across all four dimensions with verdict == "COVERED"
       (EXPLICITLY-DEFERRED and FLAGGED are excluded — deferred is out of scope on purpose;
        flagged means the spec gate never cleared, so it was never a declared-live surface)

notBacked = distinct surfaces that are EITHER
              - listed in gapReport.unbackedSurfaces[]        (declared but no owning SSOT), OR
              - the surface of a dataReality.mockSeams[] entry with declaredLive == true
                                                              (built, but still reading mock/stub data)

builtAndBacked = D - |notBacked|
completenessRatio = builtAndBacked / D          (D == 0 → ratio is "n/a", state why)
```

`byDimension` breaks the ratio down across applications / datastores / contracts / integrations so a
missing backend contract is not masked by a fully-built frontend.

A **declared-live surface reading mock data counts as NOT built** — green-but-mock is not done. This is the
same rule review-shipping's Data-Reality Gate enforces; the scorecard just aggregates it into a ratio.

### Known limit: the formula is optimistic — `ratio` is an upper bound

`builtAndBacked = D − |notBacked|` subtracts only surfaces something **names**: an `unbackedSurfaces[]` entry
or a declared-live mock seam. A declared surface that was **simply never built** is named by neither, so it
counts as *built*. Taken to its limit, an **empty codebase scores `ratio: 1.0`**.

This is deliberate. The alternative — proving "declared element X exists nowhere in this codebase" from a name
like `web-ui` — is an unprovable negative, and manufacturing findings from it is what put the v1 detectors at
~27–30% precision. The contract buys precision with a known blind spot rather than paying for recall in false
FAILs on surfaces nobody declared.

Two consequences, and neither is optional:

- **`completeness.signals.declaredCoverage`** (advisory) lists declared elements with no code evidence. When
  `unresolved > 0`, `ratio` is an **upper bound** — report it as such and check those surfaces by hand.
- **In comparative mode this can invert the winner.** An arm that never built a surface is not penalised for
  it, so a barely-built arm can out-score a complete one. `comparison.notes` flags any arm with unresolved
  surfaces; the delta is only meaningful once both arms' declared surfaces are accounted for.

### `completeness.signals` — advisory, never gating

The producer also emits a heuristic code-scan read (`surfaces`/`seams`/`ssot`, weights emitted) under
`completeness.signals`. It is **not** this axis's completeness and **never** moves `ratio` or
`fidelityVerdict`. It is kept because it catches what the contract's formula structurally cannot (a surface
with no backing at all, duplicated truth). Read it as leads for a human. Do not report `signals.blendedScore`
as the completeness score.

---

## Axis 2 — Essence (LLM-judge, via semantic-qa)

The essence assertions are the criteria. semantic-qa loads them from the product-definition **essence block**
instead of hand-authored criteria (`criteriaSource: "essence"`), then runs its normal Judge loop against the
shipped UI/behaviour (screenshots + interaction traces).

### Criteria mapping (essence block → semantic-qa criteria)

| Essence element | Becomes a criterion with | Weight |
|-----------------|--------------------------|--------|
| `differentiators[]` where `nonNegotiable: true` — scored via its `assertion` | `id` = the `D-00x` id, `name` = `statement`, `evaluationGuide` = `assertion`, `dimension: "differentiator"` | `must-pass` (the **essence floor** — must ship faithfully) |
| every `qualityBar[]` item — scored via its `assertion` | `id` = the `Q-00x` id, `evaluationGuide` = `assertion`, `dimension` = the item's `dimension` | `important` (the bar it holds itself to — a miss drags the score, isn't a hard floor break) |

Differentiators with `nonNegotiable: false` (or explicitly de-scoped) are **not** part of the essence floor;
include them only as `nice-to-have` if scored at all. `appliesTo` / `enabledBy` route each assertion to the
right shipped surface(s) to screenshot.

### Essence scoring

Each assertion is judged `pass` / `partial` / `fail` with evidence (reuse the standard semantic-qa judgment).
Per-criterion credit: `pass = 1.0`, `partial = 0.5`, `fail = 0`.

```
essenceScore = weighted average of per-criterion credit, in 0-100
                 must-pass weight 3, important weight 2, nice-to-have weight 1
                 (same weighting as the standard judgment score)

floorHeld = every nonNegotiable differentiator scored PASS
              (any partial or fail on a nonNegotiable differentiator → floorHeld = false → taste-drift)
```

`floorHeld` is the honest gate: a high `essenceScore` with a broken floor is still **taste-drift**, because a
non-negotiable differentiator did not ship faithfully. Report both.

---

## Combined verdict (per arm) — keep the axes visible

Do **not** collapse completeness and essence into one blended number. Emit a `fidelityVerdict` that *names the
drift(s)* present, plus the two axis scores side by side:

| Verdict | Rule |
|---------|------|
| `FAITHFUL` | `completenessRatio == 1.0` **and** `floorHeld == true` **and** `essenceScore >= 80` |
| `GAP-DRIFT` | `completenessRatio < 1.0` — a declared surface is missing or green-but-mock |
| `TASTE-DRIFT` | `floorHeld == false` **or** `essenceScore < 80` — the app shipped generic on the essence |
| `GAP+TASTE-DRIFT` | both conditions above hold — incomplete *and* generic |

The `80` essence threshold is the v1 default; it is recorded in the scorecard (`essenceThreshold`) so it is
explicit and tunable, not buried in prose.

---

## Comparative mode (what Project A consumes)

Same brief, two (or more) arms — e.g. **Shipkit-built** vs **raw-built** — scored against **one shared
rubric**. The rubric (declared-surface list `D` + essence assertions) is fixed from a **single source of
truth**: the captured intent (the spec `gapReport` + the product-definition essence block). Both arms are
scored against that same rubric:

- **Completeness per arm:** run review-shipping's data-reality scan against *each arm's codebase* using the
  same declared-surface list → each arm gets its own `mockSeams` → its own ratio. The raw arm is scored
  against the identical `D`.
- **Essence per arm:** run the semantic-qa essence judge against *each arm's shipped screens* with the
  identical essence criteria.

The scorecard then reports each arm plus a `comparison` block with the deltas — the **fidelity delta** is the
whole point: it shows how much closer to the captured intent one arm shipped than the other.

> **Rubric provenance matters.** The rubric comes from the intent capture, not from either arm's own build.
> If only the Shipkit arm produced a spec + essence block, that capture *is* the shared rubric both arms are
> held to — that is legitimate (it is the intent both were asked to build). Record `rubricSource` so the
> provenance is auditable.

---

## Full JSON schema

```json
{
  "$schema": "shipkit-artifact",
  "type": "fidelity-scorecard",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DDTHH:MM:SSZ",
  "source": "shipkit-semantic-qa",
  "generator": "fidelity-score.py",

  "mode": "single | comparative",
  "essenceThreshold": 80,

  "rubricSource": {
    "productDefinition": ".shipkit/product-definition.json",
    "specs": [".shipkit/specs/shipped/grade-dashboard.json"],
    "declaredSurfaceCount": 6,
    "nonNegotiableDifferentiators": ["D-001", "D-002", "D-003"],
    "qualityBar": ["Q-001", "Q-002", "Q-003"]
  },

  "arms": [
    {
      "name": "string — arm label, e.g. 'shipkit' or 'raw'",
      "codebase": "string — path or ref to the built app scored",

      "completeness": {
        "declared": 6,
        "builtAndBacked": 5,
        "ratio": 0.83,
        "byDimension": {
          "applications": "2/2",
          "datastores": "1/2",
          "contracts": "1/1",
          "integrations": "1/1"
        },
        "unbackedSurfaces": [],
        "mockSeams": [
          { "surface": "coach-dashboard", "field": "grade_band", "declaredLive": true,
            "evidence": "renders MOCK_ROWS; backing view cohort_leaderboard_v never queried",
            "source": "verification-report.json#dataReality" }
        ],

        "ratioBasis": "builtAndBacked / declared",
        "mockSeamSource": "string — which artefact the seams came from",
        "verdict": "gap-drift | complete | n/a — the half provable without essence",

        "signals": {
          "_note": "ADVISORY heuristic code-scan. Never moves ratio or fidelityVerdict.",
          "blendedScore": 0.41,
          "weights": { "surfaces": 0.70, "seams": 0.15, "ssot": 0.15 },
          "surfaces": { "score": 0.33, "findings": [] },
          "seams": { "score": 0.5, "findings": [] },
          "ssot": { "score": 0.67, "findings": [] },
          "declaredCoverage": {
            "resolved": 6, "unresolved": 1,
            "elements": [
              { "name": "GET /api/cohort/{id}/leaderboard", "dimension": "contracts",
                "resolved": false, "files": [],
                "note": "no code evidence found — not built, or built under a different name (ADVISORY)" }
            ]
          }
        }
      },

      "essence": {
        "score": 67,
        "floorHeld": false,
        "differentiators": { "pass": 2, "partial": 1, "fail": 0 },
        "qualityBar": { "pass": 2, "partial": 0, "fail": 1 },
        "results": [
          {
            "id": "D-001", "kind": "differentiator", "nonNegotiable": true,
            "assertion": "One creation flow produces exactly three difficulty variants...",
            "result": "pass",
            "evidence": "Screenshot of one flow output shows below/on/advanced variants."
          },
          {
            "id": "D-003", "kind": "differentiator", "nonNegotiable": true,
            "assertion": "Preview streams first content within 2s of any parameter change...",
            "result": "partial",
            "evidence": "Preview updates but blank-spinner measured at ~4s on first change — floor broken."
          },
          {
            "id": "Q-003", "kind": "qualityBar", "dimension": "error",
            "assertion": "Every generation/export failure shows a specific recoverable message...",
            "result": "fail",
            "evidence": "Export failure surfaces a raw stack trace on /export."
          }
        ]
      },

      "fidelityVerdict": "GAP+TASTE-DRIFT"
    }
  ],

  "comparison": {
    "completenessDelta": "string — e.g. 'shipkit +0.17' (winner arm relative to other)",
    "essenceDelta": "string — e.g. 'shipkit +31'",
    "floorDelta": "string — e.g. 'shipkit holds floor; raw breaks D-001'",
    "winner": "string — arm name with higher fidelity, or 'tie'",
    "notes": ["string — what drove the delta"]
  }
}
```

`comparison` is present only in `mode: "comparative"`. In `mode: "single"` there is exactly one arm and no
`comparison` block.

### Field notes

- `completeness.mockSeams[]` mirrors `verification-report.json` `dataReality.mockSeams` entries with
  `declaredLive: true`; it is copied (not recomputed) so the scorecard is self-contained and auditable.
- `essence.results[]` is the semantic-qa judgment `evaluations`, re-keyed by essence-assertion id. The full
  per-run judgment stays at the suite's `judgments/` path; the scorecard carries the rolled-up essence result.
- `fidelityVerdict` is derived from the two axes by the rule table above — it is never entered by hand. It is
  `null` when the essence axis is absent, and that is correct rather than lazy: with completeness alone,
  `ratio < 1.0` cannot distinguish `GAP-DRIFT` from `GAP+TASTE-DRIFT`, and `ratio == 1.0` cannot distinguish
  `FAITHFUL` from `TASTE-DRIFT`. `completeness.verdict` carries the provable half; a `verdictBasis` string
  records why the rest was not derivable.
- `generator` names the binary that produced the artefact; `source` stays the producing **skill**, per the
  artifact convention.

---

## Worked example 1 — single arm (WorksheetForge)

Scored against the WorksheetForge product-definition essence block (3 non-negotiable differentiators, 3
quality-bar items) and its spec (`D = 6` declared surfaces). One declared-live surface (`coach-dashboard`)
still reads a mock constant, and D-003's streaming-preview budget is missed.

```json
{
  "$schema": "shipkit-artifact",
  "type": "fidelity-scorecard",
  "version": "1.0",
  "lastUpdated": "2026-07-03T09:00:00Z",
  "source": "shipkit-semantic-qa",
  "mode": "single",
  "essenceThreshold": 80,
  "rubricSource": {
    "productDefinition": ".shipkit/product-definition.json",
    "specs": [".shipkit/specs/shipped/worksheet-creator.json"],
    "declaredSurfaceCount": 6,
    "nonNegotiableDifferentiators": ["D-001", "D-002", "D-003"],
    "qualityBar": ["Q-001", "Q-002", "Q-003"]
  },
  "arms": [
    {
      "name": "build",
      "codebase": ".",
      "completeness": {
        "declared": 6,
        "builtAndBacked": 5,
        "ratio": 0.83,
        "byDimension": {
          "applications": "2/2",
          "datastores": "1/2",
          "contracts": "1/1",
          "integrations": "1/1"
        },
        "unbackedSurfaces": [],
        "mockSeams": [
          { "surface": "differentiated-sets-view", "field": "difficulty_band", "declaredLive": true,
            "evidence": "renders SAMPLE_SETS array; spec declares this surface live, generation API never called",
            "source": "verification-report.json#dataReality" }
        ]
      },
      "essence": {
        "score": 72,
        "floorHeld": false,
        "differentiators": { "pass": 2, "partial": 1, "fail": 0 },
        "qualityBar": { "pass": 2, "partial": 0, "fail": 1 },
        "results": [
          { "id": "D-001", "kind": "differentiator", "nonNegotiable": true,
            "assertion": "One creation flow produces exactly three difficulty variants without re-entering the topic.",
            "result": "pass",
            "evidence": "Single flow output screenshot shows below/on/advanced variants of one worksheet." },
          { "id": "D-002", "kind": "differentiator", "nonNegotiable": true,
            "assertion": "Every generated worksheet displays the specific curriculum standard IDs it targets.",
            "result": "pass",
            "evidence": "Standard IDs (CCSS.MATH.4.NBT.5) render in the worksheet header on all sampled outputs." },
          { "id": "D-003", "kind": "differentiator", "nonNegotiable": true,
            "assertion": "Preview streams first content within 2s of any parameter change; never a blank spinner over 2s.",
            "result": "partial",
            "evidence": "Preview streams, but first content measured at ~4.1s after a difficulty change — over the 2s budget, floor broken." },
          { "id": "Q-001", "kind": "qualityBar", "dimension": "empty-state",
            "assertion": "Every list/collection view has an empty state naming and linking the next action.",
            "result": "pass",
            "evidence": "Saved-worksheets and standards-browser empty states both show a CTA." },
          { "id": "Q-002", "kind": "qualityBar", "dimension": "interaction",
            "assertion": "The wizard flow is completable by keyboard alone.",
            "result": "pass",
            "evidence": "Tab/enter advanced through all five steps without a mouse." },
          { "id": "Q-003", "kind": "qualityBar", "dimension": "error",
            "assertion": "Every generation/export failure shows a specific recoverable message with retry.",
            "result": "fail",
            "evidence": "Forced export failure rendered a raw 500 stack trace with no retry action." }
        ]
      },
      "fidelityVerdict": "GAP+TASTE-DRIFT"
    }
  ]
}
```

**Reading it:** completeness `0.83` (5/6 — one differentiated-sets surface is green-but-mock) → gap-drift.
Essence `72` with `floorHeld: false` (D-003 partial) → taste-drift. Two concrete fixes fall out: wire the
differentiated-sets surface to the live generation API, and bring the preview stream under the 2s budget.
Neither is a matter of taste — both are checkable against a named assertion.

---

## Worked example 2 — comparative (Shipkit vs raw)

Same brief and the *same rubric*, two arms. The Shipkit arm went through the no-gaps spec gate and the
data-reality gate; the raw arm was built straight from the prompt. Both are scored against the intent's
`D = 6` surfaces and the same essence assertions.

```json
{
  "$schema": "shipkit-artifact",
  "type": "fidelity-scorecard",
  "version": "1.0",
  "lastUpdated": "2026-07-03T09:30:00Z",
  "source": "shipkit-semantic-qa",
  "mode": "comparative",
  "essenceThreshold": 80,
  "rubricSource": {
    "productDefinition": ".shipkit/product-definition.json",
    "specs": [".shipkit/specs/shipped/worksheet-creator.json"],
    "declaredSurfaceCount": 6,
    "nonNegotiableDifferentiators": ["D-001", "D-002", "D-003"],
    "qualityBar": ["Q-001", "Q-002", "Q-003"]
  },
  "arms": [
    {
      "name": "shipkit",
      "codebase": "../arm-shipkit",
      "completeness": {
        "declared": 6, "builtAndBacked": 6, "ratio": 1.0,
        "byDimension": { "applications": "2/2", "datastores": "2/2", "contracts": "1/1", "integrations": "1/1" },
        "unbackedSurfaces": [], "mockSeams": []
      },
      "essence": {
        "score": 94, "floorHeld": true,
        "differentiators": { "pass": 3, "partial": 0, "fail": 0 },
        "qualityBar": { "pass": 3, "partial": 0, "fail": 0 },
        "results": [
          { "id": "D-001", "kind": "differentiator", "nonNegotiable": true, "assertion": "One creation flow produces exactly three difficulty variants.", "result": "pass", "evidence": "Three variants emitted from one flow." },
          { "id": "D-002", "kind": "differentiator", "nonNegotiable": true, "assertion": "Every worksheet displays its standard IDs.", "result": "pass", "evidence": "Standard IDs render on all outputs." },
          { "id": "D-003", "kind": "differentiator", "nonNegotiable": true, "assertion": "Preview streams first content within 2s.", "result": "pass", "evidence": "First token at ~1.3s." },
          { "id": "Q-001", "kind": "qualityBar", "dimension": "empty-state", "assertion": "Every list view has an actionable empty state.", "result": "pass", "evidence": "All three list views have CTA empty states." },
          { "id": "Q-002", "kind": "qualityBar", "dimension": "interaction", "assertion": "Wizard completable by keyboard alone.", "result": "pass", "evidence": "Full keyboard traversal confirmed." },
          { "id": "Q-003", "kind": "qualityBar", "dimension": "error", "assertion": "Failures show a specific recoverable message with retry.", "result": "pass", "evidence": "Export failure shows a retry toast." }
        ]
      },
      "fidelityVerdict": "FAITHFUL"
    },
    {
      "name": "raw",
      "codebase": "../arm-raw",
      "completeness": {
        "declared": 6, "builtAndBacked": 4, "ratio": 0.67,
        "byDimension": { "applications": "2/2", "datastores": "1/2", "contracts": "0/1", "integrations": "1/1" },
        "unbackedSurfaces": [
          { "surface": "differentiated-sets-view", "field": "difficulty_band", "reason": "no owning view; each surface computes its own band" }
        ],
        "mockSeams": [
          { "surface": "standards-browser", "field": "standard_id", "declaredLive": true,
            "evidence": "renders a hardcoded STANDARDS array; no standards API/table queried",
            "source": "verification-report.json#dataReality" }
        ]
      },
      "essence": {
        "score": 58, "floorHeld": false,
        "differentiators": { "pass": 1, "partial": 1, "fail": 1 },
        "qualityBar": { "pass": 1, "partial": 1, "fail": 1 },
        "results": [
          { "id": "D-001", "kind": "differentiator", "nonNegotiable": true, "assertion": "One creation flow produces exactly three difficulty variants.", "result": "fail", "evidence": "Only a single worksheet is produced; no difficulty variants — the core differentiator is absent." },
          { "id": "D-002", "kind": "differentiator", "nonNegotiable": true, "assertion": "Every worksheet displays its standard IDs.", "result": "partial", "evidence": "Standards shown as free-text topic, not specific curriculum IDs." },
          { "id": "D-003", "kind": "differentiator", "nonNegotiable": true, "assertion": "Preview streams first content within 2s.", "result": "pass", "evidence": "Preview streams at ~1.6s." },
          { "id": "Q-001", "kind": "qualityBar", "dimension": "empty-state", "assertion": "Every list view has an actionable empty state.", "result": "fail", "evidence": "Saved-worksheets view renders blank when empty." },
          { "id": "Q-002", "kind": "qualityBar", "dimension": "interaction", "assertion": "Wizard completable by keyboard alone.", "result": "pass", "evidence": "Keyboard traversal works." },
          { "id": "Q-003", "kind": "qualityBar", "dimension": "error", "assertion": "Failures show a specific recoverable message with retry.", "result": "partial", "evidence": "Generic 'Something went wrong' with no retry action." }
        ]
      },
      "fidelityVerdict": "GAP+TASTE-DRIFT"
    }
  ],
  "comparison": {
    "completenessDelta": "shipkit +0.33 (1.0 vs 0.67)",
    "essenceDelta": "shipkit +36 (94 vs 58)",
    "floorDelta": "shipkit holds the essence floor; raw breaks D-001 (adaptive difficulty absent) and D-002 (no standard IDs)",
    "winner": "shipkit",
    "notes": [
      "Raw arm shipped generic on the defining differentiator (D-001 adaptive difficulty) — the exact taste-drift the essence axis is built to catch.",
      "Raw arm's standards-browser is green-but-mock (declared live, hardcoded array) and differentiated-sets has no SSOT for difficulty_band — gap-drift the completeness axis catches deterministically.",
      "Delta is the fidelity signal Project A consumes: same brief, +0.33 completeness and +36 essence for the Shipkit arm."
    ]
  }
}
```

**Reading it:** the two arms share one rubric, so the deltas are apples-to-apples. The raw arm's failures are
named against specific assertions and surfaces — not vibes — which is what makes the comparison defensible.
