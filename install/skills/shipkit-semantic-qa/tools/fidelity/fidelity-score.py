#!/usr/bin/env python3
"""
fidelity-score.py - Emit the fidelity scorecard defined by
`references/fidelity-scorecard-schema.md`. That schema is THE contract; this tool
is its deterministic producer.

The scorecard scores a BUILT app against the INTENT THAT WAS CAPTURED, on two
axes that are never blended into one number that hides a failure:

  completeness  deterministic, no LLM  <- this tool computes it
  essence       LLM judge              <- semantic-qa fills it (null slot here)

--------------------------------------------------------------------------------
AXIS 1 - COMPLETENESS (the contract formula, verbatim from the schema)
--------------------------------------------------------------------------------
    D              = count of functionalSurface elements across all four
                     dimensions with verdict == "COVERED"
                     (EXPLICITLY-DEFERRED and FLAGGED excluded: deferred is out
                      of scope on purpose; flagged means the spec gate never
                      cleared, so it was never a declared-live surface)

    notBacked      = distinct surfaces that are EITHER
                       - listed in gapReport.unbackedSurfaces[], OR
                       - the surface of a mockSeams[] entry with declaredLive
                         == true (built, but still reading mock/stub data)

    builtAndBacked = D - |notBacked|
    ratio          = builtAndBacked / D          (D == 0 -> "n/a", state why)

The denominator is the DECLARED list, read from the spec - not a code re-scan.
That is the whole point: the spec is the authority on what the build was asked to
deliver, so the tool can never invent a denominator out of whatever files its
regexes tripped on.

This formula is deliberately OPTIMISTIC and it is worth being explicit about it:
an element declared but ABSENT from the code entirely is not caught here - only
surfaces that a seam or an unbackedSurfaces entry NAMES count against the ratio.
Proving "declared element X does not exist anywhere in this codebase" from a name
like "web-ui" is exactly where false positives are manufactured, so the contract
does not ask for it. The heuristic read that DOES look for absent surfaces lives
under `completeness.signals` (below) as ADVISORY - it never moves the ratio.

--------------------------------------------------------------------------------
completeness.signals - the heuristic read (advisory, never gating)
--------------------------------------------------------------------------------
The v1 tool scored a blend of surfaces*0.70 + seams*0.15 + ssot*0.15 computed
from a code re-scan, and called that "completeness". It is not the contract's
completeness, and it measured ~27-30% precision against ground truth. It is kept
- unchanged and fully auditable - as `completeness.signals`, because it does
surface things the contract's formula structurally cannot (a surface with no
backing at all, duplicated truth). Weights are still emitted, never hidden.

Read them as leads for a human, not as a score. `signals.*.score` never
contributes to `ratio` or to `fidelityVerdict`.

--------------------------------------------------------------------------------
VERDICT - derived, never entered by hand
--------------------------------------------------------------------------------
    FAITHFUL         ratio == 1.0 and floorHeld and essenceScore >= threshold
    GAP-DRIFT        ratio < 1.0
    TASTE-DRIFT      floorHeld == false or essenceScore < threshold
    GAP+TASTE-DRIFT  both

Without essence, the verdict is only PARTLY decidable, and this tool will not
guess the rest:
  - ratio < 1.0  -> gap-drift is certain, but GAP-DRIFT vs GAP+TASTE-DRIFT is not
  - ratio == 1.0 -> FAITHFUL vs TASTE-DRIFT is entirely an essence question
So `fidelityVerdict` is null unless `--essence` supplies the other axis, and
`completeness.verdict` carries the half this tool can actually prove. Pass
`--essence` and the rule table above is applied in code - the schema says the
verdict is derived and never entered by hand, so it is derived here rather than
recomputed in prose by whatever reads this.

Usage:
    fidelity-score.py <path> --spec .shipkit/specs/shipped/*.json
    fidelity-score.py <path> --spec S.json --verification-report vr.json
    fidelity-score.py <path> --spec S.json --product-definition pd.json
    fidelity-score.py <path> --spec S.json --essence essence.json --report
    fidelity-score.py --arm shipkit=../arm-shipkit --arm raw=../arm-raw --spec S.json
    fidelity-score.py --help

Deterministic: no datetime.now(). `lastUpdated` is null unless --stamp is passed,
so repeated runs on an unchanged tree are byte-identical. Exit 0 clean, 2 bad input.
"""

