# Decision Matrix Framework

## When to Use
- Binary choices: "Should we use SSR or CSR?"
- Multi-option decisions with evaluable criteria
- When the team can't agree and needs structured comparison
- Technology selection, vendor evaluation, architecture choices

## Conversational Application

### Step 1: Define the Decision
Ask: "What exactly are we deciding? Let's phrase it as a single question."

Ensure the decision is:
- Specific (not "what framework?" but "what framework for our auth layer?")
- Timely (needs to be made now, not theoretical)
- Consequential (worth the analysis time)

### Step 2: Surface Criteria
Ask: "What matters most in this decision?"

Probe for hidden criteria:
- "What would make you regret this choice in 6 months?"
- "What constraints are non-negotiable vs nice-to-have?"
- "Who else is affected, and what do they care about?"

Common criteria to suggest if missing:
- Time to implement
- Maintenance burden
- Team familiarity
- Migration cost if wrong
- Scalability ceiling
- Ecosystem/community

### Step 3: Weight the Criteria
Ask: "If you had to rank these, which 2-3 matter most?"

Use forced ranking, not equal weighting. Equal weights mean you haven't thought hard enough.

### Step 4: Score Options
For each option against each criterion:
- Don't use numbers — use relative language: "strong", "moderate", "weak"
- Ask the human to justify each score
- Challenge suspiciously uniform scoring

### Step 5: Analyze the Pattern
Look for:
- **Clear winner** — One option dominates across weighted criteria
- **Trade-off pair** — Options split on different top criteria (real decision is which criteria matters more)
- **No winner** — Options are too similar (decision doesn't matter much, pick fastest to reverse)

### Step 6: Reality Check
Ask: "If the matrix says X, but your gut says Y — what does your gut know that the matrix doesn't?"

## Output Format
Present as a conversational summary, not a table. The discussion IS the value, not the artifact.

## Common Pitfalls
- Adding too many criteria (keep to 4-6)
- Equal weighting everything (forces hard choices)
- Anchoring on first option discussed
- Ignoring reversibility (easier-to-reverse decisions need less analysis)
