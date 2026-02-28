# Criteria Derivation Patterns

This reference shows how to derive measurable success criteria from `product-definition.json` (features, patterns, differentiators) and `engineering-definition.json` (mechanisms, components). The `/shipkit-goals` skill uses these patterns to propose criteria — users validate thresholds and add business metrics.

**Philosophy:** Every feature, mechanism, pattern, and differentiator implies criteria for "how do we know this works?" These patterns make that derivation explicit.

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
  Verification: manual-check (teacher review)
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

## Pattern 2: UX Pattern → Usability + Completion + Responsiveness Criteria

Each UX pattern in `product-definition.json` implies criteria about the user experience (mechanisms come from `engineering-definition.json`):

### Usability: Can users complete the flow?

Ask: "Can a new user complete this flow without help?"

| Pattern Type | Typical Criterion | Typical Threshold |
|-------------|-------------------|-------------------|
| Wizard/multi-step flow | Task completion time | < 2 minutes for core flow |
| Search/filter interface | Time to find target item | < 30 seconds |
| Settings/configuration | Successful configuration rate | > 95% without support |
| Onboarding flow | First-success-moment time | < 5 minutes |

**Example derivation:**
```
Pattern: "Wizard Flow" (P-001)
→ Criterion: "Wizard completion time"
  Metric: "Time from wizard start to worksheet preview"
  Threshold: "80% of users complete in < 2 minutes"
  Verification: analytics (time-to-complete tracking)
```

### Completion Rate: What percentage finish?

Ask: "What dropout rate is acceptable at each step?"

| Pattern Type | Typical Criterion | Typical Threshold |
|-------------|-------------------|-------------------|
| Wizard/multi-step flow | Overall completion rate | > 80% who start, finish |
| Signup/onboarding | Conversion rate | > 60% complete onboarding |
| Checkout flow | Cart-to-purchase rate | > 30% (industry varies) |
| Form submission | Form completion rate | > 90% |

**Example derivation:**
```
Pattern: "Wizard Flow" (P-001)
→ Criterion: "Wizard completion rate"
  Metric: "Percentage of users who start the wizard and reach export"
  Threshold: "> 80%"
  Verification: analytics (funnel tracking)
```

### Responsiveness: How fast does it feel?

Ask: "What perceived speed is acceptable for interactions in this pattern?"

| Pattern Type | Typical Criterion | Typical Threshold |
|-------------|-------------------|-------------------|
| Live preview | Preview update latency | < 500ms after input change |
| Real-time collaboration | Sync visibility | < 1 second |
| Drag-and-drop | Interaction responsiveness | < 100ms visual feedback |
| Search-as-you-type | Results appearance | < 300ms after keystroke |

**Example derivation:**
```
Pattern: "Live Preview" (P-002)
→ Criterion: "Preview responsiveness"
  Metric: "Time from parameter change to preview update"
  Threshold: "< 500ms for non-generation changes"
  Verification: automated-test (UI performance test)
```

---

## Pattern 3: Differentiator → Validation Criteria

Each differentiator in `product-definition.json` is a claim about what makes the product unique. Criteria verify the claim holds (mechanisms that enable differentiators are in `engineering-definition.json`):

### Functional Validation: Does it actually work as claimed?

Ask: "Can we prove this differentiator delivers on its promise?"

**Example derivation:**
```
Differentiator: "Adaptive difficulty that creates differentiated sets" (D-001)
→ Criterion: "Differentiation works"
  Metric: "Generated difficulty variants are measurably different in complexity"
  Threshold: "Readability scores differ by > 2 grade levels between variants"
  Verification: automated-test (readability analysis)
```

### User Perception: Do users notice/value it?

Ask: "Do users recognize this as valuable compared to alternatives?"

**Example derivation:**
```
Differentiator: "Real-time preview with streaming output" (D-003)
→ Criterion: "Preview perceived as fast"
  Metric: "User satisfaction with generation speed"
  Threshold: "> 80% rate generation speed as 'fast' or 'acceptable'"
  Verification: user-feedback (in-app survey)
```

