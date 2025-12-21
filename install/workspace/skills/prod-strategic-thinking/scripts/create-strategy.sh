#!/usr/bin/env bash
# create-strategy.sh - Create business strategy canvas
# Part of shipkit prod-strategic-thinking skill

set -e

# Source shared utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
source "$REPO_ROOT/.shipkit/scripts/bash/common.sh"

# Get skill directory
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT_DIR="$SKILL_DIR/outputs"
TEMPLATE_DIR="$SKILL_DIR/templates"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Output file location
OUTPUT_FILE="$OUTPUT_DIR/business-canvas.md"

# Check if file already exists
if [[ -f "$OUTPUT_FILE" ]]; then
  echo -e "${YELLOW}⚠${NC}  Strategy already exists at: $OUTPUT_FILE"
  echo ""
  echo "Options:"
  echo "  1. Update existing strategy"
  echo "  2. Create new version (archive current)"
  echo "  3. Cancel"
  read -p "Choice [1-3]: " choice

  case $choice in
    1)
      echo -e "${GREEN}✓${NC} Proceeding with update to existing strategy"
      ;;
    2)
      # Archive existing
      TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
      ARCHIVE_FILE="$OUTPUT_DIR/business-canvas-${TIMESTAMP}.md"
      mv "$OUTPUT_FILE" "$ARCHIVE_FILE"
      echo -e "${GREEN}✓${NC} Archived existing strategy to: $ARCHIVE_FILE"
      ;;
    3)
      echo "Cancelled."
      exit 0
      ;;
    *)
      echo -e "${RED}Invalid choice${NC}"
      exit 1
      ;;
  esac
fi

# Use template
TEMPLATE="$TEMPLATE_DIR/business-canvas-template.md"

if [[ -f "$TEMPLATE" ]]; then
  cp "$TEMPLATE" "$OUTPUT_FILE"
  echo -e "${GREEN}✓${NC} Created business canvas at: $OUTPUT_FILE"
  echo ""
  echo "Next: Claude will guide you through filling out each section via dialogue"
else
  echo -e "${RED}✗${NC} Template not found: $TEMPLATE"
  exit 1
fi

exit 0
