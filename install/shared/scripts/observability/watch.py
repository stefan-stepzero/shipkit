#!/usr/bin/env python3
"""
Shipkit - Dashboard Renderer

Combines orchestration.json, skill-usage JSONL, and artifact scan
into a single auto-refreshing HTML dashboard.

Modes:
  python watch.py          — scan once, render once, exit
  python watch.py --watch  — re-render on file changes (poll every 2s)
"""

import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime
from html import escape

# Import scan module from same directory
sys.path.insert(0, str(Path(__file__).parent))
from scan import scan


# ── Data Loading ──────────────────────────────────────────────

def load_orchestration(shipkit_dir: Path) -> dict:
    """Load orchestration.json control plane data."""
    path = shipkit_dir / 'orchestration.json'
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (json.JSONDecodeError, IOError):
        return {}


def load_skill_usage(obs_dir: Path) -> list[dict]:
    """Merge all skill-usage JSONL files into a single list."""
    entries = []
    if not obs_dir.exists():
        return entries
    for f in obs_dir.glob('skill-usage.*.local.jsonl'):
        try:
            for line in f.read_text(encoding='utf-8').splitlines():
                line = line.strip()
                if line:
                    entries.append(json.loads(line))
        except (json.JSONDecodeError, IOError):
            continue
    entries.sort(key=lambda e: e.get('timestamp', ''))
    return entries


def summarize_skill_usage(entries: list[dict]) -> list[dict]:
    """Aggregate skill usage entries into per-skill summaries."""
    skills = {}
    for e in entries:
        name = e.get('skill', 'unknown')
        if name not in skills:
            skills[name] = {'skill': name, 'count': 0, 'agents': set(), 'first': None, 'last': None}
        rec = skills[name]
        rec['count'] += 1
        agent = SKILL_AGENT_MAP.get(name, e.get('agentType', ''))
        if agent:
            rec['agents'].add(agent)
        ts = e.get('timestamp', '')
        if ts:
            if not rec['first'] or ts < rec['first']:
                rec['first'] = ts
            if not rec['last'] or ts > rec['last']:
                rec['last'] = ts

    result = []
    for rec in sorted(skills.values(), key=lambda r: r.get('first', ''), reverse=False):
        result.append({
            'skill': rec['skill'],
            'count': rec['count'],
            'agents': ', '.join(sorted(rec['agents'])) if rec['agents'] else '',
            'first': rec['first'] or '',
            'last': rec['last'] or '',
        })
    return result


# ── Model Estimation ──────────────────────────────────────────

# Map agent names to models (from DOC-015 taxonomy)
AGENT_MODEL_MAP = {
    'shipkit-visionary-agent': 'opus',
    'shipkit-product-owner-agent': 'opus',
    'shipkit-architect-agent': 'opus',
    'shipkit-implementer-agent': 'opus',
    'shipkit-orch-direction-agent': 'sonnet',
    'shipkit-orch-planning-agent': 'sonnet',
    'shipkit-orch-shipping-agent': 'sonnet',
    'shipkit-orch-master-agent': 'sonnet',
    'shipkit-reviewer-direction-agent': 'sonnet',
    'shipkit-reviewer-planning-agent': 'sonnet',
    'shipkit-reviewer-shipping-agent': 'sonnet',
}

# Skills to their declared agent (from SKILL.md frontmatter `agent:` field)
SKILL_AGENT_MAP = {
    'shipkit-why-project': 'visionary',
    'shipkit-stage': 'visionary',
    'shipkit-product-discovery': 'product-owner',
    'shipkit-product-definition': 'product-owner',
    'shipkit-product-goals': 'product-owner',
    'shipkit-spec-roadmap': 'product-owner',
    'shipkit-spec': 'product-owner',
    'shipkit-test-cases': 'product-owner',
    'shipkit-feedback-bug': 'product-owner',
    'shipkit-engineering-definition': 'architect',
    'shipkit-engineering-goals': 'architect',
    'shipkit-project-context': 'architect',
    'shipkit-codebase-index': 'architect',
    'shipkit-plan': 'architect',
    'shipkit-prompt-audit': 'architect',
    'shipkit-review-shipping': 'reviewer-shipping',
    'shipkit-preflight': 'reviewer-shipping',
    'shipkit-scale-ready': 'reviewer-shipping',
    'shipkit-ux-audit': 'reviewer-shipping',
    'shipkit-review-direction': 'reviewer-direction',
    'shipkit-review-planning': 'reviewer-planning',
    'shipkit-master': 'orch-master',
    'shipkit-orch-direction': 'orch-direction',
    'shipkit-orch-planning': 'orch-planning',
    'shipkit-orch-shipping': 'orch-shipping',
    'shipkit-thinking-partner': 'thinking-partner',
}

