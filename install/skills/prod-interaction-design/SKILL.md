---
name: prod-interaction-design
description: "Use when defining user journeys, interaction patterns, and product flows"
---

# Interaction Design

## Agent Persona

**Load:** `.claude/agents/discovery-agent.md`

Adopt: User-centric thinking, maps complete journeys not just features, focuses on user emotions and behaviors.

## Purpose

Define how users interact with the product through journey mapping, interaction patterns, and screen flows. This bridges the gap between what users need (from personas and JTBD) and how they'll actually use the product.

## When to Trigger

User says:
- "How will users navigate this?"
- "Map out the user flow"
- "Design the user experience"
- "What's the interaction design?"
- "Create user journeys"

Or when:
- Personas and JTBD are defined
- Ready to design the product experience
- Need to visualize how users move through product
- Designing onboarding or key workflows

## Prerequisites

**Required:**
- Brand guidelines defined (`.shipkit/skills/prod-brand-guidelines/outputs/brand-guidelines.md`)
  - Need brand personality to inform interaction style
  - Visual direction guides UI patterns

**Recommended (provides context):**
- Personas (who we're designing for)
- Jobs-to-be-done (what they're trying to accomplish)
- Market analysis (how competitors solve this)

## Inputs

- **Personas:** Who are the users and what motivates them?
- **JTBD:** What job is the user hiring the product to do?
- **Brand guidelines:** What tone and personality should interactions have?
- **Product stage:** POC / MVP / Established (affects scope)
- **Platform:** Web / Mobile / Desktop (affects patterns)

## Process

### 1. Run the Script

```bash
.shipkit/skills/prod-interaction-design/scripts/create-journey.sh
```

This initializes the interaction design document from template.

### 2. Define Design Philosophy

**Ask the user:**
- "What are the core principles that should guide all interactions?"
- "What do we optimize for?" (Speed? Simplicity? Delight? Power?)
- "What do we NOT optimize for?" (Feature count? Complexity?)

**Common principles:**
- Simplicity over features
- User goals over business goals
- Clear feedback at every step
- Reduce cognitive load
- Build trust through consistency

### 3. Map User Journeys (One per Persona)

For each persona from `personas.md`, map their complete journey:

**Stage 1: Awareness / Discovery**
- How do they find the product?
- What problem are they experiencing?
- What questions do they have?
- What makes them explore further?

**Stage 2: Consideration / Evaluation**
- What information do they need?
- What alternatives are they comparing?
- What objections arise?
- What tips them toward "yes"?

**Stage 3: First Use / Onboarding**
- What are critical first actions?
- How quickly can they reach value? (Target: <5 min for POC/MVP)
- What's the "aha!" moment?
- Where might they get stuck?
- Where might they abandon?

**Stage 4: Regular Use / Habit Formation**
- What are the core workflows?
- How does this fit into their daily routine?
- What triggers usage?
- What rewards keep them coming back?

**Stage 5: Power Use / Mastery**
- What advanced features do they discover?
- How do they customize and optimize?
- What shortcuts and bulk actions matter?

**Stage 6: Retention / Engagement**
- How do we keep them engaged long-term?
- How do we re-engage if they lapse?
- What new value can we provide?

**Stage 7: Advocacy / Referral**
- What makes them excited to share?
- How do we make sharing easy?
- What would they say to recommend it?

### 4. Define Interaction Patterns

Document reusable patterns that create consistency:

**Navigation:**
- Primary nav structure
- How users move between sections
- Breadcrumbs, back buttons, deep linking

**Input Patterns:**
- Forms (layout, validation, error handling)
- Search (placement, suggestions, filters)
- Bulk actions (selection, operations)

**Feedback Patterns:**
- Loading states (skeletons, progress indicators)
- Success confirmation (toasts, animations)
- Error handling (prevention, messages, recovery)
- Empty states (first use, no results)

**Content Patterns:**
- Lists vs. cards vs. tables
- Progressive disclosure (expand/collapse)
- Contextual actions (hover, swipe, right-click)

### 5. Map Critical Screen Flows

For 3-5 most important flows, document screen-by-screen:

**Example: Sign Up → First Value**
```
Landing Page
  ↓
Sign Up (minimal fields)
  ↓
Onboarding Step 1 (quick setup)
  ↓
Onboarding Step 2 (optional, can skip)
  ↓
First Value Screen (user achieves something)
  ↓
Core Product Experience
```

For each screen, specify:
- Purpose (what this screen accomplishes)
- Key elements (what's on screen)
- User actions (what they can do)
- Transitions (where they go next)
- Estimated time
- Drop-off risks

### 6. Consider Context

**For POC Stage:**
- Focus on core value (< 5 minutes to "aha!")
- Minimal onboarding (1-2 steps max)
- Defer: Polish, animations, advanced features
- Manual workarounds acceptable

**For MVP Stage:**
- Complete happy path flows
- Essential error handling
- Basic onboarding (3-5 steps)
- Still defer: Power features, extensive customization

**For Established Products:**
- Full feature set with progressive disclosure
- Comprehensive error handling
- Accessibility compliance
- Power user optimizations

**Platform Considerations:**
- **Mobile:** Thumb zones, gestures, one-handed use
- **Desktop:** Keyboard shortcuts, hover states, multi-tasking
- **Web:** Browser compatibility, responsive breakpoints

### 7. Accessibility & Usability

**Accessibility Checklist:**
- [ ] Color contrast meets WCAG AA (4.5:1)
- [ ] All actions keyboard-accessible
- [ ] Screen reader friendly (semantic HTML, ARIA)
- [ ] Touch targets minimum 44x44pt
- [ ] Works with text at 200% zoom

**Usability Principles:**
- Minimize cognitive load (progressive disclosure, defaults)
- Provide clear feedback (immediate acknowledgment)
- Design for errors (prevention, validation, undo)
- Maintain consistency (visual, behavioral, terminology)
- Prioritize ruthlessly (one primary action per screen)

### 8. Define Validation Plan

**What to test:**
- Critical flows (sign up → first value, core use case)
- Error scenarios (what happens when things go wrong)
- Different user types (beginner vs. power user)

**How to test:**
- Moderated usability testing (5-8 users per persona)
- Unmoderated remote testing (10-20 users)
- First-click testing (navigation validation)
- A/B testing (optimize existing flows)

**Metrics to track:**
- Time to first value
- Task completion rate (target: >90%)
- Feature adoption (% using within 30 days)
- User satisfaction (SUS score)

## Outputs

- `.shipkit/skills/prod-interaction-design/outputs/interaction-design.md`

This comprehensive document includes:
- Design philosophy and principles
- Complete user journeys for each persona
- Reusable interaction patterns
- Critical screen flows
- Accessibility specifications
- Validation plan

## Constraints

- **DO NOT** create interaction-design.md manually
- **ALWAYS** use the create-journey.sh script
- **MUST** have brand guidelines completed first (informs interaction style)
- **MUST** map complete journeys (all 7 stages), not just happy paths
- **FOCUS** on user emotions and behaviors, not just screens and clicks

## Quality Checks

Before marking complete, verify:
- [ ] Mapped journey for each key persona
- [ ] Included all 7 journey stages (awareness → advocacy)
- [ ] Documented emotion valleys (frustration) and peaks (delight)
- [ ] Defined "aha!" moment and time to reach it
- [ ] Specified drop-off risks and mitigations
- [ ] Created reusable interaction patterns
- [ ] Mapped 3-5 critical screen flows
- [ ] Considered mobile vs. desktop differences
- [ ] Included accessibility requirements
- [ ] Defined validation/testing plan

## Next Steps

After interaction design is complete:
- **→ /prod-user-stories** - Convert journeys into actionable requirements

## Context

This is **Step 7 of 12** in the Product Discovery sequential workflow.

## Tips

**Focus on the User's Reality:**
- Don't assume they understand your product
- Don't assume they have time to learn
- Don't assume they're on a perfect device with perfect connection
- Map what they actually do, not what you wish they'd do

**Capture Emotions:**
- Where do they feel confused? Frustrated? Delighted? Accomplished?
- Emotion valleys are improvement opportunities
- Emotion peaks are what creates advocates

**Design for Errors:**
- Happy path is 10% of design
- Error handling is 90%
- Map: What can go wrong? How do we prevent it? How do we recover?

**Progressive Disclosure:**
- Show users what they need, when they need it
- Don't overwhelm with all features upfront
- Reveal power gradually as they gain proficiency

**Mobile First (Usually):**
- Most users will try on mobile first
- Design for small screen, one hand, distractions
- Desktop can add richness, but core must work mobile

## Common Mistakes to Avoid

❌ **Feature lists disguised as journeys**
- Listing screens and buttons is not a journey
- Focus on user thoughts, feelings, actions

❌ **Happy path only**
- Real users encounter errors, get confused, abandon
- Map the valleys, not just the peaks

❌ **Skipping emotions**
- "User clicks button" → Missing the "why" and "how they feel"
- "User frantically searches for export, confused by format options" → Better

❌ **Designing for yourself**
- You know the product intimately
- Users don't. Design for their lack of context.

❌ **Starting with solutions**
- "We'll add a wizard!" before understanding the problem
- First map the struggle, then design the solution

## Read References

The skill includes extended references:
- `references/reference.md` - Journey mapping fundamentals, UX principles, testing methods
- `references/examples.md` - Complete journey examples for B2B SaaS, B2C mobile, e-commerce, dev tools

Review these for detailed guidance and patterns.