---

## Pattern 4: Features → Completeness + Integration Gates

The `features` array in `product-definition.json` defines what the product does. Goals assigns features to stage gates (phasing). For each gate, derive completeness and integration criteria:

### Completeness Gate: Are all gate-scoped features functional?

```
Features assigned to gate
→ Criterion: "Gate feature completeness"
  Metric: "All gate-scoped features functional end-to-end"
  Threshold: "100% of gate features pass smoke test"
  Verification: manual-check (feature walkthrough checklist)
```

### Integration Gate: Do features work together?

```
Features with dependencies
→ Criterion: "Feature integration"
  Metric: "Core user flow works across gate features"
  Threshold: "Complete user journey (create → preview → export) works"
  Verification: automated-test (end-to-end test suite)
```

---

## Stage-Appropriate Criteria Complexity

The project stage (from `product-definition.json` or `why.json`) determines how rigorous criteria should be:

| Stage | Criteria Focus | Typical Count | Threshold Rigor |
|-------|---------------|---------------|-----------------|
| POC | "It works" — functional checks | 3-5 criteria | Binary (works/doesn't) |
| MVP | User outcomes + core performance | 8-15 criteria | Measurable thresholds |
| Production | Performance + reliability + quality gates | 15-25 criteria | Quantitative with SLAs |
| Scale | Business metrics + operational excellence | 20-40 criteria | Comprehensive with baselines |

### POC Example Criteria
- Mechanism works end-to-end (binary)
- Output is reasonable quality (manual review)
- Core flow completable (user can do the thing)

### MVP Example Criteria
- Mechanism performs within threshold (< 5s)
- Output quality meets standard (> 90% accuracy)
- Users complete flow efficiently (< 2 min, > 80% completion)
- Return usage indicates value (> 40% 7-day return)

### Production Example Criteria
- All MVP criteria, plus:
- 99th percentile performance (< 10s under load)
- Reliability SLA (> 99.5% uptime)
- Error recovery (graceful degradation, retry logic)
- Security gates (auth hardened, input validation complete)

### Scale Example Criteria
- All Production criteria, plus:
- Business metrics (conversion, retention, NPS)
- Operational metrics (incident response time, MTTR)
- Per-tenant performance (multi-tenancy doesn't degrade)

---

## Composing Stage Gates

After deriving individual criteria, group them into named gates:

### Common Gate Patterns

**MVP Launch Ready** (all must pass before launch):
- All user-outcome criteria from core UX patterns
- All technical-performance criteria from core mechanisms
- MVP completeness and integration criteria

**Beta Ready** (MVP Launch + these):
- User satisfaction criteria from differentiators
- Business metrics with initial thresholds
- Reliability criteria

**Production Ready** (Beta + these):
- Performance under load criteria
- Security criteria
- Operational readiness criteria

**Growth Ready** (Production + these):
- Retention and engagement criteria
- Scalability criteria
- Business model criteria

---

## Using This Reference

The `/shipkit-goals` skill should:

1. **Read product-definition.json** — extract features, uxPatterns, differentiators
1b. **Read engineering-definition.json** — extract mechanisms, components
2. **For each mechanism** — derive performance + quality + reliability criteria (Pattern 1)
3. **For each UX pattern** — derive usability + completion + responsiveness criteria (Pattern 2)
4. **For each differentiator** — derive validation criteria (Pattern 3)
5. **From features** — derive completeness + integration criteria per gate (Pattern 4)
6. **Assign features to gates** — determine phasing (now/next/later)
7. **Adjust complexity** — based on project stage
7. **Propose to user** — with suggested thresholds from this reference
8. **Group into gates** — based on common gate patterns above
9. **Let user customize** — adjust thresholds, add business metrics, modify gate composition

**Remember:** These patterns suggest starting points. Users bring domain expertise about what thresholds matter for their specific context.
