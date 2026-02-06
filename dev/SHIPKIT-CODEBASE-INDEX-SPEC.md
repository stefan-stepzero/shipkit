# shipkit-codebase-index Spec

Generate a project index so Claude navigates without wasteful exploration.

---

## Usage Strategy

### Two Distinct Operations

| Operation | What | When | How Often |
|-----------|------|------|-----------|
| **Generate** | Run `/codebase-index` skill | User explicitly invokes | Rare (initial setup, major changes) |
| **Read** | Claude reads the JSON file | Before exploring codebase | When Claude needs to find something |

**Critical distinction:** The skill generates the index. Reading the index is just reading a file — not a skill invocation.

### When to Generate (Rare)

User runs `/codebase-index` when:
- First time using Shipkit on a project
- Major codebase restructuring
- Index is stale (>14 days old)
- New concepts added to project

**This is NOT automatic.** User decides when to regenerate.

### When Claude Reads (Navigation Only)

Claude reads the index file when:
- User asks "where is X?"
- Claude needs to find files for a feature
- Starting work on an unfamiliar part of codebase

Claude does NOT read the index when:
- Already knows which file to edit
- Working on a file already open
- Running tests or builds
- Making edits to known files

**The index is a navigation aid, not a per-action requirement.**

---

## Enforcement Strategy

How do we ensure Claude actually uses the index instead of wasteful exploration?

### Option A: CLAUDE.md Instruction (Primary)

Add to the project's installed CLAUDE.md:

```markdown
## Codebase Navigation

If `.shipkit/codebase-index.json` exists:
1. Read it FIRST before globbing or exploring files
2. Use `concepts` to find feature-related files
3. Use `entryPoints` to find starting points
4. Check `skip` to avoid wasting context on irrelevant files
5. Don't glob or explore if the index answers the question
```

**Why this works:** Claude follows CLAUDE.md instructions. This makes index-first navigation the default behavior.

### Option B: Session Start Hook (Context Injection)

Add to session start hook (`shipkit-session-start.py`):

```python
import os
import json
from datetime import datetime

index_path = '.shipkit/codebase-index.json'

if not os.path.exists(index_path):
    print("📁 Tip: Run /codebase-index to create a project map for faster navigation")
else:
    with open(index_path) as f:
        data = json.load(f)

    generated = datetime.strptime(data['generated'], '%Y-%m-%d')
    age = (datetime.now() - generated).days

    # Print useful summary - inject navigation info into context
    print("📁 Codebase Index Summary")
    print("=" * 40)

    if age > 14:
        print(f"⚠️  Index is {age} days old. Consider running /codebase-index to update.")

    # Concepts - the key navigation info
    concepts = data.get('concepts', {})
    if concepts:
        print(f"\nConcepts ({len(concepts)}):")
        for concept, files in concepts.items():
            # Show concept and first file, truncate if many files
            first_file = files[0] if files else "?"
            more = f" (+{len(files)-1} more)" if len(files) > 1 else ""
            print(f"  • {concept}: {first_file}{more}")

    # Entry points
    entry_points = data.get('entryPoints', {})
    if entry_points:
        print(f"\nEntry Points:")
        for name, path in entry_points.items():
            print(f"  • {name}: {path}")

    # Skip list
    skip = data.get('skip', [])
    if skip:
        print(f"\nSkip: {', '.join(skip)}")

    print("=" * 40)
    print("Use concepts above for navigation. Read full index for file lists.")
```

**Why this works:** Injects the actual navigation info into Claude's context at session start. Claude doesn't need to read the index file for basic navigation — it's already visible.

**Trade-off:** Uses some context tokens, but saves multiple tool calls when Claude needs to navigate.

### Combined Effect

