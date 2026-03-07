---
name: shipkit-master
description: Master orchestrator — dispatches direction, planning, and shipping loops sequentially. Auto-loaded via session-start hook.
disable-model-invocation: true
context: fork
agent: shipkit-orch-master-agent
---

# shipkit-master - Master Orchestrator

**Purpose**: Sequential loop orchestrator. Dispatches direction → planning → shipping, with each loop managing its own internal feedback cycle via dedicated reviewers.

**Auto-loaded** at every session start via `shipkit-session-start.py` hook.

---

## Architecture

```
Master (sequencer — this skill)
  ├→ /shipkit-orch-direction  (fork → orch-direction)   → strategic artifacts + review
  ├→ /shipkit-orch-planning   (fork → orch-planning)    → definitions/specs + review
  └→ /shipkit-orch-shipping   (fork → orch-shipping)    → implementation + verification
```

Each loop orchestrator runs a **dispatch-assess-redispatch** cycle internally. Feedback stays within loops. The master stays a simple sequencer.

## Dispatch

```
1. Dispatch /shipkit-orch-direction → blocks until direction stable
2. Dispatch /shipkit-orch-planning  → blocks until planning stable
3. Dispatch /shipkit-orch-shipping  → blocks until shipping complete
4. Done → termination protocol
```

## State

Reads/writes `.shipkit/orchestration.json` for crash recovery and session continuity. If the file exists, skip completed loops and resume at the active one.

## User Input

- **Explicit skill invocation** → route directly, bypass loop dispatch
- **Keyword match** → consult `references/routing-tables.md`
- **Open-ended request** → classify to a loop, dispatch that loop
- **Input destabilizes outer loop** → block inner loops, switch to affected loop (see `references/input-classification.md`)

## Session Start Behavior

1. Read `.shipkit/orchestration.json` for `nextRecommended` and loop states
2. Scan `.shipkit/goals/` for loop stability
3. Display status and wait for user input — don't auto-execute

## Reference Documentation

- `references/routing-tables.md` — Keyword → skill routing
- `references/orchestration-modes.md` — Gated vs autonomous modes
- `references/termination-protocol.md` — Exit conditions and report format
- `references/input-classification.md` — How to classify user input to loops
- `references/loop-guards.md` — Stability criteria and maxTurns budgets
- `references/file-freshness-logic.md` — Artifact staleness detection

## Special Behaviors

- **Protected files**: Prevent manual editing of `.shipkit/` context files — route to appropriate skill
- **Progressive disclosure**: Orchestration context loaded at session start (~1500 tokens), reference docs on demand
- **Natural capabilities**: Implementation, debugging, testing, refactoring don't need skills — just do them
