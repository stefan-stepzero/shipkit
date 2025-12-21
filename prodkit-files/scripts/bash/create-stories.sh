#!/usr/bin/env bash
set -e
set -u

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

PERSONA=""
STORY=""
ACCEPTANCE=""
PRIORITY=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --persona) PERSONA="$2"; shift 2;;
    --story) STORY="$2"; shift 2;;
    --acceptance) ACCEPTANCE="$2"; shift 2;;
    --priority) PRIORITY="$2"; shift 2;;
    *) echo -e "${RED}Unknown: $1${NC}"; exit 1;;
  esac
done

[[ -z "$STORY" ]] && { echo -e "${RED}Error: Missing --story${NC}"; exit 1; }

mkdir -p .prodkit/requirements

if [[ ! -f ".prodkit/requirements/user-stories.md" ]]; then
  echo -e "# User Stories\n\nGenerated: $(date +"%Y-%m-%d")\n\n---\n" > .prodkit/requirements/user-stories.md
fi

cat >> .prodkit/requirements/user-stories.md <<EOF
## $STORY

**Priority**: $PRIORITY

**Acceptance Criteria**:
$ACCEPTANCE

**Persona**: $PERSONA

---

EOF

[[ -f ".claude/AGENTS.md" ]] || [[ -f ".github/AGENTS.md" ]] && { touch .claude/AGENTS.md 2>/dev/null || touch .github/AGENTS.md 2>/dev/null || true; }

echo -e "${GREEN}✓${NC} Added user story (Priority: $PRIORITY)"
exit 0
