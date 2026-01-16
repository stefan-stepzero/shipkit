#!/usr/bin/env bash
# create-persona.sh - Create or append persona to personas.md
set -e
set -u

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
      echo -e "${RED}Unknown argument: $1${NC}"
      exit 1
      ;;
  esac
done

# Validate
if [[ -z "$NAME" ]] || [[ -z "$GOALS" ]] || [[ -z "$PAINS" ]]; then
  echo -e "${RED}Error: Missing required arguments${NC}"
  echo "Required: --name, --goals, --pains"
  exit 1
fi

# Create directory
mkdir -p .prodkit/discovery

# Initialize file if it doesn't exist
if [[ ! -f ".prodkit/discovery/personas.md" ]]; then
  cat > .prodkit/discovery/personas.md <<EOF
# Personas

Generated: $(date +"%Y-%m-%d")

---

EOF
fi

# Append persona to file
cat >> .prodkit/discovery/personas.md <<EOF
## $NAME

**Demographics**:
- Age: $AGE
- Role: $ROLE

**Goals**:
$GOALS

**Pain Points**:
$PAINS

**Current Behavior**:
$BEHAVIORS

**Tech Savviness**: $TECH_SAVVY

**Decision Factors**:
$DECISION_FACTORS

---

EOF

# Touch AGENTS.md
if [[ -f ".claude/AGENTS.md" ]] || [[ -f ".github/AGENTS.md" ]]; then
  touch .claude/AGENTS.md 2>/dev/null || touch .github/AGENTS.md 2>/dev/null || true
fi

echo -e "${GREEN}✓${NC} Added persona '$NAME' to .prodkit/discovery/personas.md"

exit 0
