#!/usr/bin/env bash
# create-strategy.sh - Create product strategy documents
set -e
set -u

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Arguments
WINNING_ASPIRATION=""
WHERE_TO_PLAY=""
HOW_TO_WIN=""
CAPABILITIES=""
SYSTEMS=""
PROBLEM=""
SEGMENTS=""
VALUE_PROP=""
SOLUTION=""
CHANNELS=""
REVENUE=""
COSTS=""
METRICS=""
UNFAIR_ADVANTAGE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --winning-aspiration) WINNING_ASPIRATION="$2"; shift 2;;
    --where-to-play) WHERE_TO_PLAY="$2"; shift 2;;
    --how-to-win) HOW_TO_WIN="$2"; shift 2;;
    --capabilities) CAPABILITIES="$2"; shift 2;;
    --systems) SYSTEMS="$2"; shift 2;;
    --problem) PROBLEM="$2"; shift 2;;
    --segments) SEGMENTS="$2"; shift 2;;
    --value-prop) VALUE_PROP="$2"; shift 2;;
    --solution) SOLUTION="$2"; shift 2;;
    --channels) CHANNELS="$2"; shift 2;;
    --revenue) REVENUE="$2"; shift 2;;
    --costs) COSTS="$2"; shift 2;;
    --metrics) METRICS="$2"; shift 2;;
    --unfair-advantage) UNFAIR_ADVANTAGE="$2"; shift 2;;
    *)
      echo -e "${RED}Unknown argument: $1${NC}"
      exit 1
      ;;
  esac
done

# Validate required arguments
if [[ -z "$WINNING_ASPIRATION" ]] || [[ -z "$HOW_TO_WIN" ]] || [[ -z "$VALUE_PROP" ]]; then
  echo -e "${RED}Error: Missing required arguments${NC}"
  echo "Required: --winning-aspiration, --how-to-win, --value-prop"
  exit 1
fi

# Create directory
mkdir -p .prodkit/strategy

# Generate business canvas from template
if [[ -f ".prodkit/templates/structure/strategy/business-canvas.template.md" ]]; then
  cat .prodkit/templates/structure/strategy/business-canvas.template.md | \
    sed "s|{{WINNING_ASPIRATION}}|$WINNING_ASPIRATION|g" | \
    sed "s|{{WHERE_TO_PLAY}}|$WHERE_TO_PLAY|g" | \
    sed "s|{{HOW_TO_WIN}}|$HOW_TO_WIN|g" | \
    sed "s|{{CAPABILITIES}}|$CAPABILITIES|g" | \
    sed "s|{{SYSTEMS}}|$SYSTEMS|g" | \
    sed "s|{{PROBLEM}}|$PROBLEM|g" | \
    sed "s|{{SEGMENTS}}|$SEGMENTS|g" | \
    sed "s|{{SOLUTION}}|$SOLUTION|g" | \
    sed "s|{{CHANNELS}}|$CHANNELS|g" | \
    sed "s|{{REVENUE}}|$REVENUE|g" | \
    sed "s|{{COSTS}}|$COSTS|g" | \
    sed "s|{{METRICS}}|$METRICS|g" | \
    sed "s|{{UNFAIR_ADVANTAGE}}|$UNFAIR_ADVANTAGE|g" \
    > .prodkit/strategy/business-canvas.md
else
  # Fallback: Create basic file without template
  cat > .prodkit/strategy/business-canvas.md <<EOF
# Business Canvas

Generated: $(date +"%Y-%m-%d")

## Playing to Win Framework

### Winning Aspiration
$WINNING_ASPIRATION

### Where to Play
$WHERE_TO_PLAY

### How to Win
$HOW_TO_WIN

### Core Capabilities
$CAPABILITIES

### Management Systems
$SYSTEMS

## Lean Canvas

### Problem
$PROBLEM

### Customer Segments
$SEGMENTS

### Solution
$SOLUTION

### Channels
$CHANNELS

### Revenue Streams
$REVENUE

### Cost Structure
$COSTS

### Key Metrics
$METRICS

### Unfair Advantage
$UNFAIR_ADVANTAGE
EOF
fi

# Extract value proposition to separate file
cat > .prodkit/strategy/value-proposition.md <<EOF
# Value Proposition

$VALUE_PROP

---

**How We Win**: $HOW_TO_WIN

**Generated**: $(date +"%Y-%m-%d")
EOF

# Touch AGENTS.md if it exists (trigger reload)
if [[ -f ".claude/AGENTS.md" ]] || [[ -f ".github/AGENTS.md" ]]; then
  touch .claude/AGENTS.md 2>/dev/null || touch .github/AGENTS.md 2>/dev/null || true
fi

echo -e "${GREEN}✓${NC} Created .prodkit/strategy/business-canvas.md"
echo -e "${GREEN}✓${NC} Created .prodkit/strategy/value-proposition.md"

exit 0
