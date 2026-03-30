#!/usr/bin/env python3
"""
Shipkit - Session Start Hook

Context loader: resumes progress, lists available context files, checks for updates.
"""

import sys
import os
import json
import re
import urllib.request
from pathlib import Path
from datetime import datetime

HOOK_NAME = "session-start"
GITHUB_VERSION_URL = "https://raw.githubusercontent.com/stefan-stepzero/shipkit/main/VERSION"


def get_installed_version(project_root: Path) -> str:
    """Read installed Shipkit version from .shipkit/VERSION or VERSION."""
    if project_root:
        for candidate in [project_root / ".shipkit" / "VERSION", project_root / "VERSION"]:
            if candidate.exists():
                return candidate.read_text(encoding='utf-8').strip()
    return "unknown"


def get_file_age_days(file_path: Path) -> float:
    """Get file age in days."""
    if not file_path.exists():
        return -1
    mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
    return (datetime.now() - mtime).total_seconds() / 86400


def format_age(days: float) -> str:
    """Format age as human-readable string."""
    if days < 0:
        return "missing"
    if days < 1/24:
        return f"{int(days * 24 * 60)}m ago"
    if days < 1:
        return f"{int(days * 24)}h ago"
    return f"{int(days)}d ago"


def parse_version(version_str: str) -> tuple:
    """Parse version string to comparable tuple."""
    try:
        parts = version_str.strip().split('.')
        nums = [int(p) for p in parts[:3]]
        while len(nums) < 3:
            nums.append(0)
        return tuple(nums)
    except (ValueError, AttributeError):
        return (0, 0, 0)


def check_for_updates(project_root: Path) -> str | None:
    """Check if newer Shipkit version is available (once per day, 3s timeout)."""
    check_file = project_root / '.shipkit' / '.update-check.local'
    installed_version = get_installed_version(project_root)

    if installed_version == "unknown":
        return None

    # Rate limit: skip if checked within last 24 hours
    if check_file.exists():
        age_days = get_file_age_days(check_file)
        if 0 <= age_days < 1:
            try:
                lines = check_file.read_text(encoding='utf-8').strip().split('\n')
                if len(lines) >= 2 and parse_version(lines[1]) > parse_version(installed_version):
                    return f"Shipkit {lines[1]} available (you have {installed_version}). Run `/shipkit-update`"
            except Exception:
                pass
            return None

    try:
        request = urllib.request.Request(GITHUB_VERSION_URL, headers={'User-Agent': 'Shipkit/1.0'})
        with urllib.request.urlopen(request, timeout=3) as response:
            remote_version = response.read().decode('utf-8').strip()

        if not re.match(r'^\d+\.\d+(\.\d+)?$', remote_version):
            return None

        try:
            check_file.parent.mkdir(parents=True, exist_ok=True)
            check_file.write_text(f"{datetime.now().isoformat()}\n{remote_version}")
        except Exception:
            pass

        if parse_version(remote_version) > parse_version(installed_version):
            return f"Shipkit {remote_version} available (you have {installed_version}). Run `/shipkit-update`"
    except Exception:
        pass

    return None


def get_progress_summary(project_root: Path) -> str | None:
    """Get last session summary from progress.json."""
    progress_file = project_root / '.shipkit' / 'progress.json'
    if not progress_file.exists():
        return None

    try:
        data = json.loads(progress_file.read_text(encoding='utf-8'))

        # Handle JSON artifact format
        sessions = data.get('sessions', [])
        if sessions:
            last = sessions[-1]
            summary = last.get('summary', '')
            timestamp = last.get('timestamp', last.get('date', ''))
            if summary:
                if len(summary) > 80:
                    summary = summary[:77] + "..."
                return f"**Last session** ({timestamp}): {summary}"

        # Fallback: just show file age
        age = get_file_age_days(progress_file)
        return f"**Last session**: {format_age(age)}"
    except Exception:
        age = get_file_age_days(progress_file)
        return f"**Last session**: {format_age(age)}"


