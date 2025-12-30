# Core UX Principles

Share only principles relevant to user's specific component.

---

## 1. Cognitive Load Reduction

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

## 2. Immediate Feedback

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

## 3. Reversibility

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

## 4. Consistency

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

## 5. Accessibility (WCAG 2.1 AA Minimum)

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

## 6. Error Prevention

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

## 7. Mobile-First Design

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
