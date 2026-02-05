---
name: shipkit-ux-audit
description: "Use when auditing implemented UI for missing UX patterns. Triggers: 'audit UX', 'check UX', 'missing patterns', 'UX gaps'."
argument-hint: "<component or area>"
allowed-tools:
  - Read
  - Glob
  - Grep
---

# shipkit-ux-audit - Lightweight UX Guidance

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
- Existing patterns documented: `.shipkit/implementations.md`
- Architecture decisions: `.shipkit/architecture.md`
- Stack info: `.shipkit/stack.md`

**No prerequisites required** - Can provide general guidance even for new projects.

---

## Process

### Step 0: Check for Queue (Auto-Detect Mode)

**First, check if running in queue-driven mode**:

Read file (if exists): `.shipkit/.queues/ux-audit-needed.md`

**If queue file exists and has pending items**:
1. Parse the `## Pending` section for components needing UX audit
2. For each pending component:
   - Audit loading states, error handling, accessibility (Step 2-4 logic)
   - Document findings in component documentation
   - Move item from Pending to Completed in queue
3. Skip Step 1 questions (components already identified)
4. Continue with Step 2-5 for each component

**If queue file doesn't exist or is empty**:
- Continue to Step 1 (manual mode - ask user what they're building)

---

### Step 1: (Manual Mode) Confirm What User is Building

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
.shipkit/implementations.md

# Architecture decisions about UX (if file exists)
.shipkit/architecture.md

# Tech stack (to know UI framework constraints)
.shipkit/stack.md
```

**Verification before claiming patterns:**

| Claim | Required Verification |
|-------|----------------------|
| "Similar pattern exists" | `Grep: pattern="[component type]" path="implementations.md"` returns matches |
| "No existing pattern" | Grep returns 0 matches for component type AND related keywords |
| "Established UX decision" | `Grep: pattern="[pattern name]" path="architecture.md"` returns match |

**Never claim** "no similar component" without actually grepping implementations.md.

**Auto-detect**:
- Similar components in implementations.md
- Established UX patterns in architecture.md
- UI framework from stack.md (React, Vue, Svelte, etc.)

**Token budget**: Keep context reading under 1500 tokens.

---

### Step 3: Generate UX Guidance

**Provide terminal output AND log to `.shipkit/ux-decisions.md`**.

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
- Run `/shipkit-architecture-memory` to log this pattern (if new)
- Run `implement (no skill needed)` when ready to build
```

---

### Step 4: Log UX Decision

**After providing terminal guidance, append decision to `.shipkit/ux-decisions.md`**:

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
- If `.shipkit/ux-decisions.md` doesn't exist, create with header:
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
- Inline validation, clear errors, submit button states, field focus, progressive disclosure

#### For Modals:
- Escape to close, focus trap, backdrop click, return focus, ARIA labels

#### For Toggles/Switches:
- Immediate feedback, loading state, undo option, confirmation for destructive

#### For Lists:
- Empty states, loading skeletons, virtualization, optimistic updates

#### For Buttons:
- Loading states, disabled states, success feedback, 44px touch target

**Apply relevant UX principles:**
1. **Cognitive Load Reduction** - Minimize choices, clear hierarchy, progressive disclosure
2. **Immediate Feedback** - Respond to every action within 100ms
3. **Reversibility** - Allow undo for destructive actions
4. **Consistency** - Match existing patterns in the project
5. **Accessibility** - WCAG 2.1 AA minimum (always required)
6. **Error Prevention** - Validate early, confirm destructive actions
7. **Mobile-First** - Touch targets 44px+, thumb zones, responsive design

---

## Step 6: Suggest Next Steps

---

## Completion Checklist

Copy and track:
- [ ] Reviewed implemented components
- [ ] Checked against UX pattern checklist
- [ ] Documented gaps and recommendations

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

- `/shipkit-spec` - Creates feature requirements
  - **When**: Spec defines UI components needed
  - **Why**: UX guidance shapes how specified features should work
  - **Trigger**: Spec mentions forms, modals, toggles, or other UI elements

- `/shipkit-plan` - Plans implementation approach
  - **When**: Plan describes UI component structure
  - **Why**: UX patterns inform component architecture choices
  - **Trigger**: Plan needs UX pattern decisions before implementation

- `/shipkit-project-context` - Generates stack information
  - **When**: Stack includes UI framework (React, Vue, Svelte)
  - **Why**: UX guidance references stack.md to understand UI framework capabilities
  - **Trigger**: Need to know what UI primitives are available

### After This Skill

- `/shipkit-architecture-memory` - Logs architectural decisions
  - **When**: UX pattern becomes project-wide standard
  - **Why**: Document established UX patterns for future consistency
  - **Trigger**: New pattern created that should be reused across components

- `implement (no skill needed)` - Implements components
  - **When**: UX guidance complete, ready to build
  - **Why**: Implementation follows UX patterns and accessibility requirements
  - **Trigger**: User confirms "ready to implement"

- `document components manually` - Documents components
  - **When**: Component built and needs documentation
  - **Why**: Document UX decisions made for component
  - **Trigger**: Component complete, add to implementations.md

---

## Context Files This Skill Reads

**Optionally reads**:
- `.shipkit/implementations.md` - Existing UI components/patterns
- `.shipkit/architecture.md` - Past UX decisions
- `.shipkit/stack.md` - UI framework info

**Never reads**:
- Specs, plans, tasks (not relevant for UX guidance)

---

## Context Files This Skill Writes

**Writes to**:
- `.shipkit/ux-decisions.md` - Logs each UX decision with pattern, rationale, and accessibility requirements

**Write Strategy**: **APPEND** - Each UX decision is added to the end of the file, preserving full history.

**Why APPEND?**
- Historical record of UX patterns matters for consistency tracking
- Can reference past decisions to ensure new components follow established patterns
- Provides audit trail of why certain UX choices were made
- Each decision is independent and additive, never conflicts
- Other skills (like `implement (no skill needed)`) can read to understand established UX patterns

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
- `.shipkit/architecture.md` (via `/shipkit-architecture-memory`) - If UX decision becomes architectural pattern

---

## Lazy Loading Behavior

**This skill loads context on demand**:

1. User invokes `/shipkit-ux-audit`
2. Claude asks what component user is building
3. Claude optionally reads implementations.md (if exists) to check for similar patterns
4. Claude optionally reads architecture.md (if exists) for established UX decisions
5. Claude provides terminal guidance
6. Claude appends UX decision to `.shipkit/ux-decisions.md` (APPEND mode)
7. Total context: ~500-1500 tokens (focused)

**Not loaded**:
- Specs, plans, tasks, progress logs (not needed)

---

<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Has important context been saved to `.shipkit/`?
2. **Prerequisites** - Does the next action need a spec or plan first?
3. **Session length** - Long session? Consider `/shipkit-work-memory` for continuity.

**Natural capabilities** (no skill needed): Implementation, debugging, testing, refactoring, code documentation.

**Suggest skill when:** User needs to make decisions, create persistence, or check project status.
<!-- /SECTION:after-completion -->

<!-- SECTION:success-criteria -->
## Success Criteria

Guidance is complete when:
- [ ] User's component type identified
- [ ] Relevant UX principles shared (not all principles)
- [ ] Specific implementation checklist provided
- [ ] Accessibility requirements included
- [ ] Existing patterns referenced (if applicable)
- [ ] UX decision logged to `.shipkit/ux-decisions.md` (APPEND mode)
- [ ] Next steps suggested (implement or log architectural decision)
<!-- /SECTION:success-criteria -->
---

## Common Scenarios

- **Reusing existing patterns** - Check implementations.md first, reference existing components
- **Creating new patterns** - Provide guidance, suggest logging to architecture.md
- **Accessibility-focused requests** - Apply persona adaptations (see below)
- **Reviewing existing UI** - Audit against pattern checklists above

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

**Persona adaptations:**
- **ADHD-Friendly** - Minimize options, auto-save, no timers, clear success feedback
- **Elderly Users** - Large text/targets, high contrast, confirmations, easy undo
- **Mobile-First** - Touch targets 44px+, thumb zones, swipe gestures, no hover-only
- **Low-Bandwidth** - Minimize media, loading skeletons, offline support, optimistic updates
- **Accessibility-First** - Beyond WCAG AA: keyboard efficiency, excellent screen reader support

**Adapt principles to persona, but maintain accessibility baseline.**

---

---

**Remember**: Good UX is invisible. Users shouldn't think about the interface - it should just work. When in doubt, choose the pattern that requires the least cognitive load and follows existing conventions.