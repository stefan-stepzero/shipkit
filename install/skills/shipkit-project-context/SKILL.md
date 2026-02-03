---
name: shipkit-project-context
description: "Use when starting a new project or refreshing tech stack context. Triggers: 'scan project', 'what's my stack', 'refresh context', 'generate stack'."
---

# shipkit-project-context - Smart Project Context Scanner

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
- `shipkit-master` (when stack.md is missing or stale)
- `shipkit-project-status` (when it detects staleness)

**First run**:
- No `.shipkit/` directory exists
- User starts new Shipkit project

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
1. If `.shipkit/stack.md` doesn't exist → First run, proceed to Step 2
2. If `stack.md` exists:
   - Compare modification times
   - If `stack.md` newer than `package.json` → **SKIP SCAN**, just read cached file
   - If `package.json` newer than `stack.md` → Ask user to confirm rescan

**Token savings**: Cached read ~100-200 tokens vs Full scan ~1,500 tokens

---

### Step 2: Ask Before Heavy Work

**If rescan is needed, ask user first**:

**First run**: "First run detected - no context files exist. Scan now? (yes/no)"

**Stale context**: "Context appears stale: package.json modified after stack.md. Rescan? (yes/no)"

**If user says no**: "Okay, using existing context. Run `/shipkit-project-context` when you want to update."

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

#### File 1: `.shipkit/stack.md`

**Template**: See `references/templates.md` for complete stack.md template

Contains: Framework, Database, Styling, Key Dependencies, Project Structure, Total Dependencies

#### File 2: `.shipkit/env-requirements.md`

**Template**: See `references/templates.md` for complete env-requirements.md template

Contains: Required Variables, Optional Variables, Setup Instructions

#### File 3: `.shipkit/schema.md`

**Template**: See `references/templates.md` for complete schema.md template

Contains: Tables with Columns/Indexes/Relationships, Relationships Diagram, Migration History

---

### Step 5: Confirm Completion

**Output to user**: Summary of created files, framework, database, dependencies count, env vars, tables detected.

---

## Completion Checklist

Copy and track:
- [ ] Scanned package.json and project structure
- [ ] Identified tech stack and dependencies
- [ ] Created `.shipkit/stack.md`

---

## What Makes This "Lite"

**Included**:
- Smart caching via file modification time checks
- Auto-detection of framework, database, styling
- Environment variable scanning
- Basic schema extraction from migrations
- Dependency counting

**Not included** (vs full project-context):
- Deep dependency analysis (vulnerability scanning)
- Architecture diagram generation
- API endpoint discovery
- Component tree mapping
- Test coverage analysis

**Philosophy**: Just enough context to understand the stack and start building.

---

## Freshness Check Logic

**When to skip rescan**: stack.md modification time > package.json modification time

**When to suggest rescan**: package.json modification time > stack.md modification time

**When to auto-scan**: .shipkit/stack.md doesn't exist (first run)

---

## When This Skill Integrates with Others

### Before This Skill
- None - This is often the FIRST skill run in a new project

### After This Skill
- `/shipkit-project-status` - Uses context to suggest next steps
- `/shipkit-spec` - References stack.md for technical constraints
- `/shipkit-plan` - References stack.md for tech choices
- `implement (no skill needed)` - References stack.md and schema.md while coding

### Triggered By
- `/shipkit-master` - When stack.md missing or stale
- `/shipkit-project-status` - When detecting staleness

---

## Context Files This Skill Reads

**To check freshness**:
- `.shipkit/stack.md` (check if exists and modification time)
- `package.json` (modification time)
- `package-lock.json` or `pnpm-lock.yaml` or `yarn.lock` (modification time)

**To generate context**:
- `package.json` (dependencies, scripts)
- `.env.example` (environment variables)
- `supabase/migrations/*.sql` or `prisma/schema.prisma` or `drizzle/*.sql` (schema)

---

## Context Files This Skill Writes

**Write Strategy: OVERWRITE AND REPLACE**

All context files are **completely replaced** on each scan. No history is preserved because context files are snapshots of current state, not historical records.

**Creates** (first run):
- `.shipkit/stack.md`
- `.shipkit/env-requirements.md`
- `.shipkit/schema.md`

**Updates** (rescan): Same 3 files (overwrites with fresh data)

**Never modifies**: Source files (package.json, migrations, etc.) - read-only

---

## Lazy Loading Behavior

**This skill uses smart caching**:

1. User invokes `/shipkit-project-context`
2. Check if `.shipkit/stack.md` exists
3. **Fast path** (stack.md is fresh): Read 3 files, Total: ~180 tokens
4. **Slow path** (first run or stale): Full scan, Total: ~1,400 tokens

**Token savings over sessions**: First run: 1,400 tokens, Subsequent runs (fresh): 180 tokens (87% reduction)

---

## Detection Patterns

**See `references/detection-patterns.md` for complete patterns:**
- Framework detection (Next.js, React, Vue, Svelte, Remix)
- Database detection (Supabase, Prisma, Drizzle, MongoDB)
- Styling detection (Tailwind, shadcn/ui, Styled Components, CSS Modules)
- Special cases (monorepos, no database, no .env.example)

---

<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Has important context been saved to `.shipkit/`?
2. **Prerequisites** - Does the next action need a spec or plan first?
3. **Session length** - Long session? Consider `/shipkit-work-memory` for continuity.

**Natural capabilities** (no skill needed): Implementation, debugging, testing, refactoring, code documentation.

**Suggest skill when:** User needs to make decisions, create persistence, or check project status.
<!-- /SECTION:after-completion -->

<!-- SECTION:success-criteria -->
## Success Criteria

Context generation is complete when:
- [ ] `.shipkit/stack.md` exists with framework, database, styling, dependencies
- [ ] `.shipkit/env-requirements.md` exists with all env vars from .env.example
- [ ] `.shipkit/schema.md` exists with tables, columns, relationships (if migrations found)
- [ ] Modification times are current (fresher than source files)
- [ ] User can see summary of what was detected
<!-- /SECTION:success-criteria -->
---

**Remember**: This skill is about **smart context generation with aggressive caching**. Scan once, read many times. Only rescan when source files actually change.

<!-- Shipkit v1.1.0 -->
