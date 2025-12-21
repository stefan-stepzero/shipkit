#!/usr/bin/env bash
set -e
set -u

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

PERSONA=""
JOURNEY=""
ENTRY=""
MOMENTS=""
DECISIONS=""
SUCCESS=""
ERRORS=""
PATTERNS=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --persona) PERSONA="$2"; shift 2;;
    --journey) JOURNEY="$2"; shift 2;;
    --entry) ENTRY="$2"; shift 2;;
    --moments) MOMENTS="$2"; shift 2;;
    --decisions) DECISIONS="$2"; shift 2;;
    --success) SUCCESS="$2"; shift 2;;
    --errors) ERRORS="$2"; shift 2;;
    --patterns) PATTERNS="$2"; shift 2;;
    *) echo -e "${RED}Unknown: $1${NC}"; exit 1;;
  esac
done

[[ -z "$PERSONA" ]] && { echo -e "${RED}Error: Missing --persona${NC}"; exit 1; }

mkdir -p .prodkit/design

if [[ ! -f ".prodkit/design/future-state-journeys.md" ]]; then
  echo -e "# Future State Journeys\n\nGenerated: $(date +"%Y-%m-%d")\n\n---\n" > .prodkit/design/future-state-journeys.md
fi

cat >> .prodkit/design/future-state-journeys.md <<EOF
## $PERSONA: $JOURNEY

**Entry Point**: $ENTRY

**Critical Moments**: $MOMENTS

**Decision Points**: $DECISIONS

**Success State**: $SUCCESS

**Error States**: $ERRORS

---

EOF

if [[ ! -f ".prodkit/design/interaction-patterns.md" ]]; then
  echo -e "# Interaction Patterns\n\nGenerated: $(date +"%Y-%m-%d")\n\n---\n" > .prodkit/design/interaction-patterns.md
fi

cat >> .prodkit/design/interaction-patterns.md <<EOF
## $JOURNEY Patterns

$PATTERNS

---

EOF

[[ -f ".claude/AGENTS.md" ]] || [[ -f ".github/AGENTS.md" ]] && { touch .claude/AGENTS.md 2>/dev/null || touch .github/AGENTS.md 2>/dev/null || true; }

echo -e "${GREEN}✓${NC} Added journey '$JOURNEY' for '$PERSONA'"
exit 0
