#!/usr/bin/env python3
"""
Shipkit - Session Start Hook

Context loader: resumes progress, lists available context files, checks for updates.
"""

import sys
import os
import json
import re
import subprocess
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

# Size budgets (bytes) for ALWAYS-LOADED artifacts — files whose every byte enters
# context in EVERY session (`@`-imports + CLAUDE.md). Budgets are warning thresholds,
# not hard failures: the hook measures each file each session and shouts when one is
# over, at the moment the cost is being paid. ~4 bytes ≈ 1 token. Keys relative to
# project root; remediation is per-file (how to lean THAT artifact, not generic advice).
SIZE_BUDGETS = {
    'CLAUDE.md': (
        15_000,
        "prune Project Learnings / Working Preferences; move detail to `.shipkit/` files read on demand",
    ),
    '.shipkit/architecture.json': (
        10_000,
        "run `/shipkit-adr` to stub superseded decisions, or the one-time "
        "`migrate-architecture-log.py` splitter (full bodies belong in architecture-archive.json)",
    ),
    '.shipkit/stack.json': (
        6_000,
        "re-run `/shipkit-project-context` — the stack scan should stay a summary, not a lockfile dump",
    ),
    '.shipkit/why.json': (
        6_000,
        "trim to vision/constraints/approach; long-form product thinking belongs in product-definition.json",
    ),
}

# The codebase index's JUDGMENT layer (framework/concepts/coreFiles) is considered
# stale after this many days. The mechanical layer auto-refreshes on commit, so the
# nudge keys off fullRefreshedAt — NOT file mtime, which now moves on every commit.
INDEX_STALE_DAYS = 14


def _date_age_days(date_str: str) -> float:
    """Age in days from a 'YYYY-MM-DD' stamp; -1 if unparseable/empty."""
    if not date_str:
        return -1
    try:
        d = datetime.strptime(str(date_str)[:10], '%Y-%m-%d')
        return (datetime.now() - d).total_seconds() / 86400
    except Exception:
        return -1


def refresh_codebase_index(skills_dir: Path, project_root: Path) -> None:
    """Deterministic (no-LLM) mechanical refresh of the codebase index at session start.

    Catches commits made outside Claude (e.g. the user's own terminal) that the
    PostToolUse git-commit hook never saw. Best-effort: only refreshes an EXISTING
    index (never creates one), short timeout, never raises.
    """
    if project_root is None:
        return
    index_file = project_root / '.shipkit' / 'codebase-index.json'
    if not index_file.exists():
        return
    generator = skills_dir / 'shipkit-codebase-index' / 'scripts' / 'generate_index.py'
    if not generator.exists():
        return
    try:
        subprocess.run(
            [sys.executable, '-X', 'utf8', str(generator), '--refresh-mechanical'],
            cwd=str(project_root), capture_output=True, text=True, timeout=20,
        )
    except Exception:
        pass


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


def format_size(num_bytes: int) -> str:
    """Format a byte count as a human-readable size."""
    if num_bytes < 1024:
        return f"{num_bytes} B"
    return f"{num_bytes / 1024:.1f} KB"


def get_size_budget_warnings(project_root: Path) -> str | None:
    """LOUD warning when an always-loaded artifact exceeds its size budget.

    These files load into context every session; unbounded growth silently eats
    the budget that makes every other decision possible (observed: a 150 KB
    architecture.json). Ages are already surfaced elsewhere — this is the size half.
    Silent when everything is within budget.
    """
    over = []
    total = 0
    for rel_path, (budget, remedy) in SIZE_BUDGETS.items():
        f = project_root / rel_path
        if not f.exists():
            continue
        try:
            size = f.stat().st_size
        except OSError:
            continue
        total += size
        if size > budget:
            over.append((rel_path, size, budget, remedy))
    if not over:
        return None

    out = ["## ⚠️ CONTEXT BUDGET EXCEEDED — always-loaded files are oversized", '']
    out.append(
        f"These files load into context EVERY session "
        f"(always-on total: {format_size(total)} ≈ {total // 4:,} tokens). Lean them now:"
    )
    out.append('')
    for rel_path, size, budget, remedy in over:
        out.append(
            f"- **`{rel_path}` is {format_size(size)}** (budget {format_size(budget)}) — {remedy}"
        )
    return '\n'.join(out)


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


