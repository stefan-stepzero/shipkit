---
name: shipkit-project-context
description: "Use when starting a new project or refreshing tech stack context. Triggers: 'scan project', 'what's my stack', 'refresh context', 'generate stack'."
model: haiku
context: fork
---

# shipkit-project-context - Smart Project Context Scanner

**Purpose**: Generate and maintain lightweight project context files (stack, env, schema) by scanning package files, configs, and migrations. Uses file modification time checks to avoid unnecessary rescans.

**What it does**: Scans project files to detect tech stack, environment requirements, and database schema. Generates `.shipkit/stack.json` as a structured JSON artifact, plus optional markdown files for env and schema.

**Output format**: JSON — readable by Claude, renderable by mission control dashboard, and the single source of truth for project tech stack.

---

## When to Invoke

**User triggers**:
- "Scan the project"
- "Update context"
- "Rescan stack"
- "Generate project context"
- "What's my tech stack?"

**Auto-triggered by**:
- `shipkit-master` (when stack.json is missing or stale)
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
1. If `.shipkit/stack.json` doesn't exist → First run, proceed to Step 2
2. If `stack.json` exists:
   - Compare modification times
   - If `stack.json` newer than `package.json` → **SKIP SCAN**, just read cached file
   - If `package.json` newer than `stack.json` → Ask user to confirm rescan

**Token savings**: Cached read ~100-200 tokens vs Full scan ~1,500 tokens

---

### Step 2: Ask Before Heavy Work

**If rescan is needed, ask user first**:

**First run**: "First run detected - no context files exist. Scan now? (yes/no)"

**Stale context**: "Context appears stale: package.json modified after stack.json. Rescan? (yes/no)"

**If user says no**: "Okay, using existing context. Run `/shipkit-project-context` when you want to update."

---

### Step 3: Scan Project Files

**Index-Accelerated Stack Detection** — Read `.shipkit/codebase-index.json` first:

1. `Read: .shipkit/codebase-index.json`
2. If index exists:
   - `framework` gives the primary framework directly
   - `configFiles` shows all detected config files (database, testing, build tools)
   - `directories` shows project structure
   - `scripts` shows available npm scripts
   - Skip broad framework/config detection — focus Explore agent on **working patterns** the index doesn't capture (provider hierarchy, API route structure, import aliases)
3. If index doesn't exist → full stack detection as below

**USE SUBAGENT FOR COMPREHENSIVE STACK DETECTION** - For first run or full rescan:

```
Task tool with subagent_type: "Explore"
Prompt: "Scan this project to detect complete tech stack.
[If index exists, include: 'The codebase index already detected: framework=[X], config files=[list], directories=[list]. Skip re-detecting these. Focus on: working patterns (provider hierarchy, API route structure, import aliases from tsconfig), auth setup detail, and database schema specifics.']
Report:

1. FRAMEWORK: Check package.json for next, react, vue, svelte, remix, etc.
2. DATABASE: Find Supabase, Prisma, Drizzle, MongoDB in deps + find migration files
3. STYLING: Detect Tailwind, shadcn/ui, Styled Components from deps + config files
4. AUTH: Check for next-auth, clerk, supabase auth, etc.
5. WORKING PATTERNS:
   - Provider hierarchy in layout files
   - API route structure (app router vs pages)
   - Import aliases from tsconfig.json

For each: report name, version (if in package.json), config file location, confidence level."
```

**Why subagent**: Stack detection requires reading package.json, scanning for config files, checking multiple patterns. Explore agent does this efficiently.

**When to use subagent**:
- First run (no context exists)
- Full rescan requested
- Large project with many potential patterns

**When to scan manually**:
- Quick refresh of single stack item
- Targeted check (e.g., "is Prisma configured?")

**Fallback** - Manual scanning:

**Use bash commands (grep, find) to extract information.**

**Detailed commands**: See `references/bash-commands.md` for complete scanning commands

