# Fidelity checkers

Deterministic analyzers behind the **completeness axis** of the fidelity scorecard
— the "the app that ships IS the app envisioned" half of Shipkit's outcome. The
contract they serve is `../../references/fidelity-scorecard-schema.md`; the skill
that invokes them is `shipkit-semantic-qa` (fidelity mode, SKILL.md Step 5.2).

Each is a standalone CLI: target codebase path in, structured JSON to stdout
(`--report` for human-readable, `--help` for usage). Exit 0 clean, 2 on bad input.
Python 3, stdlib only, no network.

| Tool | Detects | Emits |
|------|---------|-------|
| `fidelity-score.py` | **The scorecard producer.** Emits `fidelity-scorecard-schema.md` verbatim: completeness ratio from the DECLARED surface list, `byDimension`, `essence: null` slot, `arms[]` + `comparison` for comparative mode. | `fidelity-scorecard.json` |
| `mock-seam-detector.py` | Mock/stub seams (`mockData`, `USE_MOCK`, `fake*Client`, `if (mock)`, `TODO: wire`, placeholders, hardcoded arrays) — cross-checked against the spec's declared-live surfaces via `--spec`. | `{file, line, seamKind, confidence, surface, declaredLive, evidence}[]` + summary |
| `unbacked-surface-checker.py` | UI surfaces classified by data backing: **real** / **mock** / **missing** (renders data, no source). | `{surface, backing, confidence, rendersData, evidence}[]` |
| `ssot-checker.py` | Single-source-of-truth risks: a shared metric/field *computed* in >1 file (the `grade_band`x4 pattern from the phinma retro). | `{field, fileCount, siteCount, risk, sites[]}[]` |
| `_declared.py` | Loads the declared-surface list from spec artifacts and ties built files back onto it. Not a CLI. | — |
| `_common.py` | Shared source-file walker (skips `node_modules`/`.git`/`dist`/…). Not a CLI. | — |

## The denominator comes from the spec, not from a code scan

This is the load-bearing design decision, and it is what separates v2 from v1.

A spec's `functionalSurface` is the set of things the build was **asked** to
deliver; `deferred` / `acceptanceCriteria.wontHave` are what it was asked **not**
to. So a mock seam only means "green-but-mock" if it sits on a surface the spec
declares **live** — everything else is noise *by contract*, not by judgement.

v1 re-scanned the codebase and invented its own denominator: every file the
regexes tripped on became a finding, which is why it measured **~27-30% precision**
against ground truth. v2 asks the reverse question — *given a file with a seam,
does it belong to a declared-live surface?* — and **fails open**: no match means
`declaredLive: false`, advisory only, never gating.

Fail-open is deliberate. A false "green-but-mock" FAIL on a surface nobody
declared burns trust in the gate, and a gate people learn to ignore catches
nothing. Recall is the acceptable loss; precision is the product.

Without `--spec`, `declaredLive` is `null` — *unknown*, never `false`.

> **The ~27–30% figure is v1's measured precision. v2's is NOT yet measured.** The
> mechanism is demonstrated on `_smoke/` (12 high-confidence seams → 4 gating), but
> that is a fixture, not ground truth. Re-measuring needs a real codebase whose spec
> carries `functionalSurface` — the only corpus with ground truth (phinma) predates
> the no-gaps gate, so 0 of its 42 specs declare surfaces and it cannot be scored in
> this mode. Treat "the declared cross-check fixes precision" as *designed-for and
> fixture-demonstrated*, not *confirmed*. Hand-authoring a declared list for an
> existing codebase would not settle it: that authors the ground truth the tool is
> then scored against.

```
completeness:
  declared       = functionalSurface elements, verdict COVERED  (from the SPEC)
  notBacked      = gapReport.unbackedSurfaces + mockSeams where declaredLive
  builtAndBacked = declared - |notBacked|
  ratio          = builtAndBacked / declared        (declared 0 -> "n/a")
```

## Known limit: `ratio` is an upper bound

The formula subtracts only surfaces something **names**. A declared surface that
was simply **never built** is named by neither an `unbackedSurfaces` entry nor a
seam — so it counts as *built*. An **empty codebase scores `1.0`**.

That is the price of not manufacturing findings from an unprovable negative
("`web-ui` appears nowhere, therefore it was not built" — or it was named
differently, or uses an unusual data layer). Instead:

