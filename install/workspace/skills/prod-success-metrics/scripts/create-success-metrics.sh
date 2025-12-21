#!/usr/bin/env bash
set -e

# Get script directory and repo root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"

# Source common utilities
source "$REPO_ROOT/.shipkit/scripts/bash/common.sh"

# Skill configuration
SKILL_NAME="prod-success-metrics"
OUTPUT_FILE="$REPO_ROOT/.shipkit/skills/$SKILL_NAME/outputs/success-metrics.md"
TEMPLATE_FILE="$REPO_ROOT/.shipkit/skills/$SKILL_NAME/templates/success-metrics-template.md"

# Parse flags
UPDATE_MODE=false
ARCHIVE_MODE=false
SKIP_PREREQS=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --update) UPDATE_MODE=true; shift ;;
    --archive) ARCHIVE_MODE=true; shift ;;
    --skip-prereqs) SKIP_PREREQS=true; shift ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

# Check prerequisites (unless skipped)
if [ "$SKIP_PREREQS" = false ]; then
  check_skill_prerequisites "$SKILL_NAME" "$SKIP_PREREQS"
fi

# Handle existing file
if [ -f "$OUTPUT_FILE" ]; then
  if [ "$ARCHIVE_MODE" = true ]; then
    archive_file "$OUTPUT_FILE"
    echo "Archived existing success-metrics.md"
  elif [ "$UPDATE_MODE" = true ]; then
    echo "Updating existing success-metrics.md"
  else
    echo "success-metrics.md already exists."
    echo "Use --update to modify or --archive to save and recreate"
    exit 1
  fi
fi

# Create output directory if needed
mkdir -p "$(dirname "$OUTPUT_FILE")"

# Copy template to output (if not updating)
if [ "$UPDATE_MODE" = false ]; then
  cp "$TEMPLATE_FILE" "$OUTPUT_FILE"
  echo "Created: $OUTPUT_FILE"
else
  echo "Ready to update: $OUTPUT_FILE"
fi

# Success message
echo ""
echo "✅ Success metrics initialized"
echo ""
echo "Next steps:"
echo "1. Define success metrics for your product stage"
echo "2. Set up instrumentation and tracking"
echo "3. Establish baselines and targets"
echo ""
echo "References available in: $REPO_ROOT/.shipkit/skills/$SKILL_NAME/references/"
