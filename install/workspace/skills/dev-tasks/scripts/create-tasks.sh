#!/usr/bin/env bash
# create-tasks.sh - Generate dependency-ordered task breakdown
# Part of shipkit dev-tasks skill

set -e

# =============================================================================
# SETUP
# =============================================================================

# Source shared utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
source "$REPO_ROOT/.shipkit/scripts/bash/common.sh"

# Get skill directory
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT_DIR="$SKILL_DIR/outputs"
TEMPLATE_DIR="$SKILL_DIR/templates"
REFERENCES_DIR="$SKILL_DIR/references"

# =============================================================================
# PARSE ARGUMENTS AND FLAGS
# =============================================================================

UPDATE=false
ARCHIVE=false
SKIP_PREREQS=false
FEATURE_DIR=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --update) UPDATE=true; shift ;;
    --archive) ARCHIVE=true; shift ;;
    --skip-prereqs) SKIP_PREREQS=true; shift ;;
    --cancel) echo "Cancelled."; exit 0 ;;
    --help|-h)
      echo "Usage: $0 <feature-dir> [--update|--archive|--skip-prereqs|--cancel]"
      echo ""
      echo "Arguments:"
      echo "  <feature-dir>   Path to feature spec directory (e.g., specs/1-user-authentication)"
      echo ""
      echo "Flags:"
      echo "  --update        Regenerate tasks (if spec/plan changed)"
      echo "  --archive       Archive current version and create new"
      echo "  --skip-prereqs  Skip prerequisite checks"
      echo "  --cancel        Cancel operation"
      echo "  --help, -h      Show this help message"
      exit 0
      ;;
    -*) echo "Unknown flag: $1" >&2; exit 1 ;;
    *) FEATURE_DIR="$1"; shift ;;
  esac
done

# =============================================================================
# VALIDATE ARGUMENTS
# =============================================================================

if [[ -z "$FEATURE_DIR" ]]; then
  echo -e "${RED}✗${NC} Error: Feature directory required"
  echo ""
  echo "Usage: $0 <feature-dir> [flags]"
  echo "Example: $0 specs/1-user-authentication"
  echo ""
  echo "Run '$0 --help' for more information"
  exit 1
fi

