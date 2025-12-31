# Zod Schema Patterns Reference

Complete reference for Zod validation patterns used by `/lite-data-contracts`.

## Basic Types

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

## Nullable & Optional

```typescript
z.string().nullable()           // string | null
z.string().optional()           // string | undefined
z.string().nullish()            // string | null | undefined
z.string().default('default')   // Default value if undefined
```

## Arrays & Objects

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

## Enums & Unions

```typescript
// Enums
z.enum(['draft', 'published', 'archived'])

// Unions
z.union([z.string(), z.number()])
z.string().or(z.number())       // Same as above
```

## Schema Transformations

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

## Form Input Schemas

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
