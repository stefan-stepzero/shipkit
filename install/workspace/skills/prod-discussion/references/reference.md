# Product Discussion Reference

Frameworks for clarifying questions, analyzing trade-offs, and making product decisions.

---

## Trade-Off Thinking Framework

Every product decision involves trade-offs. This framework helps surface them.

### The Core Question

**"What are we optimizing for, and what are we willing to give up?"**

Every decision prioritizes some dimensions over others:
- Speed vs Quality
- Simplicity vs Flexibility
- Cost vs Features
- Short-term vs Long-term
- User experience vs Technical debt
- Broad appeal vs Deep value for niche

---

## Clarifying Questions

When someone asks a product question or proposes an idea, clarify:

### 1. What's the Real Question?

**Surface question:** "Should we add dark mode?"

**Real questions might be:**
- Are we losing users who want dark mode?
- Will dark mode improve retention?
- Is dark mode table stakes in our category?
- What's the ROI vs other features?

**How to clarify:**
- "Help me understand the underlying concern. Are we worried about..."
- "What problem does this solve for users?"
- "What would success look like?"

### 2. What Stage Are We At?

**POC:** Validate assumptions quickly
- Prioritize: Learning speed > Polish
- Accept: Technical debt, narrow scope, manual processes

**MVP:** Prove product-market fit
- Prioritize: Core value delivery > Edge cases
- Accept: Missing nice-to-haves, some bugs, limited scale

**Established:** Sustainable growth
- Prioritize: Quality, scalability, competitive moat
- Accept: Slower feature velocity, higher bar for new features

**The trade-offs change by stage.**

### 3. What Are We Optimizing For?

Common optimization targets:
- **User acquisition:** More signups
- **Activation:** Faster time to value
- **Retention:** Users coming back
- **Revenue:** Monetization
- **Efficiency:** Lower costs, faster development
- **Competitive position:** Unique differentiation

**Different goals = different decisions.**

---

## Decision-Making Frameworks

### 1. Impact vs Effort Matrix

```
High Impact, Low Effort    → DO NOW (Quick wins)
High Impact, High Effort   → PLAN CAREFULLY (Strategic bets)
Low Impact, Low Effort     → DO IF TIME (Nice-to-haves)
Low Impact, High Effort    → DON'T DO (Money pit)
```

**Use when:** Prioritizing features or initiatives.

### 2. Reversibility Test (Amazon's Type 1 vs Type 2 Decisions)

**Type 1 (One-way door):** Hard to reverse
- Examples: Choosing tech stack, pricing model, target market
- Approach: Slow, deliberate, gather data, consult experts

**Type 2 (Two-way door):** Easy to reverse
- Examples: UI changes, feature toggles, marketing copy
- Approach: Fast, experiment, learn quickly

**Use when:** Deciding how much analysis to do.

### 3. Regret Minimization

**Ask:** "Will I regret NOT doing this in 1/5/10 years?"

**Use when:** Long-term strategic decisions (market positioning, mission, major pivots).

### 4. Opportunity Cost

**Ask:** "If we do X, what are we NOT doing?"

- Every feature has a cost: time, complexity, maintenance
- "Yes" to one thing means "no" to something else

**Use when:** Resource allocation, roadmap planning.

### 5. First Principles

**Ask:** "Why do we believe this? What's actually true vs inherited assumptions?"

Strip away conventions and reason from fundamentals.

**Example:**
- Convention: "SaaS must have free trials"
- First principles: "Users need to experience value before paying. Is a free trial the only way?"
- Alternative: Demo video, concierge onboarding, money-back guarantee

**Use when:** Challenging industry norms or inherited constraints.

---

## Trade-Off Patterns in Product Development

### 1. Speed vs Quality

**Optimize for speed when:**
- POC/MVP stage (learning > polish)
- Racing competitors to market
- Testing hypothesis cheaply

**Optimize for quality when:**
- Established product (reputation matters)
- High-stakes (healthcare, finance, security)
- Quality is the differentiator

