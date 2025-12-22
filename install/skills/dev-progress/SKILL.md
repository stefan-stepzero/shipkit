---
name: dev-progress
description: "Track development progress through roadmap at spec level. Auto-called by dev-finish after merge. Updates living progress document showing completed/current/next specs."
agent: dev-lead
---

# Development Progress Tracking

**Spec-level progress tracking through the development roadmap.**

---

## Overview

Maintains a living progress document that tracks which specs are complete, which is current, and what's next. Automatically updated after each spec completes.

**Core principle:** Spec-level tracking only. Claude Code handles task execution.

**Auto-called by:** `/dev-finish` after successful merge

---

## When to Use

**Auto-trigger:**
- Called automatically by `/dev-finish` after merge (Option 1)

**Manual trigger:**
- User says: "Show progress", "Where are we?", "What's the status?"
- `/dev-progress` (re-scans current state)

**Don't use if:**
- No roadmap exists (nothing to track against)
- Single-feature project (no roadmap needed)

---

## Prerequisites

**Required:**
- Roadmap exists (`.shipkit/skills/dev-roadmap/outputs/roadmap.md`)

**Optional:**
- Specs directory (`.shipkit/skills/dev-specify/outputs/specs/`)

---

## Process

### Step 1: Run Update Script

```bash
.shipkit/skills/dev-progress/scripts/update-progress.sh
```

**Script:**
1. Reads roadmap.md to get spec list
2. Scans git history for merged spec branches
3. Checks which spec directories exist
4. Determines current spec (exists but not merged)
5. Updates progress.md

---

### Step 2: Scan Current State

**Claude analyzes:**

1. **Roadmap:** What specs are planned?
2. **Git:** What branches are merged?
3. **Spec dirs:** What specs exist in `.shipkit/skills/dev-specify/outputs/specs/`?
4. **Current work:** Which spec exists but isn't merged yet?

**Determine status:**
- ✅ **Completed:** Spec directory exists AND branch merged
- 🔄 **In Progress:** Spec directory exists but NOT merged
- 📋 **Next Up:** No spec directory, next in roadmap sequence
- 📋 **Queued:** No spec directory, later in roadmap

---

### Step 3: Update Progress Document

**Write to:**
```
.shipkit/skills/dev-progress/outputs/progress.md
```

**Format:**
```markdown
# Development Progress

**Last Updated:** 2025-12-22 14:30
**Overall:** 2/6 specs complete (33%)

---

## Completed ✅

### Spec 1: Core Infrastructure
- ✅ Merged: 2025-12-15
- Location: specs/1-core-infrastructure/
- Branch: feature/core-infrastructure (merged to main)

### Spec 2: User Authentication
- ✅ Merged: 2025-12-20
- Location: specs/2-user-authentication/
- Branch: feature/user-auth (merged to main)

---

## Current 🔄

### Spec 3: User Dashboard
- 🔄 Status: In development
- Location: specs/3-user-dashboard/
- Branch: feature/dashboard (active)
- Started: 2025-12-21

---

## Next Up 📋

### Spec 4: External Payment Integration
**From roadmap:** High technical risk - validate early
**User Stories:** US-007
**Dependencies:** Spec 1, Spec 2

### Spec 5: Reporting
**From roadmap:** Independent of other features
**User Stories:** US-010, US-011
**Dependencies:** Spec 1, Spec 2

### Spec 6: Admin Panel
**From roadmap:** Uses UI patterns from Spec 3
**User Stories:** US-015, US-016
**Dependencies:** Spec 1, Spec 2, Spec 3

---

## Summary

- **Completed:** 2 specs
- **In Progress:** 1 spec
- **Remaining:** 3 specs
- **Total:** 6 specs
- **Progress:** 33%

---

## Next Action

**Continue current spec:**
```bash
/dev-implement  # Continue Spec 3 tasks
```

**Or if current spec done, start next:**
```bash
/dev-specify "External Payment Integration (US-007)"
```
```

---

### Step 4: Report to User

**After update, show:**
1. Progress summary (X/Y complete)
2. What just finished (if called from dev-finish)
3. What's current (if any)
4. What's next in roadmap
5. Suggested next action

**Example output:**
```
✅ Progress updated!

Spec 2: User Authentication → Complete (merged 2025-12-20)

Progress: 2/6 specs complete (33%)

Next: Spec 3 - User Dashboard (US-003, US-004, US-005)

Ready to start?
Run: /dev-specify "User Dashboard (US-003, US-004, US-005)"
```

---

## How It Works with dev-finish

**Integration flow:**

```bash
/dev-finish
  → Tests verified
  → User chooses Option 1 (merge to main)
  → Code merged successfully
  → Check: Does roadmap.md exist?
  → YES: Auto-call /dev-progress
  → Update progress.md
  → Show: "2/6 complete. Next: Spec 3"
  → Suggest: /dev-specify "Spec 3: ..."
```

**dev-finish will:**
1. Complete merge
2. Check for roadmap
3. If roadmap exists → invoke `/dev-progress`
4. Show updated progress
5. Suggest next spec

