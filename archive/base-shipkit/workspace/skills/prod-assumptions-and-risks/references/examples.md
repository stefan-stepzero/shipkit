# Assumptions & Risks Examples

Practical examples for different product types and stages.

---

## Example 1: B2B SaaS - Team Collaboration Tool (MVP Stage)

### Critical Assumptions

**Customer:**
- Remote teams will pay $10/user/month
  - **Validation:** Pricing survey of 50 target users
  - **If wrong:** Adjust to freemium or $5/user tier

**Product:**
- Users will check app daily (not just email)
  - **Validation:** Beta usage metrics (DAU/MAU ratio)
  - **If wrong:** Add email digests, Slack integration

**Market:**
- 100K potential companies in our ICP
  - **Validation:** Market research, competitor user counts
  - **If wrong:** Expand ICP or target SMBs differently

### Top 5 Risks

**1. Low Adoption (Likelihood: 3, Impact: 3, Score: 9)**
- **Risk:** Teams don't switch from Slack
- **Mitigation:**
  - [ ] Slack integration (use us inside Slack)
  - [ ] Import Slack history (reduce switching cost)
  - [ ] Free tier for small teams (trial barrier lower)
- **Owner:** Product lead
- **Deadline:** Before launch

**2. Churn After First Month (L: 2, I: 3, Score: 6)**
- **Risk:** Users don't form habit, churn quickly
- **Mitigation:**
  - [ ] Onboarding checklist (get to value in 5 min)
  - [ ] Weekly engagement emails
  - [ ] Monitor: DAU < 40% triggers intervention
- **Owner:** Growth lead

**3. Can't Hire Engineers Fast Enough (L: 2, I: 2, Score: 4)**
- **Risk:** Timeline slips, features delayed
- **Mitigation:**
  - [ ] Reduce MVP scope by 30%
  - [ ] Outsource non-core features
  - **Accept:** Some delay acceptable for MVP

---

## Example 2: B2C Mobile App - Fitness Tracker (POC Stage)

### Critical Assumptions (Test First!)

**Customer:**
- Users will work out at home (not gym)
  - **Validation:** Survey + landing page test
  - **If wrong:** Pivot to gym-based app

- Users will pay for fitness app (market saturated)
  - **Validation:** Pre-orders, waitlist conversion
  - **If wrong:** Ad-supported or B2B (corporate wellness)

**Product:**
- 10-minute workouts are "enough"
  - **Validation:** Beta testers complete workouts
  - **If wrong:** Add 20/30 min options

### Top Risks

**1. Can't Compete with Free Apps (L: 3, I: 3, Score: 9)**
- **Mitigation:**
  - [ ] Free tier (prove value before paywall)
  - [ ] Unique selling point: AI personal trainer
  - [ ] Target niche: busy parents (not general fitness)

**2. Low Retention (L: 3, I: 2, Score: 6)**
- **Mitigation:**
  - [ ] Streak mechanic (gamification)
  - [ ] Social accountability (workout with friend)
  - [ ] Monitor: <20% Day 7 retention = pivot

---

## Example 3: E-Commerce - Furniture Store (Established)

### Critical Assumptions

**Market:**
- 20% of furniture buyers will use AR before purchase
  - **Validation:** A/B test AR feature vs. control
  - **If wrong:** Deprioritize AR, focus on reviews/photos

**Business Model:**
- Return rate stays <5% (industry avg 10%)
  - **Validation:** Track return reasons for 3 months
  - **If wrong:** Adjust product descriptions, add measurements

### Top Risks

