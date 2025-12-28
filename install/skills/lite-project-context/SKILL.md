---
name: lite-project-context
description: Maintains current tech stack, environment variables, and database schema through selective scanning with smart caching. Only rescans when source files are newer than cached context. Use when starting a project or when stack.md becomes stale.
---

# project-context-lite - Smart Project Context Scanner

**Purpose**: Generate and maintain lightweight project context files (stack, env, schema) by scanning package files, configs, and migrations. Uses file modification time checks to avoid unnecessary rescans.

---

## When to Invoke

**User triggers**:
- "Scan the project"
- "Update context"
- "Rescan stack"
- "Generate project context"
- "What's my tech stack?"

**Auto-triggered by**:
- `shipkit-master-lite` (when stack.md is missing or stale)
- `project-status-lite` (when it detects staleness)

**First run**:
- No `.shipkit-lite/` directory exists
- User starts new Shipkit Lite project

---

## Prerequisites

**Required**:
- Project has `package.json` (or equivalent dependency file)

**Optional but helpful**:
- `.env.example` (for env requirements)
- Database migration files (for schema)
- Config files (next.config.js, tailwind.config.js, etc.)

---

## Process

### Step 1: Check Freshness (Smart Caching)

**Before doing any work**, check if rescan is needed:

**Commands to use**:
```bash
# Windows (PowerShell/cmd)
# Check if stack.md exists
if exist .shipkit-lite\stack.md (echo exists) else (echo missing)

# Get last modified time (Windows - use forfiles)
forfiles /P .shipkit-lite /M stack.md /C "cmd /c echo @fdate @ftime" 2>nul
forfiles /P . /M package.json /C "cmd /c echo @fdate @ftime" 2>nul

# Linux/Mac (bash)
stat -c %Y .shipkit-lite/stack.md 2>/dev/null
stat -c %Y package.json 2>/dev/null
```

**Freshness logic**:
1. If `.shipkit-lite/stack.md` doesn't exist → First run, proceed to Step 2
2. If `stack.md` exists:
   - Compare modification times
   - If `stack.md` newer than `package.json` → **SKIP SCAN**, just read cached file
   - If `package.json` newer than `stack.md` → Ask user to confirm rescan

**Token savings**:
- Cached read: ~100-200 tokens (read 3 files)
- Full scan: ~1,500 tokens (grep, find, generate)

---

### Step 2: Ask Before Heavy Work

**If rescan is needed, ask user first**:

**First run**:
```
📦 First run detected - no context files exist.

I can scan your project to generate:
  • .shipkit-lite/stack.md (tech stack)
  • .shipkit-lite/env-requirements.md (environment variables)
  • .shipkit-lite/schema.md (database schema)

This will scan:
  • package.json (dependencies)
  • .env.example (env vars)
  • Database migrations (schema)

Scan now? (yes/no)
```

**Stale context**:
```
⚠️  Context appears stale:
  • package.json modified: [date]
  • stack.md last updated: [date]

Rescan project to refresh context? (yes/no)
```

**If user says no**: "Okay, using existing context. Run `/lite-project-context` when you want to update."

**If user says yes**: Proceed to Step 3.

---

### Step 3: Scan Project Files

**Use bash commands (grep, find) to extract information**:

#### Detect Framework
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

#### Detect Database
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

#### Detect Styling
```bash
# Check for styling libraries
grep -E '"(tailwindcss|styled-components|emotion|sass)"' package.json

# Check for UI libraries
grep -E '"(@radix-ui|@headlessui|@mui|antd|chakra-ui)"' package.json
```

#### Scan Environment Variables
```bash
# Read .env.example if it exists
cat .env.example 2>/dev/null | grep -E '^[A-Z_]+=' | cut -d= -f1
```

#### Scan Database Schema
```bash
# For Supabase: Read migration files
find supabase/migrations -name "*.sql" -exec grep -h "CREATE TABLE" {} \; 2>/dev/null

# For Prisma: Read schema.prisma
grep "model " prisma/schema.prisma 2>/dev/null
```

**Count key metrics**:
```bash
# Count dependencies
grep -c '":' package.json | head -1

# Count migration files
find supabase/migrations -name "*.sql" 2>/dev/null | wc -l

# Count env vars
cat .env.example 2>/dev/null | grep -c '^[A-Z_]+='
```

---

### Step 4: Generate Context Files

**Use Write tool to create 3 files**.

#### File 1: `.shipkit-lite/stack.md`

