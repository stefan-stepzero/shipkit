#!/usr/bin/env bash
# session-start.sh - Load Shipkit Master Skill at session start
#
# This hook runs when Claude Code starts a new session (startup, resume, clear, compact).
# According to official Claude Code docs, SessionStart stdout is automatically added to context.
#
# We output:
# 1. The Shipkit Master Skill (skill definitions and guidance)
# 2. Previous session state (if exists from last /clear)

set -e

# Find plugin root (directory containing this hooks folder)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ROOT="$(dirname "$SCRIPT_DIR")"

# Path to the Shipkit Master Skill
META_SKILL="$PLUGIN_ROOT/skills/shipkit-master/SKILL.md"

# Check if the skill file exists
if [[ ! -f "$META_SKILL" ]]; then
  cat << 'EOF'
⚠️  Shipkit Master Skill not found

Expected location: .claude/skills/shipkit-master/SKILL.md

Shipkit may not be properly installed. Run the installer again.
EOF
  exit 0
fi

# Output the skill content directly to stdout
cat "$META_SKILL"

# Auto-inject previous session state if it exists
STATE_FILE=".shipkit/progress/state.md"
if [[ -f "$STATE_FILE" ]]; then
  echo ""
  echo "---"
  echo ""
  echo "## Previous Session State"
  echo ""
  cat "$STATE_FILE"
fi

exit 0
