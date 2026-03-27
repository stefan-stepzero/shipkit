#!/usr/bin/env python3
"""
Shipkit UserPromptSubmit Hook — Missing Context Early Warning

Checks if .shipkit/ context exists when user submits a prompt. If missing or
incomplete, injects a gentle nudge as additionalContext. Only warns once per
session to avoid nagging.

Hook event: UserPromptSubmit
Exit 0 + JSON: additionalContext with guidance
Exit 1: no warning needed (context exists or already warned)
"""

import json
import os
import sys
from pathlib import Path

# Key context files in priority order
CONTEXT_FILES = {
    'why.json': '/shipkit-why-project',
    'stack.json': '/shipkit-project-context',
    'architecture.json': '/shipkit-project-context',
    'product-discovery.json': '/shipkit-product-discovery',
    'product-definition.json': '/shipkit-product-definition',
    'engineering-definition.json': '/shipkit-engineering-definition',
    'goals.json': '/shipkit-product-goals',
}

# Minimum viable context — at least one of these should exist
MINIMUM_FILES = ['why.json', 'stack.json']


def find_project_root(cwd: str) -> Path | None:
    current = Path(cwd).resolve()
    for _ in range(20):
        if (current / '.claude').is_dir() or (current / '.shipkit').is_dir():
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

    cwd = hook_input.get('cwd', os.getcwd())
    project_root = find_project_root(cwd)
    if not project_root:
        sys.exit(1)

    shipkit_dir = project_root / '.shipkit'

    # Check if we already warned this session
    warn_flag = shipkit_dir / '.context-warned.local' if shipkit_dir.is_dir() else project_root / '.claude' / '.context-warned.local'
    session_id = hook_input.get('session_id', '')

    if warn_flag.exists():
        try:
            stored_session = warn_flag.read_text(encoding='utf-8').strip()
            if stored_session == session_id:
                sys.exit(1)  # Already warned this session
        except OSError:
            pass

    # Case 1: No .shipkit/ at all
    if not shipkit_dir.is_dir():
        # Write warn flag
        try:
            warn_flag.parent.mkdir(parents=True, exist_ok=True)
            warn_flag.write_text(session_id, encoding='utf-8')
        except OSError:
            pass

        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": "[Shipkit] No .shipkit/ context found. Run /shipkit-project-context to scan the codebase and /shipkit-why-project to define the project approach."
            }
        }
        print(json.dumps(output))
        sys.exit(0)

    # Case 2: .shipkit/ exists — check for minimum viable context
    has_minimum = any((shipkit_dir / f).exists() for f in MINIMUM_FILES)
    if has_minimum:
        sys.exit(1)  # Good enough — don't nag

    # Case 3: .shipkit/ exists but missing minimum files
    missing = []
    for filename, skill in CONTEXT_FILES.items():
        if not (shipkit_dir / filename).exists():
            missing.append(f"  - {filename} (run {skill})")

    if not missing:
        sys.exit(1)

    # Write warn flag
    try:
        warn_flag.write_text(session_id, encoding='utf-8')
    except OSError:
        pass

    msg = "[Shipkit] .shipkit/ exists but missing key context:\n" + "\n".join(missing[:5])
    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": msg
        }
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == '__main__':
    main()