**Template**:
```markdown
# Tech Stack

**Last scanned**: [YYYY-MM-DD HH:MM]
**Source**: package.json

---

## Framework

**[Framework Name] [Version]**
- Type: [SSR/SPA/Static/etc]
- Router: [App Router/Pages Router/Vue Router/etc]

---

## Database

**[Database Name]**
- ORM/Client: [Prisma/Supabase client/Drizzle/etc]
- Migrations: [Location of migration files]
- Auth: [Supabase Auth/NextAuth/Clerk/etc]

---

## Styling

**[Tailwind CSS/Styled Components/etc] [Version]**
- UI Components: [shadcn/ui, Radix, MUI, etc]
- Icons: [Lucide, Heroicons, etc]

---

## Key Dependencies

**Runtime:**
- [Dependency 1] [Version]
- [Dependency 2] [Version]

**Development:**
- TypeScript [Version]
- [Build tool] [Version]

---

## Project Structure Detected

**Framework conventions:**
- [e.g., Next.js App Router: app/ directory]
- [e.g., API routes: app/api/]

**Database location:**
- [e.g., supabase/migrations/]
- [e.g., prisma/schema.prisma]

---

## Total Dependencies

- **Runtime**: [X] packages
- **Development**: [Y] packages
- **Total**: [Z] packages
```

**Example output**:
```markdown
# Tech Stack

**Last scanned**: 2025-01-15 14:32
**Source**: package.json

---

## Framework

**Next.js 14.2.1**
- Type: SSR (App Router)
- Router: App Router
- React: 18.2.0

---

## Database

**Supabase (PostgreSQL)**
- ORM/Client: @supabase/supabase-js 2.39.0
- Migrations: supabase/migrations/
- Auth: Supabase Auth

---

## Styling

**Tailwind CSS 3.4.1**
- UI Components: shadcn/ui (Radix primitives)
- Icons: lucide-react

---

## Key Dependencies

**Runtime:**
- zod 3.22.4 (validation)
- react-hook-form 7.50.0
- date-fns 3.3.0

**Development:**
- TypeScript 5.3.3
- ESLint 8.56.0

---

## Project Structure Detected

**Framework conventions:**
- Next.js App Router: app/ directory
- API routes: app/api/
- Components: components/

**Database location:**
- supabase/migrations/
- 12 migration files detected

---

## Total Dependencies

- **Runtime**: 18 packages
- **Development**: 15 packages
- **Total**: 33 packages
```

---

#### File 2: `.shipkit-lite/env-requirements.md`

**Template**:
```markdown
# Environment Variables

**Last scanned**: [YYYY-MM-DD HH:MM]
**Source**: .env.example

---

## Required Variables

[For each env var in .env.example that has no default value]

### `[VAR_NAME]`
- **Purpose**: [Infer from name or add placeholder]
- **Example**: [Value from .env.example if present, or "your_value_here"]

---

## Optional Variables

[For each env var in .env.example that has a default value or is commented]

### `[VAR_NAME]`
- **Purpose**: [Infer from name]
- **Default**: [Default value if present]

---

## Setup Instructions

1. Copy `.env.example` to `.env.local`:
   ```bash
   cp .env.example .env.local
   ```

2. Fill in required variables:
   - `[VAR_NAME_1]` - [Get from...]
   - `[VAR_NAME_2]` - [Get from...]

3. Verify setup:
   ```bash
   [Command to test env vars are loaded]
   ```

---

## Notes

- ⚠️  Never commit `.env.local` to git
- 📝 Update `.env.example` when adding new variables
- 🔒 Store secrets in [Vercel/Railway/etc] environment variables for production
```

**Example output**:
```markdown
# Environment Variables

**Last scanned**: 2025-01-15 14:32
**Source**: .env.example

---

## Required Variables

### `NEXT_PUBLIC_SUPABASE_URL`
- **Purpose**: Supabase project URL
- **Example**: https://abcdefghijklmnop.supabase.co

### `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- **Purpose**: Supabase anonymous/public key
- **Example**: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

### `SUPABASE_SERVICE_ROLE_KEY`
- **Purpose**: Supabase service role key (admin access)
- **Example**: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

---

## Optional Variables

### `NEXT_PUBLIC_APP_URL`
- **Purpose**: Public URL of the application
- **Default**: http://localhost:3000

---

## Setup Instructions

1. Copy `.env.example` to `.env.local`:
   ```bash
   cp .env.example .env.local
   ```

