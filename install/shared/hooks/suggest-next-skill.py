#!/usr/bin/env python3
"""
Shipkit - Suggest Next Skill Hook

Prompts user to check what's next after Claude stops.
Delegates all intelligence to lite-whats-next skill.
"""

import sys
from pathlib import Path


def main():
    """Suggest running lite-whats-next for intelligent workflow guidance."""

    # Check if this is a Lite installation
    project_root = Path.cwd()
    shipkit_lite = project_root / '.shipkit-lite'

    if shipkit_lite.exists():
        # Lite installation - suggest lite-whats-next
        print()
        print("---")
        print()
        print("💡 **What's next?** Run `/lite-whats-next` for smart workflow guidance")
        print()
    else:
        # Full Shipkit or no Shipkit - no suggestion
        pass

    return 0


if __name__ == '__main__':
    sys.exit(main())
