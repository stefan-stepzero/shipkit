#!/usr/bin/env python3
"""
Shipkit - Artifact Scanner

Scans .shipkit/ filesystem and builds a state snapshot for the dashboard.
Can be run standalone or imported by watch.py.
"""

import json
import os
from pathlib import Path
from datetime import datetime


def format_age(mtime: float) -> str:
    """Format file age as human-readable string."""
    delta = datetime.now().timestamp() - mtime
    if delta < 60:
        return f"{int(delta)}s ago"
    if delta < 3600:
        return f"{int(delta / 60)}m ago"
    if delta < 86400:
        return f"{int(delta / 3600)}h ago"
    return f"{int(delta / 86400)}d ago"


def scan_file(path: Path) -> dict:
    """Get metadata for a single file."""
    if not path.exists():
        return {"exists": False}
    stat = path.stat()
    return {
        "exists": True,
        "size": stat.st_size,
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(timespec='seconds'),
        "age": format_age(stat.st_mtime),
    }


def scan_review(path: Path) -> dict | None:
    """Extract review summary from an assessment JSON."""
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
        checks = data.get('coherenceChecks', data.get('checks', []))
        gaps = data.get('gaps', [])
        prev_gaps = data.get('previousGaps', [])
        return {
            "status": data.get('status', 'unknown'),
            "checksTotal": len(checks),
            "checksPassed": sum(1 for c in checks if c.get('result', c.get('status')) == 'pass'),
            "gaps": len(gaps),
            "previousGapsResolved": sum(1 for g in prev_gaps if g.get('status') == 'resolved'),
        }
    except (json.JSONDecodeError, IOError):
        return {"status": "error", "checksTotal": 0, "checksPassed": 0, "gaps": 0}


def scan_goals(path: Path) -> dict | None:
    """Extract goal summary from a goals JSON."""
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
        criteria = data.get('criteria', [])
        result = {"criteriaCount": len(criteria)}
        stage = data.get('stage', {})
        if isinstance(stage, dict):
            result["stage"] = stage.get('current', stage.get('name'))
        elif isinstance(stage, str):
            result["stage"] = stage
        return result
    except (json.JSONDecodeError, IOError):
        return None


def scan_dir_count(dir_path: Path, pattern: str = '*.json') -> dict:
    """Count files in a directory."""
    if not dir_path.exists():
        return {"count": 0, "files": []}
    files = sorted(f.name for f in dir_path.glob(pattern))
    return {"count": len(files), "files": files}


def scan(shipkit_dir: Path) -> dict:
    """Full scan of .shipkit/ directory. Returns state snapshot."""
    now = datetime.now().isoformat(timespec='seconds')

    # Core artifacts
    core_files = [
        'why.json', 'vision.json', 'product-discovery.json',
        'product-definition.json', 'engineering-definition.json',
        'stack.json', 'architecture.json', 'codebase-index.json',
        'progress.json', 'spec-roadmap.json', 'orchestration.json',
    ]
    artifacts = {}
    for name in core_files:
        artifacts[name] = scan_file(shipkit_dir / name)

    # Reviews
    reviews = {}
    reviews_dir = shipkit_dir / 'reviews'
    if reviews_dir.exists():
        for f in reviews_dir.glob('*.json'):
            reviews[f.name] = scan_review(f)

    # Goals
    goals = {}
    goals_dir = shipkit_dir / 'goals'
    if goals_dir.exists():
        for f in goals_dir.glob('*.json'):
            goals[f.name] = scan_goals(f)

    # Specs and plans (check both todo/ and active/)
    specs = {"count": 0, "files": []}
    for sub in ['todo', 'active']:
        result = scan_dir_count(shipkit_dir / 'specs' / sub)
        specs["count"] += result["count"]
        specs["files"].extend(result["files"])

    plans = {"count": 0, "files": []}
    for sub in ['todo', 'active']:
        result = scan_dir_count(shipkit_dir / 'plans' / sub)
        plans["count"] += result["count"]
        plans["files"].extend(result["files"])

    return {
        "scannedAt": now,
        "artifacts": artifacts,
        "reviews": reviews,
        "goals": goals,
        "specs": specs,
        "plans": plans,
    }


def main():
    """Run scan and write artifact-state.json."""
    # Find .shipkit/ — walk up from cwd
    cwd = Path.cwd()
    shipkit_dir = None
    current = cwd
    for _ in range(20):
        if (current / '.shipkit').is_dir():
            shipkit_dir = current / '.shipkit'
            break
        parent = current.parent
        if parent == current:
            break
        current = parent

    if not shipkit_dir:
        print("No .shipkit/ directory found.")
        return 1

    state = scan(shipkit_dir)

    obs_dir = shipkit_dir / 'observability'
    obs_dir.mkdir(parents=True, exist_ok=True)

    out_file = obs_dir / 'artifact-state.json'
    out_file.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"Scan written to {out_file}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
