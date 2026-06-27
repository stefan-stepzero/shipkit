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

# Per the context-import policy: large artefacts are referenced (read on demand);
# only lean, bounded SLICES are injected always-on. Cap each injected digest so a
# large repo's index / goals file can never bloat context (AC-5 / AC-2).
MAX_DIGEST_CHARS = 3500  # ~3-4 KB per injected digest

# Artefacts the CLAUDE.md template `@`-imports (install/claude-md/shipkit.md).
# A missing one makes the `@`-import silently no-op, so the hook warns instead.
IMPORTED_ARTIFACTS = ['architecture.json', 'stack.json', 'why.json']


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


def get_missing_import_warning(shipkit_dir: Path) -> str | None:
    """Warn when a CLAUDE.md `@`-imported artefact is absent.

    The `@.shipkit/<file>` imports silently no-op when the file is missing, leaving
    the agent with zero context and no signal. The hook checks every session (the
    installer can't catch a user later deleting the file), so it surfaces the gap.
    """
    missing = [name for name in IMPORTED_ARTIFACTS if not (shipkit_dir / name).exists()]
    if not missing:
        return None
    files = ', '.join(f"`{m}`" for m in missing)
    return (f"WARNING: missing context — {files}. The CLAUDE.md `@`-import(s) silently "
            f"no-op, so the agent has no stack/architecture/vision context. "
            f"Run `/shipkit-project-context` to (re)generate.")


def get_strategic_digest(shipkit_dir: Path) -> str | None:
    """Inject a lean slice of goals/strategic.json — the always-on definition of done.

    Stage + stageImplications (focus/skip/qualityBar) + gates (name/status/criteria).
    NOT the full 15 KB file (criteria objects, rubrics) — those stay on disk to Read.
    Size-capped per the context-import policy.
    """
    strategic_file = shipkit_dir / 'goals' / 'strategic.json'
    if not strategic_file.exists():
        return None
    try:
        data = json.loads(strategic_file.read_text(encoding='utf-8'))
    except Exception:
        return None

    age = format_age(get_file_age_days(strategic_file))
    out = [f"## Stage & Gates — definition of done (age: {age})", '']

    stage = data.get('stage', {})
    if isinstance(stage, dict) and stage:
        cur = stage.get('current', '?')
        tgt = stage.get('target', '?')
        out.append(f"**Stage:** {cur} -> {tgt}")

    impl = data.get('stageImplications', {})
    if isinstance(impl, dict):
        qbar = impl.get('qualityBar')
        if qbar:
            out.append(f"**Quality bar:** {qbar}")
        focus = impl.get('focus')
        if isinstance(focus, list) and focus:
            out.append(f"**Focus this stage:** {', '.join(focus)}")
        skip = impl.get('skip')
        if isinstance(skip, list) and skip:
            out.append(f"**Out of scope this stage:** {', '.join(skip)}")
    out.append('')

    gates = data.get('gates', [])
    if isinstance(gates, list) and gates:
        out.append("**Gates (criteria that must pass):**")
        for g in gates:
            if not isinstance(g, dict):
                continue
            name = g.get('name', g.get('id', 'gate'))
            status = g.get('status', '?')
            crit = g.get('criteria', [])
            crit_str = ', '.join(crit) if isinstance(crit, list) else ''
            line = f"- {name} [{status}]"
            if crit_str:
                line += f" — {crit_str}"
            out.append(line)
        out.append('')

    out.append("*Full criteria/rubrics on disk — `Read .shipkit/goals/strategic.json` for thresholds.*")
    block = '\n'.join(out)
    if len(block) > MAX_DIGEST_CHARS:
        block = (block[:MAX_DIGEST_CHARS].rstrip() +
                 "\n... (truncated — Read `.shipkit/goals/strategic.json` for the rest)")
    return block


def get_codebase_digest(shipkit_dir: Path) -> str | None:
    """Inject a lean navigation digest from codebase-index.json — kills default-to-grep.

    concepts (concept -> files) + entryPoints + skip, size-capped. On a large index,
    inject top-N concepts + a pointer to the full on-disk file (never the whole thing).
    """
    index_file = shipkit_dir / 'codebase-index.json'
    if not index_file.exists():
        return None
    try:
        data = json.loads(index_file.read_text(encoding='utf-8'))
    except Exception:
        return None

    age = format_age(get_file_age_days(index_file))
    out = [f"## Codebase Map (index age: {age} — re-run /shipkit-codebase-index if stale)", '']

    entry = data.get('entryPoints', {})
    if isinstance(entry, dict) and entry:
        pairs = [f"{k}: `{v}`" for k, v in entry.items() if isinstance(v, str)]
        if pairs:
            out.append("**Entry points:** " + ', '.join(pairs))
            out.append('')

    pointer = "*Full index on disk — `Read .shipkit/codebase-index.json` for per-file detail.*"

    concepts = data.get('concepts', {})
    concept_lines = []
    if isinstance(concepts, dict):
        for name, files in concepts.items():
            if isinstance(files, list):
                files_str = ', '.join(f"`{f}`" for f in files)
            else:
                files_str = f"`{files}`"
            concept_lines.append(f"- **{name}:** {files_str}")

    skip = data.get('skip', [])
    skip_line = ''
    if isinstance(skip, list) and skip:
        skip_line = "**Skip (don't read):** " + ', '.join(f"`{s}`" for s in skip)

    # Budget concept lines against the size cap, reserving room for skip + pointer,
    # so a large index degrades to top-N concepts + pointer rather than dumping all.
    reserve = len(skip_line) + len(pointer) + 80
    budget = MAX_DIGEST_CHARS - len('\n'.join(out)) - reserve
    kept = []
    used = 0
    for line in concept_lines:
        if kept and used + len(line) + 1 > budget:
            break
        kept.append(line)
        used += len(line) + 1
    omitted = len(concept_lines) - len(kept)

    if kept:
        out.append("**Concepts -> files:**")
        out.extend(kept)
        if omitted > 0:
            out.append(f"- ... {omitted} more concept(s) — Read the full index for the rest.")
        out.append('')
    if skip_line:
        out.append(skip_line)
        out.append('')
    out.append(pointer)
    return '\n'.join(out)


