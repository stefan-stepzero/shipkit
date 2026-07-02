# Run-scoped artifacts — the resolution rule

The single authority on **where a skill writes its output** so that parallel runs,
worktrees, and shared-cwd workflow agents don't collide on a fixed `.shipkit/` path.
Every transient-writing skill and every reader of a transient artifact cites this file.

The rule is deliberately narrow: **only transient/run artifacts are namespaced. Durable
singletons stay shared** — they are the accreting source of truth, and per-run copies
would fragment the cross-session continuity that is the whole point of `.shipkit/`.

---

## The run root

When work runs under the orchestration engine (`shipkit-orchestrate`), the engine mints
a **run id** at run start and exposes a **run root**:

- env var **`SHIPKIT_RUN_DIR`** — set for dispatched units (incl. workflow agents that
  share the parent cwd); authoritative when present.
- **`.shipkit/active-run.json`** (fixed path) — `{ "runId": "...", "runDir":
  ".shipkit/runs/<run-id>", "startedAt": "..." }`. The pointer any skill can read to
  find the current run. Concurrent runs each write their own `.shipkit/runs/<id>/`;
  enumerate `.shipkit/runs/` to list them (don't trust `active-run.json` as a lock — it
  is last-writer-wins, only a convenience pointer).

The engine generates the id (it is a main-session skill). **Workflow scripts cannot call
`Date.now()`/`Math.random()`** — so workflow agents never mint their own id; the engine
passes `SHIPKIT_RUN_DIR` in to them.

## Resolving an output path

For a **transient** artifact `X`:

```
base = $SHIPKIT_RUN_DIR            if the env var is set
     else .shipkit/active-run.json -> runDir   if a run is active
     else .shipkit                  (no run context — solo/non-parallel; legacy path)
write X to  <base>/<X>
```

So `/shipkit-preflight` run solo writes `.shipkit/preflight.json` (unchanged,
back-compatible); the same skill dispatched inside run `r-20260630-ab12` writes
`.shipkit/runs/r-20260630-ab12/preflight.json`.

**Read-side parity (load-bearing):** a reader of a transient artifact resolves the
**same** base by the same rule. Writer and reader move together — if a writer namespaces
but a reader reads the fixed path (or vice versa), the artifact silently goes missing.

## Transient artifacts (run-scoped)

| Artifact | Written by |
|----------|-----------|
| `orchestration.json` (run-state / ledger) | shipkit-orchestrate |
| `elicitation/<skill>/questions.md`, `answers.md` | the 6 elicitive skills + engine (see `elicitation-protocol.md`) |
| `verification-report.json` | shipkit-review-shipping |
| `preflight.json` | shipkit-preflight (read by scale-ready) |
| `scale-readiness.json` | shipkit-scale-ready (reads `preflight.json`) |
| `communications/latest.html` + `communications/archive/` | shipkit-communications |
| `semantic-qa/suites/*/outputs/run-*`, `judgments/run-*` | shipkit-semantic-qa (already per-run-timestamped; nests in the run root under the engine) |

## Durable singletons (NEVER run-scoped — always at `.shipkit/<name>`)

`why.json`, `vision`, `stage`, `product-discovery.json`, `product-definition.json`,
`engineering-definition.json`, `architecture.json`, `architecture-archive.json`,
`architecture-map.json`, `stack.json`, `schema.json`, `codebase-index.json`,
`goals/*`, `metrics`, `ui-goals.json` (qa-visual's user-confirmed visual goals), and
**all specs** (`specs/{todo,active,parked,shipped}/*`).

Also durable — the **continuity singletons** written at the main session, not by parallel
agents: `progress.json` (work-memory's cross-session resume log) and `user-tasks.json`
(the standing user-task backlog). They accrete across runs by design; per-run copies
would break the continuity that is their purpose.

These are one shared, accreting source of truth. Concurrent writes to a singleton are a
**coordination/lock** concern, not a namespacing one — never solve them by forking a
per-run copy.

## Worktree composition

A worktree lane already isolates `.shipkit/` physically (separate checkout). Inside a
lane the run root is simply the lane's own `.shipkit/` — no extra work. This convention
is the **logical** isolation for the cases worktrees don't cover: workflow agents that
share the parent cwd, and two runs at the same repo root. The two compose; neither
replaces the other.

## Promoting a run result

A run's durable outcome (a finished spec, a logged decision) is written to its durable
singleton path directly (not under `runs/`). Only the transient by-products of getting
there live under `runs/<id>/`, and can be discarded once the run is integrated.
