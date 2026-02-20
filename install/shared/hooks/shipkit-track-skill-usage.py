#!/usr/bin/env python3
"""
Shipkit - Skill Usage Tracker

Tracks how many times each skill is invoked to identify usage patterns
and help discover stale or underutilized skills.

Hook type: PostToolUse (matcher: Skill)
"""

import sys
import json
from pathlib import Path
from datetime import datetime


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

    # Find project root — walk up from cwd to find .shipkit/ or .claude/
    # This handles cases where Claude cd'd into a subdirectory (e.g. frontend/)
    cwd = hook_input.get('cwd', '')
    if not cwd:
        return 0

    project_root = _find_project_root(Path(cwd))
    if not project_root:
        return 0  # Not in a Shipkit project

    shipkit_dir = project_root / '.shipkit'

    # Create .shipkit if it doesn't exist
    if not shipkit_dir.exists():
        shipkit_dir.mkdir(parents=True, exist_ok=True)

    tracking_file = shipkit_dir / 'skill-usage.json'

    # Load existing data or create new
    if tracking_file.exists():
        try:
            data = json.loads(tracking_file.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, IOError):
            data = create_empty_tracking()
    else:
        data = create_empty_tracking()

    # Update tracking
    now = datetime.now().isoformat(timespec='seconds')

    data['lastUpdated'] = now
    data['totalInvocations'] = data.get('totalInvocations', 0) + 1

    if 'skills' not in data:
        data['skills'] = {}

    if skill_name not in data['skills']:
        data['skills'][skill_name] = {
            'count': 0,
            'firstUsed': now,
            'lastUsed': now
        }

    data['skills'][skill_name]['count'] += 1
    data['skills'][skill_name]['lastUsed'] = now

    # Preserve firstUsed if it exists
    if 'firstUsed' not in data['skills'][skill_name]:
        data['skills'][skill_name]['firstUsed'] = now

    # Save updated data
    try:
        tracking_file.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
    except IOError:
        pass  # Silent fail on write error

    return 0


def create_empty_tracking():
    """Create empty tracking structure."""
    return {
        'version': '1.0',
        'created': datetime.now().isoformat(timespec='seconds'),
        'lastUpdated': datetime.now().isoformat(timespec='seconds'),
        'totalInvocations': 0,
        'skills': {}
    }


if __name__ == '__main__':
    sys.exit(main())
