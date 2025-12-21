---
description: "Use when defining how to measure product success with KPIs and instrumentation (final sequential step)"
---

# Success Metrics

## Agent Persona

**Load:** `.claude/agents/discovery-agent.md`

Adopt: Outcome-focused, measurable definitions, connects metrics to user value.

## Purpose
Define how we'll measure product success: KPIs, leading indicators, business goals, and instrumentation requirements.

**RUNS LAST** - This is the final step in the sequential ProdKit workflow.

## When to Trigger
User says:
- "How do we measure success?"
- "What KPIs matter?"
- "Define our metrics"
- "How will we know this is working?"

## Prerequisites
- Strategy defined (business goals)
- Assumptions/risks identified (what to monitor)
- User stories written (what to instrument)

## Inputs
- Strategy (`.prodkit/strategy/business-canvas.md`)
- Assumptions/risks (`.prodkit/discovery/assumptions-and-risks.md`)
- User stories (`.prodkit/requirements/user-stories.md`)

## Process

### 1. Define Business Goals (from Strategy)

**Revenue Targets**:
- MRR/ARR goals
- Timeline to profitability
- Pricing model validation

**User Growth Targets**:
- Total users
- Active users
- User segments

**Market Share Targets**:
- Position in category
- Brand recognition

### 2. Define Product KPIs (AARRR Framework)

**Acquisition**: How do users discover and sign up?
- Traffic sources
- Conversion rate (visitor → signup)
- Cost per acquisition (CAC)
- Signup rate

**Activation**: What's the "aha moment"?
- Time to first value
- % of users who reach activation milestone
- Setup completion rate
- Onboarding drop-off points

**Engagement**: How often do they use it?
- Daily/Weekly/Monthly active users (DAU/WAU/MAU)
- Session frequency
- Session duration
- Feature adoption rate
- Power user threshold

**Retention**: Do they come back?
- Day 1, Day 7, Day 30 retention
- Cohort analysis
- Churn rate
- Reasons for churn

**Revenue**: Do they pay? How much?
- Free → Paid conversion rate
- Average revenue per user (ARPU)
- Lifetime value (LTV)
- LTV:CAC ratio
- Expansion revenue

**Referral**: Do they tell others?
- Net Promoter Score (NPS)
- Viral coefficient (K-factor)
- Referral rate
- Word-of-mouth tracking

### 3. For Each KPI, Define

**Metric Name**: Clear, unambiguous name

**Current Baseline**: If product exists
- Current value
- Historical trend

**Target Value**: What success looks like
- Specific number
- Rationale (why this target?)

**Timeline**: When to hit target
- Milestone dates
- Checkpoint metrics

**How to Measure**: Instrumentation requirements
- Events to track
- Data to capture
- Analytics tools needed
- Dashboards required

### 4. Map Metrics to Assumptions/Risks

For high-risk assumptions, define:
- **Leading indicators**: Early signals
- **Lagging indicators**: Final validation
- **Thresholds**: When to pivot vs persevere

Example:
- Risk: "Users won't trust AI summaries"
- Leading indicator: Verification rate (% who click through to original)
- Lagging indicator: Retention after 7 days
- Threshold: If >50% verify everything, trust is broken

### 5. Instrumentation Plan

**Critical Events to Track**:
- User signups
- First value delivered
- Key feature usage
- Drop-off points
- Error states
- User feedback

**User Properties to Capture**:
- User role (from personas)
- Team size
- Industry
- Usage patterns

**Integration Requirements**:
- Analytics platform (Mixpanel, Amplitude, etc.)
- Session replay (FullStory, LogRocket)
- Error tracking (Sentry)
- User feedback (surveys, NPS)

### 6. Call Script

```bash
.prodkit/scripts/bash/define-metrics.sh \
  --goal "10k MRR in 6 months from launch" \
  --kpi "Daily Active Users (DAU)" \
  --current "0 (pre-launch)" \
  --target "1000 DAU" \
  --timeline "3 months post-launch" \
  --instrument "Track: app_opened, digest_viewed, item_expanded, item_marked_read. Segment by user role and team size. Dashboard: Daily active users trend with cohort breakdown."
```

Repeat for each KPI (aim for 5-8 core metrics, not 50).

## Outputs
- `.prodkit/metrics/success-definition.md`

## Constraints
- **DO NOT** create files manually
- **ALWAYS** use `define-metrics.sh` script
- **KPIs must be measurable** (avoid vanity metrics)
- **INCLUDE** instrumentation requirements
- **TIE** metrics back to assumptions/risks
- **FOCUS** on 5-8 core metrics (not everything)
- **DEFINE** thresholds for pivot decisions

## North Star Metric

Identify **one** North Star Metric that represents core value:
- Example: "Hours saved per user per week"
- Must align with value proposition
- Must be measurable
- Must be actionable

## Next Steps

After metrics defined:

**🎉 ProdKit Sequential Workflow Complete!**

You now have:
1. ✅ Strategy
2. ✅ Personas
3. ✅ Jobs-to-be-done
4. ✅ Market analysis
5. ✅ Brand guidelines
6. ✅ Interaction design
7. ✅ User stories
8. ✅ Assumptions and risks
9. ✅ Success metrics

**After completing this skill, suggest:**

```
✅ Success metrics complete.

📁 Created: .prodkit/metrics/success-definition.md

🎉 **ProdKit discovery complete!**

👉 **Next step:** `/constitution-builder --technical` - Define technical standards (stack, architecture, code rules)

This will complete your constitution before starting Spec Kit.

Would you like to build the technical constitution now?
```

**After constitution, the Spec Kit workflow begins:**
- `/specify` → `/plan` → `/tasks` → `/implement`

## Context
This is **Step 9 of 9** (FINAL) in the ProdKit sequential workflow.
