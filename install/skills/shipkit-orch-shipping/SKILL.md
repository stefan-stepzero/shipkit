---
name: shipkit-orch-shipping
id: SKL-ORCH-SHIPPING
description: Shipping loop — dispatches plan, implementation, testing, and verification skills. Builds, verifies, and gates release.
disable-model-invocation: true
context: fork
agent: shipkit-orch-shipping-agent
---

# shipkit-orch-shipping - Shipping Loop

**Purpose**: Orchestrate implementation, testing, verification, and release gating until code passes all quality checks.

## Scope

Execution artifacts that deliver working software:
- `.shipkit/plan.json` — Implementation plan
- Test files — Test specifications and code
- Code changes — Implementation
- `.shipkit/verification-report.json` — Quality verification
- Preflight checklist — Release gate

## Roster

| Skill | What It Produces |
|-------|-----------------|
| `/shipkit-plan` | plan.json |
| `/shipkit-test-cases` | test files |
| `/shipkit-team` | code changes |
| `/shipkit-verify` | verification-report.json |
| `/shipkit-preflight` | preflight checklist |

## Done Condition

`.shipkit/verification-report.json` has `status: "pass"` AND preflight passes.

## Dispatch Order

1. `/shipkit-plan` — architect produces implementation plan
2. `/shipkit-test-cases` — implementer writes test specifications
3. `/shipkit-team` — implementer builds the code
4. `/shipkit-verify` — reviewer-shipping assesses quality
5. If issues found → re-dispatch `/shipkit-team` → re-dispatch `/shipkit-verify`
6. When verification passes → `/shipkit-preflight` — final release gate
