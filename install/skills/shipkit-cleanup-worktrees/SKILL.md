---
name: shipkit-cleanup-worktrees
description: List and clean up stale implementation worktrees. Shows PR status and age for each worktree.
triggers:
  - cleanup worktrees
  - clean up worktrees
  - remove old worktrees
  - worktree cleanup
allowed-tools:
  - Read
  - Glob
  - Bash
---

# shipkit-cleanup-worktrees

Review and clean up implementation worktrees created by `/shipkit-implement-independently`. Shows each worktree's age, PR status, and allows selective or bulk cleanup.

---

## When to Invoke

**User triggers:**
- "Clean up worktrees"
- "Remove old worktrees"
- Session start warning about stale worktrees

**Use cases:**
- After completing or abandoning parallel implementations
- Periodic cleanup of accumulated worktrees
- Reclaiming disk space

---

## Prerequisites

**Required:**
- Git repository with worktrees in `.shipkit/worktrees/`
- GitHub CLI (`gh`) for PR status lookup (optional but recommended)

**No prerequisites if:**
- Just checking what worktrees exist (works without gh)

---

## Process

### Step 1: List Worktrees

Scan `.shipkit/worktrees/` for existing worktrees:

```bash
# List all worktree directories
ls -la .shipkit/worktrees/ 2>/dev/null || echo "No worktrees found"
```

For each worktree, gather:
- **Task slug**: Directory name
- **Age**: Days since creation
- **Branch**: `impl/{slug}`
- **PR status**: Open, Merged, Closed, or None

### Step 2: Get PR Status for Each

For each worktree, check its PR:

```bash
# Get PR status
gh pr list --head "impl/{slug}" --state all --json number,state,url --limit 1
```

### Step 3: Present Cleanup Options

Display worktrees with status:

```
## Worktree Cleanup

| Worktree | Age | PR Status | Recommendation |
|----------|-----|-----------|----------------|
| login-form | 2d | #42 Merged | ✅ Safe to clean |
| api-refactor | 8d | #45 Closed | ✅ Safe to clean |
| dashboard-widget | 1d | #48 Open | ⚠️ PR still open |
| experimental | 15d | None | 🔶 No PR (abandoned?) |

**Auto-selected for cleanup:**
- login-form (PR merged)
- api-refactor (PR closed)

**Require manual decision:**
- dashboard-widget (PR open - merge or close first?)
- experimental (no PR - delete work or create PR?)

[Clean selected] [Clean all] [Select manually] [Cancel]
```

### Step 4: Execute Cleanup

For each worktree to clean:

```bash
# Remove worktree
git worktree remove ".shipkit/worktrees/{slug}" --force

# Delete branch if PR was merged or closed
git branch -D "impl/{slug}"

# Prune worktree metadata
git worktree prune
```

### Step 5: Confirm Results

```
## Cleanup Complete

Removed 2 worktrees:
- login-form (branch deleted)
- api-refactor (branch deleted)

Preserved 2 worktrees:
- dashboard-widget (PR still open)
- experimental (no PR - needs decision)

Disk space freed: ~50MB
```

---

## Cleanup Recommendations

| PR Status | Age | Recommendation |
|-----------|-----|----------------|
| Merged | Any | ✅ Auto-clean |
| Closed | Any | ✅ Auto-clean |
| Open | <7d | ⚠️ Preserve |
| Open | >7d | 🔶 Review - stale PR? |
| None | <3d | ⚠️ Preserve |
| None | >7d | 🔶 Review - abandoned? |

---

## Context Files This Skill Reads

- `.shipkit/worktrees/*/` - Worktree directories
- GitHub PR status via `gh` CLI

---

## Context Files This Skill Writes

**Write Strategy: DELETE**
- Removes `.shipkit/worktrees/{slug}/` directories
- Removes `impl/{slug}` git branches
- Does not create any files

---

## When This Skill Integrates with Others

### Before This Skill
- `/shipkit-implement-independently` - Creates worktrees
  - **When**: You spawned parallel implementations
  - **Why**: This skill cleans up what that skill creates

### After This Skill
- Continue normal workflow
  - **When**: Cleanup complete
  - **Why**: Worktrees removed, disk space reclaimed

### When Session Starts
- Session hook warns about stale worktrees
  - **Trigger**: Worktrees older than 7 days detected
  - **Why**: Prompts you to review and clean up accumulated work

---

## Example Session

```
User: /shipkit-cleanup-worktrees

Claude:
## Worktree Cleanup

Found 3 worktrees in .shipkit/worktrees/:

| Worktree | Age | PR Status | Action |
|----------|-----|-----------|--------|
| user-settings | 5d | #47 Merged | ✅ Clean |
| payment-flow | 12d | #39 Closed | ✅ Clean |
| new-feature | 1d | #52 Open | ⚠️ Keep |

**Ready to clean 2 worktrees** (merged/closed PRs).
Preserve 1 worktree (open PR).

Proceed with cleanup?

User: Yes

Claude:
Cleaned up 2 worktrees:
- user-settings (removed worktree + branch)
- payment-flow (removed worktree + branch)

Preserved:
- new-feature (PR #52 still open)

Freed ~35MB disk space.
```

---

<!-- SECTION:success-criteria -->
## Success Criteria

- [ ] All worktrees listed with age and PR status
- [ ] User presented with cleanup options
- [ ] Safe worktrees (merged/closed PRs) auto-selected
- [ ] User confirmed cleanup selection
- [ ] Worktrees and branches removed
- [ ] Results summary displayed
<!-- /SECTION:success-criteria -->

---

<!-- SECTION:after-completion -->
## After Completion

Worktrees cleaned up. Disk space reclaimed.

**If worktrees preserved:**
- Open PRs need merge/close decision first
- No-PR worktrees need review (create PR or discard?)

**Next steps:**
- Continue with main workflow
- `/shipkit-implement-independently` - Start new parallel work
<!-- /SECTION:after-completion -->

---

## Troubleshooting

**"Worktree is dirty"**
- Uncommitted changes exist
- Either commit/push or use `--force` to discard

**"Branch has unmerged changes"**
- PR wasn't merged, but branch has commits
- Review the work before deleting

**"Worktree locked"**
- Another git process may be using it
- Close other terminals/editors, retry
