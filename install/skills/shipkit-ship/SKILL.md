---
name: shipkit-ship
description: "Build a spec'd + planned feature to done — the BUILD entry point. Drives the plan to a ground-truth bar via the orchestration engine (autonomous). Triggers: 'ship it', 'ship this', 'build this', 'run the build', 'build the plan'."
argument-hint: "[plan name]"
---

# shipkit-ship — Build to Done

**Purpose**: The consumer-facing **BUILD** entry point. Takes a plan
(`.shipkit/plans/`) and drives it to a confirmed, ground-truth completion bar.

**shipkit-ship is a thin caller.** It does **not** implement its own build loop — it
states the *what* (steps + bar) and hands off to the engine, which owns the *how*
(partition → fan-out → reconcile → integrate → stop-at-bar). This is Shipkit-native
**drive-to-done**: one engine, one completion contract.

**Read first**: `install/shared/references/core-automation.md` — the contract the engine
runs. This skill only assembles the call.

---

## What it does

Invoke **`shipkit-orchestrate` in `autonomous` mode** over the plan. Nothing more —
the engine runs inline in the main session, launches the parallel build, reconciles
against ground truth, integrates serially, and stops at the bar.

Pass the engine the four inputs (calling interface in
`install/skills/shipkit-orchestrate/SKILL.md`):

| Input | For a build |
|-------|-------------|
| **steps** | the plan's phases / file-ownership clusters, in dependency order — the units to build (from `.shipkit/plans/<feature>.json`) |
| **bar** | the **ground-truth** completion criteria (below) — stated explicitly; the engine advances only when they are true on disk / in git |
| **mode** | `autonomous` (build runs unattended to the bar) — add the **scale toggle** for very large / long builds |
| **elicitive** | normally **none** — a build should run with the spec/plan already resolved. If a step genuinely needs a human decision, mark it elicitive so the engine bubbles it (never inside a workflow), rather than letting a worker guess. |

---

## The bar (state it — don't let a worker self-report "done")

A build is done only when **all** of these are reconciled (verified, not reported):

1. **Functional surface complete** — every element the no-gaps spec named across the
   four dimensions (**applications / datastores / contracts / integrations**) is built,
   not just the happy path. A frontend that implies a backend has the backend.
2. **Plan acceptance met** — every acceptance criterion / phase gate in the plan passes.
3. **Tests green** — the plan's named checks (tests, build, lint) pass.
4. **Integrated** — work is committed, rebased onto the target branch, and landed per
   the integration policy (serial, one lane at a time, never forced past unverified work).

The engine reconciles each against `git` + disk artifacts each round and re-dispatches
gaps until the bar is met or the slot ceiling hits (then it reports done-vs-outstanding
— no silent truncation).

---

## Before running

The engine confirms (via `AskUserQuestion`) the things a build must not assume: the
**bar**, the **target branch**, the **integration policy** (stage-for-review vs
auto-merge), and the **slot ceiling**. `shipkit-ship` supplies the bar above as the
default; the rest are confirmed at run start.

---

## When this skill integrates with others

### Before this skill
- `/shipkit-spec` → `/shipkit-plan` — a spec (with the no-gaps gate passed) and a plan
  must exist; the plan is the build's step list and the spec's named surface is the bar.

### What it calls
- `/shipkit-orchestrate` — the engine (autonomous mode). All dispatch / reconcile /
  integrate lives there, once.

<!-- SECTION:after-completion -->
## After Completion

The engine has driven the plan to the bar (or reported done-vs-outstanding at the slot
ceiling); run-state is in `<runDir>/orchestration.json`.

**Next:** Run `/shipkit-review-shipping` — post-build review runs as the engine in
**steered** mode, one unit per app-area / screen (frontend + backend), surfacing findings
to the user to steer.
<!-- /SECTION:after-completion -->


---

## Context files this skill reads
- `.shipkit/plans/<feature>.json` — the plan (the steps)
- `.shipkit/specs/**` — the spec's named functional surface (the bar)

## Context files this skill writes
- None directly — the engine owns run-state (`<runDir>/orchestration.json`) and
  verification output per `install/shared/references/run-artifacts.md`.

---

**Remember**: `shipkit-ship` is one engine call. Its whole job is to name the bar and
delegate. "Done" means reconciled against ground truth — not the 80% that looks finished.
