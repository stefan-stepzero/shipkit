---
name: shipkit-metrics
description: "Capture current metric values for goal evaluation. Triggers: 'log metrics', 'update metrics', 'record measurements'."
argument-hint: "[metric ID or --list]"
effort: low
---

# shipkit-metrics - Metric Capture Utility

**Purpose**: Let users record current metric values into `.shipkit/metrics/latest.json` so that `/shipkit-product-goals --evaluate` and `/shipkit-engineering-goals --evaluate` can compare actuals against targets.

This is a manual capture tool — metrics come from real-world sources (analytics, APMs, test runs, user feedback) that no skill can auto-generate.

---

## When to Invoke

**User triggers**:
- "Log metrics", "Update metrics", "Record measurements"
- "Our response time is now 200ms"
- "Conversion rate hit 12%"
- "Test coverage is at 85%"

**Workflow position**:
- After goals are defined (`/shipkit-product-goals`, `/shipkit-engineering-goals`)
- Before goal evaluation (`--evaluate` mode on goals skills)

---

## Prerequisites

**Recommended** (to know which metrics to capture):
- `.shipkit/goals/product.json` — P-* criteria with thresholds
- `.shipkit/goals/engineering.json` — E-* criteria with thresholds

**If missing**: Accept any metric the user provides, using freeform IDs.

---

## Arguments

- No args or metric text → Interactive mode (show goals, ask for values)
- `--list` → Show current metrics and which criteria are still unmeasured
- Metric ID + value (e.g., `P-001 82%`) → Quick capture mode

---

## Process

### Mode 1: Interactive (default)

1. Read `.shipkit/goals/product.json` and `.shipkit/goals/engineering.json` if they exist
2. Extract all criteria IDs and their metrics/thresholds
3. Read `.shipkit/metrics/latest.json` if exists (to show what's already captured)
4. Present unmeasured criteria:

```
Metrics Capture — {N} criteria defined, {M} measured

Unmeasured:
  P-001: Task completion rate (target: > 80%)
  P-003: Page load satisfaction (target: < 3s)
  E-002: API response time (target: < 500ms)

Already measured:
  E-001: Test coverage = 85% (target: > 80%) — exceeded
  P-002: Error rate = 2.1% (target: < 5%) — at-threshold

Enter a criterion ID and its current value (e.g., "P-001 82%"), or "done" to finish:
```

5. For each value entered, validate format and add to metrics file
6. After "done", write updated file and show summary

### Mode 2: Quick Capture

If `$ARGUMENTS` contains a criterion ID and value:
1. Read existing metrics file (or create new)
2. Add/update the metric
3. Write file
4. Confirm: `Recorded P-001 = 82% (threshold: > 80% — exceeded)`

### Mode 3: List (`--list`)

1. Read goals files and metrics file
2. Show all criteria with current values and status
3. Highlight unmeasured criteria

---

## Write Strategy

**READ-MODIFY-WRITE** on `.shipkit/metrics/latest.json`:
- Read existing file (or create if missing)
- Add/update metric entries
- Update `lastUpdated` timestamp
- Update `summary` counts
- Write complete file back

---

## Context Files This Skill Reads

| File | Purpose | If Missing |
|------|---------|------------|
| `.shipkit/goals/product.json` | P-* criteria and thresholds | Accept freeform metrics |
| `.shipkit/goals/engineering.json` | E-* criteria and thresholds | Accept freeform metrics |
| `.shipkit/metrics/latest.json` | Existing measurements | Create new |

## Context Files This Skill Writes

| File | When |
|------|------|
| `.shipkit/metrics/latest.json` | Created on first run, updated on subsequent runs |

---

## When This Skill Integrates with Others

### Before This Skill
| Skill | Why |
|-------|-----|
| `shipkit-product-goals` | Defines P-* criteria with thresholds |
| `shipkit-engineering-goals` | Defines E-* criteria with thresholds |

### After This Skill
| Skill | How |
|-------|-----|
| `shipkit-product-goals --evaluate` | Reads metrics/latest.json to compare actuals vs targets |
| `shipkit-engineering-goals --evaluate` | Same |
| `shipkit-stage --evaluate` | Cross-references all criteria for graduation evidence |

---

<!-- SECTION:after-completion -->
## After Completion

**Suggest next**: Run `/shipkit-product-goals --evaluate` or `/shipkit-engineering-goals --evaluate` to see how actuals compare to targets.
<!-- /SECTION:after-completion -->

<!-- SECTION:success-criteria -->
## Success Criteria

- [ ] At least one metric value recorded
- [ ] File saved to `.shipkit/metrics/latest.json`
- [ ] Each entry has criterionId, value, measuredAt, and source
- [ ] Summary counts match actual entries
<!-- /SECTION:success-criteria -->
