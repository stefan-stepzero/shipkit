#!/usr/bin/env python3
"""
Shipkit Lite - Suggest Next Skill Hook

Suggests next skill after Claude stops responding.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta


def find_recently_modified_files(directory, minutes=1):
    """Find files modified within the last N minutes."""
    if not directory.exists():
        return []

    cutoff_time = datetime.now() - timedelta(minutes=minutes)
    recent_files = []

    for file_path in directory.rglob('*'):
        if file_path.is_file():
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            if mtime > cutoff_time:
                recent_files.append(file_path)

    return recent_files


def detect_last_skill():
    """Detect which Lite skill just completed."""
    project_root = Path.cwd()
    shipkit_lite = project_root / '.shipkit-lite'

    if not shipkit_lite.exists():
        return None

    # Check specs/active/ (lite-spec creates files here)
    specs_active = shipkit_lite / 'specs' / 'active'
    if specs_active.exists() and find_recently_modified_files(specs_active):
        return 'lite-spec'

    # Check plans/ (lite-plan creates files here)
    plans = shipkit_lite / 'plans'
    if plans.exists() and find_recently_modified_files(plans):
        return 'lite-plan'

    # Check implementations.md (lite-implement appends here)
    impl_file = shipkit_lite / 'implementations.md'
    if impl_file.exists():
        mtime = datetime.fromtimestamp(impl_file.stat().st_mtime)
        if mtime > datetime.now() - timedelta(minutes=1):
            return 'lite-implement'

    # Check architecture.md (lite-architecture-memory appends here)
    arch_file = shipkit_lite / 'architecture.md'
    if arch_file.exists():
        mtime = datetime.fromtimestamp(arch_file.stat().st_mtime)
        if mtime > datetime.now() - timedelta(minutes=1):
            return 'lite-architecture-memory'

    # Check types.md (lite-data-consistency updates here)
    types_file = shipkit_lite / 'types.md'
    if types_file.exists():
        mtime = datetime.fromtimestamp(types_file.stat().st_mtime)
        if mtime > datetime.now() - timedelta(minutes=1):
            return 'lite-data-consistency'

    # Check stack.md (lite-project-context updates here)
    stack_file = shipkit_lite / 'stack.md'
    if stack_file.exists():
        mtime = datetime.fromtimestamp(stack_file.stat().st_mtime)
        if mtime > datetime.now() - timedelta(minutes=1):
            return 'lite-project-context'

    return None


def suggest_next_skill(last_skill):
    """Return suggestion for Lite skills."""
    suggestions = {
        'lite-spec': """
✅ Specification created

👉 Next: /lite-plan - Create implementation plan
   Or: /lite-architecture-memory - Log architectural decisions first
""",
        'lite-plan': """
✅ Implementation plan ready

👉 Next: /lite-implement - Begin TDD implementation
""",
        'lite-implement': """
✅ Implementation complete

👉 Next: /lite-component-knowledge - Document this component
   Or: /lite-quality-confidence - Verify quality before shipping
""",
        'lite-architecture-memory': """
✅ Architectural decision logged

👉 Next: /lite-plan - Create implementation plan
   Or: /lite-implement - Start implementation
""",
        'lite-data-consistency': """
✅ Types updated

👉 Next: /lite-implement - Use these types in implementation
""",
        'lite-ux-coherence': """
✅ UX guidance provided

👉 Next: /lite-implement - Apply this pattern
   Or: /lite-architecture-memory - Log this as a pattern decision
""",
        'lite-quality-confidence': """
✅ Quality check complete

👉 Next: Check gap report and address any issues
""",
        'lite-project-context': """
✅ Project context refreshed

👉 Next: /lite-project-status - See project health
   Or: /lite-spec - Create your first feature spec
""",
        'lite-project-status': """
✅ Status check complete

👉 Next: Follow the suggestions above based on detected gaps
""",
    }
    return suggestions.get(last_skill, '')


def main():
    last_skill = detect_last_skill()
    if last_skill:
        suggestion = suggest_next_skill(last_skill)
        if suggestion:
            print(suggestion)
        return 0

    # No suggestion needed
    return 0


if __name__ == '__main__':
    sys.exit(main())