```
Session starts:
  Hook prints:
    📁 Codebase Index Summary
    ========================================
    Concepts (5):
      • auth: src/lib/auth.ts (+2 more)
      • database: src/lib/db.ts (+1 more)
      • payments: src/lib/stripe.ts (+1 more)
      • email: src/lib/email.ts
      • users: src/app/api/users/ (+1 more)

    Entry Points:
      • app: src/app/page.tsx
      • layout: src/app/layout.tsx
      • api: src/app/api/
      • database: prisma/schema.prisma

    Skip: src/legacy/, src/components/deprecated/
    ========================================
    Use concepts above for navigation. Read full index for file lists.

User: "Where is payment logic?"
  Claude sees from hook output: payments → src/lib/stripe.ts
  Goes directly to file. No index read needed.

User: "I need all the payment-related files"
  Claude reads full index for complete file list
  Gets: ["src/lib/stripe.ts", "src/app/api/webhooks/stripe/"]

User: "Add error handling to that function"
  Claude already knows file
  Edits directly. No navigation needed.
```

### What This Does NOT Do

- ❌ Does not run the skill on every edit
- ❌ Does not automatically regenerate the index
- ❌ Does not block Claude if index is missing
- ❌ Does not require index for every action

The index is **optional but beneficial**. Projects work without it; they just have more wasted exploration.

---

## The Actual Problem

**Without index:**
```
User: "Where is auth handled?"
Claude: [Glob **/*.ts] → 200 files listed
Claude: [Read src/utils/helpers.ts] → Not relevant (wasted context)
Claude: [Read src/components/Button.tsx] → Not relevant (wasted context)
Claude: [Read src/lib/auth.ts] → Found it!
= 4 tool calls, 2 files of wasted context
```

**With index:**
```
User: "Where is auth handled?"
Claude: [Read codebase-index.json] → concepts.auth: ["src/lib/auth.ts", ...]
Claude: [Read src/lib/auth.ts] → Got it
= 2 tool calls, 0 wasted context
```

**Goal:** Claude reads ONE file (the index) and knows where to go.

---

## What Claude Actually Needs

| Need | Why |
|------|-----|
| **Concept → files mapping** | "Where is auth?" → immediate answer |
| **Entry points** | Where to start for each concern |
| **Recently active files** | Likely relevant to current work |
| **Directories explained** | What's in each folder |
| **Files to skip** | Don't waste context on these |
| **Scripts** | What commands are available |

**What Claude does NOT need:**
- Full dependency graphs (overkill)
- Export lists (can see when reading file)
- Line counts (not useful for navigation)
- Complex heat calculations (simple recency is enough)

---

## Output: `.shipkit/codebase-index.json`

```json
{
  "generated": "2025-01-27",
  "framework": "next.js (app router)",

  "scripts": {
    "dev": "Start dev server",
    "build": "Production build",
    "test": "Run vitest tests",
    "lint": "ESLint check"
  },

  "entryPoints": {
    "app": "src/app/page.tsx",
    "layout": "src/app/layout.tsx",
    "api": "src/app/api/",
    "database": "prisma/schema.prisma",
    "auth": "src/lib/auth.ts"
  },

  "concepts": {
    "auth": ["src/lib/auth.ts", "src/app/api/auth/", "src/middleware.ts"],
    "database": ["src/lib/db.ts", "prisma/schema.prisma"],
    "payments": ["src/lib/stripe.ts", "src/app/api/webhooks/stripe/"],
    "email": ["src/lib/email.ts"],
    "users": ["src/app/api/users/", "src/services/users.ts"]
  },

  "directories": {
    "src/app": "Next.js routes and pages",
    "src/app/api": "API endpoints",
    "src/components": "React components",
    "src/lib": "Core utilities and config",
    "src/services": "Business logic"
  },

  "recentlyActive": [
    "src/app/api/payments/route.ts",
    "src/components/Checkout.tsx",
    "src/lib/stripe.ts"
  ],

  "coreFiles": [
    "src/lib/db.ts",
    "src/lib/auth.ts",
    "src/app/layout.tsx"
  ],

  "skip": [
    "src/legacy/",
    "src/components/deprecated/"
  ]
}
```

