#!/usr/bin/env python3
"""
lite-pre-ship-check: Check if UX Audit Needed

Analyzes interactive component count and determines if UX audit
is needed before shipping.

Usage:
    python check-ux-audit-needed.py [--threshold 3]

Returns:
    0: Success
    1: Error
"""

import sys
from pathlib import Path
from datetime import datetime
import argparse
import re

# Interactive component patterns
INTERACTIVE_PATTERNS = {
    'forms': [r'<form', r'onSubmit', r'handleSubmit', r'FormData'],
    'async_buttons': [r'onClick.*async', r'loading', r'isLoading', r'disabled'],
    'data_widgets': [r'useQuery', r'useMutation', r'fetch\(', r'axios'],
    'file_uploads': [r'type="file"', r'upload', r'FileReader', r'FormData.*append'],
    'modals': [r'Modal', r'Dialog', r'Popover', r'sheet'],
}

DEFAULT_THRESHOLD = 3


def find_components():
    """Find all component files"""
    component_paths = [
        'src/components/**/*.tsx',
        'src/components/**/*.jsx',
        'app/components/**/*.tsx',
        'components/**/*.tsx',
    ]

    components = []
    for pattern in component_paths:
        for file_path in Path('.').glob(pattern):
            if file_path.is_file():
                components.append(file_path)

    return components


def is_interactive(file_path):
    """Check if component is interactive (needs UX audit)"""
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception:
        return False, []

    interactive_types = []
    for interaction_type, patterns in INTERACTIVE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, content):
                if interaction_type not in interactive_types:
                    interactive_types.append(interaction_type)
                break

    return len(interactive_types) > 0, interactive_types


def determine_audit_items(interactive_types):
    """Determine what UX aspects to audit based on component type"""
    audit_items = set()

    if 'forms' in interactive_types:
        audit_items.update(['Validation feedback', 'Error messages', 'Success feedback'])

    if 'async_buttons' in interactive_types:
        audit_items.update(['Loading state', 'Disabled state', 'Success feedback'])

    if 'data_widgets' in interactive_types:
        audit_items.update(['Loading skeleton', 'Error handling', 'Empty state'])

    if 'file_uploads' in interactive_types:
        audit_items.update(['Upload progress', 'Error messages', 'File size limits'])

    if 'modals' in interactive_types:
        audit_items.update(['Escape to close', 'Focus trap', 'ARIA labels'])

    # Always check accessibility
    audit_items.add('Keyboard navigation')
    audit_items.add('Screen reader support')

    return sorted(audit_items)


def create_queue(interactive_components, threshold):
    """Create queue file for UX audit"""
    if len(interactive_components) < threshold:
        print(f"✓ Only {len(interactive_components)} interactive components (threshold: {threshold})")
        print("  UX audit not needed yet")
        return False

    queue_dir = Path('.shipkit-lite/.queues')
    queue_dir.mkdir(parents=True, exist_ok=True)
    queue_path = queue_dir / 'ux-audit-needed.md'

    # Check if queue already exists
    if queue_path.exists():
        print(f"⚠️  UX audit queue already exists")
        print(f"   Run /lite-ux-audit to complete audit")
        return False

    content = f"""# UX Audit Needed

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Reason:** {len(interactive_components)} interactive components detected, pre-ship check

## Components To Audit

"""

    for file_path, types in interactive_components:
        component_name = file_path.stem
        type_desc = ', '.join(types)
        audit_items = determine_audit_items(types)
        audit_items_str = ', '.join(audit_items)

        content += f"- [ ] {component_name}\n"
        content += f"  - Location: {file_path}\n"
        content += f"  - Type: {type_desc}\n"
        content += f"  - Audit for: {audit_items_str}\n\n"

    content += """## Completed

<!-- Items move here after /lite-ux-audit checks components -->
"""

    queue_path.write_text(content, encoding='utf-8')
    print(f"✓ Created UX audit queue with {len(interactive_components)} components")
    print(f"\n⚠️  IMPORTANT: Run /lite-ux-audit before shipping")
    print(f"   UX issues can cause bad user experience if not caught pre-ship")
    return True


def main():
    parser = argparse.ArgumentParser(description='Check if UX audit needed')
    parser.add_argument('--threshold', type=int, default=DEFAULT_THRESHOLD,
                        help=f'Interactive component threshold (default: {DEFAULT_THRESHOLD})')
    args = parser.parse_args()

    print(f"Checking for interactive components (threshold: {args.threshold})...")

    # Find all components
    components = find_components()
    if not components:
        print("✓ No components found")
        return 0

    print(f"Found {len(components)} total components")

    # Check which are interactive
    interactive_components = []
    for component_path in components:
        is_inter, types = is_interactive(component_path)
        if is_inter:
            interactive_components.append((component_path, types))

    if not interactive_components:
        print("✓ No interactive components found")
        return 0

    print(f"\nFound {len(interactive_components)} interactive components:")
    for file_path, types in interactive_components:
        print(f"  - {file_path.stem} ({', '.join(types)})")

    # Create queue if threshold met
    create_queue(interactive_components, args.threshold)

    return 0


if __name__ == '__main__':
    sys.exit(main())
