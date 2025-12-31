---
name: lite-pre-ship-check
description: Hidden detection skill that checks if UX audit is needed before shipping by analyzing interactive component count and implementations.md coverage. Auto-triggered before /lite-quality-confidence. System skill - not user-invocable.
---

# lite-pre-ship-check - Pre-Ship UX Audit Detection

**Purpose**: Automatically detect if UX audit is needed before shipping based on interactive component count and documentation coverage.

**Type**: System skill (hidden from users, auto-triggered)

**Trigger**: Before `/lite-quality-confidence` runs

---

## What This Skill Does

**Detection:**
1. Counts interactive components in codebase (forms, buttons with actions, data widgets)
2. Checks if `.shipkit-lite/implementations.md` exists and has UX notes
3. Determines if UX audit threshold met (default: 3+ interactive components)

**Queue Creation:**
1. If threshold met AND no recent UX audit, creates `.shipkit-lite/.queues/ux-audit-needed.md`
2. Lists components needing UX review (loading states, errors, accessibility, feedback)
3. Provides clear action items for `/lite-ux-audit`

**Output:**
- Queue file ready for `/lite-ux-audit` to process
- Terminal message suggesting UX audit before shipping

---

## Detection Logic

**Interactive component patterns:**
```python
INTERACTIVE_PATTERNS = {
    'forms': ['<form', 'onSubmit', 'handleSubmit'],
    'async_buttons': ['onClick.*async', 'loading', 'disabled'],
    'data_widgets': ['useEffect', 'fetch', 'loading'],
    'file_uploads': ['type="file"', 'upload', 'FileReader'],
}

THRESHOLD = 3  # Trigger UX audit if 3+ interactive components
```

**UX audit indicators:**
- Component has async operations (loading states needed)
- Component handles errors (error UI needed)
- Component accepts user input (validation, feedback needed)
- Component is user-facing (accessibility needed)

---

## Queue File Format

**Creates:** `.shipkit-lite/.queues/ux-audit-needed.md`

**Content:**
```markdown
# UX Audit Needed

**Created:** 2025-12-30 18:00
**Reason:** 5 interactive components detected, pre-ship check

## Components To Audit

- [ ] LoginForm
  - Location: src/components/LoginForm.tsx
  - Type: Form with async submit
  - Audit for: Loading state, error display, success feedback

- [ ] UserCard
  - Location: src/components/UserCard.tsx
  - Type: Interactive card with actions
  - Audit for: Loading states, disabled states, accessibility

...
```

---

## Script Location

**Detection script:** `scripts/check-ux-audit-needed.py`

**Usage:**
```bash
python scripts/check-ux-audit-needed.py [--threshold 3]
```

---

## Integration with Other Skills

### Before This Skill
- `/lite-implement` - Creates interactive components
- `/lite-component-knowledge` - Documents components

### After This Skill
- `/lite-ux-audit` - Audits components from queue
- `/lite-quality-confidence` - Runs after UX audit complete

---

## Context Files This Skill Reads

**Scans:**
- `src/components/**/*` - Component files
- `.shipkit-lite/implementations.md` - Check for UX documentation
- `.shipkit-lite/.queues/ux-audit-needed.md` - Check if audit already queued

---

## Context Files This Skill Writes

**Creates:**
- `.shipkit-lite/.queues/ux-audit-needed.md`

---

## Edge Cases

**Below threshold:**
- Don't create queue (< 3 interactive components)
- Proceed to quality checks without UX audit

**Already audited recently:**
- Check last audit date in implementations.md
- Don't re-audit if done in last 7 days

**Queue already exists:**
- Append new components, don't overwrite

---

**Remember**: Prevents shipping without UX review when significant interactive functionality exists.
