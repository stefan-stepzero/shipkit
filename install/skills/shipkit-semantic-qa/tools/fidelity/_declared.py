#!/usr/bin/env python3
"""
_declared.py - Load the DECLARED surface list from Shipkit spec artifacts and
map built code back onto it. Not a CLI.

WHY THIS EXISTS (the denominator-provenance fix)
------------------------------------------------
The v1 checkers re-scanned the codebase to invent their own denominator: every
file the regexes tripped on became a finding. That is why precision measured
~27-30% against ground truth - the tools flagged seams in fixtures, scratch
files, and unrelated code that no one ever declared live, then scored the build
down for them.

The declared list is the authority. A spec's `functionalSurface` is the set of
things the build was ASKED to deliver; `deferred` / `acceptanceCriteria.wontHave`
are the things it was asked NOT to. A mock seam only means "green-but-mock" if it
sits on a surface the spec declares LIVE. Everything else is noise by definition
- not a judgement call, a contract.

So this module answers exactly one question, in the reverse direction from the
v1 design:

    given a file with a mock seam, does it belong to a DECLARED-LIVE surface?

It deliberately does NOT try to answer "does every declared element exist in
code?" - that requires proving a negative from a name like "web-ui", which is
where false positives are manufactured. Unmatched seams default to
`declaredLive: false` (see FAIL-OPEN below).

FAIL-OPEN, DELIBERATELY
-----------------------
No match -> `declaredLive: false` -> the seam does NOT drag the score; it is
still emitted as advisory. We under-claim rather than over-claim: a false
"green-but-mock" FAIL on a surface nobody declared burns the user's trust in the
gate, and a gate people learn to ignore catches nothing. Recall is the acceptable
loss here; precision is the product.

MATCHING, PER DIMENSION (evidence differs by kind, so the matcher does too)
--------------------------------------------------------------------------
  datastores  - CONTENT match. The declared name IS the identifier in code
                (`share_links`, `cohort_leaderboard_v`). Strongest signal.
  contracts   - CONTENT match on the endpoint path literal, OR PATH match on
                route-file conventions (app/api/recipes/[id]/share/route.ts).
                `{id}` / `:id` / `[id]` are normalized to one wildcard form.
  applications- PATH-TOKEN match. Names like "coach-dashboard" are only ever
                recoverable from the file path. Weakest signal, marked as such.
  integrations- CONTENT match on the distinctive vendor token ("Supabase Auth"
                -> "supabase"), generic words dropped.

Limits (honest): name-based matching cannot prove a file IS a declared surface,
only that it carries the declared identifier. A surface renamed between spec and
build will not match and will fail open. Findings are leads, not proof.
"""

import json
import re
from pathlib import Path

# The four functionalSurface dimensions, in schema order.
DIMENSIONS = ("applications", "datastores", "contracts", "integrations")

# Only COVERED elements are declared-live. EXPLICITLY-DEFERRED is out of scope on
# purpose; FLAGGED means the spec gate never cleared, so it was never declared live.
LIVE_VERDICT = "COVERED"

# Words too generic to identify a surface on their own. Matching on these alone
# would tie a seam to any file in the repo.
STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "for", "to", "with",
    "app", "application", "ui", "web", "api", "service", "backend", "frontend",
    "server", "client", "provider", "auth", "authentication", "system",
    "module", "component", "data", "store", "db", "database", "table", "view",
    "endpoint", "rest", "graphql", "integration", "external", "internal",
    "new", "main", "core", "base", "default", "shared", "common",
}

_NON_ALNUM = re.compile(r"[^a-z0-9]+")
# Path params in any of the three dialects we see: {id} :id [id]
_PATH_PARAM = re.compile(r"(\{[^/}]+\}|:[A-Za-z_]\w*|\[[^/\]]+\])")
_HTTP_VERB = re.compile(r"^(GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\s+", re.I)


def _tokens(name):
    """Lowercase alnum tokens of a declared name, minus stopwords.

    'coach-dashboard' -> {'coach', 'dashboard'};  'Supabase Auth' -> {'supabase'}
    """
    raw = {t for t in _NON_ALNUM.split(name.lower()) if t}
    return {t for t in raw if t not in STOPWORDS and len(t) > 2}


