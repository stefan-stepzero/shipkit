# MVP Product Constitution

**Context:** Minimum Viable Product - Proving product-market fit
**Generated:** [Date]

---

## Prime Directive
Ship to real users weekly. Get real feedback.

---

## FORBIDDEN

- ❌ **Perfect UI** (functional > beautiful)
- ❌ **Edge cases** (handle happy path only)
- ❌ **Enterprise features** (serve individual users first)
- ❌ **Premature optimization** (slow code that works > fast code that doesn't)
- ❌ **Building features users didn't ask for**
- ❌ **Scalability concerns** (10 users ≠ 10,000 users, solve real problems)
- ❌ **Comprehensive testing** (manual verification is fine)
- ❌ **Multiple payment tiers** (one price, simple)
- ❌ **Admin dashboards** (use database directly)
- ❌ **Fancy animations** (users want fast, not flashy)

---

## REQUIRED

- ✅ **Core user flow works end-to-end** (user can complete primary job)
- ✅ **Real users can access it** (deployed, not localhost)
- ✅ **One metric to track** (MAU, signups, retention - pick ONE)
- ✅ **Way to contact users** (email list minimum, better: in-app chat)
- ✅ **Basic error tracking** (know when things break - Sentry/LogRocket)
- ✅ **User feedback mechanism** (survey, email, typeform)
- ✅ **Weekly user conversations** (talk to 3-5 users minimum)
- ✅ **Can ship in < 1 day** (small iterations only)
- ✅ **Clear success criteria** (what proves this works?)
- ✅ **Recovery plan** (can rollback/fix in minutes, not hours)

---

## ALLOWED TECHNICAL DEBT

**Manual processes:**
- You can manually onboard users
- You can manually run reports
- You can manually handle edge cases

**Code quality:**
- Hacky code if isolated and documented with `// TODO: Clean up after validation`
- Missing tests if you manually verify each release
- Duplicate code if it ships faster
- Hardcoded values if they're easy to change later

**Infrastructure:**
- Single server (no load balancer yet)
- Monolith (microservices are premature)
- Simple auth (email/password, no SSO yet)
- File uploads to local disk (S3 later)

**Design:**
- Tailwind defaults are fine
- Stock photos are fine
- Basic responsive (desktop + mobile, tablet can wait)
- Accessibility basics (semantic HTML, alt text, that's it)

---

## Decision Framework

**When choosing between options, ask:**

1. **Does this help us learn if users want this?** (YES → Do it, NO → Skip it)
2. **Can we ship this in < 3 days?** (NO → Break it down further)
3. **Will this work for our first 100 users?** (YES → Good enough)
4. **Can we do this manually instead?** (YES → Do it manually first)

**Red flags:**
- "We'll need this when we scale" → Not MVP
- "This will make it more robust" → Not MVP
- "Competitors have this" → Maybe not MVP
- "This is best practice" → Maybe not MVP

**Green lights:**
- "Users asked for this 5 times" → Probably MVP
- "Can't do core job without it" → Definitely MVP
- "Takes 2 hours to build" → Probably worth it
- "Critical security/privacy issue" → Must fix

---

## Quality Standards

**What "done" means:**

**For features:**
- [ ] Works on happy path for target user
- [ ] Deployed to production
- [ ] 3 real users tested it
- [ ] Error tracking in place
- [ ] Can be explained in one sentence

**For bugs:**
- [ ] Reproduced in production
- [ ] Fixed and verified
- [ ] Deployed within 1 day
- [ ] User who reported it confirmed fix

**For releases:**
- [ ] Core flow still works (manual smoke test)
- [ ] No errors in last hour (check error tracker)
- [ ] Can rollback in < 5 minutes if needed

---

## Metrics That Matter

**Track these, ignore everything else:**

1. **Activation:** % of signups who complete core action
2. **Retention:** % who come back next week
3. **One key metric:** [Define based on your product]

**Ignore for now:**
- Conversion rate (too early)
- LTV (not enough data)
- Viral coefficient (focus on delight first)
- Page load time (unless > 3 seconds)

---

## Success Criteria

**MVP is successful when:**
- ✓ 10+ people using this weekly
- ✓ Users get value (they come back, they tell friends)
- ✓ Positive feedback > Negative feedback
- ✓ Core metric is trending up week-over-week

**Then graduate to V1.0 and adopt a more mature constitution.**

---

**Review this constitution:** Every 2 weeks
**Update when:** You hit 100 weekly active users or 6 months, whichever comes first
