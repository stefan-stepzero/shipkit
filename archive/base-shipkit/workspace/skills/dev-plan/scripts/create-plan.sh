#!/usr/bin/env bash
# create-plan.sh - Create or update implementation plan
# Part of shipkit dev-plan skill

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
OUTPUT_BASE_DIR="$SKILL_DIR/outputs/specs"
REGISTRY_FILE="$REPO_ROOT/.shipkit/skills/dev-specify/outputs/specs/registry.txt"
TEMPLATE_DIR="$SKILL_DIR/templates"
REFERENCES_DIR="$SKILL_DIR/references"

# =============================================================================
# PARSE FLAGS
# =============================================================================

WITH_CHECKLIST=false
UPDATE=false
ARCHIVE=false
SKIP_PREREQS=false
SPEC_PATH=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --with-checklist) WITH_CHECKLIST=true; shift ;;
    --update) UPDATE=true; shift ;;
    --archive) ARCHIVE=true; shift ;;
    --skip-prereqs) SKIP_PREREQS=true; shift ;;
    --cancel) echo "Cancelled."; exit 0 ;;
    --help|-h)
      echo "Usage: $0 <spec-path> [--with-checklist|--update|--archive|--skip-prereqs|--cancel]"
      echo ""
      echo "Arguments:"
      echo "  <spec-path>     Path to spec directory (e.g., specs/1-user-authentication)"
      echo ""
      echo "Flags:"
      echo "  --with-checklist  Include acceptance test checklist"
      echo "  --update          Update existing plan"
      echo "  --archive         Archive current version and create new"
      echo "  --skip-prereqs    Skip prerequisite checks"
      echo "  --cancel          Cancel operation"
      echo "  --help, -h        Show this help message"
      exit 0
      ;;
    *)
      if [[ -z "$SPEC_PATH" ]]; then
        SPEC_PATH="$1"
        shift
      else
        echo "Unknown flag: $1" >&2
        exit 1
      fi
      ;;
  esac
done

# =============================================================================
# VALIDATE SPEC PATH
# =============================================================================

if [[ -z "$SPEC_PATH" ]]; then
  echo -e "${RED}Error: Spec number required${NC}"
  echo "Usage: $0 <spec-number> [flags]"
  echo "Example: $0 001"
  echo ""
  echo "Available specs:"
  if [[ -f "$REGISTRY_FILE" && -s "$REGISTRY_FILE" ]]; then
    while IFS='|' read -r num name created; do
      echo "  $num: $name"
    done < "$REGISTRY_FILE"
  else
    echo "  (no specs created yet)"
  fi
  exit 1
fi

# Normalize to 3-digit spec number
SPEC_NUM=$(printf "%03d" "$SPEC_PATH")

# Validate it's a valid number
if [[ ! "$SPEC_NUM" =~ ^[0-9]{3}$ ]]; then
  echo -e "${RED}Error: Invalid spec number: $SPEC_PATH${NC}"
  echo "Expected: 001, 002, 003, etc."
  exit 1
fi

# Read spec name from registry
SPEC_NAME=""
if [[ -f "$REGISTRY_FILE" && -s "$REGISTRY_FILE" ]]; then
  while IFS='|' read -r num name created; do
    if [[ "$num" == "$SPEC_NUM" ]]; then
      SPEC_NAME="$name"
      break
    fi
  done < "$REGISTRY_FILE"

  if [[ -z "$SPEC_NAME" ]]; then
    echo -e "${RED}Error: Spec $SPEC_NUM not found in registry${NC}"
    echo "Available specs:"
    while IFS='|' read -r num name created; do
      echo "  $num: $name"
    done < "$REGISTRY_FILE"
    exit 1
  fi
else
  echo -e "${YELLOW}Warning: Registry not found, proceeding without spec name${NC}"
  SPEC_NAME="Spec $SPEC_NUM"
fi

echo -e "${CYAN}Spec:${NC} $SPEC_NUM - $SPEC_NAME"
echo ""

# =============================================================================
# CHECK PREREQUISITES
# =============================================================================

# Check that dev-specify has been run (spec.md exists)
SPECIFY_OUTPUTS_DIR="$REPO_ROOT/.shipkit/skills/dev-specify/outputs/specs"
SPEC_FILE="$SPECIFY_OUTPUTS_DIR/$SPEC_NUM/spec.md"

