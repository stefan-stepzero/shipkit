---
name: lite-data-consistency
description: Maintains canonical TypeScript types and validation schemas across codebase. Reads existing types, component contracts, and database schema. Defines or updates types when user creates components or Server Actions. Generates Zod validation. Detects schema mismatches and suggests migrations.
---

# data-consistency-lite - Type Definitions & Validation Schema Manager

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
- After `/lite-project-context` generates schema.md (suggest: "Define types?")
- During `/lite-implement` when user creates components with data props
- During `/lite-implement` when user creates Server Actions with parameters
- When type errors occur during implementation
- After database migrations (check alignment)

---

## Prerequisites

**Optional but helpful**:
- Database schema: `.shipkit-lite/schema.md` (from project-context-lite)
- Existing types: `.shipkit-lite/types.md`
- Component contracts: `.shipkit-lite/component-contracts.md`

**Can run standalone**: Yes - creates files if they don't exist

---

## Process

### Step 1: Read Existing Context

**Before asking questions, read existing type definitions**:

```bash
# Database schema (if exists)
.shipkit-lite/schema.md

# Existing types (if exists)
.shipkit-lite/types.md

# Component contracts (if exists)
.shipkit-lite/component-contracts.md

# Validation schemas (if exists)
.shipkit-lite/validation-schemas.md
```

**Why read first**:
- Understand existing data shapes
- Check for schema alignment
- Avoid redefining existing types
- Maintain consistency with database

**If files don't exist**: Continue to questions (will create them)

---

### Step 2: Determine What Needs Typing

**Auto-detect from context when possible**:

```
IF user just created a component:
  → Check component code for props interface
  → Identify data shapes from props

IF user just created Server Action:
  → Check function parameters
  → Identify input/output types

IF user explicitly asks "define types for X":
  → Use X as the subject
```

**Ask clarifying question if unclear**:
- "What data shape does this component/action need?"
- "Is this for a component, Server Action, or both?"

---

### Step 3: Check Database Alignment

**If schema.md exists, check for alignment**:

```
1. Read schema.md to see database table structures
2. Compare requested type fields with database columns
3. Detect mismatches:
   - Fields in type but not in database
   - Different data types (string vs number, etc.)
   - Missing nullable annotations

IF mismatch detected:
  → Ask: "Should this align with the database schema?"
  → If YES:
    - Option A: "Adjust type to match database?"
    - Option B: "Database needs migration - add fields?"
  → If NO:
    - Proceed with type as-is (client-only type)
```

**Example mismatch detection**:
```
Type requested: Recipe with is_shared (boolean)
Schema.md shows: recipes table has no is_shared column
→ Mismatch detected
→ Ask: "Database needs migration to add is_shared column?"
```

---

### Step 4: Ask Type Definition Questions

**Only ask what isn't clear from context**:

**Question 1: Data shape** (if not obvious)
- "What fields does this type need?"
- "What's the structure of this data?"

**Question 2: Validation requirements** (if applicable)
- "Generate Zod validation schema?" (default: yes)
- "Any validation rules? (min/max length, regex, etc.)"

**Question 3: Alignment confirmation** (if mismatch found)
- "This doesn't match database schema. Should I suggest migration?"

**Keep questions minimal** - infer as much as possible from code context.

---

### Step 5: Define TypeScript Type

**Type definition pattern**:

```typescript
// [Entity Name] - [Brief description]
export type [EntityName] = {
  id: string                    // Primary key (UUID)
  user_id: string              // Foreign key (UUID)
  [field_name]: [type]         // Field description
  created_at: string           // ISO 8601 datetime
  updated_at: string           // ISO 8601 datetime
}
```

**Type naming conventions**:
- PascalCase for type names (Recipe, User, RecipeShare)
- snake_case for field names (matches database columns)
- Use descriptive names (RecipeWithAuthor, not RecipeWithUser)

**Common TypeScript type patterns**:

