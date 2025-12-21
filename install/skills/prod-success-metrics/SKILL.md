# Success Metrics

**Define how to measure product success with KPIs and instrumentation.**

---

## What This Skill Does

This skill helps you:
1. **Identify the North Star metric** that represents core value
2. **Define stage-appropriate KPIs** (POC/MVP/Established)
3. **Set targets and baselines** for each metric
4. **Plan instrumentation** for tracking and measurement
5. **Create OKRs** that align team around measurable outcomes

**Output:** A comprehensive metrics plan with clear targets and tracking requirements.

---

## When to Use This

**Use this skill when:**
- Launching a new product or major feature
- Need to define what success looks like
- Setting up analytics and instrumentation
- Creating quarterly OKRs
- Evaluating product-market fit

**Prerequisites:**
- **prod-user-stories**: You need requirements to know what to instrument

---

## How to Use This Skill

### Step 1: Initialize

```bash
/prod-success-metrics
```

**What happens:**
- Creates `success-metrics.md` from template
- Checks prerequisite (user-stories.md must exist)
- Opens document for editing

### Step 2: Define North Star Metric

**The ONE metric that best captures core value delivered.**

**Criteria:**
- Captures value to customers (not vanity)
- Predicts business success
- Actionable by the team
- Easy to understand

**Examples:**
- Slack: Messages sent per user
- Airbnb: Nights booked
- Spotify: Time spent listening
- Dropbox: Files stored

### Step 3: Choose Stage-Appropriate Metrics

**POC Stage** - Focus on validation:
- Problem confirmation rate
- Solution validation (% completing core workflow)
- Willingness to pay

**MVP Stage** - Focus on product-market fit:
- North Star metric
- Retention (Day 7, Day 30)
- Engagement (DAU/MAU)
- NPS
- Activation rate

**Established Stage** - Focus on growth:
- All MVP metrics PLUS
- Revenue (MRR, ARPU, LTV)
- Unit economics (LTV:CAC, payback)
- Market share
- Net dollar retention

### Step 4: Set Targets

**For each metric, define:**
- **Current baseline** (if product exists)
- **Target value** (what success looks like)
- **Timeframe** (when to hit target)
- **Rationale** (why this target matters)

**Good target example:**
- Metric: Day 30 retention
- Current: 35%
- Target: 50%
- Timeframe: End of Q2
- Rationale: 50% is industry benchmark for PMF

**Bad target example:**
- Metric: Total users
- Target: "A lot more"
- Timeframe: "Soon"

### Step 5: Plan Instrumentation

**What to track:**
- User signups (source, timestamp)
- Activation event (first core action)
- Feature usage (key features individually)
- Sessions (start, end, duration)
- Conversion events (free → paid)
- Churn events (cancellation, reason)

**User properties:**
- User ID, email, signup date
- Segment/persona
- Plan tier
- Company size (if B2B)

**Tools:**
- Analytics: Mixpanel, Amplitude, GA4
- Error tracking: Sentry, Rollbar
- User feedback: Intercom, Zendesk
- A/B testing: Optimizely, LaunchDarkly

### Step 6: Create OKRs (Optional but Recommended)

**Structure:**
- **Objective**: Aspirational, qualitative goal
- **Key Results**: 3-5 measurable outcomes

**Good OKR example:**

**Objective:** Achieve product-market fit for MVP

**Key Results:**
- KR1: 40% of users return weekly (retention)
- KR2: NPS score ≥50 (satisfaction)
- KR3: 15% of users refer ≥1 friend (growth)

---

## Metric Frameworks

### HEART Framework (Google)

| Dimension | Metrics |
|-----------|---------|
| **Happiness** | NPS, CSAT, sentiment |
| **Engagement** | Sessions/user/week, features used |
| **Adoption** | New signups, feature adoption rate |
| **Retention** | Day 7/30 retention, churn |
| **Task Success** | Completion rate, time to complete |

### AARRR (Pirate Metrics)

```
Acquisition → Activation → Retention → Referral → Revenue
```

| Stage | Key Metrics |
|-------|-------------|
| Acquisition | Traffic, signups, CAC |
| Activation | Time to value, onboarding completion |
| Retention | DAU/MAU, cohort retention |
| Referral | NPS, viral coefficient |
| Revenue | MRR, ARPU, LTV:CAC |

---

## Reference Materials

**Available in `references/`:**

1. **reference.md**: Metric frameworks and methodologies
   - HEART, AARRR, Product-Led Growth
   - North Star metric selection
   - OKRs
   - Leading vs lagging indicators
   - Cohort analysis
   - Key formulas (LTV, CAC, retention, etc.)

2. **examples.md**: Practical KPI examples
   - B2B SaaS (collaboration tool)
   - B2C mobile (fitness app)
   - E-commerce (furniture store)
   - Developer tools (API monitoring)
   - Marketplace (freelance platform)

