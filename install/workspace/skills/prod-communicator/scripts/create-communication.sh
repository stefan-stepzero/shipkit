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
  echo -e "${YELLOW}⚠${NC}  No prod skill outputs found yet."
  echo ""
  echo "Run product discovery skills first:"
  echo "  /prod-strategic-thinking"
  echo "  /prod-personas"
  echo "  /prod-jobs-to-be-done"
  echo ""
  exit 1
fi

echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Prompt for communication type
echo "What type of communication do you want to create?"
echo ""
echo "  1. Investor One-Pager (high-level strategy + traction)"
echo "  2. Executive Summary (strategic brief for leadership)"
echo "  3. Team Update (product vision + roadmap for team)"
echo "  4. Customer Announcement (external product launch)"
echo "  5. Board Deck Outline (structured presentation outline)"
echo ""
read -p "Choice [1-5]: " comm_choice

case $comm_choice in
  1)
    COMM_TYPE="investor-one-pager"
    COMM_NAME="Investor One-Pager"
    TEMPLATE_FILE="$TEMPLATE_DIR/investor-one-pager-template.md"
    ;;
  2)
    COMM_TYPE="exec-summary"
    COMM_NAME="Executive Summary"
    TEMPLATE_FILE="$TEMPLATE_DIR/exec-summary-template.md"
    ;;
  3)
    COMM_TYPE="team-update"
    COMM_NAME="Team Update"
    TEMPLATE_FILE="$TEMPLATE_DIR/team-update-template.md"
    ;;
  4)
    COMM_TYPE="customer-announcement"
    COMM_NAME="Customer Announcement"
    TEMPLATE_FILE="$TEMPLATE_DIR/customer-announcement-template.md"
    ;;
  5)
    COMM_TYPE="board-deck"
    COMM_NAME="Board Deck Outline"
    TEMPLATE_FILE="$TEMPLATE_DIR/board-deck-template.md"
    ;;
  *)
    echo "Invalid choice. Cancelled."
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
