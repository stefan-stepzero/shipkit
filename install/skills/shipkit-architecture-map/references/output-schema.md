# Architecture Map Schema Reference

This document defines the JSON schema for `.shipkit/architecture-map.json` — the code-derived,
refreshable "current belief of the system architecture" (the **what-is** map).

It is a *separate artefact* from `.shipkit/architecture.json` (the **why** — append-only decisions
log). This map never touches that file.

## JSON Schema

```json
{
  "$schema": "shipkit-artifact",
  "type": "architecture-map",
  "version": "1.0",
  "lastUpdated": "2026-06-27T14:30:00Z",
  "source": "shipkit-architecture-map",

  "applications": [
    {
      "id": "APP-001",
      "name": "web",
      "responsibility": "User-facing Next.js app + API routes",
      "kind": "frontend",
      "path": "apps/web",
      "confidence": "verified",
      "notes": ""
    }
  ],

  "datastores": [
    {
      "id": "DS-001",
      "name": "app-db",
      "kind": "postgres",
      "purpose": "Primary relational store (users, orders)",
      "ownedBy": "APP-001",
      "evidence": "prisma/schema.prisma",
      "confidence": "verified"
    }
  ],

  "contracts": [
    {
      "id": "CON-001",
      "name": "POST /api/checkout",
      "boundary": "external -> APP-001",
      "shape": "src/app/api/checkout/route.ts (Zod CheckoutInput)",
      "kind": "rest",
      "confidence": "verified"
    }
  ],

  "integrations": [
    {
      "id": "INT-001",
      "name": "Stripe",
      "direction": "outbound",
      "kind": "saas",
      "usedBy": "APP-001",
      "evidence": "src/lib/stripe.ts",
      "confidence": "verified"
    }
  ]
}
```

## Field Reference

### Top-level Metadata

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `$schema` | string | Yes | Constant: `"shipkit-artifact"` |
| `type` | string | Yes | Constant: `"architecture-map"` |
| `version` | string | Yes | Schema version (`"1.0"`) |
| `lastUpdated` | string | Yes | ISO 8601 timestamp of the run that wrote this file |
| `source` | string | Yes | Maintaining skill: `"shipkit-architecture-map"` |

### `applications[]` (APP-NNN)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Stable ID `APP-NNN`. Preserved across refreshes for surviving units. |
| `name` | string | Yes | Short name (package/service name) |
| `responsibility` | string | Yes | One line: what this unit does |
| `kind` | enum | Yes | `service` \| `frontend` \| `worker` \| `cli` \| `lib` |
| `path` | string | No | Repo-relative path to the unit's root |
| `confidence` | enum | No | `verified` \| `inferred` (default `verified`) |
| `notes` | string | No | Drift vs engineering-definition, caveats |

### `datastores[]` (DS-NNN)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Stable ID `DS-NNN` |
| `name` | string | Yes | Logical store name |
| `kind` | string | Yes | `postgres` \| `redis` \| `s3` \| `sqlite` \| `mysql` \| `mongo` \| ... |
| `purpose` | string | Yes | What it stores / why it exists |
| `ownedBy` | string | Yes | Cross-reference to an `APP-NNN` that owns/connects to it |
| `evidence` | string | No | File grounding the claim (schema, client init, compose service) |
| `confidence` | enum | No | `verified` \| `inferred` |

### `contracts[]` (CON-NNN)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Stable ID `CON-NNN` |
| `name` | string | Yes | Contract name (route, event topic, RPC method) |
| `boundary` | string | Yes | `APP-A -> APP-B`, or `external -> APP-A` for inbound public APIs |
| `shape` | string | Yes | Schema/type path (Zod/TS/JSON Schema/protobuf) or short description |
| `kind` | enum | Yes | `rest` \| `graphql` \| `event` \| `rpc` \| `fn` |
| `confidence` | enum | No | `verified` \| `inferred` |

### `integrations[]` (INT-NNN)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Stable ID `INT-NNN` |
| `name` | string | Yes | External system name (Stripe, SendGrid, OpenAI, ...) |
| `direction` | enum | Yes | `inbound` \| `outbound` |
| `kind` | enum | Yes | `external-api` \| `webhook` \| `queue` \| `saas` |
| `usedBy` | string | Yes | Cross-reference to the `APP-NNN` that uses it |
| `evidence` | string | No | File grounding the claim (SDK import, outbound URL) |
| `confidence` | enum | No | `verified` \| `inferred` |

## Cross-Reference Integrity

These references MUST resolve to an ID that exists in the same file:

| Field | Points at |
|-------|-----------|
| `datastores[].ownedBy` | an `applications[].id` |
| `contracts[].boundary` | one or two `applications[].id` (or the literal `external`) |
| `integrations[].usedBy` | an `applications[].id` |

The maintaining skill re-reads the written file and confirms every reference resolves before
declaring done.

## ID Stability (replace-on-rerun)

The file is rewritten whole on each run, but IDs are **stable**: the skill reads the prior map and
reuses the existing ID for any entity that still exists, allocating the next free number only for
new entities. This lets specs, docs, and reviews cite `APP-002` / `CON-005` durably across refreshes.

## Coexistence with `architecture.json`

| Artefact | Question it answers | Maintained by | Strategy |
|----------|---------------------|---------------|----------|
| `architecture-map.json` | What does the system look like *now*? | `shipkit-architecture-map` | code-derived, replace-on-rerun, 14-day staleness |
| `architecture.json` | *Why* did we decide X? | `shipkit-engineering-definition` | decisions log, append-only |

This skill does not read or write `architecture.json`.
