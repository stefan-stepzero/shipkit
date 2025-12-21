# Strategic Thinking Reference

Extended guidance for developing product strategy.

## Table of Contents

- Strategy frameworks overview
- Product vs feature strategy
- Validating strategic assumptions
- Common strategy mistakes
- Strategy for different business models

## Strategy Frameworks Overview

### Playing to Win (AG Lafley & Roger Martin)

**Five Key Choices:**
1. **Winning Aspiration:** What does success look like?
2. **Where to Play:** Which customers, markets, channels?
3. **How to Win:** What's your competitive advantage?
4. **Core Capabilities:** What must you be great at?
5. **Management Systems:** How will you execute?

**Use when:** Established company, competitive market

### Lean Canvas (Ash Maurya)

**Nine Blocks:**
1. Problem (top 3)
2. Solution (top 3 features)
3. Unique Value Proposition
4. Unfair Advantage
5. Customer Segments
6. Key Metrics
7. Channels
8. Cost Structure
9. Revenue Streams

**Use when:** Startup, new product, testing business model

### Business Model Canvas (Osterwalder)

**Focus:** How you create, deliver, and capture value

**Use when:** Understanding/designing entire business model

**For Shipkit:** We use a simplified combination focusing on:
- Value proposition (core)
- Target customers (who)
- Success metrics (how we measure)
- Business model (how we make money)

## Product vs Feature Strategy

### When is this a "product strategy"?

✅ **New Product Strategy:**
- Greenfield product
- New business line
- Significant pivot
- New market entry

**Requires:** Full business canvas (all 4 sections)

### When is this a "feature strategy"?

✅ **Feature/Enhancement:**
- Adding to existing product
- Serving existing customer base
- Incremental improvement
- Tactical addition

**Requires:**
- Section 1 (how does this feature deliver value?)
- Section 2 (which existing personas does this serve?)
- Section 3 (how do we measure feature success?)
- Section 4 (skip or reference existing business model)

**Key Question:** Does this change who you serve or how you make money?
- **No:** It's a feature strategy (reference existing)
- **Yes:** It's a product strategy (complete all sections)

## Validating Strategic Assumptions

### Critical Assumptions to Test

**Value Proposition Assumptions:**
- [ ] People actually have this problem
- [ ] The problem is painful enough to pay for
- [ ] Our solution solves the problem better than alternatives
- [ ] Users will change behavior to adopt our solution

**Market Assumptions:**
- [ ] Target market is large enough
- [ ] We can reach these customers
- [ ] Customers have budget/authority to buy
- [ ] Market timing is right (not too early/late)

**Business Model Assumptions:**
- [ ] Customers will pay our price
- [ ] Unit economics work (LTV > CAC)
- [ ] We can acquire customers at assumed CAC
- [ ] Churn will be at acceptable levels

### How to Validate

**Cheapest to Most Expensive:**

1. **Customer Interviews** (Free)
   - Talk to 10-20 potential customers
   - Ask about problem, current solutions, willingness to pay
   - Validate: Problem exists, people care

2. **Landing Page Test** ($100-500)
   - Create simple landing page describing solution
   - Drive traffic (ads, social)
   - Measure: Email signups, pre-orders
   - Validate: Demand exists

3. **Prototype/Mockups** ($500-2,000)
   - Clickable prototype (Figma, InVision)
   - Show to potential users
   - Validate: Solution resonates, UI makes sense

4. **Concierge MVP** (Time investment)
   - Manually deliver the value
   - 5-10 customers
   - Validate: Users get value, willing to pay

5. **Minimum Viable Product** ($5K-50K+)
   - Build simplest version that delivers core value
   - Launch to early adopters
   - Validate: Product-market fit

## Common Strategy Mistakes

### 1. Solution Looking for Problem

**Symptom:**
- "I built this cool technology, who needs it?"
- Starting with solution before validating problem

**Fix:**
- Talk to customers first
- Validate problem is real and painful
- Then design solution

### 2. Boiling the Ocean

**Symptom:**
- "We'll serve everyone!"
- "All businesses 1-10,000 employees"
- Multiple customer segments at once

**Fix:**
- Pick ONE primary segment
- Go deep before going wide
- Master one segment, then expand

### 3. Feature != Product

