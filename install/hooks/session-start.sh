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

# Suggest status check for session resume
echo ""
echo "---"
echo ""
echo "## Session Start"
echo ""
echo "📍 **Need to orient?** Run \`/shipkit-status\` to see where you are and what's next."
echo ""

exit 0