**How Claude uses each section:**

| Section | Claude's Question | How Index Helps |
|---------|------------------|-----------------|
| `concepts` | "Where is auth?" | Direct lookup → file list |
| `entryPoints` | "Where do I start?" | Go-to files for each concern |
| `directories` | "What's in src/lib?" | Purpose without exploring |
| `recentlyActive` | "What's being worked on?" | Focus on relevant files |
| `coreFiles` | "What's important?" | Key files, many dependents |
| `skip` | "Should I read this?" | Avoid wasting context |
| `scripts` | "How do I run tests?" | Available commands |

---

## Python Script

### What Script Does vs What Claude Does

| Task | Script | Claude |
|------|--------|--------|
| Detect framework | ✅ | |
| Parse package.json scripts | ✅ | |
| Find recently modified files (git) | ✅ | |
| Detect core files (most imported) | ✅ | |
| Build concepts mapping | | ✅ (requires understanding) |
| Generate JSON | ✅ | |
| Invoke script | | ✅ |
| Read and use index | | ✅ |

**Key insight:** The script does mechanical analysis. Claude adds semantic understanding (what concepts exist).

### Script: `generate_index.py`

```python
#!/usr/bin/env python3
"""
Generate codebase index for Claude Code.
Outputs to .shipkit/codebase-index.json
"""

import json
import os
import subprocess
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

OUTPUT_PATH = '.shipkit/codebase-index.json'
SOURCE_EXTENSIONS = {'.ts', '.tsx', '.js', '.jsx', '.py'}
EXCLUDE_DIRS = {'node_modules', 'dist', '.next', '__pycache__', '.git', 'venv'}


def run_git(args):
    """Run git command and return output."""
    try:
        result = subprocess.run(['git'] + args, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError:
        return ''


def detect_framework(root):
    """Detect project framework."""
    root = Path(root)

    if (root / 'next.config.js').exists() or (root / 'next.config.mjs').exists():
        if (root / 'src/app').exists() or (root / 'app').exists():
            return 'next.js (app router)'
        return 'next.js (pages router)'
    if (root / 'vite.config.ts').exists():
        return 'vite'
    if (root / 'pyproject.toml').exists():
        return 'python'
    return 'unknown'


def parse_scripts(root):
    """Parse scripts from package.json with descriptions."""
    pkg_path = Path(root) / 'package.json'
    if not pkg_path.exists():
        return {}

    try:
        data = json.loads(pkg_path.read_text())
        scripts = data.get('scripts', {})

        # Add simple descriptions
        descriptions = {
            'dev': 'Start dev server',
            'build': 'Production build',
            'start': 'Start production server',
            'test': 'Run tests',
            'lint': 'Lint check',
            'typecheck': 'Type check',
        }

        return {k: descriptions.get(k, v) for k, v in scripts.items()}
    except:
        return {}


def get_recently_active(root, days=14, limit=10):
    """Get recently modified files from git."""
    since = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    output = run_git(['log', f'--since={since}', '--name-only', '--pretty=format:'])

    counts = defaultdict(int)
    for line in output.strip().split('\n'):
        line = line.strip()
        if line and not line.startswith(' ') and Path(root, line).exists():
            # Only include source files
            if Path(line).suffix in SOURCE_EXTENSIONS:
                counts[line] += 1

    # Return top N by modification count
    sorted_files = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return [f for f, _ in sorted_files[:limit]]


def find_core_files(root, limit=5):
    """Find files that are imported most often (heuristic for core files)."""
    import_counts = defaultdict(int)

    for path in Path(root).rglob('*'):
        if path.suffix not in SOURCE_EXTENSIONS:
            continue
        if any(excl in path.parts for excl in EXCLUDE_DIRS):
            continue

        try:
            content = path.read_text(encoding='utf-8', errors='ignore')
            # Simple import detection
            for line in content.split('\n'):
                if 'from' in line and ('import' in line or 'require' in line):
                    # Extract path
                    if '@/' in line:
                        # Alias import like @/lib/db
                        parts = line.split('@/')
                        if len(parts) > 1:
                            imported = 'src/' + parts[1].split("'")[0].split('"')[0]
                            import_counts[imported] += 1
        except:
            pass

    # Return top N
    sorted_files = sorted(import_counts.items(), key=lambda x: x[1], reverse=True)
    return [f for f, _ in sorted_files[:limit]]


def scan_directories(root):
    """Scan top-level directories and guess their purpose."""
    dir_purposes = {
        'src/app': 'Next.js routes and pages',
        'src/pages': 'Next.js pages',
        'src/components': 'React components',
        'src/lib': 'Core utilities and config',
        'src/utils': 'Utility functions',
        'src/services': 'Business logic',
        'src/hooks': 'React hooks',
        'src/types': 'TypeScript types',
        'src/api': 'API utilities',
        'app': 'Next.js App Router',
        'pages': 'Next.js Pages Router',
        'components': 'React components',
        'lib': 'Utilities',
        'prisma': 'Database schema',
        'public': 'Static assets',
    }

    result = {}
    for dir_path, purpose in dir_purposes.items():
        if (Path(root) / dir_path).exists():
            result[dir_path] = purpose

    return result


def detect_entry_points(root):
    """Detect common entry points."""
    entries = {}
    root = Path(root)

    # Next.js App Router
    for candidate in ['src/app/page.tsx', 'app/page.tsx']:
        if (root / candidate).exists():
            entries['app'] = candidate
            break

    for candidate in ['src/app/layout.tsx', 'app/layout.tsx']:
        if (root / candidate).exists():
            entries['layout'] = candidate
            break

    # API
    for candidate in ['src/app/api/', 'app/api/', 'src/pages/api/', 'pages/api/']:
        if (root / candidate).exists():
            entries['api'] = candidate
            break

    # Database
    if (root / 'prisma/schema.prisma').exists():
        entries['database'] = 'prisma/schema.prisma'

    # Common lib files
    for name in ['auth', 'db', 'config']:
        for candidate in [f'src/lib/{name}.ts', f'lib/{name}.ts']:
            if (root / candidate).exists():
                entries[name] = candidate
                break

    return entries


def generate_index():
    """Generate the codebase index."""
    root = run_git(['rev-parse', '--show-toplevel']).strip()
    if not root:
        print("Error: Not a git repository")
        return

    os.chdir(root)

    print("Generating codebase index...")

    index = {
        'generated': datetime.now().strftime('%Y-%m-%d'),
        'framework': detect_framework(root),
        'scripts': parse_scripts(root),
        'entryPoints': detect_entry_points(root),
        'concepts': {},  # Claude fills this in
        'directories': scan_directories(root),
        'recentlyActive': get_recently_active(root),
        'coreFiles': find_core_files(root),
        'skip': []  # User/Claude adds these
    }

    # Write output
    output_dir = Path(OUTPUT_PATH).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, 'w') as f:
        json.dump(index, f, indent=2)

    print(f"✅ Index created at {OUTPUT_PATH}")
    print(f"   Framework: {index['framework']}")
    print(f"   Entry points: {len(index['entryPoints'])}")
    print(f"   Recently active: {len(index['recentlyActive'])} files")
    print(f"   Core files: {len(index['coreFiles'])} files")
    print(f"\n💡 Run /codebase-index to have Claude add concept mappings")


if __name__ == '__main__':
    generate_index()
```

