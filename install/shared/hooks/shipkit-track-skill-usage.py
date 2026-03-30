#!/usr/bin/env python3
"""
Shipkit - Skill Usage Tracker

Appends one JSONL line per Skill() invocation to .shipkit/observability/.
Each session gets its own file (keyed by session_id). Session-start hook
cleans old files.

Hook type: PostToolUse (matcher: Skill)
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime

HOOK_NAME = "track-skill-usage"

def _find_project_root(start: Path) -> Path | None:
    """Walk up from start to find the project root (directory containing .shipkit/ or .claude/)."""
    current = start.resolve()
    for _ in range(20):  # Safety limit
        if (current / '.shipkit').is_dir() or (current / '.claude').is_dir():
            return current
        parent = current.parent
        if parent == current:
            break  # Hit filesystem root
        current = parent
    return None


def main():
    print(f"[shipkit:{HOOK_NAME}] running", file=sys.stderr)
    # Read hook input from stdin
    try:
        hook_input = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        return 0  # Silent exit on parse error

    # Extract skill name from tool_input
    tool_input = hook_input.get('tool_input', {})
    skill_name = tool_input.get('skill', '')

    if not skill_name:
        return 0  # No skill to track

    # Find project root
    cwd = hook_input.get('cwd', '')
    if not cwd:
        return 0

    project_root = _find_project_root(Path(cwd))
    if not project_root:
        return 0  # Not in a Shipkit project

    obs_dir = project_root / '.shipkit' / 'observability'
    obs_dir.mkdir(parents=True, exist_ok=True)

    # Build JSONL entry
    session_id = hook_input.get('session_id', 'unknown')
    agent_id = hook_input.get('agent_id', '')
    agent_type = hook_input.get('agent_type', '')
    now = datetime.now().isoformat(timespec='seconds')

    entry = {
        'skill': skill_name,
        'timestamp': now,
        'session': session_id,
    }
    if agent_id:
        entry['agentId'] = agent_id
    if agent_type:
        entry['agentType'] = agent_type

    # Append to session-specific JSONL file (atomic append, no read-modify-write)
    tracking_file = obs_dir / f'skill-usage.{session_id}.local.jsonl'
    try:
        with open(tracking_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    except IOError:
        pass  # Silent fail on write error

    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        print(f"[shipkit:{HOOK_NAME}] ERROR: {e}", file=sys.stderr)
        sys.exit(0)
