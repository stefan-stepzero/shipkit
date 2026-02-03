---
name: shipkit-data-contracts
description: "Use when validating data shapes across layers or checking type alignment. Triggers: 'validate contracts', 'check types', 'data shape mismatch'."
---

# shipkit-data-contracts - Type Definitions & Validation Schema Manager

**Purpose**: Maintain canonical TypeScript types and Zod validation schemas across the codebase, ensuring alignment with database schema and preventing type mismatches.

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
- Existing types: `.shipkit/types.md`
- Component contracts: `.shipkit/component-contracts.md`

**Can run standalone**: Yes - creates files if they don't exist

---

## Process

### Step 0: Check for Queue (Auto-Detect Mode)

**First, check if running in queue-driven mode**:

Read file (if exists): `.shipkit/.queues/define-data-contracts.md`

**If queue file exists and has pending items**:
1. Parse the `## Pending` section for data types needing validation
2. For each pending type: Check database alignment, generate TypeScript types, create Zod schemas
3. Save to `.shipkit/types.md` and `.shipkit/validation-schemas.md`
4. Move item from Pending to Completed in queue
5. Skip Step 2 questions (types already identified)

**If queue file doesn't exist or is empty**: Continue to Step 1 (manual mode)

---

### Step 1: (Manual Mode) Read Existing Context

**Read existing type definitions before asking questions**:
- `.shipkit/schema.md` - Database schema (if exists)
- `.shipkit/types.md` - Existing types (if exists)
- `.shipkit/component-contracts.md` - Component contracts (if exists)
- `.shipkit/validation-schemas.md` - Existing Zod schemas (if exists)

**If files don't exist**: Continue to questions (will create them)

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
2. Compare requested type fields with database columns
3. Detect mismatches: Fields in type but not in database, different data types, missing nullable annotations

**IF mismatch detected**:
- Ask: "Should this align with the database schema?"
- Option A: "Adjust type to match database?"
- Option B: "Database needs migration - add fields?"

---

### Step 4: Ask Type Definition Questions

**Only ask what isn't clear from context**:
- **Data shape** (if not obvious): "What fields does this type need?"
- **Validation requirements** (if applicable): "Generate Zod validation schema?" (default: yes)
- **Alignment confirmation** (if mismatch found): "This doesn't match database schema. Should I suggest migration?"

---

### Step 5: Define TypeScript Type

**Type definition pattern**:

```typescript
export type [EntityName] = {
  id: string                    // Primary key (UUID)
  user_id: string              // Foreign key (UUID)
  [field_name]: [type]         // Field description
  created_at: string           // ISO 8601 datetime
  updated_at: string           // ISO 8601 datetime
}
```

**Type naming conventions**: PascalCase for type names, snake_case for field names (matches database columns).

---

### Step 6: Generate Zod Validation Schema

**Generate Zod schema for runtime validation** (default: yes unless user says no):

```typescript
import { z } from 'zod'

export const [EntityName]Schema = z.object({
  id: z.string().uuid(),
  user_id: z.string().uuid(),
  [field_name]: z.[validator](),
  created_at: z.string().datetime(),
  updated_at: z.string().datetime()
})

export type [EntityName] = z.infer<typeof [EntityName]Schema>
```

**Form input schemas** (subset of full schema):

```typescript
export const CreateRecipeSchema = RecipeSchema.omit({
  id: true, created_at: true, updated_at: true
})
export const UpdateRecipeSchema = RecipeSchema.partial().required({ id: true })
```

---

### Step 7: Define Component Contracts (if applicable)

**If type is for a component**, define prop interface:

```typescript
interface [ComponentName]Props {
  [entity]: [EntityType]           // Main data prop
  [handler]?: ([param]: [type]) => void  // Optional event handlers
  className?: string               // Optional styling
}
```

---

### Step 8: Detect Schema Mismatches

**Compare types.md with schema.md** (if schema.md exists):

For each field in type definition:
1. Check if corresponding column exists in schema.md
2. Check if data types are compatible (string → TEXT/VARCHAR/UUID, number → INTEGER/BIGINT, etc.)
3. Check nullable alignment

**If mismatch found**: Suggest migration with ALTER TABLE statement.

---

### Step 9: Write Type Definitions

**Append to appropriate files using Write tool**:

- `.shipkit/types.md` - TypeScript type definitions (canonical types)
- `.shipkit/validation-schemas.md` - Zod validation schemas
- `.shipkit/component-contracts.md` - Component prop interfaces

