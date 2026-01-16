---
name: lite-project-context
description: "Use when starting a new project or refreshing tech stack context. Triggers: 'scan project', 'what's my stack', 'refresh context', 'generate stack'."
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

**Before doing any work**, check if rescan is needed.

**Commands**: See `references/bash-commands.md` for platform-specific freshness checks

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

**Use bash commands (grep, find) to extract information.**

**Detailed commands**: See `references/bash-commands.md` for complete scanning commands

**What to detect**:
- Framework: Next.js, React, Vue, Svelte, Remix (from package.json)
- Database: Supabase, Prisma, Drizzle, MongoDB (from dependencies + migration files)
- Styling: Tailwind, shadcn/ui, Styled Components (from dependencies)
- Environment variables: Parse .env.example
- Database schema: Extract from migrations or schema files
- Metrics: Count dependencies, migrations, env vars

---

### Step 4: Generate Context Files

**Use Write tool to create 3 files**.

#### File 1: `.shipkit-lite/stack.md`

**Template**: See `references/templates.md` for complete stack.md template

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

**Template**: See `references/templates.md` for complete env-requirements.md template

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

**Template**: See `references/templates.md` for complete schema.md template

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

## Completion Checklist

Copy and track:
- [ ] Scanned package.json and project structure
- [ ] Identified tech stack and dependencies
- [ ] Created `.shipkit-lite/stack.md`
- [ ] Invoke `/lite-whats-next` for workflow guidance

**REQUIRED FINAL STEP:** After completing this skill, you MUST invoke `/lite-whats-next` for workflow guidance. This is mandatory per lite.md meta-rules.

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

## When This Skill Integrates with Others

### Before This Skill
- None - This is often the FIRST skill run in a new project
  - **When**: User opens project for the first time with Shipkit Lite
  - **Why**: Need to understand tech stack before doing any work
  - **Trigger**: No `.shipkit-lite/` directory exists

### After This Skill
- `/lite-project-status` - Uses context to suggest next steps
  - **When**: After initial context scan
  - **Why**: Status needs stack.md to assess project health
  - **Trigger**: User wants to see what to work on next

- `/lite-spec` - References stack.md for technical constraints
  - **When**: Writing feature specifications
  - **Why**: Specs must align with chosen framework/database
  - **Trigger**: User asks to spec a feature

- `/lite-plan` - References stack.md for tech choices
  - **When**: Planning implementation
  - **Why**: Plans must use existing stack, not invent new tech
  - **Trigger**: User asks to plan a feature

- `/lite-implement` - References stack.md and schema.md while coding
  - **When**: Writing code
  - **Why**: Code must match framework conventions and database schema
  - **Trigger**: User starts implementation

### Triggered By
- `/lite-shipkit-master` - When stack.md missing or stale
  - **When**: Session starts
  - **Why**: Master needs context to route skills properly
  - **Trigger**: Missing or outdated stack.md detected

- `/lite-project-status` - When detecting staleness
  - **When**: Checking project health
  - **Why**: Stale context gives wrong suggestions
  - **Trigger**: package.json newer than stack.md

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

**See `references/detection-patterns.md` for complete patterns:**
- Framework detection (Next.js, React, Vue, Svelte, Remix)
- Database detection (Supabase, Prisma, Drizzle, MongoDB)
- Styling detection (Tailwind, shadcn/ui, Styled Components, CSS Modules)
- Special cases (monorepos, no database, no .env.example)

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

## Example Flows

**See `references/example-flows.md` for complete flows:**
- Flow 1: First Run
- Flow 2: Cached Read (Fresh Context)
- Flow 3: Stale Context
- Flow 4: Triggered by shipkit-master-lite

---

**Remember**: This skill is about **smart context generation with aggressive caching**. Scan once, read many times. Only rescan when source files actually change.