def _endpoint_path(name):
    """Extract the path from a contract name: 'POST /api/x/{id}' -> '/api/x/{id}'."""
    stripped = _HTTP_VERB.sub("", name.strip())
    return stripped.split()[0] if stripped else ""


def _path_segments(endpoint):
    """Literal (non-param) segments of an endpoint path, lowercased.

    '/api/recipes/{id}/share' -> ['api', 'recipes', 'share']
    Params are dropped: they are named differently in every dialect and carry no
    identifying signal.
    """
    out = []
    for seg in endpoint.split("/"):
        seg = seg.strip()
        if not seg or _PATH_PARAM.fullmatch(seg):
            continue
        out.append(seg.lower())
    return out


def load_specs(spec_paths):
    """Read spec JSON artifacts. Returns (specs, errors) - never raises on bad JSON."""
    specs, errors = [], []
    for p in spec_paths:
        path = Path(p)
        try:
            specs.append((path, json.loads(path.read_text(encoding="utf-8"))))
        except Exception as e:
            errors.append({"spec": str(path), "error": str(e)})
    return specs, errors


def _deferred_tokens(spec):
    """Token sets for elements the spec explicitly put OUT of scope.

    A mock seam on a deferred surface is fine and must never fail the gate
    (review-shipping: 'a mock seam on a surface the spec explicitly defers is
    fine - note it, don't fail').
    """
    out = []
    for d in spec.get("deferred") or []:
        el = d.get("element")
        if el:
            out.append(_tokens(el))
    ac = spec.get("acceptanceCriteria") or {}
    for w in ac.get("wontHave") or []:
        if isinstance(w, str) and _tokens(w):
            out.append(_tokens(w))
    return [t for t in out if t]


def load_declared(spec_paths):
    """Build the declared-surface list from one or more spec artifacts.

    Returns:
      {
        elements: [{name, kind, dimension, evidence, spec}]  # verdict == COVERED
        unbackedSurfaces: [{surface, field, reason, spec}]
        deferredTokens: [set[str]]
        specs: [str], errors: [{spec, error}]
      }
    """
    specs, errors = load_specs(spec_paths)
    elements, unbacked, deferred_tokens = [], [], []

    for path, spec in specs:
        fs = spec.get("functionalSurface") or {}
        for dim in DIMENSIONS:
            for el in fs.get(dim) or []:
                if (el.get("verdict") or "").upper() != LIVE_VERDICT:
                    continue
                elements.append({
                    "name": el.get("name", ""),
                    "kind": el.get("kind", ""),
                    "dimension": dim,
                    "evidence": el.get("evidence", ""),
                    "spec": path.name,
                })
        # gapReport.unbackedSurfaces: declared but with no owning SSOT.
        # NOTE: a SAVED spec has gapReport.status == "clear", which REQUIRES
        # unbackedSurfaces == [] - so this is normally empty by construction.
        # Read anyway: it costs nothing and covers hand-edited / in-flight /
        # legacy specs, and the scorecard schema names it as an input.
        gr = spec.get("gapReport") or {}
        for u in gr.get("unbackedSurfaces") or []:
            unbacked.append({
                "surface": u.get("surface", ""),
                "field": u.get("field", ""),
                "reason": u.get("reason", ""),
                "spec": path.name,
            })
        deferred_tokens.extend(_deferred_tokens(spec))

    return {
        "elements": elements,
        "unbackedSurfaces": unbacked,
        "deferredTokens": deferred_tokens,
        "specs": [str(p) for p, _ in specs],
        "errors": errors,
    }


def _norm_path(relpath):
    """Normalized token set for a source path: 'src/app/coach/page.tsx' ->
    {'src','app','coach','page','tsx'} (stopwords retained here - we match
    declared tokens INTO this set, so its own generic entries are harmless)."""
    return {t for t in _NON_ALNUM.split(relpath.lower()) if t}