```typescript
// UUID fields
id: string
user_id: string

// Nullable fields
share_token: string | null

// Arrays
ingredients: string[]
tags: Tag[]

// Enums
status: 'draft' | 'published' | 'archived'

// Optional fields (not in database, client-only)
isSelected?: boolean

// Dates (stored as ISO 8601 strings)
created_at: string
updated_at: string

// JSON columns
metadata: Record<string, unknown>
settings: { theme: string; notifications: boolean }

// Nested objects (JOIN results)
author: {
  id: string
  name: string
  avatar_url: string | null
}
```

---

### Step 6: Generate Zod Validation Schema

**Generate Zod schema for runtime validation** (default: yes unless user says no):

**Zod schema pattern**:

```typescript
import { z } from 'zod'

// [Entity Name] validation schema
export const [EntityName]Schema = z.object({
  id: z.string().uuid(),
  user_id: z.string().uuid(),
  [field_name]: z.[validator](),
  created_at: z.string().datetime(),
  updated_at: z.string().datetime()
})

// Infer type from schema (alternative to manual type)
export type [EntityName] = z.infer<typeof [EntityName]Schema>
```

**Common Zod validation patterns**:

```typescript
// UUID
z.string().uuid()

// Required string with constraints
z.string().min(1).max(200)
z.string().email()
z.string().url()
z.string().regex(/^[a-z0-9-]+$/)

// Nullable
z.string().nullable()
z.string().optional()

// Numbers
z.number().int().positive()
z.number().min(0).max(100)

// Booleans
z.boolean()

// Arrays
z.array(z.string())
z.array(RecipeSchema)

// Enums
z.enum(['draft', 'published', 'archived'])

// Dates (ISO 8601 strings)
z.string().datetime()

// JSON
z.record(z.unknown())
z.object({ theme: z.string(), notifications: z.boolean() })

// Nested objects
z.object({
  id: z.string().uuid(),
  name: z.string(),
  avatar_url: z.string().url().nullable()
})

// Partial types (for updates)
z.object({...}).partial()

// Pick/Omit (for forms)
RecipeSchema.omit({ id: true, created_at: true })
```

**Form input schemas** (subset of full schema):

```typescript
// For creating new records (no id, timestamps)
export const CreateRecipeSchema = RecipeSchema.omit({
  id: true,
  created_at: true,
  updated_at: true
})

// For updating records (all fields optional except id)
export const UpdateRecipeSchema = RecipeSchema.partial().required({ id: true })
```

---

### Step 7: Define Component Contracts (if applicable)

**If type is for a component**, define prop interface:

```typescript
// [ComponentName] component props
interface [ComponentName]Props {
  [entity]: [EntityType]           // Main data prop
  [handler]?: ([param]: [type]) => void  // Optional event handlers
  [flag]?: boolean                 // Optional flags
  className?: string               // Optional styling
}

// Example:
interface RecipeCardProps {
  recipe: Recipe
  onShare?: (recipeId: string) => void
  onDelete?: (recipeId: string) => void
  showActions?: boolean
  className?: string
}
```

**Component prop patterns**:

```typescript
// Data props (required)
user: User
recipes: Recipe[]

// Event handlers (optional)
onClick?: () => void
onChange?: (value: string) => void
onSubmit?: (data: FormData) => void

// Render props (optional)
renderHeader?: () => React.ReactNode
children?: React.ReactNode

// Flags (optional)
isLoading?: boolean
isDisabled?: boolean
showActions?: boolean

// Styling (optional)
className?: string
style?: React.CSSProperties
```

---

### Step 8: Detect Schema Mismatches

**Compare types.md with schema.md** (if schema.md exists):

**Mismatch detection logic**:

```
FOR each field in type definition:
  1. Check if corresponding column exists in schema.md
  2. Check if data types are compatible:
     - string → TEXT, VARCHAR, UUID
     - number → INTEGER, BIGINT, DECIMAL
     - boolean → BOOLEAN
     - string[] → TEXT[] or JSON
  3. Check nullable alignment:
     - type: string | null → schema: column_name TEXT NULL
     - type: string → schema: column_name TEXT NOT NULL

IF mismatch found:
  → Record mismatch details
  → Suggest migration

IF no mismatch:
  → Types aligned with schema ✓
```

