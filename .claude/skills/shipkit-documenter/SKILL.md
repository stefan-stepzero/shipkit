---
name: shipkit-documenter
description: Document bugs, ideas, improvements, and decisions. Manages docs/development/manifest.json as the central registry.
argument-hint: "document|list|status [title or filters]"
---

# Shipkit Documenter

Keeps `docs/development/` tidy. Every artifact gets a manifest entry. New items get their own JSON file in a category subfolder and a manifest entry.

## Folder Structure

```
docs/development/
├── manifest.json
├── system-design/       # Architecture, pipeline design, design philosophy
├── cc-reference/        # Claude Code changelog, agent teams, plugins
├── quality-standards/   # Skill quality patterns, best practices
├── integration/         # 7-file integration system
├── dev-progress/        # Session reports, scout/analyst/opportunity reports
├── inspiration/         # External references, analysis, community insights
└── archive/             # Superseded documents
```

## Modes

### `document [title]` (default when no mode specified)

Create a new documented item.

1. Read `docs/development/manifest.json`
2. Get the `nextId` counter
3. Ask the user (if not provided via args):
   - **Title** — short description
   - **Category** — which folder: system-design, cc-reference, quality-standards, integration, dev-progress, inspiration
   - **Tags** — freeform tags (e.g., bug, idea, improvement, decision, hooks, skills, windows)
   - **Details** — what to capture (description, context, affected files, etc.)
4. Create the item file at `docs/development/{category}/DOC-{nextId}-{slug}.json` where `{slug}` is a 2-3 word kebab-case summary derived from the title:

```json
{
  "$schema": "shipkit-dev-artifact",
  "type": "documented-item",
  "id": "DOC-NNN",
  "title": "...",
  "description": "...",
  "status": "open",
  "tags": ["..."],
  "createdAt": "ISO8601",
  "updatedAt": "ISO8601",
  "context": {}
}
```

The `context` object holds whatever is relevant — `affectedFiles`, `reproSteps`, `alternatives`, `rationale`, `sketch`, etc. No rigid schema, just what makes sense for this item.

5. Add entry to manifest's `entries` array (with `file` path including category subfolder)
6. Increment `nextId` in manifest
7. Save manifest

### `list [filters]`

Show what's in the manifest, grouped by category.

1. Read `docs/development/manifest.json`
2. Group entries by their folder prefix (system-design, cc-reference, etc.)
3. Display as grouped tables: ID, title, status, tags
4. If filters provided, match against tags, status, or category (e.g., `list bug`, `list open`, `list cc-reference`)

### `update <id>`

Update an existing item.

1. Read the item file referenced by the manifest entry
2. Ask what to change (status, description, add notes, etc.)
3. Update the item file and set `updatedAt`
4. Update the manifest entry if title/status/tags changed

### `status`

Quick summary of the manifest.

1. Read manifest
2. Show: total entries, count by status, count by category, count by most-used tags, last 5 updated items

### `register <file>`

Add an existing file in `docs/development/` to the manifest without creating a new item file.

1. Verify the file exists in `docs/development/` (check subfolders too)
2. Ask for title and tags
3. Add entry to manifest with the file path relative to `docs/development/` (e.g., `cc-reference/agent-teams-best-practices.md`)
4. Increment `nextId`, save manifest

### `clean`

Audit manifest against actual files.

1. Read manifest
2. Check each entry's `file` exists on disk (resolving paths relative to `docs/development/`)
3. Scan all subfolders (system-design, cc-reference, quality-standards, integration, dev-progress, inspiration, archive) for files NOT in the manifest (excluding directories and the manifest itself)
4. Report: missing files (in manifest but not on disk), untracked files (on disk but not in manifest)
5. Offer to fix: remove stale entries, register untracked files

## Output Quality Checklist

- [ ] Manifest `nextId` is always greater than the highest existing DOC-NNN id
- [ ] Every new item has both a JSON file and a manifest entry
- [ ] `updatedAt` on manifest reflects the latest change
- [ ] No duplicate IDs in manifest
- [ ] Tags are lowercase, hyphenated
- [ ] File paths in manifest include category subfolder prefix

## Context Files

- **Reads:** `docs/development/manifest.json`
- **Writes:** `docs/development/manifest.json`, `docs/development/{category}/DOC-NNN-{slug}.json`
