---
name: shipkit-review-direction
id: SKL-REVIEW-DIRECTION
description: Assess strategic artifact coherence — checks that vision aligns with why, goals are complete, and stage is realistic. Writes direction-assessment.json.
disable-model-invocation: true
context: fork
agent: shipkit-reviewer-direction-agent
---

# shipkit-review-direction - Direction Assessment

**Purpose**: Read all direction artifacts and assess whether they are coherent, complete, and internally consistent. Write a structured assessment for the direction orchestrator.

## Input

Read these artifacts:
- `.shipkit/why.json`
- `.shipkit/vision.json`
- `.shipkit/goals/strategic.json`
- `.shipkit/goals/product.json`
- `.shipkit/goals/engineering.json`
- `.shipkit/product-discovery.json`
- `.shipkit/product-definition.json`
- `.shipkit/engineering-definition.json`
- `.shipkit/metrics/latest.json`

## Coherence Checks

1. **Vision ↔ Why**: Does the vision describe a future that fulfills the stated purpose?
2. **Goals ↔ Vision**: Do goals, if achieved, realize the vision?
3. **Goals ↔ Stage**: Are thresholds realistic for the current stage?
4. **Completeness**: Are all required artifacts present with non-placeholder content?
5. **Internal consistency**: Do goals reference capabilities the vision describes?

## Output

Write `.shipkit/reviews/direction-assessment.json` with structured findings.

`status: "pass"` when all checks pass. `status: "gaps_found"` with specific `gaps[]` entries when issues exist. Each gap must include `artifact`, `issue`, `evidence`, and `fix` fields.