**Migration suggestion format**:

```markdown
⚠️ Schema Mismatch Detected

**Type field**: is_shared (boolean)
**Database**: Column does not exist in recipes table

**Suggested migration**:
ALTER TABLE recipes ADD COLUMN is_shared BOOLEAN DEFAULT FALSE;
ALTER TABLE recipes ADD COLUMN share_token TEXT;

Run `/lite-user-instructions` to track this migration task.
```

---

### Step 9: Write Type Definitions

**Append to appropriate files using Write tool**:

**File 1: `.shipkit-lite/types.md`** (canonical types)

```markdown
# TypeScript Type Definitions

Canonical type definitions for the project. These types represent the shape of data throughout the application.

**Last Updated**: [timestamp]

---

## [Entity Name]

**Added**: [YYYY-MM-DD]
**Source**: [Database table name] OR [Client-only]

```typescript
export type [EntityName] = {
  id: string
  // ... fields
}
```

**Notes**:
- [Any important context about this type]
- [Schema alignment status]

---

[Append new types here]
```

**File 2: `.shipkit-lite/validation-schemas.md`** (Zod schemas)

```markdown
# Validation Schemas (Zod)

Runtime validation schemas for data validation in forms, Server Actions, and API endpoints.

**Last Updated**: [timestamp]

---

## [Entity Name] Schema

**Added**: [YYYY-MM-DD]

```typescript
import { z } from 'zod'

export const [EntityName]Schema = z.object({
  // ... validators
})

// Form input schemas
export const Create[EntityName]Schema = [EntityName]Schema.omit({
  id: true,
  created_at: true,
  updated_at: true
})
```

**Usage**:
```typescript
// In Server Action
const validatedData = CreateRecipeSchema.parse(formData)

// In component
const { data, errors } = useFormState(createRecipeAction, initialState)
```

---

[Append new schemas here]
```

**File 3: `.shipkit-lite/component-contracts.md`** (component props)

```markdown
# Component Contracts

TypeScript interfaces for component props. These define the contracts between components and their consumers.

**Last Updated**: [timestamp]

---

## [ComponentName]

**Added**: [YYYY-MM-DD]
**Location**: [File path]

```typescript
interface [ComponentName]Props {
  // ... props
}
```

**Usage**:
```tsx
import { Recipe } from '@/types'

export function RecipeCard({ recipe, onShare }: RecipeCardProps) {
  // ...
}
```

---

[Append new contracts here]
```

---

### Step 10: Update Existing Types (if needed)

**When updating existing types** (not just appending):

1. Read existing type definition from types.md
2. Add new fields with comments marking them as new
3. Preserve existing fields
4. Update "Last Updated" timestamp
5. Add note about what changed

**Update format**:

```typescript
export type Recipe = {
  id: string
  user_id: string
  title: string
  ingredients: string[]
  instructions: string
  is_shared: boolean        // NEW: Added 2025-01-15 for sharing feature
  share_token: string | null // NEW: Added 2025-01-15 for public sharing
  created_at: string
  updated_at: string
}
```

**Change note**:
```markdown
**Changes**:
- 2025-01-15: Added is_shared and share_token fields for sharing feature
```

---

### Step 11: Suggest Migration (if mismatch detected)

**If database schema mismatch detected**, suggest adding to user tasks:

```
⚠️ Database migration needed

**Type changes require schema updates**:
- Add is_shared column (BOOLEAN)
- Add share_token column (TEXT, nullable)

**Suggested migration**:
```sql
ALTER TABLE recipes ADD COLUMN is_shared BOOLEAN DEFAULT FALSE;
ALTER TABLE recipes ADD COLUMN share_token TEXT;
CREATE INDEX idx_recipes_share_token ON recipes(share_token) WHERE share_token IS NOT NULL;
```

👉 Run `/lite-user-instructions` to track migration task
```

