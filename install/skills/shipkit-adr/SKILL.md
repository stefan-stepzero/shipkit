---
name: shipkit-adr
description: "Land one architecture decision atomically: full entry to architecture-archive.json, hard-capped lean entry to architecture.json. Handles new decisions, supersession, amendment. Triggers: 'record this decision', 'log an ADR', 'we decided', 'supersede ADR', 'that replaces the earlier decision'."
argument-hint: "[decision summary]"
allowed-tools: Read, Edit, Write
effort: low
---

# shipkit-adr - Land a Decision Atomically

**Purpose**: Record one architecture decision the moment it's made — as a single atomic transaction across both decision files, with a hard length cap on what enters the always-loaded lean index.

**Why this exists**: `architecture.json` is `@`-imported into CLAUDE.md, so every byte of it loads into every session. The moment a decision gets recorded is exactly when a long rationale is freshest and most tempting to paste in. This skill enforces the lean/archive split at that moment: full reasoning is preserved (archive), context stays cheap (lean).

**Output**: One entry appended to `.shipkit/architecture-archive.json` (full) + the capped projection in `.shipkit/architecture.json` (lean).

---

## When to Invoke

**User triggers**:
- "Record this decision" / "log an ADR"
- "We decided X" (after a decision is settled in conversation)
- "ADR-NNN is superseded by this" / "that replaces the earlier decision"
- "Amend ADR-NNN"

**Agent triggers**: Any skill or agent that has just made an architecture-level decision mid-work lands it here instead of hand-editing `architecture.json`.

---

## Prerequisites

None. If either decision file is missing, this skill initializes it (schemas below). The canonical convention both files follow is `shipkit-engineering-definition/references/architecture-log-schema.md` — read it for edge cases; the operative rules are inlined here.

---

## Hard Caps (non-negotiable)

What enters the **lean** file is capped. Full text always survives in the archive — leaning relocates information, it never loses it.

| Lean field | Cap |
|---|---|
| `decision` | one line, ≤ 120 chars |
| `rationale` | one line, ≤ 160 chars |
| superseded entry | stub only: `{ id, status, supersededBy, decision }` — nothing else |

If the user's phrasing exceeds a cap, compress it for the lean file and put the full text in the archive entry. Never widen the cap; never put `alternatives` in the lean file.

---

## Process

### Step 1: Capture the decision

From the conversation (or `$ARGUMENTS`), establish:
- **decision** — what was decided (one line)
- **rationale** — why (full form for archive; one-line form for lean)
- **alternatives** — what was considered and rejected (archive only; may be empty)
- **scope** — `cross-cutting` or `mechanism:M-NNN`
- **relationship** — is this NEW, does it SUPERSEDE an existing ADR, or AMEND one? Supersession is marked explicitly here, at write time — it is never auto-detected later.

Ask only for what the conversation hasn't already settled (usually nothing or one question).

### Step 2: Read both files, allocate the ID

Read `.shipkit/architecture.json` and `.shipkit/architecture-archive.json`. New ID = max ADR number seen in **either** file + 1 (scanning both self-heals any drift from a previously interrupted write). If a file is missing, initialize it with the schema skeleton below before proceeding.

### Step 3: Archive first (full entry)

Append to `architecture-archive.json` `decisions[]`:

```json
{ "id": "ADR-NNN", "status": "active", "decision": "...", "rationale": "full — as long as needed",
  "alternatives": ["..."], "scope": "...", "date": "YYYY-MM-DD" }
```

- **Supersession**: new entry also gets `"supersedes": "ADR-MMM"`; set ADR-MMM's `"status": "superseded"`, `"supersededBy": "ADR-NNN"` — keep its full body.
- **Amendment**: new entry appended; ADR-MMM gets `"amendedBy": ["ADR-NNN", ...]` and **stays** `active`.
- Archive is append-only: never delete an entry, never change an original `date`.

### Step 4: Then lean (capped projection)

Update `architecture.json` `decisions[]`:

- New/amending ADR → append `{ "id", "decision", "rationale" (one line), "scope", "date" }` within the caps above.
- **Supersession** → also collapse ADR-MMM to the stub: `{ "id": "ADR-MMM", "status": "superseded", "supersededBy": "ADR-NNN", "decision": "<one line>" }`.
- **Amendment** → ADR-MMM keeps its capped active form; it is NOT stubbed.

Recompute `lastUpdated` on **both** files.

Ordering is the crash-safety guarantee: archive-first means an interrupted run can only leave the archive ahead of the lean file — nothing is lost, and the next run's Step 2 (max-ID across both) reconciles.

### Step 5: Budget check + confirm

If `architecture.json` now exceeds ~10 KB (the session-start hook's budget), tell the user: it's time to supersede/stub stale decisions or run the one-time `migrate-architecture-log.py` splitter.

Confirm in one line: `ADR-NNN landed: <decision> (supersedes ADR-MMM, lean 4.1 KB)`.

---

## File skeletons (only when initializing a missing file)

`architecture.json`: `{ "$schema": "shipkit-artifact", "type": "architecture-decisions", "version": "1.0", "lastUpdated": "...", "source": "shipkit-adr", "note": "Lean active-decisions index. Full ADR bodies live in .shipkit/architecture-archive.json — read on demand.", "decisions": [], "patterns": [], "constraints": [] }`

`architecture-archive.json`: same shape with `"type": "architecture-decisions-archive"` and the note pointing the other way.

---

## When This Skill Integrates with Others

### Before This Skill
- Nothing required — this is the moment-of-decision capture path. For deriving a full decision log from an engineering blueprint, that's `/shipkit-engineering-definition` (the primary writer), not this.

<!-- SECTION:after-completion -->
### After This Skill
- If the decision changes the current-state architecture, refresh `/shipkit-architecture-map`.
- If the lean file is over budget, run the `migrate-architecture-log.py` splitter (opt-in, dry-run by default).
<!-- /SECTION:after-completion -->

---

## Context Files This Skill Reads

- `.shipkit/architecture.json` — current lean index (ID allocation, supersession targets)
- `.shipkit/architecture-archive.json` — full log (ID allocation, prior bodies)

## Context Files This Skill Writes

- `.shipkit/architecture-archive.json` — **APPEND** (full entry; status/link updates on related entries only)
- `.shipkit/architecture.json` — **EDIT** (append capped entry; collapse superseded entries to stubs; `lastUpdated`)
  - **Write strategy**: targeted Edit calls per the Structured Artifact Updates rule — never a script.
