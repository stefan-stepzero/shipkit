# Prompt Architecture Audit Checklist

Detailed checks per dimension with IDs, severity, scan methods, and pass criteria.

---

## Dimension 1: Decomposition (PA-DEC)

> Is each prompt focused on one task, or doing too much?

### PA-DEC-001: God Prompt Detection
**Severity**: Should Fix
**Scan**: Read each prompt template. Count distinct instructions/tasks.
**Pass**: Prompt handles 1-2 related tasks
**Fail**: Prompt handles 3+ unrelated tasks (extract, analyze, format, validate in one call)
**Fix**: Break into focused sub-prompts with clear input/output contracts

### PA-DEC-002: Mixed Concerns
**Severity**: Should Fix
**Scan**: Check if prompts mix data extraction with formatting, or analysis with action.
**Pass**: Each prompt has a single responsibility
**Fail**: Same prompt extracts data AND formats output AND makes decisions
**Fix**: Separate into extraction stage + formatting stage

### PA-DEC-003: Decomposition Opportunity
**Severity**: Minor
**Scan**: Check prompt token count (estimate from template length). Prompts over ~2000 tokens are candidates.
**Pass**: Prompts are concise and focused
**Fail**: Large prompts that could be split for reliability
**Fix**: Identify independent sections that could be separate calls

---

## Dimension 2: Parallelization (PA-PAR)

> Are independent operations running concurrently?

### PA-PAR-001: Sequential Independent Calls
**Severity**: Should Fix
**Scan**: In multi-stage pipelines, check if stages with no data dependency run sequentially.
**Pass**: Independent stages use Promise.all or equivalent
**Fail**: Sequential `await` for calls that don't depend on each other
**Example**: Summarize + classify run sequentially but share only the original input
**Fix**: Wrap independent calls in Promise.all

### PA-PAR-002: Fan-Out Opportunity
**Severity**: Minor
**Scan**: Check for loops that call LLMs sequentially (e.g., `for...of` with `await` inside).
**Pass**: Batch processing uses parallelism with concurrency control
**Fail**: Sequential loop over items with individual LLM calls
**Fix**: Use Promise.all with concurrency limiter (e.g., p-limit)

### PA-PAR-003: Unnecessary Data Dependencies
**Severity**: Minor
**Scan**: Trace data flow between stages. Check if full output is passed when only a subset is needed.
**Pass**: Each stage receives only what it needs
**Fail**: Full previous output passed when only one field is used
**Fix**: Extract needed fields before passing to next stage

---

## Dimension 3: Schema Tightness (PA-SCH)

> Is LLM output validated before use?

### PA-SCH-001: Unvalidated JSON Parse
**Severity**: Critical
**Scan**: `Grep: pattern="JSON\.parse\(" → Read context → Check for try/catch and schema validation`
**Pass**: JSON.parse wrapped in try/catch with schema validation (Zod, etc.)
**Fail**: Raw JSON.parse on LLM output with no validation
**Fix**: Add Zod schema + parse with `.safeParse()`

### PA-SCH-002: No Structured Output Mode
**Severity**: Should Fix
**Scan**: Check if API calls requesting JSON use structured output features (response_format, generateObject).
**Pass**: Uses provider's structured output mode where available
**Fail**: Relies on prompt instructions alone for JSON format
**Fix**: Use `response_format: { type: "json_schema" }` (OpenAI) or `generateObject` (Vercel AI)

### PA-SCH-003: Schema-Response Mismatch
**Severity**: Critical
**Scan**: Compare Zod/TypeScript schema with what the prompt asks for.
**Pass**: Schema matches prompt instructions exactly
**Fail**: Schema expects fields the prompt doesn't mention, or vice versa
**Fix**: Align prompt instructions with validation schema

