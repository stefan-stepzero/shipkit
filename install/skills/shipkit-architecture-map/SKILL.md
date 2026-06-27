---
name: shipkit-architecture-map
description: "Maintain a code-derived 'current belief of the system architecture' map — key applications, datastores, contracts, and integration points. Triggers: 'map architecture', 'architecture map', 'what does the system look like', 'refresh architecture map'."
context: fork
model: sonnet
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Write
effort: medium
---

# shipkit-architecture-map — Living Architecture Map

**Purpose**: Maintain `.shipkit/architecture-map.json` — a continuously-refreshable, code-derived answer to *"what does the system currently look like?"* (applications, datastores, contracts, integrations). It is the **what-is** map.

**This is distinct from `.shipkit/architecture.json`**, which is the **why** — the append-only decisions log. This skill never reads or writes `architecture.json`; the two artefacts coexist (decisions vs current-state).

---

## When to Invoke

**User triggers**:
- "Map the architecture"
- "What does the system currently look like?"
- "Refresh the architecture map"
- "Show me applications / datastores / contracts / integrations"

**Auto-suggested when**:
- No `.shipkit/architecture-map.json` exists and the repo has real source code
- The existing map is older than **14 days** (staleness)
- A major structural change landed (new service, new datastore, new external integration)

---

## What This Map Contains

| Section | What it captures | ID prefix |
|---------|------------------|-----------|
| `applications` | Deployable/runnable units: services, frontends, workers, CLIs, libraries | `APP-NNN` |
| `datastores` | Persistence: postgres, redis, s3, sqlite, mongo, etc. | `DS-NNN` |
| `contracts` | Interface/data shapes at boundaries: REST/GraphQL routes, events, RPC, shared types | `CON-NNN` |
| `integrations` | External systems: third-party APIs, webhooks, queues, SaaS | `INT-NNN` |

IDs are **stable cross-references**: `datastores[].ownedBy` points at an `APP-NNN`, `contracts[].boundary` names `APP-NNN -> APP-NNN`, `integrations[].usedBy` points at an `APP-NNN`.

**Full schema:** `references/output-schema.md` · **Realistic example:** `references/example.json`

---

## Process

### Completion Tracking (MANDATORY)

Before starting, create one task per section so coverage is provable:

1. `TaskCreate`: "Staleness check + load prior map (preserve IDs)"
2. `TaskCreate`: "Read upstream hints (codebase-index, engineering-definition)"
3. `TaskCreate`: "Derive applications (APP-*)"
4. `TaskCreate`: "Derive datastores (DS-*)"
5. `TaskCreate`: "Derive contracts (CON-*)"
6. `TaskCreate`: "Derive integrations (INT-*)"
7. `TaskCreate`: "Write architecture-map.json (replace)"
8. `TaskCreate`: "Verify cross-references resolve + no empty required sections"

**Rules**:
- `TaskUpdate` to `completed` only after the section holds verified, code-grounded data — not guesses.
- The final task requires re-reading the written file and confirming every `ownedBy` / `usedBy` / `boundary` reference points at an ID that exists in the map.
- An entity you cannot ground in a file/config gets `"confidence": "inferred"` rather than being asserted as fact.

### Step 0: Staleness Check & ID Preservation

```bash
# Does a map already exist, and how old is it?
ls -la .shipkit/architecture-map.json 2>/dev/null
```

- **If it exists**: `Read` it first. This run is **replace-on-rerun** (the file is rewritten whole), but **reuse existing IDs** for entities that still exist so cross-references and external citations stay stable. Allocate new IDs (next free number per prefix) only for genuinely new entities. Do not renumber survivors.
- **If absent**: start IDs at `APP-001`, `DS-001`, `CON-001`, `INT-001`.

If the map exists and is **less than 14 days old**, tell the user the age and ask whether to refresh anyway (a structural change may justify it) before doing the full scan.

### Step 1: Read Upstream Hints (context-derived layer)

Read these if present — they are *hints*, not the source of truth. The source of truth is the code.

- `.shipkit/codebase-index.json` — `framework`, `entryPoints`, `concepts` (database/payments/api), `directories`. Maps concepts to files fast.
- `.shipkit/engineering-definition.json` — `components[]`, declared mechanisms, intended data contracts, chosen stack. Names the *intended* architecture; reconcile it against what the code actually shows.

Note any drift between intent (engineering-definition) and reality (code) in the relevant entity's `notes`.

### Step 2: Derive from Code (primary source)

Scan the actual repo. Use the codebase-index `skip`/`concepts` to avoid wasted exploration. For a large repo, dispatch an `Explore` subagent per section to scan in parallel.

**Applications (APP-*)** — find runnable/deployable units:
- Package manifests: `package.json` (per workspace/monorepo package), `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`
- Entry points: `main`/`index`/`app` files, `src/app` (Next.js), `cmd/` (Go), `__main__.py`, server bootstraps, worker/queue consumers, CLI entrypoints (`bin`, `scripts`)
- Containerisation: `Dockerfile`, `docker-compose.yml` services, `Procfile`
- Classify `kind`: `service` | `frontend` | `worker` | `cli` | `lib`

