---
name: shipkit-prompt-audit
description: Audit LLM prompt pipeline architecture — decomposition, parallelization, chain integrity, schema validation, fallback paths. Finds structural issues no linter catches.
argument-hint: "[scope or directory]"
model: opus
context: fork
agent: shipkit-reviewer-agent
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# shipkit-prompt-audit - LLM Prompt Architecture Audit

**Purpose**: Find structural problems in how your app talks to LLMs — monolithic prompts, missing fallbacks, sequential bottlenecks, unvalidated outputs, unsafe inputs.

**What this is NOT**: Not a prompt text quality checker. Not "make this prompt better." This audits the **engineering architecture** around prompts — how they're decomposed, chained, validated, and recovered from failure.

---

## When to Invoke

- `/shipkit-prompt-audit` — audit all LLM integrations
- `/shipkit-prompt-audit src/ai/` — focus on specific directory
- "Audit my prompts", "Check prompt architecture", "LLM pipeline review"
- "Are my AI calls structured well?"
- "Check my prompts for anti-patterns"

**Workflow position**:
- After implementing AI features, before shipping
- When AI features feel slow or unreliable
- During architecture review of LLM-heavy applications
- When scaling from prototype to production AI

---

## Prerequisites

**Required**:
- Project has LLM integrations (API calls to OpenAI, Anthropic, Gemini, etc.)

**Recommended**:
- `.shipkit/stack.json` — Knows which AI SDKs are in use
- `.shipkit/architecture.json` — Knows pipeline design intent

**If no LLM integrations found**: Report cleanly and exit. Don't fabricate findings.

---

## Process

### Step 1: Discover LLM Integration Points

Scan the codebase for all LLM-related code using detection patterns.

**USE SUBAGENT FOR DISCOVERY** — Launch Explore subagent for efficient parallel scanning:

```
Task tool with subagent_type: "Explore"
Prompt: "Find all LLM integration points in this codebase.

Search for these patterns (see references/detection-patterns.md for full list):

API CLIENTS:
- OpenAI: openai.chat.completions, new OpenAI(
- Anthropic: anthropic.messages, new Anthropic(
- Gemini: googleGenerativeAI, model.generateContent
- LangChain: ChatOpenAI, LLMChain, RunnableSequence
- Vercel AI: generateText, streamText, generateObject

PROMPT TEMPLATES:
- Template literals with system/user roles
- Prompt files (.prompt, .txt used as prompts)
- Structured message arrays [{role, content}]

SCHEMA VALIDATION:
- Zod schemas near AI calls
- JSON.parse on AI responses
- Structured output definitions

Return for each integration point:
- File path and line number
- Provider/SDK used
- Whether it's a single call or part of a chain
- Input source and output destination"
```

**Why subagent**: Discovery requires many parallel grep/glob operations across the codebase. Explore agent handles this efficiently.

**Fallback** (if subagent unavailable) — Manual scanning:

```
1. Grep for API client instantiation:
   pattern: "new OpenAI\(|new Anthropic\(|GoogleGenerativeAI|ChatOpenAI"

2. Grep for API calls:
   pattern: "chat\.completions\.create|messages\.create|generateContent|generateText|streamText"

3. Grep for prompt templates:
   pattern: "system.*role|role.*system|You are a|As an AI"

4. Glob for prompt files:
   pattern: "**/*.prompt", "**/*.prompt.md", "**/prompts/**"
```

**If zero integration points found**: Report "No LLM integrations detected" and exit cleanly.

**Output of Step 1**: List of all LLM integration points with file:line references.

---

### Step 2: Map Pipeline Topology

For each discovered integration point, trace the data flow:

**For each LLM call, determine:**

| Question | How to Check | Classification |
|----------|-------------|----------------|
| Is this a single call or part of a chain? | Read surrounding code for sequential AI calls | `SINGLE` / `CHAIN` |
| Does output feed into another prompt? | Grep for variable reuse in next AI call | `FEEDS_NEXT` / `TERMINAL` |
| Are there parallel calls? | Check for Promise.all, concurrent AI calls | `PARALLEL` / `SEQUENTIAL` |
| Is the output validated? | Check for schema validation, JSON.parse, type checks | `VALIDATED` / `UNVALIDATED` |
| Is there error handling? | Check for try/catch, fallback logic | `HANDLED` / `UNHANDLED` |

