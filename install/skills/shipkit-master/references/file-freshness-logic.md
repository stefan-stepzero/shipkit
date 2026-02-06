# File Freshness Logic

**Purpose**: Define how to determine if context files are "stale" and need updating

---

## Freshness Thresholds

| File | Stale If | Compare Against | Rationale |
|------|----------|-----------------|-----------|
| `.shipkit/stack.json` | > 7 days old OR older than `package.json` | `package.json` mtime | Stack should reflect current dependencies |
| `.shipkit/architecture.md` | > 14 days old OR major structural changes | `src/` directory mtime | Architecture evolves slower than code |
| `.shipkit/why.md` | > 30 days old | None (absolute) | Vision rarely changes |
| `.shipkit/specs/*.md` | > 7 days AND feature not shipped | Git history | Specs shouldn't linger unimplemented |
| `.shipkit/plans/*.md` | > 3 days AND plan not started | None (absolute) | Plans should be executed promptly |

---

## Freshness Check Algorithm

```python
def is_file_stale(file_path: str) -> tuple[bool, str]:
    """
    Returns (is_stale: bool, reason: str)
    """
    import os
    from datetime import datetime, timedelta

    if not os.path.exists(file_path):
        return False, "File doesn't exist"

    file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
    age_days = (datetime.now() - file_mtime).days

    # Determine threshold based on file type
    if "stack.json" in file_path:
        threshold_days = 7
        compare_file = "package.json"
    elif "architecture.md" in file_path:
        threshold_days = 14
        compare_file = None
    elif "why.md" in file_path:
        threshold_days = 30
        compare_file = None
    elif "/specs/" in file_path:
        threshold_days = 7
        compare_file = None
    elif "/plans/" in file_path:
        threshold_days = 3
        compare_file = None
    else:
        threshold_days = 7
        compare_file = None

    # Check absolute age
    if age_days > threshold_days:
        return True, f"Last modified {age_days} days ago (threshold: {threshold_days})"

    # Check relative freshness (if compare file specified)
    if compare_file and os.path.exists(compare_file):
        compare_mtime = datetime.fromtimestamp(os.path.getmtime(compare_file))
        if compare_mtime > file_mtime:
            return True, f"Older than {compare_file}"

    return False, "Fresh"
```

---

## Freshness Indicators in Session Start

When displaying session status, use these indicators:

| Status | Symbol | Message |
|--------|--------|---------|
| Fresh (< 50% of threshold) | ✓ | "stack.json (2 days)" |
| Aging (50-100% of threshold) | ⚠ | "stack.json (5 days - consider updating)" |
| Stale (> threshold) | ✗ | "stack.json (12 days - STALE)" |
| Missing | ○ | "stack.json (not found)" |

---

## Comparison Logic for stack.json

`stack.json` has special comparison logic because it documents the tech stack:

```
stack.json is STALE if ANY of:
1. Modified > 7 days ago
2. package.json modified more recently (dependencies changed)
3. New config files detected that aren't documented:
   - tsconfig.json exists but TypeScript not in stack.json
   - tailwind.config.js exists but Tailwind not in stack.json
   - prisma/schema.prisma exists but Prisma not in stack.json
```

---

## Bash Commands for Freshness Check

**Get file age in days**:
```bash
# Unix/Mac
file_age_days=$(( ($(date +%s) - $(stat -f %m "$file")) / 86400 ))

# Linux
file_age_days=$(( ($(date +%s) - $(stat -c %Y "$file")) / 86400 ))

# Windows (PowerShell)
$age = (Get-Date) - (Get-Item $file).LastWriteTime
$days = $age.Days
```

**Compare two files**:
```bash
# Returns 0 if file1 is newer than file2
[ "$file1" -nt "$file2" ] && echo "file1 is newer"
```

---

## When to Trigger Freshness Warnings

**Session Start**: Always check core context files
- `.shipkit/stack.json`
- `.shipkit/architecture.md`
- `.shipkit/why.md`

**Before Skill Execution**: Check skill-specific files
- `/shipkit-spec` → Check existing specs in `.shipkit/specs/`
- `/shipkit-plan` → Check existing plans in `.shipkit/plans/`
- `/shipkit-architecture-memory` → Check `architecture.md`

**After Major Changes**: Prompt for updates
- After `npm install` / `pip install` → Suggest stack.json update
- After creating new directories → Suggest architecture.md update
- After shipping feature → Suggest moving spec to `implemented/`

---

## Example Session Start Output

```
Session Start: shipkit-master loaded

Context Freshness:
  ✓ stack.json (2 days)
  ⚠ architecture.md (12 days - consider updating)
  ✓ why.md (5 days)

Active Work:
  ✓ specs/auth-flow.md (1 day)
  ✗ plans/refactor-api.md (5 days - STALE, not started?)

Suggestions:
  → architecture.md is aging. Run /shipkit-project-context to refresh.
  → plans/refactor-api.md may be abandoned. Archive or execute?
```
