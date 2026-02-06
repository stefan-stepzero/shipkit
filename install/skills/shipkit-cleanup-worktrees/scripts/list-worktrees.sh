#!/usr/bin/env bash
#
# list-worktrees.sh - List all implementation worktrees with status
#
# Usage: list-worktrees.sh
#
# Returns JSON array of worktrees with age and PR status.

set -e

WORKTREE_DIR=".shipkit/worktrees"

# Check if worktrees directory exists
if [ ! -d "$WORKTREE_DIR" ]; then
    echo '{"worktrees": [], "count": 0}'
    exit 0
fi

# Get list of worktrees
WORKTREES=$(ls -1 "$WORKTREE_DIR" 2>/dev/null || echo "")

if [ -z "$WORKTREES" ]; then
    echo '{"worktrees": [], "count": 0}'
    exit 0
fi

# Check if gh is available for PR status
HAS_GH="false"
if command -v gh &> /dev/null && gh auth status &> /dev/null 2>&1; then
    HAS_GH="true"
fi

# Build JSON array
echo "{"
echo '  "worktrees": ['

FIRST="true"
COUNT=0

while IFS= read -r SLUG; do
    [ -z "$SLUG" ] && continue
    [ ! -d "$WORKTREE_DIR/$SLUG" ] && continue

    COUNT=$((COUNT + 1))

    if [ "$FIRST" = "true" ]; then
        FIRST="false"
    else
        echo ","
    fi

    # Get worktree age in days
    CREATED=$(stat -c %Y "$WORKTREE_DIR/$SLUG" 2>/dev/null || stat -f %m "$WORKTREE_DIR/$SLUG" 2>/dev/null || echo "0")
    NOW=$(date +%s)
    AGE_DAYS=$(( (NOW - CREATED) / 86400 ))

    # Branch name
    IMPL_BRANCH="impl/$SLUG"

    # Get PR status if gh is available
    PR_NUMBER="null"
    PR_STATE="null"
    PR_URL="null"

    if [ "$HAS_GH" = "true" ]; then
        PR_JSON=$(gh pr list --head "$IMPL_BRANCH" --state all --json number,state,url --limit 1 2>/dev/null || echo "[]")
        if [ "$PR_JSON" != "[]" ]; then
            PR_NUMBER=$(echo "$PR_JSON" | jq -r '.[0].number')
            PR_STATE=$(echo "$PR_JSON" | jq -r '.[0].state')
            PR_URL=$(echo "$PR_JSON" | jq -r '.[0].url')
        fi
    fi

    # Determine recommendation
    RECOMMENDATION="keep"
    if [ "$PR_STATE" = "MERGED" ] || [ "$PR_STATE" = "CLOSED" ]; then
        RECOMMENDATION="clean"
    elif [ "$PR_STATE" = "null" ] && [ "$AGE_DAYS" -gt 7 ]; then
        RECOMMENDATION="review"
    elif [ "$PR_STATE" = "OPEN" ] && [ "$AGE_DAYS" -gt 7 ]; then
        RECOMMENDATION="review"
    fi

    # Output JSON object
    printf '    {
      "slug": "%s",
      "path": "%s/%s",
      "branch": "%s",
      "age_days": %d,
      "pr_number": %s,
      "pr_state": %s,
      "pr_url": %s,
      "recommendation": "%s"
    }' "$SLUG" "$WORKTREE_DIR" "$SLUG" "$IMPL_BRANCH" "$AGE_DAYS" \
       "$( [ "$PR_NUMBER" = "null" ] && echo "null" || echo "$PR_NUMBER" )" \
       "$( [ "$PR_STATE" = "null" ] && echo "null" || echo "\"$PR_STATE\"" )" \
       "$( [ "$PR_URL" = "null" ] && echo "null" || echo "\"$PR_URL\"" )" \
       "$RECOMMENDATION"

done <<< "$WORKTREES"

echo ""
echo "  ],"
echo "  \"count\": $COUNT,"
echo "  \"has_gh\": $HAS_GH"
echo "}"