**Hybrid approach:**
- Ship fast to internal beta, slow to public
- Fast for non-critical features, slow for core experience
- "Feature flags" allow gradual rollout

### 2. Simplicity vs Flexibility

**Optimize for simplicity when:**
- Targeting non-technical users
- MVP (prove core value first)
- Reducing onboarding friction

**Optimize for flexibility when:**
- Power users demand customization
- Competing on configurability
- Established product expanding use cases

**Hybrid approach:**
- Simple by default, advanced mode available
- Progressive disclosure (hide complexity until needed)
- Opinionated defaults, but allow overrides

### 3. Broad vs Deep

**Optimize for broad (horizontal) when:**
- Large addressable market
- Network effects matter (more users = more value)
- Revenue from volume

**Optimize for deep (vertical) when:**
- Niche with specific pain
- High willingness to pay
- Deep integration needed

**Example:**
- Slack (broad): Communication tool for all teams
- Salesforce (deep): CRM for sales teams with complex workflows

### 4. Build vs Buy

**Build when:**
- Core differentiator (competitive advantage)
- Unique requirements (no solution fits)
- Long-term cost lower than licensing

**Buy when:**
- Commodity feature (auth, payments, analytics)
- Fast time-to-market critical
- Maintenance burden high

**Trade-off:** Control & customization vs Speed & focus

### 5. Self-Serve vs High-Touch

**Self-serve when:**
- Low price point (<$100/mo)
- Simple product (quick to understand)
- Large volume target (SMBs, consumers)

**High-touch (sales-led) when:**
- High price point (>$10k/yr)
- Complex product (needs explanation)
- Enterprise customers (require customization, security review)

**Trade-off:** Scalability vs Deal size

---

## Reframing Questions as Trade-Offs

### Example 1: "Should we add feature X?"

**Reframe as:**
- **What we gain:** [User value, competitive parity, revenue]
- **What we give up:** [Engineering time, complexity, maintenance]
- **Alternative:** [What else could we do with that time?]
- **Decision criteria:** [What metric would tell us this was the right call?]

**Discussion structure:**
1. **Context:** What's driving this request?
2. **Options:**
   - Option A: Build feature X
   - Option B: Build alternative Y (addresses same need differently)
   - Option C: Don't build, focus on core experience
3. **Pros/Cons:** For each option
4. **Recommendation:** Based on stage, goals, constraints

### Example 2: "How should we price this?"

**Reframe as:**
- **What we're optimizing for:** [Adoption volume vs Revenue per customer]
- **Trade-off:** Low price (more users, less $ each) vs High price (fewer users, more $ each)
- **Constraints:** [CAC, LTV, competitive pricing, perceived value]

**Options:**
- **Freemium:** Free tier + paid upgrades
  - Pros: Low friction, viral growth, large user base
  - Cons: Low conversion (2-5%), support costs on free tier
- **Free trial:** 14-30 days, then pay
  - Pros: Higher conversion (15-25%), qualified users only
  - Cons: Activation pressure, some lost users
- **Flat pricing:** $X/month for everyone
  - Pros: Simple, predictable
  - Cons: Leaves money on table (enterprise would pay more)
- **Tiered pricing:** Good/Better/Best
  - Pros: Captures value at different segments, upsell path
  - Cons: Complexity, "paradox of choice"

### Example 3: "Should we pivot?"

**Reframe as:**
- **What's not working:** [Specific metrics, feedback, market signals]
- **Options:**
  - Pivot: New market / New product / New approach
  - Persevere: Give current strategy more time
  - Iterate: Small changes, not wholesale pivot
- **Sunk cost fallacy:** Don't let past investment drive future decisions
- **Decision criteria:** What would have to be true to pivot vs persevere?

**Framework:**
1. **Diagnose:** Why isn't current approach working?
2. **Options:** Pivot directions or doubling down
3. **Test:** Can we validate pivot hypothesis cheaply before committing?
4. **Decide:** Based on conviction, runway, opportunity cost

---

## Best Practices from Product Skills

