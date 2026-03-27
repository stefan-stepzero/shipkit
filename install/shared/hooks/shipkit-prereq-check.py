#!/usr/bin/env python3
"""
Shipkit InstructionsLoaded Hook — Prerequisite Validation

When a Shipkit skill is loaded, checks if its required .shipkit/ context files
exist. If missing, injects additionalContext listing what's needed and which
skill to run.

Hook event: InstructionsLoaded
Exit 0 + JSON: additionalContext with missing prerequisites
Exit 1: not a Shipkit skill, or all prerequisites met
"""

import json
import os
import sys
from pathlib import Path

# Skill name → list of (required file, skill to create it)
SKILL_PREREQUISITES = {
    'shipkit-spec': [
        ('why.json', '/shipkit-why-project'),
        ('product-definition.json', '/shipkit-product-definition'),
    ],
    'shipkit-plan': [
        ('why.json', '/shipkit-why-project'),
    ],
    'shipkit-engineering-definition': [
        ('why.json', '/shipkit-why-project'),
        ('product-definition.json', '/shipkit-product-definition'),
        ('stack.json', '/shipkit-project-context'),
    ],
    'shipkit-engineering-goals': [
        ('why.json', '/shipkit-why-project'),
        ('engineering-definition.json', '/shipkit-engineering-definition'),
    ],
    'shipkit-product-definition': [
        ('why.json', '/shipkit-why-project'),
        ('product-discovery.json', '/shipkit-product-discovery'),
    ],
    'shipkit-product-goals': [
        ('why.json', '/shipkit-why-project'),
        ('product-definition.json', '/shipkit-product-definition'),
    ],
    'shipkit-product-discovery': [
        ('why.json', '/shipkit-why-project'),
    ],
    'shipkit-spec-roadmap': [
        ('why.json', '/shipkit-why-project'),
        ('product-definition.json', '/shipkit-product-definition'),
    ],
    'shipkit-review-shipping': [
        ('why.json', '/shipkit-why-project'),
    ],
    'shipkit-preflight': [
        ('why.json', '/shipkit-why-project'),
        ('stack.json', '/shipkit-project-context'),
    ],
    'shipkit-scale-ready': [
        ('why.json', '/shipkit-why-project'),
        ('architecture.json', '/shipkit-project-context'),
    ],
    'shipkit-vision': [
        ('why.json', '/shipkit-why-project'),
    ],
    'shipkit-stage': [
        ('why.json', '/shipkit-why-project'),
    ],
    'shipkit-communications': [
        ('why.json', '/shipkit-why-project'),
    ],
    'shipkit-orch-direction': [
        ('why.json', '/shipkit-why-project'),
    ],
    'shipkit-orch-planning': [
        ('why.json', '/shipkit-why-project'),
    ],
    'shipkit-orch-shipping': [
        ('why.json', '/shipkit-why-project'),
    ],
}


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


def extract_skill_name(file_path: str) -> str | None:
    """Extract skill name from an InstructionsLoaded file path."""
    # Match paths like .claude/skills/shipkit-spec/SKILL.md or install/skills/shipkit-spec/SKILL.md
    parts = Path(file_path).parts
    for i, part in enumerate(parts):
        if part == 'skills' and i + 1 < len(parts):
            candidate = parts[i + 1]
            if candidate.startswith('shipkit-'):
                return candidate
    return None


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(1)

    # Only process skill loads, not CLAUDE.md or rules
    file_path = hook_input.get('file_path', '')
    skill_name = extract_skill_name(file_path)
    if not skill_name:
        sys.exit(1)

    # Check if this skill has prerequisites
    prereqs = SKILL_PREREQUISITES.get(skill_name)
    if not prereqs:
        sys.exit(1)

    cwd = hook_input.get('cwd', os.getcwd())
    project_root = find_project_root(cwd)
    if not project_root:
        sys.exit(1)

    shipkit_dir = project_root / '.shipkit'
    if not shipkit_dir.is_dir():
        # No .shipkit/ at all — the context-check hook handles this
        sys.exit(1)

    # Check which prerequisites are missing
    missing = []
    for filename, skill in prereqs:
        if not (shipkit_dir / filename).exists():
            missing.append(f"  - .shipkit/{filename} (run {skill})")

    if not missing:
        sys.exit(1)  # All good

    msg = f"[Shipkit] /{skill_name} prerequisites missing:\n" + "\n".join(missing)
    output = {
        "hookSpecificOutput": {
            "hookEventName": "InstructionsLoaded",
            "additionalContext": msg
        }
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == '__main__':
    main()