### PA-SCH-004: Optional Fields That Should Be Required
**Severity**: Should Fix
**Scan**: Check Zod schemas for `.optional()` on fields the pipeline requires downstream.
**Pass**: Required downstream fields are required in schema
**Fail**: Fields used in later stages are marked optional
**Fix**: Make downstream-required fields required in schema

---

## Dimension 4: Chain Integrity (PA-CHN)

> Does data flow correctly between pipeline stages?

### PA-CHN-001: Unchecked Stage Output
**Severity**: Critical
**Scan**: Between pipeline stages, check if output of stage N is validated before becoming input of stage N+1.
**Pass**: Each stage output is validated or type-checked before next stage
**Fail**: Raw output passed directly to next prompt with no checking
**Fix**: Add validation between stages

### PA-CHN-002: Silent Stage Failure
**Severity**: Critical
**Scan**: Check if a stage can return null/undefined/empty and whether the next stage handles it.
**Pass**: Empty/null results are caught and handled before next stage
**Fail**: Next stage will receive undefined and produce garbage output
**Fix**: Add null checks and early exit or fallback between stages

### PA-CHN-003: Type Narrowing Between Stages
**Severity**: Should Fix
**Scan**: Check if TypeScript types are maintained across pipeline stages.
**Pass**: Types are consistent and narrowed between stages
**Fail**: `any` types between stages, or type assertions without validation
**Fix**: Use typed interfaces for inter-stage data

---

## Dimension 5: Cache Boundaries (PA-CAC)

> Are deterministic or expensive calls cached?

### PA-CAC-001: Repeated Identical Calls
**Severity**: Should Fix
**Scan**: Check for LLM calls with the same prompt template and static inputs called multiple times.
**Pass**: Deterministic calls are cached (in-memory, Redis, etc.)
**Fail**: Same prompt+input called repeatedly with no caching
**Fix**: Add memoization or cache layer for deterministic prompts

### PA-CAC-002: Expensive Stage Without Memoization
**Severity**: Minor
**Scan**: Identify pipeline stages that use large models (GPT-4, Claude Opus) with stable inputs.
**Pass**: Expensive stages cache results where input is deterministic
**Fail**: Every request hits the expensive model even for repeated queries
**Fix**: Add cache with appropriate TTL

### PA-CAC-003: No Cache Invalidation
**Severity**: Minor
**Scan**: If caching exists, check for invalidation logic.
**Pass**: Cache has TTL or explicit invalidation on data changes
**Fail**: Cache exists but never invalidates (stale results forever)
**Fix**: Add TTL or event-based cache invalidation

---

## Dimension 6: Fallback Paths (PA-FBK)

> What happens when things go wrong?

### PA-FBK-001: No Error Handling on AI Call
**Severity**: Critical
**Scan**: Check each AI API call for try/catch or .catch().
**Pass**: Every AI call has error handling
**Fail**: Bare await with no try/catch
**Fix**: Add try/catch with appropriate error handling

### PA-FBK-002: No Retry Logic
**Severity**: Should Fix
**Scan**: Check for retry mechanisms on AI calls.
**Pass**: Transient failures (429, 500, timeout) trigger retries with backoff
**Fail**: Single attempt, failure is final
**Fix**: Add retry with exponential backoff (most SDKs have built-in options)

### PA-FBK-003: No Degraded Experience
**Severity**: Should Fix
**Scan**: Check if AI failure results in user-facing error or graceful degradation.
**Pass**: AI failure shows fallback content or cached result
**Fail**: AI failure = blank page or error message
**Fix**: Add fallback path (cached result, simpler model, static content)

### PA-FBK-004: Rate Limit Handling
**Severity**: Should Fix
**Scan**: `Grep: pattern="429\|rate.limit\|RateLimitError\|too.many.requests"`
**Pass**: Rate limits are caught and handled (queue, backoff, or user message)
**Fail**: Rate limit errors crash the request
**Fix**: Add rate limit detection with backoff or queuing

---

## Dimension 7: Context Efficiency (PA-CTX)

> Are prompts lean and efficient with tokens?

