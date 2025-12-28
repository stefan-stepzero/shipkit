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

**Based on component type, reference these principles**:

#### For Forms:
- Inline validation (validate as user types)
- Clear error messages (specific, actionable)
- Submit button states (default, loading, disabled, success)
- Field focus management (auto-focus first field)
- Progressive disclosure (show fields only when needed)
- Mobile-friendly input types (email, tel, number)

#### For Modals:
- Escape key to close
- Focus trap (tab stays within modal)
- Backdrop click to close (or disable if destructive)
- Clear close button (X in corner)
- Heading for screen readers (aria-labelledby)
- Return focus to trigger element on close

#### For Toggles/Switches:
- Immediate feedback (no "save" button needed)
- Loading state while processing
- Success confirmation (toast or inline)
- Undo option for reversible actions
- Confirmation for destructive actions
- Clear labels (not just on/off)

#### For Lists:
- Empty states (friendly message + CTA)
- Loading skeletons (not spinners)
- Virtualization for >100 items
- Infinite scroll vs pagination (choose based on use case)
- Optimistic updates (immediate feedback)
- Clear item actions (visible on hover/focus)

#### For Buttons:
- Loading states (spinner + disabled)
- Disabled states (low opacity + cursor)
- Success feedback (checkmark or toast)
- Destructive confirmation (modal or inline)
- Touch target 44px minimum (mobile)
- Clear label (not just icon)

---

## Core UX Principles (Progressive Disclosure)

**Share only principles relevant to user's specific component.**

### 1. Cognitive Load Reduction
**When to mention**: Forms, multi-step workflows, complex UIs

**Principles**:
- Minimize decisions user must make
- Progressive disclosure (show advanced options only when needed)
- Sensible defaults (pre-fill when possible)
- Chunking (group related fields/actions)
- One primary action per screen

**Example guidance**:
"Use progressive disclosure: show basic fields first, 'Advanced options' link reveals rest. Reduces cognitive load for 80% of users who need simple flow."

---

### 2. Immediate Feedback
**When to mention**: Forms, toggles, buttons, async actions