2. Fill in required variables:
   - `NEXT_PUBLIC_SUPABASE_URL` - Get from Supabase project settings
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY` - Get from Supabase project settings → API
   - `SUPABASE_SERVICE_ROLE_KEY` - Get from Supabase project settings → API

3. Verify setup:
   ```bash
   npm run dev
   ```

---

## Notes

- ⚠️  Never commit `.env.local` to git
- 📝 Update `.env.example` when adding new variables
- 🔒 Store secrets in Vercel environment variables for production
```

---

#### File 3: `.shipkit-lite/schema.md`

**Template**:
```markdown
# Database Schema

**Last scanned**: [YYYY-MM-DD HH:MM]
**Source**: [supabase/migrations/*.sql or prisma/schema.prisma or drizzle/...]

---

## Tables

### `[table_name_1]`

**Columns:**
- `id` - [type] - [Primary key/constraints]
- `[column_2]` - [type] - [constraints]
- `created_at` - timestamp - [default]

**Indexes:**
- [Index descriptions if detected]

**Relationships:**
- [Foreign keys if detected]

---

### `[table_name_2]`

[Same structure as above]

---

## Relationships Diagram

```
[table_1]
  └─ id → [table_2].foreign_key_id

[table_2]
  └─ id → [table_3].foreign_key_id
```

---

## Migration History

**Total migrations**: [X] files

**Latest migration**: [filename]
- **Applied**: [date from filename if timestamp-based]
- **Changes**: [Brief description of what it does]

---

## Notes

- 🔄 Run migrations: `[command based on detected DB tool]`
- 📝 Schema last modified: [date of newest migration file]
- ⚠️  Manual schema changes should be done via migrations, not direct SQL
```

**Example output**:
```markdown
# Database Schema

**Last scanned**: 2025-01-15 14:32
**Source**: supabase/migrations/*.sql

---

## Tables

### `users`

**Columns:**
- `id` - uuid - Primary key
- `email` - text - Unique, not null
- `created_at` - timestamptz - Default: now()

**Indexes:**
- Unique index on `email`

**Relationships:**
- Referenced by: `recipes.user_id`, `favorites.user_id`

---

### `recipes`

**Columns:**
- `id` - uuid - Primary key
- `user_id` - uuid - Foreign key → users.id
- `title` - text - Not null
- `ingredients` - text[] - Array of ingredients
- `instructions` - text
- `created_at` - timestamptz - Default: now()

**Indexes:**
- Index on `user_id`

**Relationships:**
- `user_id` → `users.id` (CASCADE on delete)

---

### `favorites`

**Columns:**
- `user_id` - uuid - Foreign key → users.id
- `recipe_id` - uuid - Foreign key → recipes.id
- `created_at` - timestamptz - Default: now()

**Indexes:**
- Primary key: `(user_id, recipe_id)`

**Relationships:**
- `user_id` → `users.id`
- `recipe_id` → `recipes.id`

---

## Relationships Diagram

```
users
  ├─ id → recipes.user_id
  └─ id → favorites.user_id

recipes
  └─ id → favorites.recipe_id
```

---

## Migration History

**Total migrations**: 12 files

**Latest migration**: `20250115143000_add_favorites_table.sql`
- **Applied**: 2025-01-15
- **Changes**: Added favorites table with composite primary key

---

## Notes

- 🔄 Run migrations: `supabase db push`
- 📝 Schema last modified: 2025-01-15
- ⚠️  Manual schema changes should be done via migrations, not direct SQL
```

---

### Step 5: Confirm Completion

**Output to user**:
```
✅ Project context generated

📁 Created:
  • .shipkit-lite/stack.md
  • .shipkit-lite/env-requirements.md
  • .shipkit-lite/schema.md

📊 Summary:
  • Framework: [Next.js 14.2.1]
  • Database: [Supabase (PostgreSQL)]
  • Dependencies: [33 total]
  • Env vars: [4 required, 1 optional]
  • Tables: [3 detected]

📝 Context is now cached. I'll only rescan when package.json changes.

👉 Next: /lite-project-status
   See overall project health and next steps

Ready to continue?
```

---

## What Makes This "Lite"

**Included**:
- ✅ Smart caching via file modification time checks
- ✅ Auto-detection of framework, database, styling
- ✅ Environment variable scanning
- ✅ Basic schema extraction from migrations
- ✅ Dependency counting

**Not included** (vs full project-context):
- ❌ Deep dependency analysis (vulnerability scanning)
- ❌ Architecture diagram generation
- ❌ API endpoint discovery
- ❌ Component tree mapping
- ❌ Test coverage analysis
- ❌ Performance benchmarking
- ❌ Multi-environment config management

