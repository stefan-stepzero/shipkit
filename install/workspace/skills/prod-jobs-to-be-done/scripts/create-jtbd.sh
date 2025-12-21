#!/usr/bin/env bash
set -e

# Source shared utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
source "$REPO_ROOT/.shipkit/scripts/bash/common.sh"

# Get skill directory
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT_DIR="$SKILL_DIR/outputs"
TEMPLATE_DIR="$SKILL_DIR/templates"

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

# Output file location
OUTPUT_FILE="$OUTPUT_DIR/jobs-to-be-done.md"

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}    Jobs-to-be-Done Mapping${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check if file already exists
if [[ -f "$OUTPUT_FILE" ]]; then
  echo -e "${YELLOW}⚠${NC}  Jobs-to-be-Done mapping already exists at: $OUTPUT_FILE"
  echo ""
  echo "Options:"
  echo "  1. Update existing JTBD mapping"
  echo "  2. Create new version (archive current)"
  echo "  3. Cancel"
  read -p "Choice [1-3]: " choice

  case $choice in
    1)
      echo -e "${CYAN}Updating existing JTBD mapping...${NC}"
      ;;
    2)
      TIMESTAMP=$(date +%Y%m%d-%H%M%S)
      ARCHIVE_FILE="$OUTPUT_DIR/jobs-to-be-done-$TIMESTAMP.md"
      mv "$OUTPUT_FILE" "$ARCHIVE_FILE"
      echo -e "${GREEN}✓${NC} Archived to: $ARCHIVE_FILE"
      ;;
    3)
      echo "Cancelled."
      exit 0
      ;;
    *)
      echo "Invalid choice. Cancelled."
      exit 1
      ;;
  esac
fi

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