**1. Supply Chain Disruption (L: 2, I: 3, Score: 6)**
- **Risk:** Supplier delays, inventory shortages
- **Mitigation:**
  - [ ] Multi-source key items
  - [ ] Safety stock for bestsellers
  - [ ] Transparent lead times (don't over-promise)
- **Contingency:** Delay promotions if stock low

**2. Poor Product Photos Increase Returns (L: 2, I: 2, Score: 4)**
- **Mitigation:**
  - [ ] 360° photos, zoom, measurements
  - [ ] Customer photo uploads (social proof + reality check)
  - [ ] AR visualization (see in your space)

---

## Example 4: Developer Tool - API Monitoring (POC Stage)

### Assumptions to Test First

**Customer:**
- Developers will pay for monitoring (free tools exist)
  - **Test:** Freemium model, upsell on alerts/integrations
  - **Early indicator:** Conversion to paid within 30 days

**Product:**
- 5-minute setup is acceptable (competitors: 2 min)
  - **Test:** Beta user onboarding sessions
  - **Target:** <3 min to first alert

### Top Risks

**1. False Positive Alerts (L: 3, I: 3, Score: 9)**
- **Risk:** Alert fatigue, users ignore notifications
- **Mitigation:**
  - [ ] Smart thresholds (3 failures, not 1)
  - [ ] Maintenance mode (silence during deploys)
  - [ ] Alert customization per endpoint
- **Monitor:** If >20% alerts snoozed = too noisy

**2. Can't Differentiate from DataDog/NewRelic (L: 2, I: 3, Score: 6)**
- **Mitigation:**
  - [ ] Focus on simplicity (not enterprise features)
  - [ ] Pricing: 10x cheaper for solo devs/startups
  - [ ] Niche: API-only (not full observability)

---

## Example 5: Platform Risk - Dependency on Third-Party API

### Assumption

"Stripe API will remain stable and available"

### Risks

**API Changes Breaking Integration (L: 2, I: 3, Score: 6)**
- **Mitigation:**
  - [ ] Use versioned API (pin to v2023-10)
  - [ ] Monitor Stripe changelog weekly
  - [ ] Test in staging before production upgrade
  - [ ] Fallback: Manual payment processing (short-term)

**Stripe Downtime Blocks Checkout (L: 1, I: 3, Score: 3)**
- **Mitigation:**
  - [ ] Queue failed payments, retry automatically
  - [ ] Display status page during Stripe outages
  - **Accept:** Rare enough, not worth full redundancy

**Pricing Increase (L: 2, I: 2, Score: 4)**
- **Mitigation:**
  - [ ] Contract negotiation (lock rates)
  - [ ] Alternative processor (Adyen) evaluated yearly
  - **Accept:** Pass cost to customers if necessary

---

## Pre-Mortem Example

**Scenario:** "It's 6 months from now. Our MVP failed. Why?"

**Team Brainstorm Results:**

1. "No one wanted to pay for it" (market assumption wrong)
   → **Mitigation:** Validate pricing in month 1, not month 6

2. "We built features no one used" (product assumption wrong)
   → **Mitigation:** Ship partial MVP, measure usage before adding

3. "Engineering took 2x longer than estimated" (execution risk)
   → **Mitigation:** Cut scope by 40%, add buffer to timeline

4. "Key engineer quit, progress stalled" (team risk)
   → **Mitigation:** Document tribal knowledge, pair programming

5. "Competitor launched similar product first" (market risk)
   → **Mitigation:** Ship faster (cut nice-to-haves), differentiate

**Result:** 5 new risks identified, 3 added to high-priority list.

---

## Stage-Specific Examples

### POC: Focus on Hypothesis Validation

**Assumption:** "Busy parents want 10-min home workouts"

**Test:**
- Landing page: "10-Minute Workouts for Busy Parents"
- Collect emails (target: 100 in 2 weeks)
- If <50: assumption wrong, pivot

**Don't worry about:**
- Scalability (100 users max)
- Edge cases (happy path only)
- Advanced features (prove basics first)

### MVP: Focus on Must-Haves

**Assumption:** "Users will onboard themselves (no hand-holding)"

**Test:**
- Track completion rate of self-serve onboarding
- Target: >60% complete setup
- If <40%: Add chat support or simplify

**Address risks:**
- Security (SSL, encrypted data)
- Reliability (99% uptime)
- Quality (no critical bugs)

### Established: Focus on Sustainability

**Assumption:** "Current tech stack scales to 1M users"

**Test:**
- Load testing at 10x current usage
- Architecture review with senior engineers
- Plan migration if approaching limits

**Mitigate all material risks:**
- Disaster recovery plans
- Security audits
- Competitive moats
- Regulatory compliance

---

## Quick Wins: Assumptions You Can Test This Week

1. **Pricing:** Van Westendorp survey (4 questions, 50 responses)
2. **Problem:** User interviews (10 people, 30 min each)
3. **Interest:** Landing page + ads ($100 budget, measure clicks)
4. **UX:** Prototype test (Figma clickthrough, 5 users)
5. **Technical:** Spike to prove tech works (2-day build)

**Rule of thumb:** If you can't test an assumption in <2 weeks, break it down into smaller testable pieces.
