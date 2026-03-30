#!/usr/bin/env python3
"""
Shipkit SubagentStart Hook — Phase Context Injection

Injects current orchestration state into every dispatched subagent so agents
start with awareness of project stage, current loop, and completed artifacts.

Hook event: SubagentStart
Exit 0 + JSON: additionalContext injected into subagent
Exit 1: silently skipped (no .shipkit/, built-in agent, etc.)
"""

import json
import os
import sys
from pathlib import Path

HOOK_NAME = "subagent-context"
# Built-in agents that don't need orchestration context
SKIP_AGENTS = {"Explore", "Plan", "Bash", "general-purpose", "statusline-setup", "claude-code-guide"}


def find_project_root(cwd: str) -> Path | None:
    current = Path(cwd).resolve()
    for _ in range(20):
        if (current / '.shipkit').is_dir():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None


def read_json_safe(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError):
        return None


def build_context(project_root: Path) -> str | None:
    shipkit = project_root / '.shipkit'
    if not shipkit.is_dir():
        return None

    parts = []

    # Project identity from why.json
    why = read_json_safe(shipkit / 'why.json')
    if why:
        name = why.get('projectName') or why.get('name') or project_root.name
        approach = why.get('approach', {}).get('oneLiner', '')
        stage = why.get('stage', '')
        parts.append(f"Project: {name}")
        if stage:
            parts.append(f"Stage: {stage}")
        if approach:
            parts.append(f"Approach: {approach}")

    # Current orchestration state from progress.json
    progress = read_json_safe(shipkit / 'progress.json')
    if progress:
        current_loop = progress.get('currentLoop', '')
        current_dispatch = progress.get('currentDispatch', '')
        if current_loop:
            parts.append(f"Loop: {current_loop}")
        if current_dispatch:
            parts.append(f"Dispatch: {current_dispatch}")

    # List completed artifacts
    completed = []
    for name in ['why.json', 'product-discovery.json', 'product-definition.json',
                 'engineering-definition.json', 'goals.json', 'stack.json',
                 'architecture.json', 'codebase-index.json']:
        if (shipkit / name).exists():
            completed.append(name.replace('.json', ''))
    if completed:
        parts.append(f"Context: {', '.join(completed)}")

    # Active specs count
    specs_dir = shipkit / 'specs' / 'active'
    if specs_dir.is_dir():
        specs = list(specs_dir.glob('*.json'))
        if specs:
            parts.append(f"Active specs: {len(specs)}")

    if not parts:
        return None

    return ' | '.join(parts)


def main():
    print(f"[shipkit:{HOOK_NAME}] running", file=sys.stderr)
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(1)

    # Skip built-in agents
    agent_type = hook_input.get('agent_type', '')
    if agent_type in SKIP_AGENTS:
        sys.exit(1)

    cwd = hook_input.get('cwd', os.getcwd())
    project_root = find_project_root(cwd)
    if not project_root:
        sys.exit(1)

    context = build_context(project_root)
    if not context:
        sys.exit(1)

    output = {
        "hookSpecificOutput": {
            "hookEventName": "SubagentStart",
            "additionalContext": f"[Shipkit] {context}"
        }
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"[shipkit:{HOOK_NAME}] ERROR: {e}", file=sys.stderr)
        sys.exit(0)
