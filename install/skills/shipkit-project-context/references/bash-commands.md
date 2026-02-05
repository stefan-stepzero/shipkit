# Bash Commands for Project Context

Platform-specific commands for scanning project files and checking freshness.

---

## Freshness Check Commands

### Check Modification Times

**Windows (PowerShell-compatible)**:
```bash
# Get modification time of stack.md
(Get-Item ".shipkit/stack.md" -ErrorAction SilentlyContinue).LastWriteTime

# Get modification time of package.json
(Get-Item "package.json").LastWriteTime

# Compare: is stack.md newer than package.json?
# (Stack is fresh if its mtime > package.json mtime)
```

**Unix/Mac**:
```bash
# Get modification time as timestamp
stat -f %m .shipkit/stack.md 2>/dev/null || echo 0
stat -f %m package.json

# Or with date format
stat -f "%Sm" -t "%Y-%m-%d %H:%M" .shipkit/stack.md
```

**Cross-platform (prefer in Claude Code)**:
```python
# Use Python for reliable cross-platform
import os
from pathlib import Path

stack = Path('.shipkit/stack.md')
pkg = Path('package.json')

if stack.exists() and pkg.exists():
    stack_mtime = os.path.getmtime(stack)
    pkg_mtime = os.path.getmtime(pkg)
    is_fresh = stack_mtime > pkg_mtime
```

---

## Dependency File Detection

### Find Primary Dependency File

```bash
# Check which dependency manager is used
ls package.json 2>/dev/null && echo "npm/yarn/pnpm"
ls pyproject.toml 2>/dev/null && echo "python"
ls go.mod 2>/dev/null && echo "go"
ls Cargo.toml 2>/dev/null && echo "rust"
ls Gemfile 2>/dev/null && echo "ruby"
```

### Extract Dependencies (JavaScript)

```bash
# Get production dependencies
cat package.json | jq -r '.dependencies | keys[]' 2>/dev/null

# Get dev dependencies
cat package.json | jq -r '.devDependencies | keys[]' 2>/dev/null

# Count total
cat package.json | jq '[.dependencies, .devDependencies] | map(keys | length) | add'
```

**Without jq** (use grep):
```bash
# Count dependencies (rough)
grep -c '"[^"]*":' package.json
```

### Extract Dependencies (Python)

```bash
# From pyproject.toml
grep -A 100 '\[project.dependencies\]' pyproject.toml | grep -E '^\s*"' | head -20

# From requirements.txt
cat requirements.txt | grep -v '^#' | grep -v '^$'
```

---

## Schema/Migration Detection

### Supabase Migrations

```bash
# List migrations
ls -la supabase/migrations/*.sql 2>/dev/null

# Count migrations
ls supabase/migrations/*.sql 2>/dev/null | wc -l

# Get latest migration
ls -t supabase/migrations/*.sql 2>/dev/null | head -1

# Extract table names from migrations
grep -h "CREATE TABLE" supabase/migrations/*.sql 2>/dev/null | \
  sed 's/.*CREATE TABLE.*"\([^"]*\)".*/\1/' | sort -u
```

### Prisma Schema

```bash
# Check for Prisma schema
ls prisma/schema.prisma 2>/dev/null

# Extract model names
grep "^model " prisma/schema.prisma 2>/dev/null | awk '{print $2}'

# Count models
grep -c "^model " prisma/schema.prisma 2>/dev/null
```

### Drizzle Schema

```bash
# Find Drizzle schema files
ls -la drizzle/*.sql 2>/dev/null
ls -la src/db/schema/*.ts 2>/dev/null

# Extract table definitions (TypeScript)
grep -h "export const.*Table" src/db/schema/*.ts 2>/dev/null
```

---

## Config File Detection

### Framework Detection

```bash
# Next.js
ls next.config.{js,mjs,ts} 2>/dev/null && echo "Next.js"

# Vite
ls vite.config.{js,ts} 2>/dev/null && echo "Vite"

# Remix
ls remix.config.{js,ts} 2>/dev/null && echo "Remix"

# Nuxt
ls nuxt.config.{js,ts} 2>/dev/null && echo "Nuxt"
```

### Styling Detection

```bash
# Tailwind
ls tailwind.config.{js,ts,cjs,mjs} 2>/dev/null && echo "Tailwind"

# CSS Modules
ls **/*.module.css 2>/dev/null | head -1 && echo "CSS Modules"

# Styled Components (check package.json)
grep -q "styled-components" package.json && echo "Styled Components"
```

---

## Environment Variable Scanning

### Extract from .env.example

```bash
# Get variable names only
grep -E '^[A-Z_]+=' .env.example 2>/dev/null | cut -d= -f1

# Count variables
grep -c -E '^[A-Z_]+=' .env.example 2>/dev/null

# Get with descriptions (comments above)
grep -B1 -E '^[A-Z_]+=' .env.example 2>/dev/null
```

### Detect Required vs Optional

```bash
# Required often have no default
grep -E '^[A-Z_]+=$' .env.example 2>/dev/null

# Optional often have defaults
grep -E '^[A-Z_]+=.+' .env.example 2>/dev/null
```

---

## CLI Detection

### Check for Installed CLIs

**Windows**:
```bash
where supabase 2>nul && echo "supabase: installed"
where stripe 2>nul && echo "stripe: installed"
where vercel 2>nul && echo "vercel: installed"
where gh 2>nul && echo "gh: installed"
```

**Unix/Mac**:
```bash
which supabase 2>/dev/null && echo "supabase: installed"
which stripe 2>/dev/null && echo "stripe: installed"
which vercel 2>/dev/null && echo "vercel: installed"
which gh 2>/dev/null && echo "gh: installed"
```

---

## Performance Notes

| Operation | Typical Time | Token Cost |
|-----------|--------------|------------|
| File existence check | <100ms | ~10 tokens |
| Read small config | <200ms | ~50-200 tokens |
| Glob pattern scan | <500ms | ~20 tokens |
| Migration scan | <1s | ~100-300 tokens |
| Full project scan | 2-5s | ~800-1200 tokens |

**Recommendation**: Always check freshness first. If stack.md is fresh, skip the full scan.