# Convert to absolute path if relative
if [[ ! "$FEATURE_DIR" = /* ]]; then
  FEATURE_DIR="$REPO_ROOT/$FEATURE_DIR"
fi

# Validate feature directory exists
if [[ ! -d "$FEATURE_DIR" ]]; then
  echo -e "${RED}✗${NC} Feature directory not found: $FEATURE_DIR"
  exit 1
fi

# Extract feature name from directory
FEATURE_NAME=$(basename "$FEATURE_DIR")

echo -e "${CYAN}Feature:${NC} $FEATURE_NAME"
echo -e "${CYAN}Directory:${NC} $FEATURE_DIR"
echo ""

# =============================================================================
# CHECK PREREQUISITES
# =============================================================================

# dev-tasks requires dev-plan (reads plan.md and spec.md)
if [[ "$SKIP_PREREQS" == "false" ]]; then
  check_skill_prerequisites "dev-tasks" "$SKIP_PREREQS"
fi

# =============================================================================
# CHECK REQUIRED FILES
# =============================================================================

echo -e "${CYAN}Checking required files...${NC}"
echo ""

SPEC_FILE="$FEATURE_DIR/spec.md"
PLAN_FILE="$FEATURE_DIR/plan.md"
CONSTITUTION_FILE="$REPO_ROOT/.shipkit/skills/dev-constitution/outputs/constitution.md"

MISSING_FILES=false

# Check spec.md (REQUIRED)
if [[ -f "$SPEC_FILE" ]]; then
  echo -e "  ${GREEN}✓${NC} Found: spec.md"
else
  echo -e "  ${RED}✗${NC} Missing: spec.md (REQUIRED)"
  MISSING_FILES=true
fi

# Check plan.md (REQUIRED)
if [[ -f "$PLAN_FILE" ]]; then
  echo -e "  ${GREEN}✓${NC} Found: plan.md"
else
  echo -e "  ${RED}✗${NC} Missing: plan.md (REQUIRED)"
  MISSING_FILES=true
fi

# Check constitution.md (RECOMMENDED)
if [[ -f "$CONSTITUTION_FILE" ]]; then
  echo -e "  ${GREEN}✓${NC} Found: constitution.md"
else
  echo -e "  ${YELLOW}⚠${NC} Missing: constitution.md (recommended)"
  echo "  Run /dev-constitution to establish technical standards"
fi

echo ""

if [[ "$MISSING_FILES" == "true" ]]; then
  echo -e "${RED}✗${NC} Cannot generate tasks without required files"
  echo ""
  echo "Required files missing. Please ensure:"
  echo "  1. spec.md exists (run /dev-specify first)"
  echo "  2. plan.md exists (run /dev-plan first)"
  exit 1
fi

# =============================================================================
# CHECK OPTIONAL FILES
# =============================================================================

echo -e "${CYAN}Checking optional files...${NC}"
echo ""

DATA_MODEL_FILE="$FEATURE_DIR/data-model.md"
CONTRACTS_DIR="$FEATURE_DIR/contracts"
RESEARCH_FILE="$FEATURE_DIR/research.md"
QUICKSTART_FILE="$FEATURE_DIR/quickstart.md"

AVAILABLE_DOCS=()

if [[ -f "$DATA_MODEL_FILE" ]]; then
  echo -e "  ${GREEN}✓${NC} Found: data-model.md"
  AVAILABLE_DOCS+=("$DATA_MODEL_FILE")
fi

if [[ -d "$CONTRACTS_DIR" ]]; then
  CONTRACT_COUNT=$(find "$CONTRACTS_DIR" -type f \( -name "*.yaml" -o -name "*.yml" -o -name "*.json" \) 2>/dev/null | wc -l)
  if [[ $CONTRACT_COUNT -gt 0 ]]; then
    echo -e "  ${GREEN}✓${NC} Found: contracts/ ($CONTRACT_COUNT files)"
    AVAILABLE_DOCS+=("$CONTRACTS_DIR")
  fi
fi

if [[ -f "$RESEARCH_FILE" ]]; then
  echo -e "  ${GREEN}✓${NC} Found: research.md"
  AVAILABLE_DOCS+=("$RESEARCH_FILE")
fi

if [[ -f "$QUICKSTART_FILE" ]]; then
  echo -e "  ${GREEN}✓${NC} Found: quickstart.md"
  AVAILABLE_DOCS+=("$QUICKSTART_FILE")
fi

if [[ ${#AVAILABLE_DOCS[@]} -eq 0 ]]; then
  echo -e "  ${YELLOW}⚠${NC} No optional files found (will generate from spec + plan only)"
fi

echo ""

# =============================================================================
# ENSURE OUTPUT DIRECTORIES EXIST
# =============================================================================

# Create output directory mirroring feature structure
FEATURE_OUTPUT_DIR="$OUTPUT_DIR/specs/$FEATURE_NAME"
mkdir -p "$FEATURE_OUTPUT_DIR"

# =============================================================================
# OUTPUT FILE LOCATION
# =============================================================================

OUTPUT_FILE="$FEATURE_OUTPUT_DIR/tasks.md"

echo -e "${CYAN}Output location:${NC} $OUTPUT_FILE"
echo ""

# =============================================================================
# CHECK IF FILE EXISTS AND HANDLE DECISION
# =============================================================================

check_output_exists "$OUTPUT_FILE" "Tasks for $FEATURE_NAME" "$UPDATE" "$ARCHIVE"

# =============================================================================
# CHECK TEMPLATE EXISTS
# =============================================================================

TEMPLATE_FILE="$TEMPLATE_DIR/tasks-template.md"
if [[ ! -f "$TEMPLATE_FILE" ]]; then
  echo -e "${RED}✗${NC} Template not found: $TEMPLATE_FILE"
  exit 1
fi

echo -e "${GREEN}✓${NC} Template available: $TEMPLATE_FILE"
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

echo -e "${GREEN}✓${NC} Ready for Claude to generate dependency-ordered tasks"
echo ""
echo -e "${CYAN}Next Steps:${NC}"
echo "  1. Claude reads template: $TEMPLATE_FILE"
echo "  2. Claude reads references in: $REFERENCES_DIR/"
echo "  3. Claude reads required files:"
echo "     • $SPEC_FILE"
echo "     • $PLAN_FILE"
if [[ -f "$CONSTITUTION_FILE" ]]; then
  echo "     • $CONSTITUTION_FILE"
fi
echo "  4. Claude reads optional files (if available):"
for doc in "${AVAILABLE_DOCS[@]}"; do
  echo "     • $doc"
done
echo "  5. Claude analyzes dependencies between components"
echo "  6. Claude generates dependency-ordered tasks with [P] parallel markers"
echo "  7. Claude organizes tasks by user story (each story = phase)"
echo "  8. Claude validates spec/plan consistency"
echo "  9. Claude writes to: $OUTPUT_FILE"
echo ""
echo -e "${CYAN}Task Generation Strategy:${NC}"
echo "  • TDD integration: Test tasks before implementation tasks"
echo "  • User story organization: Each story is a phase"
echo "  • Dependency ordering: Sequential tasks ordered by dependencies"
echo "  • Parallel markers: [P] indicates tasks that can run in parallel"
echo "  • Constitution-driven: Task patterns follow established standards"
echo ""
echo -e "${YELLOW}Remember:${NC} Tasks must be specific enough for immediate execution"
echo ""

exit 0
