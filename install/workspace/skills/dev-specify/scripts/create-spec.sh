#!/usr/bin/env bash
# create-spec.sh - Create or update feature specification
# Part of shipkit dev-specify skill

set -e

# Source shared utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
source "$REPO_ROOT/.shipkit/scripts/bash/common.sh"

# Get skill directory
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT_DIR="$SKILL_DIR/outputs/specs"
REGISTRY_FILE="$OUTPUT_DIR/registry.txt"
TEMPLATE_DIR="$SKILL_DIR/templates"
REFERENCES_DIR="$SKILL_DIR/references"

# Parse flags and arguments
FEATURE_DESC=""
UPDATE=false
CLARIFY=false
SKIP_PREREQS=false
SPEC_NAME=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --update)
      UPDATE=true
      shift
      ;;
    --clarify)
      CLARIFY=true
      shift
      ;;
    --skip-prereqs)
      SKIP_PREREQS=true
      shift
      ;;
    --spec)
      SPEC_NAME="$2"
      shift 2
      ;;
    --cancel)
      echo "Cancelled."
      exit 0
      ;;
    --help|-h)
      echo "Usage: $0 [\"feature description\"] [options]"
      echo ""
      echo "Arguments:"
      echo "  \"feature description\"  Natural language description of the feature"
      echo ""
      echo "Flags:"
      echo "  --update        Update an existing spec (requires --spec)"
      echo "  --clarify       Resolve [NEEDS_CLARIFICATION] markers in spec"
      echo "  --spec NAME     Specify which spec to update/clarify"
      echo "  --skip-prereqs  Skip prerequisite checks"
      echo "  --cancel        Cancel operation"
      echo ""
      echo "Examples:"
      echo "  $0 \"Add user authentication\""
      echo "  $0 --clarify --spec 1-user-authentication"
      echo "  $0 --update --spec 1-user-authentication"
      exit 0
      ;;
    -*)
      echo -e "${RED}Unknown flag: $1${NC}" >&2
      exit 1
      ;;
    *)
      # First non-flag argument is feature description
      if [[ -z "$FEATURE_DESC" ]]; then
        FEATURE_DESC="$1"
      fi
      shift
      ;;
  esac
done

