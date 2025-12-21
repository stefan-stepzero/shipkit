#!/usr/bin/env bash
set -euo pipefail

# Find plugin root (directory containing this hooks folder)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ROOT="$(dirname "$SCRIPT_DIR")"

# Path to the meta-skill that gets injected
META_SKILL="$PLUGIN_ROOT/skills/meta/using-shipkit.md"

# JSON-safe string escaping
json_escape() {
    local str="$1"
    str="${str//\\/\\\\}"      # Backslashes
    str="${str//\"/\\\"}"      # Double quotes
    str="${str//$'\n'/\\n}"    # Newlines
    str="${str//$'\r'/\\r}"    # Carriage returns
    str="${str//$'\t'/\\t}"    # Tabs
    printf '%s' "$str"
}

# Read the meta-skill content
if [[ -f "$META_SKILL" ]]; then
    SKILL_CONTENT=$(cat "$META_SKILL")
else
    SKILL_CONTENT="Error: Meta-skill not found at $META_SKILL"
fi

# Escape for JSON
ESCAPED_CONTENT=$(json_escape "$SKILL_CONTENT")

# Output JSON that Claude Code will inject into session context
cat << EOF
{
  "hook": "SessionStart",
  "context": {
    "type": "system_instruction",
    "priority": "high",
    "content": "$ESCAPED_CONTENT"
  }
}
EOF

exit 0
