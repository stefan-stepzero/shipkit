#!/usr/bin/env python3
"""
fidelity-score.py - Compose the P1 completeness checkers into a fidelity
scorecard (the COMPLETENESS axis of the two-axis fidelity fitness function).

This is the Phase-2 scorecard composer. It runs the three deterministic P1
checkers against a target codebase and folds their findings into a single,
transparent completeness read, broken down byDimension (surfaces / seams / ssot).
The essence axis (Phase 3) is left as a null slot for a later LLM judge to fill.

--------------------------------------------------------------------------------
HOW COMPLETENESS IS COMPUTED (no hidden magic weights)
--------------------------------------------------------------------------------
Completeness is a weighted blend of three dimension scores, each in [0,1]:

  1. surfaces  (PRIMARY - the "builtAndBacked / declaredSurfaces" ratio)
       declaredDataSurfaces = surfaces the checker says SHOULD carry data
                              = backing in {real, mock} OR (missing AND rendersData).
                              (A low-confidence 'missing' surface that renders NO
                              data is static/layout - it has no data fidelity to
                              measure, so it is excluded from the denominator, not
                              counted as a gap.)
       backedSurfaces       = surfaces classified 'real'.
       surfacesScore        = backedSurfaces / declaredDataSurfaces
                              (1.0 when there are no data surfaces).
       -> mock and missing-with-render surfaces count as NOT backed: they drag
          the score down. This IS the spec's builtAndBacked/declared ratio.

  2. seams     (RISK FLAG - mock-seam density, HIGH-confidence only)
       filesWithHighConfSeams = distinct files with >=1 high-confidence mock seam.
       seamsScore = (filesScanned - filesWithHighConfSeams) / filesScanned
                    (1.0 when nothing was scanned).
       -> only HIGH-confidence seams subtract; low/med seams are listed as advisory
          but do not move the score (they are the checker's known noisy classes).

  3. ssot      (RISK FLAG - duplicated-truth violations)
       weightedViolations = (highRisk count * 1.0) + (medRisk count * 0.5)
       ssotScore = 1 / (1 + weightedViolations)
       -> monotonic decay: 0 violations -> 1.0; one med -> 0.667; grows harder to
          push down as violations pile up. No arbitrary denominator.

  OVERALL:
       weights = { surfaces: 0.70, seams: 0.15, ssot: 0.15 }   (emitted explicitly)
       score   = surfacesScore*0.70 + seamsScore*0.15 + ssotScore*0.15
       Rationale (deliberate, not hidden): completeness is FUNDAMENTALLY the backed-
       surface ratio, so surfaces dominates. Seams and SSOT are integrity RISK FLAGS
       that shave the score but must not dominate it. The weights are emitted in the
       JSON (`completeness.weights`) so the blend is fully auditable.

  fidelityVerdict (COMPLETENESS SIGNAL ONLY - essence axis is still pending):
       FAITHFUL   if there are zero unbacked surfaces (no mock, no missing-render)
                  AND zero high-confidence seams AND zero high-risk SSOT violations.
       GAP-DRIFT  otherwise (any unbacked/mock surface, high-conf seam, or high-risk
                  duplication). The fixture and phinma both land here.
       NOTE: essence is null until Phase 3, so a FAITHFUL here means "complete",
       not yet "faithful to the vision". verdictBasis records this.

--------------------------------------------------------------------------------
Usage:
    python fidelity-score.py <path>                 # JSON scorecard (default)
    python fidelity-score.py <path> --report        # human-readable
    python fidelity-score.py <path> --stamp 2026-07-03T00:00:00Z
    python fidelity-score.py <path> --out fidelity-scorecard.json
    python fidelity-score.py --help

Deterministic: no datetime.now() at import or run time. `generatedAt` is null
unless you pass --stamp, so repeated runs on an unchanged tree are byte-identical.
Exit 0 on a clean run, 2 on a bad path.
"""

import sys
import json
import argparse
import importlib.util
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))


