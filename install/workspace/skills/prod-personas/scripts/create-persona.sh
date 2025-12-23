#!/usr/bin/env bash
# create-persona.sh - Create or append persona to personas.md
# Part of shipkit prod-personas skill

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
SKIP_PREREQS=false
NAME=""
AGE=""
ROLE=""
GOALS=""
PAINS=""
BEHAVIORS=""
TECH_SAVVY=""
DECISION_FACTORS=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --skip-prereqs)
      SKIP_PREREQS=true
      shift
      ;;
    --name)
      NAME="$2"
      shift 2
      ;;
    --age)
      AGE="$2"
      shift 2
      ;;
    --role)
      ROLE="$2"
      shift 2
      ;;
    --goals)
      GOALS="$2"
      shift 2
      ;;
    --pains)
      PAINS="$2"
      shift 2
      ;;
    --behaviors)
      BEHAVIORS="$2"
      shift 2
      ;;
    --tech-savvy)
      TECH_SAVVY="$2"
      shift 2
      ;;
    --decision-factors)
      DECISION_FACTORS="$2"
      shift 2
      ;;
    --help|-h)
      echo "Usage: $0 [options]"
      echo ""
      echo "Flags:"
      echo "  --skip-prereqs        Skip prerequisite checks"
      echo "  --name <value>        Persona name (required)"
      echo "  --goals <value>       Goals (required)"
      echo "  --pains <value>       Pain points (required)"
      echo "  --age <value>         Age (optional)"
      echo "  --role <value>        Role (optional)"
      echo "  --behaviors <value>   Current behavior (optional)"
      echo "  --tech-savvy <value>  Tech savviness (optional)"
      echo "  --decision-factors    Decision factors (optional)"
      exit 0
      ;;
    *)
      echo -e "${RED}Unknown argument: $1${NC}" >&2
      exit 1
      ;;
  esac
done

# Check prerequisites
check_skill_prerequisites "prod-personas" "$SKIP_PREREQS"

# Validate required fields (only when provided - Claude will provide via dialogue)
if [[ -n "$NAME" ]] && [[ -z "$GOALS" || -z "$PAINS" ]]; then
  echo -e "${RED}Error: Missing required arguments${NC}" >&2
  echo "Required: --name, --goals, --pains" >&2
  exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Output file location
OUTPUT_FILE="$OUTPUT_DIR/personas.md"

# Initialize file if it doesn't exist
if [[ ! -f "$OUTPUT_FILE" ]]; then
  cat > "$OUTPUT_FILE" <<EOF
# Personas

Generated: $(date +"%Y-%m-%d")

---

EOF
  echo -e "${GREEN}✓${NC} Created personas file: $OUTPUT_FILE"
fi

# If persona data provided, append it
if [[ -n "$NAME" ]]; then
  cat >> "$OUTPUT_FILE" <<EOF
## $NAME

**Demographics**:
- Age: ${AGE:-Not specified}
- Role: ${ROLE:-Not specified}

**Goals**:
$GOALS

**Pain Points**:
$PAINS

**Current Behavior**:
${BEHAVIORS:-Not specified}

**Tech Savviness**: ${TECH_SAVVY:-Not specified}

**Decision Factors**:
${DECISION_FACTORS:-Not specified}

---

EOF
  echo -e "${GREEN}✓${NC} Added persona '$NAME' to $OUTPUT_FILE"
else
  # No persona data - Claude will fill via dialogue
  echo -e "${CYAN}Template available at:${NC} $TEMPLATE_DIR/persona-template.md"
  echo -e "${CYAN}Output file:${NC} $OUTPUT_FILE"
  echo ""
  echo "Ready for Claude to guide persona creation via dialogue"
fi

exit 0
