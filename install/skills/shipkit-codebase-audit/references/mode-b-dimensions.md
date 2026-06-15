# Mode B — Reconciliation

Mode B reasons about what deterministic tooling cannot see. It is **always fed Mode A's results** and excludes anything Mode A already reported. Two tiers share the same dimensions; they differ only in coverage strategy.

## Intent source (resolve first)

| Repo type | Intent source | Signal |
|-----------|---------------|--------|
| Shipkit | `.shipkit/engineering-definition.json` (`components[]`, `dataContracts`), `architecture.json`, `specs/active/*.json` | High |
| Non-Shipkit | README + entry points (`main`/`bin`/`exports` in `package.json`) + exported API surface | Lower — **state the caveat in output** |

`intentSource` is recorded in the artifact summary (`shipkit` / `code-surface` / `none`).

## The four dimensions

1. **Contract drift** — an exported signature/type changed but a caller still depends on the old shape. (Tooling sees the export exists; it doesn't see the *semantic* mismatch.)
2. **Half-wired seams** — something is imported/registered but never invoked; a route/flag/handler declared but unreachable; a DI binding with no resolver.
3. **Declared-but-unbuilt** — intent names a component/feature with no implementation behind it.
4. **Built-but-undeclared** — implemented surface area with no intent backing → candidate dead feature (cross-check Mode A's unused-export findings to avoid double counting).

## Shared grounded-context bundle

Built **once** before any fan-out, passed **identically** to every worker:
- dependency graph (who imports whom),
- exported API surface,
- Mode A results (so workers skip linter-visible issues),
- resolved intent source.

No worker re-derives the global picture — that guarantees consistency and avoids redundant cost.

---

## Standard tier (`deep`)

Launch the four dimensions as **parallel read-only `Explore` agents** (Agent tool, single message, multiple calls). Each agent gets the grounded bundle + its dimension brief, returns findings with `file:line` evidence. Synthesize, dedupe against Mode A, write the artifact.

Good coverage at moderate cost — appropriate for routine pre-milestone checks. It does **not** guarantee every file is individually examined (that's the exhaustive tier).

---

## Exhaustive tier (`exhaustive`)

Full coverage — every file (or slice) is examined by a dedicated worker. Expensive; opt-in; announce it.

### Protocol

1. **Partition** the file set:
   - default **one agent per file**;
   - above ~150 source files, group into cohesive **slices** by dependency cluster (fallback: directory). Each slice must be small enough that the worker never truncates.
   - `log` the partition count and the slice strategy chosen (no silent capping).

2. **Dispatch** read-only `Explore` workers via the Agent tool, **batched to the concurrency cap**. Each worker receives the grounded bundle + its unit(s), and writes to disk:
   - `integrity[]` findings, and
   - a **contract ledger** (`provides` / `expects`) — see `output-schema.md`.

3. **Reconcile-join** (NOT mere dedup): join every `expects` against the matching `provides` across all ledgers to surface cross-file drift (mismatch / expected-but-unprovided / provided-but-unconsumed). Merge + dedupe integrity findings against each other and against Mode A.

4. **Coverage guarantee** — count ledger files on disk against the expected unit set. **Re-dispatch missing units until the gap is zero.** Reconcile against the on-disk artifacts, never against an agent's self-report (agents over-claim).

### Concurrency-independent correctness (the documented fallback)

The reconcile-join + gap-redispatch loop does not care whether workers ran in parallel or one at a time. If the runtime can't fan out wide (concurrency caps, throttling, a host that serializes dispatch), workers run **batched-sequentially** — coverage and correctness are identical; only wall-clock changes. Note the degraded throughput in the output; never reduce coverage to fit.

### Why per-file fan-out (not one big agent)

A single agent over a whole repo is *forced* to truncate — the root cause of silently-dropped findings. Partitioning to units small enough to never truncate, then proving coverage at the merge, is what makes "no detail missed" a guarantee rather than a hope.
