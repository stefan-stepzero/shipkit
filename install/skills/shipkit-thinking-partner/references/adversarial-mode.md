# Adversarial Mode — Debate Orchestration

This reference holds the full orchestration logic for the thinking-partner's **adversarial mode**. The SKILL.md only detects the mode and hands off here. Read this file when adversarial mode is triggered.

**What adversarial mode is:** instead of one interactive discussion, the thinking-partner convenes a panel of single-minded **resource advocates** (see `resource-advocates.md`) who debate a concrete decision over 3 rounds — autonomously, with no user input during the debate — then it synthesizes the debate into a tension map + decision matrix.

**Why it exists:** a single agent playing all sides drifts toward premature consensus. Real advocates pushing hard for their own resource surface conflicts that balanced analysis smooths over. The output is the *tension*, made explicit and unavoidable.

---

## Architecture (how the dispatch actually works)

The thinking-partner runs **inline** in the main conversation (it is not a fork — this is deliberate, so it can use `AskUserQuestion`). It orchestrates the debate by dispatching the `shipkit-resource-advocate` skill once per advocate per round, via the **Skill tool**. Each dispatch spawns a forked advocate (`context: fork` + `shipkit-resource-advocate-agent`) with its own isolated context.

```
User → /shipkit-thinking-partner (adversarial trigger)
  └─ [inline orchestrator, main conversation]
       ├─ Skill: /shipkit-resource-advocate "time" "<context>" round:opening      → [fork] → position
       ├─ Skill: /shipkit-resource-advocate "scope" "<context>" round:opening     → [fork] → position
       ├─ ... (one dispatch per advocate, per round)
       └─ [inline] synthesize all positions → tension map + decision matrix
```

This is **one level of fork** (inline orchestrator → advocate fork). DOC-023 confirms an inline/main context can dispatch forks via the Skill tool, forks can read `references/`, and forks return their output to the caller. Agent Teams (`TeamCreate`) is intentionally NOT used — it has a known Windows in-process shutdown bug and is reserved for the future parallel-execution upgrade.

> **Note vs. spec:** the original spec described "2-level nesting" assuming the thinking-partner was itself a fork. It is not — it stays inline so `AskUserQuestion` works for setup. The functional requirement (each advocate runs in its own fork via Skill dispatch) is fully met.

---

## Step A — Confirm the debate inputs (the only user interaction)

Use `AskUserQuestion`. Gather exactly three things, then run autonomously:

1. **The decision** — restate the concrete decision to be debated in one sentence. Confirm or refine.
2. **The options** — the 2-4 concrete options on the table (e.g. "Option A: rebuild now" vs "Option B: patch and defer"). If the user hasn't given options, ask for them — a debate needs something to debate.
3. **Advocate selection (optional override)** — propose 3-5 advocates from the pool (see selection guidance in `resource-advocates.md`), and let the user override. Show the proposed set with a one-line reason each. Default to your proposed set if they don't override.

**Selection rules:**
- Pick 3-5 advocates. Never fewer than 3 (too thin), never more than 5 (token blow-out, diminishing returns).
- Always include at least one pair of **natural enemies** — otherwise the debate is flat. If the user's override has no opposing tension, warn them.
- Bind the selection to the actual decision, not generic defaults.

After Step A, **do not ask the user anything else until synthesis.** The debate runs autonomously.

---

## Step B — Build the decision context payload

Assemble a compact, self-contained context string passed to every advocate. It must include:
- The decision (one sentence).
- The options (labeled A/B/C... with a one-line description each).
- Any hard constraints from `.shipkit/why.json`, `architecture.json`, `stack.json` already read in Step 1 (stage, budget, deadline, non-negotiables) — summarized, not pasted wholesale.

Keep it tight (target < 250 words). Every advocate gets the *same* context; only the `resource-id` and `round` differ.

---

## Step C — Run the 3 rounds

Fixed at 3 rounds. More rounds = diminishing returns. Each advocate gets `maxTurns: 3` per dispatch (runaway guard).

### Round 1 — Opening Positions
- For each selected advocate, dispatch:
  `/shipkit-resource-advocate "<resource-id>" "<decision-context>" round:opening`
- Each advocate argues for its resource's priority **with no knowledge of the others' positions**.
- Collect each returned position. Keep them structured (see Position Format below).

### Round 2 — Rebuttals
- For each advocate, dispatch:
  `/shipkit-resource-advocate "<resource-id>" "<decision-context>" round:rebuttal positions:<round1-summary>`