---

### Step 12: Suggest Next Step

**Output to user**:

```
✅ Types defined

📁 Updated files:
  • .shipkit-lite/types.md
  • .shipkit-lite/validation-schemas.md
  • .shipkit-lite/component-contracts.md (if component)

📋 Summary:
  • Type: [EntityName]
  • Fields: [X] fields
  • Zod schema: ✓ Generated
  • Schema alignment: [✓ Aligned | ⚠️ Migration needed]

**Next steps**:
[Context-specific suggestion]
```

**Context-specific suggestions**:

```
IF schema mismatch detected:
  → "Run `/lite-user-instructions` to track migration task"

IF types defined during implementation:
  → "Continue with `/lite-implement` to use these types"

IF types defined during planning:
  → "Run `/lite-plan` to create implementation plan"

IF standalone type definition:
  → "Types ready. Use in components or Server Actions."
```

---

## What Makes This "Lite"

**Included**:
- ✅ TypeScript type definitions (canonical types.md)
- ✅ Zod validation schema generation
- ✅ Component prop interfaces
- ✅ Schema mismatch detection (compare field names)
- ✅ Migration suggestions
- ✅ Form input schema variants (Create/Update)

**Not included** (vs full data-consistency):
- ❌ Complex type inference from existing code
- ❌ Automatic type generation from database schema
- ❌ Type dependency graph visualization
- ❌ Breaking change detection across types
- ❌ Type versioning and migration tracking
- ❌ OpenAPI/GraphQL schema generation
- ❌ Cross-service type sharing
- ❌ Type coverage analysis
- ❌ Advanced Zod patterns (transforms, refinements, custom validators)

**Philosophy**: Maintain canonical types and catch obvious schema mismatches. Not a comprehensive type system manager.

---

## Integration with Other Skills

**Before data-consistency-lite**:
- `/lite-project-context` - Generates schema.md for alignment checking
- `/lite-spec` - Defines data requirements
- `/lite-plan` - Identifies needed types

**After data-consistency-lite**:
- `/lite-implement` - Use defined types in components/actions
- `/lite-user-instructions` - Track migration tasks (if schema mismatch)
- `/lite-plan` - Create plan using defined types

**During implementation**:
- `/lite-implement` can invoke `/lite-data-consistency` when creating components with data

---

## Context Files This Skill Reads

**Primary**:
- `.shipkit-lite/schema.md` - Database schema (from project-context-lite)
- `.shipkit-lite/types.md` - Existing type definitions

**Secondary**:
- `.shipkit-lite/component-contracts.md` - Existing component contracts
- `.shipkit-lite/validation-schemas.md` - Existing Zod schemas

---

## Context Files This Skill Writes

**Appends to**:
- `.shipkit-lite/types.md` - TypeScript type definitions
- `.shipkit-lite/validation-schemas.md` - Zod validation schemas
- `.shipkit-lite/component-contracts.md` - Component prop interfaces

**Creates if missing**:
- All three files above (with proper structure)

**Never modifies**:
- schema.md, stack.md, architecture.md (read-only)

---

## Lazy Loading Behavior

**This skill loads context ON DEMAND**:

1. User invokes `/lite-data-consistency`
2. Claude reads this SKILL.md
3. Claude reads `.shipkit-lite/schema.md` (if exists) - ~500-1000 tokens
4. Claude reads `.shipkit-lite/types.md` (if exists) - ~500-1500 tokens
5. Claude asks clarifying questions
6. Claude generates types and validation
7. Claude appends to type files
8. Total context: ~1500-3000 tokens (focused)

**Not loaded unless needed**:
- Specs, plans, implementations
- User tasks, progress logs
- Other context files

---

## Type Definition Examples

### Example 1: Simple Entity Type

**User**: "Define types for Recipe"

**Context**: schema.md shows recipes table with id, user_id, title, ingredients (TEXT[]), instructions, created_at

**Output** (appended to types.md):