**Philosophy**: Just enough context to understand the stack and start building.

---

## Freshness Check Logic

**When to skip rescan**:
```
IF stack.md exists
  AND stack.md modification time > package.json modification time
  AND stack.md modification time > package-lock.json modification time
  THEN → Read cached files only (~100 tokens)
```

**When to suggest rescan**:
```
IF stack.md exists
  BUT package.json modification time > stack.md modification time
  OR package-lock.json modification time > stack.md modification time
  THEN → Ask user: "Context appears stale. Rescan?"
```

**When to auto-scan** (no asking):
```
IF .shipkit-lite/stack.md doesn't exist
  THEN → This is first run, scan automatically after user confirms
```

---

## Integration with Other Skills

**Before project-context-lite**:
- None - This is often the FIRST skill run

**After project-context-lite**:
- `shipkit-master-lite` - Reads stack.md, architecture.md at session start
- `project-status-lite` - Uses context to suggest next steps
- `plan-lite` - References stack.md for tech choices
- `implement-lite` - References stack.md and schema.md while coding
- `spec-lite` - References stack.md for technical constraints

**Triggered by**:
- `shipkit-master-lite` - When stack.md missing or stale
- `project-status-lite` - When detecting staleness

---

## Context Files This Skill Reads

**To check freshness**:
- `.shipkit-lite/stack.md` (check if exists and modification time)
- `package.json` (modification time)
- `package-lock.json` or `pnpm-lock.yaml` or `yarn.lock` (modification time)

**To generate context**:
- `package.json` (dependencies, scripts)
- `package-lock.json` or equivalent (version locking)
- `.env.example` (environment variables)
- `supabase/migrations/*.sql` or `prisma/schema.prisma` or `drizzle/*.sql` (schema)
- Config files: `next.config.js`, `tailwind.config.js`, etc. (optional)

---

## Context Files This Skill Writes

**Write Strategy: OVERWRITE AND REPLACE**

All context files are **completely replaced** on each scan. No history is preserved because:
- Context files are snapshots of *current* state, not historical records
- Source files (`package.json`, migrations) already provide history via git
- Smart caching prevents unnecessary overwrites (only rescan when sources change)
- Old context has no value - you only need to know the current stack

**Creates** (first run):
- `.shipkit-lite/stack.md`
- `.shipkit-lite/env-requirements.md`
- `.shipkit-lite/schema.md`

**Updates** (rescan):
- Same 3 files (overwrites with fresh data)
- **Each file timestamp updates** to mark freshness
- **Old content is discarded** - no append, no archive

**Never modifies**:
- Source files (package.json, migrations, etc.) - read-only

**Why OVERWRITE?**
- Context files are *derived* from source files (not primary data)
- Adding a dependency makes old stack info obsolete, not historical
- Freshness checks rely on file modification times
- Appending would create duplicates and break freshness logic
- Archiving adds complexity with no benefit (source files are the archive)

---

## Lazy Loading Behavior

**This skill uses smart caching**:

1. User invokes `/lite-project-context`
2. Check if `.shipkit-lite/stack.md` exists
3. **Fast path** (stack.md is fresh):
   - Read stack.md (~50 tokens)
   - Read env-requirements.md (~30 tokens)
   - Read schema.md (~100 tokens)
   - Total: ~180 tokens
   - Display summary, suggest next skill
4. **Slow path** (first run or stale):
   - Ask user to confirm scan
   - Scan package.json (~300 tokens)
   - Scan .env.example (~100 tokens)
   - Scan migrations (~500 tokens)
   - Generate 3 files (~500 tokens)
   - Total: ~1,400 tokens

**Token savings over sessions**:
- First run: 1,400 tokens
- Subsequent runs (fresh): 180 tokens (87% reduction)

---

## Detection Patterns

### Framework Detection

```bash
# Next.js
grep '"next":' package.json → "Next.js"
grep '"app-dir"' next.config.js → "App Router" vs "Pages Router"

# React (standalone)
grep '"react":' package.json AND NOT grep '"next":' → "React SPA"

# Vue
grep '"vue":' package.json → "Vue.js"

# Svelte
grep '"svelte":' package.json → "Svelte"

# Remix
grep '"@remix-run/react":' package.json → "Remix"
```

### Database Detection

```bash
# Supabase
grep '"@supabase/supabase-js":' package.json
find supabase/migrations -name "*.sql" | wc -l → migration count

# Prisma
grep '"@prisma/client":' package.json
cat prisma/schema.prisma | grep "model " | wc -l → model count

# Drizzle
grep '"drizzle-orm":' package.json
find drizzle -name "*.sql" | wc -l

# MongoDB
grep '"mongodb":' package.json → "MongoDB"
```

