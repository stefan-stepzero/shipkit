# Pre-Mortem Framework

## When to Use
- Before committing to a major decision or architecture
- When confidence is high (that's when blind spots are largest)
- Risk assessment for launches, migrations, or major features
- When the user says "what could go wrong?"

## Conversational Application

### Step 1: Set the Scene
Say: "Imagine it's 6 months from now. This decision has failed spectacularly. What happened?"

The key shift: move from "what might go wrong" (optimistic framing) to "it already failed" (forces concrete thinking).

### Step 2: Generate Failure Modes
Ask: "Tell me 3 ways this could fail."

Then probe each category:
- **Technical failures** — "What breaks under load? What's the single point of failure?"
- **User failures** — "Where do users get confused, frustrated, or give up?"
- **Business failures** — "What if the market doesn't want this? What if a competitor ships first?"
- **Team failures** — "What if the key person leaves? What if scope creeps?"
- **Integration failures** — "What third-party dependency could break or change?"

### Step 3: Rate Each Failure
For each failure mode, assess:
- **Likelihood** — How probable is this? (Low / Medium / High)
- **Impact** — If it happens, how bad is it? (Annoying / Painful / Fatal)
- **Detectability** — Would we notice before it's too late? (Early / Late / After)

Focus on the **high-impact, low-detectability** failures — these are the killers.

### Step 4: Identify Mitigation
For each critical failure:
- "Can we prevent it?" (design change, constraint, process)
- "Can we detect it early?" (monitoring, canary, feature flag)
- "Can we recover from it?" (rollback plan, fallback, data backup)
- "Can we reduce blast radius?" (progressive rollout, isolation)

### Step 5: Decision Checkpoint
Ask: "Knowing all this, do we still proceed? What changes?"

Three outcomes:
- **Proceed with mitigations** — Address top 2-3 risks, accept the rest
- **Modify the approach** — The pre-mortem revealed a better path
- **Kill the idea** — Risks outweigh benefits (rare but valuable)

### Step 6: Create Risk Register
Summarize as:
- Top 3 risks with mitigations
- Monitoring triggers (what signals should we watch for?)
- Rollback criteria (when do we pull the plug?)

## Common Pitfalls
- Being too abstract ("users might not like it")
- Only considering technical failures (business and user failures kill more projects)
- Generating risks without mitigations (analysis without action)
- Using pre-mortem to justify inaction (every decision has risks)
