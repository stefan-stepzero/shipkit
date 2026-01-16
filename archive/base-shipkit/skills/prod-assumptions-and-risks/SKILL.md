# Assumptions & Risks

**Identify critical assumptions and assess risks before building.**

---

## What This Skill Does

This skill helps you:
1. **Identify critical assumptions** that underpin your product's success
2. **Validate assumptions** before investing time/money
3. **Assess risks** using Likelihood × Impact scoring
4. **Plan mitigations** for high-priority risks
5. **Run pre-mortems** to uncover hidden failure modes

**Output:** A concise, actionable assumptions & risks document.

---

## When to Use This

**Use this skill when:**
- Starting a new product or feature
- Making strategic decisions (pricing, market, tech stack)
- Entering a new market or launching to new audience
- Before committing significant resources
- Planning an MVP or major release

**Prerequisites:**
- **prod-user-stories**: You need user stories to identify what assumptions underpin them

---

## How to Use This Skill

### Step 1: Read References

Read all files in the skill's references directory:
```bash
.shipkit/skills/prod-assumptions-and-risks/references/
```

**If >2 files exist:** Ask the user which files are most relevant for this task.

This includes built-in guidance (reference.md, examples.md) and any user-added files (PDFs, research, notes).

---

### Step 2: Initialize

```bash
/prod-assumptions-and-risks
```

**What happens:**
- Creates `assumptions-risks.md` from template
- Checks prerequisite (user-stories.md must exist)
- Opens document for editing

### Step 3: Identify Critical Assumptions

**Work through these categories:**

1. **Customer Assumptions**
   - Who will use this?
   - What will they pay?
   - Why will they switch from alternatives?

2. **Product Assumptions**
   - What must the product do/be?
   - What experience must it deliver?
   - What performance is required?

3. **Market Assumptions**
   - Market size and accessibility
   - Competition and differentiation
   - Distribution channels

4. **Business Model Assumptions**
   - Revenue model
   - Cost structure
   - Unit economics

5. **Execution Assumptions**
   - Team capabilities
   - Timeline estimates
   - Technical feasibility

**For each assumption, define:**
- How you'll validate it (test)
- What you'll do if it's wrong (pivot plan)

### Step 4: Assess Risks

**Use Likelihood × Impact scoring (1-9 scale):**

**Likelihood:**
- 1 = Unlikely (<25%)
- 2 = Possible (25-50%)
- 3 = Likely (>50%)

**Impact:**
- 1 = Low (minor setback)
- 2 = Medium (delays or reduced scope)
- 3 = High (project failure)

**Priority Score = Likelihood × Impact**
- 6-9 = High priority (address now)
- 3-4 = Medium priority (monitor and plan)
- 1-2 = Low priority (accept)

### Step 5: Plan Mitigations

**For each high-priority risk (6-9), choose a mitigation strategy:**

1. **Mitigate**: Reduce likelihood or impact
   - Example: Add redundancy, improve testing, simplify scope

2. **Avoid**: Change approach to eliminate risk
   - Example: Use proven tech instead of experimental, buy vs build

3. **Transfer**: Share risk with others
   - Example: Insurance, partnerships, outsourcing

4. **Accept**: Acknowledge risk, plan contingency
   - Example: Low-cost risks you can recover from

### Step 6: Run Pre-Mortem (Optional but Powerful)

**Exercise:** "It's 6 months from now. We failed. Why?"

**How to run:**
1. Gather team (PM, eng, design, stakeholders)
2. Imagine project failed spectacularly
3. Brainstorm failure reasons (5-10 minutes)
4. Identify top 5 most likely causes
5. Convert to risks and add mitigations

**This surfaces assumptions and risks you wouldn't think of otherwise.**

---

## Stage-Specific Guidance

### POC Stage
**Focus:** Hypothesis validation

**Critical assumptions:**
- Problem exists and is painful
- Target users are reachable
- Proposed solution resonates

**Key risks:**
- Problem isn't real or urgent
- Can't reach target users
- Solution doesn't resonate

**Validation speed matters more than perfection.**

### MVP Stage
**Focus:** Must-have features only

**Critical assumptions:**
- Users will onboard themselves
- Core feature set is sufficient
- Pricing is acceptable

**Key risks:**
- Low adoption (poor product-market fit)
- High churn (not delivering value)
- Can't acquire users economically

**Test assumptions before scaling.**

### Established Stage
**Focus:** Sustainability and growth

**Critical assumptions:**
- Current tech/team scales to next milestone
- Competitive moat is defensible
- Unit economics improve with scale

**Key risks:**
- Technical debt limits velocity
- Competition commoditizes product
- Regulatory or compliance changes

**Address all material risks proactively.**

---

## Template Structure

The template uses **token-lean tables** for efficiency:

