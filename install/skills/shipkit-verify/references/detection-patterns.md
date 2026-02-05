# Detection Patterns for Verification

Ready-to-use Glob and Grep patterns for verifying claims. Each pattern includes the tool call format and interpretation guide.

---

## Structural Integrity Patterns

### Orphan Code Detection

**Find exported symbols:**
```
Grep: pattern="export (const|function|class|type|interface) (\w+)"
      glob="**/*.{ts,tsx}"
      output_mode="content"
```

**Verify each export is used:**
```
Grep: pattern="import.*{.*SYMBOL_NAME.*}"
      glob="**/*.{ts,tsx}"
      output_mode="count"

If count = 0 or 1 (just the definition): CREATED_UNUSED
```

### Missing Wiring Detection

**React components not rendered:**
```
# Step 1: Find component definitions
Glob: pattern="**/components/**/*.tsx"

# Step 2: For each component, check if it's rendered
Grep: pattern="<ComponentName"
      glob="**/*.{tsx,jsx}"
      output_mode="count"

If count = 0: WIRING_MISSING (component exists but never rendered)
```

**Routes not registered:**
```
# Step 1: Find route handler files
Glob: pattern="**/app/**/route.{ts,js}"
      # or for pages router:
Glob: pattern="**/pages/api/**/*.{ts,js}"

# Step 2: Check if route is called anywhere (tests, links, fetches)
Grep: pattern="/api/route-name"
      glob="**/*.{ts,tsx,js,jsx}"
      output_mode="count"

If count = 0 and not a new API: verify if intentionally unused
```

### Broken Import Detection

**Find all imports in changed files:**
```
Grep: pattern="^import .* from ['\"](\\..*)['\"]"
      path="src/changed-file.tsx"
      output_mode="content"
```

**Verify each relative import target exists:**
```
# For import './AuthCard'
Glob: pattern="**/AuthCard.{ts,tsx,js,jsx}"

If Glob returns empty: BROKEN_IMPORT
```

### Circular Dependency Detection

**Check for mutual imports:**
```
# Step 1: Get imports from file A
Grep: pattern="import .* from ['\"].*fileB"
      path="src/fileA.ts"

# Step 2: Get imports from file B
Grep: pattern="import .* from ['\"].*fileA"
      path="src/fileB.ts"

If both return matches: CIRCULAR
```

---

## Error Resilience Patterns

### Unhandled Async Detection

**Find await statements:**
```
Grep: pattern="await "
      glob="**/*.{ts,tsx}"
      output_mode="content"
      -B=3  # Show 3 lines before for context
```

**Check for try/catch wrapper:**
```
# Manual verification of Grep output:
# Look for 'try {' within the preceding 3-10 lines
# If no try block: unhandled async
```

**Find Promise chains without catch:**
```
Grep: pattern="\\.then\\([^)]+\\)(?!\\.catch)"
      glob="**/*.{ts,tsx,js,jsx}"
      output_mode="content"
```

### Missing Error Boundary (React)

**Find route/page components:**
```
Glob: pattern="**/app/**/page.tsx"
      # or
Glob: pattern="**/pages/**/*.tsx"
```

**Check for ErrorBoundary wrapper:**
```
Grep: pattern="ErrorBoundary|error\\.tsx"
      path="src/app/layout.tsx"
      output_mode="count"

If count = 0: no error boundary at root level
```

---

## Security Patterns

### Hardcoded Secrets

**Find potential hardcoded credentials:**
```
Grep: pattern="(password|secret|api_?key|token|credential)\\s*[:=]\\s*['\"][^'\"]+['\"]"
      glob="**/*.{ts,tsx,js,jsx,json}"
      -i  # Case insensitive
      output_mode="content"
```

**Exclude false positives:**
- `.env*` files (expected location for secrets)
- `*.test.*` files (test fixtures)
- `*.example*` files (documentation)
- Type definitions (just defining shape)

### Missing Auth Check

**Find API routes:**
```
Glob: pattern="**/api/**/*.{ts,js}"
```