**Build a topology map and serialize it for graph visualization:**

For each multi-stage pipeline, build a `pipelines[]` entry with `stages` (nodes) and `edges` (data flow):

```
Pipeline: [name/purpose]
  Stage 1: [provider] [model] — [purpose]
    Input: [source]
    Output: [validated? schema?]
    Fallback: [yes/no]
    ↓
  Stage 2: [provider] [model] — [purpose]
    Input: [from Stage 1 output]
    Output: [validated? schema?]
    Fallback: [yes/no]
```

**Capture as graph-ready data:**
- Each stage becomes a node: `{ id, promptId, provider, purpose, location }`
- Each data dependency becomes an edge: `{ id, source, target, dataFlow, validated }`
- Mark `validated: true` if data is schema-checked between stages, `false` otherwise
- Tag pipeline type: `"chain"` (sequential), `"parallel"` (concurrent stages), `"mixed"` (both)
- Link `issues[]` to relevant issue IDs from the audit findings

This topology data powers the pipeline flow graph in Mission Control.

**For multi-stage pipelines (3+ stages)**:
- Identify which stages could run in parallel
- Note sequential dependencies that can't be parallelized
- Flag stages that share no data dependencies but run sequentially

---

### Step 3: Audit 10 Dimensions

Review each integration point and pipeline against these dimensions.

**See `references/audit-checklist.md` for detailed checks per dimension.**

**FOR MULTIPLE INTEGRATION POINTS (3+), USE PARALLEL SUBAGENTS:**

```
Launch these Task agents IN PARALLEL (single message, multiple tool calls):

1. ARCHITECTURE AGENT (subagent_type: "Explore")
   Prompt: "Audit prompt decomposition and parallelization for these LLM integrations: [list files:lines]
   PA-DEC: Check for God Prompts (too many concerns), identify decomposition opportunities.
   PA-PAR: Check for sequential calls that could run parallel, unnecessary data dependencies.
   PA-CHN: Check chain integrity - does each stage get what it needs, are intermediates type-checked?
   Report Pass/Fail/Warning with file:line evidence and anti-pattern matches."

2. VALIDATION & SAFETY AGENT (subagent_type: "Explore")
   Prompt: "Audit schema validation and input safety for these LLM integrations: [list files:lines]
   PA-SCH: Check if outputs are validated with schema/zod, structured output modes used, JSON.parse wrapped.
   PA-INP: Check for input sanitization, prompt injection defenses, system/user content separation.
   PA-REF: Check if prompts reference existing code/data, examples are valid, no deprecated APIs/models.
   Report Pass/Fail/Warning with file:line evidence and anti-pattern matches."

3. RELIABILITY AGENT (subagent_type: "Explore")
   Prompt: "Audit reliability patterns for these LLM integrations: [list files:lines]
   PA-FBK: Check for fallback paths on failure, retry logic with backoff, rate limit handling.
   PA-CAC: Check if deterministic prompts are cached, expensive stages memoized, cache invalidation exists.
   PA-CTX: Check for unnecessary context, repeated context across stages, token limit risks.
   PA-CON: Check if output format instructions are explicit and testable.
   Report Pass/Fail/Warning with file:line evidence and anti-pattern matches."
```

**Why parallel subagents**:
- 10 dimensions across multiple integration points = many checks
- Each agent focuses on related dimensions
- Findings grouped logically (architecture vs safety vs reliability)

**When to use parallel agents:**
- 3+ LLM integration points discovered
- Multi-stage pipelines detected
- Deep audit requested

**When to scan manually:**
- 1-2 simple integration points
- Single-stage prompts only

#### Dimension 1: Decomposition (PA-DEC)
- Is the prompt doing too many things at once? (God Prompt)
- Could it be broken into focused sub-tasks?
- Are different concerns mixed in one prompt?

#### Dimension 2: Parallelization (PA-PAR)
- Are independent stages running sequentially?
- Could Promise.all/concurrent execution speed things up?
- Are there unnecessary data dependencies between stages?

#### Dimension 3: Schema Tightness (PA-SCH)
- Is the LLM output validated against a schema?
- Are structured output modes used where available?
- Is JSON.parse wrapped in try/catch?

