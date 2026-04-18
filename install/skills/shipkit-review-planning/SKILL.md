---
name: shipkit-review-planning
description: Internal reviewer — assesses planning artifact alignment. Checks definitions agree, specs cover roadmap, no gaps. Dispatched by orch-planning, not for direct use.
user-invocable: false
context: fork
agent: shipkit-reviewer-planning-agent
effort: medium
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
- `.shipkit/why.json`
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
9. **Prerequisites by phase**: Group blocking user tasks by their `blocksPhase` value. Report separately:
   - Current-phase blockers (tasks where `blocksPhase` matches `why.json` current stage AND `blocking: true`)
   - Future-phase blockers (tasks where `blocksPhase` is a later stage)
   - General tasks (tasks where `blocksPhase` is `null`)

   **Only current-phase blockers count as blocking prerequisites.** Future-phase tasks are informational — do NOT count them in the blocker total. If a task has no `blocksPhase` field (legacy format), infer from context or treat as current-phase.

### Completion Tracking

Create tasks for each alignment check:
- `TaskCreate`: "Check 1: Completeness (all artifacts present)"
- `TaskCreate`: "Check 2: Product ↔ Engineering alignment"
- `TaskCreate`: "Check 3: Definition ↔ Specs"
- `TaskCreate`: "Check 4: Specs ↔ Roadmap"
- `TaskCreate`: "Check 5: Plans ↔ Specs"
- `TaskCreate`: "Check 6: Stage alignment"
- `TaskCreate`: "Check 7: Goal coverage"
- `TaskCreate`: "Check 8: Architecture consistency"
- `TaskCreate`: "Check 9: Prerequisites by phase"
- `TaskCreate`: "Write planning-assessment.json"

`TaskUpdate` each task to `in_progress` when starting it, `completed` when done.

Each check task requires evidence — do NOT mark complete without citing specific artifacts. Do NOT write the assessment until all 9 checks are completed.

## Output

Write `.shipkit/reviews/planning-assessment.json` with structured findings.

`status: "pass"` when all checks pass. `status: "gaps_found"` with specific `gaps[]` entries when issues exist. Each gap must include `artifact`, `issue`, `relatedArtifact`, `evidence`, and `fix` fields.

**For prerequisite reporting**, the assessment must include a `prerequisites` summary object:
```json
{
  "prerequisites": {
    "currentPhase": "phase-0",
    "blocking": [{ "id": "...", "title": "...", "blocksPhase": "phase-0" }],
    "futurePhase": [{ "id": "...", "title": "...", "blocksPhase": "phase-1" }],
    "general": [{ "id": "...", "title": "...", "blocksPhase": null }]
  }
}
```
The `blocking` array drives the blocker count. `futurePhase` and `general` are informational only.

## After Completion

Assessment written to `.shipkit/reviews/planning-assessment.json`.

**Next:** The calling orchestrator (`shipkit-orch-planning-agent`) reads this assessment:
- If **gaps found**: re-dispatches the affected upstream skills for revision, then re-runs this reviewer.
- If **pass**: proceeds to the next loop phase (or reports completion to shipkit-orch-master-agent).

This skill is normally invoked by the orchestrator, not called directly by the user.
