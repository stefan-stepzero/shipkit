# Git Detection Patterns for Progress Tracking

**Purpose:** Learn how to detect completed specs using git commands

**When to reference:** When updating progress and need to determine which specs are merged

---

## Table of Contents

1. [Core Concept](#core-concept)
2. [Detecting Merged Branches](#detecting-merged-branches)
3. [Detecting Active Branches](#detecting-active-branches)
4. [Correlating Branches to Specs](#correlating-branches-to-specs)
5. [Handling Edge Cases](#handling-edge-cases)
6. [Complete Detection Script](#complete-detection-script)

---

## Core Concept

**A spec is "complete" when:**
1. Spec directory exists (`.shipkit/skills/dev-specify/outputs/specs/NNN-feature-name/`)
2. **AND** the feature branch has been merged to main
3. **AND** (optionally) the branch has been deleted after merge

**Detection strategy:**
- List all spec directories
- For each spec, check if its branch was merged
- Mark as "complete" if merged, "current" if exists but not merged, "next" if doesn't exist

---

## Detecting Merged Branches

### Method 1: Check Merge Commits

**Pattern:** Look for merge commits in git log

```bash
# Find all merge commits mentioning "Spec" or numbered branches
git log --all --merges --oneline --grep="Spec"

# Example output:
# a1b2c3d Merge branch 'feature/001-core-infrastructure' into main
# e4f5g6h Merge branch 'feature/002-user-auth' into main
```

**Pros:**
- Shows explicit merge commits
- Works with GitHub PR merges

**Cons:**
- Requires specific commit message format
- May miss squash merges

---

### Method 2: Check if Branch is in Main History

**Pattern:** Check if branch exists in main's history

```bash
# Check if specific branch was merged into main
git branch --merged main | grep "feature/001-core-infrastructure"

# If output = branch name → merged
# If output = empty → not merged or branch deleted
```

**Pros:**
- Works regardless of commit messages
- Works with squash and rebase merges

**Cons:**
- Requires branch still exists (not deleted)
- Doesn't work if branch was deleted after merge

---

### Method 3: Check if Branch Exists (Deleted = Merged)

**Pattern:** Assume deleted branches were merged

```bash
# List all branches (local and remote)
git branch -a

# If branch doesn't exist → likely merged and deleted
# If branch exists → check Method 1 or 2
```

**Workflow:**
1. Does spec directory exist? YES
2. Does branch exist? NO
3. **Assumption:** Branch was merged and deleted → Spec complete ✅

**Pros:**
- Works with typical workflow (merge → delete branch)
- Simple logic

**Cons:**
- Assumption may be wrong (branch could be manually deleted)
- Requires team discipline (always delete after merge)

---

### Method 4: Reflog Analysis (Most Reliable)

**Pattern:** Check git reflog for merge evidence

```bash
# Search reflog for branch merge
git reflog --all | grep "feature/001-core-infrastructure"

# Example output:
# a1b2c3d HEAD@{2}: merge feature/001-core-infrastructure: Merge made by the 'ort' strategy.
```

**Pros:**
- Most reliable (shows actual merge events)
- Works even if branch deleted

**Cons:**
- Reflog can be pruned (old history lost)
- More complex to parse

---

## Detecting Active Branches

### Check Current Branch

```bash
# Get current branch name
git branch --show-current

# Example output:
# feature/003-product-catalog
```

**Use:** Determine which spec is "current" (in progress)

---

### List All Feature Branches

```bash
# List all branches matching pattern
git branch | grep "feature/"

# Example output:
#   feature/003-product-catalog
#   feature/004-cart-checkout
```

**Use:** Find all in-progress specs (multiple may exist)

---

### Check Branch Status vs Main

```bash
# Check how far ahead/behind main
git rev-list --left-right --count main...feature/003-product-catalog

# Example output:
# 5       12
# ^       ^
# |       └─ 12 commits ahead of main
# └─ 5 commits behind main (need to rebase)
```

**Use:** Show progress on current branch

---

## Correlating Branches to Specs

### Branch Naming Convention

**Standard pattern:**
```
feature/NNN-feature-name

Examples:
feature/001-core-infrastructure
feature/002-user-auth
feature/003-product-catalog
```

**Spec directory pattern:**
```
specs/NNN-feature-name/

Examples:
specs/001-core-infrastructure/
specs/002-user-auth/
specs/003-product-catalog/
```

**Correlation logic:**
- Extract `NNN` from branch name
- Check if `specs/NNN-*/` exists
- Match branch to spec directory

---

### Extraction Script

```bash
#!/usr/bin/env bash

# Extract spec number from branch name
extract_spec_number() {
  local branch="$1"
  # Extract NNN from feature/NNN-name
  if [[ "$branch" =~ feature/([0-9]{3})- ]]; then
    echo "${BASH_REMATCH[1]}"
  else
    echo ""
  fi
}

# Example usage
branch="feature/003-product-catalog"
spec_num=$(extract_spec_number "$branch")
echo "Spec number: $spec_num"  # Output: 003

# Find matching spec directory
specs_dir="specs"
spec_dir=$(find "$specs_dir" -name "${spec_num}-*" -type d)
echo "Spec directory: $spec_dir"  # Output: specs/003-product-catalog/
```

---

### Matching Algorithm

```bash
#!/usr/bin/env bash

# For each spec directory, find its merge status
SPECS_DIR="specs"
for spec_dir in "$SPECS_DIR"/*; do
  spec_name=$(basename "$spec_dir")

  # Extract spec number (e.g., "003" from "003-product-catalog")
  if [[ "$spec_name" =~ ^([0-9]{3})- ]]; then
    spec_num="${BASH_REMATCH[1]}"

    # Construct expected branch name
    branch_name="feature/$spec_name"

    # Check if branch exists
    if git show-ref --verify --quiet "refs/heads/$branch_name"; then
      # Branch exists

      # Check if merged
      if git branch --merged main | grep -q "$branch_name"; then
        echo "$spec_name: ✅ Complete (merged)"
      else
        echo "$spec_name: 🔄 Current (in progress)"
      fi
    else
      # Branch doesn't exist (likely merged and deleted)
      echo "$spec_name: ✅ Complete (merged, branch deleted)"
    fi
  fi
done
```

---

## Handling Edge Cases

### Edge Case 1: Squash Merge

**Problem:** Squash merge doesn't create merge commit

**Detection:**
```bash
# Check if commits from branch exist in main
git log main --oneline | grep "Spec 3:"

# If commit messages preserved → merged
# If not → check Method 3 (branch deleted)
```

**Workaround:** Use branch deletion as proxy for merge completion

---

### Edge Case 2: Rebased Branch

**Problem:** Rebase changes commit hashes, hard to track

**Detection:**
```bash
# Compare branch and main by commit messages
git log feature/003-catalog --format="%s" | head -5
git log main --format="%s" | grep -F "$(git log feature/003-catalog --format='%s' | head -1)"

# If commit message exists in main → likely rebased and merged
```

**Workaround:** Use branch deletion as proxy

---

### Edge Case 3: Multiple Branches per Spec

**Problem:** `feature/003-bug-fix` and `feature/003-add-feature` both for Spec 3

**Detection:**
```bash
# Find all branches matching spec number
git branch | grep "feature/003-"

# Example output:
#   feature/003-product-catalog (main branch)
#   feature/003-bug-fix (bug fix branch)
```

**Resolution:**
- Primary branch (matches spec directory name exactly) determines status
- Secondary branches are patches/improvements
- Spec "complete" when primary branch merged

---

### Edge Case 4: Branch Deleted Without Merge

**Problem:** Branch deleted manually, but never merged

**Detection:**
```bash
# Check if any commits from spec exist in main
SPEC_DIR="specs/003-product-catalog"

# Get first commit in spec directory
FIRST_COMMIT=$(git log --all --diff-filter=A --format="%H" -- "$SPEC_DIR" | tail -1)

# Check if that commit is in main's history
if git merge-base --is-ancestor "$FIRST_COMMIT" main; then
  echo "Spec merged"
else
  echo "Spec NOT merged (directory exists but no merge)"
fi
```

**Safeguard:** Check for spec directory commits in main history

---

### Edge Case 5: Spec Built Directly on Main

**Problem:** No feature branch, commits directly to main

**Detection:**
```bash
# Spec directory exists
# No corresponding feature branch
# Spec files committed directly to main

# Detection:
ls specs/003-product-catalog/  # Exists
git branch | grep "feature/003-"  # Empty

# Status: ✅ Complete (no branch needed, built on main)
```

**Resolution:** If spec directory exists and no branch, assume complete

---

## Complete Detection Script

**Full script for detecting spec status:**

```bash
#!/usr/bin/env bash
# detect-spec-status.sh

set -euo pipefail

SPECS_DIR="specs"
MAIN_BRANCH="main"

detect_spec_status() {
  local spec_dir="$1"
  local spec_name=$(basename "$spec_dir")

  # Extract spec number
  if [[ ! "$spec_name" =~ ^([0-9]{3})- ]]; then
    return  # Skip non-standard names
  fi

  local spec_num="${BASH_REMATCH[1]}"
  local branch_name="feature/$spec_name"

  # Check if branch exists (local or remote)
  local branch_exists=false
  if git show-ref --verify --quiet "refs/heads/$branch_name" || \
     git show-ref --verify --quiet "refs/remotes/origin/$branch_name"; then
    branch_exists=true
  fi

  if $branch_exists; then
    # Branch exists - check if merged
    if git branch --merged "$MAIN_BRANCH" | grep -q "$branch_name"; then
      echo "$spec_name: ✅ Complete (merged, branch still exists)"
    else
      echo "$spec_name: 🔄 Current (in progress)"
    fi
  else
    # Branch doesn't exist - check if commits in main
    local spec_commits=$(git log --all --format="%H" -- "$spec_dir" | head -1)

    if [[ -n "$spec_commits" ]] && git merge-base --is-ancestor "$spec_commits" "$MAIN_BRANCH" 2>/dev/null; then
      echo "$spec_name: ✅ Complete (merged, branch deleted)"
    else
      echo "$spec_name: ⚠️  Unknown (directory exists but no branch/merge evidence)"
    fi
  fi
}

# Main logic
if [[ ! -d "$SPECS_DIR" ]]; then
  echo "No specs directory found: $SPECS_DIR"
  exit 1
fi

echo "Scanning specs..."
echo

for spec_dir in "$SPECS_DIR"/*; do
  if [[ -d "$spec_dir" ]]; then
    detect_spec_status "$spec_dir"
  fi
done
```

**Usage:**
```bash
./detect-spec-status.sh

# Example output:
# Scanning specs...
#
# 001-core-infrastructure: ✅ Complete (merged, branch deleted)
# 002-user-auth: ✅ Complete (merged, branch deleted)
# 003-product-catalog: 🔄 Current (in progress)
# 004-cart-checkout: ⚠️  Unknown (directory exists but no branch/merge evidence)
```

---

## Best Practices

### 1. Consistent Branch Naming
- Always use `feature/NNN-feature-name` format
- Matches spec directory name exactly
- Makes correlation trivial

### 2. Delete Branches After Merge
- Clean workflow: merge → delete
- Makes detection simple (no branch = merged)
- Keeps branch list clean

### 3. Meaningful Commit Messages
- Include spec number in commits: `"Spec 3: Add product catalog"`
- Makes grep-based detection easier
- Improves git history readability

### 4. Merge Commit Messages
- Use format: `"Merge branch 'feature/003-catalog' into main"`
- Makes merge detection reliable
- Standard GitHub/GitLab format

### 5. Don't Delete Unmerged Branches
- Only delete after successful merge
- Prevents false positives
- If must delete, create git tag first

---

## Quick Reference Commands

```bash
# List all merged branches
git branch --merged main

# List all unmerged branches
git branch --no-merged main

# Check if specific branch was merged
git branch --merged main | grep "feature/003-catalog"

# Find all merge commits
git log --merges --oneline --all

# Check if commit is in main
git merge-base --is-ancestor <commit-hash> main

# List all feature branches
git branch | grep "feature/"

# Get current branch
git branch --show-current

# Check if branch exists (local)
git show-ref --verify --quiet refs/heads/feature/003-catalog

# Check if branch exists (remote)
git show-ref --verify --quiet refs/remotes/origin/feature/003-catalog
```

---

## Using Git Detection in dev-progress

**Integration with progress tracking:**

1. **Script collects git data:**
   ```bash
   # update-progress.sh
   MERGED_BRANCHES=$(git branch --merged main)
   ACTIVE_BRANCHES=$(git branch --no-merged main)
   CURRENT_BRANCH=$(git branch --show-current)
   ```

2. **Script outputs structured data:**
   ```bash
   echo "MERGED: $MERGED_BRANCHES"
   echo "ACTIVE: $ACTIVE_BRANCHES"
   echo "CURRENT: $CURRENT_BRANCH"
   ```

3. **Claude analyzes data:**
   - Parse merged branches
   - Correlate to spec directories
   - Mark specs as complete/current/next
   - Generate progress.md

4. **Progress document updated:**
   ```markdown
   ## Completed ✅
   - Spec 1 (merged 2025-12-10)
   - Spec 2 (merged 2025-12-12)

   ## Current 🔄
   - Spec 3 (branch: feature/003-catalog)
   ```

---

## Troubleshooting

### "Can't detect if spec is merged"

**Symptoms:**
- Spec directory exists
- Branch deleted
- No merge evidence in git

**Solutions:**
1. Check git log for spec directory: `git log -- specs/003-catalog/`
2. Check reflog: `git reflog --all | grep "003"`
3. Ask user directly: "Was Spec 3 merged?"

---

### "Multiple specs in progress"

**Symptoms:**
- Multiple unmerged branches with different spec numbers

**Solution:**
- List all in "Current 🔄" section
- Show each with branch name
- Normal for parallel development

---

### "Branch exists but spec directory doesn't"

**Symptoms:**
- Branch `feature/003-catalog` exists
- No `specs/003-*/` directory

**Solution:**
- Spec not created yet (branch created prematurely)
- Or spec directory deleted (error)
- Status: "Branch exists but spec not created"

---

## Summary

**Reliable detection strategy:**
1. List all spec directories (ground truth)
2. For each spec, check branch status
3. Use branch deletion as merge proxy (if branch deleted → merged)
4. Use `git branch --merged` as confirmation (if branch exists)
5. Mark as complete, current, or next

**Key insight:** Spec directories are source of truth. Git state determines completion status.

**Remember:** Git detection is a heuristic. When in doubt, ask the user!
