#!/usr/bin/env python3
"""
unbacked-surface-checker.py - Classify UI surfaces by how their data is backed.

Heuristic v1. Enumerates UI "surfaces" (route/page components under app/ or
pages/, and files named *Dashboard*/*Page*/*View*/*Screen*) and classifies each
surface's data source as:

    real    - imports/uses a real client, query, api, or datastore call
    mock    - references a mock seam (mockData, USE_MOCK, fake*Client, ...)
    missing - renders data (tables/charts/.map over records) but no discernible
              real source and no mock seam (a surface with nothing behind it)

Motivation (from the phinma retro): staff dashboards ran on mock data for
6-11 days before their DB views existed, and surfaces were built before their
backing API/view. This flags "surface exists, backing does not."

Precision/recall caveat: surface detection is name/path based, and "real"
detection keys off common client libs (supabase, react-query, fetch, axios,
prisma, trpc, swr). A real surface using an unusual data layer may be
mis-classified 'missing'; low-confidence findings are marked. Heuristic, not proof.

Usage:
    python unbacked-surface-checker.py <path>            # JSON (default)
    python unbacked-surface-checker.py <path> --report
    python unbacked-surface-checker.py --help
"""

import sys
import json
import argparse
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import iter_source_files, read_lines, rel  # noqa: E402

SURFACE_EXTS = {".tsx", ".jsx", ".vue", ".svelte", ".astro"}

# A file is a "surface" if under one of these dir segments...
SURFACE_DIRS = ("/app/", "/pages/", "/routes/", "/screens/", "/views/", "/dashboards/")
# ...or its basename hints at a top-level surface.
SURFACE_NAME = re.compile(r"(dashboard|page|view|screen|route)", re.I)
# Next.js/Remix route-file conventions.
ROUTE_FILE = re.compile(r"^(page|index|route|layout|\+page|\+layout)\.\w+$", re.I)

# Real backing signals.
REAL_SRC = re.compile(
    r"(supabase|createClient|\.from\(|useQuery|useMutation|useInfiniteQuery|"
    r"useSWR|\bfetch\(|axios|\bprisma\b|trpc|graphql|gql`|useLoaderData|"
    r"getServerSideProps|getStaticProps|\brpc\(|drizzle|knex|\bquery\()",
    re.I)

# Mock backing signals (mirror of mock-seam-detector's high-conf rules).
MOCK_SRC = re.compile(
    r"\b(mock[_A-Z]?\w*|MOCK_[A-Z0-9_]+|USE_MOCK|useMock|isMock|"
    r"(fake|mock|stub|dummy)\w*(client|service|api|repo|store|data|db))\b")

# Data-rendering signals (does the surface actually paint dynamic data?).
RENDERS_DATA = re.compile(
    r"(\.map\(|\.forEach\(|<[A-Z]\w*(Table|Chart|Grid|List|Card|Graph|Metric|Stat)"
    r"|dataKey=|columns\s*=|rows\s*=|\{[a-zA-Z_]\w*\.(map|length|filter)\b)")


def is_surface(path):
    p = path.as_posix()
    if path.suffix.lower() not in SURFACE_EXTS:
        return False
    if any(seg in p for seg in SURFACE_DIRS):
        return True
    if ROUTE_FILE.match(path.name):
        return True
    if SURFACE_NAME.search(path.stem):
        return True
    return False


def classify(path, root):
    text = "\n".join(read_lines(path))
    mock_hit = MOCK_SRC.search(text)
    real_hit = REAL_SRC.search(text)
    renders = RENDERS_DATA.search(text)

    if mock_hit:
        backing, conf, ev = "mock", "high", mock_hit.group(0)
    elif real_hit:
        backing, conf, ev = "real", "high", real_hit.group(0)
    elif renders:
        # renders dynamic data yet no source found -> the concerning case
        backing, conf, ev = "missing", "med", "renders data, no data-source import"
    else:
        # no source and no dynamic rendering: likely static/layout, not concerning
        backing, conf, ev = "missing", "low", "no data source and no data rendering (likely static/layout)"

    return {
        "surface": rel(path, root),
        "backing": backing,
        "confidence": conf,
        "rendersData": bool(renders),
        "evidence": ev[:160],
    }


def build_report(root):
    root = Path(root).resolve()
    surfaces = []
    for f in iter_source_files(root):
        if is_surface(f):
            surfaces.append(classify(f, root))

    counts = {"real": 0, "mock": 0, "missing": 0}
    for s in surfaces:
        counts[s["backing"]] += 1
    # concerning = mock, or missing-with-render (high-signal); low missing is soft
    concerning = [s for s in surfaces
                  if s["backing"] == "mock"
                  or (s["backing"] == "missing" and s["rendersData"])]

    return {
        "tool": "unbacked-surface-checker",
        "version": "1.0",
        "target": str(root),
        "summary": {
            "surfacesFound": len(surfaces),
            "byBacking": counts,
            "concerningCount": len(concerning),
        },
        "surfaces": surfaces,
    }


def print_report(result):
    s = result["summary"]
    print(f"unbacked-surface-checker  target={result['target']}")
    print(f"  surfaces: {s['surfacesFound']}   real={s['byBacking']['real']} "
          f"mock={s['byBacking']['mock']} missing={s['byBacking']['missing']}   "
          f"concerning={s['concerningCount']}")
    print()
    order = {"mock": 0, "missing": 1, "real": 2}
    for surf in sorted(result["surfaces"], key=lambda x: (order[x["backing"]], x["surface"])):
        print(f"  [{surf['backing']:>7} / {surf['confidence']:>4}] {surf['surface']}")
        print(f"          {surf['evidence']}")


def main():
    ap = argparse.ArgumentParser(
        description="Classify UI surfaces as real / mock / missing backing (heuristic).",
        epilog="Heuristic v1 - surface detection is name/path based; 'real' keys "
               "off common data libs. Low-confidence 'missing' (no render) is "
               "likely static, not a true gap. Findings are leads.")
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
