#!/usr/bin/env bash
# create-constitution.sh - Create or update technical constitution
# Part of shipkit dev-constitution skill

set -e

# =============================================================================
# SETUP
# =============================================================================

# Source shared utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
source "$REPO_ROOT/.shipkit/scripts/bash/common.sh"

# Get skill directory
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT_DIR="$SKILL_DIR/outputs"
TEMPLATE_DIR="$SKILL_DIR/templates"
REFERENCES_DIR="$SKILL_DIR/references"

# =============================================================================
# PARSE FLAGS
# =============================================================================

CREATE=false
UPDATE=false
ARCHIVE=false
SKIP_PREREQS=false
INTERACTIVE=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --create) CREATE=true; shift ;;
    --update) UPDATE=true; shift ;;
    --archive) ARCHIVE=true; shift ;;
    --skip-prereqs) SKIP_PREREQS=true; shift ;;
    --interactive) INTERACTIVE=true; shift ;;
    --cancel) echo "Cancelled."; exit 0 ;;
    --help|-h)
      echo "Usage: $0 [--create|--update|--archive|--skip-prereqs|--interactive|--cancel]"
      echo ""
      echo "Flags:"
      echo "  --create        Force creation (default: auto-detects mode)"
      echo "  --update        Update existing constitution with versioning"
      echo "  --archive       Archive current version and create new"
      echo "  --skip-prereqs  Skip prerequisite checks"
      echo "  --interactive   Force interactive mode (ignore product artifacts)"
      echo "  --cancel        Cancel operation"
      echo "  --help, -h      Show this help message"
      exit 0
      ;;
    *) echo "Unknown flag: $1" >&2; exit 1 ;;
  esac
done

# =============================================================================
# CHECK PREREQUISITES
# =============================================================================

# Constitution is recommended after prod-user-stories but not strictly required
if [[ "$SKIP_PREREQS" == "false" ]]; then
  check_skill_prerequisites "dev-constitution" "$SKIP_PREREQS"
fi

# =============================================================================
# ENSURE DIRECTORIES EXIST
# =============================================================================

mkdir -p "$OUTPUT_DIR"

# =============================================================================
# OUTPUT FILE LOCATION
# =============================================================================

OUTPUT_FILE="$OUTPUT_DIR/constitution.md"

# =============================================================================
# CHECK IF FILE EXISTS AND HANDLE DECISION
# =============================================================================

check_output_exists "$OUTPUT_FILE" "Technical Constitution" "$UPDATE" "$ARCHIVE"

# =============================================================================
# CHECK TEMPLATE EXISTS
# =============================================================================

TEMPLATE_FILE="$TEMPLATE_DIR/constitution-template.md"
if [[ ! -f "$TEMPLATE_FILE" ]]; then
  echo -e "${RED}✗${NC} Template not found: $TEMPLATE_FILE"
  exit 1
fi

echo -e "${GREEN}✓${NC} Template available: $TEMPLATE_FILE"

# =============================================================================
# SCAN FOR PRODUCT ARTIFACTS
# =============================================================================

echo ""
echo -e "${CYAN}Scanning for product artifacts...${NC}"
echo ""

PROD_ARTIFACTS_DIR="$REPO_ROOT/.shipkit/skills"
ARTIFACTS_FOUND=0

# Product artifacts to look for
declare -A PRODUCT_ARTIFACTS=(
  ["prod-strategic-thinking"]="prod-strategic-thinking/outputs/business-canvas.md"
  ["prod-constitution-builder"]="prod-constitution-builder/outputs/product-constitution.md"
  ["prod-personas"]="prod-personas/outputs/personas.md"
  ["prod-jobs-to-be-done"]="prod-jobs-to-be-done/outputs/jobs-to-be-done.md"
  ["prod-market-analysis"]="prod-market-analysis/outputs/market-analysis.md"
  ["prod-brand-guidelines"]="prod-brand-guidelines/outputs/brand-guidelines.md"
  ["prod-interaction-design"]="prod-interaction-design/outputs/interaction-design.md"
  ["prod-user-stories"]="prod-user-stories/outputs/user-stories.md"
  ["prod-assumptions-and-risks"]="prod-assumptions-and-risks/outputs/assumptions-and-risks.md"
  ["prod-success-metrics"]="prod-success-metrics/outputs/success-metrics.md"
)

