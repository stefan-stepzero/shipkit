# User Persona Adaptations

If user specifies persona, adapt guidance accordingly.

---

## ADHD-Friendly

**Principles**:
- Minimize options (decision fatigue)
- One task at a time (focus)
- Clear progress indicators (motivation)
- Auto-save everything (working memory)
- No time limits (anxiety)
- Success feedback (dopamine)

**Example adaptations**:
- Multi-step form: 5 fields max per page, clear progress (step 2 of 4)
- Form auto-save: Save draft every 30 seconds
- Buttons: Large, high-contrast, clear labels (reduce decision fatigue)
- Feedback: Immediate success messages (dopamine hit)
- Timers: No countdown timers or "time remaining" warnings

---

## Elderly Users

**Principles**:
- Large text (18px minimum)
- High contrast (7:1 ratio)
- Simple language (no jargon)
- Large touch targets (48px minimum)
- Confirmation for all actions
- Undo for everything

**Example adaptations**:
- Text size: 18px body, 24px headings minimum
- Color contrast: 7:1 ratio (stricter than WCAG AA)
- Buttons: 48px × 48px minimum, clear labels
- Confirmations: "Are you sure?" for all actions
- Undo: Available for every change, visible for 10 seconds

---

## Mobile-First

**Principles**:
- Touch targets 44px minimum
- Thumb-friendly zones (bottom of screen)
- Swipe gestures (where appropriate)
- Avoid hover-only interactions
- Responsive breakpoints
- Mobile input types (tel, email)

**Example adaptations**:
- Navigation: Bottom tab bar (thumb-friendly)
- Modals: Bottom sheets on mobile (easier to reach)
- Buttons: 48px minimum touch targets
- Inputs: type="tel" for phone, type="email" for email
- Gestures: Swipe left to delete, pull to refresh
- No hover states: All actions available via tap

---

## Low-Bandwidth

**Principles**:
- Minimize images/media
- Loading skeletons (not live data)
- Offline support (service workers)
- Optimistic updates (immediate feedback)
- Progress indicators for uploads

**Example adaptations**:
- Images: Only essential, lazy-loaded, compressed
- Skeletons: Show layout immediately, load data progressively
- Offline: Service worker caches UI, syncs when online
- Uploads: Show progress bar, allow cancellation
- Data: Paginate results, load on demand

---

## Accessibility-First (Beyond WCAG AA)

**Principles**:
- Keyboard-only navigation must be efficient
- Screen reader support must be excellent
- Focus management must be predictable
- ARIA labels must be descriptive
- Color never the only indicator

**Example adaptations**:
- Keyboard shortcuts: Well-documented, visible hints
- Skip links: "Skip to main content" at top
- Focus indicators: 3px solid outline (extra visible)
- ARIA landmarks: nav, main, aside, footer
- Error messages: aria-live="assertive" for critical errors

---

**Remember**: Personas guide adaptations, but accessibility is always mandatory. Never compromise on keyboard navigation, screen readers, or WCAG AA compliance.
