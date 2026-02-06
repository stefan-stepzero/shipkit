# First Principles Framework

## When to Use
- Challenging "we've always done it this way" assumptions
- Rethinking an approach from scratch
- When inherited constraints may no longer apply
- Foundational architecture or strategy decisions
- When the user feels stuck or constrained

## Conversational Application

### Step 1: Identify the Assumption Stack
Ask: "What do you believe to be true about this problem?"

List every assumption, including obvious ones:
- "Users need to sign in" — do they? Always?
- "We need a database" — do we? What if we didn't?
- "This needs to be real-time" — does it? What latency is actually acceptable?

### Step 2: Challenge Each Assumption
For each assumption, ask:
- "Is this a law of physics, or a choice?"
- "Who decided this, and when? Are conditions the same?"
- "What would change if this assumption were false?"

Categorize into:
- **Fundamental truths** — Cannot be changed (laws of physics, regulatory requirements)
- **Inherited constraints** — Were true once, may not be now
- **Conventions** — "How it's done" without questioning why
- **Fears** — Assumptions driven by risk aversion, not evidence

### Step 3: Remove Convention Layer
Ask: "If we were starting from zero today, with what we know now, would we make this same choice?"

Strip away:
- Historical decisions made with less information
- Industry conventions that may not apply to your context
- Optimizations for problems you don't have yet

### Step 4: Rebuild from Fundamentals
Ask: "Given only the fundamental truths, what's the simplest thing that could work?"

Build up from:
- What does the user actually need to accomplish?
- What's the minimum path between user intent and outcome?
- What must be true for this to work?

### Step 5: Compare Paths
Place the first-principles solution next to the current/conventional approach:
- Where do they differ?
- What does the conventional approach add that's actually unnecessary?
- What does the first-principles approach miss that's genuinely important?

### Step 6: Pragmatic Synthesis
Ask: "Given where we are today, what's the most practical path that stays true to first principles?"

Pure first-principles thinking is theoretical. The value is in finding where convention diverges from fundamentals, then making conscious choices about each divergence.

## Common Pitfalls
- Going too abstract ("what even IS a user?")
- Ignoring legitimate constraints disguised as conventions
- Assuming first-principles always means simpler (sometimes complexity is fundamental)
- Forgetting migration cost from current state