**Check each route for auth verification:**
```
Grep: pattern="(getSession|getServerSession|auth\\(|requireAuth|isAuthenticated)"
      path="src/app/api/protected-route/route.ts"
      output_mode="count"

If count = 0 on route that should be protected: missing auth
```

### Input Validation Missing

**Find form handlers:**
```
Grep: pattern="(handleSubmit|onSubmit|FormData)"
      glob="**/*.{ts,tsx}"
      output_mode="files_with_matches"
```

**Check for validation:**
```
Grep: pattern="(zod|yup|joi|validate|schema\\.parse)"
      path="src/components/ContactForm.tsx"
      output_mode="count"

If count = 0: consider adding input validation
```

---

## Spec Alignment Patterns

### Acceptance Criteria Verification

**Read active spec:**
```
Read: file_path=".shipkit/specs/active/feature-name.md"
```

**Extract acceptance criteria:**
```
# Look for patterns like:
# - [ ] User can...
# - Given... When... Then...
# - AC1: ...
```

**For each criterion, verify implementation:**
```
# Example: "User can reset password"
Grep: pattern="(resetPassword|reset-password|forgotPassword)"
      glob="**/*.{ts,tsx}"
      output_mode="files_with_matches"

If empty: acceptance criterion not implemented
```

### Feature Flag Check

**Find feature references:**
```
Grep: pattern="FEATURE_FLAG_NAME|featureFlags\\.featureName"
      glob="**/*.{ts,tsx}"
      output_mode="content"
```

**Verify flag is documented:**
```
Grep: pattern="FEATURE_FLAG_NAME"
      path=".env.example"
      output_mode="count"

If count = 0: undocumented feature flag
```

---

## Common Verification Sequences

### "Is this component used?" Sequence

```
1. Glob: pattern="**/ComponentName.{ts,tsx}"
   → Confirms file exists (or NOT_CREATED if empty)

2. Read: file_path="[result from step 1]"
   → Get exported symbol names

3. Grep: pattern="import.*ComponentName|<ComponentName"
         glob="**/*.{ts,tsx}"
         output_mode="count"
   → Count usages

4. Classification:
   - Glob empty → NOT_CREATED
   - Grep count = 0 → CREATED_UNUSED
   - Grep count = 1 (only export) → CREATED_UNUSED
   - Grep count > 1 → Used (not an issue)
```

### "Is this route working?" Sequence

```
1. Glob: pattern="**/api/route-name/route.{ts,js}"
   → Confirms route file exists

2. Read: file_path="[route file]"
   → Check handler implementation

3. Grep: pattern="(GET|POST|PUT|DELETE|PATCH)"
         path="[route file]"
   → Verify HTTP methods exported

4. Grep: pattern="/api/route-name"
         glob="**/*.{ts,tsx}"
   → Find client-side calls

5. Classification:
   - Step 1 empty → Route NOT_CREATED
   - Step 3 empty → Route exists but no handlers
   - Step 4 empty → Route exists but unused (might be okay for new routes)
```

### "Is error handling complete?" Sequence

```
1. Grep: pattern="async function|async \\("
         path="src/changed-file.ts"
   → Find async functions

2. For each async function:
   Grep: pattern="try\\s*\\{|.catch\\("
         path="src/changed-file.ts"
         -A=20 -B=2  # Context around the async
   → Check for error handling

3. Classification:
   - Has try/catch or .catch() → Handled
   - No error handling → Unhandled async (report with line number)
```

---

## Evidence Citation Format

When reporting findings, use this format:

```markdown
**[Dimension]: [Issue Title]** [STATE_CLASSIFICATION]
- Evidence: `[Tool]("[pattern/path]")` → [result summary]
- Evidence: `[Tool]("[pattern/path]")` → [result summary]
- File: `path/to/file.ts:line`
- Classification: [STATE] (brief explanation)
- Impact: [What happens if not fixed]
```

