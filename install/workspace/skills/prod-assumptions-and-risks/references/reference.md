# Assumptions & Risk Management Reference

Concise guide to identifying assumptions, assessing risks, and planning mitigations.

---

## Assumption Identification

### What is an Assumption?

**Something you believe to be true but haven't validated.**

**Examples:**
- "Users will pay $20/month" (assumption until proven)
- "Market size is 10M potential users" (assumption until researched)
- "Users want feature X" (assumption until tested)

### How to Find Assumptions

**Ask:**
1. "For this to succeed, what must be true about our customers?"
2. "What must be true about our product?"
3. "What must be true about our market/timing?"
4. "What must be true about our team/execution?"

**Look in:**
- User stories ("As a user, I want..." - assumes users want this)
- Business model ("We'll charge $X" - assumes willingness to pay)
- Technical specs ("We'll use tech Y" - assumes it can scale)
- Go-to-market plan ("We'll acquire via channel Z" - assumes channel works)

### Types of Assumptions

**Customer Assumptions:**
- Problem exists and is painful
- Target segment is large enough
- Users will change behavior
- Willingness to pay at price point

**Product Assumptions:**
- Feature set is complete enough
- UX is intuitive enough
- Performance is acceptable
- Integration needs are met

**Market Assumptions:**
- Timing is right (not too early/late)
- Competition is beatable
- Distribution channels are accessible
- Regulatory environment is favorable

**Execution Assumptions:**
- Team has required skills
- Timeline is achievable
- Budget is sufficient
- Dependencies will be met

### Validating Assumptions

**Cheap & Fast:**
- **User interviews:** 5-10 convos can validate/invalidate
- **Landing page test:** Measure interest before building
- **Prototype test:** Click-through mockups
- **Pricing survey:** Willingness-to-pay questions

**More Expensive:**
- **Pilot/Beta:** Small group tests real product
- **Market research:** TAM/SAM analysis
- **Technical spike:** Proof-of-concept build

**Prioritize validation by:**
1. **Risk:** What's the cost if we're wrong?
2. **Uncertainty:** How confident are we?
3. **Impact:** How much does this affect success?

---

## Risk Assessment

### Risk = Likelihood × Impact

**Likelihood (1-3):**
- **Low (1):** Unlikely to happen (<25% chance)
- **Medium (2):** Could happen (25-75% chance)
- **High (3):** Likely to happen (>75% chance)

**Impact (1-3):**
- **Low (1):** Minor inconvenience, easy recovery
- **Medium (2):** Delays timeline or increases cost, recoverable
- **High (3):** Project failure or major pivot required

**Priority Score = Likelihood × Impact (1-9)**
- **7-9:** Address immediately (high priority)
- **4-6:** Plan mitigation (medium priority)
- **1-3:** Monitor (low priority)

### Common Risks by Category

**Technical:**
- Scalability (can't handle users)
- Reliability (frequent downtime)
- Security (data breach)
- Integration (third-party fails)
- Technical debt (slows future dev)

**Market:**
- Competition (better/cheaper alternative)
- Timing (too early, users not ready)
- Adoption (switching costs too high)
- Regulation (compliance changes)

**Execution:**
- Team (key person leaves)
- Timeline (wrong estimates)
- Budget (burn rate too high)
- Scope creep (mission drift)

**Product:**
- Usability (too complex)
- Value prop (not compelling)
- Quality (bugs drive churn)
- Completeness (missing must-haves)

---

## Risk Mitigation Strategies

### 4 Ways to Handle Risk

**1. Mitigate (Reduce Likelihood or Impact)**
- Add redundancy (backup systems)
- Build safeguards (validation, testing)
- Create buffers (timeline, budget)
- **Example:** Load testing reduces scalability risk

**2. Avoid (Eliminate the Risk)**
- Don't do the risky activity
- Choose different approach
- **Example:** Use proven tech instead of bleeding-edge

**3. Transfer (Make it Someone Else's Problem)**
- Insurance
- Outsource to specialist
- Partnership agreements
- **Example:** Use AWS (they handle infrastructure risk)

**4. Accept (Live with It)**
- Risk too low to worry about
- Cost to mitigate > potential impact
- Monitor and respond if it happens
- **Example:** Accept risk of minor bugs in POC

### Mitigation Planning Template

**For each high-priority risk:**

**Preventive (reduce likelihood):**
- What actions make this less likely to happen?

**Detective (early warning):**
- How will we know if this is starting to happen?
- What metrics indicate trouble?

**Corrective (response plan):**
- If this happens, what do we do?
- Who's responsible for acting?

---

## Practical Frameworks

### Pre-Mortem Exercise

**"It's 6 months from now. The project failed. Why?"**

1. Team imagines project failed
2. Everyone writes reasons why (5 min)
3. Share and discuss
4. Convert top reasons into risks to mitigate

**Benefits:** Surfaces concerns people are afraid to voice.

### FMEA (Failure Modes & Effects Analysis)

Systematic way to identify failure points:

1. List all components/steps
2. For each, ask: "How could this fail?"
3. Rate: Severity × Likelihood × Detectability
4. Prioritize highest scores for mitigation

### Dependency Mapping

**Identify what must happen for you to succeed:**
- External dependencies (partners, APIs, regulations)
- Internal dependencies (hiring, funding, features)
- Timing dependencies (market readiness, competition)

**For each:**
- Status: Available, in-progress, or uncertain
- Contingency: What if this falls through?

---

## Risk Monitoring

### When to Reassess

**Regular:**
- Weekly: High-priority risks
- Monthly: All risks + new risk identification
- Quarterly: Full assumption validation

**Event-Driven:**
- Major milestone (launch, funding round)
- Assumption invalidated (user research contradicts belief)
- Risk materializes (something goes wrong)
- Market change (new competitor, regulation)

### Key Metrics

**Define thresholds that trigger action:**
- "If conversion < 2%, we have a problem"
- "If churn > 5%/month, pause new acquisition"
- "If load time > 3 sec, prioritize performance"

---

## Common Mistakes

**1. Confusing Assumptions with Facts**
- ❌ "Users need this" (assumption disguised as fact)
- ✅ "We assume users need this. We'll validate by..."

**2. Not Validating Riskiest Assumptions First**
- ❌ Build for 6 months, then test pricing
- ✅ Test pricing in week 1 (cheap, high-impact)

**3. Ignoring Low-Likelihood, High-Impact Risks**
- ❌ "Data breach won't happen to us"
- ✅ "Unlikely, but catastrophic. We'll add encryption."

**4. Analysis Paralysis**
- ❌ Spend 3 months documenting every possible risk
- ✅ Identify top 5-10 risks, mitigate those, ship

**5. Not Updating as You Learn**
- ❌ Write assumptions document, never revisit
- ✅ Living document, update as you validate/invalidate

---

## Quick Reference

**Assumption Validation Hierarchy:**
1. Cheapest/fastest first (interviews, surveys)
2. Build minimum to test (prototype, landing page)
3. Ship MVP to validate at scale

**Risk Prioritization:**
1. High likelihood + High impact = Address now
2. Low likelihood + High impact = Plan contingency
3. High likelihood + Low impact = Accept or quick fix
4. Low likelihood + Low impact = Ignore

**Mitigation Strategy Selection:**
- **Mitigate:** Most common (reduce risk)
- **Avoid:** When alternative approach is easy
- **Transfer:** When specialists can handle better
- **Accept:** When cost > benefit

---

**Resources:**
- *The Lean Startup* by Eric Ries (assumption testing)
- *Inspired* by Marty Cagan (risk in product development)
- Pre-mortem technique: HBR article "Performing a Project Premortem"