# Skills that dispatch to known agents
SKILL_MODEL_MAP = {
    'shipkit-why-project': 'opus',
    'shipkit-product-discovery': 'opus',
    'shipkit-product-definition': 'opus',
    'shipkit-engineering-definition': 'opus',
    'shipkit-stage': 'opus',
    'shipkit-product-goals': 'opus',
    'shipkit-engineering-goals': 'opus',
    'shipkit-project-context': 'opus',
    'shipkit-codebase-index': 'opus',
    'shipkit-spec-roadmap': 'opus',
    'shipkit-spec': 'opus',
    'shipkit-plan': 'opus',
    'shipkit-test-cases': 'opus',
    'shipkit-review-shipping': 'opus',
    'shipkit-preflight': 'opus',
    'shipkit-orch-direction': 'sonnet',
    'shipkit-orch-planning': 'sonnet',
    'shipkit-orch-shipping': 'sonnet',
    'shipkit-review-direction': 'sonnet',
    'shipkit-review-planning': 'sonnet',
}


def estimate_model(entry: dict) -> str:
    """Guess model from skill name or agent type."""
    skill = entry.get('skill', '')
    if skill in SKILL_MODEL_MAP:
        return SKILL_MODEL_MAP[skill]
    agent = entry.get('agentType', '')
    if agent in AGENT_MODEL_MAP:
        return AGENT_MODEL_MAP[agent]
    return 'unknown'


def cost_summary(entries: list[dict]) -> dict:
    """Count invocations per model."""
    counts = {'opus': 0, 'sonnet': 0, 'unknown': 0}
    for e in entries:
        model = estimate_model(e)
        counts[model] = counts.get(model, 0) + 1
    return counts


# ── HTML Rendering ────────────────────────────────────────────

LOOP_NAMES = ['direction', 'planning', 'shipping']


def render_pipeline_status(orch: dict) -> str:
    """Render pipeline progress bars."""
    loops = orch.get('loops', {})
    if not loops:
        return '<div class="section"><h2>Pipeline Status</h2><p class="muted">No orchestration data</p></div>'

    rows = []
    for name in LOOP_NAMES:
        loop = loops.get(name, {})
        status = loop.get('status', 'pending')
        dispatches = loop.get('completedDispatches', [])
        review_cycles = loop.get('reviewCycles', 0)
        current = loop.get('currentSkill')
        count = len(dispatches)

        if status == 'pass':
            bar_class = 'bar-pass'
            label = 'PASS'
            pct = 100
        elif status == 'partial':
            bar_class = 'bar-partial'
            label = 'PARTIAL'
            pct = 60
        elif status == 'in_progress':
            bar_class = 'bar-active'
            label = f'{count} done'
            pct = min(95, max(10, count * 15))
        else:
            bar_class = 'bar-pending'
            label = 'PENDING'
            pct = 0

        current_html = f' <span class="current-skill">→ {escape(current)}</span>' if current else ''
        rows.append(f'''
        <div class="loop-row">
          <span class="loop-name">{name.title()}</span>
          <div class="bar-track">
            <div class="bar-fill {bar_class}" style="width:{pct}%"></div>
          </div>
          <span class="loop-label">{label}</span>
          <span class="loop-meta">{count} skills | {review_cycles} review cycles{current_html}</span>
        </div>''')

    return f'<div class="section"><h2>Pipeline Status</h2>{"".join(rows)}</div>'


def render_current_activity(orch: dict) -> str:
    """Render what's currently happening."""
    overall_status = orch.get('status', '')
    if overall_status in ('completed', 'pass', 'partial'):
        return f'<div class="section"><h2>Current Activity</h2><p class="status-done">Pipeline {overall_status}</p></div>'

    loops = orch.get('loops', {})
    active_loop = orch.get('activeLoop', '')
    if not active_loop or active_loop not in loops or active_loop == 'none':
        if not orch:
            return '<div class="section"><h2>Current Activity</h2><p class="muted">No orchestration data</p></div>'
        return '<div class="section"><h2>Current Activity</h2><p class="muted">No active loop</p></div>'

    loop = loops[active_loop]
    loop_status = loop.get('status', '')
    if loop_status in ('pass', 'partial'):
        return f'''<div class="section"><h2>Current Activity</h2>
        <p class="status-done">{active_loop.title()} loop {loop_status} — awaiting next loop</p></div>'''

    current = loop.get('currentSkill', '')
    if current:
        return f'''<div class="section"><h2>Current Activity</h2>
        <p class="status-active">Active loop: <strong>{active_loop}</strong> — dispatching <code>{escape(current)}</code></p></div>'''
    return f'''<div class="section"><h2>Current Activity</h2>
    <p class="status-active">Active loop: <strong>{active_loop}</strong> — between dispatches</p></div>'''


