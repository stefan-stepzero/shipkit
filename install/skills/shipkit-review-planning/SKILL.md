---
name: shipkit-review-planning
description: Internal reviewer — assesses planning artifact alignment. Checks definitions agree, specs cover roadmap, no gaps. Dispatched by orch-planning, not for direct use.
context: fork
agent: shipkit-reviewer-planning-agent
---

# shipkit-review-planning - Planning Assessment

**Purpose**: Read all planning artifacts and cross-reference them for alignment. Write a structured assessment for the planning orchestrator.

## Input

**Required artifacts** (the planning loop must produce all of these):
- `.shipkit/stack.json`
- `.shipkit/codebase-index.json`
- `.shipkit/spec-roadmap.json`
- `.shipkit/specs/*.json` — at least one spec per roadmap item
- `.shipkit/plans/*.json` — at least one plan per spec
- `.shipkit/test-cases/` — test specifications
- `.shipkit/user-tasks.json` — manual user tasks

**Direction context** (produced by prior loop, read for cross-reference):
- `.shipkit/why.json`, `.shipkit/vision.json`
- `.shipkit/product-definition.json`, `.shipkit/engineering-definition.json`
- `.shipkit/architecture.json`
- `.shipkit/goals/strategic.json`, `.shipkit/goals/product.json`, `.shipkit/goals/engineering.json`

## Alignment Checks

1. **Completeness**: Are ALL required planning artifacts present? Missing artifacts are gaps.
2. **Product ↔ Engineering**: Every product feature has a corresponding mechanism?
3. **Definition ↔ Specs**: Every defined feature has a spec?
4. **Specs ↔ Roadmap**: Roadmap includes all specs with sensible priority?
5. **Plans ↔ Specs**: Every spec has a plan? Plans reference the correct spec?
6. **Stage alignment**: Specs and plans scoped for current stage?
7. **Goal coverage**: Specs, if implemented, satisfy product and engineering goals?
8. **Architecture consistency**: Do plans align with architecture.json decisions?

## Output

Write `.shipkit/reviews/planning-assessment.json` with structured findings.

`status: "pass"` when all checks pass. `status: "gaps_found"` with specific `gaps[]` entries when issues exist. Each gap must include `artifact`, `issue`, `relatedArtifact`, `evidence`, and `fix` fields.