```markdown
## Recipe

**Added**: 2025-01-15
**Source**: recipes table

```typescript
export type Recipe = {
  id: string                // UUID primary key
  user_id: string          // UUID foreign key to users
  title: string            // Recipe title
  ingredients: string[]    // List of ingredients
  instructions: string     // Cooking instructions
  created_at: string       // ISO 8601 timestamp
  updated_at: string       // ISO 8601 timestamp
}
```

**Schema alignment**: ✓ Aligned with database

---
```

**Output** (appended to validation-schemas.md):

```markdown
## Recipe Schema

**Added**: 2025-01-15

```typescript
import { z } from 'zod'

export const RecipeSchema = z.object({
  id: z.string().uuid(),
  user_id: z.string().uuid(),
  title: z.string().min(1).max(200),
  ingredients: z.array(z.string()),
  instructions: z.string().min(1),
  created_at: z.string().datetime(),
  updated_at: z.string().datetime()
})

// Form input schema (for creating recipes)
export const CreateRecipeSchema = RecipeSchema.omit({
  id: true,
  created_at: true,
  updated_at: true
})

// Update schema (all fields optional except id)
export const UpdateRecipeSchema = RecipeSchema.partial().required({ id: true })
```

**Usage**:
```typescript
// In Server Action
const validatedData = CreateRecipeSchema.parse(formData)
```

---
```

### Example 2: Type with Schema Mismatch

**User**: "Add sharing fields to Recipe type"

**Context**: schema.md shows recipes table does NOT have is_shared or share_token columns

**Process**:
1. Read schema.md → No is_shared/share_token columns
2. Read types.md → Current Recipe type
3. Ask: "Should I add database columns too?"
4. User: "Yes"
5. Update types.md with new fields
6. Generate updated Zod schema
7. Detect mismatch
8. Suggest migration

**Output** (updated in types.md):

```markdown
## Recipe

**Added**: 2025-01-15
**Last Updated**: 2025-01-16
**Source**: recipes table

```typescript
export type Recipe = {
  id: string
  user_id: string
  title: string
  ingredients: string[]
  instructions: string
  is_shared: boolean        // NEW: Added 2025-01-16 for sharing feature
  share_token: string | null // NEW: Added 2025-01-16 for public sharing
  created_at: string
  updated_at: string
}
```

**Schema alignment**: ⚠️ Migration needed

**Changes**:
- 2025-01-16: Added is_shared and share_token fields for sharing feature

---
```

**Migration suggestion**:

```
⚠️ Database migration needed

**Suggested migration**:
```sql
ALTER TABLE recipes ADD COLUMN is_shared BOOLEAN DEFAULT FALSE;
ALTER TABLE recipes ADD COLUMN share_token TEXT;
CREATE INDEX idx_recipes_share_token ON recipes(share_token) WHERE share_token IS NOT NULL;
```

👉 Run `/lite-user-instructions` to track migration task
```

### Example 3: Component Contract

**User**: "Define props for RecipeCard component"

**Context**: Recipe type already exists in types.md

**Output** (appended to component-contracts.md):

```markdown
## RecipeCard

**Added**: 2025-01-16
**Location**: components/RecipeCard.tsx

```typescript
import { Recipe } from '@/types'

interface RecipeCardProps {
  recipe: Recipe                           // Recipe data
  onShare?: (recipeId: string) => void    // Share button handler
  onDelete?: (recipeId: string) => void   // Delete button handler
  showActions?: boolean                   // Show action buttons
  className?: string                      // Optional styling
}
```

**Usage**:
```tsx
export function RecipeCard({
  recipe,
  onShare,
  onDelete,
  showActions = true,
  className
}: RecipeCardProps) {
  return (
    <div className={className}>
      <h3>{recipe.title}</h3>
      {/* ... */}
    </div>
  )
}
```

---
```

### Example 4: Nested Type with JOIN Result

**User**: "Define type for Recipe with author info"

**Output** (appended to types.md):

```markdown
## RecipeWithAuthor

**Added**: 2025-01-16
**Source**: recipes JOIN users

```typescript
import { Recipe } from './Recipe'

