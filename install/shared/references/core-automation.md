# Core automation — the orchestration contract

The canonical contract behind **`shipkit-orchestrate`**. Phase skills (build, review,
direction) and the engine itself read this. It defines *how Shipkit drives a set of
steps to completion*: choose a substrate, dispatch, reconcile against ground truth,
re-dispatch the gaps, integrate, stop at the bar. One contract, two governance modes
(see `references/modes.md`).

This is consumer-portable — it depends only on Claude Code primitives (Workflow tool,
Agent/teams, Bash/git) and the `.shipkit/` workspace. Nothing user-specific.

---

## 0. The one rule

**Advance only on ground truth, never on a worker's self-report.** Everything below
serves that rule. An agent's return text over-claims, and a rate-limited agent returns
the API error *as its result text without throwing*. So "done" is never a claim you
accept — it's a state you verify on disk / in git. (§5)

---

## 1. The substrate: Workflow vs teams vs subagents

Three ways to run work in parallel. Pick by the job, not habit.

| | Workflow tool | Agent teams (teammates) | Plain subagents |
|---|---|---|---|
| Coordination | deterministic JS script | autonomous peers + mailbox + shared task list | main session's judgment, per turn |
| Per-agent worktree | `agent({isolation:'worktree'})` — automatic | manual only (coordinator wires it) | `isolation:"worktree"` (then not addressable) |
| Launch site | **main session only** | main session / lead only | any |
| Live mid-run steering | no (fire-and-collect) | yes (SendMessage a teammate) | limited |
| Resumable after crash | **yes** (`resumeFromRunId`) | no | no |
| Can run git/shell | no — integrate inline after | yes | yes |