**Creates if missing**: All three files above (with proper structure)

**Never modifies**: schema.md, stack.md, architecture.md (read-only)

---

### Step 10: Update Existing Types (if needed)

When updating existing types:
1. Read existing type definition from types.md
2. Add new fields with comments marking them as new (e.g., `// NEW: Added 2025-01-15`)
3. Preserve existing fields
4. Update "Last Updated" timestamp

---

### Step 11: Suggest Migration (if mismatch detected)

**If database schema mismatch detected**, suggest adding to user tasks with migration SQL.

Suggest: "Run `/shipkit-user-instructions` to track migration task"

---

### Step 12: Suggest Next Step

**Output to user**: Summary of updated files, fields, schema alignment status.

---

## Completion Checklist

Copy and track:
- [ ] Identified data contracts to validate
- [ ] Checked alignment across layers
- [ ] Documented any mismatches or fixes

---

## What Makes This "Lite"

**Included**:
- TypeScript type definitions (canonical types.md)
- Zod validation schema generation
- Component prop interfaces
- Schema mismatch detection (compare field names)
- Migration suggestions
- Form input schema variants (Create/Update)

**Not included** (vs full data-consistency):
- Complex type inference from existing code
- Automatic type generation from database schema
- Type dependency graph visualization
- Breaking change detection across types
- Cross-service type sharing

**Philosophy**: Maintain canonical types and catch obvious schema mismatches. Not a comprehensive type system manager.

---

## Integration with Other Skills

**Before shipkit-data-contracts**:
- `/shipkit-project-context` - Generates schema.md for alignment checking
- `/shipkit-spec` - Defines data requirements
- `/shipkit-plan` - Identifies needed types

**After shipkit-data-contracts**:
- `implement (no skill needed)` - Use defined types in components/actions
- `/shipkit-user-instructions` - Track migration tasks (if schema mismatch)
- `/shipkit-plan` - Create plan using defined types

---

## Context Files This Skill Reads

**Primary**:
- `.shipkit/schema.md` - Database schema (from shipkit-project-context)
- `.shipkit/types.md` - Existing type definitions

**Secondary**:
- `.shipkit/component-contracts.md` - Existing component contracts
- `.shipkit/validation-schemas.md` - Existing Zod schemas

---

## Context Files This Skill Writes

**Appends to**:
- `.shipkit/types.md` - TypeScript type definitions
- `.shipkit/validation-schemas.md` - Zod validation schemas
- `.shipkit/component-contracts.md` - Component prop interfaces

**Creates if missing**: All three files above (with proper structure)

**Never modifies**: schema.md, stack.md, architecture.md (read-only)

---

## Lazy Loading Behavior

**This skill loads context ON DEMAND**:

1. User invokes `/shipkit-data-contracts`
2. Claude reads this SKILL.md
3. Claude reads `.shipkit/schema.md` (if exists) - ~500-1000 tokens
4. Claude reads `.shipkit/types.md` (if exists) - ~500-1500 tokens
5. Claude asks clarifying questions
6. Claude generates types and validation
7. Total context: ~1500-3000 tokens (focused)

---

## Type Definition Examples

**Complete examples with schema detection**: See `references/type-examples.md`

---

## Zod Schema Patterns Reference

**Complete Zod patterns**: See `references/zod-patterns.md`

---

<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Has important context been saved to `.shipkit/`?
2. **Prerequisites** - Does the next action need a spec or plan first?
3. **Session length** - Long session? Consider `/shipkit-work-memory` for continuity.

**Natural capabilities** (no skill needed): Implementation, debugging, testing, refactoring, code documentation.

**Suggest skill when:** User needs to make decisions, create persistence, or check project status.
<!-- /SECTION:after-completion -->

<!-- SECTION:success-criteria -->
## Success Criteria

Types are defined when:
- [ ] TypeScript type added to types.md
- [ ] Zod schema added to validation-schemas.md (if requested)
- [ ] Component contract added to component-contracts.md (if applicable)
- [ ] Schema alignment checked (if schema.md exists)
- [ ] Migration suggested (if mismatch detected)
- [ ] Files have proper timestamps and notes
- [ ] User informed of next steps
<!-- /SECTION:success-criteria -->
---

**Remember**: This is a lightweight type manager for POC/MVP work. Maintain canonical types, catch obvious mismatches, generate validation. For comprehensive type systems, upgrade to full `/data-consistency`.

<!-- Shipkit v1.2.0 -->
