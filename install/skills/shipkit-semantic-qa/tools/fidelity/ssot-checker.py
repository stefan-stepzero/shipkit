#!/usr/bin/env python3
"""
ssot-checker.py - Find shared fields/metrics computed in more than one place.

Heuristic v1. Single-source-of-truth risk detector. Scans for fields/metrics
that are *derived* (computed via arithmetic, comparison-banding, ternary,
reduce/filter/map, Math.*, or switch) and reports any field name that is
computed in >1 file. A metric derived independently in several files is a
duplication-of-truth risk: the definitions drift.

Motivation (from a real-project retrospective): `grade_band` was implemented independently
on 4+ surfaces before late unification; a mastery metric was shown via the wrong
field on 3 staff surfaces. Both are "same metric, computed N times" -> exactly
what this flags.

Precision/recall caveat: this keys off assignment/derivation syntax, so it finds
where a field is COMPUTED, not merely read. It cannot know two computations are
semantically the same metric - it matches on field NAME. Expect false positives
for generic names (suppressed via a stop-list) and misses where the same metric
uses different names on each surface. Heuristic, not proof.

Usage:
    python ssot-checker.py <path>            # JSON (default)
    python ssot-checker.py <path> --report
    python ssot-checker.py <path> --min-files 3
    python ssot-checker.py --help
"""

import sys
import json
import argparse
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import iter_source_files, read_lines, rel  # noqa: E402

# Assignment or object-property that binds a field to an expression.
#   fieldName = <rhs>     |     fieldName: <rhs>
ASSIGN = re.compile(r"\b([a-zA-Z_][a-zA-Z0-9_]{3,})\s*[:=]\s*(?![=:])(.+)")

# The RHS counts as a *derivation* (not a plain literal/passthrough) if it
# contains computation. Comparison operators catch "banding" logic (grade_band).
DERIVED = re.compile(
    r"(\?.*:|[-+*/%]\s*\w|<=?|>=?|===|!==|\.reduce\(|\.filter\(|\.map\(|"
    r"Math\.|Number\(|parseFloat|parseInt|\bswitch\b|\bcase\b|"
    r"\bif\b.*\belse\b|\bfloor\b|\bround\b|\bceil\b|\bsum\b|\bavg\b|\bmean\b)")

# Common names that are noise, not metrics.
STOP = {
    "data", "result", "results", "value", "values", "props", "state", "style",
    "styles", "className", "children", "index", "count", "item", "items", "list",
    "name", "names", "type", "types", "error", "errors", "response", "request",
    "config", "options", "params", "query", "queries", "body", "header", "headers",
    "content", "message", "status", "label", "labels", "title", "color", "colors",
    "width", "height", "size", "length", "total", "current", "next", "prev",
    "return", "const", "await", "async", "function", "export", "import", "default",
    "class", "true", "false", "null", "undefined", "this", "self", "props",
}

# A field name is "metric-like" if snake_case or contains a metric-ish word,
# which sharpens precision toward the domain metrics we care about.
METRIC_HINT = re.compile(
    r"(_|band|score|rate|pct|percent|ratio|avg|mean|total|sum|count|mastery|"
    r"grade|level|rank|progress|pace|completion|streak|delta|index|metric|"
    r"weight|threshold|status|tier)", re.I)


def scan_file(path, root):
    """Return {field: [(line, evidence)]} of derivation sites in one file."""
    sites = {}
    for i, raw in enumerate(read_lines(path), start=1):
        line = raw.strip()
        if not line or line.startswith(("//", "#", "*", "/*")):
            continue
        m = ASSIGN.search(line)
        if not m:
            continue
        field, rhs = m.group(1), m.group(2)
        low = field.lower()
        if low in STOP or len(field) < 4:
            continue
        if not METRIC_HINT.search(field):
            continue
        if not DERIVED.search(rhs):
            continue
        sites.setdefault(field, []).append((i, line[:160]))
    return sites


def build_report(root, min_files):
    root = Path(root).resolve()
    # field -> {relfile -> [(line, evidence)]}
    field_map = {}
    files_scanned = 0
    for f in iter_source_files(root):
        files_scanned += 1
        r = rel(f, root)
        for field, hits in scan_file(f, root).items():
            field_map.setdefault(field, {}).setdefault(r, []).extend(hits)

    violations = []
    for field, per_file in field_map.items():
        if len(per_file) < min_files:
            continue
        sites = []
        for relfile, hits in sorted(per_file.items()):
            for line, ev in hits:
                sites.append({"file": relfile, "line": line, "evidence": ev})
        n_files = len(per_file)
        risk = "high" if n_files >= 3 else "med"
        violations.append({
            "field": field,
            "fileCount": n_files,
            "siteCount": len(sites),
            "risk": risk,
            "sites": sites,
        })

    violations.sort(key=lambda v: (-v["fileCount"], v["field"]))
    return {
        "tool": "ssot-checker",
        "version": "1.0",
        "target": str(root),
        "minFiles": min_files,
        "summary": {
            "filesScanned": files_scanned,
            "violations": len(violations),
            "highRisk": sum(1 for v in violations if v["risk"] == "high"),
        },
        "violations": violations,
    }


def print_report(result):
    s = result["summary"]
    print(f"ssot-checker  target={result['target']}  (min-files={result['minFiles']})")
    print(f"  files scanned: {s['filesScanned']}   violations: {s['violations']}   "
          f"high-risk: {s['highRisk']}")
    print()
    for v in result["violations"]:
        print(f"  [{v['risk']:>4}] {v['field']}  "
              f"(computed in {v['fileCount']} files, {v['siteCount']} sites)")
        for site in v["sites"]:
            print(f"         {site['file']}:{site['line']}  {site['evidence']}")
        print()


def main():
    ap = argparse.ArgumentParser(
        description="Find shared fields/metrics computed in >1 file (SSOT risk, heuristic).",
        epilog="Heuristic v1 - matches on field NAME + derivation syntax. Cannot "
               "prove two computations are the same metric, and misses same-metric/"
               "different-name cases. Findings are leads.")
    ap.add_argument("path", help="Path to the target codebase")
    ap.add_argument("--report", action="store_true", help="Human-readable output")
    ap.add_argument("--json", action="store_true", help="Force JSON (default)")
    ap.add_argument("--min-files", type=int, default=2,
                    help="Min distinct files a field must be computed in to flag (default 2)")
    args = ap.parse_args()

    root = Path(args.path)
    if not root.exists():
        print(f"error: path not found: {root}", file=sys.stderr)
        sys.exit(2)

    result = build_report(root, args.min_files)
    if args.report and not args.json:
        print_report(result)
    else:
        print(json.dumps(result, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