import sys
import json
import argparse
import importlib.util
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from _declared import load_declared, resolve_declared, DIMENSIONS  # noqa: E402
from _common import iter_source_files, read_lines, rel  # noqa: E402


def _load_checker(filename):
    """Import a hyphen-named checker module by file path and return it."""
    mod_name = "fidelity_checker_" + filename.replace("-", "_").replace(".py", "")
    spec = importlib.util.spec_from_file_location(mod_name, _HERE / filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# Advisory-signal weights. Emitted in the JSON so the blend stays auditable, but
# these NEVER move `ratio` or `fidelityVerdict` - signals are leads, not a score.
SIGNAL_WEIGHTS = {"surfaces": 0.70, "seams": 0.15, "ssot": 0.15}

DEFAULT_ESSENCE_THRESHOLD = 80


def _round(x, n=3):
    return round(x + 0.0, n)


# ---------------------------------------------------------------------------
# Axis 1: completeness (the contract)
# ---------------------------------------------------------------------------

def compute_completeness(declared, mock_seams, seam_source):
    """The schema's Axis-1 formula. Deterministic arithmetic over two artefacts."""
    elements = declared["elements"]
    # name -> dimension, so notBacked can be attributed byDimension.
    dim_of = {el["name"]: el["dimension"] for el in elements}

    # notBacked: distinct DECLARED SURFACES, from either source.
    not_backed = {}

    for u in declared["unbackedSurfaces"]:
        name = u["surface"]
        not_backed.setdefault(name, {
            "surface": name,
            "reason": "declared but no owning SSOT (gapReport.unbackedSurfaces)",
            "detail": u.get("reason", ""),
            "field": u.get("field", ""),
            "source": "spec#gapReport.unbackedSurfaces",
        })

    for s in mock_seams:
        if not s.get("declaredLive"):
            continue  # only declared-live seams count - the whole precision fix
        name = s.get("surface")
        if not name:
            continue
        not_backed.setdefault(name, {
            "surface": name,
            "reason": "declared live but reading mock/stub data (green-but-mock)",
            "detail": s.get("evidence", ""),
            "field": "",
            "source": seam_source,
        })

    declared_count = len(elements)
    # A notBacked surface only subtracts if it IS a declared element - a seam tied
    # to something outside the declared list must not push builtAndBacked negative.
    counted = {n for n in not_backed if n in dim_of}
    built_and_backed = declared_count - len(counted)

    if declared_count == 0:
        ratio = "n/a"
        ratio_basis = ("no COVERED functionalSurface elements in the given spec(s) - "
                       "nothing was declared, so there is no ratio to compute")
    else:
        ratio = _round(built_and_backed / declared_count)
        ratio_basis = "builtAndBacked / declared"

    by_dim = {}
    for dim in DIMENSIONS:
        d_total = sum(1 for el in elements if el["dimension"] == dim)
        d_bad = sum(1 for n in counted if dim_of.get(n) == dim)
        by_dim[dim] = f"{d_total - d_bad}/{d_total}"

    return {
        "declared": declared_count,
        "builtAndBacked": built_and_backed,
        "ratio": ratio,
        "ratioBasis": ratio_basis,
        "byDimension": by_dim,
        "unbackedSurfaces": [v for k, v in sorted(not_backed.items())
                             if v["source"].startswith("spec#")],
        "mockSeams": [s for s in mock_seams if s.get("declaredLive")],
        "mockSeamSource": seam_source,
        # The half of the verdict this tool can actually prove.
        "verdict": ("gap-drift" if (ratio != "n/a" and ratio < 1.0)
                    else ("complete" if ratio != "n/a" else "n/a")),
    }


# ---------------------------------------------------------------------------
# completeness.signals (advisory heuristics - never gating)
# ---------------------------------------------------------------------------

def signal_surfaces(unbacked_report):
    surfaces = unbacked_report["surfaces"]
    data_surfaces = [
        s for s in surfaces
        if s["backing"] in ("real", "mock")
        or (s["backing"] == "missing" and s["rendersData"])
    ]
    backed = [s for s in data_surfaces if s["backing"] == "real"]
    unbacked = [s for s in data_surfaces if s["backing"] != "real"]
    declared = len(data_surfaces)
    return {
        "score": _round((len(backed) / declared) if declared else 1.0),
        "weight": SIGNAL_WEIGHTS["surfaces"],
        "dataSurfaces": declared,
        "backedSurfaces": len(backed),
        "unbackedSurfaces": len(unbacked),
        "formula": "backedSurfaces / dataSurfaces (mock+missing-render = not backed; static excluded)",
        "findings": [
            {"surface": s["surface"], "backing": s["backing"],
             "confidence": s["confidence"], "rendersData": s["rendersData"],
             "evidence": s["evidence"]}
            for s in sorted(unbacked, key=lambda x: (x["backing"], x["surface"]))
        ],
    }


def signal_seams(mock_report):
    findings = mock_report["findings"]
    files_scanned = mock_report["summary"]["filesScanned"]
    high = [f for f in findings if f["confidence"] == "high"]
    files_with_high = {f["file"] for f in high}
    score = ((files_scanned - len(files_with_high)) / files_scanned) if files_scanned else 1.0
    return {
        "score": _round(score),
        "weight": SIGNAL_WEIGHTS["seams"],
        "filesScanned": files_scanned,
        "filesWithHighConfSeams": len(files_with_high),
        "highConfSeams": len(high),
        "totalSeams": len(findings),
        "declaredLiveSeams": mock_report["summary"].get("declaredLiveSeams", 0),
        "formula": "(filesScanned - filesWithHighConfSeams) / filesScanned (only high-confidence seams subtract)",
        "findings": [
            {"file": f["file"], "line": f["line"], "seamKind": f["seamKind"],
             "confidence": f["confidence"], "declaredLive": f.get("declaredLive"),
             "surface": f.get("surface"), "evidence": f["evidence"]}
            for f in findings if f["confidence"] in ("high", "med")
        ],
    }


def signal_ssot(ssot_report):
    violations = ssot_report["violations"]
    high = sum(1 for v in violations if v["risk"] == "high")
    med = sum(1 for v in violations if v["risk"] == "med")
    weighted = high * 1.0 + med * 0.5
    return {
        "score": _round(1.0 / (1.0 + weighted)),
        "weight": SIGNAL_WEIGHTS["ssot"],
        "violations": len(violations),
        "highRisk": high,
        "medRisk": med,
        "weightedViolations": _round(weighted, 2),
        "formula": "1 / (1 + weightedViolations); weightedViolations = high*1.0 + med*0.5",
        "findings": violations,
    }


def build_signals(root, declared, ssot_min_files, mock_report):
    unbacked_mod = _load_checker("unbacked-surface-checker.py")
    ssot_mod = _load_checker("ssot-checker.py")

    surf = signal_surfaces(unbacked_mod.build_report(root))
    seam = signal_seams(mock_report)
    ssot = signal_ssot(ssot_mod.build_report(root, ssot_min_files))
    coverage = resolve_declared(
        root, declared, iter_source_files,
        lambda p: "\n".join(read_lines(p)), rel)

    blended = _round(surf["score"] * SIGNAL_WEIGHTS["surfaces"]
                     + seam["score"] * SIGNAL_WEIGHTS["seams"]
                     + ssot["score"] * SIGNAL_WEIGHTS["ssot"])
    return {
        "_note": ("ADVISORY heuristic read of the codebase - leads for a human, "
                  "not a score. Never contributes to completeness.ratio or to "
                  "fidelityVerdict. Measured ~27-30% precision against ground "
                  "truth before the declared-surface cross-check; treat "
                  "undeclared findings with particular suspicion."),
        "blendedScore": blended,
        "weights": SIGNAL_WEIGHTS,
        "surfaces": surf,
        "seams": seam,
        "ssot": ssot,
        # The contract formula cannot see a declared element that was simply never
        # built (it is optimistic - an empty tree scores 1.0). This is the lead
        # for that blind spot. Advisory: "no evidence found" is an unprovable
        # negative, so it prompts a look, it does not fail a build.
        "declaredCoverage": coverage,
    }


# ---------------------------------------------------------------------------
# Axis 2: essence (supplied, not computed - this tool has no judge)
# ---------------------------------------------------------------------------

def load_essence(path):
    """Read a semantic-qa essence result. Must carry score + floorHeld."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if "score" not in data or "floorHeld" not in data:
        raise ValueError("essence file must contain 'score' and 'floorHeld' "
                         "(see fidelity-scorecard-schema.md section 'Axis 2')")
    return data


def derive_verdict(ratio, essence, threshold):
    """The schema's verdict rule table, in code. Returns (verdict, basis)."""
    if ratio == "n/a":
        return None, ("no declared surfaces - completeness is n/a, so no verdict "
                      "is derivable")

    gap = ratio < 1.0
    if essence is None:
        if gap:
            return None, ("gap-drift is certain (ratio < 1.0) but GAP-DRIFT vs "
                          "GAP+TASTE-DRIFT needs the essence axis - run "
                          "semantic-qa --fidelity, or pass --essence")
        return None, ("completeness is 1.0; FAITHFUL vs TASTE-DRIFT is entirely "
                      "an essence question - run semantic-qa --fidelity, or pass "
                      "--essence")

    taste = (not essence["floorHeld"]) or essence["score"] < threshold
    if gap and taste:
        return "GAP+TASTE-DRIFT", "ratio < 1.0 and essence floor/threshold missed"
    if gap:
        return "GAP-DRIFT", "ratio < 1.0"
    if taste:
        return "TASTE-DRIFT", (f"floorHeld={essence['floorHeld']}, "
                               f"score={essence['score']} vs threshold {threshold}")
    return "FAITHFUL", (f"ratio == 1.0, floor held, "
                        f"score {essence['score']} >= {threshold}")


# ---------------------------------------------------------------------------
# Arms
# ---------------------------------------------------------------------------

def load_verification_report(path):
    """Pull dataReality.mockSeams from review-shipping's verification report.

    That report is the schema's stated source for built-and-backed, and it is
    produced by the skill that owns the Data-Reality Gate - so when it exists it
    is authoritative and we do NOT re-scan behind it.
    """
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    dr = data.get("dataReality") or {}
    return list(dr.get("mockSeams") or [])


def build_arm(name, root, declared, args, mock_mod, essence=None):
    root = Path(root).resolve()
    if not root.exists():
        raise ValueError(f"arm '{name}': path not found: {root}")

    # Always run the detector: signals need the full scan regardless of where the
    # gating seams come from.
    mock_report = mock_mod.build_report(root, declared)

    if args.verification_report:
        seams = load_verification_report(args.verification_report)
        seam_source = f"verification-report.json#dataReality ({args.verification_report})"
    else:
        seams = [
            {"surface": f["surface"], "file": f["file"], "line": f["line"],
             "declaredLive": f["declaredLive"], "evidence": f["evidence"],
             "seamKind": f["seamKind"], "confidence": f["confidence"]}
            for f in mock_report["findings"]
            # Gate on high/med only: 'low' is the detector's own known noisy class
            # (bare 'stub'/'placeholder' words, comment mentions).
            if f["declaredLive"] and f["confidence"] in ("high", "med")
        ]
        seam_source = "mock-seam-detector.py (no --verification-report given)"

    completeness = compute_completeness(declared, seams, seam_source)
    completeness["signals"] = build_signals(root, declared, args.ssot_min_files,
                                            mock_report)

    verdict, basis = derive_verdict(completeness["ratio"], essence,
                                    args.essence_threshold)

    return {
        "name": name,
        "codebase": str(root),
        "completeness": completeness,
        "essence": essence,
        "fidelityVerdict": verdict,
        "verdictBasis": basis,
    }


def build_rubric_source(declared, args):
    rubric = {
        "productDefinition": args.product_definition,
        "specs": declared["specs"],
        "declaredSurfaceCount": len(declared["elements"]),
        "nonNegotiableDifferentiators": [],
        "qualityBar": [],
    }
    if args.product_definition:
        try:
            pd = json.loads(Path(args.product_definition).read_text(encoding="utf-8"))
        except Exception as e:
            rubric["error"] = f"product-definition unreadable: {e}"
            return rubric
        # nonNegotiable DEFAULTS TO TRUE when omitted - differentiators are
        # non-negotiable by intent (product-definition output-schema.md).
        rubric["nonNegotiableDifferentiators"] = [
            d.get("id") for d in (pd.get("differentiators") or [])
            if d.get("nonNegotiable", True)
        ]
        rubric["qualityBar"] = [q.get("id") for q in (pd.get("qualityBar") or [])]
    return rubric


def build_comparison(arms):
    """Deltas between exactly two arms. Completeness is always comparable;
    essence only when both arms were judged."""
    a, b = arms[0], arms[1]
    ra, rb = a["completeness"]["ratio"], b["completeness"]["ratio"]

    notes = []
    if ra == "n/a" or rb == "n/a":
        comp_delta, winner = "n/a", "tie"
        notes.append("completeness n/a on at least one arm - nothing declared")
    else:
        hi = a if ra >= rb else b
        comp_delta = (f"{hi['name']} +{_round(abs(ra - rb))} "
                      f"({max(ra, rb)} vs {min(ra, rb)})")
        winner = hi["name"] if ra != rb else "tie"

    ea, eb = a["essence"], b["essence"]
    if ea and eb:
        ehi = a if ea["score"] >= eb["score"] else b
        ess_delta = (f"{ehi['name']} +{abs(ea['score'] - eb['score'])} "
                     f"({max(ea['score'], eb['score'])} vs {min(ea['score'], eb['score'])})")
        floor_delta = (f"{a['name']} floorHeld={ea['floorHeld']}; "
                       f"{b['name']} floorHeld={eb['floorHeld']}")
    else:
        ess_delta, floor_delta = None, None
        notes.append("essence axis absent on at least one arm - completeness "
                     "delta only; winner reflects completeness, not fidelity")

    # The optimistic formula counts a never-built surface as built, so an arm that
    # shipped less can score HIGHER. Say so where the winner is declared, not
    # only in the JSON - this is the one place the delta could mislead.
    for arm in (a, b):
        cov = arm["completeness"]["signals"]["declaredCoverage"]
        if cov["unresolved"]:
            notes.append(
                f"arm '{arm['name']}': {cov['unresolved']} declared surface(s) have "
                f"no code evidence, yet count as builtAndBacked - its ratio is an "
                f"UPPER BOUND and this delta may be flattering it. Verify "
                f"signals.declaredCoverage before trusting the winner.")

    return {
        "completenessDelta": comp_delta,
        "essenceDelta": ess_delta,
        "floorDelta": floor_delta,
        "winner": winner,
        "notes": notes,
    }


def build_scorecard(args):
    declared = load_declared(args.spec)
    mock_mod = _load_checker("mock-seam-detector.py")

    essence = load_essence(args.essence) if args.essence else None

    arms = [build_arm(name, path, declared, args, mock_mod, essence)
            for name, path in args.arms]

    card = {
        "$schema": "shipkit-artifact",
        "type": "fidelity-scorecard",
        "version": "1.0",
        "lastUpdated": args.stamp,  # null unless --stamp; never datetime.now()
        "source": "fidelity-score.py",
        "mode": "comparative" if len(arms) > 1 else "single",
        "essenceThreshold": args.essence_threshold,
        "rubricSource": build_rubric_source(declared, args),
        "arms": arms,
    }
    if declared["errors"]:
        card["rubricSource"]["specErrors"] = declared["errors"]
    if len(arms) == 2:
        card["comparison"] = build_comparison(arms)
    elif len(arms) > 2:
        card["comparison"] = {
            "_note": ("comparison block is defined for exactly two arms; "
                      f"{len(arms)} given - compare arms[] directly"),
        }
    return card


# ---------------------------------------------------------------------------

def print_report(sc):
    print(f"fidelity-scorecard  mode={sc['mode']}  "
          f"declared={sc['rubricSource']['declaredSurfaceCount']} surfaces")
    print(f"  lastUpdated: {sc['lastUpdated']}")
    for s in sc["rubricSource"]["specs"]:
        print(f"  rubric: {s}")
    for e in sc["rubricSource"].get("specErrors") or []:
        print(f"  ! spec unreadable: {e['spec']}: {e['error']}")
    print()

    for arm in sc["arms"]:
        c = arm["completeness"]
        print(f"  ARM: {arm['name']}   ({arm['codebase']})")
        ratio = c["ratio"]
        shown = ratio if ratio == "n/a" else f"{ratio:.3f}"
        print(f"    COMPLETENESS  {c['builtAndBacked']}/{c['declared']}  ({shown})"
              f"   [{c['verdict']}]")
        print("    byDimension:  " + "  ".join(
            f"{k}={v}" for k, v in c["byDimension"].items()))
        ess = arm["essence"]
        if ess:
            print(f"    ESSENCE       {ess['score']}  floorHeld={ess['floorHeld']}")
        else:
            print("    ESSENCE       (not judged - semantic-qa fills this axis)")
        print(f"    VERDICT       {arm['fidelityVerdict'] or '(not derivable)'}")
        print(f"                  {arm['verdictBasis']}")

        if c["unbackedSurfaces"]:
            print("    UNBACKED (declared, no owning SSOT):")
            for u in c["unbackedSurfaces"]:
                print(f"      - {u['surface']}  {u['detail']}")
        if c["mockSeams"]:
            print("    GREEN-BUT-MOCK (declared live, reading mock data):")
            for m in c["mockSeams"]:
                loc = f"{m.get('file','?')}:{m.get('line','?')}"
                print(f"      - {m.get('surface')}  {loc}")
                print(f"          {m.get('evidence','')[:100]}")

        sig = c["signals"]
        cov = sig["declaredCoverage"]
        if cov["unresolved"]:
            # Loud on purpose: the contract formula counts these as BUILT, so this
            # line is the only place an unbuilt-but-declared surface shows up.
            print(f"    !! {cov['unresolved']}/{cov['resolved'] + cov['unresolved']} "
                  f"declared surfaces have NO code evidence - the ratio above "
                  f"counts them as built:")
            for e in cov["elements"]:
                if not e["resolved"]:
                    print(f"      ? {e['name']}  ({e['dimension']}/{e['kind']}) "
                          f"- not found, or built under another name")
        print(f"    signals (ADVISORY, not scored): blend={sig['blendedScore']:.3f}"
              f"  surfaces={sig['surfaces']['score']:.2f}"
              f"  seams={sig['seams']['score']:.2f}"
              f"  ssot={sig['ssot']['score']:.2f}")
        adv = sig["seams"]["totalSeams"] - sig["seams"]["declaredLiveSeams"]
        print(f"      {sig['surfaces']['unbackedSurfaces']} unbacked-surface leads, "
              f"{sig['seams']['highConfSeams']} high-conf seams "
              f"({adv} on undeclared surfaces), "
              f"{sig['ssot']['violations']} ssot violations, "
              f"{cov['resolved']}/{cov['resolved'] + cov['unresolved']} declared "
              f"surfaces found in code")
        print()

    cmp = sc.get("comparison")
    if cmp and "winner" in cmp:
        print("  COMPARISON")
        print(f"    completeness: {cmp['completenessDelta']}")
        print(f"    essence:      {cmp['essenceDelta'] or '(not judged)'}")
        print(f"    floor:        {cmp['floorDelta'] or '(not judged)'}")
        print(f"    winner:       {cmp['winner']}")
        for n in cmp["notes"]:
            print(f"    note: {n}")


def _parse_arm(s):
    if "=" not in s:
        raise argparse.ArgumentTypeError(
            f"--arm expects name=path, got '{s}' (e.g. --arm shipkit=../arm-shipkit)")
    name, path = s.split("=", 1)
    if not name or not path:
        raise argparse.ArgumentTypeError(f"--arm expects name=path, got '{s}'")
    return (name, path)


def main():
    ap = argparse.ArgumentParser(
        description="Emit the fidelity scorecard (completeness axis) defined by "
                    "references/fidelity-scorecard-schema.md.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "COMPLETENESS (the contract - denominator comes from the SPEC):\n"
            "  declared       = functionalSurface elements with verdict COVERED\n"
            "  notBacked      = gapReport.unbackedSurfaces + mockSeams where\n"
            "                   declaredLive == true\n"
            "  builtAndBacked = declared - |notBacked|\n"
            "  ratio          = builtAndBacked / declared   (declared 0 -> n/a)\n\n"
            "completeness.signals = the old surfaces/seams/ssot code-scan blend,\n"
            "kept as ADVISORY leads. It never moves ratio or fidelityVerdict.\n\n"
            "VERDICT is derived, never guessed: without --essence only the\n"
            "completeness half is decidable, so fidelityVerdict stays null and\n"
            "completeness.verdict carries what is provable.\n\n"
            "Deterministic: lastUpdated is null unless --stamp is passed."
        ),
    )
    ap.add_argument("path", nargs="?", default=None,
                    help="Target codebase (single-arm mode). Use --arm for two arms.")
    ap.add_argument("--arm", action="append", type=_parse_arm, default=None,
                    metavar="NAME=PATH",
                    help="Named arm for comparative mode; repeat for each arm")
    ap.add_argument("--arm-name", default="build",
                    help="Arm label in single-arm mode (default: build)")
    ap.add_argument("--spec", nargs="+", required=True, metavar="SPEC",
                    help="Spec artifact(s) declaring the surfaces "
                         "(.shipkit/specs/**/*.json). The rubric's denominator.")
    ap.add_argument("--verification-report", default=None, metavar="PATH",
                    help="review-shipping verification-report.json. When given, "
                         "its dataReality.mockSeams is authoritative and the "
                         "detector is not used for gating.")
    ap.add_argument("--product-definition", default=None, metavar="PATH",
                    help="product-definition.json, for rubricSource provenance")
    ap.add_argument("--essence", default=None, metavar="PATH",
                    help="Essence axis result ({score, floorHeld, ...}) from "
                         "semantic-qa. Enables full verdict derivation.")
    ap.add_argument("--essence-threshold", type=int,
                    default=DEFAULT_ESSENCE_THRESHOLD,
                    help=f"Essence pass threshold (default {DEFAULT_ESSENCE_THRESHOLD})")
    ap.add_argument("--report", action="store_true", help="Human-readable output")
    ap.add_argument("--json", action="store_true", help="Force JSON (default)")
    ap.add_argument("--stamp", default=None,
                    help="Value for lastUpdated (ISO timestamp). Omitted = null, "
                         "keeping runs deterministic.")
    ap.add_argument("--ssot-min-files", type=int, default=2,
                    help="Min distinct files for an SSOT violation (default 2)")
    ap.add_argument("--out", default=None, help="Also write the JSON scorecard here")
    args = ap.parse_args()

    if args.arm and args.path:
        print("error: give either <path> (single arm) or --arm name=path "
              "(one or more), not both", file=sys.stderr)
        sys.exit(2)
    if not args.arm and not args.path:
        print("error: need a target: <path> or --arm name=path", file=sys.stderr)
        sys.exit(2)
    args.arms = args.arm if args.arm else [(args.arm_name, args.path)]

    try:
        scorecard = build_scorecard(args)
    except (ValueError, OSError, json.JSONDecodeError) as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(2)

    if not scorecard["rubricSource"]["declaredSurfaceCount"]:
        print("warning: no COVERED functionalSurface elements in the given "
              "spec(s) - completeness is n/a and no seam can be declared-live",
              file=sys.stderr)

    payload = json.dumps(scorecard, indent=2)
    if args.out:
        Path(args.out).write_text(payload + "\n", encoding="utf-8")

    if args.report and not args.json:
        print_report(scorecard)
        if args.out:
            print(f"  (JSON written to {args.out})")
    else:
        print(payload)
    sys.exit(0)


if __name__ == "__main__":
    main()
