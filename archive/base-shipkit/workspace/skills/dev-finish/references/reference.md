# dev-finish - Complete Development Work

## Purpose

The dev-finish skill guides completion of development work by presenting structured options for integrating code after implementation is complete.

## Core Principle

**Verify tests → Determine base → Present options → Execute choice**

## When to Use

Use dev-finish when:
- Implementation is complete
- All code changes are committed
- Ready to integrate work into main branch
- Need to decide between merge, PR, or cleanup

## Prerequisites

**Required:**
- All tests must pass
- No uncommitted changes
- All work committed to current branch

**Not required:**
- Specific skill outputs (dev-finish works with any completed branch)

## The Process

### Phase 1: Verification

Before offering any options, verify:

1. **Git status is clean**
   - No uncommitted changes
   - All work is committed
   - Currently on a feature branch

2. **Tests pass**
   - Run project test suite
   - All tests must pass
   - No failures or errors

3. **Base branch identified**
   - Determine where code should merge (main/master/develop)
   - Verify base branch exists
   - Confirm merge-base is valid

**If any verification fails:** Stop and report the issue. Do not proceed to options.

### Phase 2: Present Options

After verification passes, present exactly these options:

```
Implementation complete! What would you like to do?

1. Merge to <base-branch> locally
2. Keep branch as-is (handle later)
3. Discard this work
```

**Do not add explanations or additional options.** Keep it concise and structured.

### Phase 3: Execute Choice

#### Option 1: Merge Locally

**Purpose:** Integrate code into base branch immediately

**Workflow:**
1. Switch to base branch
2. Pull latest changes
3. Merge feature branch
4. Run tests on merged result
5. Delete feature branch if tests pass

**When to use:**
- Simple changes ready to integrate
- No code review required
- Solo development or pair programming
- Quick fixes or small features

**Result:**
- Code merged to base branch
- Feature branch deleted
- Working directory on base branch

#### Option 2: Keep As-Is

**Purpose:** Preserve branch without integration

**Workflow:**
1. Report branch name and status
2. Leave everything as-is
3. No cleanup or changes

**When to use:**
- Need to switch contexts
- Want to create PR manually later
- Waiting for something (approval, dependency, etc.)
- Need to show work to someone first

**Result:**
- Branch preserved unchanged
- Can return later to finish
- No cleanup or modifications

#### Option 3: Discard Work

**Purpose:** Delete branch and all changes permanently

**Workflow:**
1. Show commits to be deleted
2. Require typed confirmation ("discard")
3. Switch to base branch
4. Force delete feature branch

**When to use:**
- Experiment didn't work out
- Wrong approach taken
- Started over on different branch
- Prototype or throwaway code

**Result:**
- Branch deleted permanently
- All commits lost (unless backed up)
- Cannot be recovered

**Safety:** Requires explicit "discard" confirmation to prevent accidents.

## Test Verification

### Test Detection

The script automatically detects test commands based on project type:

| Project Type | Detection File | Test Command |
|--------------|----------------|--------------|
| Node.js | package.json | npm test |
| Rust | Cargo.toml | cargo test |
| Python | pytest.ini, pyproject.toml | pytest |
| Go | go.mod | go test ./... |
| Ruby | Gemfile | bundle exec rspec |

If detection fails, Claude will ask for the test command.

### Test Failure Handling

**If tests fail:**
1. Show failure output
2. Report: "Cannot proceed with merge/PR until tests pass"
3. Stop immediately
4. Do not present options
5. User must fix tests and re-run

**Tests must pass before offering any completion options.**

### Post-Merge Verification

For Option 1 (merge locally), tests are run again AFTER merging:
- Ensures merge didn't break anything
- Catches integration issues
- Verifies base branch is still healthy

If post-merge tests fail:
- Merge is complete but broken
- User must fix before proceeding
- Branch already deleted (merge is committed)

## Branch Detection

### Base Branch Discovery

Script tries these branches in order:
1. `main`
2. `master`
3. `develop`

First branch that exists AND has a valid merge-base with HEAD is chosen.

### Fallback

If auto-detection fails, Claude asks: "Which branch did this split from?"

### Validation

- Checks branch exists: `git rev-parse --verify <branch>`
- Checks merge-base: `git merge-base HEAD <branch>`
- Both must succeed for auto-selection

## Git Workflows

### Standard Merge Workflow

```bash
# Option 1 executes:
git checkout main           # Switch to base
git pull                    # Get latest
git merge feature-branch    # Merge
npm test                    # Verify
git branch -d feature-branch # Cleanup
```

### Keep Workflow

```bash
# Option 2 executes:
# (nothing - just reports status)
```

### Discard Workflow

```bash
# Option 3 executes:
git log main..feature-branch --oneline  # Show commits
# (wait for "discard" confirmation)
git checkout main           # Switch to base
git branch -D feature-branch # Force delete
```

## Error Handling

### Uncommitted Changes

**Error:** Uncommitted changes detected

