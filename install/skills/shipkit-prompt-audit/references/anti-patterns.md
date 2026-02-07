# Prompt Architecture Anti-Patterns

Common structural problems in LLM-integrated applications. Each anti-pattern includes detection method, severity, and resolution.

---

## 1. God Prompt

**What it is**: A single massive prompt that extracts, analyzes, formats, validates, and decides — all in one LLM call.

**Why it's bad**:
- Unreliable: more tasks = more failure modes in one call
- Hard to debug: which part failed?
- Expensive: can't cache or parallelize sub-tasks
- Fragile: changing one task risks breaking others

**Detection**:
```
Read prompt templates. Look for:
- Multiple distinct instruction sections ("First, extract... Then, analyze... Finally, format...")
- Prompts over ~2000 tokens of instructions
- 3+ unrelated output fields
```

**Severity**: Should Fix

**Resolution**: Decompose into focused single-task prompts chained together. Each prompt has one job with a clear schema.

---

## 2. Sequential Everything

**What it is**: Pipeline stages that run one after another when some could run in parallel.

**Why it's bad**:
- Slow: total latency = sum of all stages
- Wasteful: independent stages wait unnecessarily

**Detection**:
```
In multi-stage pipelines, trace data dependencies:
1. List all stages and their inputs
2. If Stage B doesn't use Stage A's output, they're independent
3. Check for sequential await patterns on independent calls

Grep: pattern="await.*\n.*await" multiline=true
Then verify the awaited calls are AI-related and independent.
```

**Severity**: Should Fix (if 3+ sequential stages with independent pairs)

**Resolution**: Use `Promise.all` for independent stages. Keep sequential only where output feeds input.

**Example**:
```
BAD:  const summary = await summarize(text)
      const sentiment = await classify(text)    // doesn't need summary!
      const keywords = await extract(text)       // doesn't need either!

GOOD: const [summary, sentiment, keywords] = await Promise.all([
        summarize(text),
        classify(text),
        extract(text)
      ])
```

---

## 3. Parse and Pray

**What it is**: Calling `JSON.parse()` on LLM output with no validation, no try/catch, no schema check.

**Why it's bad**:
- LLMs don't guarantee valid JSON
- Even valid JSON may not match expected shape
- Crashes propagate to users as 500 errors

**Detection**:
```
Grep: pattern="JSON\.parse\(" glob="**/*.{ts,tsx,js,jsx}"
Then read context:
- Is it parsing an LLM response?
- Is there a try/catch?
- Is there schema validation (Zod, etc.)?
```

**Severity**: Critical (if used on user-facing paths)

**Resolution**:
1. Use structured output modes (response_format, generateObject) where available
2. Wrap in try/catch
3. Validate with Zod `.safeParse()`
4. Have a fallback for parse/validation failure

---

## 4. Reactive Normalization

**What it is**: Accepting whatever format the LLM returns, then writing normalization code to handle variations.

**Why it's bad**:
- Grows into a sprawling normalization layer
- Each new variation adds more edge-case code
- LLM output shifts with model updates, breaking normalizers

**Detection**:
```
Look for post-processing code near LLM calls:
- String replacements on AI output (.replace, .trim, regex cleanup)
- Multiple if/else branches handling different output shapes
- "Fixing" AI output format after the fact

Grep: pattern="\.replace\(.*\)|\.trim\(\)" near AI call results
Read context to confirm it's cleaning LLM output.
```

**Severity**: Should Fix

**Resolution**: Constrain the output format at the prompt level (structured output, strict schema). Don't clean up — require correctness.

---

## 5. Silent Swallower

**What it is**: Catching errors from LLM calls and silently returning empty/default values without logging or alerting.

**Why it's bad**:
- Failures are invisible
- Stale/empty data propagates through the system
- Users see broken experiences with no error message
- Debugging requires reproducing the exact failure

**Detection**:
```
Grep: pattern="catch.*\{" near AI calls
Then read the catch block:
- Does it log the error?
- Does it return a default/empty value?
- Does it notify the user?

Look for: catch blocks that return {} or [] or null or ""
with no console.error, logging, or monitoring call.
```

**Severity**: Should Fix (Critical if on payment/auth paths)

**Resolution**: Log errors with context (input, model, stage). Return typed error objects. Show user-facing degraded state.

---

## 6. Injection Boulevard

**What it is**: User input injected directly into system prompts or prompt templates with no sanitization.

**Why it's bad**:
- Prompt injection: user can override system instructions
- Data exfiltration: user can extract system prompt
- Behavior manipulation: user can change AI behavior

**Detection**:
```
Trace user input from HTTP request to prompt construction:
1. Find route handlers that accept user input
2. Trace the input to where it's used in a prompt
3. Check:
   - Is it in the system message? (worst)
   - Is it in the user message? (better, but still needs limits)
   - Is there sanitization? (length limits, character filtering)

Grep: pattern="\$\{.*\}" or "f\".*\{.*\}" in files containing system prompts.
Cross-reference with request handlers.
```

**Severity**: Critical

**Resolution**:
1. Always put user input in user messages, never in system
2. Add input length limits
3. Sanitize special characters if needed
4. Consider input/output guardrails

---

## 7. Optional That Should Be Mandatory

