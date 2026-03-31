---
name: shipkit-orch-direction
description: Direction loop — defines WHY, WHAT, and strategic foundations. Dispatches producer skills and reviews coherence. Can be invoked standalone or by shipkit-master.
context: fork
agent: shipkit-orch-direction-agent
effort: high
---

# shipkit-orch-direction - Direction Loop

**Purpose**: Orchestrate the production and review of strategic artifacts until direction is coherent and stable.

## Standalone Invocation

If invoked directly (no `orchestration.json` exists or `activeLoop` is not set by master):
1. Check that `.shipkit/` directory exists — if not, tell the user to run `/shipkit-why-project` first
2. Create `orchestration.json` yourself with `activeLoop: "direction"`
3. Proceed with normal dispatch order below

## Scope

Strategic artifacts that define WHY, WHAT, and HOW at definition level:
- `.shipkit/why.json` — Project vision and purpose
- `.shipkit/vision.json` — Strategic vision
- Stage assessment in why.json
- `.shipkit/product-discovery.json` — Personas and user journeys
- `.shipkit/product-definition.json` — Features, patterns, differentiators
- `.shipkit/engineering-definition.json` — Mechanisms, components, stack
- `.shipkit/architecture.json` — Architecture decisions (derived from engineering-definition)
- `.design-system/` — Design principles, tokens, aesthetic direction (UI projects only)
- `.shipkit/goals/product.json` — Product success criteria
- `.shipkit/goals/engineering.json` — Engineering success criteria

## Roster

| Skill | What It Produces |
|-------|-----------------|
| `/shipkit-why-project` | why.json |
| `/shipkit-vision` | vision.json |
| `/shipkit-stage` | goals/strategic.json |
| `/shipkit-product-discovery` | product-discovery.json |
| `/shipkit-product-definition` | product-definition.json |
| `/shipkit-engineering-definition` | engineering-definition.json + architecture.json |
| `/shipkit-design-system` | .design-system/ (DIRECTION.md, PRINCIPLES.md, MATURITY.md, tokens/) — **UI projects only** |
| `/shipkit-product-goals` | goals/product.json |
| `/shipkit-engineering-goals` | goals/engineering.json |
| `/shipkit-review-direction` | reviews/direction-assessment.json |

## Done Condition

All direction artifacts exist AND `.shipkit/reviews/direction-assessment.json` has `status: "pass"`.

## Orchestration Tracking

After each skill dispatch and after each review cycle, update `.shipkit/orchestration.json`:

```json
{
  "activeLoop": "direction",
  "status": "in_progress",
  "loops": {
    "direction": {
      "status": "in_progress",
      "currentSkill": "shipkit-vision",
      "completedDispatches": [
        { "skill": "shipkit-why-project", "timestamp": "ISO" }
      ],
      "reviewCycles": 0
    }
  }
}
```

Set `status` to `"pass"` or `"partial"` when the loop finishes. Increment `reviewCycles` each time `/shipkit-review-direction` runs.

## Dispatch Order

### Completion Tracking (MANDATORY)

Before dispatching any skills, create tasks for every dispatch in the roster:

1. `TaskCreate` for each of the 8 producer dispatches:
   - "Dispatch: /shipkit-why-project"
   - "Dispatch: /shipkit-vision"
   - "Dispatch: /shipkit-stage"
   - "Dispatch: /shipkit-product-discovery"
   - "Dispatch: /shipkit-product-definition"
   - "Dispatch: /shipkit-engineering-definition"
   - "Dispatch: /shipkit-design-system" (skip if no UI — check stack.json for frontend framework)
   - "Dispatch: /shipkit-product-goals"
   - "Dispatch: /shipkit-engineering-goals"
2. `TaskCreate`: "Review: /shipkit-review-direction"
3. `TaskCreate`: "Re-dispatch for gaps (if needed)"
4. `TaskCreate`: "Re-review after fixes (if needed)"

**Rules:**
- `TaskUpdate` each task to `completed` only after the dispatched skill finishes AND you update orchestration.json
- Do NOT declare the loop done until: (a) the review task is marked `completed`, AND (b) `direction-assessment.json` reports `status: "pass"`
- If review returns gaps: update re-dispatch and re-review tasks to `in_progress`, dispatch fixes, then re-review
- Before declaring done, read orchestration.json and verify completedDispatches count >= 8 producers + 1 passing review

1. `/shipkit-why-project` — establishes foundation
2. `/shipkit-vision` — builds on why
3. `/shipkit-stage` — sets constraints
4. `/shipkit-product-discovery` — informs product definition
5. `/shipkit-product-definition` — informs engineering definition
6. `/shipkit-engineering-definition` — informs goals and design system
7. `/shipkit-design-system` — scaffolds design direction + tokens (UI projects only; skip for CLI/API)
8. `/shipkit-product-goals` — defines product success
9. `/shipkit-engineering-goals` — defines technical success
10. `/shipkit-review-direction` — assesses coherence
11. If gaps found → re-dispatch specific producers → re-review