- `completeness.signals.declaredCoverage` lists declared elements with **no code
  evidence**, advisory. When `unresolved > 0` the ratio is an upper bound.
- In **comparative mode this can invert the winner** — an arm that never built a
  surface is not penalised for it. `comparison.notes` flags it.

## `completeness.signals` — advisory, never gating

v1's `surfaces*0.70 + seams*0.15 + ssot*0.15` blend survives as
`completeness.signals`, unchanged and weight-emitting, because it catches things
the contract's formula structurally cannot. It **never** moves `ratio` or
`fidelityVerdict`. Read it as leads for a human; do not quote `blendedScore` as
the completeness score.

On `_smoke/` the split is the whole argument: contract ratio **0.857** (one
genuinely green-but-mock surface) vs advisory blend **0.408** (dragged by 9 seams
on surfaces nobody declared).

## Verdict: derived, never guessed

`fidelity-score.py` applies the schema's rule table in code. Without `--essence`
it emits `fidelityVerdict: null` on purpose — `ratio < 1.0` cannot distinguish
`GAP-DRIFT` from `GAP+TASTE-DRIFT`, and `ratio == 1.0` cannot distinguish
`FAITHFUL` from `TASTE-DRIFT`. `completeness.verdict` carries the provable half.

## Usage

```bash
# scorecard (declared list is required — it IS the denominator)
python fidelity-score.py . --spec .shipkit/specs/shipped/*.json --report

# prefer review-shipping's dataReality when it exists (it owns the gate)
python fidelity-score.py . --spec S.json --verification-report .shipkit/verification-report.json

# full verdict: both axes
python fidelity-score.py . --spec S.json --essence essence.json --report

# comparative — one rubric, many arms, enforced by construction
python fidelity-score.py --arm shipkit=../arm-shipkit --arm raw=../arm-raw --spec S.json --report

# individual checkers
python mock-seam-detector.py . --spec S.json --report
python mock-seam-detector.py . --spec S.json --declared-live-only
python unbacked-surface-checker.py . --report
python ssot-checker.py . --min-files 3
```

Deterministic: no `datetime.now()`. `lastUpdated` is `null` unless `--stamp` is
passed, so repeated runs on an unchanged tree are byte-identical.

## Honesty / limits

Regex heuristics, not proofs. Good recall on common JS/TS/Python patterns
(validated against the phinma failure shapes); confidence marked per finding.

- **mock-seam**: over-flags generic words (`stub`, `placeholder`); comment-only
  mentions downgrade to low confidence. `--spec` is what turns it from a grep
  into a gate.
- **unbacked-surface**: surface detection is name/path based; "real" keys off
  common data libs (supabase, react-query, fetch, axios, prisma, trpc, swr). A
  low-confidence `missing` (no data rendering) is likely static/layout. A real
  surface on an unusual data layer may mis-classify `missing`.
- **ssot**: matches field **name** + derivation syntax — cannot prove two
  computations are the same metric, misses same-metric/different-name cases.
- **`_declared` matching**: name-based. It cannot prove a file *is* a declared
  surface, only that it carries the declared identifier. A surface renamed
  between spec and build will not match, and will fail open.

### Out of scope: the temporal blind spot

These tools are **static** — they see the tree as it is now, never its history.
The phinma root cause was a **git-timeline property**: surfaces were *built before
their backing view existed* (mock dashboards ran 6-11 days ahead of their DB
views). A repo that shipped mock-first and wired up later looks **identical** at
HEAD to one built backing-first. No static analysis can separate them; catching
declare-before-build needs a commit-timeline checker, which is a different tool.

## Fixture

`_smoke/` mirrors the phinma failure shapes, with `_smoke/spec.json` as its
declared list. It exercises all three cross-check paths — expect **12
high-confidence seams, only 4 gating**:

| Path | File | Expected |
|------|------|----------|
| **GATING** | `StaffDashboard.tsx` | declared live + mock seams -> fails the gate |
| **DEFERRED** | `PredictivePacing.tsx` | matches `deferred[]` -> suppressed despite high-conf seams |
| **FAIL-OPEN** | `scratch/ExperimentPanel.tsx` | declared nowhere -> advisory only |

```bash
python fidelity-score.py _smoke --spec _smoke/spec.json --report
```
