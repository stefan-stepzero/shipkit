---
name: prod-trade-off-analysis
description: "Use anytime to evaluate features against constraints and recommend what to build, defer, or cut"
---

# Trade-Off Analysis

## Agent Persona

**Load:** `.claude/agents/discovery-agent.md`

Adopt: Pragmatic, ROI-focused, balances user value vs effort, decisive recommendations.

## Purpose
Evaluate features against Time/Quality/Scope constraints and opportunity cost. Recommend what to build, defer, or cut.

**Can run ANYTIME**:
- Before Spec Kit (rough estimates)
- After Spec Kit (with real effort data from `tasks.md`)
- During development (scope adjustments)

## When to Trigger
User says:
- "Should we build [feature]?"
- "Is this worth it?"
- "Prioritize features"
- "What should we cut?"
- "We're running out of time, what can we defer?"

## Inputs
- User stories (`.prodkit/requirements/user-stories.md`)
- Strategy (`.prodkit/strategy/business-canvas.md`)
- Personas (`.prodkit/discovery/personas.md`)
- **Optional**: Spec Kit tasks.md (effort estimates, if available from `.devkit/specs/*/tasks.md`)

## Process

### 1. List Features to Evaluate

From user stories or from user's specific request.

For each feature/story:
- Feature name
- Brief description
- Current priority (Must/Should/Could/Won't)

### 2. Assess Value (0-10 scale)

**Strategic Alignment** (0-10):
- Does this serve our winning aspiration?
- Does it reinforce how we win?
- Does it support our positioning?

**User Impact** (0-10):
- How many personas benefit?
- How much does it improve their lives?
- Is it a must-have or nice-to-have?
- Does it solve a high-pain problem?

**Competitive Necessity** (0-10):
- Do competitors have this?
- Is it table stakes?
- Or is it differentiating?
- Can we launch without it?

**Calculate Value Score**:
```
Value Score = (Strategic Alignment + User Impact + Competitive Necessity) / 3
```

### 3. Assess Cost

**Implementation Effort** (estimate % of total project time):
- If Spec Kit tasks.md exists, use those estimates
- Otherwise, rough estimate:
  - Small: 5-10%
  - Medium: 10-25%
  - Large: 25-50%
  - Huge: 50%+

**Opportunity Cost**:
- What else could we build with this time?
- How many other features could this fund?

**Maintenance Burden**:
- Ongoing costs
- Technical complexity
- Support burden

**Calculate Cost Score**:
```
Cost Score = Implementation Effort (as decimal)
```

### 4. Calculate ROI

```
ROI = Value Score / Cost Score
```

Higher ROI = better investment.

### 5. Categorize

Based on ROI:

**BUILD** (ROI > 2.0):
- High value, reasonable cost
- Clear winners
- Prioritize these

**DEFER to V2** (ROI 1.0-2.0):
- Good value but expensive
- Or moderate value, moderate cost
- Save for later

**CUT** (ROI < 1.0):
- Low value relative to cost
- Not worth the effort
- Remove from scope

### 6. Special Considerations

**Dependencies**:
- Some features enable others
- Infrastructure features may have low direct ROI but high enabling value

**Risk Mitigation**:
- Features that de-risk assumptions
- Learning features
- May justify lower ROI

**MVP Philosophy**:
- What's the minimum to deliver core value?
- Can we ship without this?

### 7. Call Script for Each Feature

```bash
.prodkit/scripts/bash/calculate-tradeoffs.sh \
  --feature "Real-time collaboration" \
  --strategic-value "3" \
  --user-impact "6" \
  --competitive "7" \
  --effort "65" \
  --opportunity-cost "Could build: digest view, keyboard shortcuts, AND mobile app" \
  --maintenance "High - WebSocket infrastructure, scaling complexity"
```

Repeat for each feature being evaluated.

## Outputs
- `.prodkit/analysis/feature-tradeoffs.md`
- `.prodkit/analysis/recommended-scope.md`

## Constraints
- **DO NOT** create files manually
- **ALWAYS** use `calculate-tradeoffs.sh` script
- **BREAK DOWN** to feature-level (not epic-level)
- **JUSTIFY** every BUILD decision
- **BE HONEST** about opportunity costs
- **USE** Spec Kit data when available

## Recommended Scope Output

The script generates a recommended scope document:

**BUILD NOW** (MVP):
- List of high-ROI features
- Total effort estimate
- Justification

**DEFER TO V2**:
- Good ideas, wrong time
- Revisit after launch

**CUT**:
- Not worth it
- Explicitly out of scope

## When to Run

**Before Spec Kit**:
- Validate user stories scope
- Rough estimates only
- Strategic prioritization

**After Spec Kit**:
- Use real effort estimates from tasks.md
- More accurate ROI calculations
- Final scope decisions

**During Development**:
- Scope adjustments
- Time running out
- What to cut?

## Integration with Spec Kit

If Spec Kit `tasks.md` exists for a feature:
1. Read `.devkit/specs/[feature]/tasks.md`
2. Sum effort estimates
3. Use as Cost Score input
4. More accurate trade-off analysis

## Context
This is an **ASYNC** skill - can be called anytime, not part of sequential workflow.
