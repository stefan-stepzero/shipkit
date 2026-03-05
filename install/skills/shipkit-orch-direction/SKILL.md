---
name: shipkit-orch-direction
id: SKL-ORCH-DIRECTION
description: Direction loop — dispatches strategic skills and assesses coherence. Produces why, vision, stage, and goals artifacts.
disable-model-invocation: true
context: fork
agent: shipkit-orch-direction-agent
---

# shipkit-orch-direction - Direction Loop

**Purpose**: Orchestrate the production and review of strategic artifacts until direction is coherent and stable.

## Scope

Strategic artifacts that define WHY and WHERE:
- `.shipkit/why.json` — Project vision and purpose
- `.shipkit/vision.json` — Strategic vision
- Stage assessment in why.json
- `.shipkit/goals/product.json` — Product success criteria
- `.shipkit/goals/engineering.json` — Engineering success criteria

## Roster

| Skill | What It Produces |
|-------|-----------------|
| `/shipkit-why-project` | why.json |
| `/shipkit-vision` | vision.json |
| `/shipkit-stage` | stage in why.json |
| `/shipkit-product-goals` | goals/product.json |
| `/shipkit-engineering-goals` | goals/engineering.json |
| `/shipkit-review-direction` | reviews/direction-assessment.json |

## Done Condition

All direction artifacts exist AND `.shipkit/reviews/direction-assessment.json` has `status: "pass"`.

## Dispatch Order

1. `/shipkit-why-project` — establishes foundation
2. `/shipkit-vision` — builds on why
3. `/shipkit-stage` — sets constraints
4. `/shipkit-product-goals` — defines product success
5. `/shipkit-engineering-goals` — defines technical success
6. `/shipkit-review-direction` — assesses coherence
7. If gaps found → re-dispatch specific producers → re-review
