# Engineering Criteria Derivation Patterns

This reference shows how to derive measurable technical performance criteria from `engineering-definition.json` (mechanisms, components, design decisions). The `/shipkit-engineering-goals` skill uses these patterns to propose criteria — users validate thresholds.

**Philosophy:** Every mechanism implies criteria for "how do we know this performs?" These patterns make that derivation explicit.

> **Product and strategic criteria** (UX patterns, differentiators, business metrics) are handled by `/shipkit-product-goals`. See that skill's `references/derivation-patterns.md`.

---

## Pattern 1: Mechanism → Performance + Quality + Reliability Criteria

Each mechanism in `engineering-definition.json` implies three types of criteria:

### Performance: How fast?

Ask: "What's the acceptable speed for this mechanism?"

| Mechanism Type | Typical Criterion | Typical Threshold |
|---------------|-------------------|-------------------|
| LLM/AI pipeline | Generation/response time | < 5 seconds for first content |
| Search/query engine | Query response time | < 500ms for 95th percentile |
| Data processing pipeline | Processing throughput | N items per second/minute |
| Real-time sync | Sync latency | < 1 second for updates |
| File generation (PDF, etc.) | Generation time | < 10 seconds for standard size |

**Example derivation:**
```
Mechanism: "LLM Generation Chain" (M-001)
→ Criterion: "Generation speed"
  Metric: "Time from submit to first streamed content"
  Threshold: "< 5 seconds"
  Verification: automated-test (load test with timer)
```

### Quality: How good is the output?

Ask: "How do we verify the mechanism produces correct/useful results?"

| Mechanism Type | Typical Criterion | Typical Threshold |
|---------------|-------------------|-------------------|
| LLM/AI pipeline | Output accuracy/relevance | > 90% on human review sample |
| Recommendation engine | Recommendation relevance | Click-through rate > 15% |
| Matching algorithm | Match quality | > 85% user-confirmed matches |
| Content generation | Content appropriateness | < 5% flagged as inappropriate |
| Data transformation | Data accuracy | 100% for critical fields |

**Example derivation:**
```
Mechanism: "LLM Generation Chain" (M-001)
→ Criterion: "Content quality"
  Metric: "Grade-appropriateness of generated questions"
  Threshold: "> 90% accuracy on manual review of 20 samples"
  Verification: manual-check (teacher review) → semantic-qa (Claude judges)
```

### Reliability: How often does it work?

Ask: "What failure rate is acceptable for this mechanism?"

| Mechanism Type | Typical Criterion | Typical Threshold |
|---------------|-------------------|-------------------|
| LLM/AI pipeline | Completion rate (no errors) | > 99% of requests succeed |
| External API integration | Uptime / availability | > 99.5% over 30 days |
| Background job | Job success rate | > 99.9% of jobs complete |
| Real-time feature | Connection stability | < 1% dropped connections |

**Example derivation:**
```
Mechanism: "LLM Generation Chain" (M-001)
→ Criterion: "Generation reliability"
  Metric: "Percentage of generation requests that complete without error"
  Threshold: "> 99%"
  Verification: analytics (error rate tracking)
```

---

## Pattern 2: Infrastructure Criteria (Always Include)

These are stage-gated — always propose at or above MVP:

| Criterion | Threshold | Checkability | Tool |
|-----------|-----------|-------------|------|
| Build compiles | 0 errors | `verifiable` | `build` |
| Test suite passes | 0 failures | `verifiable` | `test` |
| Lint clean | 0 warnings | `verifiable` | `lint` |
| CI pipeline passes | Green on all checks | `verifiable` | `build` |

---

## Checkability Classification

### Engineering Criteria

| Criterion Type | Default Checkability | Default Verification Tool | Rationale |
|---------------|---------------------|--------------------------|-----------|
| Performance (speed) | `verifiable` | `semantic-qa` | Script can time API calls and pipelines |
| Quality (output correctness) | `verifiable` | `semantic-qa` | Claude can judge output against rubric |
| Reliability (error rate) | `observable` | `none` | Needs sustained production traffic |
| Build health | `verifiable` | `build` | Build command exits 0 or not |
| Test coverage | `verifiable` | `test` | Test suite passes or not |
| Lint compliance | `verifiable` | `lint` | Lint exits 0 or not |

### Key Distinction

| Seems Observable | Actually Verifiable | How |
|-----------------|--------------------|----|
| "API is fast enough" | "API responds in < 500ms" | Timed test request |
| "Output quality is good" | "Output matches rubric" | Semantic QA judges against criteria |
| "System handles load" | "10 concurrent requests succeed" | Load test script |

The distinction: "API responds in < 500ms in test" = verifiable. "p95 latency < 500ms under production load for 30 days" = observable.

**When uncertain**: default to `observable`. Safer to under-promise.

---

## Stage-Appropriate Criteria Complexity

| Stage | Engineering Focus | Typical Count | Threshold Rigor |
|-------|------------------|---------------|-----------------|
| POC | "It compiles" — build passes | 1-3 criteria | Binary |
| Alpha | "It works" — happy path tests, basic perf | 3-6 criteria | Rough thresholds |
| MVP | "It performs" — response times, coverage, CI | 6-12 criteria | Quantitative |
| Scale | "It scales" — SLAs, p99, load tests, MTTR | 12-20 criteria | Comprehensive with baselines |
