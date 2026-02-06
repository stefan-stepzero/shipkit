#!/usr/bin/env bash
#
# setup-worktree.sh - Create an isolated git worktree for independent implementation
#
# Usage: setup-worktree.sh <task-slug>
#
# Creates:
#   - Worktree at .shipkit/worktrees/<task-slug>/
#   - Branch: impl/<task-slug>
#
# Outputs JSON with worktree info on success, or error message on failure.

set -e

TASK_SLUG="$1"

if [ -z "$TASK_SLUG" ]; then
    echo '{"error": "Task slug required", "usage": "setup-worktree.sh <task-slug>"}'
    exit 1
fi

# Sanitize task slug (lowercase, alphanumeric and hyphens only)
TASK_SLUG=$(echo "$TASK_SLUG" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g' | sed 's/--*/-/g' | sed 's/^-//' | sed 's/-$//')

if [ -z "$TASK_SLUG" ]; then
    echo '{"error": "Invalid task slug after sanitization"}'
    exit 1
fi

# Paths
WORKTREE_DIR=".shipkit/worktrees"
WORKTREE_PATH="${WORKTREE_DIR}/${TASK_SLUG}"
IMPL_BRANCH="impl/${TASK_SLUG}"

# Get current branch (this is the PR target)
SOURCE_BRANCH=$(git branch --show-current)

if [ -z "$SOURCE_BRANCH" ]; then
    echo '{"error": "Not on a branch (detached HEAD?)"}'
    exit 1
fi

# Check if worktree already exists
if [ -d "$WORKTREE_PATH" ]; then
    echo "{\"error\": \"Worktree already exists\", \"path\": \"$WORKTREE_PATH\"}"
    exit 1
fi

# Check if branch already exists
if git show-ref --verify --quiet "refs/heads/$IMPL_BRANCH"; then
    echo "{\"error\": \"Branch already exists\", \"branch\": \"$IMPL_BRANCH\"}"
    exit 1
fi

# Ensure worktrees directory exists
mkdir -p "$WORKTREE_DIR"

# Ensure .shipkit/worktrees is in .gitignore
GITIGNORE=".gitignore"
if [ -f "$GITIGNORE" ]; then
    if ! grep -q "^\.shipkit/worktrees" "$GITIGNORE"; then
        echo "" >> "$GITIGNORE"
        echo "# Shipkit independent implementation worktrees" >> "$GITIGNORE"
        echo ".shipkit/worktrees/" >> "$GITIGNORE"
    fi
else
    echo "# Shipkit independent implementation worktrees" > "$GITIGNORE"
    echo ".shipkit/worktrees/" >> "$GITIGNORE"
fi

# Create worktree with new branch from current HEAD
git worktree add -b "$IMPL_BRANCH" "$WORKTREE_PATH" HEAD

# Verify creation
if [ -d "$WORKTREE_PATH" ]; then
    # Get absolute path
    ABS_PATH=$(cd "$WORKTREE_PATH" && pwd)

    echo "{
  \"success\": true,
  \"task_slug\": \"$TASK_SLUG\",
  \"worktree_path\": \"$WORKTREE_PATH\",
  \"absolute_path\": \"$ABS_PATH\",
  \"impl_branch\": \"$IMPL_BRANCH\",
  \"source_branch\": \"$SOURCE_BRANCH\"
}"
else
    echo '{"error": "Worktree creation failed - directory not found"}'
    exit 1
fi
