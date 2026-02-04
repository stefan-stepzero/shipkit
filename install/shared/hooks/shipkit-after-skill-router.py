#!/usr/bin/env python3
"""
Shipkit - After-Skill Router Hook

Reads .last-skill breadcrumb and triggers appropriate detection mode.
This creates the causality chain between creation skills and follow-up skills.

Flow:
1. Parent skill writes skill name to .shipkit/.last-skill
2. This hook reads that file after any skill completes
3. Routes to shipkit-detect with appropriate mode
4. shipkit-detect scans artifacts and creates queue for follow-up skill
"""

import subprocess
import sys
from pathlib import Path

# Map parent skills to detection modes
# Only skills that still exist can write breadcrumbs
SKILL_TO_MODE = {
    "shipkit-spec": "services",           # After spec → detect external services
    "shipkit-plan": "contracts",          # After plan → detect data structures
}


def main():
    # Find project root (hook is in .claude/hooks/)
    hook_dir = Path(__file__).parent

    # Determine if we're in install directory or deployed .claude directory
    if hook_dir.name == 'hooks' and hook_dir.parent.name == 'shared':
        # We're in install/shared/hooks/ (before installation)
        # Can't run detection without a project context
        return 0

    # We're in .claude/hooks/ (after installation)
    claude_dir = hook_dir.parent
    project_root = claude_dir.parent
    shipkit_dir = project_root / '.shipkit'

    # Check for breadcrumb file
    last_skill_file = shipkit_dir / '.last-skill'
    if not last_skill_file.exists():
        return 0

    # Read and clear the breadcrumb
    try:
        last_skill = last_skill_file.read_text().strip()
        last_skill_file.unlink()  # Clear after reading
    except Exception:
        return 0

    # Check if this skill triggers detection
    mode = SKILL_TO_MODE.get(last_skill)
    if not mode:
        return 0

    # Find the detect script
    detect_script = claude_dir / 'skills' / 'shipkit-detect' / 'scripts' / 'detect.py'
    if not detect_script.exists():
        print(f"⚠️  shipkit-detect script not found at {detect_script}")
        return 0

    # Run detection
    print(f"🔍 Auto-detecting after {last_skill}...")
    print()

    try:
        result = subprocess.run(
            [sys.executable, str(detect_script), f"--mode={mode}"],
            cwd=str(project_root),
            capture_output=True,
            text=True,
        )

        # Show output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)

        return result.returncode

    except Exception as e:
        print(f"⚠️  Detection failed: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())