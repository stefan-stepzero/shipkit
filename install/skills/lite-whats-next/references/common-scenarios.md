# Common Scenarios

## Scenario 1: Brand New Project

**State**: Nothing exists

**Analysis**:
- Pillar 1 (Vision): ❌ Missing (no why.md)
- Pillar 2 (Understand): ❌ Missing (no stack.md)
- Pillar 3 (Co-design): ❌ Missing (no specs)
- Pillar 4 (Execute): ❌ Not started
- Pillar 5 (Document): ❌ Missing

**Recommendation**:
```
Run: /lite-why-project

Why: Starting a project without vision leads to aimless decisions.
     Define who/why/where first, then everything else aligns.

What this accomplishes:
- Pillar 1: Vision defined
- Outcome: Claude knows your goals for better suggestions
```

---

## Scenario 2: Vision + Stack, No Specs

**State**: why.md and stack.md exist, no specs

**Analysis**:
- Pillar 1 (Vision): ✅ Complete
- Pillar 2 (Understand): ✅ Complete
- Pillar 3 (Co-design): ❌ Missing
- Pillar 4 (Execute): ❌ Not started
- Pillar 5 (Document): ❌ Missing

**Recommendation**:
```
Run: /lite-spec

Why: You know your vision and tech stack. Time to plan your first feature.

What this accomplishes:
- Pillar 3: Co-design initiated
- Outcome: Clear feature spec guides implementation
```

---

## Scenario 3: Code Exists, No Docs

**State**: Source code in src/, no implementations.md

**Analysis**:
- Pillar 1 (Vision): ✅ Complete
- Pillar 2 (Understand): ✅ Complete
- Pillar 3 (Co-design): ✅ Complete (2 specs, 2 plans)
- Pillar 4 (Execute): ⏳ In Progress
- Pillar 5 (Document): ❌ Missing (no implementations.md)

**Recommendation**:
```
Run: /lite-component-knowledge

Why: You've built components but haven't documented them.
     Document now (2 min) vs trying to remember later (20 min).

What this accomplishes:
- Pillar 5: Document current state
- Outcome: Future you (or teammates) can understand your code

Alternative Paths:
- Continue building: /lite-implement (if rushing)
- Ship current feature: /lite-quality-confidence
```

---

## Scenario 4: Spec Exists, No Plan

**State**: specs/active/recipe-sharing.md exists, no plan

**Analysis**:
- Pillar 3 (Co-design): ⏳ Partial (spec exists, plan missing)

**Recommendation**:
```
Run: /lite-plan

Why: You have a spec but no implementation plan.
     Planning helps break work into manageable tasks.

What this accomplishes:
- Pillar 3: Co-design complete
- Outcome: Clear roadmap from spec to implementation
```

---

## Scenario 5: Missing Dependencies Warning

**State**: User just ran /lite-plan but no spec exists

**Recommendation**:
```
Run: /lite-spec

⚠️  Note: You created a plan without a spec. Consider creating
          a spec first for better alignment.

Why: Plans work best when based on clear specifications.

What this accomplishes:
- Pillar 3: Proper co-design flow (spec → plan)
- Outcome: Implementation has clear requirements

Alternative Paths:
- Proceed anyway: /lite-implement (use plan as-is)
```

---

## Scenario 6: Just Completed Implementation

**State**: User just completed /lite-implement, code works

**Analysis**:
- Pillar 4 (Execute): ✅ Complete for this feature
- Pillar 5 (Document): ⚠️ Partial (implementations.md may be stale)

**Recommendation**:
```
Run: /lite-component-knowledge

Why: Document what you just built while it's fresh in your mind.
     Knowledge capture is easiest immediately after implementation.

What this accomplishes:
- Pillar 5: Update implementations.md with new components
- Outcome: Team/future-you knows what was built and how it works

Alternative Paths:
- Quality check first: /lite-quality-confidence (verify before documenting)
- Log session: /lite-work-memory (capture progress before ending)
```

---

## Scenario 7: UX Inconsistency Detected

**State**: User built multiple features with different UX patterns

**Analysis**:
- Pillar 3 (Co-design): ⚠️ UX patterns diverging
- Pillar 5 (Quality): ⚠️ Coherence issues

**Recommendation**:
```
Run: /lite-ux-coherence

Why: Inconsistent UX confuses users. Early detection prevents
     costly refactoring later.

What this accomplishes:
- Pillar 5: Quality check for UX consistency
- Outcome: Unified interaction patterns across features

Alternative Paths:
- Document first: /lite-component-knowledge (capture current state)
- Continue building: Accept technical debt for speed
```

---

## Scenario 8: Spec Exists, UI Uncertain

**State**: Spec exists for UI-heavy feature, user unsure about interaction design

**Analysis**:
- Pillar 3 (Co-design): ⏳ Partial (spec exists, UI untested)
- Pillar 4 (Execute): ❌ Not started (risky to implement without validation)

**Recommendation**:
```
Run: /lite-prototyping

Why: Building UI without validation wastes time on wrong approaches.
     Rapid prototyping validates interactions before committing to code.

What this accomplishes:
- Pillar 3: UI/UX validated through user feedback
- Outcome: Confident direction for implementation

Alternative Paths:
- Skip prototyping: /lite-plan (proceed directly to implementation)
- Get UX guidance: /lite-ux-coherence (design patterns first)
```


---

## Scenario 9: Prototype Complete, Ready to Document

**State**: Prototype iteration complete, user satisfied with UI/UX direction

**Analysis**:
- Pillar 3 (Co-design): ✅ UI validated (prototype exists)
- Pillar 3 (Co-design): ⏳ Learnings not yet documented
- Pillar 4 (Execute): ❌ Not started (ready to plan implementation)

**Recommendation**:
```
Run: /lite-prototype-to-spec

Why: Prototype learnings (what worked, what didn't) are valuable.
     Extract them to spec before prototype is deleted or forgotten.

What this accomplishes:
- Pillar 3: Validated UI patterns preserved in spec
- Outcome: Implementation has clear UI/UX guidance

Next Steps After Extraction:
- Plan implementation: /lite-plan (uses updated spec with UI patterns)
- Delete prototype: rm -rf .shipkit-mockups/[name]/ (after extraction)

Alternative Paths:
- Keep prototype as reference: Leave in .shipkit-mockups/ during implementation
- Skip extraction: Proceed to /lite-plan (risk losing UI insights)
```

---
