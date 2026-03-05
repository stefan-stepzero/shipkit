# Termination Protocol

Exit when the shipping loop reports complete (all verifiable criteria passing across all 3 goal files). Observable criteria at `not-measured` do NOT block exit.

## Exit Sequence

1. Run `/shipkit-work-memory` to persist session state
2. Generate termination report:

```
ORCHESTRATION COMPLETE

Verifiable criteria: {N}/{N} passing
Observable criteria: {M} awaiting real data

Verified (done):
  ✓ E-001: Build passes [build]
  ✓ E-002: Tests pass [test]
  ✓ P-003: Checkout flow completes E2E [visual-qa]

Awaiting data:
  ◌ S-001: DAU > 100 [needs analytics after launch]
  ◌ P-001: Completion rate > 80% [needs real user funnel]

Next steps for human:
  1. Deploy to staging/production
  2. Set up analytics for observable criteria
  3. Re-run /shipkit-product-goals --evaluate after collecting data
```

3. **Stop** — do not re-dispatch agents after termination

## Verifiable vs Observable

**Verifiable criteria** (`checkability: "verifiable"`):
- Can be checked by tools (build, test, lint, visual-qa)
- Drive dispatching and termination
- `not-measured` or `below-threshold` → needs work
- `at-threshold` or `exceeded` → passing

**Observable criteria** (`checkability: "observable"`):
- Need real-world data (DAU, retention, revenue)
- Do NOT drive dispatching or block termination
- `not-measured` → awaiting real data (expected)
- `below-threshold` → may need adjustment (only if data exists)
