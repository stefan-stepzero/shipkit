---
name: shipkit-orch-shipping
description: Shipping loop — spawns implementation team, verifies quality, gates release. Can be invoked standalone or by shipkit-master.
context: fork
agent: shipkit-orch-shipping-agent
effort: high
---

# shipkit-orch-shipping - Shipping Loop

**Purpose**: Orchestrate implementation via an Agent Team, then verify quality and gate release.

## Standalone Invocation

If invoked directly (no `orchestration.json` exists or `activeLoop` is not set by master):
1. Verify planning artifacts exist (`.shipkit/plans/` with at least one plan, `.shipkit/test-cases/`) — if missing, tell the user to run `/shipkit-orch-planning` first
2. Create `orchestration.json` yourself with `activeLoop: "shipping"`
3. Proceed with normal dispatch order below

## Scope

Execution that delivers working software:
- Code changes — Implementation by Agent Team
- `.shipkit/verification-report.json` — Quality verification
- `.shipkit/preflight.json` — Release gate

## Roster

| Step | Method | What It Produces |
|------|--------|-----------------|
| `/shipkit-work-memory` | Skill dispatch | progress.json (checkpoint) |
| Implement | Direct team (Agent tool) | code changes |
| `/shipkit-review-shipping` | Skill dispatch → reviewer-shipping | verification-report.json |
| `/shipkit-preflight` | Skill dispatch → reviewer-shipping | preflight.json |

## Done Condition

`.shipkit/verification-report.json` has `status: "pass"` AND preflight passes.

## Orchestration Tracking

After each major step and after each review cycle, update `.shipkit/orchestration.json` (read existing content first, merge your loop state):

```json
{
  "loops": {
    "shipping": {
      "status": "in_progress",
      "currentSkill": "shipkit-review-shipping",
      "completedDispatches": [
        { "skill": "implementation-team", "timestamp": "ISO" }
      ],
      "reviewCycles": 0
    }
  }
}
```

Set `activeLoop` to `"shipping"` on entry. Set `status` to `"pass"` or `"partial"` when done. Increment `reviewCycles` each time `/shipkit-review-shipping` runs.

## Dispatch Order

### Completion Tracking

Create tasks for each dispatch:
- `TaskCreate`: "Dispatch: /shipkit-work-memory (checkpoint)"
- `TaskCreate`: "Create Agent Team with plan assignments"
- `TaskCreate`: "Monitor team until implementation complete"
- `TaskCreate`: "Dispatch: /shipkit-review-shipping"
- `TaskCreate`: "Fix issues + re-review (if needed)"
- `TaskCreate`: "Dispatch: /shipkit-preflight (release gate)"

Verification passing is NOT the finish line — preflight must also pass. Do NOT skip preflight after a clean verification report.

1. `/shipkit-work-memory` — checkpoint progress before implementation begins
2. Read `.shipkit/plans/` and `.shipkit/test-cases/` produced by planning loop
3. Create Agent Team — spawn teammates with plan assignments
4. Monitor team progress via TaskList until implementation complete
5. `/shipkit-review-shipping` — reviewer-shipping assesses quality
6. If issues found → assign fixes to teammates → re-dispatch `/shipkit-review-shipping`
7. When verification passes → `/shipkit-preflight` — final release gate
