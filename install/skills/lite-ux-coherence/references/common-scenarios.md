# Common UX Guidance Scenarios

Practical examples of how lite-ux-coherence works in different situations.

---

## Scenario 1: Building New Toggle

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

---

## Scenario 2: New Pattern, No Existing Reference

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

---

## Scenario 3: Accessibility-Focused Request

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

---

## Scenario 4: Checking Existing UI

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

**See main SKILL.md for the full UX guidance process and pattern checklists.**
