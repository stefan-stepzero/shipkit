---
description: "Use when extracting assumptions and identifying strategic risks (runs after all other discovery)"
---

# Assumptions and Risks

## Agent Persona

**Load:** `.claude/agents/discovery-agent.md`

Adopt: Skeptical, surfaces hidden assumptions, thinks about failure modes.

## Purpose
Extract and analyze assumptions from all prior artifacts. Identify strategic risks that could invalidate the product direction.

**RUNS LAST** - after all other discovery work (skills 1-7).

**Focus**: Strategic risks, not operational/technical risks.

## When to Trigger
User says:
- "What could go wrong?"
- "What are we assuming?"
- "Identify risks"
- "What needs to be true for this to work?"

Or automatically:
- When user completes user stories
- When ready to move to Spec Kit

## Prerequisites
**ALL** previous artifacts must exist:
- Strategy
- Personas
- JTBD
- Market analysis
- Brand guidelines
- Journeys
- User stories

## Inputs
- **ALL** `.prodkit/` artifacts from skills 1-7

## Process

### 1. Read ALL Artifacts

**IMPORTANT**: You MUST read every prior artifact:
```
.prodkit/strategy/business-canvas.md
.prodkit/discovery/personas.md
.prodkit/discovery/jobs-to-be-done-current.md
.prodkit/discovery/market-analysis.md
.prodkit/brand/personality.md
.prodkit/design/future-state-journeys.md
.prodkit/requirements/user-stories.md
```

### 2. Extract Assumptions from Each Artifact

**From Strategy**:
- Market size assumptions
- Competitive positioning assumptions
- Business model viability
- Revenue model assumptions

**From Personas**:
- User behavior assumptions
- Pain point intensity assumptions
- Decision-making assumptions

**From JTBD**:
- Willingness to switch assumptions
- Current solution inadequacy
- Frequency assumptions

**From Market Analysis**:
- Market timing assumptions
- Competitive response assumptions
- Barrier to entry assumptions

**From Journeys**:
- User capability assumptions (technical skill)
- Workflow integration assumptions
- Adoption assumptions

**From User Stories**:
- Technical feasibility assumptions
- Build time assumptions
- Complexity assumptions

### 3. Assess Each Assumption

For each assumption:

**Impact if Wrong**: High / Medium / Low
- What happens if this assumption is false?

**Confidence Level**: High / Medium / Low
- How certain are we this is true?

**How to Test**: What would validate or invalidate?
- Specific experiments
- Metrics to track
- User research methods

**Risk Level**: Calculate from impact × (1 - confidence)
- High impact + Low confidence = HIGH RISK
- Low impact + High confidence = LOW RISK

### 4. Identify Strategic Risks

**Market Risks**:
- Market too small
- Wrong timing (too early/late)
- Market moving away from solution

**User Risks**:
- Won't adopt
- Won't pay
- Won't switch from existing solution
- Won't achieve promised value

**Competitive Risks**:
- Incumbents respond aggressively
- New entrants with better solution
- Commoditization

**Execution Risks**:
- Can't deliver promised experience
- Too complex to build
- Can't acquire users cost-effectively

**Business Model Risks**:
- CAC too high
- LTV too low
- Churn too high
- Unit economics don't work

### 5. For Each Risk, Define Mitigation

- What can we do to reduce likelihood?
- What can we do to reduce impact?
- Early warning indicators?

### 6. Call Script

```bash
.prodkit/scripts/bash/identify-risks.sh \
  --assumption "Users will trust AI-generated summaries without verification" \
  --impact "High" \
  --confidence "Medium" \
  --test "Show 10 beta users AI summaries vs manual summaries, measure trust and verification behavior" \
  --risk "Users won't switch from existing tools (Slack, email)" \
  --likelihood "Medium" \
  --risk-impact "High" \
  --mitigation "Free trial, easy import, Slack integration, no commitment required, quick wins in first session"
```

Repeat for each assumption and risk.

## Outputs
- `.prodkit/discovery/assumptions-and-risks.md`

## Constraints
- **DO NOT** create files manually
- **ALWAYS** use `identify-risks.sh` script
- **MUST** read ALL previous artifacts before starting
- **FOCUS** on strategic risks, not bugs/edge cases/technical risks
- **EVERY** assumption needs a "how to test"
- **EVERY** risk needs mitigation strategy

## Next Steps
After risks identified:
- Define success metrics (final step)

## Context
This is **Step 8 of 9** in the ProdKit sequential workflow.