**What to detect**:
- Framework: Next.js, React, Vue, Svelte, Remix (from package.json)
- Database: Supabase, Prisma, Drizzle, MongoDB (from dependencies + migration files)
- Styling: Tailwind, shadcn/ui, Styled Components (from dependencies)
- Environment variables: Parse .env.example
- Database schema: Extract from migrations or schema files
- Metrics: Count dependencies, migrations, env vars
- **Available CLIs**: Check for installed dev CLIs (see CLI Detection below)

### Verification Before Claims

Before claiming any stack item, verify it with tool calls:

| Claim | Required Verification |
|-------|----------------------|
| "Uses Next.js" | `Read: package.json` contains `"next":` with version |
| "Uses Prisma" | `Glob: "**/prisma/schema.prisma"` exists AND readable |
| "Tailwind configured" | `Glob: "tailwind.config.*"` exists |
| "CLI available" | `Bash: "cli-name --version"` succeeds (not just `where/which`) |

**Confidence levels for stack entries:**

| Level | Definition | Evidence Required |
|-------|------------|-------------------|
| HIGH | Verified in package.json AND config file exists | Both checks pass |
| MEDIUM | Verified in package.json only | Dependency present, no config found |
| LOW | Inferred from file patterns only | No package.json entry, just files |

**Report confidence in stack.json output:**

Each stack entry includes a `confidence` field. Example:

```json
{
  "name": "Next.js",
  "version": "14.2.0",
  "purpose": "React framework with SSR/SSG",
  "confidence": "high",
  "evidence": "package.json + next.config.js"
}
```

**Fallback behavior:**
- If verification fails, mark as "unverified" rather than guessing
- If config file missing for a dependency, note it and continue
- If CLI check fails, mark as "not installed" in Available CLIs

**See also:** `shared/references/VERIFICATION-PROTOCOL.md` for standard verification patterns.

---

### Step 3.5: Detect Working Patterns

**Purpose**: Capture how this codebase works so Claude can follow patterns immediately.

**Detection patterns**: See `references/detection-patterns.md` for complete patterns

| Pattern | How to Detect | Fallback |
|---------|---------------|----------|
| Provider nesting | Scan layout.tsx for `<*Provider>` hierarchy | Mark TBD |
| API route structure | Glob routes + read sample | Describe common pattern |
| Component conventions | Analyze structure, naming | Note "varies" |
| Import aliases | Read tsconfig.json paths | Skip if none |

**Why this matters**: Claude has implicit defaults from training. Working Patterns override defaults with project-specific conventions.

**Example output** (included in stack.json `workingPatterns` field):

```json
{
  "workingPatterns": {
    "providerHierarchy": [
      "QueryClientProvider (React Query)",
      "AuthProvider (Supabase auth)",
      "ThemeProvider (next-themes)"
    ],
    "apiPatterns": [
      { "pattern": "Auth", "location": "/api/auth/*", "methods": ["POST"] },
      { "pattern": "CRUD", "location": "/api/[resource]/*", "methods": ["GET", "POST", "PUT", "DELETE"] }
    ],
    "componentConventions": {
      "location": "src/components/",
      "structure": "Feature folders",
      "naming": "PascalCase"
    },
    "importAliases": {
      "@/*": "./src/*"
    }
  }
}
```

**If detection fails**: Mark section as TBD and note that manual input is needed.

---

### Step 4: Generate Context Files

**Use Write tool to create 3 files**.

#### File 1: `.shipkit/stack.json`

**Create file using Write tool**: `.shipkit/stack.json`

The output MUST conform to the JSON schema below. This is a strict contract -- mission control and other skills depend on this structure.