#### Dimension 4: Chain Integrity (PA-CHN)
- Does each stage receive what it needs from the previous?
- Are intermediate results type-checked?
- Could a stage fail silently and corrupt downstream?
- Do early knowledge-gathering stages ask the right questions for downstream needs?

#### Dimension 5: Cache Boundaries (PA-CAC)
- Are deterministic prompts (same input = same output) cached?
- Are expensive stages memoized?
- Is there cache invalidation logic?

#### Dimension 6: Fallback Paths (PA-FBK)
- What happens when an LLM call fails?
- Is there retry logic with backoff?
- Is there a degraded experience (fallback to simpler model/static content)?
- Are rate limits handled?

#### Dimension 7: Context Efficiency (PA-CTX)
- Are prompts including unnecessary context?
- Is the same context repeated across chain stages?
- Could RAG/retrieval reduce prompt size?
- Are token limits being approached?

#### Dimension 8: Constraint Precision (PA-CON)
- Are output format instructions explicit?
- Are constraints testable (not vague)?
- Are few-shot examples used where format matters?
- Does the task verb match the intended cognitive mode? (generate vs evaluate vs research)

#### Dimension 9: Input Safety (PA-INP)
- Is user input sanitized before injection into prompts?
- Are prompt injection defenses in place?
- Are system prompts separated from user content?

#### Dimension 10: Reference Integrity (PA-REF)
- Do prompts reference code/data that exists?
- Are hardcoded examples still valid?
- Do prompts reference deprecated APIs or models?

---

### Step 3.5: Verification Protocol

**Critical: Execute tools before classifying findings.**

Every finding MUST be backed by actual tool output. Follow the same verification protocol as `/shipkit-verify`:

| Step | Action |
|------|--------|
| **1. IDENTIFY** | What tool call proves this claim? |
| **2. RUN** | Execute the Glob/Grep/Read |
| **3. READ** | Examine full output |
| **4. CLASSIFY** | Determine severity from evidence |
| **5. REPORT** | State finding WITH evidence |

**Anti-pattern checks** (see `references/anti-patterns.md`):
- Check each integration point against known anti-patterns
- Cross-reference with pipeline topology
- Classify matches by severity

---

### Step 4: Generate Report

**Create file using Write tool**: `.shipkit/prompt-audit.json`

The output MUST conform to the schema below. This is a strict contract — mission control and other skills depend on this structure.

---

## JSON Schema

**Full schema**: See `references/output-schema.md`
**Example output**: See `references/example.json`

### Quick Reference

```json
{
  "$schema": "shipkit-artifact",
  "type": "prompt-audit",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DD",
  "source": "shipkit-prompt-audit",
  "summary": {
    "totalPromptsAudited": number,
    "totalIssuesFound": number,
    "bySeverity": { "critical", "shouldFix", "minor" },
    "integrationPoints": number,
    "providers": ["OpenAI", "Anthropic", ...],
    "pipelines": { "singleStage", "multiStage" }
  },
  "prompts": [{
    "id", "location", "provider", "purpose", "pipelineType", "score",
    "issues": [{ "id", "dimension", "severity", "title", "evidence", "impact", "fix", "antiPattern?" }]
  }],
  "pipelines": [{
    "id", "name", "type",
    "stages": [{ "id", "promptId", "provider", "purpose", "location" }],
    "edges": [{ "id", "source", "target", "dataFlow", "validated" }],
    "issues?": ["issue-id-refs"]
  }],
  "patterns": {
    "antiPatterns": [{ "name", "instances", "files", "description" }],
    "positivePatterns": [{ "name", "instances", "description" }]
  },
  "recommendations": [{ "priority", "title", "description", "affectedFiles", "effort" }]
}
```

### Key Fields

| Field | Description |
|-------|-------------|
| `prompts[].pipelineType` | `"single"` \| `"chain"` \| `"parallel"` |
| `prompts[].issues[].severity` | `"critical"` \| `"shouldFix"` \| `"minor"` |
| `pipelines[].type` | `"chain"` \| `"parallel"` \| `"mixed"` |
| `pipelines[].edges[].validated` | Whether data between stages is schema-checked |
| `recommendations[].effort` | `"low"` \| `"medium"` \| `"high"` |

---

