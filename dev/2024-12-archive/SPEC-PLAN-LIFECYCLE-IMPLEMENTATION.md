# Spec & Plan Lifecycle Implementation

**Created:** 2025-12-31
**Status:** ✅ COMPLETE

---

## What Was Implemented

**Option 2 (Auto-move with override)** for BOTH specs and plans.

### The Workflow

```
1. User runs /shipkit-spec
   → Creates: .shipkit/specs/active/feature.md

2. User runs /shipkit-plan
   → Creates: .shipkit/plans/active/feature-plan.md

3. User runs /shipkit-implement
   → Builds feature
   → At completion, ALWAYS suggests: /shipkit-quality-confidence

4. User runs /shipkit-quality-confidence
   → Verifies acceptance criteria
   → If PASSED, asks: "Archive spec and plan? (Y/n)"
   → Default is YES (just hit Enter)

5. If user confirms (Y or Enter):
   → Adds completion metadata to both files
   → Moves spec: specs/active/ → specs/implemented/
   → Moves plan: plans/active/ → plans/implemented/
   → Shows: "✅ Feature complete! Spec and plan archived to implemented/"

6. /shipkit-whats-next automatically prioritizes quality-confidence
   → Step 0.5: Detects recent implementation (implementations.md updated)
   → Suggests: /shipkit-quality-confidence as HIGH priority
```

---

## Folder Structure

**Before:**
```
.shipkit/
  specs/active/
    feature-a.md          # Pending
    feature-b.md          # Implemented but not moved
    feature-c.md          # In progress
  plans/
    feature-a-plan.md     # No way to tell if done!
    feature-b-plan.md
```

**After:**
```
.shipkit/
  specs/
    active/
      feature-a.md        # Pending spec
      feature-c.md        # In progress spec
    implemented/
      feature-b.md        # ✓ Completed (with metadata)
  plans/
    active/
      feature-a-plan.md   # Pending plan
      feature-c-plan.md   # In progress plan
    implemented/
      feature-b-plan.md   # ✓ Completed (with metadata)
```

**Benefits:**
- ✅ Clear separation: active = pending, implemented = done
- ✅ Can scan active/ folders to see what's left to build
- ✅ Completion metadata preserved (when shipped, by whom)
- ✅ Default YES makes archival easy (just hit Enter)
- ✅ Can override if need to iterate more (type 'n')

---

## Files Modified

### 1. Plans Use Active/Implemented Folders

**File: `install/skills/shipkit-plan/SKILL.md`**
- Changed: `plans/[name].md` → `plans/active/[name].md`
- All references updated (4 locations)

**File: `install/skills/shipkit-implement/SKILL.md`**
- Changed: References to `plans/` → `plans/active/`
- Added: "Next Steps After Implementation" section
- Recommends: /shipkit-quality-confidence immediately after implementing

---

### 2. Quality Confidence Moves Both

**File: `install/skills/shipkit-quality-confidence/SKILL.md`**

**Changed behavior:**
- Old: "Move spec to implemented? (yes/no)" - explicit yes required
- New: "Archive spec and plan? (Y/n)" - default YES, just hit Enter

**Now moves BOTH:**
1. Spec: `specs/active/` → `specs/implemented/`
2. Plan: `plans/active/` → `plans/implemented/`

**Adds completion metadata:**
```markdown
---
**Status**: Implemented
**Date**: 2025-12-31
**Completed**: Quality checks passed
---
```

**User can still override:**
- Type 'n' to keep in active/ (iterate more)
- Warns: "Spec/plan will remain in active/ until you archive them"

---

### 3. Auto-Suggest Quality Confidence

**File: `install/skills/shipkit-implement/SKILL.md`**

Added "Next Steps After Implementation" section:
```
✅ Feature implemented!

Next: /shipkit-quality-confidence

This will:
• Verify all acceptance criteria from spec
• Run final quality checks
• Move spec and plan to implemented/ folder (marks feature complete)

Run /shipkit-quality-confidence now to verify and complete this feature?
```

**Why this matters:**
- Users reminded to run quality check
- Prevents specs/plans from accumulating in active/
- Creates completion record automatically

---

### 4. Workflow Brain Prioritizes Quality Check

**File: `install/skills/shipkit-whats-next/SKILL.md`**

Added Step 0.5: "Check for Post-Implementation Quality Check"

**Detection:**
- implementations.md modified in last 60 minutes
- Source files modified in last 60 minutes
- No recent quality check run