def _load_checker(filename):
    """Import a hyphen-named checker module by file path and return it."""
    mod_name = "fidelity_checker_" + filename.replace("-", "_").replace(".py", "")
    spec = importlib.util.spec_from_file_location(mod_name, _HERE / filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# Explicit, auditable dimension weights (see module docstring).
WEIGHTS = {"surfaces": 0.70, "seams": 0.15, "ssot": 0.15}


def _round(x, n=3):
    return round(x + 0.0, n)


def compute_surfaces(unbacked_report):
    """surfaces dimension: builtAndBacked / declaredDataSurfaces."""
    surfaces = unbacked_report["surfaces"]
    # Surfaces that SHOULD carry data (exclude static/layout: missing + no render).
    data_surfaces = [
        s for s in surfaces
        if s["backing"] in ("real", "mock")
        or (s["backing"] == "missing" and s["rendersData"])
    ]
    backed = [s for s in data_surfaces if s["backing"] == "real"]
    unbacked = [s for s in data_surfaces if s["backing"] != "real"]
    declared = len(data_surfaces)
    score = (len(backed) / declared) if declared else 1.0
    dim = {
        "score": _round(score),
        "weight": WEIGHTS["surfaces"],
        "declaredDataSurfaces": declared,
        "backedSurfaces": len(backed),
        "unbackedSurfaces": len(unbacked),
        "formula": "backedSurfaces / declaredDataSurfaces (mock+missing-render = not backed; static excluded)",
    }
    findings = [
        {
            "surface": s["surface"],
            "backing": s["backing"],
            "confidence": s["confidence"],
            "rendersData": s["rendersData"],
            "evidence": s["evidence"],
        }
        for s in sorted(unbacked, key=lambda x: (x["backing"], x["surface"]))
    ]
    return dim, findings


def compute_seams(mock_report):
    """seams dimension: fraction of files free of HIGH-confidence mock seams."""
    findings = mock_report["findings"]
    files_scanned = mock_report["summary"]["filesScanned"]
    high = [f for f in findings if f["confidence"] == "high"]
    files_with_high = {f["file"] for f in high}
    score = ((files_scanned - len(files_with_high)) / files_scanned) if files_scanned else 1.0
    dim = {
        "score": _round(score),
        "weight": WEIGHTS["seams"],
        "filesScanned": files_scanned,
        "filesWithHighConfSeams": len(files_with_high),
        "highConfSeams": len(high),
        "totalSeams": len(findings),
        "formula": "(filesScanned - filesWithHighConfSeams) / filesScanned (only high-confidence seams subtract)",
    }
    # Emit high + med seams as the signal (drop low-confidence noise from the card).
    emitted = [
        {
            "file": f["file"],
            "line": f["line"],
            "seamKind": f["seamKind"],
            "confidence": f["confidence"],
            "evidence": f["evidence"],
        }
        for f in findings if f["confidence"] in ("high", "med")
    ]
    return dim, emitted


def compute_ssot(ssot_report):
    """ssot dimension: 1 / (1 + weightedViolations)."""
    violations = ssot_report["violations"]
    high = sum(1 for v in violations if v["risk"] == "high")
    med = sum(1 for v in violations if v["risk"] == "med")
    weighted = high * 1.0 + med * 0.5
    score = 1.0 / (1.0 + weighted)
    dim = {
        "score": _round(score),
        "weight": WEIGHTS["ssot"],
        "violations": len(violations),
        "highRisk": high,
        "medRisk": med,
        "weightedViolations": _round(weighted, 2),
        "formula": "1 / (1 + weightedViolations); weightedViolations = high*1.0 + med*0.5",
    }
    return dim, violations


def build_scorecard(root, stamp=None, ssot_min_files=2):
    root = Path(root).resolve()

    mock_mod = _load_checker("mock-seam-detector.py")
    unbacked_mod = _load_checker("unbacked-surface-checker.py")
    ssot_mod = _load_checker("ssot-checker.py")

    mock_report = mock_mod.build_report(root)
    unbacked_report = unbacked_mod.build_report(root)
    ssot_report = ssot_mod.build_report(root, ssot_min_files)

    surf_dim, unbacked_surfaces = compute_surfaces(unbacked_report)
    seam_dim, mock_seams = compute_seams(mock_report)
    ssot_dim, ssot_violations = compute_ssot(ssot_report)

    score = (
        surf_dim["score"] * WEIGHTS["surfaces"]
        + seam_dim["score"] * WEIGHTS["seams"]
        + ssot_dim["score"] * WEIGHTS["ssot"]
    )
    score = _round(score)

    # Verdict from the completeness signal alone (essence pending Phase 3).
    clean = (
        surf_dim["unbackedSurfaces"] == 0
        and seam_dim["filesWithHighConfSeams"] == 0
        and ssot_dim["highRisk"] == 0
    )
    verdict = "FAITHFUL" if clean else "GAP-DRIFT"

    return {
        "tool": "fidelity-score",
        "version": "1.0",
        "target": str(root),
        "generatedAt": stamp,  # null unless --stamp; never datetime.now()
        "completeness": {
            "score": score,
            "weights": WEIGHTS,
            "byDimension": {
                "surfaces": surf_dim,
                "seams": seam_dim,
                "ssot": ssot_dim,
            },
            "unbackedSurfaces": unbacked_surfaces,
            "mockSeams": mock_seams,
            "ssotViolations": ssot_violations,
        },
        "essence": None,  # Phase 3 (LLM essence judge) fills this
        "fidelityVerdict": verdict,
        "verdictBasis": "completeness-only; essence axis pending (Phase 3). "
                        "A FAITHFUL verdict here means 'complete', not yet "
                        "'faithful to the captured vision'.",
    }


def print_report(sc):
    c = sc["completeness"]
    d = c["byDimension"]
    print(f"fidelity-score  target={sc['target']}")
    print(f"  generatedAt: {sc['generatedAt']}")
    print()
    print(f"  COMPLETENESS: {c['score']:.3f}    VERDICT: {sc['fidelityVerdict']}")
    print(f"  (essence axis: pending Phase 3)")
    print()
    print("  byDimension (score x weight):")
    for name in ("surfaces", "seams", "ssot"):
        dim = d[name]
        contrib = dim["score"] * dim["weight"]
        print(f"    {name:<9} {dim['score']:.3f} x {dim['weight']:.2f} = {contrib:.3f}")
    print()
    s = d["surfaces"]
    print(f"  surfaces: {s['backedSurfaces']}/{s['declaredDataSurfaces']} backed "
          f"({s['unbackedSurfaces']} unbacked)")
    sm = d["seams"]
    print(f"  seams:    {sm['filesWithHighConfSeams']}/{sm['filesScanned']} files with "
          f"high-conf seams ({sm['highConfSeams']} high-conf, {sm['totalSeams']} total)")
    ss = d["ssot"]
    print(f"  ssot:     {ss['violations']} violations "
          f"(high={ss['highRisk']}, med={ss['medRisk']})")
    print()
    if c["unbackedSurfaces"]:
        print("  UNBACKED SURFACES:")
        for u in c["unbackedSurfaces"]:
            print(f"    [{u['backing']:>7}] {u['surface']}  ({u['evidence']})")
    if c["mockSeams"]:
        print("  MOCK SEAMS (high/med):")
        for m in c["mockSeams"]:
            print(f"    [{m['confidence']:>4}] {m['seamKind']:<18} {m['file']}:{m['line']}")
    if c["ssotViolations"]:
        print("  SSOT VIOLATIONS:")
        for v in c["ssotViolations"]:
            print(f"    [{v['risk']:>4}] {v['field']} (in {v['fileCount']} files)")


def main():
    ap = argparse.ArgumentParser(
        description="Compose the P1 checkers into a fidelity scorecard "
                    "(completeness axis).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "COMPLETENESS FORMULA (transparent, weights emitted in JSON):\n"
            "  score = surfaces*0.70 + seams*0.15 + ssot*0.15\n"
            "  surfaces = backedSurfaces / declaredDataSurfaces "
            "(mock+missing-render = not backed; static/layout excluded)\n"
            "  seams    = (filesScanned - filesWithHighConfSeams) / filesScanned "
            "(only high-conf seams subtract)\n"
            "  ssot     = 1 / (1 + weightedViolations), weighted = high*1.0 + med*0.5\n"
            "  verdict  = FAITHFUL if no unbacked surfaces + no high-conf seams + "
            "no high-risk ssot, else GAP-DRIFT (completeness-only; essence pending).\n"
            "Deterministic: generatedAt is null unless --stamp is passed."
        ),
    )
    ap.add_argument("path", help="Path to the target codebase")
    ap.add_argument("--report", action="store_true", help="Human-readable output")
    ap.add_argument("--json", action="store_true", help="Force JSON (default)")
    ap.add_argument("--stamp", default=None,
                    help="Value for generatedAt (e.g. an ISO timestamp). "
                         "Omitted = null, keeping runs deterministic.")
    ap.add_argument("--ssot-min-files", type=int, default=2,
                    help="Min distinct files for an SSOT violation (default 2)")
    ap.add_argument("--out", default=None,
                    help="Also write the JSON scorecard to this path")
    args = ap.parse_args()

    root = Path(args.path)
    if not root.exists():
        print(f"error: path not found: {root}", file=sys.stderr)
        sys.exit(2)

    scorecard = build_scorecard(root, stamp=args.stamp,
                                ssot_min_files=args.ssot_min_files)

    payload = json.dumps(scorecard, indent=2)
    if args.out:
        Path(args.out).write_text(payload + "\n", encoding="utf-8")

    if args.report and not args.json:
        print_report(scorecard)
        if args.out:
            print(f"\n  (JSON written to {args.out})")
    else:
        print(payload)
    sys.exit(0)


if __name__ == "__main__":
    main()