export type RecipeWithAuthor = Recipe & {
  author: {
    id: string
    name: string
    avatar_url: string | null
  }
}
```

**Notes**:
- Extends Recipe type with author info from JOIN
- Used in recipe detail views
- Not a database table (query result type)

---
```

---

## Schema Mismatch Detection Logic

**Inline guidance for detecting mismatches** (no references/ folder):

### Field Existence Check

```
FOR each field in type definition:
  IF field NOT in schema.md table:
    → Mismatch: Field missing from database
    → Suggest: ALTER TABLE [table] ADD COLUMN [field] [type]
```

### Data Type Compatibility

```
TypeScript → PostgreSQL mappings:
- string → TEXT, VARCHAR, UUID
- number → INTEGER, BIGINT, DECIMAL, NUMERIC
- boolean → BOOLEAN
- string[] → TEXT[], JSON
- Date → TIMESTAMP, TIMESTAMPTZ
- Record<string, unknown> → JSON, JSONB

IF types don't match:
  → Warn: "Type mismatch: TypeScript [type] vs Database [type]"
```

### Nullable Alignment

```
IF type: string | null:
  → Database should: column_name TEXT NULL OR DEFAULT NULL

IF type: string (not nullable):
  → Database should: column_name TEXT NOT NULL

IF mismatch:
  → Warn: "Nullable mismatch"
  → Suggest: ALTER TABLE [table] ALTER COLUMN [field] [SET|DROP] NOT NULL
```

### Simple Detection Only

**Lite version limitations**:
- Only checks field names and basic types
- Does NOT validate complex constraints (CHECK, FOREIGN KEY)
- Does NOT validate indexes
- Does NOT validate enum values
- Does NOT check cascading effects

**For comprehensive schema validation, upgrade to full /data-consistency**

---

## Zod Schema Patterns Reference

**Inline Zod patterns** (no references/ folder):

### Basic Types

```typescript
// Strings
z.string()                      // Any string
z.string().min(1)               // Non-empty
z.string().max(200)             // Max length
z.string().email()              // Email validation
z.string().url()                // URL validation
z.string().uuid()               // UUID format
z.string().regex(/^[a-z0-9-]+$/) // Custom pattern

// Numbers
z.number()                      // Any number
z.number().int()                // Integer only
z.number().positive()           // Positive only
z.number().min(0).max(100)      // Range

// Booleans
z.boolean()

// Dates
z.string().datetime()           // ISO 8601 string
z.date()                        // Date object
```

### Nullable & Optional

```typescript
z.string().nullable()           // string | null
z.string().optional()           // string | undefined
z.string().nullish()            // string | null | undefined
z.string().default('default')   // Default value if undefined
```

### Arrays & Objects

```typescript
// Arrays
z.array(z.string())             // string[]
z.array(RecipeSchema)           // Recipe[]
z.array(z.string()).min(1)      // Non-empty array

// Objects
z.object({
  name: z.string(),
  age: z.number()
})

// Nested objects
z.object({
  author: z.object({
    id: z.string().uuid(),
    name: z.string()
  })
})

// Records (dynamic keys)
z.record(z.string())            // Record<string, string>
z.record(z.unknown())           // Record<string, unknown>
```

### Enums & Unions

```typescript
// Enums
z.enum(['draft', 'published', 'archived'])

// Unions
z.union([z.string(), z.number()])
z.string().or(z.number())       // Same as above
```

### Schema Transformations

```typescript
// Partial (all fields optional)
RecipeSchema.partial()

// Pick (subset of fields)
RecipeSchema.pick({ id: true, title: true })

// Omit (exclude fields)
RecipeSchema.omit({ created_at: true, updated_at: true })

// Required (remove optional)
RecipeSchema.required()

// Extend (add fields)
RecipeSchema.extend({
  new_field: z.string()
})

// Merge (combine schemas)
RecipeSchema.merge(TimestampSchema)
```

### Form Input Schemas

