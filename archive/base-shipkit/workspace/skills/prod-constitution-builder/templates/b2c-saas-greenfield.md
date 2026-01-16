# Established B2C Product Constitution

**Context:** Established product with proven product-market fit
**Generated:** [Date]

---

## Prime Directive
Protect user trust while continuing to innovate.

---

## FORBIDDEN

- ❌ **Breaking existing user workflows** (grandfather old flows, AB test changes)
- ❌ **Surprising users with UI changes** (announce, preview, migrate gradually)
- ❌ **Removing features without data** (usage <1% AND alternatives exist)
- ❌ **Shipping without metrics** (how do we know if this worked?)
- ❌ **Ignoring accessibility** (WCAG 2.1 AA minimum)
- ❌ **Degrading performance** (p95 latency budget enforced)
- ❌ **Dark patterns** (user-hostile growth hacks)
- ❌ **Bypassing design system** (consistency > innovation)
- ❌ **Skipping user research** (minimum 5 users for major changes)
- ❌ **Breaking mobile experience** (60%+ of traffic)

---

## REQUIRED

- ✅ **A/B test major changes** (statistically significant sample)
- ✅ **Backward compatibility** (migrations, not rewrites)
- ✅ **Error budgets met** (99.9% uptime minimum)
- ✅ **Performance budget** (core web vitals in green)
- ✅ **Design review** (follows system, maintains consistency)
- ✅ **Analytics instrumentation** (how do we measure success?)
- ✅ **User research for big bets** (interviews, usability tests)
- ✅ **Mobile-first development** (then adapt to desktop)
- ✅ **Gradual rollouts** (feature flags, %  rollout, kill switch)
- ✅ **Documentation updated** (help docs, release notes)

---

## ALLOWED TECHNICAL DEBT

**Strategic debt only:**

- Short-term hacks if documented and scheduled for cleanup
- Duplicate code if it isolates risk (don't refactor critical paths)
- Workarounds for third-party bugs (with monitoring)

**NOT allowed:**
- Skipping tests on critical paths
- Ignoring known security issues
- Letting tech debt accumulate without plan

---

## Decision Framework

**For new features:**

1. **Does this serve our core user?** (reference personas)
2. **Does it move our North Star metric?** (or leading indicator)
3. **Can we measure impact?** (instrument before shipping)
4. **Does it respect existing mental models?** (or is change worth it?)
5. **What's the rollback plan?** (feature flags, kill switch)

**For removing features:**

1. **Usage < 1% AND declining?** (check analytics)
2. **Alternative exists?** (migration path)
3. **Communicated 60+ days advance?** (email, in-app, blog)
4. **Power users consulted?** (they'll be loudest critics)

**For technical decisions:**

1. **Does this improve reliability/performance?** (green light)
2. **Does this improve developer velocity?** (probably yes)
3. **Is this resume-driven development?** (probably no)

---

## Quality Standards

**What "done" means:**

**For features:**
- [ ] Design approved (follows design system)
- [ ] Instrumented (can measure success)
- [ ] A/B test plan if major change
- [ ] Tested on mobile + desktop
- [ ] Accessibility checked (screen reader, keyboard nav)
- [ ] Performance budget met (core web vitals)
- [ ] Gradual rollout plan (start 5%, then 25%, 50%, 100%)
- [ ] Documentation updated
- [ ] Rollback plan documented

**For bugs:**
- [ ] Severity assessed (P0/P1/P2)
- [ ] Root cause identified
- [ ] Fix + test to prevent regression
- [ ] Deployed within SLA (P0: 4hrs, P1: 24hrs, P2: 1week)

**For releases:**
- [ ] All tests passing (unit, integration, E2E)
- [ ] Staging tested (smoke test critical paths)
- [ ] Performance regression check
- [ ] Feature flags configured
- [ ] Rollback plan ready
- [ ] On-call engineer notified

---

## Metrics That Matter

**Health metrics (monitor always):**

- **Reliability:** Uptime, error rate, p95 latency
- **Growth:** MAU, retention cohorts, activation rate
- **Engagement:** DAU/MAU ratio, sessions per user
- **Business:** Revenue, conversion rate, churn

**Per-feature metrics:**

- Usage rate (% of users who use it)
- Success rate (% who complete intended action)
- Impact on North Star (does it move the needle?)

---

## User Trust Principles

**We protect user trust by:**

1. **Privacy first:** Collect minimum data, transparent policies
2. **Respect attention:** No dark patterns, no spam, clear unsubscribe
3. **Reliable:** 99.9% uptime, fast load times, works offline where possible
4. **Accessible:** Works for all users (disability, slow connections, old devices)
5. **Transparent:** Honest pricing, clear terms, admit mistakes
6. **User control:** Easy to export data, delete account, change settings

**If a decision compromises trust → Don't do it**

---

## Innovation vs Stability Balance

**Innovate on:**
- New features (in isolated experiments)
- Non-critical UI (personalization, delight)
- Internal tools (move fast)

**Maintain stability on:**
- Core user flows (don't break what works)
- Authentication/payments (rock solid)
- Data integrity (never lose user data)

**Rule:** 70% maintain/optimize, 30% new features

---

## Success Criteria

**Product is healthy when:**
- ✓ Users trust us (NPS > 50, churn < 5%)
- ✓ Product is reliable (99.9%+ uptime)
- ✓ Growth is sustainable (positive unit economics)
- ✓ Team can ship (velocity maintained)

---

**Review this constitution:** Quarterly
**Update when:** Product phase changes, major pivot, or annually
