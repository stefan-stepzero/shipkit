#!/usr/bin/env bash
# create-communication.sh - Generate stakeholder communications
# Part of shipkit prod-communicator skill

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

# Generate output filenames with timestamp
DATE_STAMP=$(date +%Y-%m-%d)
TIME_STAMP=$(date +%Y-%m-%dT%H:%M:%SZ)
HTML_FILE="$OUTPUT_DIR/update-${DATE_STAMP}.html"
HTML_TEMPLATE="$TEMPLATE_DIR/update-template.html"

echo ""
echo -e "${CYAN}Creating $COMM_NAME...${NC}"
echo -e "${CYAN}Source artifacts: ${AVAILABLE_SOURCES[*]}${NC}"
echo ""

# Archive old HTML update files
if ls "$OUTPUT_DIR"/update-*.html 1> /dev/null 2>&1; then
  echo -e "${YELLOW}Archiving previous updates...${NC}"
  for old_file in "$OUTPUT_DIR"/update-*.html; do
    if [[ -f "$old_file" ]]; then
      OLD_DATE=$(basename "$old_file" | sed 's/update-\(.*\)\.html/\1/')
      ARCHIVE_NAME="$OUTPUT_DIR/archive-${OLD_DATE}.html"
      mv "$old_file" "$ARCHIVE_NAME"
      echo -e "${GREEN}✓${NC} Archived: $(basename "$old_file") → $(basename "$ARCHIVE_NAME")"
    fi
  done
  echo ""
fi

# Check if HTML template exists
if [[ ! -f "$HTML_TEMPLATE" ]]; then
  echo -e "${RED}✗${NC} HTML template not found: $HTML_TEMPLATE"
  exit 1
fi

# Create HTML file from template
cp "$HTML_TEMPLATE" "$HTML_FILE"

# Replace placeholders in HTML
sed -i "s|{{DATE}}|$DATE_STAMP|g" "$HTML_FILE" 2>/dev/null || \
  sed -i '' "s|{{DATE}}|$DATE_STAMP|g" "$HTML_FILE"
sed -i "s|{{TIMESTAMP}}|$TIME_STAMP|g" "$HTML_FILE" 2>/dev/null || \
  sed -i '' "s|{{TIMESTAMP}}|$TIME_STAMP|g" "$HTML_FILE"
sed -i "s|{{TITLE}}|$COMM_NAME|g" "$HTML_FILE" 2>/dev/null || \
  sed -i '' "s|{{TITLE}}|$COMM_NAME|g" "$HTML_FILE"
sed -i "s|{{SOURCES}}|${AVAILABLE_SOURCES[*]}|g" "$HTML_FILE" 2>/dev/null || \
  sed -i '' "s|{{SOURCES}}|${AVAILABLE_SOURCES[*]}|g" "$HTML_FILE"

echo -e "${GREEN}✓${NC} Created: $HTML_FILE"
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Ready for Claude${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Claude should now:"
echo ""
echo "  1. Read source artifacts from available product skills"
echo "  2. ${GREEN}EDIT${NC} the HTML file: $HTML_FILE"
echo "  3. Replace placeholders with actual content"
echo "  4. Enhance styling to make it beautiful and engaging"
echo "  5. Ensure content matches the communication type: $COMM_NAME"
echo ""
echo -e "${CYAN}HTML file location:${NC} $HTML_FILE"
echo -e "${CYAN}References available:${NC} $SKILL_DIR/references/"
echo -e "${CYAN}MD template (optional):${NC} $TEMPLATE_FILE"
echo ""
echo -e "${YELLOW}Note:${NC} Edit the HTML file directly - don't create new files"
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

exit 0