def match_element(relpath, text, element):
    """Does `relpath`/`text` carry evidence of this declared element?

    Returns (matched: bool, confidence: 'high'|'med'|'low', evidence: str).
    Content evidence outranks path evidence: an identifier in the file is a much
    stronger tie than a word in its path.
    """
    name = element["name"]
    dim = element["dimension"]
    low_text = text.lower()

    if dim == "datastores":
        # The declared name IS the code identifier. Word-boundary exact match.
        if name and re.search(r"\b" + re.escape(name.lower()) + r"\b", low_text):
            return True, "high", f"references declared datastore '{name}'"
        return False, "low", ""

    if dim == "contracts":
        endpoint = _endpoint_path(name)
        segs = _path_segments(endpoint)
        if not segs:
            return False, "low", ""
        # (a) the literal path appears in the file (fetch('/api/recipes/...'))
        literal = "/".join(segs)
        if literal and literal in low_text.replace("\\", "/"):
            return True, "high", f"references declared endpoint path '{endpoint}'"
        # (b) the file IS the route: every literal segment on the path, in order
        p = relpath.lower().replace("\\", "/")
        idx, ordered = 0, True
        for seg in segs:
            found = p.find("/" + seg, idx)
            if found < 0:
                found = p.find(seg, idx)
            if found < 0:
                ordered = False
                break
            idx = found + len(seg)
        if ordered:
            return True, "high", f"route file for declared endpoint '{endpoint}'"
        return False, "low", ""

    if dim == "integrations":
        toks = _tokens(name)
        if toks and all(re.search(r"\b" + re.escape(t), low_text) for t in toks):
            return True, "med", f"references declared integration '{name}'"
        return False, "low", ""

    # applications: only the path can carry the name. Weakest tier - require
    # EVERY distinctive token, else 'web-ui' would match the whole repo.
    toks = _tokens(name)
    if not toks:
        return False, "low", ""
    ptoks = _norm_path(relpath)
    if all(any(t in pt or pt in t for pt in ptoks) for t in toks):
        return True, "med", f"path matches declared application surface '{name}'"
    return False, "low", ""


def is_deferred(relpath, declared):
    """True if this path looks like an explicitly-deferred (out-of-scope) surface."""
    ptoks = _norm_path(relpath)
    for toks in declared.get("deferredTokens") or []:
        if toks and all(any(t in pt or pt in t for pt in ptoks) for t in toks):
            return True
    return False


def classify_file(relpath, text, declared):
    """Tie a source file to the declared-live surface list.

    Returns {declaredLive, surface, dimension, confidence, matchEvidence}.
    Fail-open: no match -> declaredLive False (see module docstring).
    """
    if is_deferred(relpath, declared):
        return {
            "declaredLive": False, "surface": None, "dimension": None,
            "confidence": "high", "declaredMatches": [],
            "matchEvidence": "surface is explicitly deferred / wontHave - out of scope",
        }

    matches = []
    for el in declared.get("elements") or []:
        matched, conf, ev = match_element(relpath, text, el)
        if matched:
            matches.append((el, conf, ev))

    if not matches:
        return {
            "declaredLive": False, "surface": None, "dimension": None,
            "confidence": "low", "declaredMatches": [],
            "matchEvidence": "no declared-live surface matched this file",
        }

    # ANY match makes the file declared-live. Which surface to LABEL it with is a
    # separate question: prefer the dimensions that are themselves surfaces a seam
    # can sit ON (an app screen, a route file) over ones the file merely
    # REFERENCES (a datastore named in a TODO is evidence of relevance, but the
    # seam is on the dashboard, not on the view it fails to query). Dimension
    # priority leads; confidence only breaks ties within a dimension.
    dim_priority = {"applications": 3, "contracts": 2, "datastores": 1, "integrations": 0}
    conf_rank = {"high": 3, "med": 2, "low": 1}
    el, conf, ev = max(
        matches,
        key=lambda m: (dim_priority.get(m[0]["dimension"], 0), conf_rank[m[1]]),
    )
    return {
        "declaredLive": True,
        "surface": el["name"],
        "dimension": el["dimension"],
        "confidence": conf,
        "declaredMatches": sorted({m[0]["name"] for m in matches}),
        "matchEvidence": ev,
    }
