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
      echo "Usage: $0 --maturity <value> --business-model <value> [options]"
      echo ""
      echo "Required flags:"
      echo "  --maturity <value>    Set maturity: poc|mvp|v1|established"
      echo "  --business-model <v>  Set model: b2c|b2b|marketplace|side-project"
      echo ""
      echo "Optional flags:"
      echo "  --update              Update existing constitution"
      echo "  --archive             Archive current and create new version"
      echo "  --skip-prereqs        Skip prerequisite checks"
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

# Validate required flags
if [[ -z "$MATURITY" ]]; then
  echo -e "${RED}✗${NC} Error: --maturity flag is required" >&2
  echo "  Valid values: poc|mvp|v1|established" >&2
  echo "  Run with --help for usage information" >&2
  exit 1
fi

if [[ -z "$BUSINESS_MODEL" ]]; then
  echo -e "${RED}✗${NC} Error: --business-model flag is required" >&2
  echo "  Valid values: b2c|b2b|marketplace|side-project" >&2
  echo "  Run with --help for usage information" >&2
  exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Map flags to actual template filenames
case "${MATURITY}-${BUSINESS_MODEL}" in
  mvp-side-project)
    TEMPLATE_FILE="side-project-mvp.md"
    ;;
  poc-side-project)
    TEMPLATE_FILE="side-project-poc.md"
    ;;
  v1-b2b)
    TEMPLATE_FILE="b2b-saas-greenfield.md"
    ;;
  v1-b2c)
    TEMPLATE_FILE="b2c-saas-greenfield.md"
    ;;
  established-*)
    # Existing project works for any business model
    TEMPLATE_FILE="existing-project.md"
    ;;
  poc-*)
    # For experimental projects (poc + any other business model)
    TEMPLATE_FILE="experimental.md"
    ;;
  *)
    echo -e "${RED}✗${NC} Error: No template available for maturity=$MATURITY, business-model=$BUSINESS_MODEL" >&2
    echo "  Available combinations:" >&2
    echo "    mvp + side-project" >&2
    echo "    poc + side-project" >&2
    echo "    v1 + b2b" >&2
    echo "    v1 + b2c" >&2
    echo "    established + [any]" >&2
    exit 1
    ;;
esac

TEMPLATE_PATH="$TEMPLATE_DIR/$TEMPLATE_FILE"

# Verify template exists
if [[ ! -f "$TEMPLATE_PATH" ]]; then
  echo -e "${RED}✗${NC} Template file not found: $TEMPLATE_PATH" >&2
  exit 1
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
