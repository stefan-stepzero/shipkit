# Product Constitution Builder Reference

## What is a Product Constitution?

A constitution is your product's **rule book** - the non-negotiable principles and constraints that guide every decision.

Unlike a strategy (what to build) or roadmap (when to build), a constitution defines **how you build** and **what you never do**.

## Constitution Structure

**Prime Directive:** Single focus, one sentence
**FORBIDDEN:** What you never do (❌)
**REQUIRED:** What you always do (✅)
**ALLOWED TECHNICAL DEBT:** What shortcuts are okay
**Success Criteria:** How you know it's working

## When to Use Each Template

### POC (Proof of Concept)
**Use when:** Validating if idea has legs
**Timeline:** 1-2 weeks MAX
**Goal:** Answer "will people use this?"
**Philosophy:** Speed > everything, throwaway code

### MVP (Minimum Viable Product)
**Use when:** Proving product-market fit
**Timeline:** 2-6 months
**Goal:** Get real users, real feedback
**Philosophy:** Ship weekly, iterate fast, learn

### Established B2C
**Use when:** 1000+ active users, proven PMF
**Goal:** Scale while maintaining trust
**Philosophy:** Protect users, maintain quality, keep innovating

### Established B2B
**Use when:** Enterprise customers, compliance needs
**Goal:** Enterprise-grade reliability
**Philosophy:** Trust, security, compliance first

## How Constitutions Evolve

```
POC → MVP → Established
(2 weeks)   (6 months)   (ongoing)

Throwaway  → Real product → Scale & trust
Speed > all → Ship weekly → Reliability matters
No rules   → Some rules → Many rules
```

## Common Patterns

### FORBIDDEN Sections

**POC:** Almost everything (production code, security, testing)
**MVP:** Perfection, edge cases, premature optimization
**Established:** Breaking changes, downtime, bypassing process

### REQUIRED Sections

**POC:** 5 user interviews, one feature works
**MVP:** Weekly ships, user feedback, one metric
**Established:** A/B tests, backward compatibility, monitoring

### ALLOWED TECHNICAL DEBT

**POC:** Literally everything (it's throwaway)
**MVP:** Documented hacks, manual processes
**Established:** Strategic debt only, with plan

## Constitution Anti-Patterns

❌ **Too vague:**
```markdown
## FORBIDDEN
- Bad code
- Confusing UI
```

✅ **Specific:**
```markdown
## FORBIDDEN
- ❌ Shipping without error tracking
- ❌ Features without analytics instrumentation
```

---

❌ **Aspirational (not enforced):**
```markdown
## REQUIRED
- Write good tests (but we don't actually check)
```

✅ **Enforced:**
```markdown
## REQUIRED
- ✅ Tests pass in CI (blocks merge)
```

---

❌ **One-size-fits-all:**
```markdown
Same rules for POC, MVP, and established product
```

✅ **Context-appropriate:**
```markdown
POC: No tests
MVP: Manual testing
Established: Automated tests required
```

## Using the Constitution

### In Decision Making

**Example: Should we build an admin dashboard?**

Check POC constitution:
- FORBIDDEN: Admin dashboards (use database directly)
- Decision: No

Check Established constitution:
- REQUIRED: Audit logs, monitoring
- Decision: Yes, but only if >100 customers need it

### In Code Review

**Example: PR adds complex caching**

Check MVP constitution:
- FORBIDDEN: Premature optimization
- Reviewer: "Is this solving a real performance problem or theoretical? Reject if theoretical."

### In Product Decisions

**Example: User requests 10 new features**

Check constitution:
- Prime Directive: Ship to users weekly, get feedback
- REQUIRED: Users asked for this 5+ times
- Decision: Which feature was requested most? Build that, defer rest.

## How to Reference in Skills

**All prod-* skills should load the constitution:**

```markdown
## Constitution

Load: `.shipkit/skills/prod-constitution-builder/outputs/product-constitution.md`

All decisions must align with the product constitution.
```

**Dev-* skills reference it for context:**

```markdown
## Product Context

If product constitution exists (`.shipkit/skills/prod-constitution-builder/outputs/product-constitution.md`), reference it to understand:
- What technical debt is allowed
- What quality standards apply
- What constraints exist
```

## When to Update Constitution

**Triggers to update:**
- Product phase changes (POC → MVP → Established)
- Business model changes (B2C → B2B)
- Major pivot
- Compliance requirements added
- Team > 10 people (need more process)

**Review cadence:**
- POC: Never (it's 2 weeks)
- MVP: Every 2 weeks
- Established: Quarterly

## Resources

**Templates:**
- `templates/poc-constitution.md`
- `templates/mvp-constitution.md`
- `templates/established-b2c-constitution.md`
- `templates/established-b2b-constitution.md`

**Internal:**
- Strategic context: `.shipkit/skills/prod-strategic-thinking/outputs/business-canvas.md`

---

A good constitution is:
1. **Specific:** Clear rules, not aspirations
2. **Enforced:** Actually followed, not ignored
3. **Context-appropriate:** Right for your phase
4. **Living:** Updated as product evolves
