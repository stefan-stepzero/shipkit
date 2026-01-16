#!/usr/bin/env python3
"""
Section-based skill management for Shipkit Lite.

Skills use section markers to identify replaceable blocks:
    <!-- SECTION:after-completion -->
    ... content ...
    <!-- /SECTION:after-completion -->

Usage:
    python skill-sections.py list                    # List all sections in all skills
    python skill-sections.py show <skill> <section>  # Show a section's content
    python skill-sections.py update <section>        # Update section in all skills from template
    python skill-sections.py add <skill> <section>   # Add a section to a skill
    python skill-sections.py migrate                 # Add section markers to existing skills
"""

import argparse
import re
from pathlib import Path

SKILLS_DIR = Path(__file__).parent.parent / 'install' / 'skills'
TEMPLATES_DIR = SKILLS_DIR / '_templates'

# Section marker pattern
SECTION_PATTERN = r'<!-- SECTION:(\w+[-\w]*) -->\n(.*?)<!-- /SECTION:\1 -->'

# Known sections and their templates
SECTIONS = {
    'after-completion': 'after-completion.md',
    'success-criteria': 'success-criteria.md',
    'context-reads': 'context-reads.md',
    'context-writes': 'context-writes.md',
}

# Patterns to identify existing sections (for migration)
LEGACY_PATTERNS = {
    'after-completion': [
        r'## Success Criteria\n\n.*?invoke `/lite-whats-next`.*?(?=\n## |\n---|\Z)',
        r'\*\*REQUIRED FINAL STEP:\*\*.*?meta-rules\.',
        r'\*\*Now invoke `/lite-whats-next`\*\*.*?guidance\.',
    ],
    'success-criteria': [
        r'## Success Criteria\n\n(?:.*?(?=\n## |\n---|\Z))',
    ],
}


def load_template(section_name: str) -> str:
    """Load a section template."""
    template_file = SECTIONS.get(section_name)
    if not template_file:
        raise ValueError(f"Unknown section: {section_name}")

    template_path = TEMPLATES_DIR / template_file
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    return template_path.read_text(encoding='utf-8').strip()


def wrap_section(section_name: str, content: str) -> str:
    """Wrap content in section markers."""
    return f"<!-- SECTION:{section_name} -->\n{content}\n<!-- /SECTION:{section_name} -->"


def find_sections(content: str) -> dict:
    """Find all sections in content."""
    sections = {}
    for match in re.finditer(SECTION_PATTERN, content, re.DOTALL):
        sections[match.group(1)] = {
            'content': match.group(2).strip(),
            'full_match': match.group(0),
            'start': match.start(),
            'end': match.end(),
        }
    return sections


def find_skill_files():
    """Find all SKILL.md files (excluding templates)."""
    return [f for f in SKILLS_DIR.glob('*/SKILL.md') if '_templates' not in str(f)]


def cmd_list(args):
    """List all sections in all skills."""
    skill_files = find_skill_files()

    print(f"Scanning {len(skill_files)} skills for sections...\n")

    for skill_file in sorted(skill_files):
        skill_name = skill_file.parent.name
        content = skill_file.read_text(encoding='utf-8')
        sections = find_sections(content)

        if sections:
            print(f"{skill_name}:")
            for section_name in sections:
                print(f"  - {section_name}")
        else:
            print(f"{skill_name}: (no sections)")

    return 0


def cmd_show(args):
    """Show a section's content."""
    skill_path = SKILLS_DIR / args.skill / 'SKILL.md'
    if not skill_path.exists():
        print(f"Skill not found: {args.skill}")
        return 1

    content = skill_path.read_text(encoding='utf-8')
    sections = find_sections(content)

    if args.section not in sections:
        print(f"Section '{args.section}' not found in {args.skill}")
        print(f"Available sections: {list(sections.keys()) or 'none'}")
        return 1

    print(sections[args.section]['content'])
    return 0


def cmd_update(args):
    """Update a section in all skills from template."""
    template_content = load_template(args.section)
    wrapped = wrap_section(args.section, template_content)

    skill_files = find_skill_files()
    updated = 0

    for skill_file in skill_files:
        skill_name = skill_file.parent.name
        content = skill_file.read_text(encoding='utf-8')
        sections = find_sections(content)

        if args.section in sections:
            # Replace existing section
            old_section = sections[args.section]['full_match']
            new_content = content.replace(old_section, wrapped)

            if new_content != content:
                if not args.dry_run:
                    skill_file.write_text(new_content, encoding='utf-8')
                print(f"{'[WOULD UPDATE]' if args.dry_run else '[UPDATED]'} {skill_name}")
                updated += 1

    print(f"\n{'Would update' if args.dry_run else 'Updated'}: {updated} skills")
    return 0