---

## User Flow

### Flow 1: Generate Index

```
User: /codebase-index

Claude: "I'll generate a codebase index.

Running the index generator script...
[Runs python generate_index.py]

✅ Base index created. Now I'll add concept mappings.

Scanning for common concepts...

I found these concepts in your codebase:
- **auth**: src/lib/auth.ts, src/middleware.ts, src/app/api/auth/
- **database**: src/lib/db.ts, prisma/schema.prisma
- **payments**: src/lib/stripe.ts, src/app/api/webhooks/stripe/

Are there other concepts I should add? Or any files to skip?"

User: "Add 'email' and skip the legacy folder"

Claude: [Updates index]
"Done. Index saved to .shipkit/codebase-index.json

I'll now use this to navigate your codebase faster."
```

### Flow 2: Claude Uses Index

```
User: "Where is the payment logic?"

Claude: [Reads codebase-index.json]
[Finds concepts.payments: ["src/lib/stripe.ts", "src/app/api/webhooks/stripe/"]]

"Payment logic is in:
- **src/lib/stripe.ts** — Stripe utilities
- **src/app/api/webhooks/stripe/** — Webhook handlers

Want me to open either of these?"
```

### Flow 3: What's Active?

```
User: "What are we working on?"

Claude: [Reads index.recentlyActive]

"Based on recent git activity:
1. src/app/api/payments/route.ts (8 commits this week)
2. src/components/Checkout.tsx (5 commits)
3. src/lib/stripe.ts (4 commits)

Looks like payments/checkout is the focus."
```

