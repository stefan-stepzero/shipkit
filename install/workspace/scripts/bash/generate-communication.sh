#!/usr/bin/env bash
set -e
set -u

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

ARTIFACTS=""
AUDIENCE=""
FORMAT=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --artifacts) ARTIFACTS="$2"; shift 2;;
    --audience) AUDIENCE="$2"; shift 2;;
    --format) FORMAT="$2"; shift 2;;
    *) echo -e "${RED}Unknown: $1${NC}"; exit 1;;
  esac
done

[[ -z "$ARTIFACTS" ]] || [[ -z "$AUDIENCE" ]] || [[ -z "$FORMAT" ]] && { 
  echo -e "${RED}Error: Missing required arguments${NC}"
  echo "Required: --artifacts, --audience, --format"
  exit 1
}

mkdir -p .prodkit/comms

FILENAME=".prodkit/comms/$(date +%Y-%m-%d)-$AUDIENCE-$FORMAT.html"
TEMPLATE=".prodkit/templates/communication/${AUDIENCE}-${FORMAT}.template.html"

if [[ -f "$TEMPLATE" ]]; then
  cp "$TEMPLATE" "$FILENAME"
  echo -e "${GREEN}✓${NC} Generated $FILENAME from template"
else
  cat > "$FILENAME" <<EOF
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Product Communication</title>
  <style>
    body { font-family: -apple-system, sans-serif; padding: 60px; max-width: 1000px; margin: 0 auto; }
    h1 { color: #0f172a; }
    h2 { color: #2563eb; font-size: 14px; text-transform: uppercase; }
  </style>
</head>
<body>
  <h1>Product Communication</h1>
  <p>Generated: $(date +"%Y-%m-%d")</p>
  <p><strong>Audience</strong>: $AUDIENCE</p>
  <p><strong>Artifacts</strong>: $ARTIFACTS</p>
  <p><em>Note: Template not found. This is a placeholder.</em></p>
</body>
</html>
EOF
  echo -e "${YELLOW}⚠${NC} Template not found, created basic HTML at $FILENAME"
fi

[[ -f ".claude/AGENTS.md" ]] || [[ -f ".github/AGENTS.md" ]] && { touch .claude/AGENTS.md 2>/dev/null || touch .github/AGENTS.md 2>/dev/null || true; }

echo -e "${GREEN}✓${NC} Communication artifact: $FILENAME"
exit 0
