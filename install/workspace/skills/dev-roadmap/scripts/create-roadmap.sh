#!/usr/bin/env bash
# Create development roadmap from user stories
set -euo pipefail

# =============================================================================
# FLAG PARSING
# =============================================================================

UPDATE=false
ARCHIVE=false
SKIP_PREREQS=false

show_help() {
  cat << 'EOF'
Usage: create-roadmap.sh [OPTIONS]

Create a development roadmap that sequences features by technical dependencies.

OPTIONS:
  --update        Update existing roadmap (preserves old version)
  --archive       Archive current and create new version
  --skip-prereqs  Skip prerequisite checks (dangerous)
  --help, -h      Show this help message

EXAMPLES:
  # Create new roadmap
  ./create-roadmap.sh

  # Update existing roadmap
  ./create-roadmap.sh --update

  # Archive old and create new
  ./create-roadmap.sh --archive

PREREQUISITES:
  - User stories must exist (.shipkit/skills/prod-user-stories/outputs/user-stories.md)
  - Constitution must exist (.shipkit/skills/dev-constitution/outputs/constitution.md)

OUTPUT:
  - .shipkit/skills/dev-roadmap/outputs/roadmap.md

EOF
}

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
    --help|-h)
      show_help
      exit 0
      ;;
    --cancel)
      echo "Operation cancelled."
      exit 0
      ;;
    *)
      echo "Unknown flag: $1" >&2
      echo "Use --help for usage information" >&2
      exit 1
      ;;
  esac
done

# =============================================================================
# SETUP
# =============================================================================

# Get script directory and source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Source common.sh from workspace scripts
COMMON_SH="$SCRIPT_DIR/../../../scripts/bash/common.sh"
if [[ ! -f "$COMMON_SH" ]]; then
  echo "ERROR: common.sh not found at: $COMMON_SH" >&2
  exit 1
fi
source "$COMMON_SH"

# Setup paths
OUTPUT_DIR="$SKILL_DIR/outputs"
OUTPUT_FILE="$OUTPUT_DIR/roadmap.md"
TEMPLATE_FILE="$SKILL_DIR/templates/roadmap-template.md"

# Registry for existing specs
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
REGISTRY_FILE="$REPO_ROOT/.shipkit/skills/dev-specify/outputs/specs/registry.txt"

# =============================================================================
# HEADER
# =============================================================================

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}  Development Roadmap Creator${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo

# =============================================================================
# PREREQUISITE CHECKS
# =============================================================================

echo -e "${BLUE}Checking prerequisites...${NC}"
echo

# Use common.sh function to check prerequisites
check_skill_prerequisites "dev-roadmap" "$SKIP_PREREQS"

echo

# =============================================================================
# OUTPUT FILE EXISTENCE CHECK
# =============================================================================

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Use common.sh function to check if output exists
check_output_exists "$OUTPUT_FILE" "Roadmap" "$UPDATE" "$ARCHIVE"

# =============================================================================
# LOAD TEMPLATE
# =============================================================================

if [[ ! -f "$TEMPLATE_FILE" ]]; then
  echo -e "${RED}ERROR: Template not found: $TEMPLATE_FILE${NC}" >&2
  exit 1
fi

echo -e "${BLUE}Loading template...${NC}"

# Copy template to output
cp "$TEMPLATE_FILE" "$OUTPUT_FILE"

# Replace {{DATE}} with current date
sed -i "s/{{DATE}}/$(date +%Y-%m-%d)/g" "$OUTPUT_FILE" 2>/dev/null || \
  sed -i '' "s/{{DATE}}/$(date +%Y-%m-%d)/g" "$OUTPUT_FILE"

echo -e "${GREEN}✓${NC} Roadmap template created"
echo

# =============================================================================
# GATHER CONTEXT PATHS
# =============================================================================

REPO_ROOT=$(get_repo_root)

USER_STORIES_PATH="$REPO_ROOT/.shipkit/skills/prod-user-stories/outputs/user-stories.md"
CONSTITUTION_PATH="$REPO_ROOT/.shipkit/skills/dev-constitution/outputs/constitution.md"
RISKS_PATH="$REPO_ROOT/.shipkit/skills/prod-assumptions-and-risks/outputs/assumptions-and-risks.md"
STRATEGY_PATH="$REPO_ROOT/.shipkit/skills/prod-strategic-thinking/outputs/business-canvas.md"

# =============================================================================
# CHECK FOR EXISTING SPECS
# =============================================================================

echo -e "${BLUE}Checking for existing specs...${NC}"
echo

# List existing specs from registry
if [[ -f "$REGISTRY_FILE" && -s "$REGISTRY_FILE" ]]; then
  SPEC_COUNT=$(wc -l < "$REGISTRY_FILE" | tr -d ' ')
  if [[ $SPEC_COUNT -gt 0 ]]; then
    echo -e "  ${BLUE}○${NC} Existing specs ($SPEC_COUNT):"
    head -10 "$REGISTRY_FILE" | while IFS='|' read -r num name created; do
      echo "     $num: $name"
    done
    if [[ $SPEC_COUNT -gt 10 ]]; then
      echo "     ... and $((SPEC_COUNT - 10)) more"
    fi
  else
    echo -e "  ${BLUE}○${NC} No existing specs (starting from spec 001)"
  fi
else
  echo -e "  ${BLUE}○${NC} No existing specs (starting from spec 001)"
fi

echo

# =============================================================================
# REPORT TO CLAUDE
# =============================================================================

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}Ready for Claude${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo
echo "Claude should now:"
echo
echo "  1. Read context:"
echo "     ${GREEN}✓${NC} $USER_STORIES_PATH"
echo "     ${GREEN}✓${NC} $CONSTITUTION_PATH"
[[ -f "$RISKS_PATH" ]] && echo "     ${BLUE}○${NC} $RISKS_PATH (optional)"
[[ -f "$STRATEGY_PATH" ]] && echo "     ${BLUE}○${NC} $STRATEGY_PATH (optional)"
echo
echo "  2. Analyze existing specs (if any):"
echo "     - Check registry: $REGISTRY_FILE"
echo "     - Reference existing spec numbers when sequencing"
echo
echo "  3. Analyze and sequence NEW features:"
echo "     - Identify foundation (Spec 1 or next available: Core Infrastructure)"
echo "     - Build dependency graph (what blocks what)"
echo "     - Group tightly coupled features (same domain/tables)"
echo "     - Sequence by engineering logic (foundation → risky → critical path)"
echo
echo "  4. Fill in template placeholders:"
echo "     - {{TECH_STACK}} - From constitution"
echo "     - {{FOUNDATION_REASONING}} - Why infrastructure first"
echo "     - {{INFRASTRUCTURE_COMPONENTS}} - Database, auth, API, etc."
echo "     - {{SEQUENCED_SPECS}} - Numbered specs with rationale"
echo "     - {{TOTAL_SPECS}} - Total number of specs"
echo "     - {{ADDITIONAL_NOTES}} - Any relevant notes"
echo
echo "  5. Write to: $OUTPUT_FILE"
echo
echo -e "${CYAN}Output location:${NC} $OUTPUT_FILE"
echo
echo -e "${YELLOW}Remember:${NC}"
echo "  - Foundation first (enables all features)"
echo "  - Risky/uncertain next (validate early)"
echo "  - Critical path before parallel work (unblock maximum work)"
echo "  - Group tightly coupled features (minimize context switching)"
echo
