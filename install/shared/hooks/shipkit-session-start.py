#!/usr/bin/env python3
"""
Shipkit - Session Start Hook

Loads context at session start with smart freshness detection.
Provides actionable summary of where the project is and what to do next.
"""

import sys
import os
import json
import re
import urllib.request
from pathlib import Path
from datetime import datetime, timedelta

GITHUB_VERSION_URL = "https://raw.githubusercontent.com/stefan-stepzero/shipkit/main/VERSION"


def get_installed_version() -> str:
    """Read installed Shipkit version from .shipkit/VERSION."""
    version_file = Path(".shipkit/VERSION")
    if version_file.exists():
        return version_file.read_text(encoding='utf-8').strip()
    return "unknown"


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
    """Check if stack.json is fresher than package.json."""
    stack_file = project_root / '.shipkit' / 'stack.json'
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
    impl_dir = project_root / '.shipkit' / 'implementations'

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
    progress_file = project_root / '.shipkit' / 'progress.json'

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

    summary = "; ".join(summary_lines) if summary_lines else "See progress.json"
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
    specs_dir = project_root / '.shipkit' / 'specs' / 'active'
    if specs_dir.exists():
        specs = list(specs_dir.glob('*.md'))
        counts['specs'] = len(specs)
        if specs:
            oldest = max(get_file_age_days(s) for s in specs)
            counts['oldest_spec_days'] = oldest

    # Count active plans
    plans_dir = project_root / '.shipkit' / 'plans' / 'active'
    if plans_dir.exists():
        plans = list(plans_dir.glob('*.md'))
        counts['plans'] = len(plans)
        if plans:
            oldest = max(get_file_age_days(p) for p in plans)
            counts['oldest_plan_days'] = oldest

    # Count user tasks
    tasks_file = project_root / '.shipkit' / 'user-tasks' / 'active.md'
    if tasks_file.exists():
        content = tasks_file.read_text(encoding='utf-8')
        # Count uncompleted tasks (lines with [ ])
        counts['user_tasks'] = content.count('[ ]')

    return counts


def parse_version(version_str: str) -> tuple:
    """
    Parse version string to comparable tuple.

    Handles: "1.2", "1.2.0", "1.2.3"
    Returns: (1, 2, 0) tuple padded to 3 parts
    Invalid input returns (0, 0, 0)
    """
    try:
        parts = version_str.strip().split('.')
        nums = [int(p) for p in parts[:3]]
        while len(nums) < 3:
            nums.append(0)
        return tuple(nums)
    except (ValueError, AttributeError):
        return (0, 0, 0)


def check_for_updates(project_root: Path) -> str | None:
    """
    Check if newer Shipkit version is available on GitHub.

    Behavior:
    - Checks at most once per day (rate limited via .update-check file mtime)
    - 3 second timeout to avoid blocking session start
    - Fails silently on any error (network, parse, permission)
    - Compares semantic versions (major.minor.patch)

    Returns: Message string if update available, None otherwise.
    """
    check_file = project_root / '.shipkit' / '.update-check'
    installed_version = get_installed_version()

    # Can't check for updates if we don't know current version
    if installed_version == "unknown":
        return None

    # Rate limit: skip network check if checked within last 24 hours
    if check_file.exists():
        age_days = get_file_age_days(check_file)
        if age_days >= 0 and age_days < 1:
            # Already checked recently - but still show cached message if update exists
            try:
                lines = check_file.read_text(encoding='utf-8').strip().split('\n')
                if len(lines) >= 2:
                    cached_remote = lines[1]
                    if parse_version(cached_remote) > parse_version(installed_version):
                        return f"⚡ Shipkit {cached_remote} available (you have {installed_version}). Run `/shipkit-update`"
            except Exception:
                pass
            return None

    # Perform network check
    try:
        request = urllib.request.Request(
            GITHUB_VERSION_URL,
            headers={'User-Agent': 'Shipkit-UpdateCheck/1.0'}
        )
        with urllib.request.urlopen(request, timeout=3) as response:
            remote_version = response.read().decode('utf-8').strip()

        # Validate format (digits and dots only, 2-3 parts)
        if not re.match(r'^\d+\.\d+(\.\d+)?$', remote_version):
            return None

        # Cache result: line 1 = timestamp, line 2 = version
        try:
            check_file.parent.mkdir(parents=True, exist_ok=True)
            check_file.write_text(f"{datetime.now().isoformat()}\n{remote_version}")
        except Exception:
            pass  # Cache write failure is non-fatal

        # Compare versions
        if parse_version(remote_version) > parse_version(installed_version):
            return f"⚡ Shipkit {remote_version} available (you have {installed_version}). Run `/shipkit-update`"

    except Exception:
        # Network timeout, DNS failure, GitHub down, etc. - fail silently
        pass

    return None


