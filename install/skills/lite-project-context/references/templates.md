# Context File Templates

Templates for generating `.shipkit-lite/` context files.

---

## Template 1: stack.md

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

---

## Template 2: env-requirements.md

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

---

## Template 3: schema.md

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