```json
{
  "$schema": "shipkit-artifact",
  "type": "stack",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DD",
  "source": "shipkit-project-context",

  "summary": {
    "framework": "Next.js 14.2",
    "language": "TypeScript 5.3",
    "database": "Supabase (PostgreSQL)",
    "deployment": "Vercel",
    "totalDependencies": 42,
    "totalDevDependencies": 18,
    "envVarsRequired": 5
  },

  "stack": {
    "framework": [
      { "name": "Next.js", "version": "14.2.0", "purpose": "React framework with SSR/SSG", "confidence": "high", "evidence": "package.json + next.config.js" }
    ],
    "language": [
      { "name": "TypeScript", "version": "5.3.3", "purpose": "Type-safe JavaScript", "confidence": "high", "evidence": "package.json + tsconfig.json" }
    ],
    "database": [
      { "name": "Supabase", "version": "2.39.0", "purpose": "PostgreSQL BaaS with auth", "confidence": "high", "evidence": "package.json + supabase/config.toml" }
    ],
    "auth": [
      { "name": "Supabase Auth", "version": null, "purpose": "Authentication via Supabase", "confidence": "medium", "evidence": "package.json only" }
    ],
    "payments": [],
    "styling": [
      { "name": "Tailwind CSS", "version": "3.4.0", "purpose": "Utility-first CSS", "confidence": "high", "evidence": "package.json + tailwind.config.ts" },
      { "name": "shadcn/ui", "version": null, "purpose": "Component library", "confidence": "low", "evidence": "components/ui/ folder exists" }
    ],
    "testing": [
      { "name": "Vitest", "version": "1.2.0", "purpose": "Unit/integration testing", "confidence": "high", "evidence": "package.json + vitest.config.ts" }
    ],
    "other": []
  },

  "dependencies": {
    "next": "14.2.0",
    "@supabase/supabase-js": "2.39.0",
    "react": "18.2.0",
    "react-dom": "18.2.0"
  },

  "devDependencies": {
    "typescript": "5.3.3",
    "tailwindcss": "3.4.0",
    "vitest": "1.2.0",
    "eslint": "8.56.0"
  },

  "envRequirements": [
    { "name": "NEXT_PUBLIC_SUPABASE_URL", "required": true, "description": "Supabase project URL" },
    { "name": "NEXT_PUBLIC_SUPABASE_ANON_KEY", "required": true, "description": "Supabase anonymous key" },
    { "name": "SUPABASE_SERVICE_ROLE_KEY", "required": true, "description": "Supabase service role key (server-only)" }
  ],

  "availableCLIs": [
    { "name": "supabase", "installed": true, "useFor": "db diff, db push, db reset, functions deploy" },
    { "name": "stripe", "installed": false, "useFor": "listen (webhooks), trigger, logs tail" },
    { "name": "vercel", "installed": true, "useFor": "deploy, env pull, dev" },
    { "name": "gh", "installed": true, "useFor": "pr create, issue, api" }
  ],

  "recommendedCLIs": ["stripe"],

  "workingPatterns": {
    "providerHierarchy": [],
    "apiPatterns": [],
    "componentConventions": {
      "location": "",
      "structure": "",
      "naming": ""
    },
    "importAliases": {},
    "projectStructure": {
      "srcDir": true,
      "appRouter": true,
      "apiRoutes": "app/api/"
    }
  }
}
```

**Note**: The example above shows a typical Next.js + Supabase project. Adapt field values to whatever stack is detected. Empty arrays/objects for categories with no detected entries.

### Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `$schema` | string | yes | Always `"shipkit-artifact"` -- identifies this as a Shipkit-managed file |
| `type` | string | yes | Always `"stack"` -- artifact type for routing/rendering |
| `version` | string | yes | Schema version for forward compatibility |
| `lastUpdated` | string | yes | ISO date of last modification |
| `source` | string | yes | Always `"shipkit-project-context"` |
| `summary` | object | yes | Quick-glance fields: framework, language, database, deployment, counts |
| `stack` | object | yes | Categories of detected technologies |
| `stack.<category>[]` | array | yes | Array of stack entries per category |
| `stack.<category>[].name` | string | yes | Technology name |
| `stack.<category>[].version` | string/null | yes | Detected version or null |
| `stack.<category>[].purpose` | string | yes | What it does in this project |
| `stack.<category>[].confidence` | enum | yes | `"high"` \| `"medium"` \| `"low"` |
| `stack.<category>[].evidence` | string | yes | What verification confirmed it |
| `dependencies` | object | yes | Key production packages (name: version) |
| `devDependencies` | object | yes | Key dev packages (name: version) |
| `envRequirements` | array | yes | Required/optional env vars |
| `envRequirements[].name` | string | yes | Variable name |
| `envRequirements[].required` | boolean | yes | Whether required for app to run |
| `envRequirements[].description` | string | yes | What the variable is for |
| `availableCLIs` | array | yes | Detected dev CLIs |
| `availableCLIs[].name` | string | yes | CLI command name |
| `availableCLIs[].installed` | boolean | yes | Whether CLI is available |
| `availableCLIs[].useFor` | string | yes | Common commands |
| `recommendedCLIs` | array | no | CLIs to suggest installing |
| `workingPatterns` | object | yes | Project-specific conventions |

### Summary Object

The `summary` field MUST be kept in sync with the `stack` data. It exists so the dashboard can render overview cards without parsing the full structure. Recompute it every time the file is written.

### Stack Categories

Standard categories: `framework`, `language`, `database`, `auth`, `payments`, `styling`, `testing`, `other`. Add additional categories as needed (e.g., `monitoring`, `email`, `storage`). Empty categories should be present as empty arrays.

#### File 2: `.shipkit/env-requirements.md`

**Template**: See `references/templates.md` for complete env-requirements.md template

Contains: Required Variables, Optional Variables, Setup Instructions

#### File 3: `.shipkit/schema.json`

**Template**: See `references/templates.md` for complete schema.json template

Contains: Tables with Columns/Indexes/Relationships, Relationships Diagram, Migration History (structured JSON format)

---

### Step 5: Confirm Completion

**Output to user**: Summary of created files, framework, database, dependencies count, env vars, tables detected.

---

## Completion Checklist

Copy and track:
- [ ] Scanned package.json and project structure
- [ ] Identified tech stack and dependencies
- [ ] Checked for available CLIs (supabase, stripe, vercel, gh, etc.)
- [ ] Created `.shipkit/stack.json` (includes CLI availability)

---

## Shipkit Artifact Convention

This skill follows the **Shipkit JSON artifact convention** -- a standard structure for all `.shipkit/*.json` files that enables mission control visualization.

**Every JSON artifact MUST include these top-level fields:**

```json
{
  "$schema": "shipkit-artifact",
  "type": "<artifact-type>",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DD",
  "source": "<skill-name>",
  "summary": { ... }
}
```

- `$schema` -- Always `"shipkit-artifact"`. Lets the reporter hook identify files to ship to mission control.
- `type` -- The artifact type (`"stack"`, `"goals"`, `"spec"`, `"plan"`, etc.). Dashboard uses this for rendering.
- `version` -- Schema version. Bump when fields change.
- `lastUpdated` -- When this file was last written.
- `source` -- Which skill wrote this file.
- `summary` -- Aggregated data for dashboard cards. Structure varies by type.

Skills that haven't migrated to JSON yet continue writing markdown. The reporter hook ships both: JSON artifacts get structured dashboard rendering, markdown files fall back to metadata-only (exists, date, size).

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

**When to skip rescan**: stack.json modification time > package.json modification time

**When to suggest rescan**: package.json modification time > stack.json modification time

**When to auto-scan**: .shipkit/stack.json doesn't exist (first run)

---

## When This Skill Integrates with Others

### Before This Skill
- None - This is often the FIRST skill run in a new project

### After This Skill
- `/shipkit-project-status` - Uses context to suggest next steps
- `/shipkit-spec` - References stack.json for technical constraints
- `/shipkit-plan` - References stack.json for tech choices
- `implement (no skill needed)` - References stack.json and schema.json while coding

