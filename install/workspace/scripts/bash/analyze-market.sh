#!/usr/bin/env bash
# analyze-market.sh - Create market analysis document
set -e
set -u

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

RIVALRY=""
NEW_ENTRANTS=""
BUYER_POWER=""
SUPPLIER_POWER=""
SUBSTITUTES=""
COMPETITORS=""
MARKET_SIZE=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --rivalry) RIVALRY="$2"; shift 2;;
    --new-entrants) NEW_ENTRANTS="$2"; shift 2;;
    --buyer-power) BUYER_POWER="$2"; shift 2;;
    --supplier-power) SUPPLIER_POWER="$2"; shift 2;;
    --substitutes) SUBSTITUTES="$2"; shift 2;;
    --competitors) COMPETITORS="$2"; shift 2;;
    --market-size) MARKET_SIZE="$2"; shift 2;;
    *)
      echo -e "${RED}Unknown argument: $1${NC}"
      exit 1
      ;;
  esac
done

if [[ -z "$RIVALRY" ]]; then
  echo -e "${RED}Error: Missing --rivalry${NC}"
  exit 1
fi

mkdir -p .prodkit/discovery

cat > .prodkit/discovery/market-analysis.md <<EOF
# Market Analysis

Generated: $(date +"%Y-%m-%d")

## Porter's Five Forces

### Competitive Rivalry
$RIVALRY

### Threat of New Entrants
$NEW_ENTRANTS

### Bargaining Power of Buyers
$BUYER_POWER

### Bargaining Power of Suppliers
$SUPPLIER_POWER

### Threat of Substitutes
$SUBSTITUTES

## Competitive Landscape

**Key Competitors**: $COMPETITORS

## Market Sizing

$MARKET_SIZE

---
EOF

if [[ -f ".claude/AGENTS.md" ]] || [[ -f ".github/AGENTS.md" ]]; then
  touch .claude/AGENTS.md 2>/dev/null || touch .github/AGENTS.md 2>/dev/null || true
fi

echo -e "${GREEN}✓${NC} Created .prodkit/discovery/market-analysis.md"
exit 0
