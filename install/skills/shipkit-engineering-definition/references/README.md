# shipkit-engineering-definition References

## Purpose
Extended documentation, schema details, and examples for shipkit-engineering-definition (v1 — technical approach).

## Contents

| File | Purpose |
|------|---------|
| `output-schema.md` | Full JSON schema for `.shipkit/engineering-definition.json` — mechanisms, components, design decisions, and all field definitions |
| `architecture-log-schema.md` | **Canonical** convention for the architecture decisions log — the lean `architecture.json` + full `architecture-archive.json` split, the capped-active and superseded-stub schemas, and the dual-write rule every writer must follow |
| `example.json` | Realistic WorksheetForge example with 3 mechanisms, 4 components, and 3 design decisions |

## When to Use
- `output-schema.md` — When you need the exact field definitions and types for engineering-definition.json
- `architecture-log-schema.md` — Before writing `architecture.json` / `architecture-archive.json`, or when adding/superseding an ADR. The dual-write rule and stub schema live here.
- `example.json` — When you need a concrete reference for how the format looks with real data
