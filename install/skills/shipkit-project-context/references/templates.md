# Templates for Project Context Files

Output templates for stack.json, env-requirements.md, and schema.json.

---

## stack.json Template

```markdown
# Tech Stack

**Generated**: [YYYY-MM-DD]

## Core

| Layer | Technology | Version |
|-------|------------|---------|
| Framework | [Next.js/Remix/etc] | [major.minor] |
| Database | [PostgreSQL/MongoDB/etc] | — |
| ORM | [Prisma/Drizzle/Supabase] | — |
| Styling | [Tailwind/CSS Modules/etc] | — |
| Auth | [NextAuth/Supabase Auth/etc] | — |

## Working Patterns

### Provider Hierarchy

[List providers from outermost to innermost, if detected]

1. `QueryClientProvider` (React Query)
2. `AuthProvider` (Supabase)
3. `ThemeProvider` (next-themes)

*If not detected: "Run `/shipkit-project-context` after adding providers"*

### API Patterns

| Pattern | Location | Methods |
|---------|----------|---------|
| [Auth] | `/api/auth/*` | POST |
| [CRUD] | `/api/[resource]/*` | GET, POST, PUT, DELETE |
| [Server Actions] | `/app/actions/*` | — |

*If not detected: "API structure varies - check individual routes"*

### Component Conventions

| Aspect | Convention |
|--------|------------|
| Location | `src/components/` |
| Structure | [Flat/Feature folders/Domain folders] |
| Naming | [PascalCase/kebab-case] |
| Tests | [Co-located/Separate __tests__] |

### Import Aliases

| Alias | Path |
|-------|------|
| `@/*` | `./src/*` |
| `@/components/*` | `./src/components/*` |

*If none configured: "No import aliases configured"*

## Key Dependencies

[List only key deps, not exhaustive list]

- **UI**: shadcn/ui, Radix
- **Forms**: react-hook-form, zod
- **State**: React Query
- **Payments**: Stripe

## Project Structure

```
[project-root]/
├── src/
│   ├── app/          # App Router pages
│   ├── components/   # React components
│   ├── lib/          # Utilities
│   └── ...
├── supabase/         # Supabase config
└── ...
```

## Available CLIs

| CLI | Status | Use For |
|-----|--------|---------|
| supabase | [Installed/Missing] | `db diff`, `db push`, `functions deploy` |
| stripe | [Installed/Missing] | `listen`, `trigger`, `logs tail` |
| vercel | [Installed/Missing] | `deploy`, `env pull`, `dev` |
| gh | [Installed/Missing] | `pr create`, `issue`, `api` |

**Recommended installs**: [List if any are missing but should be installed]
```

---

## env-requirements.md Template

```markdown
# Environment Variables

**Generated**: [YYYY-MM-DD]
**Source**: `.env.example`

## Required Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `DATABASE_URL` | PostgreSQL connection | `postgresql://...` |
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project URL | `https://xxx.supabase.co` |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anon key | `eyJ...` |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase admin key | `eyJ...` |

## Optional Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `NEXT_PUBLIC_APP_URL` | App base URL | `http://localhost:3000` |
| `LOG_LEVEL` | Logging verbosity | `info` |

## Third-Party Services

| Service | Required Variables |
|---------|-------------------|
| Stripe | `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET` |
| Resend | `RESEND_API_KEY` |
| OpenAI | `OPENAI_API_KEY` |

## Setup Instructions

1. Copy `.env.example` to `.env.local`
2. Fill in required variables from Supabase dashboard
3. For Stripe: run `stripe login` then `stripe listen --forward-to localhost:3000/api/webhooks`
4. For production: set all variables in Vercel/hosting platform
```

---

## schema.json Template

```json
{
  "$schema": "shipkit-artifact",
  "type": "schema",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DD",
  "source": "shipkit-project-context",

  "summary": {
    "tableCount": 3,
    "migrationCount": 3,
    "lastMigration": "20240201_add_subscriptions.sql",
    "schemaSource": "supabase/migrations/*.sql"
  },

  "tables": [
    {
      "name": "users",
      "columns": [
        { "name": "id", "type": "uuid", "constraints": ["PK", "default uuid_generate_v4()"] },
        { "name": "email", "type": "text", "constraints": ["NOT NULL", "UNIQUE"] },
        { "name": "created_at", "type": "timestamptz", "constraints": ["NOT NULL", "default now()"] }
      ],
      "indexes": [
        { "name": "users_email_idx", "columns": ["email"] }
      ]
    },
    {
      "name": "profiles",
      "columns": [
        { "name": "id", "type": "uuid", "constraints": ["PK", "FK → users.id"] },
        { "name": "full_name", "type": "text", "constraints": [] },
        { "name": "avatar_url", "type": "text", "constraints": [] }
      ],
      "indexes": []
    }
  ],

  "relationships": [
    { "from": "profiles.id", "to": "users.id", "type": "1:1" },
    { "from": "users.id", "to": "subscriptions.user_id", "type": "1:*" },
    { "from": "subscriptions.product_id", "to": "products.id", "type": "*:1" }
  ],

  "migrations": [
    { "order": 1, "file": "20240101_init.sql", "description": "Initial schema" },
    { "order": 2, "file": "20240115_add_profiles.sql", "description": "Add profiles table" },
    { "order": 3, "file": "20240201_add_subscriptions.sql", "description": "Add subscription tables" }
  ]
}
```

---

## Template Usage Guidelines

### Keep it Minimal

**Good**:
```markdown
| Framework | Next.js | 14 |
```

**Avoid**:
```markdown
| Framework | Next.js (React-based full-stack framework with App Router, Server Components, Server Actions, ISR, middleware, and edge functions) | 14.2.15 |
```

### Mark Unknown Items

```markdown
| Database | PostgreSQL | — |
| ORM | TBD | — |
```

Use `TBD` for items that need human input.
Use `—` for version when not relevant.

### Skip Empty Sections

If no API routes are detected, either:
1. Note "No API routes detected"
2. Or skip the section entirely

Don't fill with placeholder content.

### Working Patterns Are Key

The Working Patterns section is the most valuable part of stack.json. It tells Claude:
- What order to wrap providers
- How to structure new API routes
- How to name and organize components
- What import aliases to use

**This section directly impacts implementation quality.**