FOUND_ARTIFACTS=()

for skill in "${!PRODUCT_ARTIFACTS[@]}"; do
  artifact_path="${PRODUCT_ARTIFACTS[$skill]}"
  full_path="$PROD_ARTIFACTS_DIR/$artifact_path"

  if [[ -f "$full_path" ]]; then
    echo -e "  ${GREEN}✓${NC} Found: $artifact_path"
    FOUND_ARTIFACTS+=("$full_path")
    ARTIFACTS_FOUND=$((ARTIFACTS_FOUND + 1))
  fi
done

if [[ $ARTIFACTS_FOUND -eq 0 ]]; then
  echo -e "  ${YELLOW}⚠${NC} No product artifacts found"
fi

echo ""

# =============================================================================
# DETERMINE MODE
# =============================================================================

MODE="interactive"

if [[ "$INTERACTIVE" == "true" ]]; then
  echo -e "${CYAN}Mode:${NC} Interactive (forced by --interactive flag)"
  echo "Product artifacts will be ignored."
elif [[ $ARTIFACTS_FOUND -gt 0 ]]; then
  MODE="extraction"
  echo -e "${CYAN}Mode:${NC} Automatic Extraction"
  echo "Found $ARTIFACTS_FOUND product artifacts to extract from."
  echo ""
  echo -e "${CYAN}Extraction Strategy:${NC}"
  echo "  • Read product artifacts for technical implications"
  echo "  • Auto-generate initial constitution draft"
  echo "  • Claude will refine with user dialogue"
else
  echo -e "${CYAN}Mode:${NC} Interactive Dialogue"
  echo "No product artifacts found. Constitution will be built through conversation."
fi

echo ""

# =============================================================================
# REFERENCE FILES
# =============================================================================

echo -e "${CYAN}Available references:${NC}"
if [[ -f "$REFERENCES_DIR/reference.md" ]]; then
  echo -e "  ${GREEN}✓${NC} $REFERENCES_DIR/reference.md"
else
  echo -e "  ${YELLOW}⚠${NC} $REFERENCES_DIR/reference.md (missing)"
fi

if [[ -f "$REFERENCES_DIR/examples.md" ]]; then
  echo -e "  ${GREEN}✓${NC} $REFERENCES_DIR/examples.md"
else
  echo -e "  ${YELLOW}⚠${NC} $REFERENCES_DIR/examples.md (missing)"
fi

echo ""

# =============================================================================
# READY FOR CLAUDE
# =============================================================================

echo -e "${GREEN}✓${NC} Ready for Claude to create Technical Constitution"
echo ""
echo -e "${CYAN}Next Steps:${NC}"
echo "  1. Claude reads template: $TEMPLATE_FILE"
echo "  2. Claude reads references in: $REFERENCES_DIR/"
if [[ "$MODE" == "extraction" ]]; then
  echo "  3. Claude reads ${#FOUND_ARTIFACTS[@]} product artifacts"
  echo "  4. Claude auto-extracts technical constraints"
  echo "  5. Claude generates draft constitution"
  echo "  6. User reviews and refines sections"
else
  echo "  3. Claude asks clarifying questions (interactive)"
  echo "  4. User provides technical preferences and constraints"
  echo "  5. Claude generates constitution from responses"
fi
echo "  7. Claude writes to: $OUTPUT_FILE"
echo ""
echo -e "${CYAN}Output location:${NC} $OUTPUT_FILE"
echo ""

# If extraction mode, output artifact list for Claude
if [[ "$MODE" == "extraction" && ${#FOUND_ARTIFACTS[@]} -gt 0 ]]; then
  echo -e "${CYAN}Product artifacts to read:${NC}"
  for artifact in "${FOUND_ARTIFACTS[@]}"; do
    echo "  • $artifact"
  done
  echo ""
fi

echo -e "${YELLOW}Remember:${NC} Keep it LEAN (<500 words), HIGH-LEVEL principles only"
echo ""

exit 0
