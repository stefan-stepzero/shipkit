---
name: shipkit-review-direction
description: Internal reviewer — assesses strategic artifact coherence. Checks vision/why alignment, goal completeness, stage realism. Dispatched by orch-direction, not for direct use.
user-invocable: false
context: fork
agent: shipkit-reviewer-direction-agent
effort: medium
---

# shipkit-review-direction - Direction Assessment

**Purpose**: Read all direction artifacts and assess whether they are coherent, complete, and internally consistent. Write a structured assessment for the direction orchestrator.

## Input

**Required artifacts** (the direction loop must produce all of these):
- `.shipkit/why.json`
- `.shipkit/vision.json`
- `.shipkit/product-discovery.json`
- `.shipkit/product-definition.json`
- `.shipkit/engineering-definition.json`
- `.shipkit/architecture.json`
- `.shipkit/design-system/` (DIRECTION.md, PRINCIPLES.md, tokens/ — if exists)
- `.shipkit/goals/strategic.json`
- `.shipkit/goals/product.json`
- `.shipkit/goals/engineering.json`

**Optional context** (read if present, don't flag as missing):
- `.shipkit/metrics/latest.json` — only exists after implementation

## Coherence Checks

1. **Completeness**: Are ALL 9 required direction artifacts present with non-placeholder content? Missing artifacts are gaps.
2. **Vision ↔ Why**: Does the vision describe a future that fulfills the stated purpose?
3. **Goals ↔ Vision**: Do goals, if achieved, realize the vision?
4. **Goals ↔ Stage**: Are thresholds realistic for the current stage? Do all goals have rubrics?
5. **Internal consistency**: Do goals reference capabilities the vision describes?
6. **Architecture ↔ Engineering Definition**: Are architecture decisions consistent with the mechanisms and components defined?
7. **Design System ↔ Vision** (if `.shipkit/design-system/` exists): Do principles align with the vision? Does aesthetic direction fit the target audience? Does token format match the stack?

## Output

Write `.shipkit/reviews/direction-assessment.json` with structured findings.

`status: "pass"` when all checks pass. `status: "gaps_found"` with specific `gaps[]` entries when issues exist. Each gap must include `artifact`, `issue`, `evidence`, and `fix` fields.
