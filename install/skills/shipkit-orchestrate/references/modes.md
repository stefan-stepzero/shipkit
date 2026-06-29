# Orchestration modes

The engine has one loop (delegate → reconcile-against-ground-truth → re-dispatch →
stop-at-bar; see `install/shared/references/core-automation.md`). **Mode** is the
*governance* wrapped around that loop — who steers, and whether it runs unattended. Same
loop, same `.shipkit/` artifact flow, same ground-truth rule in every mode.

---

## autonomous — run to the bar, unattended

The main session acts as coordinator/integrator and drives the loop to completion
without waiting on the user. This is the Shipkit-native **drive-to-done**.

- **When**: build over a plan; direction-propose; any scope where the bar is explicit
  and the work is largely mechanical or independently verifiable.
- **Confirm before running** (use `AskUserQuestion`): the **bar** (what must be true per
  item to count as done — tested / reviewed / matches spec / named checks), the
  **target branch**, the **integration policy** (stage-for-review vs auto-merge), and a
  **slot ceiling** (the hard cap on rounds, e.g. 6 rounds). The bar confirmation is the
  whole reason this is governed and not just "keep going".
- **Substrate**: Workflow fan-out from the main session is the default (resumable via
  `resumeFromRunId`, automatic per-agent worktrees). Fall back to teams only per the
  substrate rule.
- **Loop**: each slot dispatches/resumes the round, reconciles against ground truth
  (`git log`, disk artifacts — never self-reports), re-dispatches gaps, integrates per
  policy, updates the ledger, and early-exits the moment the scope meets the bar.
- **Stop**: bar met, or slots exhausted (then report what's done vs outstanding — no
  silent truncation).

## steered — coordinate, surface to the user

The main session is the coordinator; the user stays in the loop and steers between
rounds. This is the Shipkit-native **team-lead**.

- **When**: review (one unit per app-area / screen, frontend + backend); interactive
  build; anything where the user wants to direct as findings come in.
- **Flow**: partition into areas, dispatch one scoped unit per area, read back *concise*
  summaries (not dumps), surface findings/decisions to the user, take direction, then
  dispatch the next round. The lead coordinates through units — it does not implement
  inline.
- **Substrate**: teammates (addressable, live SendMessage steering) or subagents per
  area; worktrees only if units would edit overlapping files. Workflow fan-out for any
  mechanical sub-phase, launched from the main session.
- **Reconciliation**: same ground-truth rule — verify each area's output before marking
  it done; the user steers, but "done" is still reconciled, not reported.

## scale toggle — resilience on autonomous

Not a separate mode: a flag on **autonomous** for very large or very long fan-outs.

- Rate-limit-aware pacing (a rate-limited agent returns its error *as result text*;
  reconciliation catches it and re-dispatches).
- Lean on Workflow resumability (`resumeFromRunId`) so a multi-hour run survives
  interruption.
- Respect the concurrency caps (`min(16, cores-2)` concurrent, 1000 total) — size the
  round and let the rest queue.

---

## Picking the mode (caller guidance)

| Caller | Mode | Why |
|--------|------|-----|
| build (over a plan) | autonomous | bar is explicit (named surface + acceptance + green); mostly mechanical parallel work |
| direction (new project) | autonomous-propose | propose the grounded foundation, bubble only the few high-leverage questions |
| review | steered | judgment per area; the user wants findings surfaced to steer |
| interactive build | steered | user directing as it goes |
| huge unattended build | autonomous + scale | long run; needs resumability + pacing |

In every mode the contract is identical: partition, dispatch, **reconcile against
ground truth**, re-dispatch gaps, integrate serially, stop at the bar.