**Symptom:**
- Building feature as standalone product
- "Uber for X"
- Missing the full value chain

**Fix:**
- Understand why existing player doesn't offer this
- Identify if this is vitamin (nice) or painkiller (critical)
- Consider if this should be feature of existing product

### 4. Ignoring Unit Economics

**Symptom:**
- "We'll make it up in volume"
- CAC > LTV
- Negative gross margins

**Fix:**
- Calculate unit economics early
- Ensure path to profitability exists
- Don't assume things get better at scale without evidence

### 5. No Differentiation

**Symptom:**
- "We'll execute better"
- "Ours has better UI"
- Competing on features not values

**Fix:**
- Identify unfair advantage
- Understand why customers would switch
- Build around unique insight/capability

## Strategy for Different Business Models

### B2C SaaS

**Focus:**
- Viral growth potential
- Self-serve onboarding
- Low CAC, high volume
- Engagement metrics

**Key Metrics:**
- DAU/MAU (stickiness)
- Viral coefficient
- Net Promoter Score
- Conversion rate (free → paid)

**Critical Assumptions:**
- Users will invite friends
- Problem is obvious enough for self-serve
- Can acquire users organically

### B2B SaaS

**Focus:**
- Sales process and CAC
- Retention and expansion
- Multi-stakeholder buying
- Enterprise compliance

**Key Metrics:**
- MRR/ARR growth
- Net Revenue Retention
- CAC Payback period
- Logo retention

**Critical Assumptions:**
- Can reach decision makers
- Budget exists for this category
- ROI is demonstrable
- Integration with existing stack is feasible

### Marketplace

**Focus:**
- Two-sided liquidity
- Supply-demand balance
- Network effects
- Platform take rate

**Key Metrics:**
- GMV (Gross Merchandise Value)
- Take rate
- Supply/demand ratio
- Repeat transaction rate

**Critical Assumptions:**
- Chicken-egg problem is solvable
- Both sides will adopt
- Can achieve liquidity in geography/category
- Take rate sustainable for both sides

### Side Project / Indie Hacker

**Focus:**
- Speed to revenue
- Minimal complexity
- Niche audience
- Profitability over growth

**Key Metrics:**
- MRR
- Time to first dollar
- Profitability
- Hours per week required

**Critical Assumptions:**
- Can build alone/small team
- Market doesn't require network effects
- Niche is big enough for sustainable income
- Can maintain while doing other work

## Using Strategy to Drive Decisions

### Feature Prioritization

**Does this feature align with strategy?**
- Does it serve our target customer?
- Does it strengthen our differentiation?
- Does it move our key metrics?

**Example:**
```
Feature Request: Advanced analytics dashboard
Strategy Check:
- Target Customer: Early-stage startups ❌ (They want simple)
- Differentiation: Ease of use ❌ (This adds complexity)
- Key Metric: Time to first value ❌ (This delays it)
Decision: Deprioritize or make optional
```

### Market Expansion

**When to expand to new segment?**
- [ ] Achieved strong product-market fit in primary segment
- [ ] Economics work (profitable cohorts)
- [ ] Team/infrastructure can support expansion
- [ ] New segment aligns with core value prop

**Don't expand when:**
- Still searching for PMF in primary segment
- Unit economics don't work yet
- Would require significant product changes
- Dilutes focus from primary customer

### Pivot Decisions

**When to pivot?**
- Consistent evidence strategy isn't working
- Better opportunity discovered
- Market changed fundamentally
- Can't achieve unit economics

**Types of pivots:**
- Customer segment pivot (same product, different customer)
- Value capture pivot (same product, different revenue model)
- Product pivot (different solution to same problem)
- Problem pivot (different problem for same customer)

## Resources

**Books:**
- "Playing to Win" - AG Lafley & Roger Martin
- "Running Lean" - Ash Maurya
- "The Lean Startup" - Eric Ries
- "Obviously Awesome" - April Dunford (Positioning)

**Tools:**
- Strategyzer.com (Canvas templates)
- Miro/Mural (Collaborative strategy sessions)
- Dovetail (Customer research)

**Internal:**
- Template: `templates/business-canvas-template.md` (single adaptive template for all contexts)
- Examples: `examples.md`

---

Use this reference to develop strategy that is focused, validated, and drives product decisions.