```typescript
// Create schema (no id, timestamps)
const CreateRecipeSchema = RecipeSchema.omit({
  id: true,
  created_at: true,
  updated_at: true
})

// Update schema (all optional except id)
const UpdateRecipeSchema = RecipeSchema.partial().required({ id: true })

// Search params schema
const RecipeSearchSchema = z.object({
  query: z.string().optional(),
  page: z.coerce.number().int().positive().default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20)
})
```

---

## Success Criteria

Types are defined when:
- [ ] TypeScript type added to types.md
- [ ] Zod schema added to validation-schemas.md (if requested)
- [ ] Component contract added to component-contracts.md (if applicable)
- [ ] Schema alignment checked (if schema.md exists)
- [ ] Migration suggested (if mismatch detected)
- [ ] Files have proper timestamps and notes
- [ ] User informed of next steps

---

## Common Scenarios

### Scenario 1: Define Type for New Component

```
User: "Define types for RecipeCard component"

Claude (data-consistency-lite):
1. Read .shipkit-lite/schema.md → Find recipes table
2. Read .shipkit-lite/types.md → Check if Recipe type exists
3. Recipe type exists → Reuse it
4. Ask: "What props does RecipeCard need?"
5. User: "Recipe data, share handler, delete handler"
6. Generate component contract
7. Append to component-contracts.md
8. "✓ Component contract defined. Use in RecipeCard.tsx"
```

### Scenario 2: Define Type with Schema Mismatch

```
User: "Add sharing fields to Recipe"

Claude (data-consistency-lite):
1. Read .shipkit-lite/schema.md → recipes table has no is_shared column
2. Read .shipkit-lite/types.md → Current Recipe type
3. Detect mismatch
4. Ask: "Database doesn't have is_shared. Add it?"
5. User: "Yes"
6. Update Recipe type with new fields (marked as NEW)
7. Update RecipeSchema with new validators
8. Suggest migration SQL
9. "⚠️ Migration needed. Run /lite-user-instructions to track"
```

### Scenario 3: Generate Validation for Server Action

```
User: "Create validation for createRecipe Server Action"

Claude (data-consistency-lite):
1. Read .shipkit-lite/types.md → Recipe type exists
2. Read .shipkit-lite/validation-schemas.md → RecipeSchema exists
3. Generate CreateRecipeSchema (omit id, timestamps)
4. Append to validation-schemas.md
5. "✓ Validation schema ready. Use in Server Action:
   const validatedData = CreateRecipeSchema.parse(formData)"
```

### Scenario 4: Type Already Exists

```
User: "Define type for Recipe"

Claude (data-consistency-lite):
1. Read .shipkit-lite/types.md
2. Find existing Recipe type
3. "Recipe type already exists in types.md:
   - Fields: id, user_id, title, ingredients, instructions
   - Zod schema: ✓ Available
   - Schema aligned: ✓

   Need to update it or use as-is?"
```

---

## Tips for Effective Type Management

**Keep types canonical**:
- One source of truth in types.md
- Import from types.md across codebase
- Don't duplicate type definitions

**Use Zod for runtime validation**:
- Generate Zod schemas by default
- Use for form inputs, Server Actions, API endpoints
- Catch type errors at runtime

**Check schema alignment**:
- Always compare with schema.md
- Suggest migrations when mismatched
- Track migrations in user-instructions-lite

**Mark changes clearly**:
- Use // NEW: Added YYYY-MM-DD comments
- Update "Last Updated" timestamps
- Document what changed and why

**Generate form schemas**:
- Create/Update variants for forms
- Omit server-generated fields (id, timestamps)
- Use partial() for update forms

**When to upgrade to full /data-consistency**:
- Complex type inference needed
- Automatic schema generation required
- Breaking change detection across types
- Type versioning and migration tracking
- Cross-service type sharing

---

**Remember**: This is a lightweight type manager for POC/MVP work. Maintain canonical types, catch obvious mismatches, generate validation. For comprehensive type systems, upgrade to full `/data-consistency`.
