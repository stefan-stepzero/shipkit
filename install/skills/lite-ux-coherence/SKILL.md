---
name: lite-ux-coherence
description: Provides UX guidance for consistent, user-friendly UI patterns by checking existing implementations and applying best practices. Use when user asks "what's the best UX pattern", "how should this UI work", or before building new UI components.
---

# ux-coherence-lite - Lightweight UX Guidance

**Purpose**: Ensures UI patterns stay consistent and user-friendly across the application by providing UX guidance based on general best practices, existing patterns in the project, and optional user-specified personas (e.g., ADHD-friendly, elderly users).

---

## When to Invoke

**User triggers**:
- "What's the best UX pattern for this?"
- "How should this UI work?"
- "UX guidance for [component]"
- "Make this accessible"
- "Check UX consistency"

**Before**:
- Building new UI components
- Implementing forms, modals, toggles, lists, buttons
- Creating user interactions

**During**:
- Reviewing implemented UI
- Refining user experience
- Fixing UX inconsistencies

---

## Prerequisites

**Optional but helpful**:
- Existing patterns documented: `.shipkit-lite/implementations.md`
- Architecture decisions: `.shipkit-lite/architecture.md`
- Stack info: `.shipkit-lite/stack.md`

**No prerequisites required** - Can provide general guidance even for new projects.

---

## Process

### Step 1: Confirm What User is Building

**Before providing guidance**, ask 2-3 questions:

1. **What UI element are you building?**
   - If not clear from user's message, ask specifically
   - Examples: "Form? Modal? Toggle? List? Button?"

2. **Any specific UX concerns or user needs?**
   - "Do you have specific accessibility requirements?"
   - "Any target user personas?" (e.g., ADHD-friendly, elderly users, mobile-first)
   - "Known constraints?" (e.g., must work offline, low bandwidth)

3. **Is this a new pattern or matching existing?**
   - "Have you built similar UI before in this project?"
   - Will check implementations.md to verify

**Why ask**: Tailor guidance to actual needs, not generic advice.

---

### Step 2: Read Existing Context

**Check for established patterns**:

```bash
# Existing UI patterns (if file exists)
.shipkit-lite/implementations.md

# Architecture decisions about UX (if file exists)
.shipkit-lite/architecture.md

# Tech stack (to know UI framework constraints)
.shipkit-lite/stack.md
```

**Auto-detect**:
- Similar components in implementations.md
- Established UX patterns in architecture.md
- UI framework from stack.md (React, Vue, Svelte, etc.)

**Token budget**: Keep context reading under 1500 tokens.

---

### Step 3: Generate UX Guidance

**Provide terminal output AND log to `.shipkit-lite/ux-decisions.md`**.

**Terminal output template**:

```
🎨 UX Guidance: [Component Name]

**Recommended Pattern**: [Pattern name and type]

**Why**: [1-2 sentence rationale based on principles below]

**Implementation Checklist**:
✓ [Specific implementation detail 1]
✓ [Specific implementation detail 2]
✓ [Specific implementation detail 3]
✓ [Accessibility requirement 1]
✓ [Accessibility requirement 2]

**Accessibility Notes**:
- [WCAG requirement 1]
- [WCAG requirement 2]
- [Keyboard interaction]
- [Screen reader consideration]

**[IF pattern exists in implementations.md]**
**Existing Pattern Match**: [ComponentName] in implementations.md
- Reuse: [specific pattern to follow]
- Location: [file path from implementations.md]

**[IF new pattern being established]**
**New Pattern**: This establishes a new pattern for your project
- Consider logging to architecture.md if this becomes standard

**Next Steps**:
- [Specific action 1]
- Run `/lite-architecture-memory` to log this pattern (if new)
- Run `/lite-implement` when ready to build
```

---

### Step 4: Log UX Decision

**After providing terminal guidance, append decision to `.shipkit-lite/ux-decisions.md`**:

```markdown
## [Component Name] - [Current Date]

**Component Type**: [Form/Modal/Toggle/List/Button/etc]
**Pattern**: [Specific pattern recommended]
**Rationale**: [Why this pattern was chosen - 1-2 sentences]
**Accessibility**: [Key WCAG requirements applied]
**Existing Match**: [Reference to similar component in implementations.md, if found]
**User Persona Adaptation**: [ADHD/Elderly/Mobile/etc, if user specified]

**Implementation Checklist**:
- [ ] [Key requirement 1]
- [ ] [Key requirement 2]
- [ ] [Accessibility requirement]

---
```

**File operation**:
- If `.shipkit-lite/ux-decisions.md` doesn't exist, create with header:
  ```markdown
  # UX Decisions Log

  This file tracks all UX guidance provided for components. Each entry documents the pattern chosen, rationale, and accessibility requirements.

  ---
  ```
- Then append the new decision entry
- Each entry is separated by `---`