**Suggests:**
```
🎯 PRIORITY: Implementation complete, quality check recommended

Recommendation: /shipkit-quality-confidence

Why: Verify acceptance criteria, run quality checks, and mark feature as
complete (archives spec and plan).
```

**Priority: 🟡 HIGH** (after queue work, before normal workflow)

---

### 5. Documentation Updated

**File: `install/claude-md/shipkit.md`**

Updated:
- File structure shows active/ and implemented/ folders
- Skill invocation shows full workflow
- Protected files section explains archival
- Workflow pattern includes quality-confidence

**New workflow:**
```
/shipkit-spec → specs/active/
  → /shipkit-plan → plans/active/
    → /shipkit-implement
      → /shipkit-quality-confidence → moves to implemented/
```

---

## How It Works

### Scenario: Building a Feature

```
Day 1:
  User: "/shipkit-spec - build login feature"
  → Creates: specs/active/login.md

Day 2:
  User: "/shipkit-plan"
  → Creates: plans/active/login-plan.md

Day 3-4:
  User: "/shipkit-implement"
  → Builds feature
  → At end, Claude says:
    "✅ Feature implemented!
     Next: /shipkit-quality-confidence

     This will verify acceptance criteria and mark feature as complete.

     Run /shipkit-quality-confidence now?"

Day 5:
  User: "/shipkit-quality-confidence"
  → Runs all checks
  → ✅ PASSED
  → Claude asks: "Archive spec and plan? (Y/n)"
  → User hits Enter (default YES)
  → Moves both files to implemented/
  → Adds completion metadata
  → Shows: "✅ Feature complete! Spec and plan archived to implemented/"

Result:
  .shipkit/
    specs/
      active/          # Empty (or only has pending specs)
      implemented/
        login.md       # With completion metadata
    plans/
      active/          # Empty (or only has pending plans)
      implemented/
        login-plan.md  # With completion date
```

---

## Key Design Decisions

### 1. Default YES (Y/n) Not Explicit Confirmation

**Rationale:**
- Most users want to archive after quality check passes
- Just hitting Enter = archived (low friction)
- Can still type 'n' to keep iterating
- Balances automation with user control

### 2. Move BOTH Spec and Plan Together

**Rationale:**
- They're paired (one spec → one plan)
- Both represent the "done" state
- Inconsistent to archive one but not the other
- Simpler to move together

### 3. Auto-Suggest After Implementation

**Rationale:**
- Users forget to run quality check
- shipkit-implement now always reminds them
- shipkit-whats-next detects recent implementation
- Two mechanisms ensure it's not forgotten

### 4. Plans Get Same Treatment as Specs

**Rationale:**
- User specifically requested this
- Consistent lifecycle across artifacts
- Easier to track completion
- Plans are important enough to deserve archival

---

## Migration for Existing Projects

**Old projects will have:**
```
.shipkit/
  specs/active/
    feature-a.md
    feature-b.md      # Might be done, might not be
  plans/
    feature-a-plan.md  # Might be done, might not be
```

**What happens:**
1. New specs/plans go to active/ folders ✓
2. Old specs stay in specs/active/ until quality check run
3. Old plans stay in plans/ (no /implemented yet)
4. User can manually move old files if needed
5. Or just run /shipkit-quality-confidence on each to archive

**No breaking changes** - old structure still works, just messier

---

## Testing Checklist

When you test after installation:

- [ ] /shipkit-spec creates files in specs/active/
- [ ] /shipkit-plan creates files in plans/active/
- [ ] /shipkit-implement suggests /shipkit-quality-confidence at end
- [ ] /shipkit-quality-confidence asks "Archive spec and plan? (Y/n)"
- [ ] Hitting Enter (default YES) moves both files
- [ ] Completion metadata added to both files
- [ ] /shipkit-whats-next prioritizes quality-confidence after implementation
- [ ] Active folders only show pending work
- [ ] Implemented folders preserve completed work

---

## Summary

**What you asked for:**
> "Option two for specs and plans and they both get triggered once quality
> confidence is done, which itself should be triggered after the implementation
> skill rate"

**What was delivered:**
✅ Option 2 (Auto-move with override: Y/n default)
✅ For BOTH specs and plans
✅ Both moved when quality-confidence passes
✅ Quality-confidence auto-suggested after implement
✅ shipkit-whats-next prioritizes it
✅ All documentation updated

**The lifecycle is now complete and automatic!** 🎉
