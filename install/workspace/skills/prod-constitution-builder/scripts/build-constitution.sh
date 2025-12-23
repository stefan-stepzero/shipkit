#!/usr/bin/env bash
# build-constitution.sh - Generate product constitution based on context
# Part of shipkit prod-constitution-builder skill

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
MATURITY=""
BUSINESS_MODEL=""

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
    --maturity)
      MATURITY="$2"
      shift 2
      ;;
    --business-model)
      BUSINESS_MODEL="$2"
      shift 2
      ;;
    --cancel)
      echo "Cancelled."
      exit 0
      ;;
    --help|-h)
      echo "Usage: $0 [options]"
      echo ""
      echo "Flags:"
      echo "  --update              Update existing constitution"
      echo "  --archive             Archive current and create new version"
      echo "  --skip-prereqs        Skip prerequisite checks"
      echo "  --maturity <value>    Set maturity: poc|mvp|v1|established"
      echo "  --business-model <v>  Set model: b2c|b2b|marketplace|side-project"
      echo "  --cancel              Cancel operation"
      exit 0
      ;;
    *)
      echo -e "${RED}Unknown flag: $1${NC}" >&2
      exit 1
      ;;
  esac
done

# Check prerequisites
check_skill_prerequisites "prod-constitution-builder" "$SKIP_PREREQS"

# Try to detect from strategic-thinking output if not provided
STRATEGY_FILE="$REPO_ROOT/.shipkit/skills/prod-strategic-thinking/outputs/business-canvas.md"

if [[ -z "$MATURITY" || -z "$BUSINESS_MODEL" ]] && [[ -f "$STRATEGY_FILE" ]]; then
  echo -e "${CYAN}Reading context from strategic thinking...${NC}"

  # Extract context from strategy (simple grep for now)
  if [[ -z "$MATURITY" ]]; then
    if grep -q "POC\|Proof of Concept" "$STRATEGY_FILE"; then
      MATURITY="poc"
    elif grep -q "MVP" "$STRATEGY_FILE"; then
      MATURITY="mvp"
    elif grep -q "Established" "$STRATEGY_FILE"; then
      MATURITY="established"
    else
      MATURITY="mvp"  # Default
    fi
  fi

  if [[ -z "$BUSINESS_MODEL" ]]; then
    if grep -q "B2C" "$STRATEGY_FILE"; then
      BUSINESS_MODEL="b2c"
    elif grep -q "B2B" "$STRATEGY_FILE"; then
      BUSINESS_MODEL="b2b"
    elif grep -q "Marketplace" "$STRATEGY_FILE"; then
      BUSINESS_MODEL="marketplace"
    elif grep -q "Side project" "$STRATEGY_FILE"; then
      BUSINESS_MODEL="side-project"
    else
      BUSINESS_MODEL="b2c"  # Default
    fi
  fi
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Select template based on maturity + business model
TEMPLATE_FILE="${MATURITY}-${BUSINESS_MODEL}-constitution.md"
TEMPLATE_PATH="$TEMPLATE_DIR/$TEMPLATE_FILE"

# Fallback to maturity-only template if specific combo doesn't exist
if [[ ! -f "$TEMPLATE_PATH" ]]; then
  TEMPLATE_FILE="${MATURITY}-constitution.md"
  TEMPLATE_PATH="$TEMPLATE_DIR/$TEMPLATE_FILE"
fi

# Final fallback to generic template
if [[ ! -f "$TEMPLATE_PATH" ]]; then
  TEMPLATE_FILE="mvp-constitution.md"
  TEMPLATE_PATH="$TEMPLATE_DIR/$TEMPLATE_FILE"
fi

# Output file
OUTPUT_FILE="$OUTPUT_DIR/product-constitution.md"

# Check if file exists and handle decision
check_output_exists "$OUTPUT_FILE" "Constitution" "$UPDATE" "$ARCHIVE"

# Copy template to output
if [[ -f "$TEMPLATE_PATH" ]]; then
  cp "$TEMPLATE_PATH" "$OUTPUT_FILE"

  echo ""
  echo -e "${GREEN}✓${NC} Created product constitution at: $OUTPUT_FILE"
  echo -e "${CYAN}  Context:${NC} ${MATURITY} / ${BUSINESS_MODEL}"
  echo -e "${CYAN}  Template:${NC} ${TEMPLATE_FILE}"
  echo ""
  echo "This constitution will guide all product decisions."
  echo "Reference it in all prod-* skills."
else
  echo -e "${RED}✗${NC} Template not found: $TEMPLATE_PATH" >&2
  exit 1
fi

exit 0