def main():
    print(f"[shipkit:{HOOK_NAME}] running", file=sys.stderr)
    # Parse hook input
    try:
        hook_input = json.load(sys.stdin)
    except Exception:
        hook_input = {}

    # Resolve skills_dir from the hook's OWN location — works whether installed
    # in a project's .claude/, at user level ~/.claude/, or run from source.
    hook_dir = Path(__file__).parent
    if hook_dir.name == 'hooks' and hook_dir.parent.name == 'shared':
        skills_dir = hook_dir.parent.parent / 'skills'   # source repo (install/shared/hooks)
    else:
        skills_dir = hook_dir.parent / 'skills'          # installed (.claude/hooks → .claude/skills)

    # Resolve project root from the SESSION, NOT the hook's file location.
    # At user scope the hook lives in ~/.claude, so deriving the project from the
    # hook path would wrongly point at $HOME. CLAUDE_PROJECT_DIR is the session's
    # project root; fall back to the hook input's cwd.
    env_dir = os.environ.get('CLAUDE_PROJECT_DIR', '')
    input_cwd = hook_input.get('cwd', '') if isinstance(hook_input, dict) else ''
    if env_dir:
        project_root = Path(env_dir)
    elif input_cwd:
        project_root = Path(input_cwd)
    else:
        project_root = None

    # Collect output lines instead of printing directly
    lines = []

    # Master skill must be installed.
    master_skill = skills_dir / 'shipkit-master' / 'SKILL.md'
    if not master_skill.exists():
        lines.append("Shipkit not properly installed. Run the installer again.")
        _emit_context('\n'.join(lines), project_root)
        return 0

    # Gate the heavy orchestration injection on an ACTIVATED Shipkit project
    # (a project with a .shipkit/ folder). This matters at user scope, where the
    # hook fires in every project globally — we must not dump the master skill
    # (~1500 tokens) + routing into unrelated work. A project is activated the
    # first time any /shipkit-* skill writes into .shipkit/. Until then, emit a
    # single-line hint. At project scope the installer creates .shipkit/, so this
    # path is behavior-preserving (full context loads as before).
    shipkit_dir = (project_root / '.shipkit') if project_root is not None else None
    if shipkit_dir is None or not shipkit_dir.exists():
        lines.append(
            "Shipkit is installed. Run `/shipkit-project-context` to activate it "
            "in this project (creates `.shipkit/` and loads full context next session)."
        )
        _emit_context('\n'.join(lines), project_root)
        return 0

    # ── Activated Shipkit project: load full orchestration context ──
    lines.append(master_skill.read_text(encoding='utf-8'))
    lines.append('')
    lines.append('---')
    lines.append('')

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

    # ── Progress resume ──
    progress = get_progress_summary(project_root)
    if progress:
        lines.append(progress)
        lines.append('')

    # ── Missing `@`-import warning (hook-warn guard) ──
    import_warning = get_missing_import_warning(shipkit_dir)
    if import_warning:
        lines.append(import_warning)
        lines.append('')

    # ── Stage & gates: lean always-on "definition of done" ──
    strategic = get_strategic_digest(shipkit_dir)
    if strategic:
        lines.append(strategic)
        lines.append('')

    # ── Codebase navigation map: lean digest (stops default-to-grep) ──
    codebase = get_codebase_digest(shipkit_dir)
    if codebase:
        lines.append(codebase)
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

    artifact_count = found_count + spec_count + plan_count
    _emit_context('\n'.join(lines), project_root, artifact_count)
    return 0


def _emit_context(content: str, project_root: Path = None, artifact_count: int = 0):
    """Output context using the structured additionalContext CC pattern.

    Emits reloadSkills (refresh skill registry on session start) and a dynamic
    sessionTitle. Per hooks-reference.md / official CC docs (SessionStart output
    schema), ALL SessionStart fields — hookEventName, additionalContext,
    sessionTitle, reloadSkills, watchPaths — live INSIDE hookSpecificOutput;
    hookEventName is required. sessionTitle is honoured only on source=startup|resume
    (ignored on clear/compact, which is harmless). watchPaths registers .shipkit/ so
    FileChanged events can fire when context files change. Placing any of these at the
    top level silently no-ops them, so they must be nested.
    """
    project_name = project_root.name if project_root else "project"
    session_title = f"Shipkit — {project_name} ({artifact_count} artifacts)"
    watch_dir = str(project_root / ".shipkit") if project_root else ".shipkit"
    output = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": content,
            "sessionTitle": session_title,
            "reloadSkills": True,
            "watchPaths": [watch_dir]
        }
    }
    print(json.dumps(output))


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        print(f"[shipkit:{HOOK_NAME}] ERROR: {e}", file=sys.stderr)
        sys.exit(0)
