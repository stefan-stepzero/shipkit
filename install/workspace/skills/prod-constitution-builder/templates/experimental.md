# Experimental Product Constitution

**Context:** Experimental Project - Testing new technology or ideas
**Generated:** [Date]

---

## Prime Directive
Learn what works and what doesn't. Document findings over shipping features.

---

## FORBIDDEN

- ❌ **Premature optimization** (learn first, optimize later)
- ❌ **Production deployment** (keep it experimental)
- ❌ **Feature creep** (focus on the experiment hypothesis)
- ❌ **Traditional timelines** (experiments end when you learn enough)
- ❌ **Perfectionism** (good enough to test is good enough)
- ❌ **Hiding failures** (failed experiments are valuable data)

---

## REQUIRED

- ✅ **Clear hypothesis** (what are you testing?)
- ✅ **Success/failure criteria** (how will you know?)
- ✅ **Document everything** (decisions, learnings, dead ends)
- ✅ **Define "done"** (what signals experiment is complete?)
- ✅ **Time-box exploration** (set maximum time investment)
- ✅ **Share learnings** (blog post, doc, presentation)

---

## ALLOWED (Encouraged)

**This is a learning environment. Optimize for DISCOVERY:**

- Try multiple approaches to same problem
- Use bleeding-edge/unstable tech
- Break conventions and best practices
- Prototype without tests (document findings instead)
- Abandon code mid-stream (learnings > code)
- Extreme approaches (push boundaries)
- Mix incompatible technologies (see what happens)
- Build to throw away
- Fail loudly and learn from it

**The ONLY thing that matters:** Are you learning what you set out to learn?

---

## Decision Framework

**Primary question:** Does this help me learn faster?

- **YES →** Do it (even if unconventional)
- **NO →** Don't do it (even if "best practice")

**Secondary question:** Am I documenting what I learn?

- **YES →** Good, keep going
- **NO →** Stop and document before continuing

---

## Experiment Types

### Technology Experiment
**Goal:** Can we use [new tech] for [use case]?
**Example:** "Can we use WebAssembly for real-time collaboration?"
**Success:** Clear answer on feasibility, performance, developer experience

### Architecture Experiment
**Goal:** Does [pattern] solve [problem] better?
**Example:** "Does event sourcing simplify our audit requirements?"
**Success:** Data on trade-offs, implementation complexity, maintainability

### UX Experiment
**Goal:** Will users [behave differently] with [new pattern]?
**Example:** "Will users engage more with conversational UI vs traditional forms?"
**Success:** User feedback, behavioral data, preference insights

### Integration Experiment
**Goal:** Can [system A] work with [system B]?
**Example:** "Can we integrate our auth with enterprise SSO providers?"
**Success:** Integration patterns, gotchas, feasibility assessment

---

## Documentation Requirements

**Must capture:**

1. **Hypothesis** - What we thought would happen
2. **Approach** - What we actually tried
3. **Results** - What actually happened
4. **Learnings** - What we learned
5. **Recommendation** - Should we adopt this? Why/why not?
6. **Evidence** - Code snippets, metrics, screenshots

**Format:** Markdown doc, internal blog post, or README

---

## Success Criteria

**Experiment is successful when you can answer:**

1. **Did we test the hypothesis?** (YES/NO)
2. **Do we have clear data?** (YES/NO)
3. **Can we make a decision?** (Adopt / Iterate / Abandon)
4. **Are findings documented?** (YES/NO)
5. **Did we learn something unexpected?** (Bonus points)

**If 4/5 YES → Experiment complete**
**If < 4 YES → Refine and continue**

---

## Transition Paths

**After experiment completes:**

### If findings are positive:
- Adopt experimental approach in real project
- Use MVP or Greenfield constitution for implementation
- Reference experiment docs in technical decisions

### If findings are negative:
- Document why approach didn't work
- Archive experiment code
- Share learnings to prevent others from repeating

### If findings are unclear:
- Refine hypothesis
- Design better test
- Time-box additional exploration (max 1 week)

---

## Quality Standards

**Code quality: Low to Medium**
- Focus on "works enough to test"
- Skip edge cases
- Minimal error handling
- No production polish

**Documentation quality: HIGH**
- Clear hypothesis
- Detailed findings
- Honest assessment
- Actionable recommendations

**The code is disposable. The learnings are permanent.**

---

**Timeline:** Variable (time-boxed per hypothesis)
**Next Step:** Document findings → Decide (Adopt / Iterate / Abandon) → Archive or Implement