def render_skill_invocations(usage_summary: list[dict]) -> str:
    """Render skill usage table."""
    if not usage_summary:
        return '<div class="section"><h2>Skill Invocations</h2><p class="muted">No skill usage data</p></div>'

    rows = []
    for s in usage_summary:
        rows.append(f'''<tr>
          <td><code>{escape(s["skill"])}</code></td>
          <td class="num">{s["count"]}x</td>
          <td>{escape(s["agents"])}</td>
        </tr>''')

    return f'''<div class="section"><h2>Skill Invocations</h2>
    <table>
      <thead><tr><th>Skill</th><th>Count</th><th>Agent</th></tr></thead>
      <tbody>{"".join(rows)}</tbody>
    </table></div>'''


ARTIFACT_GROUPS = [
    ('Direction', [
        'why.json', 'product-discovery.json',
        'product-definition.json', 'engineering-definition.json',
        'architecture.json',
    ]),
    ('Planning', [
        'stack.json', 'codebase-index.json', 'spec-roadmap.json',
    ]),
    ('Shipping', [
        'progress.json',
    ]),
    ('System', [
        'orchestration.json',
    ]),
]


def render_artifact_chain(artifacts: dict, orch: dict) -> str:
    """Render artifact existence/status grid, grouped by loop."""
    loops = orch.get('loops', {})

    def loop_status(name: str) -> str:
        return loops.get(name.lower(), {}).get('status', 'pending')

    html_parts = []
    for group_name, files in ARTIFACT_GROUPS:
        status = loop_status(group_name)
        cells = []
        for name in files:
            info = artifacts.get(name, {})
            if info.get('exists'):
                size = info.get('size', 0)
                size_str = f'{size / 1024:.1f}KB' if size > 1024 else f'{size}B'
                age = info.get('age', '')
                cells.append(f'<div class="artifact ok"><div class="art-name">{name}</div>'
                             f'<div class="art-meta">OK {size_str}</div>'
                             f'<div class="art-age">{escape(age)}</div></div>')
            elif status == 'pending':
                cells.append(f'<div class="artifact pending"><div class="art-name">{name}</div>'
                             f'<div class="art-meta">PENDING</div></div>')
            else:
                cells.append(f'<div class="artifact missing"><div class="art-name">{name}</div>'
                             f'<div class="art-meta">MISSING</div></div>')
        html_parts.append(f'<div class="artifact-group"><div class="group-label">{group_name}</div>'
                          f'<div class="artifact-grid">{"".join(cells)}</div></div>')

    return f'<div class="section"><h2>Artifact Chain</h2>{"".join(html_parts)}</div>'


def render_review_status(reviews: dict, orch: dict) -> str:
    """Render review status. Uses orchestration.json loop verdict as primary source,
    with assessment file details as supplementary info."""
    loops = orch.get('loops', {})
    review_map = {
        'Direction': ('direction-assessment.json', 'direction'),
        'Planning': ('planning-assessment.json', 'planning'),
        'Shipping': ('shipping-assessment.json', 'shipping'),
    }

    rows = []
    for label, (filename, loop_key) in review_map.items():
        loop = loops.get(loop_key, {})
        loop_status = loop.get('status', '')
        review = reviews.get(filename)

        # Primary: orchestration.json loop verdict
        if loop_status in ('pass', 'partial'):
            css = 'pass' if loop_status == 'pass' else 'partial'
            status_label = loop_status.upper()
            cycles = loop.get('reviewCycles', 0)
            detail = f'{cycles} review cycle{"s" if cycles != 1 else ""}'
            # Supplement with assessment details if available
            if review:
                checks_total = review.get('checksTotal', 0)
                checks_passed = review.get('checksPassed', 0)
                detail += f', {checks_passed}/{checks_total} checks'
            rows.append(f'<div class="review-row"><span class="review-name">{label}</span>'
                        f'<span class="review-status {css}">{status_label}</span>'
                        f'<span class="review-detail">({detail})</span></div>')
        elif review:
            # Fallback: assessment file only (orchestration.json missing or loop in progress)
            status = review.get('status', 'unknown').upper()
            checks_total = review.get('checksTotal', 0)
            checks_passed = review.get('checksPassed', 0)
            gaps = review.get('gaps', 0)
            css = 'pass' if status == 'PASS' else 'fail'
            detail = f'{checks_passed}/{checks_total} checks'
            if gaps:
                detail += f', {gaps} gaps'
            rows.append(f'<div class="review-row"><span class="review-name">{label}</span>'
                        f'<span class="review-status {css}">{status}</span>'
                        f'<span class="review-detail">({detail})</span></div>')
        else:
            rows.append(f'<div class="review-row"><span class="review-name">{label}</span>'
                        f'<span class="review-status not-run">NOT RUN</span></div>')

    return f'<div class="section"><h2>Review Status</h2>{"".join(rows)}</div>'


