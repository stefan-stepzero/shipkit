# Shipkit Stack Tooling

Tools, repos, and configurations specific to the Shipkit tech stack.

---

## The Stack

| Layer | Technology |
|-------|------------|
| **Framework** | Next.js (App Router) |
| **Hosting** | Vercel |
| **Database/Auth/Storage** | Supabase |
| **ORM** | Prisma |
| **Payments** | Lemon Squeezy |
| **Email** | Resend + React Email |
| **Styling** | Tailwind + shadcn/ui |

---

## External Skills (from skills.sh)

Skills that directly support this stack:

| Skill | Source | What It Helps With |
|-------|--------|-------------------|
| **vercel-react-best-practices** | vercel-labs/agent-skills | React patterns, Next.js conventions |
| **web-design-guidelines** | vercel-labs/agent-skills | UI/UX patterns |
| **supabase-postgres-best-practices** | supabase/agent-skills | RLS, queries, auth patterns |
| **tailwind-v4-shadcn** | jezweb/claude-skills | Tailwind v4 + shadcn patterns |
| **react-hook-form-zod** | jezweb/claude-skills | Form validation patterns |

### Installation

```bash
# Download skills for reference (Windows-friendly)
mkdir -p .claude/skills

# Vercel React patterns
curl -sL -o .claude/skills/vercel-react.md \
  https://raw.githubusercontent.com/vercel-labs/agent-skills/main/skills/vercel-react-best-practices/SKILL.md

# Supabase patterns
curl -sL -o .claude/skills/supabase.md \
  https://raw.githubusercontent.com/supabase/agent-skills/main/skills/supabase-postgres-best-practices/SKILL.md

# Tailwind + shadcn
curl -sL -o .claude/skills/tailwind-shadcn.md \
  https://raw.githubusercontent.com/jezweb/claude-skills/main/skills/tailwind-v4-shadcn/SKILL.md
```

---

## Stack-Specific Pre-Push Hooks

### Complete `.husky/pre-push` for Shipkit Stack

```bash
#!/bin/sh

echo "🚀 Running Shipkit stack checks..."

# 1. Prisma schema validation
echo "→ Validating Prisma schema..."
npx prisma validate || exit 1

# 2. Generate Prisma client (catches schema/client mismatch)
echo "→ Checking Prisma client..."
npx prisma generate || exit 1

# 3. TypeScript type check
echo "→ Type checking..."
npx tsc --noEmit || exit 1

# 4. Next.js lint
echo "→ Linting..."
npm run lint || exit 1

# 5. Run tests
echo "→ Running tests..."
npm test || exit 1

# 6. Next.js build (catches SSR issues, import errors)
echo "→ Verifying build..."
npm run build || exit 1

echo "✓ All checks passed!"
```

### Faster Version (Skip Build)

For quicker iteration, skip the build check:

```bash
#!/bin/sh

echo "🚀 Running quick checks..."

npx prisma validate || exit 1
npx tsc --noEmit || exit 1
npm run lint || exit 1
npm test || exit 1

echo "✓ Quick checks passed!"
```

---

## Stack-Specific Pre-Commit Hooks

### lint-staged Configuration

**package.json:**
```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md,css}": [
      "prettier --write"
    ],
    "prisma/schema.prisma": [
      "npx prisma validate",
      "npx prisma format"
    ]
  }
}
```

### Tailwind Class Sorting

Install Prettier plugin for consistent Tailwind class ordering:

```bash
npm install -D prettier-plugin-tailwindcss
```

**prettier.config.js:**
```javascript
module.exports = {
  plugins: ['prettier-plugin-tailwindcss'],
  tailwindConfig: './tailwind.config.ts',
}
```

---

## CLI Tools by Stack Component

### Next.js

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `next lint` | ESLint with Next.js rules | Pre-commit, pre-push |
| `next build` | Full production build | Pre-push, CI |
| `next dev --turbo` | Fast dev server | Development |

**Next.js lint config (eslint.config.js):**
```javascript
import { dirname } from "path";
import { fileURLToPath } from "url";
import { FlatCompat } from "@eslint/eslintrc";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname,
});

const eslintConfig = [
  ...compat.extends("next/core-web-vitals", "next/typescript"),
];

export default eslintConfig;
```

### Prisma

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `prisma validate` | Check schema syntax | Pre-commit, pre-push |
| `prisma format` | Format schema file | Pre-commit |
| `prisma generate` | Generate client types | After schema changes |
| `prisma db push` | Push schema to dev DB | Development |
| `prisma migrate dev` | Create migration | When ready to persist |
| `prisma migrate deploy` | Apply migrations | CI/CD, production |

