# shipkit-engineering-definition References

## Purpose
Extended documentation, schema details, and examples for shipkit-engineering-definition (v1 — technical approach).

## Contents

| File | Purpose |
|------|---------|
| `output-schema.md` | Full JSON schema for `.shipkit/engineering-definition.json` — mechanisms, components, design decisions, and all field definitions (including the `uses` / `whyNotStandard` ecosystem fields) |
| `architecture-log-schema.md` | **Canonical** convention for the architecture decisions log — the lean `architecture.json` + full `architecture-archive.json` split, the capped-active and superseded-stub schemas, and the dual-write rule every writer must follow |
| `example.json` | Realistic WorksheetForge example with 3 mechanisms, 4 components, and 3 design decisions — shows ecosystem defaults (`uses` / `whyNotStandard`) applied |
| `mechanism-standards.md` | Stack-agnostic map of common mechanism types → the standard solution to default to, plus anti-patterns. Read during Step 2b (Ecosystem Audit). |
| `ecosystem-defaults/<stack>.md` | Per-stack ecosystem defaults — the concrete libraries/patterns for a given stack (`python-llm`, `python-api`, `nextjs-fullstack`, `react-spa`). LLM-generated, dated, with refresh notes. Read during Step 2b for the matching stack(s). |

## When to Use
- `output-schema.md` — When you need the exact field definitions and types for engineering-definition.json
- `architecture-log-schema.md` — Before writing `architecture.json` / `architecture-archive.json`, or when adding/superseding an ADR. The dual-write rule and stub schema live here.
- `example.json` — When you need a concrete reference for how the format looks with real data
- `mechanism-standards.md` — During Step 2b (Ecosystem Audit): the stack-agnostic "what to reach for" map. Start here, then open the matching `ecosystem-defaults/<stack>.md`.
- `ecosystem-defaults/<stack>.md` — During Step 2b: the stack-specific library/pattern defaults. Read the file(s) matching the project stack (consult multiple for hybrid stacks).
