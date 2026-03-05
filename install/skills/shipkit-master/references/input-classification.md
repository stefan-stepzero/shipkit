# Input Classification Rules

Master classifies every input to determine which orchestration loop it affects.

---

## Classification Table

| Input Signal | Affects Loop | Action |
|-------------|-------------|--------|
| "Why are we building this?" / challenges vision | direction | Destabilizes direction |
| "Change the stage" / "We're not MVP yet" | direction | Destabilizes direction |
| "Revenue targets changed" / business metric shift | direction | Destabilizes direction |
| "Add a feature" / "Users need X" | planning | Destabilizes planning |
| "Change the spec" / "Spec is wrong" | planning | Destabilizes planning |
| "Users don't understand the flow" / UX issue | planning | Destabilizes planning (needs spec revision) |
| "We need better performance" / engineering criteria | planning | Destabilizes planning |
| "This is broken" / "Bug report" | shipping | Stays in shipping |
| "Tests fail" / "Build broken" | shipping | Stays in shipping |
| "Ship it" / "Deploy" | shipping | Stays in shipping |
| Explicit skill name (e.g., "/shipkit-spec") | N/A | Direct routing — bypass classification |
| "What's next?" / "Continue" | current | Check orchestration.json nextRecommended |
| "Help me think about X" | depends | Classify by topic — vision=direction, product=planning, tech=planning |

---

## Signal Classification (from metrics/latest.json)

| Signal Type | criterionId Prefix | Affects Loop |
|------------|-------------------|-------------|
| Business metrics (DAU, revenue, retention) | S-* | direction |
| User outcome metrics (completion rate, satisfaction) | P-* | planning |
| Technical metrics (response time, error rate, build status) | E-* | shipping |
| Unclassified (no criterionId) | — | Queue to pendingInput for human classification |

---

## Destabilization Rules

**When input destabilizes a loop:**
1. Mark the affected loop as `active`
2. Mark all **inner** loops as `blocked`
3. Set `activeLoop` to the destabilized loop
4. Log the destabilization in `dispatchLog`

**When input is in the current active loop:**
- Process normally — dispatch to appropriate skill
- No loop transition needed

**When input is in an inner loop and outer loops are stable:**
- Valid — inner loop can proceed
- Only blocked if an outer loop becomes unstable

**When input is in an outer loop that was stable:**
- This is an escalation — the outer loop needs attention before inner work continues

---

## The Escalation Pattern

If during shipping (Loop 3) you discover that a spec is wrong:

```
1. Classify: "spec is wrong" → affects planning (Loop 2)
2. Destabilize planning: planning.status = "active"
3. Block shipping: shipping.status = "blocked"
4. Switch: activeLoop = "planning"
5. After planning re-stabilizes: unblock shipping
```

---

## Ambiguous Input

When input is hard to classify:
- Default to the **current active loop** — most input relates to what you're working on
- If genuinely ambiguous, ask the user: "Does this affect the vision/strategy, the product plan, or the current implementation?"
- Never guess on direction-level input — always confirm with the user before destabilizing direction
