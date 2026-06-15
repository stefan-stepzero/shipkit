---
name: shipkit-codebase-audit
description: Audit a codebase for dead code, orphaned modules, unused dependencies, and unwired seams. Quick tier runs knip-class checks ephemerally (no repo mutation); deep and exhaustive tiers add intent↔code reconciliation. Portable to any repo, including ones with no tooling installed.
argument-hint: "[scope or directory] [deep|exhaustive]"
model: opus
allowed-tools: Read, Glob, Grep, Bash
effort: high
---

# shipkit-codebase-audit - Dead Code & Wiring Audit

**Purpose**: Deliver one outcome — *this codebase has nothing stale, orphaned, or unwired*. Find unused exports, unreachable files, unused dependencies, broken imports, and the contract drift that linters can't see.

**What this is**: A standing operating procedure. Its value is **remembering** that dead-code and wiring checks must happen, running them the **same way in any repo** (even repos with no tooling installed), and **reasoning past** what the tooling is blind to. Running a linter is a natural capability — this skill is the discipline around it, not the linter itself.

**What this is NOT**:
- Not an auto-fixer — it reports, it does not delete code (deletion is a deliberate call you make).
- Not a code-quality reviewer — that's `/shipkit-review-shipping` (12 dimensions on recent changes).
- Not a production-readiness gate — that's `/shipkit-preflight`.
- Not the framework-internal wiring validator — `/shipkit-validate-wiring` and `/shipkit-wiring-graph` validate Shipkit's OWN component graph; this audits **your application code**.

---

## When to Invoke

| Invocation | Tier | What runs |
|------------|------|-----------|
| `/shipkit-codebase-audit` | **quick** (default) | Mode A only — ephemeral knip-class run + report. Cheap, CI-suitable. |
| `/shipkit-codebase-audit deep` | **standard** | Mode A, then a handful of parallel dimension agents reason about blind spots. |
| `/shipkit-codebase-audit exhaustive` | **exhaustive** | Mode A, then one agent per file (or slice) + contract-ledger reconcile-join. Full coverage. Expensive — opt-in. |
| `/shipkit-codebase-audit src/` | quick on a scope | Limit the audit to a directory. |

Also triggers on: "audit my codebase", "find dead code", "what's unused here", "check for orphaned modules", "is anything unwired", "deep/exhaustive codebase audit".

