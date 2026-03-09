---
name: shipkit-vision
description: Internal producer — strategic visionary gateway. Sets project direction, stage, and business goals. Dispatched by orch-direction.
argument-hint: "<gap description or strategic question>"
context: fork
agent: shipkit-visionary-agent
---

# shipkit-vision - Strategic Vision Gateway

**Purpose**: Activate the Visionary agent to set or adjust project direction, stage, and strategic goals.

---

## Your Task

You have been dispatched by the master orchestrator to close a strategic gap.

**Gap context from master**: $ARGUMENTS

## Process

1. Read `.shipkit/goals/strategic.json` (if exists) to understand current strategic state
2. Read `.shipkit/why.json` (if exists) to understand current vision
3. Based on the gap described above:
   - If no vision exists → run `/shipkit-why-project` to establish it
   - If no strategic goals exist → run `/shipkit-stage` to set stage + business metrics
   - If strategic goals are unmet → assess what needs adjustment (stage, constraints, metrics)
   - If stage change needed → run `/shipkit-stage` to update stage and cascade constraints
4. Write results back to `.shipkit/goals/strategic.json` and `.shipkit/why.json`
5. Report what you produced and what changed

## Context Files

**Reads**: `.shipkit/why.json`, `.shipkit/goals/strategic.json`, `README.md`, `package.json`

**Artifact strategy: replace** — Overwrites the existing artifact file. Previous content is not preserved.

**Writes**: `.shipkit/why.json`, `.shipkit/goals/strategic.json`

## Exit Conditions

Done when:
- `.shipkit/why.json` exists with vision and stage
- `.shipkit/goals/strategic.json` exists with criteria and thresholds
- The specific gap described in $ARGUMENTS is addressed