def cmd_add(args):
    """Add a section to a skill."""
    skill_path = SKILLS_DIR / args.skill / 'SKILL.md'
    if not skill_path.exists():
        print(f"Skill not found: {args.skill}")
        return 1

    content = skill_path.read_text(encoding='utf-8')
    sections = find_sections(content)

    if args.section in sections:
        print(f"Section '{args.section}' already exists in {args.skill}")
        return 1

    template_content = load_template(args.section)
    wrapped = wrap_section(args.section, template_content)

    # Add before the last --- or at end
    if content.rstrip().endswith('---'):
        # Insert before final ---
        content = content.rstrip()[:-3] + '\n' + wrapped + '\n\n---\n'
    else:
        content = content.rstrip() + '\n\n' + wrapped + '\n'

    if not args.dry_run:
        skill_path.write_text(content, encoding='utf-8')

    print(f"{'[WOULD ADD]' if args.dry_run else '[ADDED]'} {args.section} to {args.skill}")
    return 0


def cmd_migrate(args):
    """Add section markers to existing skills by identifying legacy patterns."""
    skill_files = find_skill_files()

    print("Migration: Adding section markers to skills\n")
    print("This will:")
    print("1. Remove old lite-whats-next invocation patterns")
    print("2. Add standardized <!-- SECTION:after-completion --> block")
    print("3. Wrap existing Success Criteria in <!-- SECTION:success-criteria -->")
    print()

    migrated = 0

    for skill_file in sorted(skill_files):
        skill_name = skill_file.parent.name
        content = skill_file.read_text(encoding='utf-8')
        original = content
        changes = []

        # Skip if already has sections
        if '<!-- SECTION:' in content:
            print(f"[SKIP] {skill_name} (already has sections)")
            continue

        # Remove legacy whats-next patterns
        for pattern in LEGACY_PATTERNS.get('after-completion', []):
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, '', content, flags=re.DOTALL)
                changes.append("Removed lite-whats-next pattern")

        # Find Success Criteria section and wrap it
        success_match = re.search(
            r'(## Success Criteria\n\n)(.*?)(?=\n## |\n---|\Z)',
            content,
            re.DOTALL
        )
        if success_match:
            old_section = success_match.group(0)
            # Don't wrap if it contains whats-next (already removed above)
            if 'whats-next' not in old_section.lower():
                header = success_match.group(1)
                body = success_match.group(2).strip()
                new_section = f"<!-- SECTION:success-criteria -->\n## Success Criteria\n\n{body}\n<!-- /SECTION:success-criteria -->"
                content = content.replace(old_section, new_section)
                changes.append("Wrapped Success Criteria in section markers")

        # Add after-completion section if not present
        if '<!-- SECTION:after-completion -->' not in content:
            template = load_template('after-completion')
            wrapped = wrap_section('after-completion', template)

            # Insert before Success Criteria or at end
            if '<!-- SECTION:success-criteria -->' in content:
                content = content.replace(
                    '<!-- SECTION:success-criteria -->',
                    wrapped + '\n\n<!-- SECTION:success-criteria -->'
                )
            else:
                content = content.rstrip() + '\n\n' + wrapped + '\n'
            changes.append("Added after-completion section")

        # Clean up extra blank lines
        content = re.sub(r'\n{3,}', '\n\n', content)

        if content != original:
            if not args.dry_run:
                skill_file.write_text(content, encoding='utf-8')
            print(f"{'[WOULD MIGRATE]' if args.dry_run else '[MIGRATED]'} {skill_name}")
            for change in changes:
                print(f"  - {change}")
            migrated += 1
        else:
            print(f"[OK] {skill_name} (no changes needed)")

    print(f"\n{'Would migrate' if args.dry_run else 'Migrated'}: {migrated} skills")

    if args.dry_run and migrated > 0:
        print("\nRun without --dry-run to apply changes")

    return 0


def main():
    parser = argparse.ArgumentParser(description='Section-based skill management')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # list command
    subparsers.add_parser('list', help='List all sections in all skills')

    # show command
    show_parser = subparsers.add_parser('show', help='Show a section content')
    show_parser.add_argument('skill', help='Skill name')
    show_parser.add_argument('section', help='Section name')

    # update command
    update_parser = subparsers.add_parser('update', help='Update section in all skills')
    update_parser.add_argument('section', help='Section name')

    # add command
    add_parser = subparsers.add_parser('add', help='Add section to a skill')
    add_parser.add_argument('skill', help='Skill name')
    add_parser.add_argument('section', help='Section name')

    # migrate command
    subparsers.add_parser('migrate', help='Migrate existing skills to use sections')

    args = parser.parse_args()

    commands = {
        'list': cmd_list,
        'show': cmd_show,
        'update': cmd_update,
        'add': cmd_add,
        'migrate': cmd_migrate,
    }

    return commands[args.command](args)


if __name__ == '__main__':
    exit(main())