**Why log this?**
- Creates historical record of UX patterns
- Other skills can reference established patterns
- Ensures consistency across components
- Provides audit trail for UX decisions

---

### Step 5: Apply Progressive Disclosure

**Only share relevant principles** - Don't dump entire UX knowledge base.

**Quick reference by component type**:

#### For Forms:
- See `references/common-patterns.md` → Forms Pattern
- Key: Inline validation, clear errors, submit button states, field focus, progressive disclosure

#### For Modals:
- See `references/common-patterns.md` → Modal Pattern
- Key: Escape to close, focus trap, backdrop click, return focus, ARIA labels

#### For Toggles/Switches:
- See `references/common-patterns.md` → Toggle Pattern
- Key: Immediate feedback, loading state, undo option, confirmation for destructive

#### For Lists:
- See `references/common-patterns.md` → List Pattern
- Key: Empty states, loading skeletons, virtualization, optimistic updates

#### For Buttons:
- See `references/common-patterns.md` → Button Pattern
- Key: Loading states, disabled states, success feedback, 44px touch target

**Apply relevant UX principles from** `references/ux-principles.md`:
1. Cognitive Load Reduction
2. Immediate Feedback
3. Reversibility
4. Consistency
5. Accessibility (WCAG 2.1 AA - always required)
6. Error Prevention
7. Mobile-First Design

---

## Step 6: Suggest Next Steps

**After providing guidance and logging decision, suggest**:

```
**Next Steps**:

[IF pattern exists in implementations.md]
1. Review [ExistingComponent] in implementations.md
2. Reuse that pattern for consistency
3. Run `/lite-implement` when ready to build

[IF new pattern]
1. Use the pattern above
2. Run `/lite-architecture-memory` to log this UX decision
   (Log: "[Pattern name] pattern for [component type]")
3. Run `/lite-implement` when ready to build

[IF integration needed]
- Run `/lite-integration-guardrails` if connecting to external service
- Run `/lite-data-consistency` if managing complex state

Ready to implement?
```

---

## What Makes This "Lite"

**Included**:
- ✅ General UX best practices (inline in SKILL.md)
- ✅ Common pattern guidance (forms, modals, toggles, lists, buttons)
- ✅ WCAG 2.1 AA accessibility basics
- ✅ Progressive disclosure (only relevant principles)
- ✅ Reads existing patterns from implementations.md
- ✅ Adapts to user personas (ADHD, elderly, etc. if specified)

**Not included** (vs full ux-coherence):
- ❌ No references/ folder (all guidance inline)
- ❌ No comprehensive UX library
- ❌ No design system templates
- ❌ No detailed research methodologies
- ❌ No usability testing frameworks
- ❌ No analytics integration

**Philosophy**: Provide good-enough UX guidance for POC/MVP, not comprehensive design system.

---

## When This Skill Integrates with Others

### Before This Skill

- `/lite-spec` - Creates feature requirements
  - **When**: Spec defines UI components needed
  - **Why**: UX guidance shapes how specified features should work
  - **Trigger**: Spec mentions forms, modals, toggles, or other UI elements

- `/lite-plan` - Plans implementation approach
  - **When**: Plan describes UI component structure
  - **Why**: UX patterns inform component architecture choices
  - **Trigger**: Plan needs UX pattern decisions before implementation

- `/lite-project-context` - Generates stack information
  - **When**: Stack includes UI framework (React, Vue, Svelte)
  - **Why**: UX guidance references stack.md to understand UI framework capabilities
  - **Trigger**: Need to know what UI primitives are available

### After This Skill

- `/lite-architecture-memory` - Logs architectural decisions
  - **When**: UX pattern becomes project-wide standard
  - **Why**: Document established UX patterns for future consistency
  - **Trigger**: New pattern created that should be reused across components

- `/lite-implement` - Implements components
  - **When**: UX guidance complete, ready to build
  - **Why**: Implementation follows UX patterns and accessibility requirements
  - **Trigger**: User confirms "ready to implement"

- `/lite-component-knowledge` - Documents components
  - **When**: Component built and needs documentation
  - **Why**: Document UX decisions made for component
  - **Trigger**: Component complete, add to implementations.md

---

## Context Files This Skill Reads

**Optionally reads**:
- `.shipkit-lite/implementations.md` - Existing UI components/patterns
- `.shipkit-lite/architecture.md` - Past UX decisions
- `.shipkit-lite/stack.md` - UI framework info

**Never reads**:
- Specs, plans, tasks (not relevant for UX guidance)

---

## Context Files This Skill Writes

**Writes to**:
- `.shipkit-lite/ux-decisions.md` - Logs each UX decision with pattern, rationale, and accessibility requirements

**Write Strategy**: **APPEND** - Each UX decision is added to the end of the file, preserving full history.

