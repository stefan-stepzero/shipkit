#!/usr/bin/env bash
# build-constitution.sh - Generate product constitution based on context
# Part of shipkit prod-constitution-builder skill

set -e

# Source shared utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
source "$REPO_ROOT/.shipkit/scripts/bash/common.sh"

# Get skill directory
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT_DIR="$SKILL_DIR/outputs"
TEMPLATE_DIR="$SKILL_DIR/templates"

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Parse arguments
MATURITY=""
BUSINESS_MODEL=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --maturity) MATURITY="$2"; shift 2;;
    --business-model) BUSINESS_MODEL="$2"; shift 2;;
    --help|-h)
      echo "Usage: $0 [--maturity <poc|mvp|v1|established>] [--business-model <b2c|b2b|marketplace|side-project>]"
      echo ""
      echo "If not provided, will attempt to read from strategic-thinking output"
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

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

# Check if constitution already exists
if [[ -f "$OUTPUT_FILE" ]]; then
  echo -e "${YELLOW}⚠${NC}  Constitution already exists at: $OUTPUT_FILE"
  echo ""
  echo "Options:"
  echo "  1. Update with new template (archive current)"
  echo "  2. Keep existing"
  read -p "Choice [1-2]: " choice

  case $choice in
    1)
      TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
      ARCHIVE_FILE="$OUTPUT_DIR/product-constitution-${TIMESTAMP}.md"
      mv "$OUTPUT_FILE" "$ARCHIVE_FILE"
      echo -e "${GREEN}✓${NC} Archived existing constitution to: $ARCHIVE_FILE"
      ;;
    2)
      echo "Keeping existing constitution."
      exit 0
      ;;
    *)
      echo "Invalid choice"
      exit 1
      ;;
  esac
fi

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
  echo -e "ERROR: Template not found: $TEMPLATE_PATH" >&2
  exit 1
fi

exit 0
