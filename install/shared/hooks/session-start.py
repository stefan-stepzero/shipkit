#!/usr/bin/env python3
"""
Shipkit Session Start Hook

Loads the master skill at session start (works for both full Shipkit and Lite).
Output goes to Claude Code as context.
"""

import sys
from pathlib import Path


def main():
    # Find paths (hook is in .claude/hooks/ after installation)
    hook_dir = Path(__file__).parent

    # Determine if we're in install directory or deployed .claude directory
    if hook_dir.name == 'hooks' and hook_dir.parent.name == 'shared':
        # We're in install/shared/hooks/ (before installation)
        skills_dir = hook_dir.parent.parent / 'skills'
    else:
        # We're in .claude/hooks/ (after installation)
        claude_dir = hook_dir.parent
        skills_dir = claude_dir / 'skills'
        project_root = claude_dir.parent

    # Try to find master skill (Lite first, then full Shipkit)
    master_skill = skills_dir / 'lite-shipkit-master' / 'SKILL.md'
    is_lite = True

    if not master_skill.exists():
        # Try full Shipkit
        master_skill = skills_dir / 'shipkit-master' / 'SKILL.md'
        is_lite = False

    if not master_skill.exists():
        print("⚠️  Shipkit Master Skill not found")
        print()
        print("Expected location: .claude/skills/shipkit-master/SKILL.md")
        print("             or: .claude/skills/lite-shipkit-master/SKILL.md")
        print()
        print("Shipkit may not be properly installed. Run the installer again.")
        return 0

    # Output the master skill
    print(master_skill.read_text(encoding='utf-8'))
    print()
    print("---")
    print()

    # Load context files based on version
    if 'project_root' in locals():
        if is_lite:
            # Shipkit Lite: Load .shipkit-lite/ files
            stack_file = project_root / '.shipkit-lite' / 'stack.md'
            if stack_file.exists():
                print("# Current Stack (cached)")
                print()
                print(stack_file.read_text(encoding='utf-8'))
                print()
                print("---")
                print()

            arch_file = project_root / '.shipkit-lite' / 'architecture.md'
            if arch_file.exists():
                print("# Architectural Decisions (cached)")
                print()
                print(arch_file.read_text(encoding='utf-8'))
                print()
                print("---")
                print()

            # Session start message for Lite
            print("## Session Start")
            print()
            print("📍 **Need to orient?** Run `/lite-project-status` to see project health.")
            print()
        else:
            # Full Shipkit: Just show session start message
            print("## Session Start")
            print()
            print("📍 **Need to orient?** Run `/shipkit-status` to see where you are and what's next.")
            print()

    return 0


if __name__ == '__main__':
    sys.exit(main())
