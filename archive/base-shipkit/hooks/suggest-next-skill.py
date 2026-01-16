#!/usr/bin/env python3
"""
Shipkit - Suggest Next Skill Hook

Instructs Claude to invoke lite-whats-next after skill completion.
Delegates all intelligence to lite-whats-next skill.
"""

import sys
from pathlib import Path


def main():
    """Instruct Claude to invoke lite-whats-next for intelligent workflow guidance."""

    # Check if this is a Lite installation
    project_root = Path.cwd()
    shipkit_lite = project_root / '.shipkit-lite'

    if shipkit_lite.exists():
        # Directive to Claude (not suggestion to user)
        print()
        print("─" * 60)
        print("🤖 CLAUDE: Invoke /lite-whats-next now to provide workflow guidance")
        print("─" * 60)
        print()
    else:
        # Full Shipkit or no Shipkit - no suggestion
        pass

    return 0


if __name__ == '__main__':
    sys.exit(main())