def get_smart_recommendation(project_root: Path, counts: dict, has_stack: bool) -> str:
    """Generate smart recommendation based on project state."""

    # Priority 1: No stack context yet
    if not has_stack:
        return "/shipkit-project-context → Scan your codebase first"

    # Priority 2: Pending user tasks (blocking)
    if counts['user_tasks'] > 0:
        return f"/shipkit-user-instructions → {counts['user_tasks']} pending manual task(s)"

    # Priority 3: Active plan ready for implementation
    if counts['plans'] > 0:
        return "Continue implementing the active plan (no skill needed)"

    # Priority 4: Active spec ready for planning
    if counts['specs'] > 0:
        return "/shipkit-plan → Create plan for active spec"

    # Priority 5: Check for stale specs
    if counts['oldest_spec_days'] > 7:
        return "/shipkit-project-status → Check for stale specs"

    # Default: Status check or new work
    return "/shipkit-project-status → See full project health"


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

    # Load shipkit-master skill
    master_skill = skills_dir / 'shipkit-master' / 'SKILL.md'

    if not master_skill.exists():
        print("⚠️  Shipkit not properly installed")
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

    shipkit_dir = project_root / '.shipkit'

    # ═══════════════════════════════════════════════════════════════
    # UPDATE CHECK (once per day, 3s timeout, silent on failure)
    # ═══════════════════════════════════════════════════════════════

    update_msg = check_for_updates(project_root)

    # ═══════════════════════════════════════════════════════════════
    # SESSION START SUMMARY
    # ═══════════════════════════════════════════════════════════════

    print("# 🚀 Session Start")
    print()

    if update_msg:
        print(update_msg)
        print()

    # Check if .shipkit exists at all
    if not shipkit_dir.exists():
        print("📂 No `.shipkit/` folder found - this is a fresh project.")
        print()
        print("**Start with:** `/shipkit-project-context` to scan your codebase")
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
        warnings.append(f"• Stack context is {stack_status} → run `/shipkit-project-context`")
    if not impl_fresh and impl_stale > 0:
        warnings.append(f"• {impl_stale} implementation doc(s) stale → review and update manually")
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

    has_stack = (project_root / '.shipkit' / 'stack.json').exists()
    recommendation = get_smart_recommendation(project_root, counts, has_stack)

    print("## 💡 Recommended Next")
    print()
    print(f"**{recommendation}**")
    print()
    print("Or run `/shipkit-project-status` for full health check.")
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

    # Load stack.json (only if fresh)
    stack_file = shipkit_dir / 'stack.json'
    if stack_file.exists():
        if stack_fresh:
            print("# Tech Stack (current)")
            print()
            print(stack_file.read_text(encoding='utf-8'))
        else:
            print(f"# Tech Stack ({stack_status})")
            print()
            print("*Stack context may be outdated. Run `/shipkit-project-context` to refresh.*")
            print()
            # Still show it but with warning
            content = stack_file.read_text(encoding='utf-8')
            # Show truncated version if stale
            lines = content.split('\n')[:30]
            print('\n'.join(lines))
            if len(content.split('\n')) > 30:
                print("\n... (truncated, run /shipkit-project-context to refresh)")
        print()
        print("---")
        print()

    # Load architecture.json (decisions - usually stable)
    arch_file = shipkit_dir / 'architecture.json'
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

    # ─────────────────────────────────────────────────────────────────
    # Codebase Index Summary (for navigation)
    # ─────────────────────────────────────────────────────────────────

    index_file = shipkit_dir / 'codebase-index.json'
    if not index_file.exists():
        print("📁 **Tip:** Run `/shipkit-codebase-index` to create a project map for faster navigation")
        print()
    else:
        try:
            index_data = json.loads(index_file.read_text(encoding='utf-8'))

            index_generated = datetime.strptime(index_data.get('generated', '2000-01-01'), '%Y-%m-%d')
            index_age = (datetime.now() - index_generated).days

            print("# 📁 Codebase Index")
            print()

            if index_age > 14:
                print(f"⚠️ Index is {index_age} days old. Consider running `/shipkit-codebase-index` to update.")
                print()

            # Concepts - the key navigation info
            concepts = index_data.get('concepts', {})
            if concepts:
                print(f"**Concepts ({len(concepts)}):**")
                for concept, files in concepts.items():
                    first_file = files[0] if files else "?"
                    more = f" (+{len(files)-1} more)" if len(files) > 1 else ""
                    print(f"  • {concept}: `{first_file}`{more}")
                print()

            # Entry points
            entry_points = index_data.get('entryPoints', {})
            if entry_points:
                print("**Entry Points:**")
                for name, path in entry_points.items():
                    print(f"  • {name}: `{path}`")
                print()

            # Skip list
            skip = index_data.get('skip', [])
            if skip:
                print(f"**Skip:** {', '.join(skip)}")
                print()

            print("*Use concepts above for navigation. Read full index for complete file lists.*")
            print()
            print("---")
            print()
        except Exception:
            # If index is malformed, suggest regenerating
            print("📁 Codebase index exists but couldn't be read. Run `/shipkit-codebase-index` to regenerate.")
            print()

    # ─────────────────────────────────────────────────────────────────
    # Skill Usage Summary (if tracking data exists)
    # ─────────────────────────────────────────────────────────────────

    usage_file = shipkit_dir / 'skill-usage.json'
    if usage_file.exists():
        try:
            usage_data = json.loads(usage_file.read_text(encoding='utf-8'))
            skills = usage_data.get('skills', {})

            if skills:
                now = datetime.now()
                stale_skills = []
                nudges = []

                # Build lookup: skill_name -> days since last use
                skill_age = {}
                for skill_name, data in skills.items():
                    last_used_str = data.get('lastUsed', '')
                    if last_used_str:
                        try:
                            last_used = datetime.fromisoformat(last_used_str)
                            days_ago = (now - last_used).days
                            skill_age[skill_name] = days_ago
                            if days_ago >= 14:
                                stale_skills.append((skill_name, days_ago, data.get('count', 0)))
                        except ValueError:
                            pass

                # Contextual nudges: cross-reference project state with usage
                def skill_stale_or_never(name, threshold=7):
                    """True if skill was never used or last used > threshold days ago."""
                    return name not in skills or skill_age.get(name, 999) > threshold

                if counts['specs'] > 0 and skill_stale_or_never('shipkit-plan'):
                    nudges.append("You have active specs → consider `/shipkit-plan`")

                if counts['plans'] > 0 and skill_stale_or_never('shipkit-verify'):
                    nudges.append("Implementation in progress → `/shipkit-verify` to check your work")

                if counts['plans'] > 0 and skill_stale_or_never('shipkit-preflight', 14):
                    nudges.append("Approaching release? → `/shipkit-preflight` for launch checks")

                quality_skills = ['shipkit-verify', 'shipkit-preflight', 'shipkit-ux-audit']
                if not any(s in skills for s in quality_skills) and (counts['specs'] > 0 or counts['plans'] > 0):
                    nudges.append("No quality skills used yet → try `/shipkit-verify` or `/shipkit-ux-audit`")

                # Only show section if there's something to report
                if stale_skills or nudges:
                    print("# 📊 Skill Usage")
                    print()

                    if stale_skills:
                        stale_skills.sort(key=lambda x: x[1], reverse=True)
                        print(f"**Stale skills** (not used in 14+ days):")
                        for skill, days, count in stale_skills[:5]:
                            print(f"  • `/{skill}`: {days}d ago (used {count}x)")
                        print()

                    if nudges:
                        for nudge in nudges[:3]:  # Cap at 3 to keep it lightweight
                            print(f"  💡 {nudge}")
                        print()

                    print("---")
                    print()
        except Exception:
            pass  # Silent fail on parse errors

    # ─────────────────────────────────────────────────────────────────
    # Stale Worktrees Warning
    # ─────────────────────────────────────────────────────────────────

    worktrees_dir = shipkit_dir / 'worktrees'
    if worktrees_dir.exists():
        stale_worktrees = []
        for worktree in worktrees_dir.iterdir():
            if worktree.is_dir():
                age_days = get_file_age_days(worktree)
                if age_days > 7:
                    stale_worktrees.append((worktree.name, int(age_days)))

        if stale_worktrees:
            stale_worktrees.sort(key=lambda x: x[1], reverse=True)
            print("# ⚠️ Stale Worktrees")
            print()
            print(f"**{len(stale_worktrees)} worktree(s) older than 7 days:**")
            for name, days in stale_worktrees[:5]:
                print(f"  • `.shipkit/worktrees/{name}` ({days}d old)")
            print()
            print("Run `/shipkit-cleanup-worktrees` to review and clean up.")
            print()
            print("---")
            print()

    # ─────────────────────────────────────────────────────────────────
    # Available Context Files Manifest
    # ─────────────────────────────────────────────────────────────────

    print("# 📚 Available Context Files")
    print()
    print("**Check these BEFORE re-discovering patterns:**")
    print()
    print("| File | Status | Read When |")
    print("|------|--------|-----------|")

    # Check each context file
    context_files = [
        ('why.md', 'Before product decisions'),
        ('stack.json', 'Before implementing (check patterns)'),
        ('architecture.json', 'Before design decisions'),
        ('schema.md', 'Before database work'),
        ('codebase-index.json', 'For navigation'),
    ]

    for filename, read_when in context_files:
        file_path = shipkit_dir / filename
        if file_path.exists():
            age = get_file_age_days(file_path)
            status = format_age(age)
        else:
            status = "Missing"
            read_when = f"Create: `/shipkit-project-context`" if filename in ['stack.json', 'schema.md'] else f"Create when needed"

        print(f"| `{filename}` | {status} | {read_when} |")

    print()
    print("*Read context files before exploring. Patterns are already documented.*")
    print()

    return 0


if __name__ == '__main__':
    sys.exit(main())