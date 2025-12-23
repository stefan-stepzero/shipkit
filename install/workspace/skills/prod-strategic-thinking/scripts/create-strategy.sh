#!/usr/bin/env bash
# create-strategy.sh - Create business strategy canvas
# Part of shipkit prod-strategic-thinking skill

set -e

# Source shared utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
source "$REPO_ROOT/.shipkit/scripts/bash/common.sh"

# Get skill directory
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT_DIR="$SKILL_DIR/outputs"
TEMPLATE_DIR="$SKILL_DIR/templates"

# Parse flags
UPDATE=false
ARCHIVE=false
SKIP_PREREQS=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --update)
      UPDATE=true
      shift
      ;;
    --archive)
      ARCHIVE=true
      shift
      ;;
    --skip-prereqs)
      SKIP_PREREQS=true
      shift
      ;;
    --cancel)
      echo "Cancelled."
      exit 0
      ;;
    --help|-h)
      echo "Usage: $0 [--update|--archive|--skip-prereqs|--cancel]"
      echo ""
      echo "Flags:"
      echo "  --update        Update existing strategy"
      echo "  --archive       Archive current and create new version"
      echo "  --skip-prereqs  Skip prerequisite checks"
      echo "  --cancel        Cancel operation"
      exit 0
      ;;
    *)
      echo -e "${RED}Unknown flag: $1${NC}" >&2
      exit 1
      ;;
  esac
done

# Check prerequisites (strategic-thinking has none, but this shows the pattern)
check_skill_prerequisites "prod-strategic-thinking" "$SKIP_PREREQS"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Output file location
OUTPUT_FILE="$OUTPUT_DIR/business-canvas.md"

# Check if file exists and handle decision
check_output_exists "$OUTPUT_FILE" "Strategy" "$UPDATE" "$ARCHIVE"

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