### PA-CTX-001: Duplicated Context Across Stages
**Severity**: Should Fix
**Scan**: In multi-stage pipelines, check if the same context (system prompt, examples) is repeated.
**Pass**: Shared context extracted, each stage gets only what it needs
**Fail**: Same 500-token system prompt in every stage of a 5-stage pipeline
**Fix**: Extract shared context; pass only stage-specific instructions

### PA-CTX-002: Entire Document in Prompt
**Severity**: Should Fix
**Scan**: Check for large string interpolation into prompts (full documents, entire files).
**Pass**: Uses chunking, summarization, or RAG for large content
**Fail**: Entire document crammed into single prompt
**Fix**: Implement chunking or RAG; summarize if full content not needed

### PA-CTX-003: Token Limit Awareness
**Severity**: Should Fix
**Scan**: Check if prompt construction accounts for token limits.
**Pass**: Prompt size is checked or bounded before sending
**Fail**: No size checking; will fail silently when context is too large
**Fix**: Add token estimation and truncation/chunking logic

---

## Dimension 8: Constraint Precision (PA-CON)

> Are output instructions clear and testable?

### PA-CON-001: Vague Output Instructions
**Severity**: Minor
**Scan**: Read prompt templates for output format instructions.
**Pass**: Explicit format instructions ("Return JSON with fields: name (string), score (number 1-10)")
**Fail**: Vague instructions ("Return the result in a nice format")
**Fix**: Add explicit format specifications with types and constraints

### PA-CON-002: Missing Examples for Complex Formats
**Severity**: Minor
**Scan**: Check if prompts requesting complex structured output include examples.
**Pass**: Complex formats have 1-2 examples
**Fail**: Expects complex nested JSON with no example
**Fix**: Add a few-shot example showing expected output shape

---

## Dimension 9: Input Safety (PA-INP)

> Is user input handled safely?

### PA-INP-001: Direct User Input in Prompt
**Severity**: Critical
**Scan**: Trace user input from request to prompt template. Check for sanitization.
**Pass**: User input is sanitized, length-limited, and placed in user message (not system)
**Fail**: Raw user input interpolated directly into system prompt
**Fix**: Move user input to user message; sanitize; add length limits

### PA-INP-002: No Input Length Limits
**Severity**: Should Fix
**Scan**: Check if user-provided text has length validation before prompt construction.
**Pass**: Input is truncated or rejected if too long
**Fail**: Unlimited user input passed to prompt (token bomb risk)
**Fix**: Add input length validation

### PA-INP-003: System/User Boundary
**Severity**: Should Fix
**Scan**: Check if system instructions and user content are properly separated.
**Pass**: System prompt in system role, user content in user role
**Fail**: User content injected into system message, or all in one message
**Fix**: Separate system instructions from user-provided content

---

## Dimension 10: Reference Integrity (PA-REF)

> Do prompts reference things that actually exist?

### PA-REF-001: Hardcoded Model References
**Severity**: Minor
**Scan**: `Grep: pattern="gpt-3\.5\|gpt-4-0613\|claude-2\|claude-instant" glob="**/*.{ts,tsx,js,jsx,py}"`
**Pass**: Model names are configurable or use latest aliases
**Fail**: Hardcoded model names that may be deprecated
**Fix**: Use environment variables or configuration for model selection

### PA-REF-002: Stale Few-Shot Examples
**Severity**: Minor
**Scan**: Check if few-shot examples in prompts reference current data formats.
**Pass**: Examples match current schema and data shapes
**Fail**: Examples reference fields or formats that no longer exist
**Fix**: Update examples to match current data structures

### PA-REF-003: Deprecated API Usage
**Severity**: Should Fix
**Scan**: Check for deprecated SDK methods or API endpoints.
**Pass**: Uses current API methods
**Fail**: Uses deprecated completion endpoints, old chat formats, etc.
**Fix**: Migrate to current API versions
