# Bash Commands for Scanning

Detailed bash commands for extracting project information.

---

## Detect Framework

```bash
# Check package.json for framework
grep -E '"(next|react|vue|svelte|nuxt|gatsby)"' package.json

# Detect framework version
grep '"next":' package.json | grep -oE '[0-9]+\.[0-9]+\.[0-9]+'
```

**Auto-detect patterns**:
- Next.js: `"next":` in dependencies
- React: `"react":` (check if Next.js also present)
- Vue: `"vue":`
- Svelte: `"svelte":`
- Remix: `"@remix-run/react":`

---

## Detect Database

```bash
# Check for database libraries
grep -E '"(supabase|prisma|drizzle|pg|mysql|mongodb)"' package.json

# Find migration files
# Supabase
find . -path "*/supabase/migrations/*.sql" 2>/dev/null | head -5

# Prisma
find . -name "schema.prisma" 2>/dev/null

# Drizzle
find . -path "*/drizzle/*.sql" 2>/dev/null | head -5
```

**Auto-detect patterns**:
- Supabase: `"@supabase/supabase-js":` + `supabase/migrations/` folder
- Prisma: `"@prisma/client":` + `prisma/schema.prisma`
- Drizzle: `"drizzle-orm":` + `drizzle/` folder
- Raw PostgreSQL: `"pg":`

---

## Detect Styling

```bash
# Check for styling libraries
grep -E '"(tailwindcss|styled-components|emotion|sass)"' package.json

# Check for UI libraries
grep -E '"(@radix-ui|@headlessui|@mui|antd|chakra-ui)"' package.json
```

---

## Scan Environment Variables

```bash
# Read .env.example if it exists
cat .env.example 2>/dev/null | grep -E '^[A-Z_]+=' | cut -d= -f1
```

---

## Scan Database Schema

```bash
# For Supabase: Read migration files
find supabase/migrations -name "*.sql" -exec grep -h "CREATE TABLE" {} \; 2>/dev/null

# For Prisma: Read schema.prisma
grep "model " prisma/schema.prisma 2>/dev/null
```

---

## Count Key Metrics

```bash
# Count dependencies
grep -c '":' package.json | head -1

# Count migration files
find supabase/migrations -name "*.sql" 2>/dev/null | wc -l

# Count env vars
cat .env.example 2>/dev/null | grep -c '^[A-Z_]+='
```

---

## Freshness Check Commands

### Windows (PowerShell/cmd)

```bash
# Check if stack.md exists
if exist .shipkit-lite\stack.md (echo exists) else (echo missing)

# Get last modified time (Windows - use forfiles)
forfiles /P .shipkit-lite /M stack.md /C "cmd /c echo @fdate @ftime" 2>nul
forfiles /P . /M package.json /C "cmd /c echo @fdate @ftime" 2>nul
```

### Linux/Mac (bash)

```bash
stat -c %Y .shipkit-lite/stack.md 2>/dev/null
stat -c %Y package.json 2>/dev/null
```