**Workflow position**: any time for `quick` (it's a hygiene sweep); `deep`/`exhaustive` before a milestone, a refactor, or a release.

---

## Prerequisites

**Required**: none. The skill is portable — it works in a repo with no dead-code tooling installed and in a repo with no `.shipkit/` directory.

**Improves results when present**:
- `.shipkit/codebase-index.json` — narrows discovery (index-accelerated).
- `.shipkit/engineering-definition.json`, `.shipkit/architecture.json`, `.shipkit/specs/active/*.json` — the **intent source** for Mode B (see Portability Caveat).
- A previous `.shipkit/codebase-audit.json` — enables run-over-run delta tracking.

---

## The Model: Two Modes, One Outcome

- **Mode A — the floor (deterministic).** Run knip-class tooling. Catches unused exports / files / dependencies / unresolved imports. Fast, exact, no judgment.
- **Mode B — the ceiling (reasoning).** Reconcile **intent ↔ code**: contract drift, half-wired seams, declared-but-unbuilt and built-but-undeclared components. Reasons **only about what Mode A could not see** — it is always fed Mode A's results so no agent re-discovers a linter finding.

`quick` = A. `deep` = A then B (dimension sweep). `exhaustive` = A then B (per-file fan-out). **A always runs first and feeds B.**

---

## Process

### Completion Tracking

Create tasks after scoping:
- `TaskCreate`: "Mode A sweep + parse"
- `TaskCreate`: "Write codebase-audit.json"
- For `deep`/`exhaustive`: `TaskCreate`: "Mode B reconcile" and "Reconcile-join + gap re-dispatch"
- `TaskCreate`: "Present summary"

`TaskUpdate` to `in_progress`/`completed` as you go. Do NOT present results until the artifact is written and (for deep/exhaustive) every expected unit has a finding.

---

### Step 0 — Detect (always)

**See `references/detection-patterns.md` for the full matrices.**

1. **Package manager + layout**: lockfile (`package-lock.json` → npm, `pnpm-lock.yaml` → pnpm, `yarn.lock` → yarn, `bun.lockb` → bun) and `workspaces` / `pnpm-workspace.yaml` for monorepos. This picks the ephemeral runner: `npx` / `pnpm dlx` / `yarn dlx` / `bunx`.
2. **Existing tooling/config** (detect-before-anything, never duplicate): `knip.json`/`knip.jsonc`/`.knip.*`, `knip` in `devDependencies`, a `depcheck`/`ts-prune`/`unimported` config, or a `lint:dead`-style script. If a tool is already installed, **prefer the installed one** (no network needed).
3. **Language**: if the repo is not JS/TS and no equivalent dead-code tool is available, **report cleanly** ("no dead-code tooling available for `<lang>`") and skip to a Mode-B-only audit if `deep`/`exhaustive` was requested, or exit cleanly for `quick`. **Never fabricate findings.**

---

### Step 1 — Mode A sweep (all tiers)

1. Run the knip-class check **ephemerally** via the detected runner — e.g. `npx --yes knip --no-progress` (or the installed binary if present). No install, no repo mutation.
2. Parse output into: `unusedExports`, `unusedFiles`, `unusedDependencies`, `unresolvedImports`, `unusedDevDependencies`.
3. If the runner fails (offline sandbox, network block), **report the failure explicitly** — do not silently pass. Suggest the installed-tooling path or the opt-in persistence below.

**Mode A mutates nothing in the consumer's source, `package.json`, or lockfile.**

---

### Step 2 — Persistence (opt-in only)

After the sweep, if no dead-code tooling is wired into the repo, **offer** (never perform silently):

> "knip isn't wired into this repo. Want me to add it as a devDep + a `lint:dead` script so this check runs in CI? (I won't touch anything unless you say yes.)"

If accepted, follow **`install discipline`** below. v1 persists a devDep + a `lint:dead` script only (CI-line wiring is a later enhancement). Idempotent: a no-op if already wired.

---

### Step 3 — Mode B, standard tier (`deep` only)

Resolve the **intent source** (see Portability Caveat), build the shared context (dependency graph + exported API surface + Mode A results + intent), then launch parallel dimension agents.

**Use the Agent tool with `subagent_type: "Explore"` (read-only) — one agent per dimension, in a single message:**

- **Contract drift** — exported signatures/types that callers no longer match.
- **Half-wired seams** — a module imports/wires something that exists but is never invoked, or a feature flag/route declared but not reachable.
- **Declared-but-unbuilt** — intent (spec/engineering-definition) names a component with no implementation.
- **Built-but-undeclared** — implemented surface area with no intent backing (candidate dead feature).

Each agent is **fed the Mode A results** and told to exclude anything already reported. **See `references/mode-b-dimensions.md`.**

---

### Step 4 — Mode B, exhaustive tier (`exhaustive` only)

The full-coverage tier. **See `references/mode-b-dimensions.md` for the protocol and `references/output-schema.md` for the contract-ledger shape.**

1. **Announce the cost**: "Exhaustive is the expensive path — one agent per file. Proceeding." (AC: opt-in is explicit.)
2. **Build the grounded-context bundle ONCE** (dependency graph + API surface + Mode A results + intent) and pass it **identically** to every worker. No worker re-derives the global picture.
3. **Partition** the file set: default **one agent per file**; above ~150 source files, collapse to cohesive **slices** (by dependency cluster; fall back to directory), each slice small enough that no agent truncates.
4. **Dispatch** read-only `Explore` workers (Agent tool, batched to the concurrency cap). Each worker writes to disk:
   - internal-integrity findings (intra-file dead code, incoherence), and
   - a **contract ledger**: what the file **provides** (exports + signatures/types) and what it **expects** (imports + the signatures/types it relies on).
5. **Reconcile-join** (this is where drift surfaces — not mere dedup): join every `expects` against the matching `provides` across all ledgers. Flag mismatched signatures, expected-but-unprovided, and provided-but-unconsumed. Merge + dedupe integrity findings.
6. **Coverage guarantee**: count ledger files on disk against the expected unit set. **Re-dispatch any missing units until the gap is zero** — reconcile against the artifacts, never against an agent's self-report.

**Fallback (documented)**: correctness does not depend on concurrency. If the runtime can't fan out wide (concurrency caps, throttling), workers run **batched-sequentially** — full coverage is preserved by the reconcile-join + gap re-dispatch loop; only wall-clock changes.

---

### Step 5 — Write the artifact (always, every tier)

**Create** `.shipkit/codebase-audit.json` conforming to **`references/output-schema.md`** (Shipkit convention: `$schema`, `type`, `version`, `lastUpdated`, `source`, `summary`, plus findings + deltas).

- Write it on **every tier including quick** — "ephemeral" is about the tooling, never the output.
- If `.shipkit/` does not exist (non-Shipkit repo), **create it** so the artifact lands. (Writing to `.shipkit/` is sanctioned skill-data output, not a consumer-source mutation.)
- If a previous artifact exists, archive it to `.shipkit/audits/codebase-audit-[YYYY-MM-DD].json` and compute deltas (new / fixed / regressed).

---

### Step 6 — Present

```
Codebase audit complete (tier: quick|deep|exhaustive)

Scanned: X files | Package manager: pnpm | Tooling: knip (ephemeral)

Mode A (deterministic):
  Unused exports: X   Unused files: X   Unused deps: X   Unresolved imports: X

Mode B (reasoning) [deep/exhaustive only]:
  Contract drift: X   Half-wired seams: X   Declared-but-unbuilt: X   Built-but-undeclared: X
  Coverage: X/X files reconciled

Delta since last audit: +X new, -X fixed, X regressions

Top findings:
  1. [finding with file:line]
  2. ...

Full report: .shipkit/codebase-audit.json

Want me to wire knip into CI (devDep + lint:dead), or help remove any of these?
```

---

## Install Discipline (opt-in persistence only)

The **only** thing in this skill that ever touches the consumer's source/`package.json`/lockfile. Governed by:

- **Detect before install** — never add tooling/config that already exists.
- **Respect the package manager** (npm/pnpm/yarn/bun) and monorepo layout.
- **Respect existing lint config** — never clobber.
- **Surface and confirm** — adding a devDep + `lint:dead` script is a write the user approves, never silent.
- **Idempotent** — re-running on an already-wired repo is a no-op.
- **Never** delete or downgrade existing dependencies.

---

## Value-Test Honesty

This skill passes the Skill Value Test on **persistence Claude lacks**, not on capability:
- Running knip is a natural capability — Claude does it well without a skill. That is **not** the value.
- The value is the **procedural memory** (remembering the check class must run, the same way, in every repo and across sessions), the **install discipline**, and **Mode B's structured intent↔code reconciliation**.

## Portability Caveat (Mode B)

Mode A is equally portable everywhere. **Mode B's depth scales with the available intent signal:**
- In a **Shipkit repo**, intent comes from `.shipkit/` artifacts (engineering-definition components/dataContracts, architecture, active specs) — high signal.
- In a **non-Shipkit repo**, Mode B falls back to README + entry points + exported API surface — lower signal. **State this in the output** so the user knows Mode B was running with reduced intent.

---

## Differs From

| Skill | Focus |
|-------|-------|
| `/shipkit-review-shipping` | Code quality on recent changes (12 dimensions) |
| `/shipkit-preflight` | MVP production readiness checklist |
| `/shipkit-scale-ready` | Scale & operations readiness |
| `/shipkit-prompt-audit` | LLM pipeline architecture |
| `/shipkit-validate-wiring`, `/shipkit-wiring-graph` | **Framework-internal** — validate Shipkit's own component graph. This skill audits **your app code**. |

---

## Context Files This Skill Reads

| File | Purpose |
|------|---------|
| Source code + `package.json` / lockfiles | Detection + the audit target |
| `.shipkit/codebase-index.json` | Index-accelerated discovery (if present) |
| `.shipkit/engineering-definition.json`, `architecture.json`, `specs/active/*.json` | Mode B intent source (if present) |
| Previous `.shipkit/codebase-audit.json` | Delta tracking (if present) |

## Context Files This Skill Writes

**Write Strategy**: OVERWRITE with ARCHIVE.
- `.shipkit/codebase-audit.json` — the audit report (every tier; bootstraps `.shipkit/` if absent).
- `.shipkit/audits/codebase-audit-[YYYY-MM-DD].json` — archived previous report.

---

<!-- SECTION:success-criteria -->
## Success Criteria

- [ ] Package manager + monorepo layout detected; matching ephemeral runner used
- [ ] Pre-existing tooling detected and reused, never duplicated
- [ ] `quick` mutates zero consumer source/`package.json`/lockfile
- [ ] Persistence happens only after explicit confirmation and is idempotent
- [ ] Non-JS/unsupported repo reports cleanly with no fabricated findings
- [ ] `deep`/`exhaustive`: Mode A runs first; Mode B excludes Mode A findings
- [ ] Mode B intent source resolved (.shipkit/ primary, code-surface fallback) with caveat stated
- [ ] `exhaustive`: grounded bundle built once; per-file workers write ledgers to disk
- [ ] `exhaustive`: reconcile-JOINS ledgers for cross-file drift; gaps re-dispatched until coverage is complete
- [ ] Artifact written on EVERY tier (incl. quick); `.shipkit/` bootstrapped if absent
- [ ] Output conforms to the JSON schema; summary counts match findings
- [ ] Report only — no unsolicited deletion or mutation
<!-- /SECTION:success-criteria -->

---

<!-- SECTION:after-completion -->
## After Completion

Audit written to `.shipkit/codebase-audit.json`. Next steps:

1. **Remove confirmed dead code** — deletion is a natural capability; ask Claude to remove specific unused exports/files/deps, then re-run `/shipkit-codebase-audit` to verify the finding is gone.
2. **Wire the gate** — if knip isn't in the repo, accept the opt-in persistence so the check runs in CI (devDep + `lint:dead`).
3. **Go deeper before a milestone** — re-run as `/shipkit-codebase-audit deep` (or `exhaustive`) to catch contract drift and unwired seams the linter can't see.
4. **Hand to a release gate** — feed the results into `/shipkit-preflight` (production readiness) or `/shipkit-review-shipping` (change-level quality) as part of pre-ship checks.

No follow-up skill is triggered automatically — the user decides what to remove.
<!-- /SECTION:after-completion -->

---

## References

- `references/detection-patterns.md` — package-manager, tooling, and runner detection matrices; non-JS behaviour
- `references/output-schema.md` — `.shipkit/codebase-audit.json` schema + the contract-ledger shape
- `references/mode-b-dimensions.md` — Mode B dimensions (standard) and the per-file fan-out + reconcile-join protocol (exhaustive)
