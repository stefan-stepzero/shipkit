#!/usr/bin/env bash
#
# get-pr-status.sh - Get PR status for a branch
#
# Usage: get-pr-status.sh <branch-name>
#
# Returns JSON with PR state (OPEN, MERGED, CLOSED) or null if no PR exists.

set -e

BRANCH="$1"

if [ -z "$BRANCH" ]; then
    echo '{"error": "Branch name required", "usage": "get-pr-status.sh <branch-name>"}'
    exit 1
fi

# Check if gh is available
if ! command -v gh &> /dev/null; then
    echo '{"error": "GitHub CLI (gh) not found"}'
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo '{"error": "GitHub CLI not authenticated. Run: gh auth login"}'
    exit 1
fi

# Get PR info for this branch
PR_JSON=$(gh pr list --head "$BRANCH" --state all --json number,state,url,title,mergedAt,closedAt --limit 1 2>/dev/null || echo "[]")

if [ "$PR_JSON" = "[]" ]; then
    echo "{
  \"branch\": \"$BRANCH\",
  \"has_pr\": false,
  \"state\": null
}"
else
    # Parse the first (should be only) PR
    NUMBER=$(echo "$PR_JSON" | jq -r '.[0].number')
    STATE=$(echo "$PR_JSON" | jq -r '.[0].state')
    URL=$(echo "$PR_JSON" | jq -r '.[0].url')
    TITLE=$(echo "$PR_JSON" | jq -r '.[0].title')
    MERGED_AT=$(echo "$PR_JSON" | jq -r '.[0].mergedAt')
    CLOSED_AT=$(echo "$PR_JSON" | jq -r '.[0].closedAt')

    echo "{
  \"branch\": \"$BRANCH\",
  \"has_pr\": true,
  \"number\": $NUMBER,
  \"state\": \"$STATE\",
  \"url\": \"$URL\",
  \"title\": \"$TITLE\",
  \"merged_at\": $([ "$MERGED_AT" = "null" ] && echo "null" || echo "\"$MERGED_AT\""),
  \"closed_at\": $([ "$CLOSED_AT" = "null" ] && echo "null" || echo "\"$CLOSED_AT\"")
}"
fi
