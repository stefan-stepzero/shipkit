#!/usr/bin/env python3
"""Migrate a fat .shipkit/architecture.json into the lean + archive split.

OPT-IN, one-time. Nothing runs this automatically — the project owner invokes it
when ready. Default is a DRY RUN (prints before/after sizes, writes nothing); pass
--apply to actually write the files.

What it does:
  1. Reads .shipkit/architecture.json (and merges any existing
     architecture-archive.json, preferring the fuller body per ADR id).
  2. Writes the full union to architecture-archive.json (append-only; bodies preserved).
  3. Rewrites architecture.json LEAN:
       - active / amended ADRs -> capped {id, decision, scope, date, one-line rationale}
       - superseded ADRs       -> stub {id, status:"superseded", supersededBy, decision}
     designSystem / patterns / constraints are preserved as-is.

A decision is treated as superseded only when it already carries status=="superseded"
AND a supersededBy pointer. The migrator does NOT invent supersession links.

Convention: install/skills/shipkit-engineering-definition/references/architecture-log-schema.md
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

LEAN_NAME = "architecture.json"
ARCHIVE_NAME = "architecture-archive.json"


def _now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _one_line(text):
    """First sentence (or first ~140 chars) of a possibly multi-sentence string."""
    if not text:
        return text
    text = " ".join(str(text).split())
    # Prefer a sentence boundary.
    for sep in (". ", "; "):
        idx = text.find(sep)
        if 0 < idx <= 140:
            return text[: idx + 1].strip()
    return text if len(text) <= 140 else text[:137].rstrip() + "..."


def _is_superseded(adr):
    return adr.get("status") == "superseded" and adr.get("supersededBy")


def _fuller(a, b):
    """Pick the entry with the more complete body (longer rationale + more alternatives)."""
    if a is None:
        return b
    if b is None:
        return a
    score = lambda d: (len(str(d.get("rationale", ""))), len(d.get("alternatives", []) or []))
    return a if score(a) >= score(b) else b


def _cap_active(adr):
    out = {"id": adr["id"], "decision": _one_line(adr.get("decision", ""))}
    if adr.get("scope"):
        out["scope"] = adr["scope"]
    if adr.get("date"):
        out["date"] = adr["date"]
    if adr.get("rationale"):
        out["rationale"] = _one_line(adr["rationale"])
    if adr.get("status") == "amended" or adr.get("amendedBy"):
        out["status"] = "amended"
        if adr.get("amendedBy"):
            out["amendedBy"] = adr["amendedBy"]
    return out


def _stub(adr):
    return {
        "id": adr["id"],
        "status": "superseded",
        "supersededBy": adr["supersededBy"],
        "decision": _one_line(adr.get("decision", "")),
    }


def migrate(shipkit_dir, apply):
    lean_path = os.path.join(shipkit_dir, LEAN_NAME)
    archive_path = os.path.join(shipkit_dir, ARCHIVE_NAME)

    if not os.path.isfile(lean_path):
        print(f"ERROR: {lean_path} not found.", file=sys.stderr)
        return 2

    with open(lean_path, "r", encoding="utf-8") as f:
        lean = json.load(f)

    archive_existing = {}
    if os.path.isfile(archive_path):
        with open(archive_path, "r", encoding="utf-8") as f:
            for adr in json.load(f).get("decisions", []):
                archive_existing[adr["id"]] = adr

    # Build the full union (prefer fuller body per id).
    full_by_id = {}
    for adr in lean.get("decisions", []):
        full_by_id[adr["id"]] = _fuller(archive_existing.get(adr["id"]), adr)
    for adr_id, adr in archive_existing.items():
        full_by_id.setdefault(adr_id, adr)

    def sort_key(adr):
        num = "".join(ch for ch in adr["id"] if ch.isdigit())
        return int(num) if num else 0

    full_decisions = sorted(full_by_id.values(), key=sort_key)

    archive = {
        "$schema": "shipkit-artifact",
        "type": "architecture-decisions-archive",
        "version": "1.0",
        "lastUpdated": _now_iso(),
        "source": "shipkit-engineering-definition",
        "note": "Full append-only ADR log. Not @-imported — read on demand.",
        "decisions": full_decisions,
        "patterns": lean.get("patterns", []),
        "constraints": lean.get("constraints", []),
    }

    lean_decisions = [
        _stub(adr) if _is_superseded(adr) else _cap_active(adr) for adr in full_decisions
    ]
    new_lean = {
        "$schema": "shipkit-artifact",
        "type": "architecture-decisions",
        "version": "1.0",
        "lastUpdated": _now_iso(),
        "source": lean.get("source", "shipkit-engineering-definition"),
        "note": "Lean active-decisions index. Full ADR bodies live in .shipkit/architecture-archive.json — read on demand.",
        "decisions": lean_decisions,
    }
    if lean.get("designSystem"):
        new_lean["designSystem"] = lean["designSystem"]
    new_lean["patterns"] = lean.get("patterns", [])
    new_lean["constraints"] = lean.get("constraints", [])

    old_size = len(json.dumps(lean))
    new_size = len(json.dumps(new_lean))
    archive_size = len(json.dumps(archive))
    n_super = sum(1 for a in full_decisions if _is_superseded(a))

    print(f"ADRs total: {len(full_decisions)}  (superseded stubbed: {n_super})")
    print(f"lean architecture.json:   {old_size:>8} B  ->  {new_size:>8} B")
    print(f"architecture-archive.json: {archive_size:>8} B  (full bodies)")

    if not apply:
        print("\nDRY RUN — no files written. Re-run with --apply to write.")
        return 0

    with open(archive_path, "w", encoding="utf-8") as f:
        json.dump(archive, f, indent=2, ensure_ascii=False)
        f.write("\n")
    with open(lean_path, "w", encoding="utf-8") as f:
        json.dump(new_lean, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"\nWrote {lean_path}\nWrote {archive_path}")
    return 0


def main():
    p = argparse.ArgumentParser(
        description="Split a fat .shipkit/architecture.json into lean index + full archive (opt-in)."
    )
    p.add_argument(
        "--shipkit-dir",
        default=".shipkit",
        help="Path to the project's .shipkit/ directory (default: ./.shipkit)",
    )
    p.add_argument(
        "--apply",
        action="store_true",
        help="Actually write the files. Without it, runs a dry-run preview.",
    )
    args = p.parse_args()
    sys.exit(migrate(args.shipkit_dir, args.apply))


if __name__ == "__main__":
    main()
