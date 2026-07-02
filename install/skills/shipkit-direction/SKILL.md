---
name: shipkit-direction
description: "Define a project's WHY/WHAT foundation autonomously — the DIRECTION entry point. Drives the definitional steps to a coherent bar via the engine (autonomous-propose): grounds every field in a cited signal, asks only the few high-leverage decisions. Triggers: 'start a project', 'define direction', 'kick off', 'set up the vision', 'direction'."
argument-hint: "[project name or one-line goal]"
---

# shipkit-direction — Define the Foundation

**Purpose**: The consumer-facing **DIRECTION** entry point. Takes a project (a repo, a
one-line goal, or nothing) and drives the definitional foundation — vision → stage →
users → product → engineering → goals — to a coherent bar, **autonomously**: it proposes
everything it can ground in a cited signal and asks only the few high-leverage decisions.

**shipkit-direction is a thin caller.** It does not implement its own loop — it states the
*what* (steps + bar + which steps are elicitive) and hands off to the engine
(`shipkit-orchestrate`), which owns the *how* (dispatch → reconcile → re-dispatch →
stop-at-bar, with elicitation bubbled to the main session). This replaces the previous
forked direction loop.

**Read first**: `install/shared/references/ground-or-ask-calibration.md` (the propose-vs-ask
rule), `install/shared/references/elicitation-protocol.md` (the marker/resume mechanics the
elicitive steps use), and `install/shared/references/core-automation.md` (the engine contract).

---

## What it does

Invoke **`shipkit-orchestrate` in `autonomous` mode** (propose variant) over the Direction
steps. The engine runs inline in the main session, dispatches each step, reconciles its
artifact against the bar, bubbles any elicitation marker to the user, and stops when the
foundation is coherent.

Pass the engine the four inputs (calling interface in `shipkit-orchestrate/SKILL.md`):

| Input | For Direction |
|-------|---------------|
| **steps** | the definitional chain, in order: `why-project → stage → product-discovery → product-definition → engineering-definition → product-goals → engineering-goals`, with `review-direction` as the assess gate |
| **bar** | each step's named `.shipkit/` artifact exists AND is **grounded** (every field cited or flagged per the calibration), AND `review-direction` passes (coherent, no gaps) |
| **mode** | `autonomous` — propose the grounded foundation, ask only the high-leverage few (fall back to `interactive` when signals are thin) |
| **elicitive** | the steps that may pause for input: `why-project`, `stage`, `product-discovery`, `product-goals`, `engineering-goals` (plus `feedback-bug` on the feedback re-entry path — six in all). The `product-definition` / `engineering-definition` synthesis steps are **not** elicitive — they derive from upstream artifacts and only propose. Each elicitive step emits `NEEDS_ELICITATION:<slug>`; the engine batches the questions to the user and resumes. |

---

## The bar (calibrated, not interrogated)

Direction is done when the foundation is **complete and grounded**, not when every field was
confirmed by hand:

1. **Every definitional artifact exists** — why → goals, each written to its `.shipkit/` path.
2. **Every field is grounded or flagged** — proposed from a cited signal (tagged with source),
   or flagged as a low-leverage guess. **No ungrounded high-leverage value is silently
   invented** (the T5 failure). Per `ground-or-ask-calibration.md`.
3. **Only the high-leverage unknowns were asked** — batched via the marker-bubble, not
   per-artifact confirm/adjust.
4. **`review-direction` passes** — the reviewer finds the foundation coherent (vision ↔ users ↔
   product ↔ engineering ↔ goals align), no gaps.

The engine reconciles each step's artifact against this bar and re-dispatches gaps.

---

## Modes

- **autonomous** (default for new projects) — propose from signals, ask the 2–3 high-leverage
  decisions. The walk-away kickoff.
- **interactive** (thin signals — empty dir, one-line prompt) — richer elicitation, still
  calibrated (grounded fields proposed for confirmation, not asked cold).

Pick by signal density; both run the same steps through the same engine loop.

---

## When this skill integrates with others

### After this skill
- `/shipkit-spec` → `/shipkit-plan` → `/shipkit-ship` — the foundation Direction defines
  feeds the build flow.

### What it calls
- `/shipkit-orchestrate` — the engine (autonomous-propose). All dispatch / reconcile /
  elicitation-bubble lives there, once.
- The 6 elicitive producers + `review-direction` as the assess gate — dispatched by the engine.

---

## Context files this skill reads
- README, the codebase, the opening prompt, and any existing `.shipkit/` artifacts — the
  cited signals the grounding pass draws on.

## Context files this skill writes
- None directly — the engine owns run-state; the producer steps write `.shipkit/why.json`,
  `stage`/goals, `product-discovery.json`, `product-definition.json`,
  `engineering-definition.json`, and `<runDir>/elicitation/<skill>/answers.md`.

<!-- SECTION:after-completion -->
## After Completion

The foundation is defined and coherent (`review-direction` passed); the `.shipkit/`
definitional artifacts carry their grounded/guessed/confirmed provenance.

**Next:** Run `/shipkit-spec` to spec the first feature from the foundation, then
`/shipkit-plan` → `/shipkit-ship`.
<!-- /SECTION:after-completion -->

---

**Remember**: direction is one engine call in propose mode. Its whole value is a *grounded*
foundation with the few real decisions surfaced — not a wall of questions, and not a wall of
confident guesses.