**Principles**:
- Visual feedback within 100ms of action
- Loading states for >200ms operations
- Success confirmations (visual or auditory)
- Error messages immediately (don't wait for submit)
- Optimistic updates (assume success, rollback if fails)

**Example guidance**:
"Toggle should update UI immediately (optimistic update), show spinner during API call, toast confirmation on success. User knows action is processing, not wondering if click registered."

---

### 3. Reversibility
**When to mention**: Destructive actions, settings, toggles

**Principles**:
- Undo option for destructive actions
- Confirmation modals for irreversible actions
- Soft deletes (archive, don't permanently delete)
- Draft auto-save (preserve user work)
- "Are you sure?" for high-impact changes

**Example guidance**:
"Delete button should: 1) Show confirmation modal, 2) Soft delete (archive), 3) Show toast with 'Undo' action for 5 seconds. Prevents accidental data loss."

---

### 4. Consistency
**When to mention**: Any component where similar pattern exists

**Principles**:
- Match existing patterns in implementations.md
- Consistent terminology across app
- Consistent button placement (primary right, secondary left)
- Consistent icon usage (same icon = same meaning)
- Consistent color semantics (red = danger, green = success)

**Example guidance**:
"You've used inline switches for NotificationToggle (implementations.md). Reuse that pattern here for consistency. Users learn once, apply everywhere."

---

### 5. Accessibility (WCAG 2.1 AA Minimum)
**When to mention**: ALWAYS include basic accessibility checklist

**Principles**:
- Keyboard navigation (tab, enter, escape)
- Screen reader support (aria-labels, roles)
- Focus management (visible focus indicators)
- Color contrast 4.5:1 minimum (text)
- Touch targets 44px minimum (mobile)
- No text in images (use alt text)
- Semantic HTML (button, not div)

**Example accessibility checklist**:
```
Accessibility Requirements:
- aria-label="[Descriptive label]"
- Keyboard: Tab to focus, Enter to activate, Escape to close
- Focus indicator: 2px solid outline
- Color contrast: 4.5:1 minimum
- Touch target: 44px × 44px minimum
- Screen reader: Announces state changes
```

---

### 6. Error Prevention
**When to mention**: Forms, destructive actions, critical flows

**Principles**:
- Inline validation (before submit)
- Input constraints (maxLength, pattern)
- Clear format requirements (email, phone)
- Disable invalid submissions (button disabled until valid)
- Helpful error messages (not "Invalid input")

**Example guidance**:
"Email field should: validate format on blur, show error inline (not on submit), disable submit until valid email entered. Prevents user frustration from submitting invalid form."

---

### 7. Mobile-First Design
**When to mention**: Responsive components, touch interactions

**Principles**:
- Touch targets 44px minimum
- Thumb-friendly zones (bottom of screen)
- Swipe gestures (where appropriate)
- Avoid hover-only interactions
- Responsive breakpoints (mobile → tablet → desktop)
- Mobile-friendly input types (email, tel, date)

**Example guidance**:
"Bottom sheet instead of modal on mobile (thumb-friendly). Touch target 48px for close button. Swipe down to dismiss (in addition to close button)."

---

## Common Pattern Guidance (Inline Reference)

**Share only the pattern user is asking about.**

### Forms Pattern
```
Best Practices:
✓ Inline validation (on blur, not on change)
✓ Clear error messages ("Email must include @" not "Invalid")
✓ Submit button states:
  - Default: Enabled with primary color
  - Validating: "Checking..." + disabled
  - Invalid: Disabled with tooltip explaining why
  - Submitting: Spinner + "Saving..."
  - Success: Checkmark + redirect OR toast
✓ Field focus: Auto-focus first field on mount
✓ Enter to submit (when all fields valid)
✓ Progressive disclosure: Show advanced fields only when needed

Accessibility:
- Label every input (visible or aria-label)
- Error messages linked to fields (aria-describedby)
- Required fields: aria-required="true"
- Invalid fields: aria-invalid="true"
```

### Modal Pattern
```
Best Practices:
✓ Escape key to close
✓ Focus trap (tab cycles within modal)
✓ Backdrop click closes (unless destructive action)
✓ Clear close button (X in top-right)
✓ Return focus to trigger on close
✓ Max-width for readability (600px typical)
✓ Scroll content, not entire modal

Accessibility:
- role="dialog"
- aria-labelledby="[modal-heading-id]"
- aria-modal="true"
- Focus first interactive element on open
- Visible focus indicators
```

### Toggle/Switch Pattern
```
Best Practices:
✓ Immediate visual feedback (optimistic update)
✓ Loading state while API call pending
✓ Success confirmation (toast or inline checkmark)
✓ Error rollback (revert to previous state + show error)
✓ Clear label (not just on/off icons)
✓ Undo option (for reversible actions)
✓ Confirmation modal (for destructive actions)

Accessibility:
- role="switch"
- aria-checked="true|false"
- aria-label="[What this toggles]"
- Keyboard: Space or Enter to toggle
- Screen reader announces state change
```

### List Pattern
```
Best Practices:
✓ Empty state (friendly message + "Add first item" CTA)
✓ Loading skeleton (not spinner for >3 items)
✓ Virtualization (for >100 items)
✓ Infinite scroll OR pagination (choose one):
  - Infinite: For feeds, social, exploration
  - Pagination: For tables, search results, archives
✓ Optimistic updates (add/edit immediately, rollback if fails)
✓ Item actions (visible on hover/focus)
✓ Sorting/filtering (if >20 items)

Accessibility:
- Semantic list markup (ul/ol or role="list")
- aria-label="[List description]"
- Keyboard navigation (arrow keys for focus)
- Screen reader announces item count
```

### Button Pattern
```
Best Practices:
✓ States:
  - Default: Clear label + icon (optional)
  - Hover: Slight color change
  - Active: Pressed appearance
  - Disabled: 50% opacity + cursor: not-allowed
  - Loading: Spinner + disabled + "Loading..."
  - Success: Checkmark + "Saved!" (2 seconds)
✓ Destructive actions: Red + confirmation
✓ Touch target: 44px minimum (mobile)
✓ Icon + text (not icon-only unless aria-label)

Accessibility:
- Semantic button element (not div)
- aria-label (if icon-only)
- aria-busy="true" (when loading)
- aria-disabled="true" (when disabled)
- Keyboard: Enter or Space to activate
```

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

## Integration with Other Skills

**Before ux-coherence-lite**:
- `/lite-spec` - Feature requirements (UI needs)
- `/lite-plan` - Implementation approach
- `/lite-project-context` - Stack info (UI framework)

**During ux-coherence-lite**:
- Reads `.shipkit-lite/implementations.md` - Existing patterns
- Reads `.shipkit-lite/architecture.md` - UX decisions

**After ux-coherence-lite**:
- `/lite-architecture-memory` - Log new pattern (if established)
- `/lite-implement` - Build using guidance
- `/lite-component-knowledge` - Document component

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

### Scenario 1: Building New Toggle

```
User: "I'm adding a share toggle to my recipe app"

Claude (ux-coherence-lite):
1. Ask: "Share as in public/private? Any UX concerns?"
2. Read .shipkit-lite/implementations.md
3. Find: NotificationToggle pattern exists
4. Output terminal guidance:
   - Use inline switch pattern (matches NotificationToggle)
   - Immediate feedback, loading state, undo
   - Accessibility checklist
   - "Reuse NotificationToggle pattern for consistency"
5. Append to .shipkit-lite/ux-decisions.md:
   ```
   ## ShareRecipeToggle - 2025-12-28
   Component Type: Toggle/Switch
   Pattern: Inline switch with optimistic updates
   Rationale: Matches existing NotificationToggle pattern for consistency
   Existing Match: NotificationToggle in implementations.md
   ```
6. Suggest: "Run `/lite-implement` to build"
```

### Scenario 2: New Pattern, No Existing Reference

```
User: "Building a drag-and-drop file uploader"

Claude (ux-coherence-lite):
1. Ask: "File size limits? Mobile support needed?"
2. Read .shipkit-lite/implementations.md (no similar pattern)
3. Output terminal guidance:
   - Drag-and-drop zone pattern
   - Click to upload fallback (accessibility)
   - File preview, progress bar, cancel option
   - Touch-friendly on mobile (large drop zone)
   - Accessibility: keyboard upload, screen reader announcements
4. Append to .shipkit-lite/ux-decisions.md:
   ```
   ## FileUploader - 2025-12-28
   Component Type: File Upload
   Pattern: Drag-and-drop zone with click fallback
   Rationale: Drag-and-drop is intuitive, click fallback ensures accessibility
   Existing Match: None (new pattern)
   ```
5. Suggest: "Log this as architectural pattern with `/lite-architecture-memory` if it becomes standard"
6. Then: "Run `/lite-implement` to build"
```

### Scenario 3: Accessibility-Focused Request

```
User: "Make this form ADHD-friendly"

Claude (ux-coherence-lite):
1. Read .shipkit-lite/implementations.md (existing form pattern?)
2. Output terminal guidance tailored to ADHD:
   - Minimize fields (5 max per page)
   - One question at a time (progressive disclosure)
   - Clear progress indicator (step 2 of 4)
   - Auto-save drafts (reduce working memory load)
   - Large, clear buttons (reduce decision fatigue)
   - No time limits (anxiety-inducing)
   - Success feedback (dopamine hit)
3. Append to .shipkit-lite/ux-decisions.md:
   ```
   ## OnboardingForm - 2025-12-28
   Component Type: Multi-step Form
   Pattern: Progressive disclosure with auto-save
   Rationale: ADHD-friendly design reduces cognitive load and anxiety
   User Persona Adaptation: ADHD-friendly
   ```
4. Suggest: "Log this ADHD-friendly pattern with `/lite-architecture-memory` if it becomes project-wide standard"
```

### Scenario 4: Checking Existing UI

```
User: "Review my modal implementation for UX issues"

Claude (ux-coherence-lite):
1. Ask: "Share the modal code or describe behavior?"
2. User shares code
3. Check against modal pattern:
   ✓ Escape key works
   ✓ Backdrop click closes
   ✗ No focus trap (tab escapes modal)
   ✗ Missing aria-labelledby
   ✗ Doesn't return focus on close
4. Output terminal guidance: "Fix these 3 issues: [specific code changes]"
5. Append to .shipkit-lite/ux-decisions.md:
   ```
   ## ProfileModal - 2025-12-28 (Review)
   Component Type: Modal
   Pattern: Standard modal with focus trap and ARIA
   Rationale: Fixing accessibility gaps in existing implementation
   Issues Fixed: Focus trap, aria-labelledby, focus return
   ```
6. Suggest: "Run `/lite-implement` to apply fixes"
```

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

**If user specifies persona, adapt guidance**:

### ADHD-Friendly:
- Minimize options (decision fatigue)
- One task at a time (focus)
- Clear progress indicators (motivation)
- Auto-save everything (working memory)
- No time limits (anxiety)
- Success feedback (dopamine)

### Elderly Users:
- Large text (18px minimum)
- High contrast (7:1 ratio)
- Simple language (no jargon)
- Large touch targets (48px minimum)
- Confirmation for all actions
- Undo for everything

### Mobile-First:
- Touch targets 44px minimum
- Thumb-friendly zones (bottom)
- Swipe gestures (where appropriate)
- Avoid hover-only interactions
- Responsive breakpoints
- Mobile input types (tel, email)

### Low-Bandwidth:
- Minimize images/media
- Loading skeletons (not live data)
- Offline support (service workers)
- Optimistic updates (immediate feedback)
- Progress indicators for uploads

**Adapt principles to persona, but maintain accessibility baseline.**

---

**Remember**: Good UX is invisible. Users shouldn't think about the interface - it should just work. When in doubt, choose the pattern that requires the least cognitive load and follows existing conventions.