---

## SKILL.md

```markdown
---
name: shipkit-codebase-index
description: Generate project index for faster navigation
---

# Codebase Index

Generate an index so I can navigate your codebase without wasteful exploration.

## Activation

- `/codebase-index` — Generate or update index
- Auto-suggested if index doesn't exist

## What It Does

1. Runs `scripts/generate_index.py` for mechanical analysis
2. I add concept mappings (auth, database, payments, etc.)
3. Saves to `.shipkit/codebase-index.json`
4. I read this before exploring files

## What's in the Index

- **scripts**: Available npm commands
- **entryPoints**: Where to start (app, layout, api, db)
- **concepts**: Feature → files mapping (auth, payments, etc.)
- **directories**: What each folder contains
- **recentlyActive**: Files with recent git activity
- **coreFiles**: Important files (many imports)
- **skip**: Files/folders to ignore

## How It Helps

Without index: I glob → read wrong files → waste context
With index: I read index → go directly to right file

## Updating

Run `/codebase-index` anytime to regenerate.
I'll re-run the script and update concept mappings.
```

---

## Integration

This section describes what gets installed. The enforcement strategy (Option A + B) is defined in the "Enforcement Strategy" section above.

### What Gets Installed

| File | Change | Purpose |
|------|--------|---------|
| `install/claude-md/shipkit.md` | Add "Codebase Navigation" section | Option A: Instruction enforcement |
| `install/shared/hooks/shipkit-session-start.py` | Add index availability check | Option B: Session reminder |
| `install/skills/shipkit-codebase-index/` | New skill directory | The `/codebase-index` command |
| `install/skills/shipkit-codebase-index/scripts/generate_index.py` | Python script | Mechanical analysis |

### Files Created in User Projects

When user runs `/codebase-index`:

| File | Content |
|------|---------|
| `.shipkit/codebase-index.json` | The index Claude reads for navigation |

No other project files are modified. The index is self-contained.

### Relationship to Other Skills

| Skill | How It Interacts |
|-------|------------------|
| `shipkit-project-context` | Could load index as part of context loading |
| `shipkit-project-status` | Could report index age/staleness |
| `shipkit-detect` | Could suggest running /codebase-index if missing |

---

## Summary

| Component | What It Does |
|-----------|--------------|
| **Python script** | Git analysis, framework detection, find active/core files |
| **Claude** | Add concept mappings, answer questions using index |
| **JSON output** | Simple lookup table Claude reads before exploring |

**The index is for Claude, not humans.** No markdown needed.
