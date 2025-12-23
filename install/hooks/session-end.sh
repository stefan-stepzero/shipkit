#!/usr/bin/env bash
# session-end.sh - Document session progress on /clear
#
# This hook runs when a Claude Code session ends.
# We ONLY save state when the user runs /clear (reason: "clear").
#
# Why? Because:
# - Regular logout/exit → User will resume the same conversation (no state needed)
# - /clear → User wants fresh conversation but should remember progress

set -e

# Read hook input
INPUT=$(cat)
REASON=$(echo "$INPUT" | jq -r '.reason')
TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path')

# Only save state when user runs /clear
if [[ "$REASON" != "clear" ]]; then
  exit 0
fi

# Ensure progress directory exists
mkdir -p .shipkit/progress

# Archive existing state if present
STATE_FILE=".shipkit/progress/state.md"
if [[ -f "$STATE_FILE" ]]; then
  TIMESTAMP=$(date +%Y%m%d-%H%M%S)
  ARCHIVE_FILE=".shipkit/progress/state-$TIMESTAMP.md"
  mv "$STATE_FILE" "$ARCHIVE_FILE"
fi

# Exit early if no transcript
if [[ ! -f "$TRANSCRIPT_PATH" ]]; then
  exit 0
fi

# Parse transcript for last skill used
LAST_SKILL=$(grep -o '"tool_name":"Skill"' "$TRANSCRIPT_PATH" 2>/dev/null | tail -1)
if [[ -z "$LAST_SKILL" ]]; then
  # No skills used in this session
  exit 0
fi

# Get the actual skill name
LAST_SKILL_NAME=$(grep '"tool_name":"Skill"' "$TRANSCRIPT_PATH" | \
                  grep -o '"skill":"[^"]*"' | \
                  tail -1 | \
                  cut -d'"' -f4)

# Determine next skill suggestion based on workflow chain
NEXT_SKILL=""
case "$LAST_SKILL_NAME" in
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
  dev-constitution) NEXT_SKILL="dev-specify" ;;
  dev-specify) NEXT_SKILL="dev-plan" ;;
  dev-plan) NEXT_SKILL="dev-tasks" ;;
  dev-tasks) NEXT_SKILL="dev-implement" ;;
  dev-implement) NEXT_SKILL="dev-finish" ;;
  dev-roadmap) NEXT_SKILL="dev-plan (first spec)" ;;
  *) NEXT_SKILL="Check /shipkit-master" ;;
esac

# Try to detect project type from constitution
PROJECT_INFO="Unknown"
CONSTITUTION=".shipkit/skills/prod-constitution-builder/outputs/product-constitution.md"
if [[ -f "$CONSTITUTION" ]]; then
  # Try to extract project type
  PROJECT_LINE=$(grep -i "project type\|product stage" "$CONSTITUTION" 2>/dev/null | head -1 || echo "")
  if [[ -n "$PROJECT_LINE" ]]; then
    PROJECT_INFO=$(echo "$PROJECT_LINE" | sed 's/^[*#-]*//' | sed 's/^[ \t]*//' | cut -c1-50)
  fi
fi

# Count output files
OUTPUT_COUNT=$(find .shipkit/skills/*/outputs -type f -name "*.md" 2>/dev/null | wc -l)

# Write concise state
cat > "$STATE_FILE" << EOF
Last: /$LAST_SKILL_NAME
Next: /$NEXT_SKILL
Project: $PROJECT_INFO
Files: $OUTPUT_COUNT outputs
EOF

exit 0
