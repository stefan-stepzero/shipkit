#!/usr/bin/env bash
set -e
set -u

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

GOAL=""
KPI=""
CURRENT=""
TARGET=""
TIMELINE=""
INSTRUMENT=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --goal) GOAL="$2"; shift 2;;
    --kpi) KPI="$2"; shift 2;;
    --current) CURRENT="$2"; shift 2;;
    --target) TARGET="$2"; shift 2;;
    --timeline) TIMELINE="$2"; shift 2;;
    --instrument) INSTRUMENT="$2"; shift 2;;
    *) echo -e "${RED}Unknown: $1${NC}"; exit 1;;
  esac
done

[[ -z "$KPI" ]] && { echo -e "${RED}Error: Missing --kpi${NC}"; exit 1; }

mkdir -p .prodkit/metrics

if [[ ! -f ".prodkit/metrics/success-definition.md" ]]; then
  cat > .prodkit/metrics/success-definition.md <<EOF
# Success Definition

Generated: $(date +"%Y-%m-%d")

## Business Goals

$GOAL

## KPIs

---

EOF
fi

cat >> .prodkit/metrics/success-definition.md <<EOF
### $KPI

- **Current Baseline**: $CURRENT
- **Target**: $TARGET
- **Timeline**: $TIMELINE
- **How to Measure**: $INSTRUMENT

---

EOF

[[ -f ".claude/AGENTS.md" ]] || [[ -f ".github/AGENTS.md" ]] && { touch .claude/AGENTS.md 2>/dev/null || touch .github/AGENTS.md 2>/dev/null || true; }

echo -e "${GREEN}✓${NC} Added KPI: $KPI"
exit 0
