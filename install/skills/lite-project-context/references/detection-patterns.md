# Detection Patterns

Auto-detection patterns for framework, database, and styling libraries.

---

## Framework Detection

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

---

## Database Detection

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

---

## Styling Detection

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
