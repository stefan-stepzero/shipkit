#!/usr/bin/env python3
"""
Shipkit Lite - Session Start Hook

Loads lite-shipkit-master at session start and relevant context files.
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

    # Load lite-shipkit-master skill
    master_skill = skills_dir / 'lite-shipkit-master' / 'SKILL.md'

    if not master_skill.exists():
        print("⚠️  Shipkit Lite Master Skill not found")
        print()
        print("Expected location: .claude/skills/lite-shipkit-master/SKILL.md")
        print()
        print("Shipkit Lite may not be properly installed. Run the installer again.")
        return 0

    # Output the master skill
    print(master_skill.read_text(encoding='utf-8'))
    print()
    print("---")
    print()

    # Load Shipkit Lite context files
    if 'project_root' in locals():
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

        # Session start message
        print("## Session Start")
        print()
        print("📍 **Need to orient?** Run `/lite-project-status` to see project health.")
        print()

    return 0


if __name__ == '__main__':
    sys.exit(main())
