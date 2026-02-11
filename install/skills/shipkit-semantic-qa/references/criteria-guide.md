# Writing Effective Quality Criteria

Quality criteria are the core of semantic QA. They tell Claude what "good" means for your specific project. Well-written criteria produce consistent, actionable judgments. Vague criteria produce vague results.

## Criteria Format

```json
{
  "id": "SQ-001",
  "name": "Short name",
  "description": "What this criterion checks",
  "weight": "must-pass",
  "evaluationGuide": "Specific instructions for HOW to judge",
  "passExample": "What passing looks like (optional)",
  "failExample": "What failing looks like (optional)"
}
```

## Weight Levels

| Weight | Meaning | Effect on Score |
|--------|---------|-----------------|
| `must-pass` | Failing this blocks quality gate | Overall = FAIL if any must-pass fails |
| `important` | Strongly recommended | Drags score significantly |
| `nice-to-have` | Noted but not blocking | Minor score impact |

## The `evaluationGuide` Field

This is the most important field. It tells Claude exactly how to evaluate — not just what to look for, but what constitutes pass vs fail.

**Good guides are specific and binary:**
- "Check if all required fields (title, body, metadata) are present in the JSON response. Missing any required field = FAIL. Extra fields = PASS."
- "Verify no prices or quantities in the output differ from the input data. Any fabricated number = FAIL."
- "Check for horizontal scrolling or text overflow at this viewport. Any content cut off = FAIL."

**Bad guides are subjective:**
- "Output should be good quality" (what does good mean?)
- "Response should be helpful" (helpful to whom?)
- "UI should look nice" (by whose standards?)

## Backend Criteria Examples

### Data Quality
| Criterion | Guide |
|-----------|-------|
| Factual Accuracy | Cross-reference numbers/claims against input data. Any fabricated or contradicted value = FAIL |
| Completeness | Check all required output fields populated. Null/empty required field = FAIL |
| Format Compliance | Parse as expected format (JSON/CSV/etc). Invalid parse = FAIL, missing schema fields = PARTIAL |
| No Hallucination | Output must only contain information derivable from input. Novel claims not in source = FAIL |

### LLM Pipeline Quality
| Criterion | Guide |
|-----------|-------|
| Response Relevance | Output must address the input query topic. Off-topic content = FAIL |
| Instruction Following | Check each instruction in the prompt was followed. Missed instruction = PARTIAL per miss |
| Safety | No PII leakage, no harmful content, no prompt injection in output. Any occurrence = FAIL |
| Consistency | Run same input twice — outputs should be substantively equivalent. Major divergence = FAIL |

## Frontend Criteria Examples

### Layout & Visual
| Criterion | Guide |
|-----------|-------|
| No Overflow | No text truncation, no horizontal scroll, no elements extending beyond container. Any overflow = FAIL |
| Spacing Consistency | Padding/margins should be uniform across similar elements. Visible inconsistency = FAIL |
| Data Rendering | All mock data values visible and correctly formatted. Missing or garbled data = FAIL |
| Empty State | Components with no data show intentional empty state, not blank space or errors. Blank = FAIL |

### Responsive
| Criterion | Guide |
|-----------|-------|
| Mobile Layout | At 375px width: no horizontal scroll, readable text (≥14px equivalent), tap targets ≥44px. Violation = FAIL |
| Tablet Layout | At 768px: layout adapts (not just shrunk desktop). No adaptation = PARTIAL |
| Desktop Layout | At 1280px: content doesn't stretch beyond readable width. No max-width constraint = PARTIAL |

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| "Should be good" | Unquantifiable | Define what "good" means specifically |
| "Match exact format" | Too brittle, breaks on minor changes | Check structural requirements, not exact text |
| "Be fast" | Semantic QA judges quality, not performance | Use performance tests for speed |
| "No bugs" | Too broad, not observable from output alone | Check specific observable behaviors |
| Combining multiple checks | Hard to diagnose which part failed | One concern per criterion |
