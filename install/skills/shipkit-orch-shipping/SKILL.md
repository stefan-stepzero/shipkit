---
name: shipkit-orch-shipping
description: Shipping loop — spawns an implementation team, then dispatches verification and preflight. Builds, verifies, and gates release.
disable-model-invocation: true
context: fork
agent: shipkit-orch-shipping-agent
---

# shipkit-orch-shipping - Shipping Loop

**Purpose**: Orchestrate implementation via an Agent Team, then verify quality and gate release.

## Scope

Execution that delivers working software:
- Code changes — Implementation by Agent Team
- `.shipkit/verification-report.json` — Quality verification
- `.shipkit/preflight.json` — Release gate

## Roster

| Step | Method | What It Produces |
|------|--------|-----------------|
| Implement | Direct team (Agent/Task tools) | code changes |
| `/shipkit-review-shipping` | Skill dispatch → reviewer-shipping | verification-report.json |
| `/shipkit-preflight` | Skill dispatch → reviewer-shipping | preflight.json |

## Done Condition

`.shipkit/verification-report.json` has `status: "pass"` AND preflight passes.

## Dispatch Order

1. Read `.shipkit/plans/` and `.shipkit/test-cases/` produced by planning loop
2. Create Agent Team — spawn teammates with plan assignments
3. Monitor team progress via TaskList until implementation complete
4. `/shipkit-review-shipping` — reviewer-shipping assesses quality
5. If issues found → assign fixes to teammates → re-dispatch `/shipkit-review-shipping`
6. When verification passes → `/shipkit-preflight` — final release gate