**What it is**: Schema defines fields as optional (`.optional()`) but downstream code treats them as required.

**Why it's bad**:
- Runtime crashes when optional fields are absent
- Type system gives false confidence
- LLMs will sometimes omit optional fields

**Detection**:
```
1. Find Zod schemas used for AI output validation
2. List all .optional() fields
3. Trace those fields through downstream code
4. Check if they're accessed without null checks

Grep: pattern="\.optional\(\)" in files with AI-related schemas
Then trace field usage in subsequent code.
```

**Severity**: Should Fix

**Resolution**: If downstream code requires the field, make it required in the schema. If it's truly optional, add null checks everywhere it's used.

---

## 8. Unbounded Map

**What it is**: Mapping over a list with an LLM call per item with no concurrency control.

**Why it's bad**:
- 100 items = 100 concurrent API calls = rate limited
- No progress tracking or partial failure handling
- Single failure can crash the entire batch

**Detection**:
```
Look for:
- .map() with async callback containing AI calls
- Promise.all with unbounded arrays of AI calls
- for...of loops with individual AI calls (sequential but slow)

Grep: pattern="\.map\(async" in files with AI calls
Grep: pattern="Promise\.all\(" near AI call patterns
```

**Severity**: Should Fix

**Resolution**:
1. Add concurrency limiter (p-limit, p-map, or manual semaphore)
2. Add progress tracking
3. Handle partial failures (Promise.allSettled)
4. Consider batching if the API supports it

---

## 9. Task Frame Mismatch

**What it is**: A prompt's task verb ("generate", "create", "suggest") activates pattern-completion mode, when the pipeline actually needs critical analysis, evaluation, or current-knowledge retrieval — or vice versa.

**Why it's bad**:
- "Generate great X" triggers pattern completion from training data (popular, generic, potentially outdated)
- "Evaluate these X for issues" triggers critical analysis and fact-checking
- The model isn't suppressing knowledge — the framing simply doesn't activate the evaluation pathway
- This causes pipelines to produce confidently wrong output that passes schema validation perfectly

**The core insight**: LLMs have different cognitive modes activated by task framing. The same model with the same knowledge will behave differently when asked to "generate activities for Maui" vs "evaluate these activities for Maui given current conditions." Generation mode completes patterns from training data. Evaluation mode activates critical analysis.

**Detection**:
```
Read each prompt template. Check the primary task verb:

GENERATION verbs (pattern completion mode):
  "generate", "create", "suggest", "come up with", "write", "produce", "list"

ANALYSIS verbs (critical evaluation mode):
  "evaluate", "review", "check", "verify", "assess", "analyze", "identify issues"

RESEARCH verbs (knowledge retrieval mode):
  "research", "what are the current conditions", "what has changed", "investigate"

Then ask: Does the verb match what the pipeline NEEDS from this stage?

Common mismatch: An early "intelligence gathering" stage uses generation
verbs ("generate a summary of X") instead of research verbs ("what are
the current conditions, risks, and constraints for X?"). Downstream
stages then operate on pattern-completed content, not actual knowledge.
```

**Severity**: Should Fix (Critical if the pipeline makes real-world recommendations — travel, health, legal, financial)

**Resolution**:
1. Map each pipeline stage to its intended cognitive mode (generate / evaluate / research)
2. Ensure the task verb matches the intended mode
3. For early "intelligence" stages: frame as research/investigation, not generation
4. For quality gates: frame as evaluation/review, not summarization
5. Small reframe at an upstream stage often eliminates the need for bolted-on negative constraints downstream

**Example**:
```
BAD (generation mode — will reproduce popular pre-disaster Maui content):
  "Generate the best activities and venues for a trip to Maui"

BETTER (research mode — activates current-knowledge retrieval):
  "Research current conditions in Maui. What areas are affected by
   recent events? What is open/closed? What should travelers know?"

Then feed that knowledge into downstream stages that generate recommendations.
```

---

## 10. Upstream Knowledge Gap

**What it is**: A multi-stage pipeline has an early "intelligence" or "research" stage that fails to surface critical context because it asks the wrong questions — causing all downstream stages to operate on incomplete information.

**Why it's bad**:
- Downstream stages can't compensate for what upstream didn't surface
- Adding constraints downstream ("don't recommend X") is fragile and reactive
- The root cause is the upstream prompt's question framing, not downstream filtering
- Creates a false sense of safety: the pipeline "works" but produces subtly wrong output

**Detection**:
```
In multi-stage pipelines, identify the earliest "context gathering" stage:
1. What questions does it ask? (attractions? culture? → misses current conditions)
2. What does it NOT ask? (closures? recent events? safety concerns?)
3. Do downstream stages have negative constraints that compensate?
   - "Don't recommend X" or "Exclude Y" → likely papering over upstream gap
4. Would a small reframe of the upstream prompt eliminate the need
   for downstream constraints?
```

**Severity**: Should Fix (Critical for recommendation/advisory pipelines)

**Resolution**:
1. Audit what the earliest knowledge-gathering stage actually asks for
2. Add "current conditions" / "risks" / "constraints" to its question framing
3. Remove downstream negative constraints that were compensating for the gap
4. Principle: Fix the source of knowledge, not the consumers of it
