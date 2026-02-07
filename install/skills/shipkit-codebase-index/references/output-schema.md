# Codebase Index Schema Reference

This document defines the JSON schema for `.shipkit/codebase-index.json`.

## JSON Schema

```json
{
  "generated": "YYYY-MM-DD",

  "scripts": {
    "<script-name>": "<script-command>"
  },

  "recentlyActive": [
    "path/to/file.ts"
  ],

  "directories": [
    "src/app",
    "src/components"
  ],

  "configFiles": [
    "next.config.js",
    "tsconfig.json"
  ],

  "framework": "string (e.g., 'next.js (app router)')",

  "entryPoints": {
    "app": "path/to/main/entry.tsx",
    "layout": "path/to/layout.tsx",
    "api": "path/to/api/directory/",
    "database": "path/to/schema.prisma"
  },

  "concepts": {
    "<concept-name>": ["path/to/file1.ts", "path/to/file2.ts"]
  },

  "coreFiles": [
    "path/to/highly-imported-file.ts"
  ],

  "skip": [
    "path/to/legacy/folder/"
  ]
}
```

## Field Reference

### Metadata Fields

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| `generated` | string | script | ISO date when index was generated |

### Script-Generated Fields (100% reliable)

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| `scripts` | object | script | npm/yarn scripts from package.json |
| `recentlyActive` | string[] | script | Files modified in last 14 days (from git) |
| `directories` | string[] | script | Common directories that exist |
| `configFiles` | string[] | script | Configuration files that exist |

### Claude-Completed Fields (require judgment)

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| `framework` | string | claude | Detected framework (e.g., `"next.js (app router)"`, `"vite"`) |
| `entryPoints` | object | claude | Key entry files for navigation |
| `concepts` | object | claude | Concept-to-files mapping for quick lookup |
| `coreFiles` | string[] | claude | Files imported by 5+ other files (high fan-in) |
| `skip` | string[] | claude | Folders Claude should avoid reading |

### Entry Points Object

| Key | Description |
|-----|-------------|
| `app` | Main application entry point |
| `layout` | Root layout or wrapper component |
| `api` | API routes directory |
| `database` | Database schema file |
| (custom) | Project-specific entry points |

### Concepts Object

Maps abstract concepts to concrete file paths for quick lookup.

| Concept | Description | Example Files |
|---------|-------------|---------------|
| `auth` | Authentication, sessions, login | `["src/lib/auth.ts", "src/middleware.ts"]` |
| `database` | DB connections, models, schema | `["src/lib/db.ts", "prisma/schema.prisma"]` |
| `payments` | Billing, subscriptions, checkout | `["src/lib/stripe.ts", "src/api/webhook.ts"]` |
| `api` | API route handlers | `["src/app/api/"]` |
| `components` | Reusable UI components | `["src/components/"]` |

## How Claude Uses the Index

| Field | Question | How It Helps |
|-------|----------|--------------|
| `concepts` | "Where is auth?" | Direct lookup to file list |
| `entryPoints` | "Where do I start?" | Go-to files for exploration |
| `recentlyActive` | "What's being worked on?" | Focus on recent changes |
| `coreFiles` | "What's important?" | High-dependency files |
| `skip` | "Should I read this?" | Avoid wasted context |
| `configFiles` | "What tools are used?" | Stack understanding |

## Division of Labor

| Task | Script | Claude |
|------|--------|--------|
| Parse package.json scripts | Yes | |
| Get recently active files (git) | Yes | |
| List existing directories | Yes | |
| List existing config files | Yes | |
| Detect framework | | Yes |
| Identify entry points | | Yes |
| Map concepts to files | | Yes |
| Identify core files | | Yes |
| Determine skip list | | Yes |

**Principle**: Script does 100% reliable mechanical tasks. Claude does anything requiring judgment.
