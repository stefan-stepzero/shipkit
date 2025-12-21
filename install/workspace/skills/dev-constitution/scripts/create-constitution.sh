#!/usr/bin/env bash
# create-constitution.sh - Create or update technical constitution
# Part of shipkit dev-constitution skill

set -e

# Source shared utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
source "$REPO_ROOT/.shipkit/scripts/bash/common.sh"

# Get skill directory
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT_DIR="$SKILL_DIR/outputs"
TEMPLATE_DIR="$SKILL_DIR/templates"
REFERENCES_DIR="$SKILL_DIR/references"

# Parse flags
UPDATE=false
ARCHIVE=false
SKIP_PREREQS=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --create)
      # Explicit create flag (default behavior)
      shift
      ;;
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
      echo "Usage: $0 [--create|--update|--archive|--skip-prereqs|--cancel]"
      echo ""
      echo "Flags:"
      echo "  --create        Create initial constitution (default)"
      echo "  --update        Update existing constitution"
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
check_skill_prerequisites "dev-constitution" "$SKIP_PREREQS"

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

# Output file location
OUTPUT_FILE="$OUTPUT_DIR/constitution.md"

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}    Technical Constitution${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check if file exists and handle decision
check_output_exists "$OUTPUT_FILE" "Technical constitution" "$UPDATE" "$ARCHIVE"

# Check if template exists
TEMPLATE_FILE="$TEMPLATE_DIR/constitution-template.md"
if [[ ! -f "$TEMPLATE_FILE" ]]; then
  echo -e "${RED}✗${NC} Template not found: $TEMPLATE_FILE"
  exit 1
fi

echo -e "${GREEN}✓${NC} Template available: $TEMPLATE_FILE"
echo -e "${CYAN}Output file:${NC} $OUTPUT_FILE"
echo ""

# List available product artifacts for Claude to read
echo -e "${CYAN}Available product artifacts to extract from:${NC}"

PROD_SKILLS_DIR="$REPO_ROOT/.shipkit/skills"

# Check for product artifacts
ARTIFACTS_FOUND=false

if [[ -f "$PROD_SKILLS_DIR/prod-user-stories/outputs/user-stories.md" ]]; then
  echo -e "${GREEN}✓${NC} User stories: $PROD_SKILLS_DIR/prod-user-stories/outputs/user-stories.md"
  ARTIFACTS_FOUND=true
fi

if [[ -f "$PROD_SKILLS_DIR/prod-strategic-thinking/outputs/business-canvas.md" ]]; then
  echo -e "${GREEN}✓${NC} Strategy: $PROD_SKILLS_DIR/prod-strategic-thinking/outputs/business-canvas.md"
  ARTIFACTS_FOUND=true
fi

if [[ -f "$PROD_SKILLS_DIR/prod-success-metrics/outputs/success-metrics.md" ]]; then
  echo -e "${GREEN}✓${NC} Success metrics: $PROD_SKILLS_DIR/prod-success-metrics/outputs/success-metrics.md"
  ARTIFACTS_FOUND=true
fi

if [[ -f "$PROD_SKILLS_DIR/prod-assumptions-and-risks/outputs/assumptions-and-risks.md" ]]; then
  echo -e "${GREEN}✓${NC} Assumptions & risks: $PROD_SKILLS_DIR/prod-assumptions-and-risks/outputs/assumptions-and-risks.md"
  ARTIFACTS_FOUND=true
fi

if [[ -f "$PROD_SKILLS_DIR/prod-constitution-builder/outputs/product-constitution.md" ]]; then
  echo -e "${GREEN}✓${NC} Product constitution: $PROD_SKILLS_DIR/prod-constitution-builder/outputs/product-constitution.md"
  ARTIFACTS_FOUND=true
fi

if [[ "$ARTIFACTS_FOUND" == "false" ]]; then
  echo -e "${YELLOW}⚠${NC} No product artifacts found. Constitution will be minimal."
fi

echo ""
echo -e "${CYAN}References available:${NC}"
if [[ -d "$REFERENCES_DIR" ]]; then
  find "$REFERENCES_DIR" -type f -name "*.md" | while read ref; do
    echo -e "${GREEN}✓${NC} $(basename $ref): $ref"
  done
fi

echo ""
echo "Ready for Claude to create technical constitution via dialogue"
echo ""
echo -e "${YELLOW}Remember:${NC} Keep it LEAN (<500 words), HIGH-LEVEL principles only"

exit 0
