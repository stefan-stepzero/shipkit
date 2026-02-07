# Detection Patterns for Project Context

What can be automatically detected vs what requires human input.

---

## Detectable vs Human Input

| Aspect | Auto-Detectable? | Detection Method | If Not Detectable |
|--------|------------------|------------------|-------------------|
| Framework | Yes | `package.json` deps | Mark TBD |
| Database | Yes | deps + migration files | Mark TBD |
| Styling | Yes | tailwind.config, deps | Mark TBD |
| Provider nesting order | Yes | Scan layout.tsx | Mark TBD |
| API route patterns | Yes | Glob + sample read | Describe "varies" |
| Component conventions | Partial | Directory structure | Note patterns found |
| Import aliases | Yes | tsconfig.json paths | Skip section |
| **Why this exists** | No | Needs human | Prompt for `/shipkit-why-project` |
| **Data flow rules** | No | Needs human | Prompt for `/shipkit-architecture-memory` |
| **Cache invalidation** | No | Needs human | Prompt for `/shipkit-architecture-memory` |
| **Business invariants** | No | Needs human | Prompt for `/shipkit-architecture-memory` |

---

## Provider Nesting Detection

**Purpose**: Know the provider wrapping order for correct data access.

**How to detect**:
```
1. Glob: pattern="**/app/layout.tsx" OR "**/src/app/layout.tsx"
2. Read the file
3. Scan for JSX patterns: <*Provider> nesting
4. Extract order from outside-in
```

**Pattern to find**:
```
Grep: pattern="<\\w+Provider"
      path="[layout file]"
      output_mode="content"
```

**Example output for stack.json**:
```markdown
## Provider Hierarchy

1. `QueryClientProvider` (React Query)
2. `AuthProvider` (Supabase auth)
3. `ThemeProvider` (next-themes)
```

**If no providers found**: Note "No context providers detected at app level"

---

## API Route Structure Detection

**Purpose**: Understand how API routes are organized.

**How to detect**:
```
1. Glob: pattern="**/app/api/**/route.{ts,js}"
   OR pattern="**/pages/api/**/*.{ts,js}"
2. Sample 3-5 routes
3. Identify patterns:
   - Folder-based grouping (/api/auth/*, /api/users/*)
   - HTTP methods used
   - Common middleware patterns
```

**Pattern to identify**:
```
# Get route file list
Glob: pattern="**/api/**/route.ts"

# Sample a route for structure
Read: [first route file]

# Check for common patterns
Grep: pattern="export (async function|const) (GET|POST|PUT|DELETE|PATCH)"
      glob="**/api/**/route.ts"
      output_mode="files_with_matches"
```

**Example output for stack.json**:
```markdown
## API Patterns

| Pattern | Location | Example |
|---------|----------|---------|
| Auth routes | `/api/auth/*` | login, logout, session |
| CRUD routes | `/api/[resource]/*` | GET/POST/PUT/DELETE |
| Server Actions | `/app/actions/*` | form mutations |
```

**If structure varies**: Note "API structure varies - check individual routes"

---

## Component Conventions Detection

**Purpose**: Understand component organization patterns.

**How to detect**:
```
1. Glob: pattern="**/components/**/*.{tsx,jsx}"
2. Analyze structure:
   - Flat vs nested folders
   - Index file patterns (barrel exports)
   - Naming conventions (PascalCase, kebab-case)
   - Co-located styles/tests
```

**Patterns to check**:
```
# Check for barrel exports
Glob: pattern="**/components/**/index.{ts,tsx}"

# Check for co-located tests
Glob: pattern="**/components/**/*.test.{ts,tsx}"

# Check for co-located styles
Glob: pattern="**/components/**/*.module.css"
```

**Example output for stack.json**:
```markdown
## Component Conventions

| Convention | Pattern | Example |
|------------|---------|---------|
| Location | `src/components/` | — |
| Structure | Feature folders | `/components/auth/LoginForm.tsx` |
| Naming | PascalCase | `UserProfile.tsx` |
| Exports | Barrel files | `index.ts` re-exports |
| Tests | Co-located | `Component.test.tsx` |
```

---

## Import Pattern Detection

**Purpose**: Know the project's import alias conventions.

**How to detect**:
```
1. Read: tsconfig.json or jsconfig.json
2. Extract paths configuration
3. Verify usage in codebase
```

**Pattern**:
```
Read: file_path="tsconfig.json"

# Look for paths section:
# "paths": {
#   "@/*": ["./src/*"],
#   "@/components/*": ["./src/components/*"]
# }
```

**Verify usage**:
```
Grep: pattern="from ['\"]@/"
      glob="**/*.{ts,tsx}"
      output_mode="count"
```

**Example output for stack.json**:
```markdown
## Import Aliases

| Alias | Maps To |
|-------|---------|
| `@/*` | `./src/*` |
| `@/components/*` | `./src/components/*` |
| `@/lib/*` | `./src/lib/*` |
```

**If no aliases configured**: Skip section

---

## Quick Detection Sequence

For full Working Patterns detection, run in this order:

```
1. tsconfig.json → Import aliases
2. app/layout.tsx → Provider hierarchy
3. app/api/**/* → API patterns
4. components/**/* → Component conventions
5. lib/**/* OR utils/**/* → Utility organization
```

**Time budget**: ~30 seconds for all patterns
**Token budget**: ~400 tokens for detection, ~200 for output

---

## Handling Detection Failures

| Scenario | Action |
|----------|--------|
| File doesn't exist | Skip that pattern, note "Not detected" |
| Multiple conventions | List all found, note "varies" |
| Empty results | Mark TBD, suggest manual input |
| Unusual structure | Describe what was found, don't assume |

**Key principle**: Report what you find, don't invent patterns.