```markdown
## Critical Assumptions

| Assumption | How We'll Validate | If Wrong, Then... |
|------------|-------------------|-------------------|
| Users will pay $X/month | Pricing survey (50 users) | Adjust to freemium model |

## Risk Assessment

#### Risk: [Description]
- **Likelihood:** [1-3]
- **Impact:** [1-3]
- **Priority Score:** [1-9]
- **Mitigation:**
  - [ ] [Action item 1]
  - [ ] [Action item 2]
```

**This format maximizes clarity while minimizing tokens.**

---

## Reference Materials

**Available in `references/`:**

1. **reference.md**: Concise methodologies
   - Pre-mortem exercise guide
   - Risk assessment frameworks (FMEA lite)
   - Mitigation strategies
   - Assumption validation techniques

2. **examples.md**: Practical examples
   - B2B SaaS (team collaboration)
   - B2C mobile (fitness app)
   - E-commerce (furniture store)
   - Developer tools (API monitoring)
   - Platform risks (third-party dependencies)

**Add your own references:**
- Risk registers from past projects
- Post-mortems and lessons learned
- Industry-specific frameworks
- Regulatory compliance checklists

---

## Common Patterns

### 1. Pricing Assumptions
**Assumption:** Users will pay $X for Y value

**Validate:**
- Van Westendorp survey (4 questions, 50 users)
- Pre-orders or waitlist conversion
- A/B test pricing tiers

**If wrong:**
- Adjust pricing model
- Change value proposition
- Target different segment

### 2. Technical Feasibility
**Assumption:** We can build X with technology Y

**Validate:**
- 2-day spike (proof of concept)
- Consult domain experts
- Review similar implementations

**If wrong:**
- Use different tech stack
- Reduce scope
- Buy vs build

### 3. Market Size
**Assumption:** X companies/users need this

**Validate:**
- TAM/SAM/SOM analysis
- Competitor user counts
- Industry reports

**If wrong:**
- Expand addressable market
- Niche down
- Pivot to different market

### 4. User Behavior
**Assumption:** Users will do X regularly

**Validate:**
- Beta usage metrics
- User interviews
- Prototype testing

**If wrong:**
- Adjust product experience
- Add triggers/reminders
- Reconsider value prop

---

## Anti-Patterns to Avoid

❌ **Analysis paralysis**: Don't list 50+ risks. Focus on top 5-10.

❌ **No validation plan**: Every assumption needs a test, not just "we'll see."

❌ **Ignoring low-likelihood, high-impact risks**: 1×3 = 3 (medium priority) might kill your product.

❌ **Technical risks disguised as features**: "Need to use microservices" is a solution, not an assumption.

❌ **Vague mitigations**: "Monitor closely" isn't a mitigation. What's the trigger and action?

---

## Success Criteria

**You've done this well when:**

✅ **Every critical assumption has:**
- Clear validation method
- Timeline for validation (ideally <2 weeks)
- Pivot plan if wrong

✅ **Every high-priority risk (6-9) has:**
- Specific mitigation actions
- Owner assigned
- Deadline or trigger

✅ **Document is actionable:**
- Team can execute on it today
- Clear next steps
- No ambiguity

✅ **Assumptions are testable:**
- Can be proven true or false
- Results inform decisions
- Fast feedback loops

---

## Integration with Other Skills

**Before this skill:**
- `/prod-user-stories` → Understand what you're building and for whom

**After this skill:**
- `/prod-success-metrics` → Define how you'll measure if assumptions hold
- `/prod-discussion` → Make decisions when risks conflict

**Throughout development:**
- Update assumptions as you learn
- Mark validated assumptions as confirmed/refuted
- Add new risks as they emerge

---

## Tips for Success

1. **Collaborate**: Run this exercise with team (PM, eng, design)
2. **Be specific**: "Users won't pay" is vague. "Users won't pay >$10/month" is testable.
3. **Validate early**: Test riskiest assumptions first, before building
4. **Update regularly**: Review monthly, or when major decisions arise
5. **Pre-mortem is powerful**: Always run it - surfaces hidden risks
6. **Don't over-document**: Use tables, keep it concise (hence token-lean template)

---

## Quick Start Checklist

- [ ] Run `/prod-assumptions-and-risks` to initialize
- [ ] List 5-10 critical assumptions across categories (customer, product, market, business, execution)
- [ ] Define validation method for each assumption (<2 weeks to test)
- [ ] Score top 5-10 risks (Likelihood × Impact)
- [ ] Plan mitigations for high-priority risks (6-9)
- [ ] (Optional but recommended) Run pre-mortem with team
- [ ] Review with stakeholders
- [ ] Execute validation tests
- [ ] Update document as you learn

**Remember:** The goal is to surface and validate assumptions BEFORE you invest heavily. Test to learn, learn to decide, decide to build.
