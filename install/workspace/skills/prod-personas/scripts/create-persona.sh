#!/usr/bin/env bash
# create-persona.sh - Create or append persona to personas.md
# Part of shipkit prod-personas skill

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
RED='\033[0;31m'
NC='\033[0m'

# Arguments
NAME=""
AGE=""
ROLE=""
GOALS=""
PAINS=""
BEHAVIORS=""
TECH_SAVVY=""
DECISION_FACTORS=""

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --name) NAME="$2"; shift 2;;
    --age) AGE="$2"; shift 2;;
    --role) ROLE="$2"; shift 2;;
    --goals) GOALS="$2"; shift 2;;
    --pains) PAINS="$2"; shift 2;;
    --behaviors) BEHAVIORS="$2"; shift 2;;
    --tech-savvy) TECH_SAVVY="$2"; shift 2;;
    --decision-factors) DECISION_FACTORS="$2"; shift 2;;
    *)
      echo -e "${RED}Unknown argument: $1${NC}" >&2
      exit 1
      ;;
  esac
done

# Validate required fields
if [[ -z "$NAME" ]] || [[ -z "$GOALS" ]] || [[ -z "$PAINS" ]]; then
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
fi

# Append persona to file
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

exit 0