def main():
    print(f"[shipkit:{HOOK_NAME}] running", file=sys.stderr)
    # Parse hook input
    try:
        hook_input = json.load(sys.stdin)
    except Exception:
        hook_input = {}

    # Find project root
    hook_dir = Path(__file__).parent
    if hook_dir.name == 'hooks' and hook_dir.parent.name == 'shared':
        skills_dir = hook_dir.parent.parent / 'skills'
        project_root = None
    else:
        claude_dir = hook_dir.parent
        skills_dir = claude_dir / 'skills'
        project_root = claude_dir.parent

    # Collect output lines instead of printing directly
    lines = []

    # Load master skill (orchestration context for every session)
    master_skill = skills_dir / 'shipkit-master' / 'SKILL.md'
    if not master_skill.exists():
        lines.append("Shipkit not properly installed. Run the installer again.")
        _emit_context('\n'.join(lines))
        return 0

    lines.append(master_skill.read_text(encoding='utf-8'))
    lines.append('')
    lines.append('---')
    lines.append('')

    if project_root is None:
        _emit_context('\n'.join(lines))
        return 0

    shipkit_dir = project_root / '.shipkit'

    # ── Version check ──
    update_msg = check_for_updates(project_root)
    if update_msg:
        lines.append(update_msg)
        lines.append('')

    # ── Clean old observability logs ──
    obs_dir = shipkit_dir / 'observability'
    if obs_dir.exists():
        for old_log in obs_dir.glob('skill-usage.*.local.jsonl'):
            try:
                old_log.unlink()
            except OSError:
                pass

    # ── Fresh project ──
    if not shipkit_dir.exists():
        lines.append("No `.shipkit/` folder found — fresh project.")
        lines.append('')
        lines.append("Start with: `/shipkit-project-context` to scan your codebase")
        _emit_context('\n'.join(lines))
        return 0

    # ── Progress resume ──
    progress = get_progress_summary(project_root)
    if progress:
        lines.append(progress)
        lines.append('')

    # ── Available context files ──
    lines.append("## Available Context")
    lines.append('')
    lines.append("| File | Status | Purpose |")
    lines.append("|------|--------|---------|")

    context_files = [
        ('why.json', 'Project vision & purpose'),
        ('product-discovery.json', 'Personas, journeys, needs'),
        ('product-definition.json', 'Product blueprint'),
        ('engineering-definition.json', 'Engineering blueprint'),
        ('stack.json', 'Tech stack & patterns'),
        ('architecture.json', 'Architecture decisions'),
        ('codebase-index.json', 'Semantic file map'),
        ('progress.json', 'Session continuity'),
        ('spec-roadmap.json', 'Spec priority order'),
        ('orchestration.json', 'Pipeline state & crash recovery'),
    ]

    found_count = 0
    for filename, purpose in context_files:
        file_path = shipkit_dir / filename
        if file_path.exists():
            age = format_age(get_file_age_days(file_path))
            lines.append(f"| `{filename}` | {age} | {purpose} |")
            found_count += 1

    # Check for active specs and plans
    specs_dir = shipkit_dir / 'specs' / 'active'
    plans_dir = shipkit_dir / 'plans' / 'active'
    spec_count = len(list(specs_dir.glob('*.json'))) if specs_dir.exists() else 0
    plan_count = len(list(plans_dir.glob('*.json'))) if plans_dir.exists() else 0

    if spec_count > 0:
        lines.append(f"| `specs/active/` | {spec_count} spec(s) | Feature specifications |")
    if plan_count > 0:
        lines.append(f"| `plans/active/` | {plan_count} plan(s) | Implementation plans |")

    # Check for goals
    goals_dir = shipkit_dir / 'goals'
    if goals_dir.exists():
        goal_files = list(goals_dir.glob('*.json'))
        if goal_files:
            names = ', '.join(f.stem for f in goal_files)
            lines.append(f"| `goals/` | {names} | Success criteria |")

    lines.append('')

    if found_count == 0 and spec_count == 0 and plan_count == 0:
        lines.append("No context files yet. Start with `/shipkit-project-context`.")
        lines.append('')

    lines.append("*Read context files before re-discovering patterns.*")
    lines.append('')

    _emit_context('\n'.join(lines))
    return 0


def _emit_context(content: str):
    """Output context using the structured additionalContext CC pattern."""
    output = {
        "hookSpecificOutput": {
            "additionalContext": content
        }
    }
    print(json.dumps(output))


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        print(f"[shipkit:{HOOK_NAME}] ERROR: {e}", file=sys.stderr)
        sys.exit(0)