### From prod-strategic-thinking
- **Start with why:** Value proposition drives all decisions
- **Know your differentiator:** Protect it, invest in it

### From prod-personas
- **Specific > Generic:** "Busy parent" makes different trade-offs than "fitness enthusiast"
- **Jobs to be done:** Users "hire" products to make progress. What job are we solving?

### From prod-market-analysis
- **Competitive context matters:** Are we first mover (educate market) or fast follower (differentiate)?
- **Category norms:** When to follow them (table stakes) vs break them (differentiation)

### From prod-brand-guidelines
- **Brand consistency:** Does this decision align with our personality and tone?
- **Trust matters:** Don't trade short-term gains for long-term brand damage

### From prod-interaction-design
- **User experience compounds:** Small friction adds up
- **Progressive disclosure:** Don't overwhelm—show complexity when needed

### From prod-user-stories
- **Outcome > Output:** Focus on user value, not feature count
- **Must-have vs nice-to-have:** MoSCoW prioritization

### From prod-assumptions-and-risks
- **Test assumptions early:** Don't build on unvalidated beliefs
- **Pre-mortem:** "We failed. Why?" surfaces hidden risks

### From prod-success-metrics
- **Measure what matters:** Align features to metrics that predict success
- **Leading indicators:** Track early signals, don't wait for lagging outcomes

---

## Common Cognitive Biases to Avoid

### 1. Sunk Cost Fallacy
"We've already invested 6 months, we can't stop now."

**Counter:** Future decisions should be based on future value, not past investment.

### 2. Confirmation Bias
"I think dark mode is important, so I only asked users who mentioned it."

**Counter:** Actively seek disconfirming evidence. Ask "What would prove me wrong?"

### 3. HiPPO (Highest Paid Person's Opinion)
"The CEO wants this feature, so we're building it."

**Counter:** Decisions should be based on data and user value, not authority.

### 4. Feature Bloat
"Our competitor has 50 features, we need 50 too."

**Counter:** Simplicity is often the better strategy. Focus > sprawl.

### 5. Recency Bias
"The last 3 customer calls mentioned X, so X is critical."

**Counter:** Look at aggregate data, not just recent feedback.

---

## Decision Templates

### Feature Decision Template

**Feature:** [Name]

**Problem:** [What user pain does this solve?]

**Options:**
1. **Build it**
   - Pros: [User value, competitive parity, revenue impact]
   - Cons: [Engineering time, complexity, maintenance cost]
2. **Build alternative approach**
   - Pros: [Solves problem differently, maybe simpler]
   - Cons: [Trade-offs]
3. **Don't build**
   - Pros: [Focus on core, avoid complexity]
   - Cons: [Miss opportunity, competitive gap]

**Recommendation:** [Based on stage, goals, data]

**Decision criteria:** [What metric/signal would validate this decision?]

---

### Prioritization Template

**Initiative:** [Name]

**Impact:** [1-10] - How much value to users/business?

**Effort:** [1-10] - How much time/complexity?

**Confidence:** [1-10] - How sure are we of impact?

**Strategic alignment:** [Does this advance our North Star?]

**RICE Score:** (Reach × Impact × Confidence) / Effort

**Decision:** [Do now / Plan for later / Don't do]

---

## Facilitating Productive Discussions

### 1. Disagree and Commit
- Debate openly, decide together, execute aligned
- "I disagree but I'll commit to this decision"

### 2. Strong Opinions, Weakly Held
- Have a point of view, but change it with new data
- Conviction without rigidity

### 3. Socratic Method
- Ask questions to surface assumptions
- "What would have to be true for this to work?"
- "What's the strongest argument against this?"

### 4. Steelman, Don't Strawman
- Argue against the strongest version of an idea, not the weakest
- "The best case for X is... and even then, here's the trade-off..."

---

## Resources

- *The Lean Startup* by Eric Ries (experimentation over planning)
- *Thinking in Bets* by Annie Duke (decision-making under uncertainty)
- *The Mom Test* by Rob Fitzpatrick (asking good questions)
- *Inspired* by Marty Cagan (product management best practices)
