#!/usr/bin/env python3
"""
mock-seam-detector.py - Scan a codebase for mock/stub seams on surfaces that
are meant to be live.

Heuristic v1. Flags identifiers and patterns that indicate a surface is reading
fake/placeholder data instead of a real backend: mock data objects, fake/stub
clients, USE_MOCK-style flags, "wire this up" TODOs, coming-soon placeholders,
and hardcoded return arrays where a fetch/query is expected.

Precision/recall caveat: this is a regex heuristic. Recall is good on the common
JS/TS/Python patterns but it WILL miss cleverly-named mocks and WILL over-flag
words like "stub"/"placeholder" that appear in legitimate contexts (e.g. form
placeholder text). Treat findings as leads, not proof. Use --report for triage.

Usage:
    python mock-seam-detector.py <path>            # JSON to stdout (default)
    python mock-seam-detector.py <path> --report   # human-readable
    python mock-seam-detector.py --help
"""

import sys
import json
import argparse
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import iter_source_files, read_lines, rel  # noqa: E402

# Each rule: (seamKind, compiled regex, confidence). Ordered; first match on a
# line wins so we do not double-count the same line.
RULES = [
    ("mock-identifier",
     re.compile(r"\b(mock[_A-Z]?\w*|MOCK_[A-Z0-9_]+)\b"), "high"),
    ("fake-client",
     re.compile(r"\b(fake|mock|stub|dummy)\w*(client|service|api|repo|repository|store|db)\b", re.I), "high"),
    ("mock-flag",
     re.compile(r"\b(USE_MOCK|useMock|isMock|IS_MOCK|ENABLE_MOCK|VITE_USE_MOCK|NEXT_PUBLIC_USE_MOCK)\b"), "high"),
    ("mock-branch",
     re.compile(r"if\s*\(\s*!?\s*(mock|isMock|useMock|USE_MOCK)", re.I), "med"),
    ("stub",
     re.compile(r"\b(stub(bed|s)?)\b", re.I), "low"),
    ("todo-wire",
     re.compile(r"(TODO|FIXME|HACK|XXX)\b.{0,80}?\b(wire|live|real|hook\s*up|connect|integrat|replace\s+mock|backend|api)", re.I), "high"),
    ("placeholder",
     re.compile(r"\b(coming[\s._-]?soon|comingSoon|placeholder[_A-Z]?\w*|not[\s._-]?implemented|dummy[_A-Z]?\w*)\b", re.I), "low"),
    ("hardcoded-array",
     re.compile(r"\breturn\s*\[\s*\{"), "low"),
    ("hardcoded-const-array",
     re.compile(r"\b(const|let|var)\s+\w*(data|rows|items|list|results|records)\w*\s*=\s*\[\s*\{", re.I), "low"),
]

# Lines matching these are almost never real mock seams -> suppress low-conf noise.
SUPPRESS = re.compile(r"placeholder\s*=|placeholder:\s*[\"']|placeholderText|\.placeholder\b|input.*placeholder", re.I)


def scan_file(path, root):
    findings = []
    for i, line in enumerate(read_lines(path), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        for kind, rx, conf in RULES:
            m = rx.search(line)
            if not m:
                continue
            # Suppress the classic false positive: HTML/input placeholder attrs.
            if kind == "placeholder" and SUPPRESS.search(line):
                break
            # A bare mention inside a comment is weaker evidence than live code -
            # except todo-wire, which is *meant* to live in comments.
            eff_conf = conf
            is_comment = stripped.startswith(("//", "#", "*", "/*"))
            if is_comment and kind != "todo-wire":
                eff_conf = "low"
            findings.append({
                "file": rel(path, root),
                "line": i,
                "seamKind": kind,
                "confidence": eff_conf,
                "evidence": stripped[:160],
            })
            break  # one seamKind per line
    return findings


def build_report(root):
    root = Path(root).resolve()
    all_findings = []
    files_scanned = 0
    for f in iter_source_files(root):
        files_scanned += 1
        all_findings.extend(scan_file(f, root))

    by_kind = {}
    by_conf = {"high": 0, "med": 0, "low": 0}
    for fnd in all_findings:
        by_kind[fnd["seamKind"]] = by_kind.get(fnd["seamKind"], 0) + 1
        by_conf[fnd["confidence"]] = by_conf.get(fnd["confidence"], 0) + 1

    return {
        "tool": "mock-seam-detector",
        "version": "1.0",
        "target": str(root),
        "summary": {
            "filesScanned": files_scanned,
            "seamsFound": len(all_findings),
            "byKind": by_kind,
            "byConfidence": by_conf,
            "filesWithSeams": len({f["file"] for f in all_findings}),
        },
        "findings": all_findings,
    }


def print_report(result):
    s = result["summary"]
    print(f"mock-seam-detector  target={result['target']}")
    print(f"  files scanned: {s['filesScanned']}   seams: {s['seamsFound']}   "
          f"files with seams: {s['filesWithSeams']}")
    print(f"  by confidence: high={s['byConfidence'].get('high',0)} "
          f"med={s['byConfidence'].get('med',0)} low={s['byConfidence'].get('low',0)}")
    print("  by kind: " + ", ".join(f"{k}={v}" for k, v in sorted(s["byKind"].items())) or "  (none)")
    print()
    for f in result["findings"]:
        print(f"  [{f['confidence']:>4}] {f['seamKind']:<20} {f['file']}:{f['line']}")
        print(f"         {f['evidence']}")


def main():
    ap = argparse.ArgumentParser(
        description="Detect mock/stub seams in a codebase (heuristic).",
        epilog="Heuristic v1 - good recall on common patterns, expect some "
               "false positives (esp. 'stub'/'placeholder'). Findings are leads.")
    ap.add_argument("path", help="Path to the target codebase")
    ap.add_argument("--report", action="store_true", help="Human-readable output")
    ap.add_argument("--json", action="store_true", help="Force JSON (default)")
    args = ap.parse_args()

    root = Path(args.path)
    if not root.exists():
        print(f"error: path not found: {root}", file=sys.stderr)
        sys.exit(2)

    result = build_report(root)
    if args.report and not args.json:
        print_report(result)
    else:
        print(json.dumps(result, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