**Resolution:**
1. Show `git status --short` output
2. Tell user: "Please commit or stash changes before finishing"
3. Exit without options

### Tests Failing

**Error:** Test suite has failures

**Resolution:**
1. Show test failure output
2. Tell user: "Cannot proceed with merge/PR until tests pass"
3. Exit without options

### Not on a Branch

**Error:** Detached HEAD state

**Resolution:**
1. Tell user: "Not on a branch (detached HEAD)"
2. Suggest: Create a branch first (`git checkout -b feature-name`)
3. Exit without options

### No Base Branch Found

**Error:** Cannot determine where to merge

**Resolution:**
1. Show available branches
2. Ask: "Which branch did this split from?"
3. Use provided branch for merge

## Integration with Other Skills

### Called After

- **dev-implement** - After all tasks complete and tests pass
- **dev-systematic-debugging** - After fixing bugs
- Any manual development work

### Typical Flow

```
/dev-implement
  → All tasks complete
  → Tests pass
  → /dev-finish (automatic or suggested)
    → Choose option
    → Execute workflow
    → Done
```

## Common Patterns

### Solo Development

Most common: Option 1 (merge locally)
- Quick integration
- No review needed
- Immediate availability

### Team Development

Most common: Option 2 (keep as-is) then manual PR
- Create PR through GitHub/GitLab UI
- Add reviewers
- Wait for approval
- Note: Shipkit doesn't auto-create PRs (manual process)

### Experimental Work

Most common: Option 3 (discard)
- Prototype didn't work
- Try different approach
- Clean slate

## Red Flags

**Never:**
- Proceed with failing tests
- Merge without verifying tests on result
- Delete work without typed confirmation
- Auto-cleanup when user chose "keep as-is"
- Skip verification steps

**Always:**
- Verify tests pass before offering options
- Present exactly 3 options (no more, no less)
- Get typed "discard" confirmation for Option 3
- Run tests again after merge (Option 1)
- Report final status clearly

## Script Flags

### check-readiness.sh

No flags - just runs verification and presents options.

### merge-branch.sh

**Required:**
- `--option=N` - Which option to execute (1, 2, or 3)

**Optional:**
- `--help`, `-h` - Show usage information

**Examples:**
```bash
# Merge locally
./merge-branch.sh --option=1

# Keep as-is
./merge-branch.sh --option=2

# Discard
./merge-branch.sh --option=3
```

## Success Criteria

A successful dev-finish run:

1. ✅ Tests verified before options presented
2. ✅ Exactly 3 options shown (no variations)
3. ✅ User chose an option explicitly
4. ✅ Workflow executed correctly
5. ✅ Final state reported clearly
6. ✅ No unexpected errors or states

## Anti-Patterns

### Don't: Skip Test Verification

**Wrong:**
```
Implementation complete! What would you like to do?
1. Merge to main locally
...
```

**Right:**
```
Running tests...
npm test

✓ All tests pass

Implementation complete! What would you like to do?
1. Merge to main locally
...
```

### Don't: Add Custom Options

**Wrong:**
```
What would you like to do?
1. Merge to main locally
2. Create PR
3. Keep branch as-is
4. Squash and merge
5. Rebase and merge
6. Discard this work
```

**Right:**
```
What would you like to do?
1. Merge to main locally
2. Keep branch as-is
3. Discard this work
```

### Don't: Delete Without Confirmation

**Wrong:**
```bash
# User chose option 3
git branch -D feature-branch  # Immediate deletion
```

**Right:**
```bash
# User chose option 3
git log main..feature-branch --oneline
echo "Type 'discard' to confirm deletion:"
read confirmation
if [[ "$confirmation" == "discard" ]]; then
  git branch -D feature-branch
fi
```

## Quick Reference

| Step | Action | Script |
|------|--------|--------|
| 1. Verify | Run check-readiness.sh | Checks git status, runs tests, identifies base |
| 2. Choose | User selects option | Claude asks user which option (1, 2, or 3) |
| 3. Execute | Run merge-branch.sh | Executes chosen workflow |
| 4. Report | Show final status | Confirms completion or reports issues |

## Troubleshooting

### Tests won't run

**Symptom:** Script can't detect test command

**Fix:**
- Provide test command when prompted
- Or skip tests (not recommended)

### Merge conflicts

**Symptom:** Merge fails with conflicts

**Fix:**
1. Script will report conflict
2. User must resolve manually
3. Complete merge with `git merge --continue`
4. Re-run tests
5. Delete branch manually if desired

### Branch already merged

**Symptom:** Branch has no unique commits

**Fix:**
- Can safely delete with `git branch -d <branch>`
- Or use Option 2 (keep as-is) and clean up later

### Want to create PR (not supported yet)

**Symptom:** No PR option in menu

**Current Workaround:**
1. Choose Option 2 (keep as-is)
2. Push branch manually: `git push -u origin <branch>`
3. Create PR through GitHub/GitLab UI

**Future:** May add PR creation as Option 4 in future versions.
