---
name: shipkit-data-contracts
description: "Use when validating data shapes across layers or checking type alignment. Triggers: 'validate contracts', 'check types', 'data shape mismatch'."
---

# shipkit-data-contracts - Entity-Relationship & Validation Contract Manager

**Purpose**: Maintain canonical entity definitions, relationships, validation rules, and API contracts in a single structured JSON file (`.shipkit/contracts.json`), ensuring alignment with database schema and preventing type mismatches. The output is an entity-relationship graph ideal for ER diagram visualization.

---

## When to Invoke

**User triggers**:
- "Define types for this component"
- "What types do I need for this data?"
- "Create type for this Server Action"
- "Add validation for this form"
- "Check if types match database"

**Auto-suggest contexts**:
- After `/shipkit-project-context` generates schema.md (suggest: "Define types?")
- During `implement (no skill needed)` when user creates components with data props
- During `implement (no skill needed)` when user creates Server Actions with parameters
- When type errors occur during implementation
- After database migrations (check alignment)

---

## Prerequisites

**Optional but helpful**:
- Database schema: `.shipkit/schema.md` (from shipkit-project-context)
- Existing contracts: `.shipkit/contracts.json` (from previous runs of this skill)

**Can run standalone**: Yes - creates `contracts.json` if it doesn't exist

---

## Output Schema: `.shipkit/contracts.json`

This skill writes a **single JSON artifact** following the Shipkit JSON Artifact Convention. The schema is an entity-relationship graph designed for ER diagram rendering and dashboard summaries.