**Datastores (DS-*)** — find persistence:
- Schema/migration files: `schema.prisma`, `migrations/`, `*.sql`, `alembic/`, `drizzle/`
- Connection config: `DATABASE_URL`, redis/mongo/s3 clients, ORM configs
- `docker-compose.yml` data services (postgres, redis, mysql, mongo, minio)
- Classify `kind` (postgres/redis/s3/sqlite/...) and set `ownedBy` to the APP that connects to it

**Contracts (CON-*)** — find boundary shapes:
- HTTP routes/handlers: `src/app/api/**/route.ts`, Express/Fastify routers, FastAPI/Flask routes, controllers
- GraphQL: `schema.graphql`, resolvers
- Events/queues: publish/subscribe, topic/queue names
- Shared types at boundaries: Zod schemas, TS interfaces, JSON Schema, protobuf
- Set `boundary` (`APP-A -> APP-B`, or `external -> APP-A` for inbound public APIs), `kind` (rest/graphql/event/rpc/fn), and `shape` (a path to the schema/type, or a short description)

**Integrations (INT-*)** — find external systems:
- Third-party SDK imports (stripe, twilio, openai, sendgrid, aws-sdk, etc.)
- Outbound HTTP base URLs, webhook receivers, OAuth providers
- Message brokers / external queues
- Set `direction` (inbound/outbound), `kind` (external-api/webhook/queue/saas), `usedBy`

### Step 3: Verification Before Asserting

| Claim | Required check |
|-------|----------------|
| "Application X exists" | A manifest/entrypoint/Dockerfile file is read and confirms a runnable unit |
| "Datastore Y is used" | A schema, migration, client init, or compose service is found |
| "Contract Z at boundary" | The route/handler/schema file is read and the shape located |
| "Integration W" | The SDK import or outbound endpoint is found in code |

Anything that cannot be grounded gets `"confidence": "inferred"` and a `notes` line explaining the inference. Never present an inferred entity as verified.

### Step 4: Write the Map (replace-on-rerun)

Write the **complete** `.shipkit/architecture-map.json` with the Write tool (whole-file replace — do not append). Include:

```json
{
  "$schema": "shipkit-artifact",
  "type": "architecture-map",
  "version": "1.0",
  "lastUpdated": "<ISO 8601 timestamp>",
  "source": "shipkit-architecture-map",
  "applications": [],
  "datastores": [],
  "contracts": [],
  "integrations": []
}
```

If a section is genuinely empty for this repo (e.g. no external integrations), write `[]` — do not invent entries.

### Step 5: Confirm to User

```
✅ Architecture map written to .shipkit/architecture-map.json

Applications:  3 (2 service, 1 frontend)
Datastores:    2 (postgres, redis)
Contracts:     7 (5 rest, 2 event)
Integrations:  2 (stripe, sendgrid)

This is the "what-is" map (current state). The "why" decisions log
lives separately in .shipkit/architecture.json — untouched.
```

---

## Derivation Model

| Layer | Source | Role |
|-------|--------|------|
| Code scan (entrypoints, manifests, schema, routes, SDK imports) | the repo | **Primary** — ground truth |
| `codebase-index.json` | `.shipkit/` | Navigation hint (concept → files) |
| `engineering-definition.json` | `.shipkit/` | Intent hint; reconcile vs reality |
| Prior `architecture-map.json` | `.shipkit/` | ID stability across refreshes |

**Principle**: the map reflects what the code *is*, refreshed over time — not what was once designed. Where they diverge, record the divergence.

---

## Context Files This Skill Reads

- `.shipkit/codebase-index.json` — navigation hints (optional)
- `.shipkit/engineering-definition.json` — intended architecture, components (optional)
- `.shipkit/architecture-map.json` — prior run, for ID preservation (if exists)
- Actual repo source — primary derivation

**Does NOT read** `.shipkit/architecture.json` (the decisions log is a separate concern).

## Context Files This Skill Writes

- `.shipkit/architecture-map.json` — **complete replacement on each run** (replace-on-rerun, like codebase-index). IDs preserved for surviving entities.

---

## Completion Checklist

- [ ] Staleness checked; prior map loaded and IDs preserved (if any)
- [ ] Upstream hints read (codebase-index, engineering-definition) if present
- [ ] Applications derived and grounded in code
- [ ] Datastores derived and grounded in code
- [ ] Contracts derived and grounded in code
- [ ] Integrations derived and grounded in code
- [ ] Every cross-reference (`ownedBy`/`usedBy`/`boundary`) resolves to an existing ID
- [ ] Map written (whole-file replace) and re-read to verify

---

<!-- SECTION:after-completion -->
## After Completion

Architecture map written to `.shipkit/architecture-map.json`.

**Next** (the map is a current-state input for downstream work):
- `/shipkit-spec` — anchor a feature spec to the real applications/contracts it touches.
- `/shipkit-codebase-audit` — cross-check the map against the code for orphaned apps, unwired contracts, or dead integrations.
- `/shipkit-engineering-definition` — if the map reveals drift from intended architecture, revisit the engineering blueprint.

**Refresh** by re-running `/shipkit-architecture-map` after a structural change (new service, datastore, or external integration) or when the map is older than 14 days.

**Note (v1 reachability)**: this skill is standalone / user-invocable. Wiring it as an automatic input into the orchestration loops is deferred to a later iteration.
<!-- /SECTION:after-completion -->
