#!/usr/bin/env bash
# create-brand.sh - Create brand guidelines documents
set -e
set -u

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

PERSONALITY=""
COLORS=""
TYPOGRAPHY=""
VISUAL_STYLE=""
ANIMATION=""
ERROR_HANDLING=""
DIFFERENTIATION=""
REFERENCES=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --personality) PERSONALITY="$2"; shift 2;;
    --colors) COLORS="$2"; shift 2;;
    --typography) TYPOGRAPHY="$2"; shift 2;;
    --visual-style) VISUAL_STYLE="$2"; shift 2;;
    --animation) ANIMATION="$2"; shift 2;;
    --error-handling) ERROR_HANDLING="$2"; shift 2;;
    --differentiation) DIFFERENTIATION="$2"; shift 2;;
    --references) REFERENCES="$2"; shift 2;;
    *) echo -e "${RED}Unknown: $1${NC}"; exit 1;;
  esac
done

[[ -z "$PERSONALITY" ]] && { echo -e "${RED}Error: Missing --personality${NC}"; exit 1; }

mkdir -p .prodkit/brand

cat > .prodkit/brand/personality.md <<EOF
# Brand Personality

Generated: $(date +"%Y-%m-%d")

$PERSONALITY

## Tone of Voice
How we communicate with users.

---
EOF

cat > .prodkit/brand/visual-direction.md <<EOF
# Visual Direction

Generated: $(date +"%Y-%m-%d")

## Color Palette
$COLORS

## Typography
$TYPOGRAPHY

## Visual Style
$VISUAL_STYLE

## Animation & Interaction
$ANIMATION

## Error Handling
$ERROR_HANDLING

---
EOF

cat > .prodkit/brand/reference-examples.md <<EOF
# Reference Examples

Generated: $(date +"%Y-%m-%d")

## Competitive Differentiation
$DIFFERENTIATION

## Design References
$REFERENCES

---
EOF

[[ -f ".claude/AGENTS.md" ]] || [[ -f ".github/AGENTS.md" ]] && { touch .claude/AGENTS.md 2>/dev/null || touch .github/AGENTS.md 2>/dev/null || true; }

echo -e "${GREEN}✓${NC} Created .prodkit/brand/ documents"
exit 0
