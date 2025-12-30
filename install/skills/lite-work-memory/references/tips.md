# Tips for Effective Session Logging

## Be specific

- "Added share button" → "Share button with copy-to-clipboard and success toast"
- "Fixed bug" → "Fixed Safari clipboard API fallback"
- "Updated API" → "Added token-based auth to share endpoint"

---

## Log decisions

- Document WHY, not just WHAT
- Future you will thank present you
- "Used UUID v4 because crypto.randomUUID() has better browser support than custom tokens"

---

## Track blockers honestly

- Don't hide problems
- Note impact: "Blocking deployment" vs "Nice to have"
- Include what's needed to unblock

---

## Make next steps actionable

- ❌ "Continue working on feature"
- ✅ "Implement POST endpoint, add validation, write integration test"

---

## Include file paths

- Absolute or relative (but consistent)
- Makes it easy to find code later
- Shows scope of changes

---

## Progress Log as Project History

**Over time, progress.md becomes**:
- Timeline of feature evolution
- Record of architectural decisions
- Log of blockers and resolutions
- Reference for "when did we do X?"
- Handoff document for new team members
- Evidence of progress for stakeholders

**You can grep/search this file** to answer:
- "When did we add dark mode?" → Search for "dark mode"
- "What was that auth decision?" → Search for "auth"
- "What's still in progress?" → Search for "🚧"
