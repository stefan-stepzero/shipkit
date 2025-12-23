#!/usr/bin/env bash
# create-jtbd.sh - Create Jobs-to-be-Done mapping
# Part of shipkit prod-jobs-to-be-done skill

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
      echo "  --update        Update existing JTBD mapping"
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
check_skill_prerequisites "prod-jobs-to-be-done" "$SKIP_PREREQS"

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

# Output file location
OUTPUT_FILE="$OUTPUT_DIR/jobs-to-be-done.md"

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}    Jobs-to-be-Done Mapping${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check if file exists and handle decision
check_output_exists "$OUTPUT_FILE" "Jobs-to-be-Done mapping" "$UPDATE" "$ARCHIVE"

# Check if template exists
TEMPLATE_FILE="$TEMPLATE_DIR/jtbd-template.md"
if [[ ! -f "$TEMPLATE_FILE" ]]; then
  echo -e "${RED}✗${NC} Template not found: $TEMPLATE_FILE"
  exit 1
fi

# If this is a new file, create it with header
if [[ ! -f "$OUTPUT_FILE" ]]; then
  cat > "$OUTPUT_FILE" << 'EOF'
# Jobs-to-be-Done Mapping

**Generated:** $(date +%Y-%m-%d)
**Last Updated:** $(date +%Y-%m-%d)

---

EOF
  echo -e "${GREEN}✓${NC} Created: $OUTPUT_FILE"
else
  # Update timestamp
  sed -i "s/\*\*Last Updated:\*\*.*/\*\*Last Updated:\*\* $(date +%Y-%m-%d)/" "$OUTPUT_FILE"
  echo -e "${GREEN}✓${NC} Updated: $OUTPUT_FILE"
fi

echo ""
echo -e "${CYAN}Template available at:${NC} $TEMPLATE_FILE"
echo -e "${CYAN}References available in:${NC} $SKILL_DIR/references/"
echo ""
echo -e "${GREEN}✓${NC} Ready to map jobs-to-be-done"
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

exit 0
