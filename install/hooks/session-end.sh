#!/usr/bin/env bash
# session-end.sh - Document session progress on /clear
#
# This hook runs when a Claude Code session ends.
# We save minimal state to help resume context in the next session.

set -e

# Ensure progress directory exists
mkdir -p .shipkit/progress

# Archive existing state if present
STATE_FILE=".shipkit/progress/state.md"
if [[ -f "$STATE_FILE" ]]; then
  TIMESTAMP=$(date +%Y%m%d-%H%M%S 2>/dev/null || echo "backup")
  ARCHIVE_FILE=".shipkit/progress/state-$TIMESTAMP.md"
  mv "$STATE_FILE" "$ARCHIVE_FILE" 2>/dev/null || true
fi

# Find the last completed skill by checking for output files
LAST_SKILL=""

# Check product skills
for skill in prod-strategic-thinking prod-constitution-builder prod-personas \
             prod-jobs-to-be-done prod-market-analysis prod-brand-guidelines \
             prod-interaction-design prod-user-stories prod-assumptions-and-risks \
             prod-success-metrics; do
    OUTPUT_DIR=".shipkit/skills/$skill/outputs"
    if [[ -d "$OUTPUT_DIR" ]]; then
        # Find most recently modified file (portable - no -printf)
        LATEST_FILE=$(find "$OUTPUT_DIR" -type f -name "*.md" 2>/dev/null | head -1)
        if [[ -n "$LATEST_FILE" ]]; then
            LAST_SKILL="$skill"
        fi
    fi
done

# Check dev skills if no product skill found
if [[ -z "$LAST_SKILL" ]]; then
    for skill in dev-constitution-builder dev-specify dev-plan dev-tasks \
                 dev-implement dev-roadmap dev-finish; do
        OUTPUT_DIR=".shipkit/skills/$skill/outputs"
        if [[ -d "$OUTPUT_DIR" ]]; then
            LATEST_FILE=$(find "$OUTPUT_DIR" -type f -name "*.md" 2>/dev/null | head -1)
            if [[ -n "$LATEST_FILE" ]]; then
                LAST_SKILL="$skill"
            fi
        fi
    done
fi

# If no skill outputs found, exit quietly
if [[ -z "$LAST_SKILL" ]]; then
    exit 0
fi

# Determine next skill suggestion based on workflow chain
NEXT_SKILL=""
case "$LAST_SKILL" in
  prod-strategic-thinking) NEXT_SKILL="prod-constitution-builder" ;;
  prod-constitution-builder) NEXT_SKILL="prod-personas" ;;
  prod-personas) NEXT_SKILL="prod-jobs-to-be-done" ;;
  prod-jobs-to-be-done) NEXT_SKILL="prod-market-analysis" ;;
  prod-market-analysis) NEXT_SKILL="prod-brand-guidelines" ;;
  prod-brand-guidelines) NEXT_SKILL="prod-interaction-design" ;;
  prod-interaction-design) NEXT_SKILL="prod-user-stories" ;;
  prod-user-stories) NEXT_SKILL="prod-assumptions-and-risks or dev-constitution" ;;
  prod-assumptions-and-risks) NEXT_SKILL="prod-success-metrics" ;;
  prod-success-metrics) NEXT_SKILL="dev-constitution" ;;
  dev-constitution-builder) NEXT_SKILL="dev-specify" ;;
  dev-specify) NEXT_SKILL="dev-plan" ;;
  dev-plan) NEXT_SKILL="dev-tasks" ;;
  dev-tasks) NEXT_SKILL="dev-implement" ;;
  dev-implement) NEXT_SKILL="dev-finish" ;;
  dev-roadmap) NEXT_SKILL="dev-plan (first spec)" ;;
  *) NEXT_SKILL="See /shipkit-master" ;;
esac

# Try to detect project type from constitution
PROJECT_INFO="Not set"
CONSTITUTION=".shipkit/skills/prod-constitution-builder/outputs/product-constitution.md"
if [[ -f "$CONSTITUTION" ]]; then
  PROJECT_LINE=$(grep -i "project type\|product stage" "$CONSTITUTION" 2>/dev/null | head -1 || echo "")
  if [[ -n "$PROJECT_LINE" ]]; then
    PROJECT_INFO=$(echo "$PROJECT_LINE" | sed 's/^[*#-]*//' | sed 's/^[ \t]*//' | cut -c1-50)
  fi
fi

# Count output files
OUTPUT_COUNT=$(find .shipkit/skills/*/outputs -type f -name "*.md" 2>/dev/null | wc -l || echo 0)

# Write concise state
cat > "$STATE_FILE" << EOF
**Previous Session Summary**

Last completed: /$LAST_SKILL
Suggested next: /$NEXT_SKILL
Project type: $PROJECT_INFO
Output files: $OUTPUT_COUNT
EOF

exit 0
