---
name: shipkit-orch-planning
description: Internal orchestrator — planning loop. Dispatches definition and spec skills, assesses alignment. Dispatched by shipkit-master, not for direct use.
context: fork
agent: shipkit-orch-planning-agent
---

# shipkit-orch-planning - Planning Loop

**Purpose**: Orchestrate the production and review of planning artifacts until product and engineering definitions are aligned and specs are complete.

## Scope

Planning artifacts that translate definitions into actionable plans:
- `.shipkit/spec-roadmap.json` — Spec priority order
- `.shipkit/specs/*.json` — Feature specifications
- `.shipkit/plans/*.json` — Implementation plans
- `.shipkit/test-cases/` — Test specifications
- `.shipkit/user-tasks.json` — Manual user tasks

## Roster

| Skill | What It Produces |
|-------|-----------------|
| `/shipkit-spec-roadmap` | spec-roadmap.json |
| `/shipkit-spec` | specs/*.json |
| `/shipkit-plan` | plans/*.json |
| `/shipkit-test-cases` | test-cases/ |
| `/shipkit-user-instructions` | user-tasks.json |
| `/shipkit-review-planning` | reviews/planning-assessment.json |

## Done Condition

All planning artifacts exist AND `.shipkit/reviews/planning-assessment.json` has `status: "pass"`.

## Dispatch Order

1. `/shipkit-spec-roadmap` — prioritizes what to spec
2. `/shipkit-spec` — specs for each prioritized feature
3. `/shipkit-plan` — architect produces implementation plans from specs
4. `/shipkit-test-cases` — PO produces test specifications from specs and plans
5. `/shipkit-user-instructions` — manual tasks for user
6. `/shipkit-review-planning` — assesses alignment
7. If gaps found → re-dispatch specific producers → re-review
