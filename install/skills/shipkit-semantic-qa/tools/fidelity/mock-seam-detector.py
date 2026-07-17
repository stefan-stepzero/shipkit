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

DECLARED-LIVE CROSS-CHECK (--spec)
----------------------------------
A mock seam is only "green-but-mock" if it sits on a surface the spec DECLARES
LIVE. Pass `--spec` and every finding gains `declaredLive` + the `surface` it was
tied to; the summary counts them separately. Without `--spec` the tool cannot
know what was declared, so every finding carries `declaredLive: null` ("unknown",
not "no") and the raw regex read is all you get.

This is the precision fix: seams in fixtures, scratch files, and undeclared code
are exactly the false positives that put v1 at ~27-30% precision. They now come
back `declaredLive: false` and stop dragging the score, while still being listed
as advisory. Fail-open by design - see `_declared.py`.

Usage:
    python mock-seam-detector.py <path>            # JSON to stdout (default)
    python mock-seam-detector.py <path> --report   # human-readable
    python mock-seam-detector.py <path> --spec .shipkit/specs/shipped/*.json
    python mock-seam-detector.py <path> --spec S.json --declared-live-only
    python mock-seam-detector.py --help
"""

import sys
import json
import argparse
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import iter_source_files, read_lines, rel  # noqa: E402
from _declared import load_declared, classify_file  # noqa: E402

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


def scan_file(path, root, declared=None):
    findings = []
    lines = read_lines(path)
    relpath = rel(path, root)

    # Tie the FILE to the declared list once, not per finding: the surface a seam
    # sits on is a property of the file, and matching is the expensive part.
    if declared is None:
        tie = {"declaredLive": None, "surface": None, "dimension": None,
               "matchEvidence": "no --spec given; declared-live is unknown"}
    else:
        tie = classify_file(relpath, "\n".join(lines), declared)

    for i, line in enumerate(lines, start=1):
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
                "file": relpath,
                "line": i,
                "seamKind": kind,
                "confidence": eff_conf,
                "evidence": stripped[:160],
                # Declared-live cross-check (null when no --spec was given).
                "surface": tie["surface"],
                "declaredLive": tie["declaredLive"],
                "declaredMatch": tie["matchEvidence"],
            })
            break  # one seamKind per line
    return findings


def build_report(root, declared=None, declared_live_only=False):
    root = Path(root).resolve()
    all_findings = []
    files_scanned = 0
    for f in iter_source_files(root):
        files_scanned += 1
        all_findings.extend(scan_file(f, root, declared))

    if declared_live_only:
        all_findings = [f for f in all_findings if f["declaredLive"]]

    by_kind = {}
    by_conf = {"high": 0, "med": 0, "low": 0}
    for fnd in all_findings:
        by_kind[fnd["seamKind"]] = by_kind.get(fnd["seamKind"], 0) + 1
        by_conf[fnd["confidence"]] = by_conf.get(fnd["confidence"], 0) + 1

    # The gate-relevant population: high/med-confidence seams on declared-live
    # surfaces. This is what "green-but-mock" means; everything else is advisory.
    declared_live = [f for f in all_findings if f["declaredLive"]]
    gating = [f for f in declared_live if f["confidence"] in ("high", "med")]

    summary = {
        "filesScanned": files_scanned,
        "seamsFound": len(all_findings),
        "byKind": by_kind,
        "byConfidence": by_conf,
        "filesWithSeams": len({f["file"] for f in all_findings}),
        "declaredLiveSeams": len(declared_live),
        "gatingSeams": len(gating),
        "declaredLiveSurfaces": sorted({f["surface"] for f in declared_live if f["surface"]}),
    }

    return {
        "tool": "mock-seam-detector",
        "version": "2.0",
        "target": str(root),
        "declaredSource": {
            "specs": (declared or {}).get("specs", []),
            "declaredElements": len((declared or {}).get("elements", [])),
            "errors": (declared or {}).get("errors", []),
        } if declared else None,
        "summary": summary,
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
    ds = result.get("declaredSource")
    if ds:
        print(f"  declared from: {len(ds['specs'])} spec(s), "
              f"{ds['declaredElements']} declared-live elements")
        print(f"  GATING (declared-live, high/med): {s['gatingSeams']}   "
              f"declared-live seams: {s['declaredLiveSeams']}   "
              f"advisory (undeclared): {s['seamsFound'] - s['declaredLiveSeams']}")
        for e in ds.get("errors") or []:
            print(f"  ! spec unreadable: {e['spec']}: {e['error']}")
    else:
        print("  declared-live: UNKNOWN (no --spec) - all findings are raw regex leads")
    print()
    # Gating seams first: they are the ones that actually fail a build.
    order = {"high": 0, "med": 1, "low": 2}
    for f in sorted(result["findings"],
                    key=lambda x: (not x["declaredLive"], order[x["confidence"]], x["file"])):
        flag = "LIVE" if f["declaredLive"] else ("----" if f["declaredLive"] is False else " ?? ")
        print(f"  [{flag}][{f['confidence']:>4}] {f['seamKind']:<20} {f['file']}:{f['line']}")
        print(f"         {f['evidence']}")
        if f["surface"]:
            print(f"         -> declared surface: {f['surface']}")


def main():
    ap = argparse.ArgumentParser(
        description="Detect mock/stub seams in a codebase (heuristic), "
                    "cross-checked against the spec's declared-live surfaces.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Heuristic - good recall on common patterns, expect some false\n"
            "positives (esp. 'stub'/'placeholder'). Findings are leads.\n\n"
            "--spec is what makes this a GATE rather than a grep: a seam only\n"
            "means green-but-mock if it sits on a surface the spec declares LIVE\n"
            "(functionalSurface, verdict COVERED, not deferred/wontHave).\n"
            "Unmatched seams fail OPEN (declaredLive false, advisory only).\n"
            "Without --spec, declaredLive is null = unknown, never false."
        ))
    ap.add_argument("path", help="Path to the target codebase")
    ap.add_argument("--report", action="store_true", help="Human-readable output")
    ap.add_argument("--json", action="store_true", help="Force JSON (default)")
    ap.add_argument("--spec", nargs="+", default=None, metavar="SPEC",
                    help="Spec artifact(s) declaring the live surfaces "
                         "(.shipkit/specs/**/*.json). Enables the declaredLive "
                         "cross-check.")
    ap.add_argument("--declared-live-only", action="store_true",
                    help="Emit only seams on declared-live surfaces (needs --spec)")
    args = ap.parse_args()

    root = Path(args.path)
    if not root.exists():
        print(f"error: path not found: {root}", file=sys.stderr)
        sys.exit(2)

    if args.declared_live_only and not args.spec:
        print("error: --declared-live-only requires --spec", file=sys.stderr)
        sys.exit(2)

    declared = load_declared(args.spec) if args.spec else None
    if declared and not declared["elements"]:
        print("warning: no COVERED functionalSurface elements found in the given "
              "spec(s) - every seam will fail open to declaredLive=false",
              file=sys.stderr)

    result = build_report(root, declared, args.declared_live_only)
    if args.report and not args.json:
        print_report(result)
    else:
        print(json.dumps(result, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