**Verified substrate facts** (don't re-derive):
- **Workflows launch from the main session only.** A forked skill/subagent has no
  Workflow tool. So the engine runs **inline in the main session** — it cannot itself
  be a forked orchestrator. A phase skill that wants parallel fan-out hands the plan
  **up** to the engine, which launches.
- **Workflow agents have full filesystem access** to the parent cwd (default) or to
  their own worktree (`isolation:'worktree'`). The `.shipkit/` coordination substrate
  survives on workflows.
- **Concurrency caps**: `min(16, cores-2)` concurrent, 1000 total per workflow run.
  Size the parallel sub-phase to fit; excess queues.
- **Resumable**: a workflow run is resumable via `resumeFromRunId` (same session) —
  this is why it's the default for long unattended runs.
- **No elicitation inside a workflow agent** — workflow agents take no mid-run user
  input. Anything needing a human goes through the marker-bubble (§6).

**Substrate rule (how the engine chooses):**
- mechanical + parallel + no user input + bounded → **Workflow** fan-out (the default
  for parallel build).
- needs human input → run **inline at the main session**, or fork + **marker-bubble**
  (§6).
- ZDR / `disableWorkflows` / a host where workflows aren't available → **Agent-Teams
  fallback**, with the *same* completion contract and the *same* `.shipkit/` artifact
  flow. It is a fallback substrate, not a second control plane.

## 2. The worktree finding (load-bearing)

Naming a background `Agent` routes it to the **teammate** path, which **ignores
`isolation:"worktree"`** — it commits to the shared checkout. Teammates *can* use
worktrees, but only if the coordinator wires it (`git worktree add` + brief each
teammate to use `git -C <path>`). Automatic per-agent worktrees + resumability exist
only on the **Workflow** path.

**Implication:** if dispatched units touch *disjoint* files, you don't need worktrees —
the shared-dir model is fine. You need worktrees only when units would otherwise edit
**overlapping** files in parallel. A worktree-isolated unit is rooted in its worktree
(`CLAUDE_PROJECT_DIR` = the worktree) — which is what lets a unit nest its own team
without cross-writing the trunk.

## 3. Partition discipline — one scoped unit per area

The point of fan-out is *clean, directed context per unit*. Partition the work into
disjoint slices (by file-ownership cluster, page, area, or item) so each unit owns one
slice, and give each a **tight brief**: only its paths, the one outcome it owns, and
its acceptance criteria. Never hand a unit "the whole thing, find your part" — that
invites context bloat and overlap. Smaller, well-bounded slices = lower blast radius
and easier reconciliation.

## 4. The ledger — state survives context

**Run root (collision avoidance).** At run start the engine mints a **run id** and a
**run root**, and writes `.shipkit/active-run.json` (`{runId, runDir, startedAt}`) so
dispatched units and concurrent skills can find it; it also passes `SHIPKIT_RUN_DIR` in
to any workflow agent (which can't mint its own id). **Transient** artifacts — run-state,
elicitation scratch, verification/preflight reports, QA outputs, work-memory checkpoints,
generated HTML — are written under the run root (`.shipkit/runs/<run-id>/…`), NOT the
fixed path, so parallel runs / shared-cwd workflow agents / two runs at the same repo
root don't stomp each other. **Durable singletons** (definitions, specs, architecture-map)
are never run-scoped. The full rule + the transient-vs-durable lists live in
`install/shared/references/run-artifacts.md` — writers and readers both cite it.

The engine's run-state is itself a transient artifact: `<runDir>/orchestration.json`. It
is the **file** source of truth (not the conversation). Record:
- the partition and which unit owns each slice,
- per-unit status: `claimed` / `working` / `ready` / `landed` / `blocked`,
- the bar (the ground-truth completion criteria) and the target branch + integration
  policy,
- what was integrated each round and what's outstanding.

The conversation drifts; the ledger is re-readable ground truth the engine re-orients
from at any point (and across a resume).

## 5. Reconcile against ground truth (the loop)

Each round:
1. **Dispatch / resume** the units for this round (per the substrate, §1).
2. **Reconcile** — verify, don't trust:
   - code: `git log <target>..<branch>`, `git diff --stat`, files on disk;
   - artifacts: the actual named `.shipkit/` files vs the expected set.
   Count real outputs against the expected set. A unit that "reported done" but produced
   no artifact / no commit is a **gap**.
3. **Re-dispatch the gaps** until zero, or the bar is met, or the slot ceiling hits.
4. **Integrate** completed work per the policy (§7).
5. **Update the ledger.** Early-exit the moment the scope meets the bar.

Reconciliation is proven at the merge, not assumed from the dispatch.

## 6. Elicitation — the marker-bubble (never inside a workflow)

A step that needs a human decision must not guess silently and must not block a
workflow agent (which can't take input). Protocol:
- the elicitive step runs as a **forked skill** that, when it hits a genuine question,
  writes its questions to `.shipkit/elicitation/<skill>/questions.md` and emits
  `NEEDS_ELICITATION:<skill>` **on its final return line**;
- the engine (main session) **detects the marker**, runs `AskUserQuestion` for the
  batched high-leverage questions, writes `.shipkit/elicitation/<skill>/answers.md`,
  and **re-invokes** the step to resume.
- Elicitation only ever happens at the main session — never inside a workflow agent.

See `install/shared/references/elicitation-protocol.md` for the marker + file schema.

## 7. Integration policy

When units produce code on branches/worktrees, the engine integrates into the target
branch. Two policies:
- **stage-for-review** (default): merge into a staging/integration branch, or leave
  branches for the user to review before they hit `main`. Safer.
- **auto-merge**: merge into the target each round once the bar passes. Use only when
  the bar is trusted and the run is unattended.

**Serial integration discipline** (parallel build): report ready lanes (committed,
rebased onto latest target, green), then land them **one at a time** — never force past
unseen or unverified work. A failed integration stops the line; it does not get forced.

**Never add AI-attribution / co-author trailers to integration commits.**

## 8. Parallel build lifecycle (the autonomous build shape)

The concrete shape of an autonomous parallel build — the common case:

1. **Partition** the build into disjoint file-ownership clusters (§3).
2. **Fan out** one workflow agent per cluster, each `isolation:'worktree'` and rooted
   in its worktree (§2). A unit may itself fan out.
3. **Work** — each unit builds its slice to its brief.
4. **Sync** each lane — commit, then rebase onto the latest target.
5. **Serial integrate** at the main session — land ready lanes one at a time, never
   forcing past unseen/unverified work (§7).
6. **Teardown** each landed + clean worktree and its branch.

## 9. Deterministic mechanism vs judgment

Two layers — keep them separate:
- **Scripted mechanism** (deterministic, NOT an LLM step): worktree create/root,
  commit, rebase, ledger read/write, land, teardown. These are git/CLI commands the
  engine runs directly. Predictable, cheap, auditable. (Repo principle: *build
  capabilities as CLIs; the deterministic mechanism is scripted.*)
- **Judgment** (LLM steps / skills): the partition, the completion bar, the review,
  conflict resolution. These need a model.

Don't drive git through an LLM when a command will do; don't script a judgment call.
