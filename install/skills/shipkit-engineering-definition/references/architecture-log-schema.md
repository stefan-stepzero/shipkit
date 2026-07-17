# Architecture Decisions Log — Lean Index + Full Archive (canonical convention)

This is the **single, canonical** definition of how Shipkit stores architecture decisions
(ADRs). Every skill or agent that writes `architecture.json` MUST follow the dual-write rule
below. It exists once, here, and is referenced by:

- `shipkit-engineering-definition` (primary writer — derives the log from the engineering definition)
- `shipkit-design-system` (writes the `designSystem` summary into the lean file)
- `shipkit-architect-agent` (writes decisions mid-team)

> Scope note: this is the **decisions LOG** (`architecture.json` — the *why*). It is a
> different artefact from `architecture-map.json` (the current-state map — the *what-is*,
> owned by `shipkit-architecture-map`). Do not conflate them.

---

## Why split (the problem this solves)

`architecture.json` is **`@`-imported into CLAUDE.md**, so every byte loads into context every
session. Left append-only, it grows monotonically — every ADR ever made, each with full
`rationale` + `alternatives`, plus every fully-superseded decision. On a real project this
reached 150 KB / 55 ADRs and started crowding out the rest of the context budget. The artefact
meant to *inform* decisions began *destroying* the context that makes decisions possible.

**Fix:** keep a LEAN, governing index in context and relocate history + verbose justification
to an on-disk archive read only on demand. In-context cost then scales with the count of
**active** decisions, not total decisions ever made.

---

## The two files

| File | `@`-imported? | Holds |
|------|---------------|-------|
| `.shipkit/architecture.json` | **YES** (lean) | Active/governing ADRs (capped), superseded ADRs as one-line stubs, and the `designSystem` / `patterns` / `constraints` summaries |
| `.shipkit/architecture-archive.json` | **NO** (read on demand) | Every ADR with complete `rationale`, `alternatives`, and supersession history. Append-only — leaning never loses information, it relocates it. |

Use the name **`architecture-archive.json`** (not `architecture-log.json`). Both files live at
the top level of `.shipkit/`.

---

## Lean file schema — `.shipkit/architecture.json`

```json
{
  "$schema": "shipkit-artifact",
  "type": "architecture-decisions",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DDTHH:MM:SSZ",
  "source": "shipkit-engineering-definition",
  "note": "Lean active-decisions index. Full ADR bodies (rationale, alternatives, supersession history) live in .shipkit/architecture-archive.json — read it on demand.",
  "decisions": [
    {
      "id": "ADR-001",
      "decision": "What was decided (one line)",
      "rationale": "One-line rationale only — full rationale is in the archive",
      "scope": "cross-cutting | mechanism:M-001",
      "date": "YYYY-MM-DD"
    },
    {
      "id": "ADR-038",
      "status": "superseded",
      "supersededBy": "ADR-055",
      "decision": "One-line decision (replaced)"
    }
  ],
  "designSystem": { "tier": 0, "tierName": "Seed", "principles": ["..."], "tokenFormat": "css|tailwind", "location": ".shipkit/design-system/", "lastUpdated": "YYYY-MM-DD" },
  "patterns": ["Key architectural patterns in use"],
  "constraints": ["Technical constraints driving decisions"]
}
```

### Active ADR (capped) — fields kept in the lean file
`id`, `decision`, `scope`, `date`, and a **one-line** `rationale`. Drop `alternatives` and any
long-form rationale (they live in the archive). **Amended ADRs stay active** and keep this
capped active shape — an amendment does NOT stub them.

### Superseded ADR (stub) — the only fields kept in the lean file
```json
{ "id": "ADR-038", "status": "superseded", "supersededBy": "ADR-055", "decision": "<one line>" }
```
Nothing else. The full superseded body (rationale, alternatives) survives in the archive.

---

## Archive file schema — `.shipkit/architecture-archive.json`

```json
{
  "$schema": "shipkit-artifact",
  "type": "architecture-decisions-archive",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DDTHH:MM:SSZ",
  "source": "shipkit-engineering-definition",
  "note": "Full append-only ADR log. Complete rationale, alternatives, and supersession history for every decision ever made. NOT @-imported — read on demand when the lean architecture.json points here.",
  "decisions": [
    {
      "id": "ADR-001",
      "status": "active | superseded | amended | dormant",
      "decision": "What was decided",
      "rationale": "Full rationale — as long as needed",
      "alternatives": ["What was considered but rejected"],
      "scope": "cross-cutting | mechanism:M-001",
      "date": "YYYY-MM-DD",
      "supersedes": "ADR-038",
      "supersededBy": "ADR-055",
      "amendedBy": ["ADR-053"]
    }
  ],
  "patterns": ["..."],
  "constraints": ["..."]
}
```

`supersedes` / `supersededBy` / `amendedBy` are present only on the ADRs that participate in
those relationships. Archive entries are never deleted — superseding/amending sets status and
the link fields, it does not remove the old body.

---

## The dual-write rule (apply on EVERY ADR write)

Whenever a writer adds or changes an ADR:

1. **Archive first (full).** Write/append the complete entry to
   `.shipkit/architecture-archive.json` — full `rationale`, full `alternatives`, `status`, and
   any supersession/amendment links. Append-only: never delete an entry; preserve original
   `date`.
2. **Then lean (capped).** Write the capped projection into `.shipkit/architecture.json`:
   - **active or amended** ADR → `{ id, decision, scope, date, rationale(one line) }`
   - **superseded** ADR → stub `{ id, status:"superseded", supersededBy, decision(one line) }`

