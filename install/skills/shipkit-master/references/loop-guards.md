# Loop Stability Criteria & Guards

Defines when each orchestration loop is stable, what blocks progression, and guard limits.

---

## Loop Stability Criteria

### Direction (Loop 1) — stable when:
- `why.json` exists and has been human-approved
- `goals/strategic.json` exists with stage set
- No verifiable S-* criteria are `below-threshold`

### Planning (Loop 2) — stable when:
- Direction loop is stable (prerequisite)
- `product-definition.json` exists
- `engineering-definition.json` exists
- `goals/product.json` exists with criteria defined
- `goals/engineering.json` exists with criteria defined
- At least one spec exists in `specs/active/`
- No verifiable P-*/E-* criteria are `below-threshold` (unless implementation pending)

### Shipping (Loop 3) — stable when:
- Planning loop is stable (prerequisite)
- At least one plan exists in `plans/active/`
- All verifiable criteria across all goal files are `at-threshold` or `exceeded`
- This is essentially the Termination Protocol

---

## Minimum Viable Loop Progression

Not all artifacts are required to advance. The **minimum** path:

| Loop | Required to Enter | Recommended (improve quality) |
|------|-------------------|-------------------------------|
| Direction | why.json + goals/strategic.json | — |
| Planning | product-definition.json + 1 spec in specs/active/ | discovery, engineering-definition, goals |
| Shipping | 1 plan in plans/active/ + implementation started | test-cases, full goal coverage |

Master should **suggest** recommended artifacts but **not require** them for progression.

---

## Guard Limits

| Loop | Max Dispatches | Reset Trigger |
|------|---------------|---------------|
| Direction | 4 | User confirms stage + vision |
| Planning | 8 | All planning artifacts present |
| Shipping | 6 | All verifiable criteria passing |

### On exceeding guard limit:
1. Pause dispatching
2. Escalate to user: "Loop {name} has had {N} dispatches without stabilizing. What should I adjust?"
3. Wait for user input
4. Reset counter after user input

### Counter mechanics:
- Each dispatch within a loop increments that loop's `dispatchCount`
- Counters reset to 0 when loop transitions to `stable`
- Counters reset to 0 after user input at escalation
- Switching to a different loop does NOT reset the original loop's counter

---

## Loop Transition Rules

### Entering a loop:
- Can only enter if all outer loops are `stable`
- Exception: direction loop has no outer prerequisite

### Leaving a loop (stabilization):
- All stability criteria met → mark as `stable`, set `lastStabilized`
- Unblock the next inner loop

### Blocking a loop:
- When an outer loop becomes `active` or `idle`, all inner loops become `blocked`
- `blocked` loops cannot receive dispatches

### Destabilizing a loop:
- External input or signal changes a stable loop to `active`
- All inner loops immediately become `blocked`
- `destabilizedBy` records what caused it

---

## Status Values

| Status | Meaning | Can Dispatch? |
|--------|---------|---------------|
| `stable` | All criteria met, artifacts present | No (nothing to do) |
| `active` | Master is working in this loop | Yes |
| `blocked` | Outer loop not stable | No |
| `idle` | No work defined yet (fresh project) | Yes (bootstrap) |