**Example:**
```markdown
**Structural: Orphan component** [CREATED_UNUSED]
- Evidence: `Glob("**/PaymentForm.tsx")` → found at src/components/PaymentForm.tsx
- Evidence: `Grep("PaymentForm" in "**/*.tsx")` → 1 match (definition only, line 1)
- File: `src/components/PaymentForm.tsx`
- Classification: CREATED_UNUSED (component exists but never rendered)
- Impact: Dead code, likely incomplete payment feature
```

---

## Quick Reference Table

| Issue Type | Primary Tool | Pattern |
|------------|--------------|---------|
| File exists? | Glob | `**/FileName.*` |
| Symbol used? | Grep | `import.*SymbolName` |
| Component rendered? | Grep | `<ComponentName` |
| Route registered? | Glob + Grep | Route file + `/api/path` |
| Has error handling? | Grep | `try\s*\{` or `.catch(` |
| Has auth check? | Grep | `getSession\|requireAuth` |
| Has hardcoded secret? | Grep | `(secret\|key).*[:=].*['"]` |
| Acceptance criterion met? | Grep | Keywords from criterion |

---

## Pattern Expansion Patterns

When a changed file contains certain patterns, expand verification to ALL files with the same pattern.

### Auth Pattern Expansion

**Detect auth pattern in changed file:**
```
Grep: pattern="getSession|requireAuth|isAuthorized|auth\(\)"
      path="src/changed-file.ts"
      output_mode="count"
```

**If count > 0, expand to all auth files:**
```
Grep: pattern="getSession|requireAuth|isAuthorized|auth\(\)"
      glob="**/*.{ts,tsx}"
      output_mode="files_with_matches"

→ Add all matches to RIPPLE:auth scope
→ Verify consistent auth patterns across all files
```

### API Route Pattern Expansion

**Detect API route in changed file:**
```
Glob: pattern="**/api/**/*.{ts,js}"
```

**If changed file is API route, expand to all routes:**
```
Glob: pattern="**/api/**/route.{ts,js}"

→ Add all matches to RIPPLE:api scope
→ Check consistent response shapes (NextResponse vs Response)
→ Check consistent error handling patterns
```

### Validation Pattern Expansion

**Detect validation pattern in changed file:**
```
Grep: pattern="zod|z\.(string|number|object)|schema\.parse|\.safeParse"
      path="src/changed-file.ts"
      output_mode="count"
```

**If count > 0, expand to all validation code:**
```
Grep: pattern="z\.(string|number|object)|schema\.parse"
      glob="**/*.{ts,tsx}"
      output_mode="files_with_matches"

→ Add all matches to RIPPLE:validation scope
→ Verify schemas are imported from shared location
→ Check for inconsistent validation patterns
```

### Error Handling Pattern Expansion

**Detect error handling pattern in changed file:**
```
Grep: pattern="try\s*\{|\.catch\(|throw new"
      path="src/changed-file.ts"
      output_mode="count"
```

**If count > 0 AND file is async/API code, expand:**
```
Grep: pattern="async function|async \("
      glob="**/*.{ts,tsx}"
      output_mode="files_with_matches"

→ Add all matches to RIPPLE:error scope
→ Verify consistent error handling in async code
```

### Data Fetching Pattern Expansion

**Detect data fetching pattern in changed file:**
```
Grep: pattern="fetch\(|useSWR|useQuery|axios\."
      path="src/changed-file.ts"
      output_mode="count"
```

**If count > 0, expand to all fetching code:**
```
Grep: pattern="fetch\(|useSWR|useQuery"
      glob="**/*.{ts,tsx}"
      output_mode="files_with_matches"

→ Add all matches to RIPPLE:fetch scope
→ Verify consistent error handling on fetches
→ Check for loading/error state handling
```

### Pattern Expansion Decision Matrix

| Changed File Contains | Expand To | Check For |
|-----------------------|-----------|-----------|
| Auth patterns | All auth files | Consistent session checks |
| API route handlers | All API routes | Response shape consistency |
| Zod schemas | All validation code | Schema import consistency |
| Error handling | All async code | Consistent try/catch |
| Data fetching | All fetching code | Error/loading state handling |
