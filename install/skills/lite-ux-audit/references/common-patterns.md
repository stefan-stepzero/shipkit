# Common Pattern Guidance

Share only the pattern user is asking about.

---

## Forms Pattern

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

**Quick checklist for forms**:
- Inline validation (validate as user types)
- Clear error messages (specific, actionable)
- Submit button states (default, loading, disabled, success)
- Field focus management (auto-focus first field)
- Progressive disclosure (show fields only when needed)
- Mobile-friendly input types (email, tel, number)

---

## Modal Pattern

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

**Quick checklist for modals**:
- Escape key to close
- Focus trap (tab stays within modal)
- Backdrop click to close (or disable if destructive)
- Clear close button (X in corner)
- Heading for screen readers (aria-labelledby)
- Return focus to trigger element on close

---

## Toggle/Switch Pattern

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

**Quick checklist for toggles**:
- Immediate feedback (no "save" button needed)
- Loading state while processing
- Success confirmation (toast or inline)
- Undo option for reversible actions
- Confirmation for destructive actions
- Clear labels (not just on/off)

---

## List Pattern

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

**Quick checklist for lists**:
- Empty states (friendly message + CTA)
- Loading skeletons (not spinners)
- Virtualization for >100 items
- Infinite scroll vs pagination (choose based on use case)
- Optimistic updates (immediate feedback)
- Clear item actions (visible on hover/focus)

---

## Button Pattern

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

**Quick checklist for buttons**:
- Loading states (spinner + disabled)
- Disabled states (low opacity + cursor)
- Success feedback (checkmark or toast)
- Destructive confirmation (modal or inline)
- Touch target 44px minimum (mobile)
- Clear label (not just icon)

---

**Remember**: These are patterns, not rigid rules. Adapt to your specific use case while maintaining accessibility and consistency.