### Step 5: Present Results

**Output to user:**

```
Prompt Architecture Audit complete

Scanned: X integration points across Y files
Providers: [OpenAI, Anthropic, ...]
Pipelines: X single-stage, Y multi-stage

Critical: X findings
Should Fix: X findings
Minor: X suggestions

Top issues:
1. [Brief description with file reference]
2. [Brief description with file reference]
3. [Brief description with file reference]

Full report: .shipkit/prompt-audit.json

Want me to fix any of these issues?
```

---

## Priority Definitions

| Priority | Meaning | Example |
|----------|---------|---------|
| Critical | Will cause failures, security issues, or data corruption | Unvalidated LLM output used in database query; no fallback on payment-critical AI call |
| Should Fix | Quality/reliability issues, technical debt | God Prompt that should be decomposed; sequential calls that could parallelize |
| Minor | Suggestions, optimizations | Caching opportunity; slightly verbose context |

---

## Shipkit Artifact Convention

This skill follows the **Shipkit JSON artifact convention**. See `references/output-schema.md` for full documentation.

---

## What This Skill Does NOT Do

- **Rewrite prompts** — reports issues, doesn't fix them
- **Judge prompt text quality** — "make this prompt better" is not in scope
- **Run prompts** — static analysis only, no execution
- **Test output quality** — that's evaluation tooling (Promptfoo, etc.)
- **Persist beyond report** — single audit snapshot

---

## Context Files This Skill Reads

| File | Purpose |
|------|---------|
| Source code | The actual LLM integration code |
| `.shipkit/stack.json` | Know which AI SDKs/providers are used |
| `.shipkit/architecture.json` | Understand intended pipeline design |
| `package.json` / `requirements.txt` | Detect AI SDK dependencies |

---

## Context Files This Skill Writes

**Write Strategy**: OVERWRITE

- `.shipkit/prompt-audit.json` — Audit report (JSON artifact, overwritten on each run)

---

## When This Skill Integrates with Others

### Routes FROM

| Source | When |
|--------|------|
| `/shipkit-master` | User asks "audit prompts", "check AI pipeline" |
| `/shipkit-verify` | Flags AI-related code for deeper review |
| `/shipkit-preflight` | Pre-launch check of AI features |

### After This Skill

- User fixes findings (natural capability)
- Re-run `/shipkit-prompt-audit` to verify fixes
- `/shipkit-architecture-memory` — log pipeline design decisions

### Differs From

| Skill | Focus |
|-------|-------|
| `/shipkit-verify` | Code quality across 12 dimensions (breadth) |
| `/shipkit-prompt-audit` | LLM pipeline architecture (depth on AI code) |
| `/shipkit-preflight` | Production readiness (broader than AI) |
| `/shipkit-scale-ready` | Scale & operations (infrastructure focus) |

---

<!-- SECTION:after-completion -->
## After Completion

**Audit delivered. User decides next steps:**

1. **Fix critical issues** — Ask Claude to help restructure pipelines
2. **Review should-fix items** — Decide which to address now
3. **Re-run audit** — Verify fixes resolved the issues
4. **Log decisions** — Use `/shipkit-architecture-memory` for pipeline design choices

**Natural capabilities** (no skill needed): Implementing fixes, refactoring prompts, adding validation.

No follow-up skill automatically triggered.
<!-- /SECTION:after-completion -->

---

<!-- SECTION:success-criteria -->
## Success Criteria

- [ ] LLM integration points discovered via codebase scan
- [ ] Pipeline topology mapped (single vs chain, parallel vs sequential)
- [ ] All 10 dimensions audited with tool-verified evidence
- [ ] Anti-patterns checked against known patterns
- [ ] Findings prioritized (Critical / Should Fix / Minor)
- [ ] Each finding has specific file:line reference
- [ ] Report saved to `.shipkit/prompt-audit.json`
- [ ] Output conforms to JSON schema above
- [ ] Summary field is accurate
- [ ] Report only — no unsolicited fixes
<!-- /SECTION:success-criteria -->

---

## References

- `references/detection-patterns.md` — Grep/Glob patterns for discovering LLM integrations
- `references/audit-checklist.md` — Detailed checks per dimension with IDs and severity
- `references/anti-patterns.md` — Common prompt architecture anti-patterns
