# Orchestration Modes

Two modes control how the master moves through the pipeline.

## Mode 1: Gated (Default)

Mandatory user approval at loop boundaries.

**Sequence**: Direction loop → USER GATE → Planning loop → USER GATE → Shipping loop → USER GATE → done

**Triggered by**: default, or user says "step by step", "walk me through it"

**Gate questions:**

| After | Gate Question |
|-------|---------------|
| Direction loop completes | "Here's the strategic direction and stage. Does this match your intent?" |
| Planning loop completes | "Here's the product definition and specs. Is this the right direction?" |
| Shipping loop completes | "Verification passed. Ready to commit/ship?" |

**At each gate:**
1. Summarize what was produced (artifact names, key decisions)
2. Ask for approval
3. Wait for user response
4. If approved → proceed to next loop
5. If rejected → ask what to adjust, re-dispatch the loop with feedback

## Mode 2: Autonomous

Master runs through all three loops without pausing at gates. Each loop's internal feedback cycle (via reviewers) provides quality assurance instead of human review. Only stops when shipping loop reports complete, or a loop guard triggers.

**Triggered by**: user says "autonomous", "yolo", "auto", "just do it", "run with it"

**Autonomous gate replacement:**

| Gated Mode Gate | Autonomous Mode Replacement |
|----------------|---------------------------|
| After direction loop | Auto-proceed (direction is strategic, low risk) |
| After planning loop | Auto-proceed (specs are reversible) |
| After shipping loop | Self-verify via reviewer-shipping. If all verifiable criteria pass → Termination. If failures → report with evidence. |

## User Intent Shortcuts

| User Says | Interpret As | Mode |
|-----------|-------------|------|
| "Build X" / "Work on X" / "Ship X" | Full goal — advance from current state | Gated |
| "Build X autonomously" / "yolo" / "auto" / "just do it" / "run with it" | Full goal — self-verifying | Autonomous |
| "Step by step" / "Walk me through" | Full goal — explicit user steering | Gated |
| "What's next?" / "Continue" | Check goals, dispatch for largest gap | Current mode |
| "Check quality" / "Review" | Run `/shipkit-review-shipping` | N/A |
| "What's the status?" | Status report from goal files | N/A |
| Explicit skill name | Direct routing (bypass loop dispatch) | N/A |