**Add your own references:**
- Industry benchmarks
- Past dashboards/reports
- Analytics playbooks
- OKR templates

---

## Key Formulas

### Retention
```
Day X Retention = (Users active on Day X) / (Users who signed up)
```

### Stickiness (DAU/MAU)
```
DAU/MAU = Daily Active Users / Monthly Active Users
```
- >20% = good (daily habit forming)

### LTV (Customer Lifetime Value)
```
LTV = ARPU / Monthly Churn Rate
```

### LTV:CAC Ratio
```
LTV:CAC = Lifetime Value / Customer Acquisition Cost
```
- <1 = losing money
- >3 = healthy

### Viral Coefficient
```
Viral Coefficient = (Invites per user) × (Invite conversion rate)
```
- >1 = exponential growth

---

## Leading vs Lagging Indicators

**Lagging indicators** - Measure past results (outcomes):
- Revenue, market share, churn
- **Problem:** Too late to change course

**Leading indicators** - Predict future results (inputs):
- Feature adoption, engagement depth, NPS
- **Benefit:** Actionable early

**Example:**
- Lagging: Monthly churn rate
- Leading: Day 7 retention
- **Action:** If D7 retention drops → fix onboarding

---

## Cohort Analysis

**What:** Track groups of users who started at the same time.

**Why:** Shows if retention is improving or declining.

**Example:**
- Jan cohort: 30% retained at Day 30
- Feb cohort: 35%
- Mar cohort: 42% ← **Improving!**

**Target:** Retention curve flattens after week 4-8 (stabilizes).

---

## Anti-Patterns to Avoid

❌ **Vanity metrics**: Total users (many never activate)
✅ **Real metrics**: Active users

❌ **Too many metrics**: Tracking 50+ metrics
✅ **Focus**: 5-8 core metrics

❌ **No cohorts**: "Overall retention is 40%" (hides trends)
✅ **Cohorts**: Plot curves by signup month

❌ **Unrealistic targets**: "10x revenue this quarter"
✅ **Data-driven**: "Improve activation 20% to 30%"

❌ **Ignoring instrumentation**: "We'll figure it out later"
✅ **Plan upfront**: Define events, properties, tools

---

## Success Criteria

**You've done this well when:**

✅ **North Star metric is clear:**
- Captures core value
- Predictive of success
- Actionable

✅ **Metrics match your stage:**
- POC focuses on validation
- MVP focuses on PMF
- Established focuses on growth

✅ **Targets are specific:**
- Numeric targets
- Clear timeframes
- Rationale provided

✅ **Instrumentation is planned:**
- Events to track defined
- Tools selected
- Dashboards mapped out

✅ **Leading indicators identified:**
- Early signals defined
- Thresholds for action set

---

## Integration with Other Skills

**Before this skill:**
- `/prod-user-stories` → Know what you're building
- `/prod-assumptions-and-risks` → Know what to monitor

**After this skill:**
- `/dev-specify` → Build the instrumentation
- Regular reviews → Track progress against targets

**Throughout development:**
- Update baselines as you learn
- Adjust targets based on actual data
- Add new metrics as product evolves

---

## Tips for Success

1. **Start with North Star**: The ONE metric that matters most
2. **Match your stage**: Don't track revenue metrics in POC
3. **Use benchmarks**: Research industry standards for context
4. **Plan instrumentation early**: Harder to add tracking later
5. **Review regularly**: Weekly for primary metrics, monthly for secondary
6. **Cohort analysis**: Always track retention by cohort, not just overall
7. **Leading indicators**: Focus on what you can influence

---

## Common Metric Benchmarks

**Retention (B2C):**
- 20-40% Day 30 retention

**Retention (B2B SaaS):**
- 80-90% annual retention

**Engagement:**
- DAU/MAU >20% = good stickiness
- NPS >50 = strong PMF

**Unit Economics (SaaS):**
- LTV:CAC >3:1
- CAC payback <12 months
- Net dollar retention >100%

**Growth:**
- Early SaaS: 10-20% MoM
- Later SaaS: 20-40% YoY

**Activation:**
- Free trial → paid: 15-25%
- Freemium → paid: 2-5%

---

## Quick Start Checklist

- [ ] Run `/prod-success-metrics` to initialize
- [ ] Define North Star metric (captures core value)
- [ ] Choose 5-8 metrics appropriate for your stage
- [ ] Set specific targets with timeframes
- [ ] Plan instrumentation (events, properties, tools)
- [ ] Identify leading indicators (early warning signals)
- [ ] Create OKRs for this quarter (optional)
- [ ] Set up dashboards for weekly/monthly review
- [ ] Define cohort analysis approach
- [ ] Document assumptions and review schedule

**Remember:** Metrics should drive decisions, not just measure. Focus on actionable metrics that help you improve the product.
