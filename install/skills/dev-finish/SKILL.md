---
name: dev-finish
description: Complete development work by verifying all tests pass and presenting structured merge options to integrate code into base branch. Use when the user says "finish this work", "ready to merge", "complete the branch", "done implementing", or after dev-implement completes all tasks successfully.
agent: dev-lead
---

# dev-finish - Complete Development Work

## Overview

Guide completion of development work by presenting clear options for integrating code after implementation is complete.

**Core principle:** Verify tests → Determine base → Present options → Execute choice.

**Announce at start:** "I'm using the dev-finish skill to complete this work."

## When to Invoke

Use this skill when:
- Implementation is complete
- All code changes are committed
- All tests pass
- Ready to integrate work into main branch

**Triggers:**
- User says: "Finish this work", "Ready to merge", "Complete the branch"
- After `/dev-implement` completes all tasks
- When explicitly requested: `/dev-finish`

## Prerequisites

**Required:**
- All tests must pass (verified at runtime)
- No uncommitted changes
- Working on a feature branch (not main/master)

**Not required:**
- Specific skill outputs (works with any completed branch)

## Agent Persona

Load the **dev-lead** agent persona:
- Location: `.claude/agents/dev-lead.md`
- Approach: Systematic, verification-focused, clear options
- Constraints: Never proceed with failing tests, always verify before merging

## The Process

### Step 1: Run Verification Script

```bash
.shipkit/skills/dev-finish/scripts/check-readiness.sh
```

**This script:**
1. Checks git status (no uncommitted changes)
2. Identifies current branch
3. Determines base branch (main/master/develop)
4. Runs test suite
5. Presents merge options if all checks pass

**If verification fails:**
- Report the issue to user
- Do NOT proceed to Step 2
- User must fix issues and re-run

**If verification passes:**
- Script presents 3 options
- Continue to Step 2

### Step 2: Ask User to Choose Option

After script completes, ask user:

```
The verification is complete. Which option would you like?

Enter 1, 2, or 3:
```

**Do not add explanation** - the script already showed the options.

### Step 3: Execute Chosen Option

Run the merge script with chosen option:

```bash
# User chose option 1
.shipkit/skills/dev-finish/scripts/merge-branch.sh --option=1

# User chose option 2
.shipkit/skills/dev-finish/scripts/merge-branch.sh --option=2

# User chose option 3
.shipkit/skills/dev-finish/scripts/merge-branch.sh --option=3
```

### Step 4: Report Final Status

After script completes, report what happened:

**Option 1 (merged):**
```
✓ Merge complete!
  Branch: feature-auth → main
  Status: Merged and cleaned up
  Tests: Passing

You're now on the main branch with the integrated code.
```

---

### Step 5: Update Progress (if roadmap exists)

**After successful merge (Option 1 only):**

1. **Check for roadmap:**
   ```bash
   ls .shipkit/skills/dev-roadmap/outputs/roadmap.md 2>/dev/null
   ```

2. **If roadmap exists, auto-invoke:**
   ```
   /dev-progress
   ```

3. **Show updated progress:**
   ```
   📊 Progress updated!

   Spec 2: User Authentication → Complete

   Progress: 2/6 specs complete (33%)

   Next: Spec 3 - User Dashboard (US-003, US-004, US-005)

   Ready to start?
   Run: /dev-specify "User Dashboard (US-003, US-004, US-005)"
   ```

4. **If no roadmap exists:**
   Skip progress update (single-feature project)

---

**Option 2 (kept):**
```
✓ Branch preserved
  Branch: feature-auth
  Status: Ready for later handling

You can merge or create a PR when ready.
```

**Option 3 (discarded):**
```
✓ Branch discarded
  Branch: feature-auth (deleted)
  Status: Permanently removed

You're now on the main branch.
```

**Progress tracking integration:**
- After Option 1 (merge): Auto-calls `/dev-progress` if roadmap exists
- After Option 2 (keep): No progress update (not merged yet)
- After Option 3 (discard): No progress update (work abandoned)

---

## The Three Options Explained

### Option 1: Merge to Main Locally

**Purpose:** Integrate code into base branch immediately

**What happens:**
1. Switch to base branch (main/master)
2. Pull latest changes
3. Merge feature branch
4. Run tests on merged result
5. Delete feature branch (if tests pass)

**When to use:**
- Simple changes ready to integrate
- No code review required
- Solo development
- Quick fixes or small features

**Result:** Code merged, branch deleted, on base branch

### Option 2: Keep Branch As-Is

