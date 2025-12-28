#!/usr/bin/env python3
"""
Shipkit - Suggest Next Skill Hook

Suggests next skill after Claude stops responding.
Works for both full Shipkit and Shipkit Lite.
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


def detect_last_skill_lite():
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


def detect_last_skill_full():
    """Detect which full Shipkit skill just completed."""
    project_root = Path.cwd()
    shipkit = project_root / '.shipkit' / 'skills'

    if not shipkit.exists():
        return None

    # Full Shipkit skill detection (check outputs/ folders)
    skills_to_check = [
        ('prod-strategic-thinking', 'prod-constitution-builder'),
        ('prod-constitution-builder', 'prod-personas'),
        ('prod-personas', 'prod-jobs-to-be-done'),
        ('prod-jobs-to-be-done', 'prod-market-analysis'),
        ('prod-market-analysis', 'prod-brand-guidelines'),
        ('prod-brand-guidelines', 'prod-interaction-design'),
        ('prod-interaction-design', 'prod-user-stories'),
        ('prod-user-stories', 'prod-assumptions-and-risks'),
        ('prod-assumptions-and-risks', 'prod-success-metrics'),
        ('prod-success-metrics', 'dev-constitution'),
        ('dev-constitution', 'dev-specify'),
        ('dev-specify', 'dev-plan'),
        ('dev-plan', 'dev-tasks'),
        ('dev-tasks', 'dev-implement'),
        ('dev-implement', 'dev-finish'),
    ]

    for skill, _ in skills_to_check:
        output_dir = shipkit / skill / 'outputs'
        if output_dir.exists() and find_recently_modified_files(output_dir):
            return skill

    return None


def suggest_next_skill_lite(last_skill):
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


def suggest_next_skill_full(last_skill):
    """Return suggestion for full Shipkit skills."""
    suggestions = {
        'prod-strategic-thinking': """
✅ Strategic thinking complete

👉 Next: /prod-constitution-builder - Define project type and principles
""",
        'prod-constitution-builder': """
✅ Product constitution created

👉 Next: /prod-personas - Identify target users
""",
        'prod-personas': """
✅ Personas defined

👉 Next: /prod-jobs-to-be-done - Map workflows and pain points
""",
        'prod-jobs-to-be-done': """
✅ Jobs to be done mapped

👉 Next: /prod-market-analysis - Analyze competition
""",
        'prod-market-analysis': """
✅ Market analysis complete

👉 Next: /prod-brand-guidelines - Define brand identity
""",
        'prod-brand-guidelines': """
✅ Brand guidelines established

👉 Next: /prod-interaction-design - Design user journeys
""",
        'prod-interaction-design': """
✅ Interaction design complete

👉 Next: /prod-user-stories - Write requirements
""",
        'prod-user-stories': """
✅ User stories written

👉 Next: /prod-assumptions-and-risks OR /dev-constitution
""",
        'prod-assumptions-and-risks': """
✅ Assumptions and risks documented

👉 Next: /prod-success-metrics - Define KPIs
""",
        'prod-success-metrics': """
✅ Product discovery complete!

👉 Next: /dev-constitution - Start development
""",
        'dev-constitution': """
✅ Technical constitution ready

👉 Next: /dev-specify - Create feature spec
""",
        'dev-specify': """
✅ Specification created

👉 Next: /dev-plan - Generate implementation plan
""",
        'dev-plan': """
✅ Implementation plan ready

👉 Next: /dev-tasks - Break into tasks
""",
        'dev-tasks': """
✅ Tasks defined

👉 Next: /dev-implement - Execute with TDD
""",
        'dev-implement': """
✅ Implementation complete

👉 Next: /dev-finish - Merge and validate
""",
    }
    return suggestions.get(last_skill, '')


def main():
    # Try Lite first, then full Shipkit
    last_skill = detect_last_skill_lite()
    if last_skill:
        suggestion = suggest_next_skill_lite(last_skill)
        if suggestion:
            print(suggestion)
        return 0

    last_skill = detect_last_skill_full()
    if last_skill:
        suggestion = suggest_next_skill_full(last_skill)
        if suggestion:
            print(suggestion)
        return 0

    # No suggestion needed
    return 0


if __name__ == '__main__':
    sys.exit(main())
