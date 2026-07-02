# Ground-or-Ask Calibration

**The rule that makes autonomous Direction safe.** An elicitive skill running autonomously
must neither silently invent ungrounded values (the T5 hallucination failure) nor ask the
user about everything (which defeats autonomy). This file is the calibration contract every
elicitive skill references. Do not paraphrase or re-derive it — cite this file.

Pairs with `install/shared/references/elicitation-protocol.md` (the *mechanics* — marker,
state files, resume). This file is the *intelligence* — deciding, per field, propose vs ask.

---

## The core rule: GROUND-OR-ASK, gated by leverage

For **every field** the artifact needs, classify it:

1. **Grounded** — there is a **cited signal** for it (the opening prompt, `README`, the
   codebase, `package.json`, an upstream `.shipkit/` artifact). → **Propose** the value,
   **tagged with its source**. Do not ask.

2. **Ungrounded** — no signal supports it. It's a genuine unknown. Now apply the **leverage
   gate**:
   - **High-leverage** (uncertainty is real AND the cost of being wrong is high /
     hard-to-reverse) → make it a **candidate question**. These — and only these — become
     `NEEDS_ELICITATION` questions bubbled to the user (batched, a few at a time).
   - **Low-leverage** (cheap to change later, or any reasonable default works) → **propose a
     flagged default** (`guessed`, no source), don't ask. The user can correct it later.

**The failure modes this prevents:**
- Under-ask + guess an expensive decision silently → the T5 hallucination (a confidently
  invented product concept with no flags). **Never** propose an ungrounded *high-leverage*
  field as if it were grounded — that one must be asked.
- Over-ask → a 20-question interrogation that defeats the walk-away kickoff.

---

## Leverage test (apply to each ungrounded field)

Ask a field only if **both** are true:

- **Uncertainty is real** — you genuinely can't infer it from any signal (not just "I'd like
  confirmation"). If a signal points at it, it's grounded — propose, don't ask.
- **Cost-of-wrong is high** — a wrong guess is expensive to discover late or hard to reverse:
  it reshapes scope, sets a hard constraint, picks a one-way-door technology, or defines who
  the product is *for*. Renaming a field later is cheap; mistaking the target user is not.

If only one holds → propose a flagged default. If neither → propose from the obvious default.

Rule of thumb: **2–3 questions** for a typical new project, never per-artifact confirm/adjust.
If you're about to ask more than ~5, your grounding pass was too shallow — re-scan the signals.

### Weak / partial signals (the common middle case)

Signals are rarely binary. A README that says "for developers" *suggests* `targetUsers` but doesn't pin it down. Handle the middle explicitly:

- **A weak signal grounds a field only as a `guessed` default with the signal cited as its basis** — not as a confident grounded value. Propose it, flagged, so the user can correct it.
- **Escalate a weakly-grounded field to a question only if it's also high-leverage.** "For developers" is a weak signal on `targetUsers` (high-leverage) → propose "developers" as a flagged default AND, if the product hinges on *which* developers, ask the one sharpening question. A weak signal on a low-leverage field → just take the flagged default, don't ask.

The test: **would a wrong reading of this weak signal be expensive?** If yes, it's a candidate question despite the hint; if no, the hinted default is fine.

---

## Output shape: separate guessed / confirmed / needs-your-decision

Whatever the skill proposes, the proposal (and the artifact's provenance) must make three
buckets visible so the human can scan them in seconds:

| Bucket | Meaning | How it's tagged |
|--------|---------|-----------------|
| **Grounded** | proposed from a cited signal | `source: <signal>` (e.g. `README §Goals`, `package.json deps`, `opening prompt`) |
| **Guessed** | proposed default, no signal, low-leverage | `guessed: true` — visibly flagged, safe to ignore or fix later |
| **Needs your decision** | the few high-leverage unknowns | surfaced as the batched questions (the only things that pause) |

**Persist provenance in ONE canonical shape** (do not invent per-skill variants): a top-level
`_grounding` map in the artifact, keyed by the field path, each entry one of:

```json
"_grounding": {
  "targetUsers": { "source": "README §Audience" },
  "vision":      { "guessed": true, "basis": "weak signal: prompt mentions 'dashboard'" },
  "successCriteria": { "needsDecision": true }
}
```

`source` = grounded from a cited signal · `guessed` = flagged default (with `basis` if from a weak
signal) · `needsDecision` = one of the high-leverage questions that paused. Every proposed value
appears in `_grounding`; an untagged value is a bug. This makes "what did Claude guess vs know?"
answerable after the fact, consistently across every elicitive skill.

---

## How it composes with the elicitation protocol

1. **Grounding pass first.** Before generating any question, scan the cited signals and
   propose every field you can ground. This is what shrinks the question set.
2. **Only high-leverage ungrounded fields become questions.** Feed *those* into the
   elicitation-protocol's question generation (`questions.md`), emit the
   `NEEDS_ELICITATION:<slug>` marker, and pause — per `elicitation-protocol.md`. Everything
   grounded or low-leverage is already proposed; it does not pause.
3. **Inline mode still asks** (it has `AskUserQuestion`), but asks the *same* calibrated set —
   the few high-leverage questions — not a full interrogation. Autonomy and interactivity
   differ only in *how* the questions are delivered, not *which* questions.

---

## Modes

- **AUTONOMOUS (default for new projects)** — propose the grounded foundation, ask only the
  2–3 high-leverage decisions via the marker-bubble. The walk-away kickoff.
- **INTERACTIVE (fallback when signals are thin)** — richer elicitation, but still calibrated
  (grounded fields are proposed for confirmation, not asked from scratch).

Direction picks the mode from signal density (a greenfield repo with a rich README → autonomous;
an empty dir with a one-line prompt → interactive). Selected via the existing gated/autonomous switch.

---

## Do / Don't

- **Do** cite the signal for every proposed value. An untagged proposed value is a bug.
- **Do** flag every guess. A silent guess on a high-leverage field is the T5 failure.
- **Don't** ask what a signal already answers. That's over-asking.
- **Don't** propose an ungrounded high-leverage value as settled. That's the dangerous one — ask it.
- **Don't** exceed a handful of questions. If you are, re-ground first.
