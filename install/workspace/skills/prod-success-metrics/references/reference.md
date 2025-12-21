# Success Metrics Reference

Concise methodologies for defining and tracking product success.

---

## Table of Contents

- Metric Frameworks (HEART, AARRR, Product-Led Growth)
- North Star Metric
- OKRs (Objectives & Key Results)
- Leading vs Lagging Indicators
- Cohort Analysis
- Key Formulas
- Metric Selection by Stage

---

## Metric Frameworks

### HEART Framework (Google)

**Use when:** You need a balanced view of product health.

| Dimension | What It Measures | Example Metrics |
|-----------|------------------|-----------------|
| **Happiness** | User satisfaction | NPS, CSAT, sentiment analysis |
| **Engagement** | Depth of interaction | Sessions/user/week, features used |
| **Adoption** | New user uptake | New signups, feature adoption rate |
| **Retention** | Users coming back | Day 7/30 retention, churn rate |
| **Task Success** | Efficiency of core workflows | Completion rate, time to complete, error rate |

**How to use:**
1. Pick 1-2 metrics per dimension
2. Set targets based on benchmarks or goals
3. Track weekly or monthly
4. Don't try to optimize all at once - focus on bottleneck

---

### AARRR (Pirate Metrics)

**Use when:** You need to understand your funnel from acquisition to revenue.

```
Acquisition → Activation → Retention → Referral → Revenue
```

| Stage | Question | Example Metrics |
|-------|----------|-----------------|
| **Acquisition** | How do people find us? | Traffic, signups, CAC |
| **Activation** | Do they have a good first experience? | % completing onboarding, time to first value |
| **Retention** | Do they come back? | DAU/MAU, cohort retention curves |
| **Referral** | Do they tell others? | Viral coefficient, NPS, invites sent |
| **Revenue** | How do we make money? | MRR, ARPU, LTV:CAC |

**How to use:**
1. Map your funnel to these 5 stages
2. Measure conversion rate between each stage
3. Identify the leakiest bucket (biggest drop-off)
4. Focus improvements there first

**Example:**
- 10,000 visitors → 1,000 signups (10% conversion)
- 1,000 signups → 300 activated (30% activation)
- 300 activated → 150 retained at day 30 (50% retention) ← **Fix this first**

---

### Product-Led Growth (PLG) Metrics

**Use when:** Your product is self-serve (users can sign up and get value without sales).

**Core metrics:**
1. **Time to Value (TTV)**: How fast users reach "aha!" moment
   - Target: <5 minutes for consumer, <1 hour for B2B
2. **Product Qualified Leads (PQL)**: Users who've experienced core value
   - Example: Users who've completed 3+ core actions
3. **Free-to-Paid Conversion Rate**: % of free users who upgrade
   - Target: 2-5% for freemium, 15-25% for free trials
4. **Expansion Revenue**: Upsells from existing customers
   - Net dollar retention >100% means expansion exceeds churn

**PLG flywheel:**
```
Great product → Users get value → Users invite others → More users → Better product (network effects)
```

---

## North Star Metric

**Definition:** The ONE metric that best captures the core value you deliver.

**Criteria for a good North Star:**
1. **Captures value delivered** to customers (not just vanity)
2. **Leads to revenue** (predictive of business success)
3. **Actionable** by the team (you can influence it)
4. **Understandable** (everyone knows what it means)

**Examples:**

| Product Type | North Star | Why |
|--------------|------------|-----|
| Slack | Messages sent per user | More messages = more value, stickiness |
| Airbnb | Nights booked | Core value is stays, predicts revenue |
| Spotify | Time spent listening | Engagement drives retention and subscriptions |
| Dropbox | Files stored | More files = more lock-in, more upgrades |
| LinkedIn | Connections made | Network value grows with connections |

