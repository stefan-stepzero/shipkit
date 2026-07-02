# Open Decisions — Success Harness

## Phase 2 — Essence artefact shape (DECIDED)

**Decision:** Extend `.shipkit/product-definition.json` (owned by `shipkit-product-definition`) with a
checkable *essence block* — **do NOT create a new `.shipkit/differentiation.json` sidecar.**

Concretely, the extension is **additive** (no breaking change to the v3.0 schema):
1. Each item in the existing top-level `differentiators[]` array gains two fields:
   - `assertion` (string) — the differentiator restated as a *testable assertion* an evaluator can score a
     built screen/behaviour against.
   - `nonNegotiable` (boolean) — marks the 3-5 differentiators that MUST ship faithfully (the essence floor).
2. A new top-level `qualityBar[]` array — the interaction/product **quality bar**, each item a testable
   assertion with a `dimension` and the surfaces it `appliesTo`.
3. `summary` gains `totalQualityBar`.

**The "essence" that Phase 3 scores** = the `differentiators[]` items where `nonNegotiable: true`
(each via its `assertion`) **+** every `qualityBar[]` assertion. Both live in one artefact.

### Options considered

| Option | Verdict |
|--------|---------|
| **A. New `.shipkit/differentiation.json` sidecar** | Rejected. Splits "what makes this *this* app" across two files (differentiators already live in product-definition.json) → the exact drift the Project-B retro warns against. Also needs its own 7-file registration (manifest, session-start, rules) for no benefit. |
| **B. Extend `product-definition.json` (CHOSEN)** | Natural owner — it already emits `differentiators`. The essence block is the *checkable evolution* of a concept the skill already produces. One artefact for Phase 3 to read. No new file, no skill-count change, no new registration. |
| C. Extend `design-system` too | Rejected as the *home*. Design-system owns aesthetic **direction** (tokens/principles). Essence here = differentiators + product/interaction quality bar, which the *reviewer/eval scores* — a different job. The skill **references** design-system for aesthetic assertions rather than duplicating tokens. |

### Why additive rather than a clean `essence: {}` regroup
`differentiators[]` is consumed by many downstream skills (engineering-definition, product-goals,
spec, spec-roadmap, plan) and two agents. Moving it under a new `essence` object would break those
readers. Adding fields is invisible to existing consumers and keeps v3.0 back-compatible — so the
version stays `3.0` (additive optional fields), no migration needed.

**Open sub-point (non-blocking):** whether to eventually promote `qualityBar` assertions into
`shipkit-product-goals` as measurable criteria (goals-with-teeth, retro #4). Deferred — Phase 2 just
*captures* them checkably; wiring them into the goals/eval loop is Phase 3's job.
