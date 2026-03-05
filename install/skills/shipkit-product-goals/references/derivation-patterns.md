# Product Criteria Derivation Patterns

This reference shows how to derive measurable user-outcome criteria (P-*) from `product-definition.json` (features, patterns, differentiators). The `/shipkit-product-goals` skill uses these patterns to propose criteria — users validate thresholds.

**Philosophy:** Every feature, UX pattern, and differentiator implies criteria for "how do we know this works?" These patterns make that derivation explicit.

> **Business metrics** (S-* criteria) are handled by `/shipkit-stage`.
> **Engineering criteria** (E-* criteria) are handled by `/shipkit-engineering-goals`.

---

## Pattern 1: UX Pattern → Usability + Completion + Responsiveness Criteria

Each UX pattern in `product-definition.json` implies criteria about the user experience:

### Usability: Can users complete the flow?

| Pattern Type | Typical Criterion | Typical Threshold |
|-------------|-------------------|-------------------|
| Wizard/multi-step flow | Task completion time | < 2 minutes for core flow |
| Search/filter interface | Time to find target item | < 30 seconds |
| Settings/configuration | Successful configuration rate | > 95% without support |
| Onboarding flow | First-success-moment time | < 5 minutes |

### Completion Rate: What percentage finish?

| Pattern Type | Typical Criterion | Typical Threshold |
|-------------|-------------------|-------------------|
| Wizard/multi-step flow | Overall completion rate | > 80% who start, finish |
| Signup/onboarding | Conversion rate | > 60% complete onboarding |
| Checkout flow | Cart-to-purchase rate | > 30% (industry varies) |
| Form submission | Form completion rate | > 90% |

### Responsiveness: How fast does it feel?

| Pattern Type | Typical Criterion | Typical Threshold |
|-------------|-------------------|-------------------|
| Live preview | Preview update latency | < 500ms after input change |
| Real-time collaboration | Sync visibility | < 1 second |
| Drag-and-drop | Interaction responsiveness | < 100ms visual feedback |
| Search-as-you-type | Results appearance | < 300ms after keystroke |

---

## Pattern 2: Differentiator → Validation Criteria

Each differentiator in `product-definition.json` is a claim about what makes the product unique. Criteria verify the claim holds:

### Functional Validation: Does it actually work as claimed?

Ask: "Can we prove this differentiator delivers on its promise?"

**Example:**
```
Differentiator: "Adaptive difficulty that creates differentiated sets" (D-001)
→ Criterion: "Differentiation works"
  Metric: "Generated difficulty variants are measurably different in complexity"
  Threshold: "Readability scores differ by > 2 grade levels between variants"
  Verification: automated-test (readability analysis)
```

### User Perception: Do users notice/value it?

Ask: "Do users recognize this as valuable compared to alternatives?"

**Example:**
```
Differentiator: "Real-time preview with streaming output" (D-003)
→ Criterion: "Preview perceived as fast"
  Metric: "User satisfaction with generation speed"
  Threshold: "> 80% rate generation speed as 'fast' or 'acceptable'"
  Verification: user-feedback (in-app survey)
```

---

## Pattern 3: Features → Completeness + Integration Gates

The `features` array in `product-definition.json` defines what the product does. Goals assigns features to stage gates:

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

## Checkability Classification

| Criterion Type | Default Checkability | Default Verification Tool | Rationale |
|---------------|---------------------|--------------------------|-----------|
| Responsiveness (UI speed) | `verifiable` | `visual-qa` | Playwright can measure render times |
| Flow completion (E2E works) | `verifiable` | `visual-qa` | Playwright can complete the flow |
| Completion rate (% of users) | `observable` | `none` | Needs real user funnel data |
| Completion time (how fast users go) | `observable` | `none` | Needs real user behavior data |
| Page rendering | `verifiable` | `visual-qa` | Playwright can visit and screenshot |
| Differentiator validation (functional) | `verifiable` | `semantic-qa` | Can test the differentiating behavior |
| User perception (users notice/value) | `observable` | `none` | Subjective, needs real feedback |
| Feature completeness (E2E smoke test) | `verifiable` | `visual-qa` | Playwright runs E2E for each feature |
| Feature integration (features work together) | `verifiable` | `visual-qa` | E2E tests across feature boundaries |

### Key Distinction

| Seems Observable | Actually Verifiable | How |
|-----------------|--------------------|----|
| "Users can complete the wizard" | "Wizard flow works E2E" | Playwright simulates the flow |
| "Content is grade-appropriate" | "Output matches rubric" | Semantic QA judges against criteria |
| "Export produces valid PDFs" | "PDF generation succeeds" | Visual QA triggers export, checks output |
| "Preview feels responsive" | "Preview update < 500ms" | Playwright measures timing |

**When uncertain**: default to `observable`. Safer to under-promise.

---

## Stage-Appropriate Criteria Complexity

| Stage | Product Criteria Focus | Count |
|-------|----------------------|-------|
| POC | "Core flow completable" | 2-3 |
| Alpha | Core usability + basic completeness | 3-5 |
| MVP | User outcomes + completion rates | 5-10 |
| Scale | Full UX quality + satisfaction + growth | 10-15 |