**Bad North Stars:**
- ❌ Total registered users (vanity - many never activate)
- ❌ Page views (doesn't indicate value delivered)
- ❌ App downloads (doesn't mean they use it)

**How to find yours:**
1. What action represents core value? (e.g., "booking a stay" for Airbnb)
2. Does doing more of this action = better outcomes for user AND business?
3. Can your team influence it with product changes?

---

## OKRs (Objectives & Key Results)

**Use when:** You need to align team around ambitious, measurable goals.

**Structure:**
- **Objective**: Aspirational, qualitative goal (inspires action)
- **Key Results**: 3-5 measurable outcomes that prove you achieved the objective

**Good OKR example:**

**Objective:** Achieve product-market fit for MVP

**Key Results:**
- KR1: 40% of users return weekly (retention)
- KR2: NPS score ≥50 (satisfaction)
- KR3: 15% of users refer at least 1 friend (organic growth)

**Bad OKR example:**

**Objective:** Build great features

**Key Results:**
- KR1: Ship 10 features (output, not outcome)
- KR2: Have 5 sprint planning meetings (activity, not result)

**OKR anti-patterns:**
- ❌ Too many OKRs (focus on 1-3 max per quarter)
- ❌ 100% achievable (should be 60-70% confident)
- ❌ Output-focused KRs (features shipped) instead of outcome (user value)
- ❌ Individual OKRs instead of team OKRs (kills collaboration)

---

## Leading vs Lagging Indicators

**Lagging indicators:** Measure past results (outcomes)
- Examples: Revenue, market share, churn rate
- **Problem:** By the time you see it, it's too late to change course

**Leading indicators:** Predict future results (inputs)
- Examples: Feature adoption, engagement depth, NPS
- **Benefit:** Actionable, you can course-correct early

**How to use both:**
1. Set lagging indicators as your targets (what success looks like)
2. Track leading indicators to predict if you'll hit targets
3. Take action based on leading indicators

**Example:**

| Lagging Indicator | Leading Indicator | Action |
|-------------------|-------------------|--------|
| Monthly churn rate | Day 7 retention | If D7 retention drops, onboarding is broken → fix it |
| Revenue growth | # of PQLs (product-qualified leads) | If PQLs are flat, activation is failing → improve TTV |
| Market share | Feature adoption rate | If new features aren't adopted, prioritization is off |

---

## Cohort Analysis

**What it is:** Tracking groups of users who started at the same time.

**Why it matters:** Hides whether retention is improving or getting worse.

**Example:**

Without cohorts:
- "Overall 30-day retention is 40%" ← Is this good or bad? Improving or declining?

With cohorts:
- Jan cohort: 30% retained
- Feb cohort: 35% retained
- Mar cohort: 42% retained ← **Retention is improving!**

**How to do it:**
1. Group users by signup month (or week)
2. Track what % return in days/weeks 1, 2, 3, 4, etc.
3. Plot retention curves for each cohort
4. Look for trends: Are newer cohorts better or worse?

**Retention curve shapes:**

```
Flat retention = great (users stick around)
  100% |████████████████████
       |
       └─────────────────────> Time

Decaying retention = normal (some drop-off)
  100% |█████
       |      ███
       |         ██
       └──────────────────────> Time

Cliff drop = bad (users churning fast)
  100% |███
    0% |
       └──────────────────────> Time
```

**Target:** Retention curve should flatten (stabilize) after week 4-8.

---

## Key Formulas

### Retention
```
Day X Retention = (Users active on Day X) / (Users who signed up)
```

### Churn Rate
```
Monthly Churn Rate = (Users who left this month) / (Users at start of month)
```

### DAU/MAU Ratio (Stickiness)
```
DAU/MAU = (Daily Active Users) / (Monthly Active Users)
```
- Good: >20% (users come back 6+ days/month)
- Great: >50% (daily habit)

### Viral Coefficient
```
Viral Coefficient = (Invites per user) × (Conversion rate of invites)
```
- >1 = exponential growth (each user brings >1 new user)
- <1 = you still need paid acquisition

### Customer Lifetime Value (LTV)
```
LTV = (ARPU) × (Average Lifetime in months)
```
Or simplified:
```
LTV = (ARPU) / (Monthly Churn Rate)
```

### LTV:CAC Ratio
```
LTV:CAC = (Customer Lifetime Value) / (Customer Acquisition Cost)
```
- <1 = losing money on each customer
- 1-3 = break-even to marginal
- >3 = healthy (ideal)
- >5 = underspending on growth (could acquire more)

### Payback Period
```
Months to Recover CAC = (CAC) / (ARPU)
```
- Target: <12 months
- Great: <6 months

### Net Dollar Retention (NDR)
```
NDR = (Starting MRR + Expansion - Churn - Contraction) / (Starting MRR)
```
- >100% = expansion exceeds churn (very healthy)
- >120% = best-in-class SaaS

---

## Metric Selection by Stage

### POC Stage
**Goal:** Validate problem and solution

**Track:**
- **Problem validation:** % of interviews confirming pain point
- **Solution validation:** % of beta users completing core workflow
- **Willingness to pay:** % who say they'd pay $X

**Don't track yet:**
- Revenue (too early)
- Scalability metrics (premature)

### MVP Stage
**Goal:** Find product-market fit

**Track:**
- **North Star metric:** Core value delivery
- **Retention:** Day 7, Day 30 retention
- **Engagement:** DAU/MAU, sessions/user/week
- **NPS:** User satisfaction
- **Activation rate:** % reaching "aha!" moment

**Don't over-optimize:**
- Growth (focus on retention first)
- Revenue (can charge later once PMF is clear)

### Established Stage
**Goal:** Sustainable, profitable growth

**Track everything:**
- **Growth:** MRR growth rate, user growth rate
- **Unit economics:** LTV, CAC, LTV:CAC, payback period
- **Retention:** Cohort retention curves, churn rate
- **Engagement:** DAU/MAU, feature adoption
- **Revenue:** MRR, ARPU, expansion revenue
- **Market position:** Market share, competitive win rate

---

## Benchmarks (Rough Targets)

**Retention:**
- Consumer apps: 20-40% Day 30 retention
- B2B SaaS: 80-90% annual retention (10-20% churn)

**Engagement:**
- DAU/MAU >20% = good stickiness
- NPS >50 = strong product-market fit

**Unit Economics (SaaS):**
- LTV:CAC >3:1
- CAC payback <12 months
- Net Dollar Retention >100%
- Gross margin >70%

**Growth:**
- Early-stage SaaS: 10-20% MoM (triple-triple-double-double-double)
- Later-stage SaaS: 20-40% YoY

**Activation:**
- Free trial → paid: 15-25%
- Freemium → paid: 2-5%

**Take benchmarks with a grain of salt** - vary widely by industry, product, market.

---

## Common Mistakes

### 1. Vanity Metrics
❌ Total registered users (many never activate)
✅ Active users (actually using the product)

### 2. Too Many Metrics
❌ Tracking 50+ metrics (analysis paralysis)
✅ 5-7 core metrics, reviewed weekly

### 3. Ignoring Cohorts
❌ "Overall retention is 40%" (hides trends)
✅ Plot retention curves by cohort

### 4. Confusing Correlation and Causation
❌ "Users who use feature X have higher retention" → build more of X
✅ Maybe power users just use everything (survivor bias)

### 5. Optimizing Lagging Indicators Directly
❌ "We need to increase revenue!" (how?)
✅ "We need to improve activation, which drives retention, which drives revenue"

### 6. Setting Unrealistic Targets
❌ "Let's 10x revenue this quarter!"
✅ "Let's improve activation from 20% to 30% (based on A/B test results)"

---

## Resources

- *Lean Analytics* by Alistair Croll & Benjamin Yoskovitz
- *Measure What Matters* by John Doerr (OKRs)
- *Amplitude's Product Metrics Guide*
- *Mixpanel's Product Benchmarks*
- *OpenView's SaaS Benchmarks*
