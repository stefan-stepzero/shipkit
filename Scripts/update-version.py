#!/usr/bin/env python3
"""
update-version.py - Update Shipkit version

Usage:
    python scripts/update-version.py 1.2.1
"""

import re
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/update-version.py X.Y.Z")
        sys.exit(1)

    version = sys.argv[1]

    # Validate version format
    if not re.match(r'^\d+\.\d+\.\d+$', version):
        print(f"Error: Invalid version format '{version}'. Use X.Y.Z format.")
        sys.exit(1)

    # Find project root (where this script lives in scripts/)
    script_dir = Path(__file__).parent
    base_dir = script_dir.parent

    # Update VERSION file
    version_file = base_dir / "VERSION"
    version_file.write_text(version + '\n', encoding='utf-8')

    print(f"Updated VERSION to {version}")
    print()
    print("Remember to update CHANGELOG.md")


if __name__ == '__main__':
    main()
