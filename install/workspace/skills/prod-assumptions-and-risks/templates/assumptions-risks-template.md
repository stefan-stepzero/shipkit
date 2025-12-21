# Assumptions & Risks

**Product:** [Product Name]
**Created:** [Date]
**Stage:** [POC/MVP/Established]

---

## Critical Assumptions

**What must be true for this to succeed?**

### Customer/Market Assumptions

| Assumption | How We'll Validate | If Wrong, Then... |
|------------|-------------------|-------------------|
| [Users will pay $X/month for this] | Pricing survey, willingness-to-pay test | Pivot pricing model or target different segment |
| [Target market size is Y] | Market research, TAM analysis | Narrow focus or expand addressable market |
| [Users have problem X] | User interviews (min 10) | Redefine problem or pivot product |

### Product Assumptions

| Assumption | How We'll Validate | If Wrong, Then... |
|------------|-------------------|-------------------|
| [Users will change from current tool] | Onboarding tests, switching cost analysis | Reduce friction, increase value prop |
| [Feature X drives retention] | Usage analytics, cohort analysis | Deprioritize or remove feature |
| [Time to value < 5 minutes] | User testing sessions | Simplify onboarding or add guidance |

### Technical Assumptions

| Assumption | How We'll Validate | If Wrong, Then... |
|------------|-------------------|-------------------|
| [Tech stack can scale to 10K users] | Load testing, architecture review | Refactor or change infrastructure |
| [Integration with API X is reliable] | Pilot testing, SLA review | Build fallback or find alternative |
| [Team can deliver in 3 months] | Sprint velocity, complexity estimate | Reduce scope or extend timeline |

### Business Model Assumptions

| Assumption | How We'll Validate | If Wrong, Then... |
|------------|-------------------|-------------------|
| [CAC < $X, LTV > $Y] | Early cohort economics | Adjust channels or pricing |
| [Conversion rate > Z%] | Landing page tests, funnel analysis | Optimize funnel or messaging |
| [Churn rate < W%] | First 90 days tracking | Improve onboarding or product |

---

## Risk Assessment

**Likelihood:** Low (1) | Medium (2) | High (3)
**Impact:** Low (1) | Medium (2) | High (3)
**Priority = Likelihood × Impact**

### High Priority Risks (Score 6-9)

#### Risk: [Description]
- **Likelihood:** [1-3]
- **Impact:** [1-3]
- **Priority Score:** [1-9]
- **Mitigation:**
  - [ ] [Action 1]
  - [ ] [Action 2]
- **Owner:** [Who's responsible]
- **Deadline:** [When to address]

---

### Medium Priority Risks (Score 3-4)

#### Risk: [Description]
- **Likelihood:** [1-3]
- **Impact:** [1-3]
- **Priority Score:** [1-9]
- **Mitigation:**
  - [ ] [Action]
- **Owner:** [Who]

---

### Low Priority Risks (Score 1-2)

#### Risk: [Description]
- **Likelihood:** [1-3]
- **Impact:** [1-3]
- **Monitor:** [When to reassess]

---

## Common Risk Categories

### Technical Risks
- **Scalability:** Can infrastructure handle growth?
- **Reliability:** What's acceptable uptime? (e.g., 99.9%)
- **Security:** Data protection, compliance requirements
- **Integration:** Third-party dependencies
- **Technical debt:** Shortcuts that will cost us later

### Market Risks
- **Competition:** New entrant or incumbent response
- **Timing:** Too early or too late to market
- **Adoption:** Switching costs, behavior change required
- **Regulation:** Legal/compliance changes

### Execution Risks
- **Team:** Key person risk, skill gaps
- **Timeline:** Dependencies, unknowns, optimism bias
- **Budget:** Runway, burn rate, funding availability
- **Scope creep:** Feature bloat, mission drift

### Product Risks
- **Usability:** Too complex, steep learning curve
- **Value prop:** Not compelling enough vs. alternatives
- **Quality:** Bugs, poor UX, performance issues
- **Completeness:** Missing must-have features

---

## Dependency Mapping

**What external factors must align?**

### Critical Dependencies

| Dependency | Status | Risk If Unavailable | Contingency |
|------------|--------|---------------------|-------------|
| [Third-party API] | [Available/TBD] | [Can't deliver feature X] | [Build workaround or delay] |
| [Hiring engineer] | [In progress] | [Timeline slips 2 months] | [Reduce scope or outsource] |
| [Partnership with Y] | [Negotiating] | [Lose distribution channel] | [Alternative channels] |

---

## Mitigation Strategies

### For High-Priority Risks:

**Risk:** [Top risk]
1. **Preventive:** [Actions to reduce likelihood]
2. **Detective:** [How we'll know if it's happening]
3. **Corrective:** [Response plan if it occurs]
4. **Acceptance:** [If cost to mitigate > impact, acknowledge and monitor]

---

## Risk Triggers & Monitoring

**When do we reassess?**

- **Weekly:** Check high-priority risk status
- **Monthly:** Update likelihood/impact based on new data
- **Milestone-based:** After each major release or funding round
- **Event-driven:** When assumptions invalidated or risks materialize

**Key Metrics to Watch:**
- [Metric 1]: [Threshold that indicates risk]
- [Metric 2]: [Threshold]
- [Metric 3]: [Threshold]

---

## Decision Framework

**When risks materialize:**

1. **Assess:** Impact on timeline, budget, scope
2. **Decide:** Mitigate, accept, transfer, or avoid
3. **Act:** Execute mitigation plan
4. **Communicate:** Update stakeholders
5. **Learn:** Document for future reference

---

## Stage-Specific Guidance

### POC Stage
**Focus:** Validate core assumptions quickly
- Test highest-risk assumptions first (fail fast)
- Accept technical debt (prove value before perfecting)
- Defer: scaling concerns, edge cases, polish
- **Key Question:** "Does anyone want this?"

### MVP Stage
**Focus:** Reduce execution risk
- Address must-solve problems (security, reliability)
- Plan for early growth (avoid rewrite at 100 users)
- Defer: advanced features, optimizations
- **Key Question:** "Can we deliver quality basics reliably?"

### Established Stage
**Focus:** Mitigate all material risks
- Comprehensive testing, security audits
- Disaster recovery, business continuity plans
- Competitive moats, defensibility
- **Key Question:** "Can we sustain and defend this?"

---

## Change Log

| Date | Change | Reason |
|------|--------|--------|
| [Date] | [What changed] | [Why] |

---

**Next Steps:**
- Review assumptions quarterly or when invalidated
- Update risk scores as new information emerges
- Add new risks as they're identified
- Archive resolved risks (keep for learnings)
