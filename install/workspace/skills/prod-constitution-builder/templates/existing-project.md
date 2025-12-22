# Existing Project Constitution

**Context:** Adding Shipkit to an established codebase
**Generated:** [Date]

---

## Prime Directive
Document what exists, guide future work within established patterns, maintain consistency.

---

## Current State Documentation

### Tech Stack (Already Decided)
**Language(s):** [List primary languages in use]
**Framework(s):** [List frameworks currently used]
**Database(s):** [List data storage in use]
**Infrastructure:** [Hosting, deployment, CI/CD currently in place]

### Architecture Patterns (Already Established)
**Application structure:** [e.g., Monolith, Microservices, Modular monolith]
**API style:** [e.g., REST, GraphQL, gRPC, mixed]
**State management:** [How application state is managed]
**Data patterns:** [e.g., Repository pattern, Active Record, ORMs in use]

### Coding Standards (Currently Followed)
**Naming conventions:** [How files, functions, variables are named]
**File organization:** [How code is structured in directories]
**Testing approach:** [Current test coverage, frameworks, standards]
**Code review process:** [Current PR/review workflow]

### Quality Metrics (Current Baseline)
**Test coverage:** [Current %]
**Build time:** [Current time]
**Deployment frequency:** [Current cadence]
**Technical debt:** [Known issues, areas needing refactor]

---

## What We Can Change

**Low risk (safe to modify):**
- New feature implementation patterns
- Documentation approach
- Code comments and clarity
- Test coverage improvements
- Dev tooling and scripts

**Medium risk (plan carefully):**
- Refactoring existing features
- Upgrading dependencies
- Changing coding standards for new code
- Introducing new patterns alongside old

**High risk (requires team consensus):**
- Changing core architecture
- Replacing major dependencies
- Migrating databases
- Rewriting large sections

---

## What We Must Preserve

**Non-negotiable (established patterns):**
- ✅ Existing API contracts (external integrations depend on them)
- ✅ Database schemas (data migration is expensive)
- ✅ Core business logic (don't break what works)
- ✅ Team's existing workflow (unless explicitly changing)
- ✅ Production stability (no risky experiments in main codebase)

**Honor existing decisions:**
- Even if you'd choose differently today, respect that past decisions had context
- Understand why before proposing changes
- Propose improvements, don't criticize what exists

---

## Decision Framework for New Work

### When adding new features:

**Question 1:** Does an established pattern exist for this?
- **YES →** Follow existing pattern (consistency > personal preference)
- **NO →** Create new pattern, document it, propose as standard

**Question 2:** Does this introduce new technology?
- **YES →** Justify why existing tech can't solve it, get team buy-in
- **NO →** Proceed with existing tech stack

**Question 3:** Does this touch existing code?
- **YES →** Match existing style, even if outdated
- **NO →** Can use modern patterns, but document why different

### When refactoring existing code:

**Question 1:** Is this broken or causing issues?
- **YES →** Fix is justified, but maintain external behavior
- **NO →** Don't refactor for style alone (boy scout rule exceptions only)

**Question 2:** Will this improve measurable metrics?
- **YES →** (Performance, test coverage, readability) Proceed with care
- **NO →** Defer to when business value is clearer

**Question 3:** Have you preserved all existing tests?
- **YES →** Good, tests are your safety net
- **NO →** Write tests first, then refactor

---

## Standards for New Code

**Follow existing:**
- Language/framework versions in use
- File naming and organization conventions
- Testing frameworks and approaches
- Code review process
- Deployment workflow

**Improve gradually:**
- Better documentation than what exists
- Higher test coverage than baseline
- Clearer naming than old code
- More explicit error handling

**Don't:**
- Mix multiple coding styles in same feature
- Introduce new frameworks without discussion
- Refactor unrelated code "while you're there"
- Criticize existing code in commit messages

---

## Technical Debt Management

**Document, don't fix immediately:**

### Known Issues (Inherited)
[List known technical debt, don't fix during feature work]

### Areas for Future Improvement
[Track improvements, schedule dedicated time]

### Quick Wins (Safe Improvements)
[Small, low-risk improvements that don't block features]

**Rule:** Feature work is for features. Refactoring is separate, planned work.

---

## Onboarding New Patterns

**When introducing new approach:**

1. **Propose it** - Document why it's better
2. **Prototype it** - Show it working in isolated feature
3. **Get consensus** - Team must agree it's an improvement
4. **Document it** - Update this constitution
5. **Migrate gradually** - Don't force big-bang changes

**Example:** Introducing new testing pattern
- ✅ Use it in new features
- ✅ Document approach
- ⏳ Propose retroactive application
- ❌ Don't force immediate adoption everywhere

---

## Constraints and Realities

**Acknowledge limitations:**
- Legacy code exists (can't rewrite everything)
- Technical debt exists (prioritize business value)
- Team has existing habits (change takes time)
- External dependencies constrain choices
- Production systems must stay stable

**Work within constraints:**
- Improve incrementally, not revolutionarily
- Respect that "perfect" isn't realistic
- Focus on value delivery over purity
- Build trust before proposing big changes

---

## Success Criteria

**Shipkit integration is successful when:**

1. **New features ship consistently** (using Shipkit workflows)
2. **Quality improves gradually** (measurable: tests, bugs, velocity)
3. **Team adopts patterns** (voluntary adoption, not forced)
4. **Existing features still work** (no regressions introduced)
5. **Documentation improves** (specs, plans, decisions recorded)

**Metrics to track:**
- Feature delivery consistency
- Test coverage trend
- Bug report trend
- Team confidence in changes

---

## Integration with Existing Workflow

**How Shipkit fits:**

### For new features:
```
User story → /dev-specify → /dev-plan → /dev-tasks → /dev-implement
(Shipkit workflow using existing tech stack and patterns)
```

### For existing features:
```
Maintain current workflow (don't force Shipkit on existing code)
Consider Shipkit for major refactors only
```

### For bugs:
```
Use existing bug workflow (Shipkit is for new development)
```

**Transition gradually, don't disrupt what works.**

---

## Quality Standards

**Code quality: Match or exceed existing baseline**
- Same or better test coverage
- Same or better documentation
- Same or better performance
- Better clarity (this is where you can improve)

**Process quality: Enhance existing workflow**
- Add specs where missing
- Add plans for complex changes
- Keep existing review process
- Improve incrementally

**The goal: Make the codebase better, not different.**

---

**Timeline:** Ongoing (continuous integration of Shipkit practices)
**Next Step:** Start with one new feature using Shipkit → Gather team feedback → Iterate
