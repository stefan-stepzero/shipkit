#!/usr/bin/env bash
# create-communication.sh - Generate stakeholder communications
# Part of shipkit prod-communicator skill

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
COMM_TYPE=""
SKIP_PREREQS=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --type)
      COMM_TYPE="$2"
      shift 2
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
      echo "Usage: $0 [--type <type>] [--skip-prereqs|--cancel]"
      echo ""
      echo "Communication types:"
      echo "  investor-one-pager    High-level strategy + traction"
      echo "  exec-summary          Strategic brief for leadership"
      echo "  team-update          Product vision + roadmap for team"
      echo "  customer-announcement External product launch"
      echo "  board-deck           Structured presentation outline"
      echo ""
      echo "Flags:"
      echo "  --skip-prereqs  Skip prerequisite checks (continue with available artifacts)"
      echo "  --cancel        Cancel operation"
      exit 0
      ;;
    *)
      echo -e "${RED}Unknown flag: $1${NC}" >&2
      exit 1
      ;;
  esac
done

# Check prerequisites (communicator doesn't have strict prereqs, but benefits from artifacts)
# We'll skip the strict check and instead scan for available artifacts
check_skill_prerequisites "prod-communicator" "$SKIP_PREREQS"

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}    Stakeholder Communication Generator${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Detect available source artifacts
SKILLS_DIR="$REPO_ROOT/.shipkit/skills"
AVAILABLE_SOURCES=()

echo -e "${CYAN}Scanning for available artifacts...${NC}"
echo ""

if [[ -f "$SKILLS_DIR/prod-strategic-thinking/outputs/business-canvas.md" ]]; then
  echo -e "${GREEN}✓${NC} Strategic Thinking"
  AVAILABLE_SOURCES+=("strategic-thinking")
fi

if [[ -f "$SKILLS_DIR/prod-personas/outputs/personas.md" ]]; then
  echo -e "${GREEN}✓${NC} Personas"
  AVAILABLE_SOURCES+=("personas")
fi

if [[ -f "$SKILLS_DIR/prod-jobs-to-be-done/outputs/jobs-to-be-done.md" ]]; then
  echo -e "${GREEN}✓${NC} Jobs-to-be-Done"
  AVAILABLE_SOURCES+=("jtbd")
fi

if [[ -f "$SKILLS_DIR/prod-constitution-builder/outputs/product-constitution.md" ]]; then
  echo -e "${GREEN}✓${NC} Product Constitution"
  AVAILABLE_SOURCES+=("constitution")
fi

if [[ -f "$SKILLS_DIR/prod-market-analysis/outputs/market-analysis.md" ]]; then
  echo -e "${GREEN}✓${NC} Market Analysis"
  AVAILABLE_SOURCES+=("market-analysis")
fi

# Check for other potential sources
for skill_output in "$SKILLS_DIR"/prod-*/outputs/*.md; do
  if [[ -f "$skill_output" ]]; then
    SKILL_NAME=$(basename "$(dirname "$(dirname "$skill_output")")")
    if [[ ! " ${AVAILABLE_SOURCES[@]} " =~ " ${SKILL_NAME} " ]]; then
      echo -e "${GREEN}✓${NC} $SKILL_NAME"
      AVAILABLE_SOURCES+=("$SKILL_NAME")
    fi
  fi
done

if [[ ${#AVAILABLE_SOURCES[@]} -eq 0 ]]; then
  if [[ "$SKIP_PREREQS" != "true" ]]; then
    output_decision "NO_ARTIFACTS" \
      "No prod skill outputs found yet. Run product discovery skills first." \
      "--skip-prereqs (Continue anyway)"
    exit $EXIT_PREREQ_MISSING
  else
    echo -e "${YELLOW}⚠${NC}  No artifacts found, continuing with minimal context..."
  fi
fi

echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Prompt for communication type if not provided
if [[ -z "$COMM_TYPE" ]]; then
  echo "What type of communication do you want to create?"
  echo ""
  echo "  1. Investor One-Pager (high-level strategy + traction)"
  echo "  2. Executive Summary (strategic brief for leadership)"
  echo "  3. Team Update (product vision + roadmap for team)"
  echo "  4. Customer Announcement (external product launch)"
  echo "  5. Board Deck Outline (structured presentation outline)"
  echo ""

  output_decision "COMM_TYPE_NEEDED" \
    "Select communication type" \
    "--type investor-one-pager | --type exec-summary | --type team-update | --type customer-announcement | --type board-deck"
  exit $EXIT_DECISION_NEEDED
fi

# Map type to template and name
case $COMM_TYPE in
  investor-one-pager)
    COMM_NAME="Investor One-Pager"
    TEMPLATE_FILE="$TEMPLATE_DIR/investor-one-pager-template.md"
    ;;
  exec-summary)
    COMM_NAME="Executive Summary"
    TEMPLATE_FILE="$TEMPLATE_DIR/exec-summary-template.md"
    ;;
  team-update)
    COMM_NAME="Team Update"
    TEMPLATE_FILE="$TEMPLATE_DIR/team-update-template.md"
    ;;
  customer-announcement)
    COMM_NAME="Customer Announcement"
    TEMPLATE_FILE="$TEMPLATE_DIR/customer-announcement-template.md"
    ;;
  board-deck)
    COMM_NAME="Board Deck Outline"
    TEMPLATE_FILE="$TEMPLATE_DIR/board-deck-template.md"
    ;;
  *)
    echo -e "${RED}Invalid communication type: $COMM_TYPE${NC}" >&2
    exit 1
    ;;
esac

# Check if template exists
if [[ ! -f "$TEMPLATE_FILE" ]]; then
  echo -e "${RED}✗${NC} Template not found: $TEMPLATE_FILE"
  exit 1
fi

# Generate output filename with timestamp
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
OUTPUT_FILE="$OUTPUT_DIR/${COMM_TYPE}-${TIMESTAMP}.md"

echo ""
echo -e "${CYAN}Creating $COMM_NAME...${NC}"
echo -e "${CYAN}Source artifacts: ${AVAILABLE_SOURCES[*]}${NC}"
echo ""

# Create output file header
cat > "$OUTPUT_FILE" << EOF
# $COMM_NAME

**Generated:** $(date +%Y-%m-%d)
**Source Artifacts:** ${AVAILABLE_SOURCES[*]}

---

EOF

echo -e "${GREEN}✓${NC} Created: $OUTPUT_FILE"
echo ""
echo -e "${CYAN}Template available at:${NC} $TEMPLATE_FILE"
echo -e "${CYAN}References available in:${NC} $SKILL_DIR/references/"
echo ""
echo -e "${YELLOW}Claude will now read your source artifacts and fill the template...${NC}"
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

exit 0