**Why APPEND?**
- Historical record of UX patterns matters for consistency tracking
- Can reference past decisions to ensure new components follow established patterns
- Provides audit trail of why certain UX choices were made
- Each decision is independent and additive, never conflicts
- Other skills (like `/lite-implement`) can read to understand established UX patterns

**Entry Format**:
```markdown
## [Component Name] - [Date]

**Component Type**: [Form/Modal/Toggle/List/Button/etc]
**Pattern**: [Specific pattern recommended]
**Rationale**: [Why this pattern was chosen]
**Accessibility**: [Key WCAG requirements applied]
**Existing Match**: [Reference to similar component in implementations.md, if any]
**User Persona Adaptation**: [ADHD/Elderly/Mobile/etc, if specified]

**Implementation Checklist**:
- [ ] [Key requirement 1]
- [ ] [Key requirement 2]
- [ ] [Accessibility requirement]

---
```

**Also suggests writing to**:
- `.shipkit-lite/architecture.md` (via `/lite-architecture-memory`) - If UX decision becomes architectural pattern

---

## Lazy Loading Behavior

**This skill loads context on demand**:

1. User invokes `/lite-ux-coherence`
2. Claude asks what component user is building
3. Claude optionally reads implementations.md (if exists) to check for similar patterns
4. Claude optionally reads architecture.md (if exists) for established UX decisions
5. Claude provides terminal guidance
6. Claude appends UX decision to `.shipkit-lite/ux-decisions.md` (APPEND mode)
7. Total context: ~500-1500 tokens (focused)

**Not loaded**:
- Specs, plans, tasks, progress logs (not needed)

---

## Success Criteria

Guidance is complete when:
- [ ] User's component type identified
- [ ] Relevant UX principles shared (not all principles)
- [ ] Specific implementation checklist provided
- [ ] Accessibility requirements included
- [ ] Existing patterns referenced (if applicable)
- [ ] UX decision logged to `.shipkit-lite/ux-decisions.md` (APPEND mode)
- [ ] Next steps suggested (implement or log architectural decision)

---

## Common Scenarios

**See `references/common-scenarios.md` for detailed examples:**
- Scenario 1: Building New Toggle (reusing existing pattern)
- Scenario 2: New Pattern, No Existing Reference (file uploader)
- Scenario 3: Accessibility-Focused Request (ADHD-friendly form)
- Scenario 4: Checking Existing UI (modal review)

---

## Tips for Effective UX Guidance

**Be specific**:
- "Use Switch component with aria-checked" (not "make it accessible")
- "44px touch target" (not "mobile-friendly")
- "Toast with undo for 5 seconds" (not "allow reversal")

**Reference existing patterns**:
- Check implementations.md first
- Reuse patterns when applicable
- Only create new patterns when necessary

**Progressive disclosure**:
- Share only relevant principles (not all 7)
- Focus on component-specific guidance
- Don't overwhelm with theory

**Accessibility is not optional**:
- Always include basic WCAG checklist
- Keyboard navigation always required
- Screen reader support always required

**When to defer to full /ux-coherence**:
- Complex design systems
- Multi-platform consistency (web + mobile apps)
- Comprehensive accessibility audits
- User research and testing
- Advanced interaction patterns

---

## User Persona Adaptations

**When user specifies a persona, adapt guidance accordingly.**

**See `references/persona-adaptations.md` for detailed adaptations:**
- ADHD-Friendly (minimize options, auto-save, no timers, success feedback)
- Elderly Users (large text/targets, high contrast, confirmations, undo)
- Mobile-First (touch targets, thumb zones, swipe gestures, no hover-only)
- Low-Bandwidth (minimize media, skeletons, offline support, optimistic updates)
- Accessibility-First (beyond WCAG AA: keyboard efficiency, excellent screen reader support)

**Adapt principles to persona, but maintain accessibility baseline.**

---

## Reference Documentation

**This skill provides detailed guidance in reference files:**

**UX Patterns & Principles:**
- `references/ux-principles.md` - 7 core UX principles (Cognitive Load, Immediate Feedback, Reversibility, Consistency, Accessibility, Error Prevention, Mobile-First)
- `references/common-patterns.md` - UI pattern checklists (Forms, Modals, Toggles, Lists, Buttons)

**Practical Guidance:**
- `references/common-scenarios.md` - 4 UX guidance scenarios with examples
- `references/persona-adaptations.md` - 5 persona-specific adaptations (ADHD, Elderly, Mobile-First, Low-Bandwidth, Accessibility-First)

**How to use references:**
- Main SKILL.md provides the process workflow
- Reference files provide detailed patterns, principles, and examples
- Progressive disclosure: Only share relevant sections based on user's component type
- Keep guidance focused and actionable

---

**Remember**: Good UX is invisible. Users shouldn't think about the interface - it should just work. When in doubt, choose the pattern that requires the least cognitive load and follows existing conventions.
