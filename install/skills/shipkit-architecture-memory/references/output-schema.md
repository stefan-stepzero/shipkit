# Architecture Memory Output Schema

This document defines the JSON schema for `.shipkit/architecture.json`.

## Full JSON Schema

```json
{
  "$schema": "shipkit-artifact",
  "type": "architecture",
  "version": "1.0",
  "lastUpdated": "2025-01-15T10:00:00Z",
  "source": "shipkit-architecture-memory",
  "summary": {
    "totalNodes": 12,
    "totalEdges": 18,
    "totalDecisions": 5,
    "totalConstraints": 2,
    "layers": ["frontend", "api", "database"],
    "lastDecision": "Chose PostgreSQL over MongoDB for relational data"
  },
  "nodes": [
    {
      "id": "next-app",
      "label": "Next.js App",
      "type": "service",
      "layer": "frontend",
      "description": "Main web application",
      "techStack": ["Next.js 14", "React", "TypeScript"],
      "status": "active"
    }
  ],
  "edges": [
    {
      "id": "edge-1",
      "source": "next-app",
      "target": "api-gateway",
      "label": "REST/GraphQL",
      "type": "sync",
      "protocol": "HTTPS"
    }
  ],
  "decisions": [
    {
      "id": "dec-1",
      "title": "Database Selection",
      "date": "2025-01-10",
      "status": "decided",
      "decisionType": "architectural",
      "chosen": "PostgreSQL",
      "alternatives": [
        { "name": "MongoDB", "reason": "Document model poor fit for relational data" },
        { "name": "DynamoDB", "reason": "Vendor lock-in, complex querying" }
      ],
      "rationale": "Relational data model fits our domain better",
      "affectedNodes": ["database", "api-gateway"],
      "implications": [
        "Need migration tooling (Drizzle Kit)",
        "Schema-first development",
        "Strong consistency guarantees"
      ],
      "supersedes": null,
      "tradeoffs": "Less flexible schema, but stronger consistency"
    }
  ],
  "constraints": [
    {
      "id": "con-1",
      "description": "Must support 10k concurrent users",
      "type": "performance",
      "affectedNodes": ["api-gateway", "database"]
    }
  ]
}
```

## Field Reference

### Top-Level Fields (Shipkit JSON Artifact Convention)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `$schema` | string | yes | Always `"shipkit-artifact"` |
| `type` | string | yes | Always `"architecture"` for this skill |
| `version` | string | yes | Schema version, currently `"1.0"` |
| `lastUpdated` | string | yes | ISO 8601 timestamp of last modification |
| `source` | string | yes | Always `"shipkit-architecture-memory"` |
| `summary` | object | yes | Aggregated data for dashboard cards |

### Summary Object

| Field | Type | Description |
|-------|------|-------------|
| `totalNodes` | number | Count of nodes in the graph |
| `totalEdges` | number | Count of edges in the graph |
| `totalDecisions` | number | Count of decisions logged |
| `totalConstraints` | number | Count of constraints logged |
| `layers` | string[] | Unique layer names across all nodes |
| `lastDecision` | string | Title or summary of the most recent decision |

### Node Object (Architecture Graph Vertices)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique kebab-case identifier |
| `label` | string | yes | Human-readable display name |
| `type` | string | yes | One of: `service`, `database`, `queue`, `cache`, `external`, `library`, `module` |
| `layer` | string | yes | Logical layer: `frontend`, `api`, `backend`, `database`, `infrastructure`, `external` |
| `description` | string | yes | What this component does |
| `techStack` | string[] | yes | Technologies used by this node |
| `status` | string | yes | One of: `active`, `planned`, `deprecated` |

### Edge Object (Architecture Graph Connections)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique identifier (e.g., `edge-1`) |
| `source` | string | yes | Source node `id` |
| `target` | string | yes | Target node `id` |
| `label` | string | yes | Connection description (e.g., `"REST"`, `"gRPC"`) |
| `type` | string | yes | One of: `sync`, `async`, `event`, `dependency` |
| `protocol` | string | yes | Protocol used (e.g., `"HTTPS"`, `"WebSocket"`, `"TCP"`) |

### Decision Object (Architectural Decision Records)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique identifier (e.g., `dec-1`) |
| `title` | string | yes | Concise title (5-10 words) |
| `date` | string | yes | Date in `YYYY-MM-DD` format |
| `status` | string | yes | One of: `decided`, `superseded`, `deprecated` |
| `decisionType` | string | yes | One of: `architectural`, `operational` |
| `chosen` | string | yes | What was chosen - one clear sentence |
| `alternatives` | object[] | yes | Each with `name` (string) and `reason` (string: why not chosen) |
| `rationale` | string | yes | Why this was chosen - the reasoning |
| `affectedNodes` | string[] | yes | Node `id`s affected by this decision |
| `implications` | string[] | yes | Requirements/constraints created by this decision |
| `supersedes` | string\|null | yes | `id` of superseded decision, or `null` |
| `tradeoffs` | string | yes | Key tradeoff summary |

### Constraint Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique identifier (e.g., `con-1`) |
| `description` | string | yes | What the constraint is |
| `type` | string | yes | One of: `performance`, `security`, `compliance`, `budget`, `timeline`, `technical` |
| `affectedNodes` | string[] | yes | Node `id`s affected by this constraint |

## Decision Types

| Type | Definition | Examples |
|------|------------|----------|
| **architectural** | Tech choice, pattern selection, structural decision | "Use Server Actions", "Use Drizzle ORM", "Feature folders for components" |
| **operational** | Runtime behavior, data flow rules, invariants | "Invalidate X when Y changes", "Always validate at boundary", "Cache TTL = 5min" |

**Why type matters**: Architectural decisions affect code structure. Operational decisions affect runtime behavior and must be followed during implementation.

## Decision Status Lifecycle

| Status | Meaning |
|--------|---------|
| `decided` | Active decision, still applies |
| `superseded` | Replaced by a newer decision (link via `supersedes` field in the new decision) |
| `deprecated` | No longer recommended, may still exist in codebase but should be migrated |

## ID Generation Rules

- **Decisions**: `dec-[N]` where N is the next sequential number
- **Nodes**: kebab-case descriptive name (e.g., `next-app`, `postgres-db`, `api-gateway`)
- **Edges**: `edge-[N]` where N is the next sequential number
- **Constraints**: `con-[N]` where N is the next sequential number

## Shipkit Artifact Convention

This skill follows the **Shipkit JSON artifact convention** - a standard structure for all `.shipkit/*.json` files that enables dashboard visualization.

**Every JSON artifact MUST include these top-level fields:**

```json
{
  "$schema": "shipkit-artifact",
  "type": "<artifact-type>",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DD",
  "source": "<skill-name>",
  "summary": { ... }
}
```

The graph structure (nodes + edges) is compatible with React Flow for visualization.
