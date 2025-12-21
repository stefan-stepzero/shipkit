#!/usr/bin/env bash
set -e

GREEN='\033[0;32m'
NC='\033[0m'

AGENT_FILE=".claude/AGENTS.md"
[[ ! -f "$AGENT_FILE" ]] && AGENT_FILE=".github/AGENTS.md"

if [[ -f "$AGENT_FILE" ]]; then
  touch "$AGENT_FILE"
  echo -e "${GREEN}✓${NC} Triggered agent context reload"
else
  echo "No AGENTS.md file found (optional)"
fi

exit 0
