---
name: shipkit-orchestrate
description: "Core automation engine. Drives a set of steps to a confirmed ground-truth bar via a main-session delegate → reconcile → re-dispatch loop. Phase skills (build, review, direction) call it; can also run directly. Two modes: autonomous (run to done unattended) and steered (coordinate, surface to user). Triggers: invoked by a phase skill, 'orchestrate', 'drive to done', 'run this to done', 'coordinate the team'."
effort: high
---

# shipkit-orchestrate — Core Automation Engine

**Purpose**: One reusable orchestration loop that every phase skill calls, so Shipkit
has exactly **one way to drive work to completion** instead of a separate hand-rolled
loop per phase. It dispatches units, **reconciles their output against ground truth**
(never self-reports), re-dispatches the gaps, integrates, and stops at an agreed bar.

**Read first**: `install/shared/references/core-automation.md` — the contract (substrate
choice, the worktree finding, partition, the ledger, ground-truth reconciliation,
integration policy, the parallel-build lifecycle, deterministic-mechanism-vs-judgment).
This SKILL.md is the entry point; the contract is the machinery.

**Runs inline in the main session.** The engine launches Workflow fan-outs and drives
git + `AskUserQuestion`, all of which require the main session — it is *not* a forked
orchestrator. A phase skill that needs parallel fan-out hands its plan **up** to the
engine (which the main session is running), and the engine launches.

---

## Calling interface

A caller invokes the engine with four things:

| Input | What it is |
|-------|------------|
| **steps** | the ordered / parallel units to drive — each a `{ skill or work, artifact }` pair (what to run, what it must produce) |
| **bar** | the **ground-truth completion criteria** per step — the named `.shipkit/` artifacts that must exist + any check (tests green, review passed). This is what "done" means; the caller must state it. |
| **mode** | `autonomous` or `steered` (see `references/modes.md`) |
| **elicitive** | which steps may need user input — handled via the marker-bubble, never inside a workflow |

**The engine owns the loop; the caller owns the WHAT.** No caller re-implements
dispatch / reconcile / re-dispatch — that lives here, once.

---

## Modes (governance)

See `references/modes.md` for the full treatment. In brief:

- **autonomous** — run the steps to the bar unattended; reconcile against ground truth
  each round; re-dispatch gaps; stop at the bar or the slot ceiling. Used by *build*
  and *direction-propose*. (Shipkit-native drive-to-done.)
- **steered** — the main session coordinates; one unit per area; surfaces back to the
  user to steer between rounds. Used by *review* and interactive build. (Shipkit-native
  team-lead.)
- **scale toggle** — a resilience flag on autonomous (rate-limit-aware pacing) for very
  large fan-outs; not a separate mode.

---

## The loop

Each round (contract §5):

1. **Dispatch / resume** this round's units on the chosen substrate (§1 substrate rule:
   mechanical+parallel+no-input → Workflow fan-out from the main session; needs-input →
   inline / marker-bubble; ZDR/disabled/unsupported → Agent-Teams fallback).
2. **Reconcile against ground truth** — verify named artifacts on disk / git state;
   **never** trust a unit's "done". Count real outputs vs the expected set.
3. **Re-dispatch the gaps** until zero, the bar is met, or the slot ceiling hits.
4. **Integrate** completed work per policy (§7: stage-for-review default; serial land,
   one at a time, never force past unverified work).
5. **Update the ledger** (`.shipkit/orchestration.json`); early-exit at the bar.

**Stop condition**: the bar is met (every step's named artifact exists + passes its
check) — reconciled, not reported.

---

## Parallel build (autonomous)

For a build over `.shipkit/plans/`, run the lifecycle (contract §8):

**partition** into disjoint file-ownership clusters → **worktree-rooted fan-out** (one
Workflow agent per cluster, `isolation:'worktree'`) → **sync** each lane (commit +
rebase onto target) → **serial integrate** at the main session (land ready lanes one at
a time, never forcing past unseen work) → **teardown** each landed + clean worktree.

The git / worktree / ledger mechanism is **scripted-deterministic** (run as commands,
not LLM steps); the **partition, the bar, and review are judgment** (contract §9).

---

## Elicitation (steps that need a human)

An elicitive step runs as a forked skill that emits `NEEDS_ELICITATION:<skill>` on its
final line and writes its questions to `.shipkit/elicitation/<skill>/questions.md`. The
engine (main session) detects the marker, runs `AskUserQuestion` for the batched
high-leverage questions, writes `answers.md`, and re-invokes the step. **Never** elicit
inside a workflow agent (contract §6; protocol in
`install/shared/references/elicitation-protocol.md`).

---

## Ground-truth reconciliation (the non-negotiable)

The engine **advances a step only after its named artifact exists and passes the bar**
— verified on disk / git, not self-reported (contract §0, §5). A unit that returns
"done" with no artifact / no commit is a gap and is re-dispatched. This is the single
behaviour that separates the engine from "dispatch and hope".

---

## Standalone invocation

If invoked directly (not by a phase skill): ask for the **steps** + **bar** + **mode**
(use `AskUserQuestion` — don't assume the bar), write them to
`.shipkit/orchestration.json`, then run the loop.

---

## Orchestration tracking

`.shipkit/orchestration.json` is the ledger (contract §4). Read it first (merge, don't
clobber), record the partition, per-unit status (`claimed`/`working`/`ready`/`landed`/
`blocked`), the bar, target branch, integration policy, and per-round integration. It
is the resume point and the ground truth for reconciliation — not the conversation.

---

## When this skill integrates with others

### Callers (invoke the engine)
- **build** (over `.shipkit/plans/`) — engine in autonomous mode; bar = the no-gaps
  spec's named surface + the plan's acceptance + tests green.
- **review** — engine in steered mode, one unit per area/screen, frontend + backend.
- **direction** — engine in autonomous-propose mode over the Direction steps.

(These callers are thin — they state steps + bar + mode + elicitive and hand off. They
do not re-implement the loop.)

### Substrate fallback
- **Agent Teams** — the documented fallback substrate for ZDR / `disableWorkflows` /
  hosts without the Workflow tool. Same completion contract, same `.shipkit/` flow.

---

## Context files this skill reads
- `.shipkit/orchestration.json` — the ledger (resume point)
- `.shipkit/plans/`, `.shipkit/specs/` — the work (per caller)
- `.shipkit/elicitation/<skill>/answers.md` — collected answers on resume
- `install/shared/references/core-automation.md` — the contract
- `install/shared/references/elicitation-protocol.md` — the marker + file schema

## Context files this skill writes
- `.shipkit/orchestration.json` — ledger / run-state
- `.shipkit/elicitation/<skill>/questions.md` is written by the elicitive step; the
  engine writes `.shipkit/elicitation/<skill>/answers.md`

---

**Remember**: the engine is the *one* completion loop. Its whole value is that "done"
means *reconciled against ground truth*, identically across build, review, and
direction — not the 80% that looks finished.
