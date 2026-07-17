# Fidelity checkers

Deterministic, heuristic codebase analyzers that measure build **completeness**
— the "the app that ships IS the app envisioned" axis of the fidelity fitness
function (see `../../FIDELITY-MEASURE-SPEC.md`). Each is a standalone CLI: takes
a target codebase path, emits structured JSON to stdout (default), `--report`
for human-readable, `--help` for usage. Exit 0 on a clean run, 2 on a bad path.
Python 3, stdlib only.

| Tool | Detects | Emits |
|------|---------|-------|
| `mock-seam-detector.py` | Mock/stub seams on surfaces meant to be live: `mockData`, `USE_MOCK`, `fake*Client`, `if (mock)`, `TODO: wire`, coming-soon/placeholder flags, hardcoded return arrays. | `{file, line, seamKind, confidence, evidence}[]` + summary counts |
| `unbacked-surface-checker.py` | UI surfaces (routes/pages, `*Dashboard`/`*Page`/`*View`) classified by data backing: **real** (real client/query/api), **mock** (mock seam), **missing** (renders data, no source). | `{surface, backing, confidence, rendersData, evidence}[]` + byBacking counts |
| `ssot-checker.py` | Single-source-of-truth risks: a shared metric/field *computed* (derived) in >1 file — the `grade_band`×4 / mastery-metric×3 pattern from the phinma retro. | `{field, fileCount, siteCount, risk, sites[]}[]` |
| `fidelity-score.py` | **Scorecard composer (Phase 2).** Runs the three checkers above in-process and folds them into the **completeness axis** of the fidelity scorecard, broken down `byDimension` (surfaces/seams/ssot). Essence axis (Phase 3) left as a null slot. | `fidelity-scorecard.json`: `{target, generatedAt, completeness:{score, weights, byDimension, unbackedSurfaces[], mockSeams[], ssotViolations[]}, essence:null, fidelityVerdict}` |
| `_common.py` | Shared source-file walker (gitignore-ish: skips node_modules/.git/dist/build/etc.). Not a CLI. | — |

## Scorecard composer — completeness formula

`fidelity-score.py` blends three dimension scores (each in `[0,1]`) into one
completeness read. Weights are **emitted in the JSON** (`completeness.weights`),
never hidden:

```
completeness = surfaces*0.70 + seams*0.15 + ssot*0.15
```

- **surfaces** (primary — the spec's `builtAndBacked / declaredSurfaces`):
  `backedSurfaces / declaredDataSurfaces`, where a data surface is one the
  unbacked-checker says should carry data (`real`/`mock`, or `missing` **with**
  rendered data). `mock` and `missing-with-render` count as **not backed** and
  drag the score down; low-confidence `missing` (static/layout, no data) is
  excluded from the denominator rather than counted as a gap.
- **seams** (risk flag): `(filesScanned − filesWithHighConfSeams) / filesScanned`.
  Only **high-confidence** mock seams subtract; low/med seams are listed as
  advisory but do not move the score.
- **ssot** (risk flag): `1 / (1 + weightedViolations)`, where
  `weightedViolations = highRisk*1.0 + medRisk*0.5` (monotonic decay).

**Verdict** (completeness signal only — essence is pending Phase 3):
`FAITHFUL` if zero unbacked surfaces AND zero high-conf seams AND zero high-risk
SSOT; otherwise `GAP-DRIFT`. Full formula also in `fidelity-score.py --help`.

Deterministic: `generatedAt` is `null` unless `--stamp` is passed — no
`datetime.now()` — so repeated runs on an unchanged tree are byte-identical.

## Usage

```bash
python mock-seam-detector.py <path>              # JSON to stdout
python mock-seam-detector.py <path> --report     # human-readable
python unbacked-surface-checker.py <path> --report
python ssot-checker.py <path> --min-files 3      # tighten SSOT threshold
python fidelity-score.py <path>                  # composed scorecard JSON
python fidelity-score.py <path> --report         # human-readable scorecard
python fidelity-score.py <path> --out fidelity-scorecard.json --stamp 2026-07-03T00:00:00Z
```

## Honesty / limits

These are **heuristic v1** regex analyzers, not proofs. They aim for good recall
on the common JS/TS/Python patterns (validated against the phinma failure shapes)
and mark confidence per finding so downstream scoring can weight them. Known
limits, per tool `--help`:

- **mock-seam**: over-flags generic words (`stub`, `placeholder`); comment-only
  identifier mentions are downgraded to low confidence.
- **unbacked-surface**: surface detection is name/path based; "real" keys off
  common data libs (supabase, react-query, fetch, axios, prisma, trpc, swr). A
  low-confidence `missing` (no data rendering) is likely static/layout, not a
  true gap. A real surface on an unusual data layer may mis-classify `missing`.
- **ssot**: matches on field **name** + derivation syntax — cannot prove two
  computations are the same metric, and misses same-metric/different-name cases.

## Fixture

`_smoke/` is a tiny fixture mirroring the phinma failures (mock staff dashboard,
unbacked exec view, `grade_band` computed twice, a real supabase page) used to
smoke-test the checkers. Run any tool against `_smoke` to see them fire.
