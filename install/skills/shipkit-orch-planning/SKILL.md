---
name: shipkit-orch-planning
id: SKL-ORCH-PLANNING
description: Planning loop — dispatches product/engineering definition and spec skills, assesses alignment. Produces definitions, specs, and roadmap.
disable-model-invocation: true
context: fork
agent: shipkit-orch-planning-agent
---

# shipkit-orch-planning - Planning Loop

**Purpose**: Orchestrate the production and review of planning artifacts until product and engineering definitions are aligned and specs are complete.

## Scope

Planning artifacts that define WHAT and HOW at design level:
- `.shipkit/product-discovery.json` — Personas and user journeys
- `.shipkit/product-definition.json` — Features, patterns, differentiators
- `.shipkit/engineering-definition.json` — Mechanisms, components, stack
- `.shipkit/specs/*.json` — Feature specifications
- `.shipkit/spec-roadmap.json` — Spec priority order
- `.shipkit/user-instructions.json` — User task tracking

## Roster

| Skill | What It Produces |
|-------|-----------------|
| `/shipkit-product-discovery` | product-discovery.json |
| `/shipkit-product-definition` | product-definition.json |
| `/shipkit-engineering-definition` | engineering-definition.json |
| `/shipkit-spec` | specs/*.json |
| `/shipkit-spec-roadmap` | spec-roadmap.json |
| `/shipkit-user-instructions` | user-instructions.json |
| `/shipkit-review-planning` | reviews/planning-assessment.json |

## Done Condition

All planning artifacts exist AND `.shipkit/reviews/planning-assessment.json` has `status: "pass"`.

## Dispatch Order

1. `/shipkit-product-discovery` — informs product definition
2. `/shipkit-product-definition` — informs engineering definition
3. `/shipkit-engineering-definition` — informs specs
4. `/shipkit-spec-roadmap` — prioritizes what to spec
5. `/shipkit-spec` — specs for each prioritized feature
6. `/shipkit-user-instructions` — manual tasks for user
7. `/shipkit-review-planning` — assesses alignment
8. If gaps found → re-dispatch specific producers → re-review