def render_cost_estimate(costs: dict) -> str:
    """Render model usage counts."""
    opus = costs.get('opus', 0)
    sonnet = costs.get('sonnet', 0)
    unknown = costs.get('unknown', 0)

    rows = []
    if opus:
        rows.append(f'<div class="cost-row"><span>Opus</span><span class="num">{opus} calls</span></div>')
    if sonnet:
        rows.append(f'<div class="cost-row"><span>Sonnet</span><span class="num">{sonnet} calls</span></div>')
    if unknown:
        rows.append(f'<div class="cost-row"><span>Unknown</span><span class="num">{unknown} calls</span></div>')
    if not rows:
        return '<div class="section"><h2>Cost Estimate</h2><p class="muted">No usage data</p></div>'
    return f'<div class="section"><h2>Cost Estimate</h2>{"".join(rows)}</div>'


def render_specs_plans(scan_state: dict) -> str:
    """Render specs and plans counts."""
    specs = scan_state.get('specs', {})
    plans = scan_state.get('plans', {})
    specs_count = specs.get('count', 0)
    plans_count = plans.get('count', 0)

    return f'''<div class="section"><h2>Specs & Plans</h2>
    <div class="cost-row"><span>Specs (todo + active)</span><span class="num">{specs_count}</span></div>
    <div class="cost-row"><span>Plans (todo + active)</span><span class="num">{plans_count}</span></div></div>'''


CSS = '''
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'SF Mono', 'Cascadia Code', 'Consolas', monospace; background: #0d1117; color: #c9d1d9; padding: 20px; max-width: 900px; margin: 0 auto; }
h1 { color: #58a6ff; font-size: 18px; margin-bottom: 4px; }
.header { border-bottom: 1px solid #30363d; padding-bottom: 12px; margin-bottom: 20px; }
.header-meta { color: #8b949e; font-size: 12px; }
.section { margin-bottom: 24px; }
h2 { color: #58a6ff; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; border-bottom: 1px solid #21262d; padding-bottom: 4px; }
.muted { color: #484f58; font-style: italic; }

/* Pipeline bars */
.loop-row { display: flex; align-items: center; gap: 10px; margin-bottom: 6px; flex-wrap: wrap; }
.loop-name { width: 80px; font-weight: bold; color: #c9d1d9; }
.bar-track { width: 200px; height: 16px; background: #21262d; border-radius: 3px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 3px; transition: width 0.3s; }
.bar-pass { background: #238636; }
.bar-partial { background: #d29922; }
.bar-active { background: #1f6feb; }
.bar-pending { background: #21262d; }
.loop-label { font-size: 12px; font-weight: bold; min-width: 60px; }
.loop-meta { font-size: 11px; color: #8b949e; }
.current-skill { color: #d29922; }

/* Activity */
.status-active { color: #58a6ff; }
.status-done { color: #238636; font-weight: bold; }

/* Table */
table { width: 100%; border-collapse: collapse; font-size: 13px; }
th { text-align: left; color: #8b949e; font-weight: normal; border-bottom: 1px solid #21262d; padding: 4px 8px; }
td { padding: 4px 8px; border-bottom: 1px solid #161b22; }
.num { text-align: right; font-variant-numeric: tabular-nums; }

/* Artifacts */
.artifact-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 8px; }
.artifact { padding: 8px; border-radius: 4px; font-size: 12px; }
.artifact.ok { background: #0d2818; border: 1px solid #238636; }
.artifact.missing { background: #2d1b1b; border: 1px solid #da3633; }
.artifact.pending { background: #161b22; border: 1px solid #30363d; opacity: 0.5; }
.artifact-group { margin-bottom: 12px; }
.group-label { font-size: 11px; color: #8b949e; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
.art-name { font-weight: bold; margin-bottom: 2px; word-break: break-all; }
.art-meta { color: #8b949e; font-size: 11px; }
.art-age { color: #8b949e; font-size: 10px; }

/* Reviews */
.review-row { display: flex; align-items: center; gap: 10px; margin-bottom: 4px; }
.review-name { width: 80px; font-weight: bold; }
.review-status { font-size: 12px; font-weight: bold; padding: 1px 6px; border-radius: 3px; }
.review-status.pass { background: #238636; color: #fff; }
.review-status.partial { background: #d29922; color: #fff; }
.review-status.fail { background: #da3633; color: #fff; }
.review-status.not-run { background: #30363d; color: #8b949e; }
.review-detail { font-size: 12px; color: #8b949e; }

/* Cost */
.cost-row { display: flex; justify-content: space-between; padding: 3px 0; font-size: 13px; }
'''


