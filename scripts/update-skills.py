#!/usr/bin/env python3
"""
Batch update Shipkit Lite skills.

Usage:
    python scripts/update-skills.py --dry-run    # Preview changes
    python scripts/update-skills.py --apply      # Apply changes
"""

import argparse
import re
from pathlib import Path

SKILLS_DIR = Path(__file__).parent.parent / 'install' / 'skills'

# Patterns to remove (compiled regex)
PATTERNS_TO_REMOVE = [
    # Single line whats-next invocation
    (r'\*\*Now invoke `/lite-whats-next`\*\*.*?guidance\.?\n*', ''),

    # Checklist item for whats-next
    (r'- \[ \] Invoke `/lite-whats-next`.*?\n', ''),

    # Required final step block (multiline)
    (r'\*\*REQUIRED FINAL STEP:\*\*.*?meta-rules\.\n*', ''),

    # Step headers that just say "invoke whats-next"
    (r'## Step \d+: (?:Suggest Next Steps|Invoke lite-whats-next)\n+\*\*Now invoke.*?\n+---\n*', ''),
]

# Skill references to replace
SKILL_REPLACEMENTS = [
    # /lite-implement -> natural capability note
    (r'`/lite-implement`', '(implement naturally - no skill needed)'),
    (r'/lite-implement', '(implement naturally)'),

    # /lite-quality-confidence -> removed
    (r'`/lite-quality-confidence`', '(quality checks - do naturally)'),
    (r'/lite-quality-confidence', '(quality checks)'),

    # /lite-debug-systematically -> natural capability
    (r'`/lite-debug-systematically`', '(debug naturally - no skill needed)'),
    (r'/lite-debug-systematically', '(debug naturally)'),

    # /lite-document-artifact -> removed
    (r'`/lite-document-artifact`', '(document naturally - no skill needed)'),
    (r'/lite-document-artifact', '(document naturally)'),
]


def find_skill_files():
    """Find all SKILL.md files."""
    return list(SKILLS_DIR.glob('*/SKILL.md'))


def analyze_file(file_path: Path) -> dict:
    """Analyze a file for patterns to change."""
    content = file_path.read_text(encoding='utf-8')
    original = content
    changes = []

    # Apply removal patterns
    for pattern, replacement in PATTERNS_TO_REMOVE:
        matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
        if matches:
            changes.append(f"Remove: {len(matches)} instance(s) of whats-next pattern")
            content = re.sub(pattern, replacement, content, flags=re.DOTALL | re.IGNORECASE)

    # Apply skill replacements
    for pattern, replacement in SKILL_REPLACEMENTS:
        matches = re.findall(pattern, content)
        if matches:
            changes.append(f"Replace: {len(matches)} instance(s) of {pattern[:30]}...")
            content = re.sub(pattern, replacement, content)

    # Clean up multiple blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)

    return {
        'path': file_path,
        'original': original,
        'modified': content,
        'changed': original != content,
        'changes': changes,
    }


def main():
    parser = argparse.ArgumentParser(description='Update Shipkit Lite skills')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without applying')
    parser.add_argument('--apply', action='store_true', help='Apply changes')
    parser.add_argument('--skill', type=str, help='Only process specific skill (e.g., lite-spec)')
    args = parser.parse_args()

    if not args.dry_run and not args.apply:
        print("Usage: python update-skills.py --dry-run OR --apply")
        return 1

    skill_files = find_skill_files()

    if args.skill:
        skill_files = [f for f in skill_files if args.skill in str(f)]

    print(f"Found {len(skill_files)} skill files\n")

    total_changed = 0

    for skill_file in sorted(skill_files):
        result = analyze_file(skill_file)
        skill_name = skill_file.parent.name

        if result['changed']:
            total_changed += 1
            print(f"{'[WOULD CHANGE]' if args.dry_run else '[CHANGED]'} {skill_name}")
            for change in result['changes']:
                print(f"  - {change}")

            if args.apply:
                skill_file.write_text(result['modified'], encoding='utf-8')
            print()
        else:
            print(f"[OK] {skill_name}")

    print(f"\n{'Would change' if args.dry_run else 'Changed'}: {total_changed}/{len(skill_files)} files")

    if args.dry_run and total_changed > 0:
        print("\nRun with --apply to make changes")

    return 0


if __name__ == '__main__':
    exit(main())