---

## Detection Logic

### How to determine "completed"

**A spec is completed when:**
1. Spec directory exists: `.shipkit/skills/dev-specify/outputs/specs/N-feature-name/`
2. **AND** branch is merged to main

**Check via git:**
```bash
# Check if feature branch exists in git history
git log --all --grep="Merge.*feature/user-auth"

# Or check if spec directory exists and branch doesn't exist anymore (merged and deleted)
git branch -a | grep "feature/user-auth" || echo "merged"
```

---

### How to determine "current"

**A spec is current when:**
1. Spec directory exists
2. **AND** branch is NOT merged yet
3. **AND** it's the earliest incomplete spec in roadmap sequence

**Check via:**
- Spec directory exists: `ls specs/3-user-dashboard/`
- Branch exists: `git branch | grep feature/dashboard`
- Not merged: no merge commit in git log

---

### How to determine "next"

**Next spec is:**
1. First spec in roadmap that has no directory yet
2. **OR** if current spec exists, the next one in sequence after current

**Logic:**
```
Roadmap says: Spec 1, 2, 3, 4, 5, 6
Completed: 1, 2
Current: 3 (exists, not merged)
Next: 4 (when 3 completes)
```

---

## Simple Progress Calculation

```
Completed Specs / Total Specs in Roadmap = Progress %

Example:
2 completed / 6 total = 33%
```

**Only count merged specs as complete.**

---

## Constraints

**DO:**
- ✅ Track at spec level only
- ✅ Use git history to determine completion
- ✅ Show clear "completed/current/next" sections
- ✅ Suggest next action
- ✅ Keep document simple and scannable

**DON'T:**
- ❌ Track individual tasks (Claude Code handles that)
- ❌ Calculate velocity or estimates (not project management)
- ❌ Create burndown charts (overkill)
- ❌ Track time spent (out of scope)
- ❌ Show too much detail (keep it high-level)

---

## Edge Cases

### No roadmap exists
**Action:** Don't create progress document. Suggest creating roadmap first.

### Specs built out of roadmap order
**Action:** Show what's complete, note divergence from roadmap.
```
Note: Spec 4 completed before Spec 3 (out of roadmap order)
```

### Multiple specs in progress
**Action:** List all in-progress specs in "Current" section.

### Roadmap updated mid-project
**Action:** Re-scan and update progress against new roadmap.

---

## Example: E-commerce Project

**Roadmap has 9 specs.**

**After Spec 2 completes:**

```markdown
# Development Progress

**Last Updated:** 2025-12-22
**Overall:** 2/9 specs complete (22%)

## Completed ✅
- Spec 1: Core Infrastructure (merged 2025-12-10)
- Spec 2: User Auth (merged 2025-12-15)

## Current 🔄
- Spec 3: Product Catalog + Search (started 2025-12-16)

## Next Up 📋
- Spec 4: Shopping Cart + Checkout
- Spec 5: Payment Integration
- Spec 6: Order History
- Spec 7: Email Notifications
- Spec 8: Admin Panel
- Spec 9: Analytics Dashboard

Progress: 2/9 complete (22%)
```

**After Spec 3 completes:**

```markdown
# Development Progress

**Last Updated:** 2025-12-22
**Overall:** 3/9 specs complete (33%)

## Completed ✅
- Spec 1: Core Infrastructure (merged 2025-12-10)
- Spec 2: User Auth (merged 2025-12-15)
- Spec 3: Product Catalog + Search (merged 2025-12-20)

## Next Up 📋
- Spec 4: Shopping Cart + Checkout ← START HERE
- Spec 5: Payment Integration
- [... rest of roadmap]

Progress: 3/9 complete (33%)

Next Action:
Run: /dev-specify "Shopping Cart + Checkout (US-003, US-004)"
```

---

## Integration with Other Skills

**Called by:**
- `/dev-finish` - Auto-called after merge if roadmap exists

**Reads:**
- `roadmap.md` - Spec sequence
- Git history - Merge status
- Spec directories - What exists

**Updates:**
- `progress.md` - Living progress document

**Enables:**
- User visibility into project progress
- Clear "what's next" guidance
- Progress tracking without PM overhead

---

## Quick Reference

| Step | Action | Output |
|------|--------|--------|
| 1. Read roadmap | Get spec sequence | List of planned specs |
| 2. Scan git | Check merge status | Completed specs |
| 3. Check specs | What directories exist | Current/in-progress specs |
| 4. Determine next | First incomplete spec | Next action suggestion |
| 5. Update doc | Write progress.md | Updated progress tracking |

---

## Success Criteria

A good progress update:

1. ✅ Clearly shows completed specs
2. ✅ Identifies current work
3. ✅ Lists next specs in roadmap order
4. ✅ Shows simple progress % (X/Y complete)
5. ✅ Suggests next action
6. ✅ Updates automatically after each merge
7. ✅ Stays spec-level (no task details)

---

## Output Location

```
.shipkit/skills/dev-progress/outputs/progress.md
```

**Living document** - updated after each spec completes.