### Triggered By
- `/shipkit-master` - When stack.json missing or stale
- `/shipkit-project-status` - When detecting staleness

---

## Context Files This Skill Reads

**To check freshness**:
- `.shipkit/stack.json` (check if exists and modification time)
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
- `.shipkit/stack.json` (structured JSON artifact)
- `.shipkit/env-requirements.md`
- `.shipkit/schema.json`

**Updates** (rescan): Same 3 files (overwrites with fresh data)

**Archive location** (if replacing):
- `.shipkit/.archive/stack.YYYY-MM-DD.json`

**Never modifies**: Source files (package.json, migrations, etc.) - read-only

---

## Lazy Loading Behavior

**This skill uses smart caching**:

1. User invokes `/shipkit-project-context`
2. Check if `.shipkit/stack.json` exists
3. **Fast path** (stack.json is fresh): Read 3 files, Total: ~180 tokens
4. **Slow path** (first run or stale): Full scan, Total: ~1,400 tokens

**Token savings over sessions**: First run: 1,400 tokens, Subsequent runs (fresh): 180 tokens (87% reduction)

---

## Detection Patterns

**See `references/detection-patterns.md` for complete patterns:**
- What's auto-detectable vs needs human input
- Framework detection (Next.js, React, Vue, Svelte, Remix)
- Database detection (Supabase, Prisma, Drizzle, MongoDB)
- Styling detection (Tailwind, shadcn/ui, Styled Components, CSS Modules)
- Working Patterns detection (provider hierarchy, API patterns, component conventions)
- Special cases (monorepos, no database, no .env.example)

---

## CLI Detection

**Purpose**: Detect installed dev CLIs so Claude knows to use them for speed.

### Check Commands

| CLI | Windows | Unix/Mac | When to Check |
|-----|---------|----------|---------------|
| `supabase` | `where supabase` | `which supabase` | Supabase in deps |
| `stripe` | `where stripe` | `which stripe` | Stripe/payments in deps |
| `vercel` | `where vercel` | `which vercel` | Next.js or Vercel detected |
| `gh` | `where gh` | `which gh` | Always (GitHub is universal) |
| `railway` | `where railway` | `which railway` | Railway config detected |
| `wrangler` | `where wrangler` | `which wrangler` | Cloudflare/R2 in deps |
| `prisma` | `npx prisma -v` | `npx prisma -v` | Prisma in deps |
| `docker` | `where docker` | `which docker` | Dockerfile exists |

### Recommendation Logic

Based on detected services, suggest missing CLIs:

| Detected Service | Missing CLI | Suggest |
|-----------------|-------------|---------|
| `@supabase/supabase-js` | supabase | `npm i -g supabase` |
| `stripe` or `@stripe/stripe-js` | stripe | `npm i -g stripe` (or brew) |
| Next.js + no vercel | vercel | `npm i -g vercel` |
| Cloudflare R2/Workers | wrangler | `npm i -g wrangler` |

### Why CLIs Matter

Claude already knows these CLI commands from training. The value is **awareness**:
- ✅ Installed → Claude uses CLI for speed (e.g., `supabase db diff` vs writing migration manually)
- ❌ Missing → Claude suggests installation, uses SDK fallback

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
- [ ] `.shipkit/stack.json` exists with framework, database, styling, dependencies
- [ ] `.shipkit/stack.json` conforms to JSON schema (includes $schema, type, version, lastUpdated, source, summary)
- [ ] `.shipkit/stack.json` includes availableCLIs array
- [ ] `.shipkit/env-requirements.md` exists with all env vars from .env.example
- [ ] `.shipkit/schema.json` exists with tables, columns, relationships (if migrations found)
- [ ] Modification times are current (fresher than source files)
- [ ] User can see summary of what was detected (including CLI availability)
<!-- /SECTION:success-criteria -->
---

**Remember**: This skill is about **smart context generation with aggressive caching**. Scan once, read many times. Only rescan when source files actually change.