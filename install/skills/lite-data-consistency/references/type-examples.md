# Type Definition Examples

Complete examples for type definitions, component contracts, and schema management.

## Example 1: Simple Entity Type

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

## Example 2: Type with Schema Mismatch

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

## Example 3: Component Contract

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

## Example 4: Nested Type with JOIN Result

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

## Schema Mismatch Detection Logic

How to detect and handle schema mismatches between types and database.

### Field Existence Check

```
For each field in TypeScript type:
  1. Check if field exists in schema.md table definition
  2. If missing → Flag as mismatch
  3. Note: Only flag if field is NOT nullable (nullable OK to add later)
```

### Data Type Compatibility

```
Database Type → TypeScript Type mapping:

UUID, TEXT         → string
INTEGER, BIGINT    → number
BOOLEAN            → boolean
TIMESTAMPTZ, DATE  → string (ISO 8601)
JSONB              → unknown or specific type
TEXT[]             → string[]
```

### Nullable Alignment

```
Database column nullable? TypeScript field should match:

Column: NOT NULL   → Type: string
Column: NULL       → Type: string | null

Mismatch examples:
✗ DB: NOT NULL, Type: string | null  (too permissive)
✗ DB: NULL, Type: string              (too restrictive)
✓ DB: NOT NULL, Type: string          (aligned)
✓ DB: NULL, Type: string | null       (aligned)
```

### Simple Detection Only

**Lite version** detects:
- Field existence (field in type but not in DB)
- Basic type mismatches (string vs number)
- Nullable mismatches (obvious cases)

**Does NOT detect**:
- Complex constraint violations (length, pattern)
- Index requirements
- Foreign key integrity
- Performance implications

**For comprehensive detection**: Upgrade to full `/data-consistency`