def render_dashboard(orch: dict, scan_state: dict, usage: list[dict]) -> str:
    """Render the full dashboard HTML."""
    now = datetime.now().isoformat(timespec='seconds')
    status = orch.get('status') or 'unknown'
    mode = orch.get('mode') or 'unknown'
    active_loop = orch.get('activeLoop') or 'none'
    started = orch.get('startedAt', '')

    # Derive stage from goals if available
    goals = scan_state.get('goals', {})
    stage_info = goals.get('strategic.json', {})
    stage = stage_info.get('stage', '—') if stage_info else '—'

    usage_summary = summarize_skill_usage(usage)
    costs = cost_summary(usage)

    sections = [
        render_pipeline_status(orch),
        render_current_activity(orch),
        render_skill_invocations(usage_summary),
        render_artifact_chain(scan_state.get('artifacts', {}), orch),
        render_review_status(scan_state.get('reviews', {}), orch),
        render_specs_plans(scan_state),
        render_cost_estimate(costs),
    ]

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="3">
<title>Shipkit Dashboard</title>
<style>{CSS}</style>
</head>
<body>
<div class="header">
  <h1>SHIPKIT ORCHESTRATION DASHBOARD</h1>
  <div class="header-meta">
    Status: {escape(status)} | Stage: {escape(str(stage))} | Mode: {escape(mode)} | Loop: {escape(active_loop)} | Updated: {now}
  </div>
</div>
{"".join(sections)}
</body>
</html>'''


# ── Main ──────────────────────────────────────────────────────

def find_shipkit_dir() -> Path | None:
    """Walk up from cwd to find .shipkit/ directory."""
    current = Path.cwd()
    for _ in range(20):
        if (current / '.shipkit').is_dir():
            return current / '.shipkit'
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None


def get_mtimes(shipkit_dir: Path) -> dict:
    """Snapshot mtime of key files for change detection."""
    files = [
        shipkit_dir / 'orchestration.json',
    ]
    obs_dir = shipkit_dir / 'observability'
    if obs_dir.exists():
        files.extend(obs_dir.glob('skill-usage.*.local.jsonl'))
        files.append(obs_dir / 'artifact-state.json')

    mtimes = {}
    for f in files:
        if isinstance(f, Path) and f.exists():
            mtimes[str(f)] = f.stat().st_mtime
    return mtimes


def do_render(shipkit_dir: Path) -> None:
    """Run one scan + render cycle."""
    orch = load_orchestration(shipkit_dir)
    obs_dir = shipkit_dir / 'observability'
    usage = load_skill_usage(obs_dir)
    scan_state = scan(shipkit_dir)

    # Write artifact-state.json
    obs_dir.mkdir(parents=True, exist_ok=True)
    state_file = obs_dir / 'artifact-state.json'
    state_file.write_text(json.dumps(scan_state, indent=2, ensure_ascii=False), encoding='utf-8')

    # Render dashboard
    html = render_dashboard(orch, scan_state, usage)
    dash_file = obs_dir / 'dashboard.html'
    dash_file.write_text(html, encoding='utf-8')
    print(f'[{datetime.now().strftime("%H:%M:%S")}] Dashboard written to {dash_file}')


def main():
    shipkit_dir = find_shipkit_dir()
    if not shipkit_dir:
        print('No .shipkit/ directory found.')
        return 1

    watch_mode = '--watch' in sys.argv

    if not watch_mode:
        do_render(shipkit_dir)
        return 0

    # Watch mode: poll every 2s, re-render on changes
    print(f'Watching {shipkit_dir} for changes (Ctrl+C to stop)...')
    last_mtimes = {}
    while True:
        try:
            current_mtimes = get_mtimes(shipkit_dir)
            # Also re-scan artifacts periodically (they change outside tracked files)
            if current_mtimes != last_mtimes:
                do_render(shipkit_dir)
                last_mtimes = current_mtimes
            else:
                # Still re-render every 10s even without changes (artifact ages update)
                pass
            time.sleep(2)
        except KeyboardInterrupt:
            print('\nStopped.')
            return 0


if __name__ == '__main__':
    raise SystemExit(main())