**Purpose:** Preserve branch without integration

**What happens:**
1. Report branch status
2. Leave everything unchanged
3. No cleanup or modifications

**When to use:**
- Need to switch contexts
- Want to create PR manually later
- Waiting for approval or dependency
- Need to show work to someone first

**Result:** Branch preserved unchanged, can return later

### Option 3: Discard This Work

**Purpose:** Delete branch and all changes permanently

**What happens:**
1. Show commits to be deleted
2. Require typed confirmation ("discard")
3. Switch to base branch
4. Force delete feature branch

**When to use:**
- Experiment didn't work out
- Wrong approach taken
- Started over on different branch
- Prototype or throwaway code

**Result:** Branch deleted permanently, cannot recover

**Safety:** Requires explicit "discard" confirmation

## Test Verification

**Tests MUST pass before offering options.**

### Automatic Test Detection

Script detects test command based on project:

| Project Type | Detection File | Test Command |
|--------------|----------------|--------------|
| Node.js | package.json | npm test |
| Rust | Cargo.toml | cargo test |
| Python | pytest.ini | pytest |
| Go | go.mod | go test ./... |
| Ruby | Gemfile | bundle exec rspec |

### Test Failure Handling

**If tests fail:**
1. Show failure output
2. Report: "Cannot proceed with merge/PR until tests pass"
3. Do NOT present options
4. User must fix and re-run

**Tests must pass before any completion options are presented.**

### Post-Merge Verification

For Option 1, tests run again AFTER merging to ensure merge didn't break anything.

## Extended Documentation

For complete workflows, troubleshooting, and patterns, read:
- `.shipkit/skills/dev-finish/references/reference.md`
- `.shipkit/skills/dev-finish/references/README.md`

## Common Mistakes

**Skipping test verification**
- **Problem:** Merge broken code, create failing state
- **Fix:** Always verify tests before offering options

**Open-ended questions**
- **Problem:** "What should I do next?" → ambiguous
- **Fix:** Script presents exactly 3 structured options

**No confirmation for discard**
- **Problem:** Accidentally delete work
- **Fix:** Require typed "discard" confirmation

## Red Flags

**Never:**
- Proceed with failing tests
- Merge without verifying tests on result
- Delete work without typed confirmation
- Auto-cleanup when user chose "keep as-is"

**Always:**
- Verify tests pass before offering options
- Present exactly 3 options (via script)
- Get typed confirmation for Option 3
- Run tests again after merge (Option 1)
- Report final status clearly

## Integration with Other Skills

**Called after:**
- `/dev-implement` - After all tasks complete
- Any manual development work
- Bug fixes or feature additions

**Calls (conditionally):**
- `/dev-progress` - Auto-called after merge if roadmap exists

**Typical flow:**
```
/dev-implement
  → All tasks complete
  → Tests pass
  → /dev-finish (suggested)
    → Choose option
    → Execute workflow
    → If Option 1 (merged) + roadmap exists:
      → Auto-call /dev-progress
      → Show updated progress
      → Suggest next spec
    → Done
```

## Constraints

1. **Test-first mindset:** Never proceed without passing tests
2. **Clear choices:** Always present exactly 3 options (no variations)
3. **Explicit confirmation:** Require "discard" typed for Option 3
4. **Post-merge validation:** Run tests after merge (Option 1)
5. **Status reporting:** Always report final state clearly

## Quick Reference

| Step | Action | Tool |
|------|--------|------|
| 1. Verify | Run check-readiness.sh | Script checks git/tests/base |
| 2. Choose | Ask user (1, 2, or 3) | User selects option |
| 3. Execute | Run merge-branch.sh | Script executes workflow |
| 4. Report | Show final status | Confirm completion |
| 5. Progress | Update if roadmap exists (Option 1 only) | Auto-call /dev-progress |

## Success Criteria

A successful dev-finish run:

1. ✅ Tests verified before options presented
2. ✅ Exactly 3 options shown
3. ✅ User chose an option explicitly
4. ✅ Workflow executed correctly
5. ✅ Final state reported clearly
6. ✅ No unexpected errors

## Script Locations

All scripts in: `.shipkit/skills/dev-finish/scripts/`

- `check-readiness.sh` - Verify tests and present options (no flags)
- `merge-branch.sh` - Execute chosen option (requires `--option=N`)

## Next Skill Suggestion

**After completion:**
- If merged: Start next feature with `/dev-specify "feature description"`
- If kept: Can switch to other work
- If discarded: Start fresh approach with `/dev-specify "new approach"`