### Styling Detection

```bash
# Tailwind CSS
grep '"tailwindcss":' package.json → "Tailwind CSS"

# shadcn/ui
grep '"@radix-ui' package.json → "shadcn/ui (Radix primitives)"

# Styled Components
grep '"styled-components":' package.json → "Styled Components"

# CSS Modules
find . -name "*.module.css" | head -1 → "CSS Modules"
```

---

## Success Criteria

Context generation is complete when:
- [ ] `.shipkit-lite/stack.md` exists with framework, database, styling, dependencies
- [ ] `.shipkit-lite/env-requirements.md` exists with all env vars from .env.example
- [ ] `.shipkit-lite/schema.md` exists with tables, columns, relationships (if migrations found)
- [ ] Modification times are current (fresher than source files)
- [ ] User can see summary of what was detected

---

## Tips for Effective Context Scanning

**Auto-detection is best**:
- Don't ask user "What framework do you use?" - scan package.json
- Don't ask "What database?" - detect from migrations folder
- Only ask when truly ambiguous

**Keep it focused**:
- POC needs basic stack info only
- Don't over-analyze dependencies
- Skip advanced features for lite version

**Cache aggressively**:
- Check modification times before every scan
- Read cached files when fresh
- Save 80%+ tokens on subsequent runs

**When to manually trigger rescan**:
- After `npm install [new-package]`
- After adding new migrations
- After updating .env.example
- After major framework version bump

**When to upgrade to full /project-context**:
- Need dependency vulnerability scanning
- Need architecture diagram generation
- Need API endpoint discovery
- Need comprehensive analysis

---

## Special Cases

### Monorepo Detection

**If package.json has workspaces**:
```bash
grep '"workspaces":' package.json
```

**Behavior**:
- Scan root package.json
- List workspace packages
- Suggest: "Monorepo detected. Run `/lite-project-context` in each workspace for detailed context."

### No Database Detected

**If no migrations or schema files found**:
- Still generate schema.md with note: "No database detected. Add migrations to supabase/migrations/ to auto-update schema."

### No .env.example

**If .env.example doesn't exist**:
- Generate env-requirements.md with note: "No .env.example found. Create one to document required environment variables."
- Check if .env exists: "⚠️ Found .env but no .env.example. Consider creating .env.example (without secrets) for documentation."

---

## Example Flows

### Flow 1: First Run
```
User: "Scan the project"

Claude:
1. Check .shipkit-lite/stack.md → doesn't exist
2. Ask: "First run detected. Scan now?"
3. User: "Yes"
4. Scan package.json → Next.js 14, React 18, Tailwind 3
5. Scan .env.example → 4 required vars
6. Scan supabase/migrations → 3 tables
7. Generate stack.md, env-requirements.md, schema.md
8. Output: "✅ Context generated. 33 deps, 3 tables, 4 env vars."
9. Suggest: "Run `/lite-project-status` to see project health"
```

### Flow 2: Cached Read (Fresh Context)
```
User: "What's my stack?"

Claude:
1. Check .shipkit-lite/stack.md → exists
2. Compare times: stack.md (Jan 15 14:32) > package.json (Jan 14 10:00)
3. Context is fresh, skip scan
4. Read stack.md (~50 tokens)
5. Output summary from cached file
6. "Context last updated: Jan 15. Still fresh."
```

### Flow 3: Stale Context
```
User: "Update context"

Claude:
1. Check .shipkit-lite/stack.md → exists
2. Compare times: package.json (Jan 16 09:00) > stack.md (Jan 15 14:32)
3. Ask: "⚠️ Context appears stale. Rescan?"
4. User: "Yes"
5. Rescan all files
6. Detect new dependency: zod added
7. Regenerate stack.md with updated info
8. Output: "✅ Context refreshed. 34 deps (was 33), added zod."
```

### Flow 4: Triggered by shipkit-master-lite
```
Session start → shipkit-master-lite loads

shipkit-master-lite:
1. Try to read .shipkit-lite/stack.md → doesn't exist
2. Output: "⚠️ No project context found."
3. Suggest: "Run `/lite-project-context` to scan your project first."

User: "/lite-project-context"

[Follow first run flow]
```

---

**Remember**: This skill is about **smart context generation with aggressive caching**. Scan once, read many times. Only rescan when source files actually change.
