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
- `.shipkit/stack.json` — Tech stack context (prerequisite for specs/plans)
- `.shipkit/codebase-index.json` — Codebase structure index (prerequisite for plans)
- `.shipkit/spec-roadmap.json` — Spec priority order
- `.shipkit/specs/*.json` — Feature specifications
- `.shipkit/plans/*.json` — Implementation plans
- `.shipkit/test-cases/` — Test specifications
- `.shipkit/user-tasks.json` — Manual user tasks

## Roster

| Skill | What It Produces |
|-------|-----------------|
| `/shipkit-project-context` | stack.json |
| `/shipkit-codebase-index` | codebase-index.json |
| `/shipkit-spec-roadmap` | spec-roadmap.json |
| `/shipkit-spec` | specs/*.json |
| `/shipkit-plan` | plans/*.json |
| `/shipkit-test-cases` | test-cases/ |
| `/shipkit-user-instructions` | user-tasks.json |
| `/shipkit-review-planning` | reviews/planning-assessment.json |

## Done Condition

All planning artifacts exist AND `.shipkit/reviews/planning-assessment.json` has `status: "pass"`.

## Orchestration Tracking

After each skill dispatch and after each review cycle, update `.shipkit/orchestration.json` (read existing content first, merge your loop state):

```json
{
  "loops": {
    "planning": {
      "status": "in_progress",
      "currentSkill": "shipkit-spec",
      "completedDispatches": [
        { "skill": "shipkit-spec-roadmap", "timestamp": "ISO" }
      ],
      "reviewCycles": 0
    }
  }
}
```

Set `activeLoop` to `"planning"` on entry. Set `status` to `"pass"` or `"partial"` when done. Increment `reviewCycles` each time `/shipkit-review-planning` runs.

## Dispatch Order

1. `/shipkit-project-context` — scans codebase, produces stack.json (skip if fresh)
2. `/shipkit-codebase-index` — indexes codebase structure (skip if fresh)
3. `/shipkit-spec-roadmap` — prioritizes what to spec
4. `/shipkit-spec` — specs for each prioritized feature
5. `/shipkit-plan` — architect produces implementation plans from specs (reads stack.json + codebase-index.json)
6. `/shipkit-test-cases` — PO produces test specifications from specs and plans
7. `/shipkit-user-instructions` — manual tasks for user
8. `/shipkit-review-planning` — assesses alignment
9. If gaps found → re-dispatch specific producers → re-review
