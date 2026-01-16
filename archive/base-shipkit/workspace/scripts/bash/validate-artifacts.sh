#!/usr/bin/env bash
set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "Validating ProdKit artifacts..."
ERRORS=0

check_file() {
  if [[ -f "$1" ]]; then
    echo -e "${GREEN}✓${NC} $1"
  else
    echo -e "${RED}✗${NC} $1 (missing)"
    ((ERRORS++))
  fi
}

echo ""
echo "Strategy:"
check_file ".prodkit/strategy/business-canvas.md"
check_file ".prodkit/strategy/value-proposition.md"

echo ""
echo "Discovery:"
check_file ".prodkit/discovery/personas.md"
check_file ".prodkit/discovery/jobs-to-be-done-current.md"
check_file ".prodkit/discovery/market-analysis.md"
check_file ".prodkit/discovery/assumptions-and-risks.md"

echo ""
echo "Brand:"
check_file ".prodkit/brand/personality.md"
check_file ".prodkit/brand/visual-direction.md"

echo ""
echo "Design:"
check_file ".prodkit/design/future-state-journeys.md"
check_file ".prodkit/design/interaction-patterns.md"

echo ""
echo "Requirements:"
check_file ".prodkit/requirements/user-stories.md"

echo ""
echo "Metrics:"
check_file ".prodkit/metrics/success-definition.md"

echo ""
if [[ $ERRORS -eq 0 ]]; then
  echo -e "${GREEN}✓ All core artifacts present${NC}"
  exit 0
else
  echo -e "${RED}✗ $ERRORS missing artifacts${NC}"
  exit 1
fi
