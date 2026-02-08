# Data Contracts Output Schema

This document defines the JSON schema for `.shipkit/contracts.json`.

## Full JSON Schema

```json
{
  "$schema": "shipkit-artifact",
  "type": "data-contracts",
  "version": "1.0",
  "lastUpdated": "2025-01-15T10:00:00Z",
  "source": "shipkit-data-contracts",
  "summary": {
    "totalEntities": 8,
    "totalRelationships": 12,
    "totalValidationRules": 15,
    "domains": ["users", "products", "orders"],
    "lastChange": "Added Order entity with Product relationship"
  },
  "entities": [
    {
      "id": "user",
      "name": "User",
      "domain": "users",
      "description": "Application user account",
      "fields": [
        {
          "name": "id",
          "type": "string",
          "format": "uuid",
          "required": true,
          "description": "Unique identifier"
        }
      ],
      "source": "database"
    }
  ],
  "relationships": [
    {
      "id": "rel-1",
      "source": "user",
      "target": "order",
      "type": "one-to-many",
      "label": "places",
      "foreignKey": "user_id",
      "cascade": "restrict"
    }
  ],
  "validationRules": [
    {
      "id": "val-1",
      "entity": "user",
      "field": "email",
      "rule": "unique",
      "errorMessage": "Email already registered",
      "scope": "global"
    }
  ],
  "apiContracts": [
    {
      "id": "api-1",
      "endpoint": "/api/users",
      "method": "POST",
      "requestEntity": "user",
      "responseEntity": "user",
      "requiredFields": ["email", "name"],
      "authentication": "required"
    }
  ]
}
```

## Field Reference

### Top-Level Fields (Shipkit JSON Artifact Convention)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `$schema` | `"shipkit-artifact"` | yes | Always this literal value |
| `type` | `"data-contracts"` | yes | Artifact type identifier |
| `version` | `string` | yes | Schema version (currently `"1.0"`) |
| `lastUpdated` | `string` | yes | ISO 8601 datetime of last modification |
| `source` | `"shipkit-data-contracts"` | yes | Skill that wrote this file |
| `summary` | `object` | yes | Aggregated data for dashboard cards |

### Summary Object

| Field | Type | Description |
|-------|------|-------------|
| `totalEntities` | `number` | Count of entities in the `entities` array |
| `totalRelationships` | `number` | Count of items in the `relationships` array |
| `totalValidationRules` | `number` | Count of items in the `validationRules` array |
| `domains` | `string[]` | Unique domain names across all entities |
| `lastChange` | `string` | Human-readable description of most recent change |

### Entity Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string` | yes | Unique entity identifier (lowercase, e.g., `"user"`) |
| `name` | `string` | yes | Display name (PascalCase, e.g., `"User"`) |
| `domain` | `string` | yes | Domain grouping (e.g., `"users"`, `"products"`) |
| `description` | `string` | yes | What this entity represents |
| `fields` | `Field[]` | yes | Array of field definitions |
| `source` | `string` | no | Where entity originates (`"database"`, `"api"`, `"derived"`) |

### Field Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | yes | Field name (snake_case, matches database columns) |
| `type` | `string` | yes | Data type (`"string"`, `"number"`, `"boolean"`, `"object"`, `"array"`) |
| `format` | `string` | no | Format hint (`"uuid"`, `"email"`, `"datetime"`, `"url"`, `"uri"`) |
| `required` | `boolean` | yes | Whether this field is required |
| `unique` | `boolean` | no | Whether this field must be unique |
| `description` | `string` | no | Field description |
| `validation` | `string` | no | Human-readable validation rule summary |
| `default` | `any` | no | Default value if not provided |
| `nullable` | `boolean` | no | Whether this field can be null (default: false) |

### Relationship Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string` | yes | Unique relationship identifier (e.g., `"rel-1"`) |
| `source` | `string` | yes | Source entity id |
| `target` | `string` | yes | Target entity id |
| `type` | `string` | yes | Cardinality: `"one-to-one"`, `"one-to-many"`, `"many-to-many"` |
| `label` | `string` | yes | Relationship verb (e.g., `"places"`, `"contains"`, `"belongs to"`) |
| `foreignKey` | `string` | no | Foreign key field name |
| `cascade` | `string` | no | Cascade behavior: `"cascade"`, `"restrict"`, `"set-null"` |

### Validation Rule Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string` | yes | Unique rule identifier (e.g., `"val-1"`) |
| `entity` | `string` | yes | Entity id this rule applies to |
| `field` | `string` | yes | Field name this rule applies to |
| `rule` | `string` | yes | Rule type (`"unique"`, `"min"`, `"max"`, `"pattern"`, `"custom"`) |
| `errorMessage` | `string` | yes | User-facing error message |
| `scope` | `string` | no | Rule scope: `"global"`, `"per-tenant"` |
| `params` | `object` | no | Rule parameters (e.g., `{"min": 3, "max": 100}` for length rules) |

### API Contract Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string` | yes | Unique contract identifier (e.g., `"api-1"`) |
| `endpoint` | `string` | yes | API endpoint path |
| `method` | `string` | yes | HTTP method (`"GET"`, `"POST"`, `"PUT"`, `"PATCH"`, `"DELETE"`) |
| `requestEntity` | `string` | no | Entity id for request body |
| `responseEntity` | `string` | no | Entity id for response body |
| `requiredFields` | `string[]` | no | Fields required in request (subset of entity fields) |
| `authentication` | `string` | no | Auth requirement: `"required"`, `"optional"`, `"none"` |

## Entity Naming Conventions

- `id` is lowercase singular (e.g., `"user"`, `"order"`)
- `name` is PascalCase (e.g., `"User"`, `"Order"`)
- Field names are snake_case (matches database columns)

## Relationship ID Convention

Use `"rel-{source}-{target}"` for clarity.

Use descriptive `label` verbs that read naturally:
- "User **creates** Recipe"
- "Order **contains** LineItem"

## Validation Rule Types

| Rule | Description | Params Example |
|------|-------------|----------------|
| `unique` | Value must be unique | - |
| `min` | Minimum value/length | `{"min": 8}` |
| `max` | Maximum value/length | `{"max": 100}` |
| `pattern` | Regex pattern match | `{"pattern": "^[a-z]+$"}` |
| `range` | Value in range | `{"min": 1, "max": 10}` |
| `enum` | Value in list | `{"values": ["a", "b", "c"]}` |
| `custom` | Custom validation | `{"fn": "validateFoo"}` |

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

The entity-relationship structure is designed for ER diagram rendering and dashboard summaries.