**Pre-push safety for migrations:**
```bash
# In pre-push hook, warn about pending migrations
if npx prisma migrate status | grep -q "have not yet been applied"; then
  echo "⚠️  Warning: You have pending migrations"
  echo "Run 'npx prisma migrate dev' before pushing"
  # Don't exit 1 - just warn
fi
```

### Supabase

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `supabase start` | Start local Supabase | Development |
| `supabase db diff` | Generate migration from changes | After DB changes |
| `supabase gen types typescript` | Generate TS types from schema | After schema changes |
| `supabase db reset` | Reset local DB | Testing clean state |
| `supabase functions serve` | Local edge functions | Development |

**Type generation script (package.json):**
```json
{
  "scripts": {
    "db:types": "supabase gen types typescript --local > src/lib/database.types.ts"
  }
}
```

**Pre-push hook for Supabase types:**
```bash
# Check if database types are stale
if ! git diff --quiet src/lib/database.types.ts; then
  echo "⚠️  database.types.ts has uncommitted changes"
  echo "Run 'npm run db:types' and commit the result"
  exit 1
fi
```

### Vercel

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `vercel` | Deploy preview | Testing deployments |
| `vercel --prod` | Deploy production | Manual prod deploy |
| `vercel env pull` | Pull env vars locally | Setup, sync |
| `vercel build` | Local build matching Vercel | Debugging build issues |

**Vercel ignores (vercel.json):**
```json
{
  "git": {
    "deploymentEnabled": {
      "main": true,
      "dev": true
    }
  },
  "ignoreCommand": "git diff HEAD^ HEAD --quiet -- ."
}
```

### Lemon Squeezy

No CLI, but webhook testing tools:

