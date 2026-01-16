#!/usr/bin/env bash
set -e
set -u

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

FEATURE=""
STRATEGIC_VALUE=""
USER_IMPACT=""
COMPETITIVE=""
EFFORT=""
OPPORTUNITY_COST=""
MAINTENANCE=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --feature) FEATURE="$2"; shift 2;;
    --strategic-value) STRATEGIC_VALUE="$2"; shift 2;;
    --user-impact) USER_IMPACT="$2"; shift 2;;
    --competitive) COMPETITIVE="$2"; shift 2;;
    --effort) EFFORT="$2"; shift 2;;
    --opportunity-cost) OPPORTUNITY_COST="$2"; shift 2;;
    --maintenance) MAINTENANCE="$2"; shift 2;;
    *) echo -e "${RED}Unknown: $1${NC}"; exit 1;;
  esac
done

[[ -z "$FEATURE" ]] && { echo -e "${RED}Error: Missing --feature${NC}"; exit 1; }

# Calculate scores
VALUE_SCORE=$(echo "scale=2; ($STRATEGIC_VALUE + $USER_IMPACT + $COMPETITIVE) / 3" | bc)
COST_SCORE=$(echo "scale=2; $EFFORT / 100" | bc)
ROI=$(echo "scale=2; $VALUE_SCORE / $COST_SCORE" | bc)

# Determine recommendation
if (( $(echo "$ROI >= 2.0" | bc -l) )); then
  REC="BUILD"
elif (( $(echo "$ROI >= 1.0" | bc -l) )); then
  REC="DEFER TO V2"
else
  REC="CUT"
fi

mkdir -p .prodkit/analysis

if [[ ! -f ".prodkit/analysis/feature-tradeoffs.md" ]]; then
  cat > .prodkit/analysis/feature-tradeoffs.md <<EOF
# Feature Trade-offs

Generated: $(date +"%Y-%m-%d")

## Analysis

---

EOF
fi

cat >> .prodkit/analysis/feature-tradeoffs.md <<EOF
### $FEATURE

- **Value Score**: $VALUE_SCORE (Strategic: $STRATEGIC_VALUE, User Impact: $USER_IMPACT, Competitive: $COMPETITIVE)
- **Cost Score**: $COST_SCORE (Effort: $EFFORT%)
- **ROI**: $ROI
- **Recommendation**: **$REC**
- **Opportunity Cost**: $OPPORTUNITY_COST
- **Maintenance**: $MAINTENANCE

---

EOF

[[ -f ".claude/AGENTS.md" ]] || [[ -f ".github/AGENTS.md" ]] && { touch .claude/AGENTS.md 2>/dev/null || touch .github/AGENTS.md 2>/dev/null || true; }

echo -e "${GREEN}✓${NC} Analyzed '$FEATURE' → ROI: $ROI → $REC"
exit 0
