# Discussion Styles

Four conversation modes for the thinking partner. The first three are **interactive** (user in the loop every step). The fourth, **Adversarial**, is **autonomous** — a panel of resource advocates debates while the user watches. Offer the interactive three at the start of an interactive discussion; Adversarial is entered via its own triggers (see `adversarial-mode.md`).

---

## Socratic Mode

**Best for:** Users who learn by discovering answers themselves. Founders who need to articulate their own reasoning. Early-stage exploration where the answer isn't clear yet.

**How it works:**
- Almost entirely question-driven
- Claude asks, user answers
- Claude follows up based on what the answer reveals (or doesn't)
- Claude rarely states opinions — instead asks questions that expose the implications

**Example flow:**
1. "What problem are you trying to solve?"
2. "Who has this problem most acutely?"
3. "What are they doing today without your solution?"
4. "What would make them switch from that to yours?"
5. "What's the minimum version of that switch-worthy experience?"

**When to suggest:** User says "help me think through...", "I'm not sure about...", or seems to need to find their own answer.

---

## Direct Mode

**Best for:** Users who have context and want structured analysis. Experienced builders who need a sounding board, not a teacher. Time-constrained decisions.

**How it works:**
- Claude provides analysis and observations directly
- States trade-offs clearly with reasoning
- Offers perspective while acknowledging it's the user's decision
- More efficient — less back-and-forth

**Example flow:**
1. User presents the decision
2. Claude restates the core trade-off
3. Claude identifies 2-3 key considerations the user may not have weighted
4. Claude states what the decision likely hinges on
5. User decides, Claude pressure-tests the decision

**When to suggest:** User says "what do you think about...", "compare these options", or presents a well-defined problem.

---

## Framework-Guided Mode

**Best for:** Complex decisions that benefit from structured analysis. Users who want a systematic process. When multiple stakeholders need to align.

**How it works:**
- Claude selects the appropriate cognitive framework
- Walks through the framework step by step
- Each step involves a question or exercise
- Results build toward a structured conclusion

**Example flow:**
1. Claude identifies the right framework (e.g., Pre-Mortem)
2. "Let's do a pre-mortem. Imagine it's 6 months from now and this decision failed..."
3. Walk through each step of the framework
4. Synthesize findings at the end
5. Conclude with clear decision or next steps

**When to suggest:** User says "run me through...", "let's analyze this properly", or the problem clearly maps to a specific framework.

---

## Adversarial Mode (autonomous)

**Best for:** A concrete decision with discrete options where you need to *see* the genuine tension between competing resources (time, cost, scope, UX, tech-debt, risk, scale, simplicity) — not a balanced summary that smooths the conflict away. Decisions you keep going in circles on because every option sacrifices something real.

**How it works:**
- Fundamentally different from the other three: **no user input during the analysis.**
- The thinking-partner convenes 3-5 single-minded **resource advocates** and runs a 3-round debate (opening → rebuttal → final) autonomously, dispatching each advocate as its own forked agent.
- Each advocate pushes hard for ONE resource and attacks its natural enemies — the clash surfaces tradeoffs a single balanced view hides.
- You confirm the decision, options, and advocate selection up front, then watch; the output is a **tension map + decision matrix + non-negotiables**, not a back-and-forth.

**Example flow:**
1. You: "Stress test this: rebuild the billing service now, or patch and defer?"
2. Claude proposes advocates (time, scope, tech-debt, risk), you confirm.
3. Advocates debate 3 rounds with no further input from you.
4. Claude synthesizes the tension map, weighted decision matrix, consensus points, each advocate's non-negotiable, and open questions.
5. You decide what to sacrifice — the synthesis makes the tradeoff unavoidable.

**When to suggest:** User says "debate this", "stress test this decision", "adversarial analysis", "argue for and against", "resource tradeoff", or "what would [resource] say?" — or has a concrete options-on-the-table decision and wants tension surfaced, not facilitated. Full orchestration lives in `adversarial-mode.md`.

---

## Switching Styles

Styles can be switched mid-discussion. If Socratic mode is moving too slowly, suggest switching to Direct. If Direct mode is missing nuance, suggest switching to Framework-Guided.

Ask: "We've been going Socratic — want me to switch to a more direct analysis, or should we apply a specific framework?"
