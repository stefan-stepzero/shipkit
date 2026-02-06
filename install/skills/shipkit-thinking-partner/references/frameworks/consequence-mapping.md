# Consequence Mapping Framework

## When to Use
- Understanding ripple effects of a decision
- When a change touches multiple systems or stakeholders
- Migration planning and dependency analysis
- When the user asks "what else does this affect?"
- Strategic decisions with organizational impact

## Conversational Application

### Step 1: Define the Change
Ask: "What's the specific decision or change we're mapping consequences for?"

Pin it down to something concrete:
- Not "we're changing the auth system" but "we're migrating from session cookies to JWT tokens"
- Not "we're adding payments" but "we're integrating Stripe for subscription billing"

### Step 2: Map First-Order Effects
Ask: "What are the immediate, direct consequences?"

These are obvious and usually well-understood:
- What code changes?
- What data structures change?
- What user flows change?
- What tests break?

### Step 3: Map Second-Order Effects
Ask: "For each first-order effect, what does THAT cause?"

This is where blind spots live:
- If auth changes → what about existing sessions? API consumers? Mobile app?
- If data structure changes → what about existing records? Analytics? Exports?
- If user flow changes → what about documentation? Support scripts? Onboarding?

### Step 4: Map Third-Order Effects
Ask: "What are the effects of the effects of the effects?"

Usually the limit of useful analysis:
- Team skill gaps → hiring/training needs → timeline impact
- Performance change → user behavior change → business metric change
- API change → partner integration breakage → relationship impact

### Step 5: Identify Stakeholders
For each consequence, ask: "Who needs to know about this?"

Map stakeholders who are:
- **Directly affected** — Must be involved in the decision
- **Indirectly affected** — Should be informed before changes
- **Potentially affected** — Should be notified after changes
- **Unaware but affected** — These are the dangerous ones

### Step 6: Timeline the Consequences
Ask: "When does each consequence manifest?"

- **Immediate** — During implementation
- **Short-term** — First week/month after change
- **Medium-term** — First quarter
- **Long-term** — Ongoing maintenance burden

### Step 7: Identify Intervention Points
Ask: "Where can we interrupt or redirect negative consequences?"

For each negative consequence:
- Can we prevent it at the source?
- Can we add a buffer or adapter layer?
- Can we phase the rollout to limit blast radius?
- Can we create a rollback plan?

## Output Format
Present consequences as expanding circles from the decision point, not as a flat list. The spatial metaphor helps humans grasp the ripple structure.

## Common Pitfalls
- Stopping at first-order effects (most people do)
- Mapping every possible consequence (focus on likely and high-impact)
- Ignoring organizational/people consequences (not just technical)
- Analysis paralysis (map enough to decide, not everything possible)
