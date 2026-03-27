#!/usr/bin/env python3
"""
Shipkit PostToolUseFailure Hook — Orchestration Diagnostics

Logs Skill dispatch failures to .shipkit/diagnostics.local.json for debugging
orchestration issues. Only captures Skill tool failures, ignores everything else.

Hook event: PostToolUseFailure
Exit 0: logged (never blocks — PostToolUseFailure is non-blockable anyway)
Exit 1: not a Skill failure, skip
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

MAX_ENTRIES = 100


def find_project_root(cwd: str) -> Path | None:
    current = Path(cwd).resolve()
    for _ in range(20):
        if (current / '.shipkit').is_dir() or (current / '.claude').is_dir():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(1)

    # Only log Skill dispatch failures
    tool_name = hook_input.get('tool_name', '')
    if tool_name != 'Skill':
        sys.exit(1)

    cwd = hook_input.get('cwd', os.getcwd())
    project_root = find_project_root(cwd)
    if not project_root:
        sys.exit(1)

    shipkit_dir = project_root / '.shipkit'
    shipkit_dir.mkdir(parents=True, exist_ok=True)
    diag_file = shipkit_dir / 'diagnostics.local.json'

    # Build diagnostic entry
    tool_input = hook_input.get('tool_input', {})
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "skill": tool_input.get('skill', tool_input.get('name', 'unknown')),
        "error": hook_input.get('error', 'unknown error'),
        "is_interrupt": hook_input.get('is_interrupt', False),
        "agent_type": hook_input.get('agent_type', ''),
        "session_id": hook_input.get('session_id', ''),
    }

    # Read existing entries
    entries = []
    if diag_file.exists():
        try:
            entries = json.loads(diag_file.read_text(encoding='utf-8'))
            if not isinstance(entries, list):
                entries = []
        except (json.JSONDecodeError, OSError):
            entries = []

    # Append and rotate
    entries.append(entry)
    if len(entries) > MAX_ENTRIES:
        entries = entries[-MAX_ENTRIES:]

    # Write back
    try:
        diag_file.write_text(json.dumps(entries, indent=2), encoding='utf-8')
    except OSError:
        pass

    sys.exit(0)


if __name__ == '__main__':
    main()
