---
name: shipkit-review-planning
description: Internal reviewer — assesses planning artifact alignment. Checks definitions agree, specs cover roadmap, no gaps. Dispatched by orch-planning, not for direct use.
context: fork
agent: shipkit-reviewer-planning-agent
---

# shipkit-review-planning - Planning Assessment

**Purpose**: Read all planning artifacts and cross-reference them for alignment. Write a structured assessment for the planning orchestrator.

## Input

Read these artifacts:
- `.shipkit/product-discovery.json`
- `.shipkit/product-definition.json`
- `.shipkit/engineering-definition.json`
- `.shipkit/specs/*.json`
- `.shipkit/spec-roadmap.json`
- `.shipkit/user-instructions.json`

Also read direction artifacts for context:
- `.shipkit/why.json` (vision, constraints)
- `.shipkit/goals/strategic.json` (stage)
- `.shipkit/goals/strategic.json`
- `.shipkit/goals/product.json`
- `.shipkit/goals/engineering.json`
- `.shipkit/plans/*.json` (implementation plans under review)

## Alignment Checks

1. **Product ↔ Engineering**: Every product feature has a corresponding mechanism?
2. **Definition ↔ Specs**: Every defined feature has a spec?
3. **Specs ↔ Roadmap**: Roadmap includes all specs with sensible priority?
4. **Stage alignment**: Specs scoped for current stage?
5. **Completeness**: All artifacts present with non-placeholder content?
6. **Goal coverage**: Specs, if implemented, satisfy product and engineering goals?

## Output

Write `.shipkit/reviews/planning-assessment.json` with structured findings.

`status: "pass"` when all checks pass. `status: "gaps_found"` with specific `gaps[]` entries when issues exist. Each gap must include `artifact`, `issue`, `relatedArtifact`, `evidence`, and `fix` fields.