- Pass a **summary** of all Round 1 positions (NOT verbatim — summarize each to resource + position + key argument + concession, to keep payloads compact).
- Each advocate must respond to the strongest counter-arguments, especially from its natural enemies, while defending its resource. It must acknowledge at least one valid point from another advocate.

### Round 3 — Final Statements
- For each advocate, dispatch:
  `/shipkit-resource-advocate "<resource-id>" "<decision-context>" round:final positions:<round1-summary> rebuttals:<round2-summary>`
- Each advocate makes a final, concise case and MUST state:
  - its **#1 non-negotiable** (the one thing it will not trade away), and
  - its **biggest concession** (what it accepts giving up).
- This round produces the raw material for synthesis.

**Dispatch is sequential in v1** (one advocate at a time). Opening-round positions are independent and are the first candidate for the future parallel (TeamCreate) upgrade.

### Position Format (what each advocate returns)
Each advocate returns a compact block:
```
RESOURCE: <id>
POSITION: <1-2 sentence stance on this decision>
KEY ARGUMENT: <the single strongest point>
ATTACKS: <which option(s)/other-resource(s) it argues against, and why>
CONCESSION: <what it concedes — required in round:final, optional earlier>
```
Keep payloads compact — summarize prior rounds, never pass full transcripts forward.

---

## Step D — Synthesize (the deliverable)

After Round 3, the orchestrator (inline) produces a synthesis with **all five** components, in this order. This stays in the conversation — no files are written (consistent with thinking-partner's no-write philosophy).

### 1. Tension Map
A table of the fundamental conflicts the debate surfaced — the tradeoffs that can't be resolved, only chosen between.

```
| Conflict | Resources | Core Tension |
|---|---|---|
| Speed vs Quality | time ↔ scope | Shipping fast means accepting incomplete features |
| Cost vs UX | cost ↔ ux | Better UX requires more design/research investment |
```

### 2. Decision Matrix
A weighted scoring of each option against the debated resources. **Weights are derived from the debate itself** — resources whose advocates made the strongest, least-rebutted case get higher weight. State the weight next to each resource and show the weighted total.

```
| Option | Time (3) | Cost (2) | UX (4) | Weighted Total |
|---|---|---|---|---|
| Option A | 8 | 6 | 3 | 48 |
| Option B | 4 | 8 | 7 | 56 |
```
Briefly say *why* each weight is what it is (one line), so the user can challenge it.

### 3. Consensus Points
What all advocates agreed on — these are the safe decisions, the moves no resource objected to.

### 4. Non-Negotiables
Each advocate's #1 non-negotiable from Round 3 — the hard constraints any chosen option must satisfy.

### 5. Recommended Exploration
If the debate exposed unknown unknowns, unresolved questions, or a missing advocate/perspective, list them for the user to chase down.

**Do not declare a winner.** Present the tension and the matrix; the user chooses what to sacrifice. The matrix informs, it does not decide.

---

## Step E — Persistence handoff

Identical to interactive mode. The synthesis stays in conversation; suggest the appropriate capture skill:

| If the debate resolved... | Suggest |
|---|---|
| An architecture/technology decision | `/shipkit-engineering-definition` |
| Feature scope or what to build | `/shipkit-product-definition` or `/shipkit-spec` |
| An implementation approach | `/shipkit-plan` |
| Project vision/strategy/stage | `/shipkit-why-project` or `/shipkit-stage` |

Remind the user that conversation context doesn't survive sessions — the tension map and decision matrix are worth copying into an artifact while fresh. Do NOT write files yourself.

---

## Token budget (set expectations)

3-5 advocates × 3 rounds × ~500 tokens/position ≈ 4,500-7,500 tokens of debate, plus synthesis. Total ≈ **10,000-15,000 tokens**. Before launching, tell the user the rough cost and that it runs autonomously once started, so they can opt for interactive mode instead if they only want a quick gut-check.

---

## Guardrails

- **3 rounds, fixed. 3-5 advocates, capped at 5.** No exceptions — these bound the cost.
- **No user input between Step A and synthesis.** Adversarial mode's whole point is an autonomous debate the user watches, not steers.
- **Advocates must stay opinionated.** If a returned position reads balanced/bland, the dispatch failed its purpose — note it in synthesis rather than presenting it as genuine tension.
- **Summarize between rounds.** Never forward full prior-round text — it bloats payloads and blows the budget.
- **Inline orchestrator only.** Do not convert the thinking-partner to a fork — it would lose `AskUserQuestion` and break Step A.