### Full Schema Reference

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
        },
        {
          "name": "email",
          "type": "string",
          "format": "email",
          "required": true,
          "unique": true,
          "validation": "RFC 5322 email format"
        },
        {
          "name": "name",
          "type": "string",
          "required": true,
          "description": "Display name"
        },
        {
          "name": "created_at",
          "type": "string",
          "format": "datetime",
          "required": true,
          "description": "ISO 8601 creation timestamp"
        },
        {
          "name": "updated_at",
          "type": "string",
          "format": "datetime",
          "required": true,
          "description": "ISO 8601 last update timestamp"
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

### Required Top-Level Fields (Shipkit JSON Artifact Convention)

| Field | Type | Description |
|-------|------|-------------|
| `$schema` | `"shipkit-artifact"` | Always this literal value |
| `type` | `"data-contracts"` | Artifact type identifier |
| `version` | `string` | Schema version (currently `"1.0"`) |
| `lastUpdated` | `string` | ISO 8601 datetime of last modification |
| `source` | `"shipkit-data-contracts"` | Skill that wrote this file |
| `summary` | `object` | Aggregated data for dashboard cards |

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

---

## Process

### Step 0: Check for Queue (Auto-Detect Mode)

**First, check if running in queue-driven mode**:

Read file (if exists): `.shipkit/.queues/define-data-contracts.md`

**If queue file exists and has pending items**:
1. Parse the `## Pending` section for data types needing validation
2. For each pending type: Check database alignment, define entity, fields, and relationships
3. Merge into `.shipkit/contracts.json`
4. Move item from Pending to Completed in queue
5. Skip Step 2 questions (types already identified)

**If queue file doesn't exist or is empty**: Continue to Step 1 (manual mode)

---

### Step 1: (Manual Mode) Read Existing Context

**Read existing definitions before asking questions**:
- `.shipkit/schema.md` - Database schema (if exists)
- `.shipkit/contracts.json` - Existing contracts (if exists)

**If contracts.json doesn't exist**: Continue to questions (will create it)

**If contracts.json exists**: Parse it to understand existing entities, relationships, and validation rules before proceeding.

---

### Step 2: Determine What Needs Typing

**Auto-detect from context when possible**: Check component code for props interface, check function parameters for input/output types.

**Ask clarifying question if unclear**:
- "What data shape does this component/action need?"
- "Is this for a component, Server Action, or both?"

---

### Step 3: Check Database Alignment

**If schema.md exists, check for alignment**:
1. Read schema.md to see database table structures
2. Compare requested entity fields with database columns
3. Detect mismatches: Fields in entity but not in database, different data types, missing nullable annotations

**IF mismatch detected**:
- Ask: "Should this align with the database schema?"
- Option A: "Adjust entity to match database?"
- Option B: "Database needs migration - add fields?"

### Verification Before Entity Definition

Before defining any entity, verify claims with tool calls:

| Claim | Required Verification |
|-------|----------------------|
| "schema.md exists" | `Read: file_path=".shipkit/schema.md"` succeeds |
| "Table X has columns" | Parse schema.md content, extract column definitions |
| "Entity aligns with schema" | Compare field names (case-sensitive) between entity and schema |
| "Existing type at path" | `Glob: pattern="**/types/*"` AND `Grep: pattern="type TypeName"` |

**Pattern Ripple for Entities:**

When documenting an entity, find ALL usages to understand impact.

**USE PARALLEL SUBAGENTS FOR ENTITY ANALYSIS** - For comprehensive type verification:

```
Launch these Task agents IN PARALLEL (single message, multiple tool calls):

1. TYPE RIPPLE AGENT (subagent_type: "Explore")
   Prompt: "Find all usages of type '[EntityName]' in the codebase.
   Report:
   - Files that import this type
   - Components using this type as props
   - Functions with this type as parameter/return
   - Other types that extend or reference this type
   For each: file path, line number, how it's used."

2. SCHEMA ALIGNMENT AGENT (subagent_type: "Explore")
   Prompt: "Check alignment between TypeScript types and database schema.
   Read .shipkit/schema.md (or prisma/schema.prisma).
   Compare field names, types, and nullability.
   Report:
   - Fields in type but not in database
   - Fields in database but not in type
   - Type mismatches (string vs number, etc.)
   - Nullable mismatches"
```

**Why parallel subagents**:
- Type ripple and schema alignment are independent checks
- Running simultaneously speeds up validation
- Each agent focuses on one concern (usage vs correctness)

**Fallback** - Manual grep:
```
1. Grep: pattern="TypeName" glob="**/*.{ts,tsx}"
2. List all files using this type
3. Verify usages match documented shape
4. Report in output: "Type used in X files: [list]"
```

**Why this matters:** Defining an entity without knowing where its type is used leads to silent breakage when the entity changes.

**Verification sequence:**

```
1. If schema.md exists:
   - Read and parse table definitions
   - Extract column names and types
2. Before creating new entity:
   - Glob: pattern="**/types/**/*.ts" to find existing types location
   - Grep: pattern="type|interface EntityName" to check if already exists
3. After defining entity:
   - Grep: pattern="EntityName" glob="**/*.{ts,tsx}" to find all usages
   - Report usage count in confirmation
4. For schema alignment:
   - Compare each field name with schema columns
   - Flag mismatches with suggested fixes
```

**See also:** `shared/references/VERIFICATION-PROTOCOL.md` for standard verification patterns.

---

### Step 4: Ask Definition Questions

**Only ask what isn't clear from context**:
- **Data shape** (if not obvious): "What fields does this entity need?"
- **Relationships** (if applicable): "How does this entity relate to others?"
- **Validation requirements** (if applicable): "What validation rules apply?"
- **API contracts** (if applicable): "What API endpoints use this entity?"
- **Alignment confirmation** (if mismatch found): "This doesn't match database schema. Should I suggest migration?"

---

### Step 5: Define Entity

**Map the data shape to an entity object in contracts.json**:

```json
{
  "id": "recipe",
  "name": "Recipe",
  "domain": "recipes",
  "description": "A cooking recipe with ingredients and steps",
  "fields": [
    { "name": "id", "type": "string", "format": "uuid", "required": true, "description": "Primary key" },
    { "name": "title", "type": "string", "required": true, "description": "Recipe title" },
    { "name": "user_id", "type": "string", "format": "uuid", "required": true, "description": "Author foreign key" },
    { "name": "created_at", "type": "string", "format": "datetime", "required": true, "description": "Creation timestamp" },
    { "name": "updated_at", "type": "string", "format": "datetime", "required": true, "description": "Last update timestamp" }
  ],
  "source": "database"
}
```

**Entity naming conventions**: `id` is lowercase singular (e.g., `"user"`, `"order"`), `name` is PascalCase (e.g., `"User"`, `"Order"`), field names are snake_case (matches database columns).

---

### Step 6: Define Relationships

**Map entity connections to relationship objects**:

```json
{
  "id": "rel-user-recipe",
  "source": "user",
  "target": "recipe",
  "type": "one-to-many",
  "label": "creates",
  "foreignKey": "user_id",
  "cascade": "cascade"
}
```

**Relationship ID convention**: `"rel-{source}-{target}"` for clarity. Use descriptive `label` verbs that read naturally: "User **creates** Recipe", "Order **contains** LineItem".

---

### Step 7: Define Validation Rules

**Map validation requirements to rule objects**:

```json
{
  "id": "val-user-email-unique",
  "entity": "user",
  "field": "email",
  "rule": "unique",
  "errorMessage": "Email already registered",
  "scope": "global"
}
```

**Rule types**: `"unique"`, `"min"`, `"max"`, `"pattern"`, `"range"`, `"enum"`, `"custom"`. Use `params` for rules that need configuration (e.g., `{"min": 8}` for password length).

---

### Step 8: Define API Contracts (if applicable)

**If entity is used in API endpoints**, define the contract:

```json
{
  "id": "api-create-recipe",
  "endpoint": "/api/recipes",
  "method": "POST",
  "requestEntity": "recipe",
  "responseEntity": "recipe",
  "requiredFields": ["title", "user_id"],
  "authentication": "required"
}
```

---

### Step 9: Detect Schema Mismatches

**Compare entities in contracts.json with schema.md** (if schema.md exists):

For each field in each entity:
1. Check if corresponding column exists in schema.md
2. Check if data types are compatible (string -> TEXT/VARCHAR/UUID, number -> INTEGER/BIGINT, etc.)
3. Check nullable alignment

**If mismatch found**: Suggest migration with ALTER TABLE statement.

---

### Step 10: Write contracts.json

**Write the complete contracts.json using Write tool**:

1. If `.shipkit/contracts.json` exists, merge new entities, relationships, validation rules, and API contracts into the existing file
2. If `.shipkit/contracts.json` does not exist, create it with the full schema structure
3. Recalculate the `summary` object:
   - `totalEntities` = count of `entities` array
   - `totalRelationships` = count of `relationships` array
   - `totalValidationRules` = count of `validationRules` array
   - `domains` = unique `domain` values across all entities
   - `lastChange` = description of what was just added/modified
4. Update `lastUpdated` to current ISO 8601 datetime

**Merge rules when updating existing contracts.json**:
- **Entities**: Match by `id`. If entity exists, merge fields (add new, preserve existing). If entity is new, append.
- **Relationships**: Match by `id`. Replace if exists, append if new.
- **Validation rules**: Match by `id`. Replace if exists, append if new.
- **API contracts**: Match by `id`. Replace if exists, append if new.

**Creates if missing**: `.shipkit/contracts.json` (with proper structure and all required top-level fields)

**Never modifies**: schema.md, stack.json, architecture.json (read-only)

---

### Step 11: Suggest Migration (if mismatch detected)

**If database schema mismatch detected**, suggest adding to user tasks with migration SQL.

Suggest: "Run `/shipkit-user-instructions` to track migration task"

---

### Step 12: Suggest Next Step

**Output to user**: Summary of changes to contracts.json, including:
- Entities added/updated (with field counts)
- Relationships defined
- Validation rules added
- API contracts defined
- Schema alignment status
- Dashboard summary (from `summary` object)

---

## Completion Checklist

Copy and track:
- [ ] Identified data contracts to validate
- [ ] Checked alignment across layers
- [ ] Documented any mismatches or fixes
- [ ] contracts.json written with valid schema
- [ ] Summary counts are accurate

---

## What Makes This "Lite"

**Included**:
- Entity definitions with typed fields (contracts.json `entities`)
- Relationship graph for ER diagram rendering (contracts.json `relationships`)
- Validation rules with error messages (contracts.json `validationRules`)
- API contract definitions (contracts.json `apiContracts`)
- Schema mismatch detection (compare field names)
- Migration suggestions
- Dashboard summary with counts and domains

**Not included** (vs full data-consistency):
- Complex type inference from existing code
- Automatic type generation from database schema
- Breaking change detection across types
- Cross-service type sharing

**Philosophy**: Maintain canonical entity-relationship data and catch obvious schema mismatches. The JSON output is graph-ready for ER diagram visualization and dashboard cards.

---

## Integration with Other Skills

**Before shipkit-data-contracts**:
- `/shipkit-project-context` - Generates schema.md for alignment checking
- `/shipkit-spec` - Defines data requirements
- `/shipkit-plan` - Identifies needed types

**After shipkit-data-contracts**:
- `implement (no skill needed)` - Use defined entities/types in components/actions
- `/shipkit-user-instructions` - Track migration tasks (if schema mismatch)
- `/shipkit-plan` - Create plan using defined entities
- `/shipkit-mission-control` - Reads `summary` from contracts.json for dashboard cards

---

## Context Files This Skill Reads

**Primary**:
- `.shipkit/schema.md` - Database schema (from shipkit-project-context)
- `.shipkit/contracts.json` - Existing entity-relationship contracts (from previous runs)

---

## Context Files This Skill Writes

**Writes to**:
- `.shipkit/contracts.json` - Entity definitions, relationships, validation rules, and API contracts

**Creates if missing**: `.shipkit/contracts.json` (with full Shipkit JSON Artifact Convention structure)

**Never modifies**: schema.md, stack.json, architecture.json (read-only)

---

## Lazy Loading Behavior

**This skill loads context ON DEMAND**:

1. User invokes `/shipkit-data-contracts`
2. Claude reads this SKILL.md
3. Claude reads `.shipkit/schema.md` (if exists) - ~500-1000 tokens
4. Claude reads `.shipkit/contracts.json` (if exists) - ~500-2000 tokens
5. Claude asks clarifying questions
6. Claude generates entities, relationships, and validation rules
7. Claude writes updated contracts.json
8. Total context: ~1500-3000 tokens (focused)

---

<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Has important context been saved to `.shipkit/contracts.json`?
2. **Prerequisites** - Does the next action need a spec or plan first?
3. **Session length** - Long session? Consider `/shipkit-work-memory` for continuity.

**Natural capabilities** (no skill needed): Implementation, debugging, testing, refactoring, code documentation.

**Suggest skill when:** User needs to make decisions, create persistence, or check project status.
<!-- /SECTION:after-completion -->

<!-- SECTION:success-criteria -->
## Success Criteria

Contracts are defined when:
- [ ] Entity added to contracts.json `entities` array with all fields
- [ ] Relationships added to contracts.json `relationships` array (if applicable)
- [ ] Validation rules added to contracts.json `validationRules` array (if applicable)
- [ ] API contracts added to contracts.json `apiContracts` array (if applicable)
- [ ] Schema alignment checked (if schema.md exists)
- [ ] Migration suggested (if mismatch detected)
- [ ] `summary` object recalculated with accurate counts
- [ ] `lastUpdated` timestamp set to current time
- [ ] `$schema`, `type`, `version`, and `source` fields present
- [ ] User informed of next steps
<!-- /SECTION:success-criteria -->
---

**Remember**: This is a lightweight entity-relationship manager for POC/MVP work. Maintain canonical entities, relationships, and validation rules in a single JSON file. The output is graph-ready for ER diagram visualization and dashboard integration. For comprehensive type systems, upgrade to full `/data-consistency`.