if [[ ! -f "$SPEC_FILE" ]]; then
  echo "Error: Spec file not found: $SPEC_FILE"
  echo ""
  echo "Please run /dev-specify first to create the feature specification."
  exit 1
fi

# Check for constitution
if [[ "$SKIP_PREREQS" == "false" ]]; then
  check_skill_prerequisites "dev-plan" "$SKIP_PREREQS"
fi

CONSTITUTION_FILE="$REPO_ROOT/.shipkit/skills/dev-constitution/outputs/constitution.md"

# =============================================================================
# SETUP OUTPUT DIRECTORY
# =============================================================================

OUTPUT_DIR="$OUTPUT_BASE_DIR/$SPEC_NUM"
mkdir -p "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR/contracts"

# =============================================================================
# OUTPUT FILES
# =============================================================================

PLAN_FILE="$OUTPUT_DIR/plan.md"
DATA_MODEL_FILE="$OUTPUT_DIR/data-model.md"
RESEARCH_FILE="$OUTPUT_DIR/research.md"
QUICKSTART_FILE="$OUTPUT_DIR/quickstart.md"
CHECKLIST_FILE="$OUTPUT_DIR/checklist.md"

# =============================================================================
# CHECK IF FILES EXIST
# =============================================================================

if [[ -f "$PLAN_FILE" ]]; then
  check_output_exists "$PLAN_FILE" "Implementation Plan" "$UPDATE" "$ARCHIVE"
fi

# =============================================================================
# CHECK TEMPLATES EXIST
# =============================================================================

PLAN_TEMPLATE="$TEMPLATE_DIR/plan-template.md"
DATA_MODEL_TEMPLATE="$TEMPLATE_DIR/data-model-template.md"
RESEARCH_TEMPLATE="$TEMPLATE_DIR/research-template.md"
CONTRACT_TEMPLATE="$TEMPLATE_DIR/contract-template.yaml"

for template in "$PLAN_TEMPLATE" "$DATA_MODEL_TEMPLATE" "$RESEARCH_TEMPLATE" "$CONTRACT_TEMPLATE"; do
  if [[ ! -f "$template" ]]; then
    echo -e "${RED}✗${NC} Template not found: $template"
    exit 1
  fi
done

echo -e "${GREEN}✓${NC} All templates available"

# =============================================================================
# READY FOR CLAUDE
# =============================================================================

echo ""
echo -e "${GREEN}✓${NC} Ready for Claude to create Implementation Plan"
echo ""
echo -e "${CYAN}Input files:${NC}"
echo "  • Spec: $SPEC_FILE ($SPEC_NAME)"
if [[ -f "$CONSTITUTION_FILE" ]]; then
  echo "  • Constitution: $CONSTITUTION_FILE"
else
  echo -e "  ${YELLOW}⚠${NC} Constitution: Not found (proceeding without)"
fi
echo ""
echo -e "${CYAN}Templates:${NC}"
echo "  • Plan: $PLAN_TEMPLATE"
echo "  • Data Model: $DATA_MODEL_TEMPLATE"
echo "  • Research: $RESEARCH_TEMPLATE"
echo "  • Contract: $CONTRACT_TEMPLATE"
echo ""
echo -e "${CYAN}References:${NC}"
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
echo -e "${CYAN}Output files:${NC}"
echo "  • Plan: $PLAN_FILE"
echo "  • Data Model: $DATA_MODEL_FILE"
echo "  • Research: $RESEARCH_FILE"
echo "  • Quickstart: $QUICKSTART_FILE"
echo "  • Contracts: $OUTPUT_DIR/contracts/"
if [[ "$WITH_CHECKLIST" == "true" ]]; then
  echo "  • Checklist: $CHECKLIST_FILE"
fi
echo ""
echo -e "${CYAN}Planning Process:${NC}"
echo "  Phase 0: Research unknowns (web search if needed)"
echo "  Phase 1: Generate data model, contracts, quickstart"
echo "  Constitution Check: Validate design against established patterns"
echo ""
echo -e "${YELLOW}Note:${NC} Claude will follow the plan template workflow:"
echo "  1. Read spec.md and constitution.md"
echo "  2. Identify technical unknowns → research.md"
echo "  3. Design data model → data-model.md"
echo "  4. Generate API contracts → contracts/"
echo "  5. Create quickstart guide → quickstart.md"
echo "  6. Validate against constitution"
echo ""

exit 0