Recompute `lastUpdated` on both files each write.

### On a NEW ADR
- Archive: append full entry with `status:"active"`.
- Lean: append capped active entry.

### On SUPERSESSION (new ADR-NNN replaces ADR-MMM — writer marks this explicitly)
- Archive: append ADR-NNN full body with `"supersedes": "ADR-MMM"`; set ADR-MMM
  `"status":"superseded"`, `"supersededBy":"ADR-NNN"` (keep ADR-MMM's full body).
- Lean: append ADR-NNN capped; **collapse ADR-MMM to a one-line stub** (drop its rationale,
  alternatives — they remain in the archive).

### On AMENDMENT (new ADR-NNN amends ADR-MMM — partial change, MMM still governs)
- Archive: append ADR-NNN full body; set ADR-MMM `"amendedBy":["ADR-NNN", ...]` but keep
  `status` active.
- Lean: append ADR-NNN capped; **ADR-MMM stays active (capped form), NOT stubbed.**

> Supersession is marked explicitly by the writer at the moment the new ADR is created.
> Shipkit does not auto-detect it.

---

## ED↔ADR staleness signal (mechanism linkage)

**Problem this closes:** the `engineering-definition.json` is regenerated by a full skill
invocation, but ADRs land append-on-decision — often several a day. On a real build the ED
described the old auth mechanism for **three weeks** while the ADR log (the only artefact that
kept pace) had already superseded it. Nothing flagged the divergence, so fresh sessions kept
building against a stale ED. This convention makes that divergence *detectable and surfaced*.

**The linkage is the ADR `scope` field — no new link is introduced.** An ADR that governs a
mechanism already records `scope: "mechanism:M-###"` (the same id the ED mechanism carries).
That id IS the join between the decisions log and the engineering definition.

**Lean, additive rules:**

1. **When an ADR supersedes / retires / amends a mechanism's decision, it MUST carry that
   mechanism's scope** (`scope: "mechanism:M-###"`). This is already the convention for the
   original decision — keep it on the superseding/amending ADR too, so the mechanism stays
   traceable through the change.
2. **`dormant` is an allowed lean status** alongside `active | superseded | amended` — use it
   for a mechanism whose decision is retired but not directly replaced (the "DORMANT" case).
   Additive: readers that don't know it treat it as any non-active status.
3. **An ED mechanism MAY acknowledge the divergence** with two optional fields, added when a
   session reconciles rather than reasserts the old approach:
   - `supersededByADR: "ADR-###"` — this mechanism's ED description is intentionally demoted;
     the named ADR (and the ADR log generally) is the live authority.
   - `staleSince: "YYYY-MM-DD"` — optional date the divergence was acknowledged.
   Both are optional and additive; absence just means "not yet acknowledged".

**The divergence rule (computed, deterministic):**

> An ED mechanism `M-###` is **stale vs the ADR log** when the ADR archive contains a decision
> scoped to it (`scope: "mechanism:M-###"`) whose `status` is `superseded` / `dormant` /
> `deprecated`, **or** which carries an `amendedBy` link — **and** the ED mechanism does not
> already acknowledge it via `supersededByADR` / `staleSince`.

**Where it surfaces:** the `shipkit-session-start` hook computes this every session (no LLM,
reads `architecture-archive.json` — the full bodies retain scope + status + links) and emits a
one-line warning: *"engineering-definition has N mechanism(s) stale vs the ADR log (M-006, …) —
reconcile before building against them."* The check reads the **archive** because the lean
`architecture.json` superseded-stub drops `scope`; the archive is the authoritative source and
the ED writer dual-writes it on every ADR.

**Reconciliation** is either: re-run `/shipkit-engineering-definition` to bring the mechanism
back in step with the decision, **or** stamp the mechanism `supersededByADR` to record that the
ADR log is now the authority for it (the retro's "demote the ED, point at the ADR log" path).

---

## Net effect / invariants

- In-context footprint scales with **active** ADR count; each superseded ADR costs ~one line.
- **No information is lost**: every field dropped from the lean file exists in the archive.
- Only `architecture.json` is `@`-imported; `architecture-archive.json` is read on demand
  (e.g. when you need an ADR's rejected alternatives or the full chain behind a stub).

---

## One-time migration (OPT-IN — never auto-run)

For a project whose `architecture.json` is already fat (full bodies for every ADR, superseded
ones not yet stubbed), run the migrator once to split + lean it. It is **opt-in**: nothing runs
it automatically; the owner invokes it when ready. It is non-destructive (writes the archive,
then rewrites the lean file; pass `--apply` to actually write — default is a dry-run preview).

```
python install/shared/scripts/python/migrate-architecture-log.py \
    --shipkit-dir /path/to/project/.shipkit            # dry-run: prints before/after sizes
python install/shared/scripts/python/migrate-architecture-log.py \
    --shipkit-dir /path/to/project/.shipkit --apply    # writes architecture.json + architecture-archive.json
```

What it does:
1. Reads `.shipkit/architecture.json` (and merges any existing `architecture-archive.json`,
   preferring the fuller body per `id`).
2. Writes the full set to `architecture-archive.json` (append-only union by `id`).
3. Rewrites `architecture.json` lean: capped active/amended entries; superseded entries
   collapsed to stubs; `designSystem` / `patterns` / `constraints` preserved.

A decision is treated as superseded when it already carries `status:"superseded"` +
`supersededBy` (the migrator does not invent supersession links — out of scope, per the spec).
