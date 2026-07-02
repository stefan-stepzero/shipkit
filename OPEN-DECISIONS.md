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

---

## Phase 3 — Fidelity scorecard (DECIDED)

**Decision:** Build the fidelity eval as an **extension of `shipkit-semantic-qa`** (new `--fidelity` mode) +
a **`fidelity-scorecard` output schema** (`references/fidelity-scorecard-schema.md`). **No new skill** — no
count churn. The completeness half needs no code: it is arithmetic over two existing artefacts, documented as
a deterministic formula in the schema reference (a CLI would be over-build for v1).

### The scorecard shape — two axes, kept separate

`.shipkit/fidelity-scorecard.json` composes:
1. **Completeness (deterministic):** `ratio = builtAndBacked / declared`, where `declared` = spec
   `gapReport.functionalSurface` elements with `verdict: "COVERED"`, and a surface is *not backed* if it's in
   `gapReport.unbackedSurfaces[]` or is the surface of a `dataReality.mockSeams[]` entry with
   `declaredLive: true`. Broken down `byDimension`. No LLM.
2. **Essence (LLM-judge):** semantic-qa's normal Judge loop, with criteria = the essence block. Each assertion
   → pass/partial/fail with evidence; `essenceScore` (weighted) + `floorHeld` (all nonNegotiable
   differentiators PASS).

**Chosen: keep the two axes separate, never blend into one number.** A single blended score would let a
healthy essence hide a green-but-mock surface (or vice versa) — the exact drift the harness exists to catch.
A derived `fidelityVerdict` (`FAITHFUL` / `GAP-DRIFT` / `TASTE-DRIFT` / `GAP+TASTE-DRIFT`) names the drift(s)
while both axis scores stay visible.

### How semantic-qa consumes the essence block

`criteriaSource: "essence"` in `suite.json` → derive criteria from `.shipkit/product-definition.json` instead
of asking the user. Mapping: each `nonNegotiable` differentiator → a **must-pass** criterion (its `assertion`
is the `evaluationGuide`); each `qualityBar` item → an **important** criterion. `enabledBy`/`appliesTo` route
each assertion to the surface(s) to screenshot. This reuses the entire existing Judge machinery — the only new
thing is *where the criteria come from*.

### Comparative mode

`mode: "comparative"`, N `arms[]`, **one shared rubric** fixed from the captured intent (spec `gapReport` +
essence block — a single source of truth). Each arm is scored against the *same* declared-surface list
(data-reality scan run per arm's codebase) and the *same* essence assertions (judge run per arm's screens).
`comparison{}` carries the completeness/essence/floor deltas + winner. `rubricSource` records provenance so
it's auditable that both arms were held to the intent's rubric even if only one arm produced that capture.
This is the artefact Project A consumes.

### Options considered

| Option | Verdict |
|--------|---------|
| **New `shipkit-fidelity` skill** | Rejected. Count churn; semantic-qa *already* runs an LLM-judge-against-criteria loop — the essence axis is that loop with a different criteria source. A new skill would duplicate the Judge machinery (parallel-systems rule). |
| **Blend completeness + essence into one 0-100 fidelity score** | Rejected. A blended number hides the failure mode — a 90 essence masking a green-but-mock surface reads as "shipped faithfully" when it isn't. Two axes + a named verdict is the honest shape. |
| **Extend semantic-qa + schema reference (CHOSEN)** | Natural home. Essence judge = semantic-qa's existing loop reading the essence block; completeness = a documented deterministic formula over `gapReport` + `dataReality`; scorecard = an output schema composing both. No new skill, no new registration. |
| Small reader CLI for the completeness half | Rejected for v1. The formula is trivial arithmetic over two JSON files Claude reads inline; a CLI is premature. Revisit only if the count becomes large/automated enough to warrant tooling. |

**Open sub-points (non-blocking):**
- **Essence threshold** for `FAITHFUL` is `essenceScore >= 80` (v1 default, recorded as `essenceThreshold` in
  the scorecard so it's explicit/tunable). No empirical basis yet — calibrate once Project A runs real arms.
- **qualityBar weight** is `important` (not `must-pass`) — a quality-bar miss drags the score but isn't an
  essence-floor break; only nonNegotiable differentiators are the floor. If Project A shows quality-bar misses
  are as fatal as differentiator misses, promote specific `qualityBar` items to `must-pass`.
- **partial credit** = 0.5 for the essence score. Coarse but honest; revisit if it proves too lenient.

---

## Phase 4 — ED↔ADR staleness signal (DECIDED)

**Decision:** The divergence check lives in the **`shipkit-session-start` hook** as a small
deterministic (no-LLM) computation — NOT in `shipkit-architecture-map`. Linkage reuses the
existing ADR `scope: "mechanism:M-###"` field (no new join). The check reads
`architecture-archive.json` (full ADR bodies) vs `engineering-definition.json` mechanisms and
emits a one-line session-start warning when N mechanisms are stale.

**Linkage mechanism (lean, additive):**
- ED mechanisms already carry `M-###` ids; ADRs already carry `scope: "mechanism:M-###"`. That
  scope IS the link — kept on the superseding/amending ADR too.
- New allowed lean ADR status `dormant` (retired-not-replaced) alongside superseded/amended.
- ED mechanism gains OPTIONAL `supersededByADR` / `staleSince` — an *acknowledgement* marker
  that suppresses the flag once a session reconciles (records "the ADR log is now authority").
- **Divergence rule:** an ED mechanism is stale when the ADR archive has a decision scoped to it
  with status `superseded`/`dormant`/`deprecated` OR an `amendedBy` link, and the mechanism isn't
  already acknowledged.

### Options considered

| Option | Verdict |
|--------|---------|
| **Owner = `shipkit-architecture-map`** | Rejected as owner. It explicitly does NOT read `architecture.json` (decisions-log separation of concerns), it's a heavier fork skill (full code scan), and it does NOT run at session-start — the exact moment the retro failure needs catching ("a fresh session built against a stale ED"). Wrong artefact boundary + wrong trigger. |
| **Owner = session-start hook (CHOSEN)** | The surfacing point IS session-start, the computation is trivial arithmetic over two JSON files the hook already reads, it runs every session for free, needs no new skill and no fork dispatch, and matches the retro's "surface it at session-start" verbatim. |
| New `shipkit-*` divergence skill | Rejected. Count churn + parallel system; the check is 40 lines of deterministic Python in a hook that already emits digests. |

**Why read the archive, not the lean `architecture.json`:** the lean file's superseded-stub
schema drops `scope`, so superseded ADRs wouldn't be attributable to a mechanism. The archive
retains scope + status + supersession/amendment links and is dual-written on every ADR, so it's
the authoritative source. Hook falls back to the lean file if the archive is absent (best-effort;
only dormant/amended-active entries surface in that degraded case).

**Open sub-points (non-blocking):**
- **Deeper integration deferred:** the retro also suggested surfacing the divergence in
  `framework-integrity` / `architecture-map` as an explicit divergence section. v1 ships only the
  session-start surfacing (highest-leverage, the exact failure). An on-demand divergence report in
  architecture-map is a clean future add.
- **Amended = stale?** v1 counts an amended mechanism as stale (an amendment changed the approach,
  so the ED text may be out of step). If this proves too noisy (amendments that don't touch the ED
  narrative), narrow to superseded/dormant only.