# Check prerequisites
check_skill_prerequisites "dev-specify" "$SKIP_PREREQS"

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}    Feature Specification${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Handle different modes
if [[ "$UPDATE" == "true" || "$CLARIFY" == "true" ]]; then
  # UPDATE or CLARIFY mode - need existing spec
  if [[ -z "$SPEC_NAME" ]]; then
    echo -e "${RED}Error: --update and --clarify require --spec NAME${NC}" >&2
    echo "Available specs:"
    if [[ -d "$OUTPUT_DIR" ]]; then
      ls -1 "$OUTPUT_DIR" 2>/dev/null || echo "  (none)"
    else
      echo "  (none)"
    fi
    exit 1
  fi

  SPEC_DIR="$OUTPUT_DIR/$SPEC_NAME"
  SPEC_FILE="$SPEC_DIR/spec.md"

  if [[ ! -f "$SPEC_FILE" ]]; then
    echo -e "${RED}Error: Spec not found: $SPEC_FILE${NC}" >&2
    exit 1
  fi

  if [[ "$UPDATE" == "true" ]]; then
    # Archive old version
    TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
    BACKUP_FILE="$SPEC_DIR/spec-$TIMESTAMP.md.bak"
    cp "$SPEC_FILE" "$BACKUP_FILE"
    echo -e "${GREEN}✓${NC} Archived old spec: $BACKUP_FILE"
  fi

  if [[ "$CLARIFY" == "true" ]]; then
    # Check for NEEDS_CLARIFICATION markers
    CLARIFICATIONS=$(grep -c "\[NEEDS_CLARIFICATION" "$SPEC_FILE" 2>/dev/null || echo "0")
    if [[ "$CLARIFICATIONS" == "0" ]]; then
      echo -e "${GREEN}✓${NC} No clarifications needed in spec"
    else
      echo -e "${YELLOW}⚠${NC} Found $CLARIFICATIONS clarification markers in spec"
    fi
  fi

  echo -e "${CYAN}Spec:${NC} $SPEC_FILE"
  echo ""
  echo "Ready for Claude to update spec via dialogue"

else
  # CREATE mode - new spec
  if [[ -z "$FEATURE_DESC" ]]; then
    echo -e "${RED}Error: Feature description required${NC}" >&2
    echo "Usage: $0 \"feature description\""
    exit 1
  fi

  # Check if user stories exist but no roadmap
  USER_STORIES="$REPO_ROOT/.shipkit/skills/prod-user-stories/outputs/user-stories.md"
  ROADMAP_FILE="$REPO_ROOT/.shipkit/skills/dev-roadmap/outputs/roadmap.md"

  if [[ -f "$USER_STORIES" && ! -f "$ROADMAP_FILE" ]]; then
    echo -e "${YELLOW}⚠${NC} User stories exist but no roadmap found"
    echo ""
    echo "Consider running /dev-roadmap first to:"
    echo "  • Group user stories into logical specs"
    echo "  • Determine optimal implementation order"
    echo "  • Plan the full development sequence"
    echo ""
    echo "Continue creating individual spec anyway? (yes/no)"
    read -r response
    if [[ "$response" != "yes" ]]; then
      echo ""
      echo "Run /dev-roadmap first, then return to /dev-specify"
      exit 0
    fi
    echo ""
  fi

  # Initialize registry if doesn't exist
  if [[ ! -f "$REGISTRY_FILE" ]]; then
    mkdir -p "$OUTPUT_DIR"
    touch "$REGISTRY_FILE"
  fi

  # Find next available number from registry
  NEXT_NUM=1
  if [[ -f "$REGISTRY_FILE" && -s "$REGISTRY_FILE" ]]; then
    while IFS='|' read -r num name created; do
      if [[ "$num" =~ ^[0-9]{3}$ ]]; then
        # Convert to decimal (removes leading zeros)
        num_int=$((10#$num))
        if [[ $num_int -ge $NEXT_NUM ]]; then
          NEXT_NUM=$((num_int + 1))
        fi
      fi
    done < "$REGISTRY_FILE"
  fi

  # Zero-pad to 3 digits
  SPEC_NUM=$(printf "%03d" $NEXT_NUM)
  SPEC_NAME="$SPEC_NUM"
  SPEC_DIR="$OUTPUT_DIR/$SPEC_NUM"
  SPEC_FILE="$SPEC_DIR/spec.md"

  # Add to registry (pipe-delimited: number|name|timestamp)
  TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  echo "$SPEC_NUM|$FEATURE_DESC|$TIMESTAMP" >> "$REGISTRY_FILE"

  echo -e "${GREEN}✓${NC} Assigned spec number: $SPEC_NUM"

  # Check if already exists
  if [[ -d "$SPEC_DIR" ]]; then
    echo -e "${YELLOW}⚠${NC} Spec already exists: $SPEC_DIR"
    echo ""
    echo "DECISION_NEEDED: SPEC_EXISTS"
    echo "MESSAGE: Spec for this feature already exists"
    echo "OPTIONS: --update --spec $SPEC_NAME (Update existing) | --cancel (Cancel)"
    exit 10
  fi

  # Create spec directory
  mkdir -p "$SPEC_DIR"
  echo -e "${GREEN}✓${NC} Created spec directory: $SPEC_DIR"

  # Copy template to spec file
  TEMPLATE_FILE="$TEMPLATE_DIR/spec-template.md"
  if [[ ! -f "$TEMPLATE_FILE" ]]; then
    echo -e "${RED}✗${NC} Template not found: $TEMPLATE_FILE"
    exit 1
  fi

  cp "$TEMPLATE_FILE" "$SPEC_FILE"
  echo -e "${GREEN}✓${NC} Created spec file: $SPEC_FILE"
  echo ""
  echo -e "${CYAN}Spec Number:${NC} $SPEC_NUM"
  echo -e "${CYAN}Feature:${NC} $FEATURE_DESC"
  echo -e "${CYAN}Spec File:${NC} $SPEC_FILE"
fi

# List available product artifacts for Claude to read
echo ""
echo -e "${CYAN}Available product artifacts to extract from:${NC}"

PROD_SKILLS_DIR="$REPO_ROOT/.shipkit/skills"

if [[ -f "$PROD_SKILLS_DIR/prod-user-stories/outputs/user-stories.md" ]]; then
  echo -e "${GREEN}✓${NC} User stories: $PROD_SKILLS_DIR/prod-user-stories/outputs/user-stories.md"
fi

if [[ -f "$PROD_SKILLS_DIR/prod-interaction-design/outputs/interaction-design.md" ]]; then
  echo -e "${GREEN}✓${NC} Interaction design: $PROD_SKILLS_DIR/prod-interaction-design/outputs/interaction-design.md"
fi

if [[ -f "$PROD_SKILLS_DIR/prod-brand-guidelines/outputs/brand-guidelines.md" ]]; then
  echo -e "${GREEN}✓${NC} Brand guidelines: $PROD_SKILLS_DIR/prod-brand-guidelines/outputs/brand-guidelines.md"
fi

if [[ -f "$PROD_SKILLS_DIR/prod-jobs-to-be-done/outputs/jobs-to-be-done.md" ]]; then
  echo -e "${GREEN}✓${NC} Jobs to be done: $PROD_SKILLS_DIR/prod-jobs-to-be-done/outputs/jobs-to-be-done.md"
fi

if [[ -f "$PROD_SKILLS_DIR/prod-success-metrics/outputs/success-metrics.md" ]]; then
  echo -e "${GREEN}✓${NC} Success metrics: $PROD_SKILLS_DIR/prod-success-metrics/outputs/success-metrics.md"
fi

# Constitution
DEV_CONST="$REPO_ROOT/.shipkit/skills/dev-constitution/outputs/constitution.md"
if [[ -f "$DEV_CONST" ]]; then
  echo -e "${GREEN}✓${NC} Technical constitution: $DEV_CONST"
else
  echo -e "${YELLOW}⚠${NC} Technical constitution not found (run /dev-constitution first)"
fi

echo ""
echo -e "${CYAN}Template:${NC} $TEMPLATE_FILE"

echo ""
echo -e "${CYAN}References available:${NC}"
if [[ -d "$REFERENCES_DIR" ]]; then
  find "$REFERENCES_DIR" -type f -name "*.md" | while read ref; do
    echo -e "${GREEN}✓${NC} $(basename $ref): $ref"
  done
fi

echo ""
echo "Ready for Claude to fill spec via dialogue"

exit 0
