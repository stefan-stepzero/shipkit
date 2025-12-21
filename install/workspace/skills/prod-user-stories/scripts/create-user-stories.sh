#!/usr/bin/env bash
# create-user-stories.sh - Create or update user stories from interaction design
# Part of shipkit prod-user-stories skill

set -e

# Source shared utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
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
      echo "  --update        Update existing user stories"
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

# Check prerequisites
check_skill_prerequisites "prod-user-stories" "$SKIP_PREREQS"

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

# Output file location
OUTPUT_FILE="$OUTPUT_DIR/user-stories.md"

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}    User Stories${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check if file exists and handle decision
check_output_exists "$OUTPUT_FILE" "User stories" "$UPDATE" "$ARCHIVE"

# Check if template exists
TEMPLATE_FILE="$TEMPLATE_DIR/user-stories-template.md"
if [[ ! -f "$TEMPLATE_FILE" ]]; then
  echo -e "${RED}✗${NC} Template not found: $TEMPLATE_FILE"
  exit 1
fi

echo -e "${GREEN}✓${NC} Template available: $TEMPLATE_FILE"
echo -e "${CYAN}Output file:${NC} $OUTPUT_FILE"
echo ""
echo "Ready for Claude to create user stories via dialogue"

exit 0
