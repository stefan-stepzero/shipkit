#!/usr/bin/env bash
#
# teardown-worktree.sh - Remove a git worktree and optionally its branch
#
# Usage: teardown-worktree.sh <task-slug> [--delete-branch]
#
# Options:
#   --delete-branch   Also delete the impl/<task-slug> branch (use after merge)
#
# Outputs JSON with result on success, or error message on failure.

set -e

TASK_SLUG="$1"
DELETE_BRANCH="$2"

if [ -z "$TASK_SLUG" ]; then
    echo '{"error": "Task slug required", "usage": "teardown-worktree.sh <task-slug> [--delete-branch]"}'
    exit 1
fi

# Paths
WORKTREE_PATH=".shipkit/worktrees/${TASK_SLUG}"
IMPL_BRANCH="impl/${TASK_SLUG}"

# Check if worktree exists
if [ ! -d "$WORKTREE_PATH" ]; then
    echo "{\"error\": \"Worktree not found\", \"path\": \"$WORKTREE_PATH\"}"
    exit 1
fi

# Remove worktree
git worktree remove "$WORKTREE_PATH" --force 2>/dev/null || {
    # If normal remove fails, try prune
    rm -rf "$WORKTREE_PATH"
    git worktree prune
}

BRANCH_DELETED="false"

# Optionally delete branch
if [ "$DELETE_BRANCH" = "--delete-branch" ]; then
    if git show-ref --verify --quiet "refs/heads/$IMPL_BRANCH"; then
        git branch -D "$IMPL_BRANCH" 2>/dev/null || true
        BRANCH_DELETED="true"
    fi
fi

echo "{
  \"success\": true,
  \"task_slug\": \"$TASK_SLUG\",
  \"worktree_removed\": \"$WORKTREE_PATH\",
  \"branch_deleted\": $BRANCH_DELETED
}"
