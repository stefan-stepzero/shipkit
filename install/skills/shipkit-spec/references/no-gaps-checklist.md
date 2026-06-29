# No-Gaps Completeness Gate

**What it prevents**: a spec that looks complete (scenarios, edge cases, acceptance criteria all filled) but is **green-but-not-functional** — it describes a UI that calls an endpoint nobody specified, saves to a table nobody created, or leans on a service nobody named. The feature passes its own checklist and still can't run end to end.

This gate runs as part of **Step 5 (Validate Completeness)**. A spec is **not done while any element is FLAGGED**.

---

## The four dimensions

Before a spec is done, enumerate what the feature **implies** across four functional dimensions, then account for every implied element. The point is not to design these — it's to make sure none is silently missing.

| Dimension | The question | Implied by |
|-----------|--------------|------------|
| **Applications** | What runnable surfaces does this feature need to exist? (web UI, API service, background worker, CLI, mobile app) | A scenario that renders something implies a UI surface; one that serves data implies a service. |
| **Datastores** | What persistent stores does it read or write? (tables, collections, buckets, caches, queues) | Any `then` that saves, lists, updates, deletes, or "remembers" data. |
| **Contracts** | What APIs / function signatures / events / message schemas connect the surfaces? | **Every UI action that fetches or mutates data implies a contract on the other side.** This is the load-bearing dimension. |
| **Integrations** | What external services / third-party APIs / auth providers / infra does it depend on? | Auth, payments, email, storage, LLM APIs, any "via X" in the spec. |

---

## The mechanism: propose → classify → resolve

### 1. Propose the implied elements

Derive the implied inventory from three sources (use whichever exist):

- **The spec's own text** — `scenarios` (given/when/then), `technical` (databaseChanges, apiEndpoints, notes), `acceptanceCriteria`, `dependencies`. This is always available.
- **`.shipkit/architecture-map.json`** — the current-state map of apps / datastores / contracts / integrations. Tells you what already exists, so an implied element is "covered by what's there" rather than missing.
- **`.shipkit/engineering-definition.json`** — declared mechanisms and components, the intended-build surface.

### 2. Classify every implied element

| Verdict | Meaning | Blocks done? |
|---------|---------|--------------|
| **COVERED** | Named in the spec (e.g. in `technical.apiEndpoints` / `databaseChanges` / `dependencies`) **or** already exists in `architecture-map.json`. | No |
| **FLAGGED** | Implied by the spec but **named nowhere** and **not in the current architecture**. A real gap. | **Yes** |
| **EXPLICITLY-DEFERRED** | Out of scope this iteration — **named, with a reason** (typically traced to `acceptanceCriteria.wontHave` or `outOfScope`). | No |

**A spec is done only when FLAGGED = 0.** Every implied element is either covered or deferred-with-reason. Nothing dropped in silence.

### 3. The frontend-implies-backend catch (the most common gap)

Walk every scenario's `when` and `then`. For each action that **displays, fetches, lists, saves, updates, or deletes** data:

- Is there a **contract** (endpoint / function / event) that serves it? If not → **FLAGGED**.
- Is there a **datastore** that holds it? If not → **FLAGGED**.

A read-only "view shared recipe" screen with no `GET` endpoint and no row to read is the textbook failure this catch exists for. A UI that "saves your preferences" with no store and no write contract is the same class. Don't let a frontend imply a backend that the spec never names.

---

## Propose, don't interrogate

Surface the result as a **filled-in proposal**, not a questionnaire. State what the feature implies, mark what's already covered, and put **only the FLAGGED items** in front of the user — each with a one-line proposed resolution:

> *This feature implies a web UI + an API service (both exist), a `share_links` table (you've specced it), and 3 endpoints (specced). One gap: the "view shared recipe" screen reads recipe data but no public read endpoint is named. **Proposed:** add `GET /api/share/{token}`. Name it, or defer the public-view path with a reason.*

The user resolves a FLAGGED item by either (a) **naming it** (it moves to COVERED — add it to `technical`), or (b) **deferring it with a reason** (it moves to EXPLICITLY-DEFERRED). Don't ask about things already covered.

---

## Greenfield graceful-degrade

If `.shipkit/architecture-map.json` is absent or thin (new project, nothing built yet):

- **Don't fail.** Derive the four dimensions from the spec text + `engineering-definition.json` + `stack.json` alone.
- **FLAGGED still applies** — a spec that implies a backend but names no contract or store is FLAGGED whether or not a current-state map exists. The gate's value is highest greenfield, where there's no existing code to paper over the gap.
- **Skip the "already exists" branch** of COVERED (there's nothing to cross-check against) and record `architectureMapUsed: false`, `confidence: "reduced"` in the gap report so downstream readers know the map wasn't consulted.

---

## Output

Record the result on the spec artifact (see `output-schema.md`):

- **`functionalSurface`** — `applications[] / datastores[] / contracts[] / integrations[]`, each element `{ name, kind, verdict, evidence }`.
- **`gapReport`** — `{ status: "clear" | "flagged", dimensions: {...}, flagged: [...], architectureMapUsed, confidence }`.
- **`deferred`** — `[ { dimension, element, reason } ]`.

A spec written to `todo/` must have `gapReport.status: "clear"` (FLAGGED = 0). If items remain flagged, the spec is incomplete — surface them and resolve before saving.
