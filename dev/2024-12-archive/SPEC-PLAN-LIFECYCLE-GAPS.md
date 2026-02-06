# Spec & Plan Lifecycle Analysis

**Created:** 2025-12-31
**Issue:** No clear system to distinguish completed vs in-progress work

---

## What EXISTS

### Specs DO Have Lifecycle System ✅

**Documented in:** `install/skills/shipkit-spec/references/spec-lifecycle.md`

**Folder structure:**
```
.shipkit/specs/
  active/           # Work in progress
    feature-a.md
    feature-b.md
  implemented/      # Completed and shipped
    feature-x.md
    feature-y.md
```

**Movement trigger:**
- `/shipkit-quality-confidence` passes quality checks
- Asks user: "Move .shipkit/specs/active/[feature].md to specs/implemented/?"
- If user confirms → Adds completion metadata + moves file

**Completion metadata added:**
```markdown
---
**Status**: Implemented
**Date**: 2025-01-20
**Implemented by**: Claude + User
**Final notes**: Shipped with all Must Have criteria.
**Deviations**: Changed API endpoint from POST to PUT per performance testing.
---
```

**Detection impact:**
- shipkit-post-spec-check only triggers on files modified in last 2 minutes
- OLD specs in active/ won't re-trigger detection (good!)
- But they accumulate if not moved to implemented/

---

## What DOESN'T Exist

### Plans Have NO Lifecycle System ❌

**Current structure:**
```
.shipkit/plans/
  feature-a-plan.md
  feature-b-plan.md
  feature-x-plan.md  # ← No way to know if this is done!
```

**Problems:**
1. No `plans/active/` vs `plans/implemented/` separation
2. No completion metadata
3. No skill moves plans when complete
4. Old plans accumulate forever
5. Can't tell what's implemented vs what's pending

**Impact on detection:**
- shipkit-post-plan-check triggers on files modified in last 2 minutes
- Old plans in plans/ won't re-trigger (good!)
- But no way to track completion status

---

## The Core Problem

**User's concern is valid:**

> "It gets harder to scan what's been done versus what hasn't been done"

**Current state:**
- ✅ **Specs**: active/ folder shows pending work clearly (if users remember to move to implemented/)
- ❌ **Plans**: No distinction between done and pending
- ❌ **Both**: Relies on user manually moving files (not automated)

**What happens in practice:**
1. User creates spec → shipkit-post-spec-check creates queue → shipkit-integration-docs runs
2. User creates plan → shipkit-post-plan-check creates queue → shipkit-data-contracts runs
3. User implements feature
4. User runs /shipkit-quality-confidence
5. **CRITICAL STEP**: User must say "yes" to move spec to implemented/
6. **If user skips this**: Spec stays in active/ forever

**Result over time:**
```
.shipkit/specs/active/
  feature-from-2-months-ago.md     # ← Actually shipped, but looks pending
  feature-being-built-now.md       # ← Actually pending
  feature-planned-but-not-started.md  # ← Also pending
```

**Impossible to distinguish without reading each spec!**

---

## Detection Scripts Are OK (Not the Problem)

**Detection scripts use 2-minute window:**
```python
RECENT_MINUTES = 2
# Only triggers if file modified in last 2 minutes
```

**This is CORRECT behavior:**
- Detects NEW specs/plans when first created
- Doesn't re-trigger on old files (prevents spam)
- Not confused by stale files

**The problem is NOT detection - it's lifecycle management.**

---

## Proposed Solutions

### Option 1: Automated Spec Movement (Recommended)

**Change shipkit-quality-confidence behavior:**
- Currently: ASKs user to move spec
- Proposed: AUTOMATICALLY move spec if quality checks pass

**Implementation:**
```markdown
### Step 5: Archive Spec (Auto)

**If all quality checks passed:**
1. Add completion metadata to spec
2. Move: specs/active/[name].md → specs/implemented/[name].md
3. Confirm to user: "✓ Feature complete. Spec moved to implemented/"

**If quality checks failed:**
- Keep in specs/active/
- User must fix issues and re-run quality check
```

**Pros:**
- No user action required
- Clear separation: active = pending, implemented = done
- Works automatically with existing workflow

**Cons:**
- Users lose control over when to move
- May want to iterate even after quality check

---

### Option 2: Plan Lifecycle System

**Create parallel structure for plans:**
```
.shipkit/plans/
  active/
    feature-a-plan.md
  implemented/
    feature-x-plan.md
```

**Update shipkit-implement to move plans:**
```markdown
### Step 10: Archive Plan (Optional)

**After implementation complete, ask user:**
"Feature implemented. Move plan to implemented/ folder? (y/n)"

If yes:
1. Add completion note to plan
2. Move: plans/active/[name].md → plans/implemented/[name].md
```

**Pros:**
- Consistent with specs
- Clear tracking of what's implemented

**Cons:**
- More folders to manage
- Plans less important than specs (could skip this)

---

### Option 3: Status Tracking in Filenames

**Alternative: Use filename prefixes:**
```
.shipkit/specs/active/
  [PENDING] feature-a.md
  [IN-PROGRESS] feature-b.md
  [DONE] feature-x.md
```

**Pros:**
- No folder movement needed
- Easy to scan visually

**Cons:**
- Filename changes break references
- Cluttered filenames
- Not as clean as folder separation

---

### Option 4: Status Metadata File

**Create tracking file:**
```markdown
# .shipkit/status.md

## Specs

| Spec | Status | Completed |
|------|--------|-----------|
| feature-a.md | Pending | - |
| feature-b.md | In Progress | - |
| feature-x.md | Implemented | 2025-01-20 |

## Plans

| Plan | Status | Completed |
|------|--------|-----------|
| feature-a-plan.md | Pending | - |
| feature-x-plan.md | Implemented | 2025-01-20 |
```

**Pros:**
- Central tracking
- Easy to see status at a glance

**Cons:**
- Separate file to maintain
- Can get out of sync with actual files
- Users might forget to update it

---

## Recommendation

**Priority: Fix spec lifecycle (Option 1)**

1. **Make shipkit-quality-confidence auto-move specs** when quality checks pass
   - Change from "ask user" → "auto-move"
   - Add flag to skip if user wants manual control

2. **Add shipkit-project-status check** for stale active specs
   - Warn: "5 specs in active/ older than 30 days - consider archiving"
   - Helps catch forgotten specs

3. **Defer plan lifecycle** for now
   - Plans are less critical than specs
   - Can track completion via implementations.md
   - Revisit if becomes a problem

**Quick fix for NOW:**
- Update shipkit-quality-confidence SKILL.md to emphasize importance of moving specs
- Add reminder in shipkit-whats-next when specs/active/ has >5 files

---

## Files to Update (If Implementing Option 1)

1. `install/skills/shipkit-quality-confidence/SKILL.md`
   - Change Step 5 from "ask" → "auto-move"
   - Add: "Feature complete. Spec moved to specs/implemented/"

2. `install/skills/shipkit-project-status/SKILL.md`
   - Add: Check specs/active/ for stale files (>30 days)
   - Warn: "X specs may be implemented but not archived"

3. `install/skills/shipkit-whats-next/SKILL.md`
   - Add: Count specs/active/*.md
   - Suggest: "You have X active specs. Run /shipkit-project-status to review."

---

**Bottom line:** The system HAS a lifecycle design, but it's OPTIONAL (user must confirm). Making it AUTOMATIC would solve the accumulation problem.