| Tool | Purpose |
|------|---------|
| [Lemon Squeezy Webhook Tester](https://docs.lemonsqueezy.com/guides/developer-guide/webhooks) | Test webhook payloads locally |
| `ngrok` | Expose local server for webhook testing |

**Webhook testing setup:**
```bash
# Terminal 1: Run Next.js
npm run dev

# Terminal 2: Expose with ngrok
ngrok http 3000

# Copy ngrok URL to Lemon Squeezy dashboard as webhook URL
```

### Resend

| Command | Purpose |
|---------|---------|
| No CLI | Use API directly |

**Test email in development:**
```typescript
// src/lib/email.ts
import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

// In dev, log instead of send
export async function sendEmail(to: string, subject: string, html: string) {
  if (process.env.NODE_ENV === 'development') {
    console.log('📧 Email would be sent:', { to, subject });
    return { id: 'dev-mode' };
  }
  return resend.emails.send({ from: 'you@domain.com', to, subject, html });
}
```

---

## Type Safety Across the Stack

### End-to-End Type Flow

```
Supabase Schema
     ↓ (supabase gen types)
database.types.ts
     ↓ (import)
Prisma Schema (can reference)
     ↓ (prisma generate)
PrismaClient types
     ↓ (import)
API Routes / Server Actions
     ↓ (zod validation)
Frontend Components
```

### Recommended Type Generation Script

**package.json:**
```json
{
  "scripts": {
    "types:db": "supabase gen types typescript --local > src/lib/database.types.ts",
    "types:prisma": "prisma generate",
    "types:all": "npm run types:db && npm run types:prisma",
    "postinstall": "prisma generate"
  }
}
```

### Pre-push Type Check

```bash
#!/bin/sh

# Regenerate types and check for uncommitted changes
npm run types:all

if ! git diff --quiet src/lib/database.types.ts; then
  echo "❌ database.types.ts is out of sync"
  echo "Commit the updated types before pushing"
  exit 1
fi

# Then run tsc
npx tsc --noEmit || exit 1
```

---

## CI/CD for Shipkit Stack

### GitHub Actions Workflow

**.github/workflows/ci.yml:**
```yaml
name: CI

on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main]

env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
  NEXT_PUBLIC_SUPABASE_URL: ${{ secrets.NEXT_PUBLIC_SUPABASE_URL }}
  NEXT_PUBLIC_SUPABASE_ANON_KEY: ${{ secrets.NEXT_PUBLIC_SUPABASE_ANON_KEY }}

jobs:
  check:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Validate Prisma schema
        run: npx prisma validate

      - name: Generate Prisma client
        run: npx prisma generate

      - name: Lint
        run: npm run lint

      - name: Type check
        run: npx tsc --noEmit

      - name: Test
        run: npm test

      - name: Build
        run: npm run build

  # Optional: Deploy preview on PR
  preview:
    needs: check
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Vercel Preview
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
```

### Vercel + GitHub Integration (Simpler)

If using Vercel's GitHub integration, you get preview deploys automatically. Just need:

1. Connect repo to Vercel
2. Vercel runs `npm run build` on every push
3. Preview URL generated for every PR

The GitHub Actions above adds extra checks (Prisma, types) before Vercel even tries to build.

---

## Stack-Specific Gotchas

### 1. Prisma + Vercel Cold Starts

**Problem:** Prisma client not generated in Vercel build.

**Fix:** Add to package.json:
```json
{
  "scripts": {
    "postinstall": "prisma generate",
    "build": "prisma generate && next build"
  }
}
```

### 2. Supabase RLS + Server Actions

**Problem:** Server actions bypass RLS if using service role key.

**Fix:** Always use anon key + user JWT for server actions:
```typescript
import { createServerClient } from '@supabase/ssr'

export async function serverAction() {
  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!, // Not service role!
    { cookies }
  )
  // RLS policies now apply
}
```

### 3. Environment Variables in Next.js

**Problem:** Env vars not available client-side.

**Rule:**
- `NEXT_PUBLIC_*` → Available client + server
- Everything else → Server only

**Pre-push check for exposed secrets:**
```bash
# Check for non-public env vars in client code
if grep -r "process.env\." --include="*.tsx" src/components/ | grep -v "NEXT_PUBLIC"; then
  echo "❌ Found server-only env vars in client components"
  exit 1
fi
```

### 4. Tailwind + shadcn Class Conflicts

**Problem:** Custom classes override shadcn defaults unexpectedly.

**Fix:** Use `cn()` utility from shadcn:
```typescript
import { cn } from "@/lib/utils"

<Button className={cn("my-custom-class", props.className)} />
```

### 5. Lemon Squeezy Webhook Verification

**Problem:** Webhooks accepted without signature verification.

**Fix:** Always verify in production:
```typescript
import crypto from 'crypto';

export async function POST(req: Request) {
  const body = await req.text();
  const signature = req.headers.get('X-Signature');

  const hmac = crypto.createHmac('sha256', process.env.LEMON_SQUEEZY_WEBHOOK_SECRET!);
  const expectedSignature = hmac.update(body).digest('hex');

  if (signature !== expectedSignature) {
    return new Response('Invalid signature', { status: 401 });
  }

  // Process webhook...
}
```

---

## Complete package.json Scripts

```json
{
  "scripts": {
    "dev": "next dev --turbo",
    "build": "prisma generate && next build",
    "start": "next start",
    "lint": "next lint",
    "typecheck": "tsc --noEmit",
    "test": "vitest run",
    "test:watch": "vitest",

    "db:push": "prisma db push",
    "db:migrate": "prisma migrate dev",
    "db:studio": "prisma studio",
    "db:types": "supabase gen types typescript --local > src/lib/database.types.ts",

    "types:all": "npm run db:types && prisma generate",

    "check": "npm run lint && npm run typecheck && npm test",
    "check:all": "npm run check && npm run build",

    "prepare": "husky",
    "postinstall": "prisma generate"
  }
}
```

---

## Quick Setup Checklist

### Initial Setup (New Project)

```bash
# 1. Create Next.js app
npx create-next-app@latest my-app --typescript --tailwind --eslint --app

# 2. Add Prisma
npm install prisma @prisma/client
npx prisma init

# 3. Add Supabase
npm install @supabase/supabase-js @supabase/ssr

# 4. Add shadcn/ui
npx shadcn@latest init

# 5. Add dev dependencies
npm install -D husky lint-staged prettier prettier-plugin-tailwindcss vitest

# 6. Setup husky
npx husky init

# 7. Create hooks (copy from sections above)
```

### Environment Setup

**.env.local:**
```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# Database (for Prisma)
DATABASE_URL=

# Lemon Squeezy
LEMON_SQUEEZY_API_KEY=
LEMON_SQUEEZY_WEBHOOK_SECRET=

# Resend
RESEND_API_KEY=
```

**.env.example:** (commit this)
```bash
# Copy to .env.local and fill in values

NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
DATABASE_URL=
LEMON_SQUEEZY_API_KEY=
LEMON_SQUEEZY_WEBHOOK_SECRET=
RESEND_API_KEY=
```

---

## Related Resources

- [Next.js Docs](https://nextjs.org/docs)
- [Prisma Docs](https://www.prisma.io/docs)
- [Supabase Docs](https://supabase.com/docs)
- [shadcn/ui Docs](https://ui.shadcn.com)
- [Lemon Squeezy Docs](https://docs.lemonsqueezy.com)
- [Resend Docs](https://resend.com/docs)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
