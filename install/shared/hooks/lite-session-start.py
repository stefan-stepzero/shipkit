#!/usr/bin/env python3
"""
Shipkit Lite - Session Start Hook

Loads context at session start with smart freshness detection.
Provides actionable summary of where the project is and what to do next.
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta


def get_file_age_days(file_path: Path) -> float:
    """Get file age in days."""
    if not file_path.exists():
        return -1
    mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
    return (datetime.now() - mtime).total_seconds() / 86400


def get_file_mtime(file_path: Path) -> datetime:
    """Get file modification time."""
    if not file_path.exists():
        return datetime.min
    return datetime.fromtimestamp(os.path.getmtime(file_path))


def format_age(days: float) -> str:
    """Format age as human-readable string."""
    if days < 0:
        return "missing"
    if days < 1/24:  # Less than 1 hour
        minutes = int(days * 24 * 60)
        return f"{minutes}m ago"
    if days < 1:
        hours = int(days * 24)
        return f"{hours}h ago"
    if days < 7:
        return f"{int(days)}d ago"
    return f"{int(days)}d ago ⚠️"


def check_stack_freshness(project_root: Path) -> tuple[bool, str]:
    """Check if stack.md is fresher than package.json."""
    stack_file = project_root / '.shipkit-lite' / 'stack.md'
    package_json = project_root / 'package.json'
    pyproject = project_root / 'pyproject.toml'

    if not stack_file.exists():
        return False, "missing"

    stack_mtime = get_file_mtime(stack_file)

    # Check against package.json or pyproject.toml
    for dep_file in [package_json, pyproject]:
        if dep_file.exists():
            dep_mtime = get_file_mtime(dep_file)
            if stack_mtime < dep_mtime:
                return False, "stale (dependencies changed)"

    age = get_file_age_days(stack_file)
    if age > 14:
        return False, f"stale ({int(age)}d old)"

    return True, format_age(age)


def check_implementations_freshness(project_root: Path) -> tuple[bool, str, int, int]:
    """Check implementations directory for stale docs.

    Returns: (is_fresh, status_message, total_docs, stale_count)
    """
    impl_dir = project_root / '.shipkit-lite' / 'implementations'

    if not impl_dir.exists():
        return True, "not yet created", 0, 0

    # Collect all component and route docs
    component_docs = list((impl_dir / 'components').glob('*.md')) if (impl_dir / 'components').exists() else []
    route_docs = list((impl_dir / 'routes').glob('*.md')) if (impl_dir / 'routes').exists() else []

    # Skip index.md
    component_docs = [d for d in component_docs if d.name != 'index.md']
    route_docs = [d for d in route_docs if d.name != 'index.md']

    total_docs = len(component_docs) + len(route_docs)
    if total_docs == 0:
        return True, "no docs yet", 0, 0

    stale_count = 0

    # Check each doc for staleness by reading Source: header
    for doc in component_docs + route_docs:
        try:
            content = doc.read_text(encoding='utf-8')
            # Extract source path from **Source**: `path` line
            for line in content.split('\n')[:15]:  # Check first 15 lines
                if line.startswith('**Source**:'):
                    source_path = line.split('`')[1] if '`' in line else None
                    if source_path:
                        source_file = project_root / source_path
                        if source_file.exists():
                            doc_mtime = get_file_mtime(doc)
                            src_mtime = get_file_mtime(source_file)
                            if src_mtime > doc_mtime:
                                stale_count += 1
                    break
        except Exception:
            pass  # Skip files we can't parse

    if stale_count > 0:
        return False, f"{stale_count} stale doc(s)", total_docs, stale_count

    return True, f"{total_docs} docs fresh", total_docs, stale_count


def get_last_progress_entry(project_root: Path) -> tuple[str, str]:
    """Get last progress entry summary and timestamp."""
    progress_file = project_root / '.shipkit-lite' / 'progress.md'

    if not progress_file.exists():
        return "", "No sessions logged"

    content = progress_file.read_text(encoding='utf-8')

    # Find last session header (## Session: or ## YYYY-MM-DD)
    lines = content.split('\n')
    last_session_start = -1
    last_session_header = ""

    for i, line in enumerate(lines):
        if line.startswith('## Session:') or line.startswith('## 20'):
            last_session_start = i
            last_session_header = line

    if last_session_start == -1:
        age = get_file_age_days(progress_file)
        return "", f"Last updated {format_age(age)}"

    # Extract summary (next few non-empty lines after header)
    summary_lines = []
    for line in lines[last_session_start+1:last_session_start+6]:
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('---'):
            # Clean up markdown
            line = line.lstrip('- *')
            if len(line) > 60:
                line = line[:57] + "..."
            summary_lines.append(line)
            if len(summary_lines) >= 2:
                break

    summary = "; ".join(summary_lines) if summary_lines else "See progress.md"
    age = get_file_age_days(progress_file)

    return summary, format_age(age)


def count_active_items(project_root: Path) -> dict:
    """Count active specs, plans, and user tasks."""
    counts = {
        'specs': 0,
        'plans': 0,
        'user_tasks': 0,
        'oldest_spec_days': 0,
        'oldest_plan_days': 0,
    }

    # Count active specs
    specs_dir = project_root / '.shipkit-lite' / 'specs' / 'active'
    if specs_dir.exists():
        specs = list(specs_dir.glob('*.md'))
        counts['specs'] = len(specs)
        if specs:
            oldest = max(get_file_age_days(s) for s in specs)
            counts['oldest_spec_days'] = oldest

    # Count active plans
    plans_dir = project_root / '.shipkit-lite' / 'plans' / 'active'
    if plans_dir.exists():
        plans = list(plans_dir.glob('*.md'))
        counts['plans'] = len(plans)
        if plans:
            oldest = max(get_file_age_days(p) for p in plans)
            counts['oldest_plan_days'] = oldest

    # Count user tasks
    tasks_file = project_root / '.shipkit-lite' / 'user-tasks' / 'active.md'
    if tasks_file.exists():
        content = tasks_file.read_text(encoding='utf-8')
        # Count uncompleted tasks (lines with [ ])
        counts['user_tasks'] = content.count('[ ]')

    return counts


def get_smart_recommendation(project_root: Path, counts: dict, has_stack: bool) -> str:
    """Generate smart recommendation based on project state."""

    # Priority 1: No stack context yet
    if not has_stack:
        return "/lite-project-context → Scan your codebase first"

    # Priority 2: Pending user tasks (blocking)
    if counts['user_tasks'] > 0:
        return f"/lite-user-instructions → {counts['user_tasks']} pending manual task(s)"

    # Priority 3: Active plan ready for implementation
    if counts['plans'] > 0:
        return "Continue implementing the active plan (no skill needed)"

    # Priority 4: Active spec ready for planning
    if counts['specs'] > 0:
        return "/lite-plan → Create plan for active spec"

    # Priority 5: Check for stale specs
    if counts['oldest_spec_days'] > 7:
        return "/lite-project-status → Check for stale specs"

    # Default: Status check or new work
    return "/lite-project-status → See full project health"


def main():
    # Find paths
    hook_dir = Path(__file__).parent

    # Determine if we're in install directory or deployed .claude directory
    if hook_dir.name == 'hooks' and hook_dir.parent.name == 'shared':
        # We're in install/shared/hooks/ (before installation)
        skills_dir = hook_dir.parent.parent / 'skills'
        project_root = None
    else:
        # We're in .claude/hooks/ (after installation)
        claude_dir = hook_dir.parent
        skills_dir = claude_dir / 'skills'
        project_root = claude_dir.parent

    # Load lite-shipkit-master skill
    master_skill = skills_dir / 'lite-shipkit-master' / 'SKILL.md'

    if not master_skill.exists():
        print("⚠️  Shipkit Lite not properly installed")
        print("   Run the installer again.")
        return 0

    # Output the master skill (routing tables)
    print(master_skill.read_text(encoding='utf-8'))
    print()
    print("---")
    print()

    # If no project root, we're done
    if project_root is None:
        return 0

    shipkit_dir = project_root / '.shipkit-lite'

    # ═══════════════════════════════════════════════════════════════
    # SESSION START SUMMARY
    # ═══════════════════════════════════════════════════════════════

    print("# 🚀 Session Start")
    print()

    # Check if .shipkit-lite exists at all
    if not shipkit_dir.exists():
        print("📂 No `.shipkit-lite/` folder found - this is a fresh project.")
        print()
        print("**Start with:** `/lite-project-context` to scan your codebase")
        print()
        return 0

    # ─────────────────────────────────────────────────────────────────
    # Quick Status
    # ─────────────────────────────────────────────────────────────────

    counts = count_active_items(project_root)
    stack_fresh, stack_status = check_stack_freshness(project_root)
    impl_fresh, impl_status, impl_total, impl_stale = check_implementations_freshness(project_root)
    last_progress, progress_age = get_last_progress_entry(project_root)

    print("## 📊 Quick Status")
    print()
    print(f"| Artifact | Status |")
    print(f"|----------|--------|")
    print(f"| Stack context | {stack_status} |")
    print(f"| Last session | {progress_age} |")
    print(f"| Active specs | {counts['specs']} |")
    print(f"| Active plans | {counts['plans']} |")
    if impl_total > 0:
        print(f"| Implementation docs | {impl_status} |")
    if counts['user_tasks'] > 0:
        print(f"| ⚠️ Pending user tasks | {counts['user_tasks']} |")
    print()

    # Show last progress if available
    if last_progress:
        print(f"**Last work:** {last_progress}")
        print()

    # Freshness warnings
    warnings = []
    if not stack_fresh and stack_status != "missing":
        warnings.append(f"• Stack context is {stack_status} → run `/lite-project-context`")
    if not impl_fresh and impl_stale > 0:
        warnings.append(f"• {impl_stale} implementation doc(s) stale → run `/lite-component-knowledge` or `/lite-route-knowledge`")
    if counts['oldest_spec_days'] > 7:
        warnings.append(f"• Spec sitting {int(counts['oldest_spec_days'])}d without plan → review or archive")
    if counts['oldest_plan_days'] > 3:
        warnings.append(f"• Plan sitting {int(counts['oldest_plan_days'])}d without implementation → continue or archive")

    if warnings:
        print("## ⚠️ Freshness Warnings")
        print()
        for w in warnings:
            print(w)
        print()

    # ─────────────────────────────────────────────────────────────────
    # Smart Recommendation
    # ─────────────────────────────────────────────────────────────────

    has_stack = (project_root / '.shipkit-lite' / 'stack.md').exists()
    recommendation = get_smart_recommendation(project_root, counts, has_stack)

    print("## 💡 Recommended Next")
    print()
    print(f"**{recommendation}**")
    print()
    print("Or run `/lite-project-status` for full health check.")
    print()

    # ─────────────────────────────────────────────────────────────────
    # Load Core Context (only fresh files)
    # ─────────────────────────────────────────────────────────────────

    print("---")
    print()

    # Load why.md (vision - usually stable)
    why_file = shipkit_dir / 'why.md'
    if why_file.exists():
        print("# Project Vision")
        print()
        print(why_file.read_text(encoding='utf-8'))
        print()
        print("---")
        print()

    # Load stack.md (only if fresh)
    stack_file = shipkit_dir / 'stack.md'
    if stack_file.exists():
        if stack_fresh:
            print("# Tech Stack (current)")
            print()
            print(stack_file.read_text(encoding='utf-8'))
        else:
            print(f"# Tech Stack ({stack_status})")
            print()
            print("*Stack context may be outdated. Run `/lite-project-context` to refresh.*")
            print()
            # Still show it but with warning
            content = stack_file.read_text(encoding='utf-8')
            # Show truncated version if stale
            lines = content.split('\n')[:30]
            print('\n'.join(lines))
            if len(content.split('\n')) > 30:
                print("\n... (truncated, run /lite-project-context to refresh)")
        print()
        print("---")
        print()

    # Load architecture.md (decisions - usually stable)
    arch_file = shipkit_dir / 'architecture.md'
    if arch_file.exists():
        age = get_file_age_days(arch_file)
        if age > 14:
            print(f"# Architectural Decisions ({format_age(age)})")
        else:
            print("# Architectural Decisions")
        print()
        print(arch_file.read_text(encoding='utf-8'))
        print()
        print("---")
        print()

    return 0


if __name__ == '__main__':
    sys.exit(main())