def _mechanism_ids_from_scope(scope) -> list:
    """Extract mechanism ids from an ADR `scope` like 'mechanism:M-001' (or a
    comma-list 'mechanism:M-001,M-002'). Returns [] for cross-cutting/other scopes."""
    if isinstance(scope, str) and scope.startswith('mechanism:'):
        return [s.strip() for s in scope[len('mechanism:'):].split(',') if s.strip()]
    return []


def get_ed_adr_drift_warning(shipkit_dir: Path) -> str | None:
    """Flag engineering-definition mechanisms that a load-bearing ADR has invalidated.

    The Project-B retro's #2 failure: the engineering-definition described PIN auth for
    3 weeks while the ADR log (the only artefact that kept pace) had superseded it — and
    nothing flagged the divergence, so new sessions built against a stale ED. This is the
    deterministic (no-LLM) divergence check: compare ED mechanisms (`M-###`) against the
    ADR log's superseded/dormant/amended decisions scoped to a mechanism, and surface the
    count/list at session-start so a fresh session reconciles before building.

    Linkage convention (see engineering-definition/references/architecture-log-schema.md):
    an ADR scoped to a mechanism carries `scope: "mechanism:M-###"`. When such an ADR is
    superseded/dormant or amends another, the corresponding ED mechanism is stale unless it
    already acknowledges it via `supersededByADR` / `staleSince`.

    Reads `architecture-archive.json` (full ADR bodies retain scope + status + links) as the
    authoritative ADR source; falls back to the lean `architecture.json` (best-effort — the
    lean file's superseded stubs drop scope, so only dormant/amended-active entries surface).
    """
    ed_file = shipkit_dir / 'engineering-definition.json'
    if not ed_file.exists():
        return None
    adr_file = shipkit_dir / 'architecture-archive.json'
    if not adr_file.exists():
        adr_file = shipkit_dir / 'architecture.json'
    if not adr_file.exists():
        return None
    try:
        ed = json.loads(ed_file.read_text(encoding='utf-8'))
        adr = json.loads(adr_file.read_text(encoding='utf-8'))
    except Exception:
        return None

    mechanisms = ed.get('mechanisms', [])
    decisions = adr.get('decisions', [])
    if not isinstance(mechanisms, list) or not isinstance(decisions, list):
        return None

    # Map ED mechanism id -> already-acknowledged? (an explicit supersededByADR/staleSince
    # marker means a session has reconciled it, so it is no longer an UNRESOLVED drift).
    ed_ids = {}
    for m in mechanisms:
        if isinstance(m, dict) and m.get('id'):
            ed_ids[m['id']] = bool(m.get('supersededByADR') or m.get('staleSince'))

    # An ADR signals its scoped mechanism is stale when the decision was replaced
    # (superseded), retired (dormant/deprecated), or partially changed (amended).
    stale_statuses = {'superseded', 'dormant', 'deprecated'}
    stale = set()
    for d in decisions:
        if not isinstance(d, dict):
            continue
        mech_ids = _mechanism_ids_from_scope(d.get('scope'))
        if not mech_ids:
            continue
        status = str(d.get('status', '')).lower()
        signals_stale = status in stale_statuses or bool(d.get('amendedBy'))
        if not signals_stale:
            continue
        for mid in mech_ids:
            if mid in ed_ids and not ed_ids[mid]:
                stale.add(mid)

    if not stale:
        return None
    ids = ', '.join(sorted(stale))
    n = len(stale)
    return (
        f"WARNING: engineering-definition has {n} mechanism(s) stale vs the ADR log "
        f"({ids}) — a load-bearing ADR superseded/retired/amended them but the "
        f"engineering-definition still describes the old approach. Reconcile before "
        f"building against them: re-run `/shipkit-engineering-definition`, or treat the "
        f"ADR log (`architecture.json`) as the live authority."
    )


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

    # Two-tier freshness: the mechanical layer auto-refreshes on commit
    # (mechanicalRefreshedAt), so file mtime no longer signals judgment-layer age.
    # Key the staleness nudge off fullRefreshedAt — when Claude last derived the
    # framework/concepts/coreFiles fields.
    full_age = _date_age_days(data.get('fullRefreshedAt') or data.get('generated'))
    out = ["## Codebase Map", '']
    if full_age >= INDEX_STALE_DAYS:
        out.append(
            f"> Semantic layer ~{int(full_age)}d old (last full index). File-level data "
            f"auto-refreshes on commit, but framework/concepts/coreFiles may have drifted "
            f"— re-run `/shipkit-codebase-index` to refresh."
        )
        out.append('')

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

    # The engine skill (shipkit-orchestrate) is the mandatory core — must be installed.
    engine_skill = skills_dir / 'shipkit-orchestrate' / 'SKILL.md'
    if not engine_skill.exists():
        lines.append("Shipkit not properly installed. Run the installer again.")
        _emit_context('\n'.join(lines), project_root)
        return 0

    # Gate the heavy orchestration injection on an ACTIVATED Shipkit project
    # (a project with a .shipkit/ folder). This matters at user scope, where the
    # hook fires in every project globally — we must not dump the engine skill
    # (~1700 tokens) + routing into unrelated work. A project is activated the
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

    # ── Activated Shipkit project: point at the engine, don't inject its body. ──
    # Hooks inject STATE, not instructions. The engine's full protocol (~1700 tokens)
    # loads when the skill is invoked; its listing description already routes to it.
    lines.append(
        "**Shipkit active.** Engine: `/shipkit-orchestrate` — drives any set of steps to a "
        "confirmed ground-truth bar (delegate → reconcile → re-dispatch loop).\n"
        "Phase skills (build/review/direction) call it; invoke it directly to drive work to done.\n"
        "Its full protocol loads on invocation — do not re-implement orchestration inline."
    )
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

    # ── ED↔ADR staleness: flag mechanisms a load-bearing ADR has invalidated ──
    ed_drift = get_ed_adr_drift_warning(shipkit_dir)
    if ed_drift:
        lines.append(ed_drift)
        lines.append('')

    # ── Size budgets on always-loaded artifacts (loud when over, silent when fine) ──
    size_warning = get_size_budget_warnings(project_root)
    if size_warning:
        lines.append(size_warning)
        lines.append('')

    # ── Stage & gates: lean always-on "definition of done" ──
    strategic = get_strategic_digest(shipkit_dir)
    if strategic:
        lines.append(strategic)
        lines.append('')

    # ── Keep the codebase index fresh (deterministic, no LLM) before digesting it.
    #    Catches commits made outside Claude that the git-commit hook never saw. ──
    refresh_codebase_index(skills_dir, project_root)

    # ── Codebase navigation map: lean digest (stops default-to-grep) ──
    codebase = get_codebase_digest(shipkit_dir)
    if codebase:
        lines.append(codebase)
        lines.append('')

    # ── Available context files ──
    lines.append("## Available Context")
    lines.append('')
    lines.append("| File | Age | Size | Purpose |")
    lines.append("|------|-----|------|---------|")

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
            try:
                size = format_size(file_path.stat().st_size)
            except OSError:
                size = "?"
            lines.append(f"| `{filename}` | {age} | {size} | {purpose} |")
            found_count += 1

    # Check for active specs and plans
    specs_dir = shipkit_dir / 'specs' / 'active'
    plans_dir = shipkit_dir / 'plans' / 'active'
    spec_count = len(list(specs_dir.glob('*.json'))) if specs_dir.exists() else 0
    plan_count = len(list(plans_dir.glob('*.json'))) if plans_dir.exists() else 0

    if spec_count > 0:
        lines.append(f"| `specs/active/` | {spec_count} spec(s) | — | Feature specifications |")
    if plan_count > 0:
        lines.append(f"| `plans/active/` | {plan_count} plan(s) | — | Implementation plans |")

    # Check for goals
    goals_dir = shipkit_dir / 'goals'
    if goals_dir.exists():
        goal_files = list(goals_dir.glob('*.json'))
        if goal_files:
            names = ', '.join(f.stem for f in goal_files)
            lines.append(f"| `goals/` | {names} | — | Success criteria |")

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
