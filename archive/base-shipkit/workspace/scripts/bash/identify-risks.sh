#!/usr/bin/env bash
set -e
set -u

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

ASSUMPTION=""
IMPACT=""
CONFIDENCE=""
TEST=""
RISK=""
LIKELIHOOD=""
RISK_IMPACT=""
MITIGATION=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --assumption) ASSUMPTION="$2"; shift 2;;
    --impact) IMPACT="$2"; shift 2;;
    --confidence) CONFIDENCE="$2"; shift 2;;
    --test) TEST="$2"; shift 2;;
    --risk) RISK="$2"; shift 2;;
    --likelihood) LIKELIHOOD="$2"; shift 2;;
    --risk-impact) RISK_IMPACT="$2"; shift 2;;
    --mitigation) MITIGATION="$2"; shift 2;;
    *) echo -e "${RED}Unknown: $1${NC}"; exit 1;;
  esac
done

mkdir -p .prodkit/discovery

if [[ ! -f ".prodkit/discovery/assumptions-and-risks.md" ]]; then
  echo -e "# Assumptions and Risks\n\nGenerated: $(date +"%Y-%m-%d")\n\n## Assumptions\n\n---\n" > .prodkit/discovery/assumptions-and-risks.md
fi

if [[ -n "$ASSUMPTION" ]]; then
  cat >> .prodkit/discovery/assumptions-and-risks.md <<EOF
### $ASSUMPTION

- **Impact if Wrong**: $IMPACT
- **Confidence Level**: $CONFIDENCE
- **How to Test**: $TEST

EOF
fi

if [[ -n "$RISK" ]]; then
  if ! grep -q "## Strategic Risks" .prodkit/discovery/assumptions-and-risks.md; then
    echo -e "\n## Strategic Risks\n" >> .prodkit/discovery/assumptions-and-risks.md
  fi
  
  cat >> .prodkit/discovery/assumptions-and-risks.md <<EOF
### $RISK

- **Likelihood**: $LIKELIHOOD
- **Impact**: $RISK_IMPACT
- **Mitigation**: $MITIGATION

EOF
fi

[[ -f ".claude/AGENTS.md" ]] || [[ -f ".github/AGENTS.md" ]] && { touch .claude/AGENTS.md 2>/dev/null || touch .github/AGENTS.md 2>/dev/null || true; }

echo -e "${GREEN}✓${NC} Updated assumptions and risks"
exit 0
