---
name: shipkit-architecture-memory
description: "Use when making or documenting an architectural decision, technology choice, or design pattern. Triggers: 'log decision', 'why did we choose', 'architecture choice'."
argument-hint: "<decision to log>"
context: fork
agent: shipkit-architect-agent
---

# shipkit-architecture-memory - Architectural Decision Logger

**Purpose**: Maintain a structured graph of architectural nodes, edges, decisions, and constraints in JSON format — preserving full decision history with rationale, alternatives, implications, superseded decisions, and component relationships suitable for React Flow visualization.

---

## When to Invoke

**User triggers**:
- "Let's use Server Actions instead of API routes"
- "Log this decision"
- "Document this choice"
- "Remember we're using [pattern/tech/approach]"
- After making significant architectural choice

**Auto-suggest contexts**:
- After `/shipkit-spec` when approach decisions are made
- After `/shipkit-plan` when significant patterns are established
- During `implement (no skill needed)` when new patterns emerge
- When user describes an architectural choice in conversation

---

## Prerequisites

**Optional but helpful**:
- Stack defined: `.shipkit/stack.json` (to ensure consistency)
- Architecture graph exists: `.shipkit/architecture.json` (to check contradictions and existing nodes)

**Can run standalone**: Yes - creates architecture.json if it doesn't exist

---

## JSON Schema

**Output file**: `.shipkit/architecture.json`

**Full schema reference**: See `references/output-schema.md`
**Example output**: See `references/example.json`

This file uses the **Shipkit JSON Artifact Convention** and models the architecture as a **graph** (nodes + edges) suitable for React Flow rendering, plus decision and constraint records.

### Quick Reference

```json
{
  "$schema": "shipkit-artifact",
  "type": "architecture",
  "version": "1.0",
  "lastUpdated": "ISO-8601-timestamp",
  "source": "shipkit-architecture-memory",
  "summary": { "totalNodes": N, "totalEdges": N, "totalDecisions": N, ... },
  "nodes": [{ "id": "node-id", "label": "Name", "type": "service|database|cache|...", "layer": "frontend|api|...", "status": "active|planned|deprecated" }],
  "edges": [{ "id": "edge-1", "source": "node-a", "target": "node-b", "type": "sync|async|event", "protocol": "HTTPS" }],
  "decisions": [{ "id": "dec-1", "title": "...", "status": "decided|superseded", "decisionType": "architectural|operational", "chosen": "...", "rationale": "...", "supersedes": null }],
  "constraints": [{ "id": "con-1", "description": "...", "type": "performance|security|...", "affectedNodes": [...] }]
}
```

### Decision Types

| Type | Definition | Examples |
|------|------------|----------|
| **architectural** | Tech choice, pattern selection, structural decision | "Use Server Actions", "Use Drizzle ORM" |
| **operational** | Runtime behavior, data flow rules, invariants | "Invalidate X when Y changes", "Cache TTL = 5min" |

### Decision Status Lifecycle

- **decided**: Active decision, still applies
- **superseded**: Replaced by a newer decision (link via `supersedes` field)
- **deprecated**: No longer recommended, should be migrated

### ID Generation Rules

- **Decisions**: `dec-[N]` (sequential)
- **Nodes**: kebab-case descriptive name (e.g., `next-app`, `postgres-db`)
- **Edges**: `edge-[N]` (sequential)
- **Constraints**: `con-[N]` (sequential)

---

## Process

### Step 1: Read Existing Context

**Before asking questions, read existing architecture graph**:

```bash
# Check if architecture graph exists
.shipkit/architecture.json

# Check stack for consistency
.shipkit/stack.json
```

**Why read first**:
- Detect contradictions with existing decisions
- Understand established patterns and existing nodes/edges
- Don't re-ask what's already documented
- Identify affected nodes for new decisions

**If files don't exist**: Continue to questions (will create architecture.json)

### Verification Before Recording

Before recording any decision, verify claims with tool calls:

| Claim | Required Verification |
|-------|----------------------|
| "architecture.json exists" | `Read: file_path=".shipkit/architecture.json"` succeeds |
| "X decisions recorded" | Count entries in `decisions` array after reading |
| "Decision contradicts existing" | Check `decisions` array for same-domain entries |
| "Aligns with stack.json" | `Grep: pattern="technology-name"` in stack.json returns match |
| "Supersedes entry X" | Find decision by `id` in `decisions` array |
| "Node already exists" | Check `nodes` array for matching `id` |

**USE PARALLEL VERIFICATION** - Independent checks can run simultaneously:

```
Launch these operations IN PARALLEL (single message, multiple tool calls):

1. Read: .shipkit/architecture.json    # Get existing graph and decisions
2. Read: .shipkit/stack.json           # Get tech stack for consistency check
3. Grep: pattern="[pattern-keyword]" glob="**/*.{ts,tsx}"  # Find pattern usage
```

**Why parallel**: Context reads and pattern grep are independent. Parallel execution speeds up verification by ~40%.

**Pattern Ripple for Decisions:**

When recording "we use X pattern", grep for ALL instances of that pattern and document the scope:

```
Example: Recording "Use Server Actions for mutations"

1. Grep: pattern="use server|Server Action" glob="**/*.{ts,tsx}"
2. Count matches: 5 files
3. Include in decision implications: "Pattern used in 5 files: [list]"
4. Future verification can check if new files follow pattern
```

**Why this matters:** Recording a pattern decision without knowing current usage leads to inconsistent enforcement.

**Verification sequence (after parallel reads complete):**

```
1. From architecture.json read: count decisions, check for contradictions
2. From stack.json read: verify technology consistency
3. From pattern grep: document current usage count in decision entry
4. If all verifications pass -> proceed to record
```

**See also:** `shared/references/VERIFICATION-PROTOCOL.md` for standard verification patterns.

---

### Step 1b: Deep Explore of Affected Code Areas

**Beyond keyword grep, understand the actual code the decision affects.**

A grep count tells you how many files mention a pattern, but not whether the code is consistent, what alternatives are mixed in, or what would break if the pattern changes.

**Index-Accelerated Exploration** — Read `.shipkit/codebase-index.json` first:

1. `Read: .shipkit/codebase-index.json`
2. If index exists:
   - Use `concepts` to find files in the affected area (e.g., if decision is about auth, get `concepts.auth` files)
   - Use `coreFiles` to identify high-dependency files that would amplify blast radius
   - Pass affected file lists directly to Explore agents for targeted analysis
3. If index doesn't exist → agents discover affected areas via broad scanning

**Launch explore agents** — Use the Task tool with `subagent_type: Explore`:

```
Agent 1 - Current state of affected area: "Explore the codebase areas
related to [decision topic].
[If index exists, include: 'The codebase index maps these relevant files: [concept files for decision area]. Start from these — focus on consistency analysis and pattern assessment, not broad discovery.']
Look for: how [pattern/technology] is currently used, what conventions exist,
whether usage is consistent or fragmented, and what the code structure looks
like in affected areas. Report: current state summary, consistency level,
notable deviations."

Agent 2 - Impact and dependencies: "Find code that would be affected
if [decision] is applied.
[If index exists, include: 'Core files (high fan-in): [coreFiles]. Concepts: [concepts]. These are the highest-impact files — trace dependency chains from here.']
Look for: files that use the old/alternative pattern, downstream consumers,
tests that depend on current behavior, configuration that references the pattern.
Report: blast radius of the decision, contracts that must be preserved,
migration scope."
```

**Launch both agents in parallel** — they are independent searches.

**Feed findings into decision entry** — Use exploration results to populate:
- `implications` — grounded in actual code impact, not hypothetical
- `affectedNodes` — based on real files/modules found
- Pattern usage counts — exact files, not just grep hits

**If exploration reveals inconsistency**: Surface to user. Example: *"The codebase currently mixes Server Actions and API routes — 3 files use one pattern, 5 use the other. Should this decision standardize on one approach?"*

**Token budget**: Each explore agent should return a focused summary (~500 tokens).

**When to skip**: If the decision is purely about a new technology/pattern not yet present in the codebase (nothing to explore).

---

### Step 2: Capture Decision Context

**Ask user 2-3 questions to capture decision fully**:

**Question 1: What was decided?**
- "What architectural decision did you make?"
- If clear from conversation -> Skip this question
- Example: User said "Let's use Server Actions" -> Already clear

**Question 2: Why this approach?**
- "Why did you choose this approach?"
- "What problem does this solve?"
- Focus on rationale, not just description

**Question 3: What alternatives existed?**
- "What alternatives did you consider?"
- "What other options were available?"
- Capture trade-offs

**Optional Question 4 (if complex decision):**
- "What are the implications of this choice?"
- "What does this require or constrain?"

**Optional Question 5 (for graph context):**
- "Which components/services does this affect?"
- "Does this introduce a new component or change how existing ones connect?"

**Token budget**: Keep questions focused, don't over-interrogate

---

### Step 3: Check for Contradictions

**Before modifying, check existing architecture.json for conflicts**:

**Contradiction detection logic**:
```
IF architecture.json exists:
  1. Read all existing decisions from the decisions array
  2. Check if new decision contradicts any existing decision with status "decided"
  3. Look for:
     - Same problem, different solution
     - Incompatible patterns
     - Technology conflicts
     - Approach reversals

IF contradiction found:
  -> Ask user: "This contradicts [Decision title from YYYY-MM-DD]. Supersede it?"
  -> If YES: Set old decision status to "superseded", new decision's supersedes field to old id
  -> If NO: Ask for clarification

IF no contradiction:
  -> Proceed to update graph
```

**Example contradiction**:
```
Existing decision: "Use API routes for all data fetching"
New decision: "Use Server Actions for mutations"
-> NOT a contradiction (different use cases)

Existing decision: "Use REST API for backend"
New decision: "Use GraphQL for all APIs"
-> IS a contradiction
-> Ask: "This contradicts REST decision (dec-3) from 2025-01-10. Supersede it?"
```

---

### Step 4: Build Graph Updates

When recording a decision, determine what graph changes are needed:

**Identify node changes**:
```
Does the decision introduce a new component/service/technology?
  -> YES: Create a new node entry
  -> NO: Check if existing nodes need status updates

Does the decision deprecate an existing component?
  -> YES: Update that node's status to "deprecated"
```

**Identify edge changes**:
```
Does the decision change how components communicate?
  -> YES: Add/update edge entries
  -> NO: Skip edge changes

Does the decision replace a communication pattern?
  -> YES: Remove old edge, add new edge
```

**Identify constraint changes**:
```
Does the decision introduce system constraints?
  -> YES: Add constraint entries
  -> NO: Skip constraint changes
```

**Build the decision entry**:

```json
{
  "id": "dec-[next-number]",
  "title": "[5-10 word title]",
  "date": "[YYYY-MM-DD]",
  "status": "decided",
  "decisionType": "[architectural|operational]",
  "chosen": "[What was chosen - one clear sentence]",
  "alternatives": [
    { "name": "[Alternative 1]", "reason": "[Why not chosen]" },
    { "name": "[Alternative 2]", "reason": "[Why not chosen]" }
  ],
  "rationale": "[Why this was chosen]",
  "affectedNodes": ["[node-id-1]", "[node-id-2]"],
  "implications": [
    "[Implication 1]",
    "[Implication 2]"
  ],
  "supersedes": null,
  "tradeoffs": "[Key tradeoff]"
}
```

**ID generation rules**:
- Decisions: `dec-[N]` where N is the next sequential number
- Nodes: kebab-case descriptive name (e.g., `next-app`, `postgres-db`, `api-gateway`)
- Edges: `edge-[N]` where N is the next sequential number
- Constraints: `con-[N]` where N is the next sequential number

---

### Step 5: Update Architecture Graph

**Use Read + Write to update the JSON file**:

**Location**: `.shipkit/architecture.json`

**Process**:
1. Read existing architecture.json (if exists)
2. Parse the JSON
3. Add new decision to `decisions` array
4. Add/update nodes in `nodes` array (if applicable)
5. Add/update edges in `edges` array (if applicable)
6. Add constraints to `constraints` array (if applicable)
7. Update `summary` counts and metadata
8. Update `lastUpdated` timestamp
9. Write the complete JSON file back

**If creating new file**, start with this structure:

```json
{
  "$schema": "shipkit-artifact",
  "type": "architecture",
  "version": "1.0",
  "lastUpdated": "[ISO 8601 timestamp]",
  "source": "shipkit-architecture-memory",
  "summary": {
    "totalNodes": 0,
    "totalEdges": 0,
    "totalDecisions": 0,
    "totalConstraints": 0,
    "layers": [],
    "lastDecision": ""
  },
  "nodes": [],
  "edges": [],
  "decisions": [],
  "constraints": []
}
```

**When a decision is superseded**:
1. Find the old decision in `decisions` array by `id`
2. Set its `status` to `"superseded"`
3. Add new decision with `supersedes` field pointing to old decision's `id`
4. Update any affected nodes/edges as needed

**Update rules**:
- Always update `lastUpdated` with current ISO timestamp
- Always recompute `summary` fields after changes
- Never remove decisions from the array (history is preserved)
- Node and edge removals are allowed when architecture changes (set status to `"deprecated"` for nodes instead of deleting when possible)

---

### Step 6: Check Stack Consistency

**After updating, verify consistency with stack.json**:

```
IF decision involves technology choice:
  -> Check if it's documented in stack.json
  -> If NO: Suggest "Should I update stack.json to reflect this?"
  -> If YES: Verify it aligns

IF inconsistency found:
  -> Warn user: "This conflicts with stack.json which says [X]"
```

**Example**:
```
Decision: "Use Prisma for database access"
Stack.json says: "Database: PostgreSQL with Drizzle ORM"
-> Warn: "This conflicts with stack.json (Drizzle ORM). Update stack.json?"
```

---

### Step 7: Suggest Documentation (if needed)

**For complex decisions, offer extended documentation**:

```
IF decision is complex (multiple implications, significant architectural change):
  -> Suggest: "document manually to create extended architecture docs"

IF decision is simple (single pattern choice):
  -> Just log and continue
```

**Complexity indicators**:
- More than 3 implications
- Affects multiple systems (3+ affected nodes)
- Changes foundational pattern
- Requires team alignment

---

### Step 8: Suggest Next Step

---

## Completion Checklist

Copy and track:
- [ ] Identified the decision context
- [ ] Explored affected code areas (current state + blast radius)
- [ ] Implications grounded in actual codebase findings
- [ ] Documented rationale and alternatives considered
- [ ] Updated `.shipkit/architecture.json` with decision entry
- [ ] Added/updated graph nodes and edges if applicable
- [ ] Updated summary counts
- [ ] Set `lastUpdated` timestamp

---

## What Makes This "Lite"

**Included**:
- Graph-based architecture model (nodes + edges)
- Structured decision records with full context
- Contradiction detection across decisions
- Supersession tracking via decision `id` links
- Stack consistency checking
- React Flow-compatible graph structure
- Dashboard-ready summary data

**Not included** (vs full architecture-memory):
- Architecture diagram image generation
- Multi-repository decision tracking
- Team vote/approval workflows
- Decision impact analysis across codebase
- Automated dependency graph discovery from code

**Philosophy**: Structured architecture graph to maintain context and enable visualization, not comprehensive architecture documentation system.

---

## Integration with Other Skills

**Before shipkit-architecture-memory**:
- `/shipkit-spec` - Makes approach decisions worth logging
- `/shipkit-plan` - Establishes patterns worth documenting
- `/shipkit-project-context` - Generates stack.json for consistency checking

**After shipkit-architecture-memory**:
- `/shipkit-plan` - Create implementation plan using logged decisions
- `implement (no skill needed)` - Code following logged patterns
- `document manually` - Create extended architecture docs (optional)

---

## Context Files This Skill Reads

**Primary**:
- `.shipkit/architecture.json` - Existing architecture graph (to check contradictions and existing nodes)

**Secondary**:
- `.shipkit/stack.json` - Tech stack (to verify consistency)

---

## Context Files This Skill Writes

**Write Strategy: READ-MODIFY-WRITE**

**Writes to**:
- `.shipkit/architecture.json` - Architecture graph with decisions
  - **Strategy**: READ-MODIFY-WRITE (read existing JSON, add/update entries, write back)
  - **Rationale**: JSON graph structure requires full-file writes; decision history is preserved by never removing entries from the `decisions` array
  - **Process**: Read existing file -> Parse JSON -> Add/update entries -> Recompute summary -> Write full file back
  - **Note**: This skill uses `context: fork` — conversation context is forked but filesystem writes go to the real project. Always re-read `architecture.json` immediately before writing to avoid stale data.
  - **File size**: Grows slowly (decisions are infrequent); nodes/edges stay relatively stable

**Never modifies**:
- Stack, specs, plans (read-only)

---

## Lazy Loading Behavior

**This skill loads minimal context**:

1. User invokes `/shipkit-architecture-memory`
2. Claude reads this SKILL.md
3. Claude reads `.shipkit/architecture.json` (if exists) - ~500-1500 tokens
4. Claude reads `.shipkit/stack.json` (if exists) - ~200 tokens
5. Claude asks 2-3 questions
6. Claude updates architecture graph
7. Total context: ~1000-2500 tokens (lightweight)

**Not loaded unless needed**:
- Specs, plans, implementations
- User tasks, session logs
- Other context files

---

## Contradiction Detection Examples

### Example 1: No Contradiction
```
Existing decision: "Use Next.js App Router for routing"
New decision: "Use Server Actions for form submissions"
-> No conflict (Server Actions work with App Router)
-> Add decision directly
```

### Example 2: Clear Contradiction
```
Existing decision (dec-2): "Use MongoDB for database"
New decision: "Use PostgreSQL with Prisma"
-> Clear conflict (different databases)
-> Ask: "This contradicts MongoDB decision (dec-2) from 2025-01-12. Supersede it?"
-> If yes: set dec-2 status to "superseded", new decision supersedes "dec-2"
```

### Example 3: Partial Contradiction
```
Existing decision (dec-5): "Use REST API for all endpoints"
New decision: "Use tRPC for admin endpoints"
-> Partial conflict (different approach for subset)
-> Ask: "This modifies REST decision (dec-5) from 2025-01-15. Is this an exception or full replacement?"
```

### Example 4: Enhancement, Not Contradiction
```
Existing decision: "Use TypeScript for type safety"
New decision: "Use Zod for runtime validation"
-> No conflict (complementary)
-> Add decision directly
```

---

## Decision Entry Examples

**See `references/example.json` for complete examples** including:
- Architectural decisions (tech choices, patterns)
- Operational decisions (runtime behavior, invariants)
- Decisions with supersession
- Decisions that add nodes/edges/constraints

---

<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Has important context been saved to `.shipkit/`?
2. **Prerequisites** - Does the next action need a spec or plan first?
3. **Session length** - Long session? Consider `/shipkit-work-memory` for continuity.

**Natural capabilities** (no skill needed): Implementation, debugging, testing, refactoring, code documentation.

**Suggest skill when:** User needs to make decisions, create persistence, or check project status.
<!-- /SECTION:after-completion -->

<!-- SECTION:success-criteria -->
## Success Criteria

Decision is logged when:
- [ ] Affected code areas explored (current state, consistency, blast radius)
- [ ] Decision entry added to `decisions` array in architecture.json
- [ ] Includes `chosen` statement
- [ ] Includes `rationale` (WHY)
- [ ] Includes `alternatives` considered
- [ ] Includes `implications` (grounded in codebase findings)
- [ ] `supersedes` field set correctly (decision id or null)
- [ ] No contradictions with existing decisions (or user confirmed supersession)
- [ ] Graph nodes/edges updated if architecture components changed
- [ ] `summary` fields recomputed
- [ ] `lastUpdated` timestamp set
- [ ] Consistency with stack.json verified
<!-- /SECTION:success-criteria -->
---

## Common Scenarios

### Scenario 1: User Makes Decision During Planning

```
User: "Let's use Server Actions for all mutations"

Claude (shipkit-architecture-memory):
1. Read .shipkit/architecture.json (check contradictions, existing nodes)
2. Read .shipkit/stack.json (verify Next.js version)
3. Decision is clear from statement -> Skip "What was decided?" question
4. Ask: "Why Server Actions over API routes?"
5. User: "Co-location and simpler error handling"
6. Ask: "What are the implications?"
7. User: "Requires Next.js 14+"
8. Check for contradictions -> None found
9. Add decision to architecture.json, update affected nodes, recompute summary
10. "Decision logged in architecture.json. Run /shipkit-plan to create implementation plan?"
```

### Scenario 2: Decision Contradicts Existing Choice

```
User: "Actually, let's use GraphQL instead"

Claude (shipkit-architecture-memory):
1. Read .shipkit/architecture.json
2. Find existing decision (dec-3): "Use REST API for all endpoints"
3. Detect contradiction
4. Ask: "This contradicts REST decision (dec-3) from 2025-01-12. Supersede it?"
5. User: "Yes"
6. Ask: "Why GraphQL over REST?"
7. User: "Better for our complex data relationships"
8. Set dec-3 status to "superseded"
9. Add new decision with supersedes: "dec-3"
10. Update any affected edges (e.g., change protocol labels)
11. "Decision logged. dec-3 (REST API) marked as superseded."
```

### Scenario 3: Decision Introduces New Component

```
User: "We need to add Redis for caching"

Claude (shipkit-architecture-memory):
1. Read .shipkit/architecture.json
2. No existing cache nodes found
3. Ask clarifying questions about caching strategy
4. Add new node: redis-cache (type: cache, layer: infrastructure)
5. Add new edges: api-gateway -> redis-cache
6. Add decision entry with affectedNodes
7. Optionally add performance constraint
8. "Decision logged. Added redis-cache node and connection to api-gateway."
```

### Scenario 4: Complex Decision Needs Extended Docs

```
User: "We're using microservices with event-driven architecture"

Claude (shipkit-architecture-memory):
1. Ask clarifying questions
2. Add multiple nodes (services), edges (event bus connections), decision entry
3. Detect complexity (multiple implications, affects multiple systems)
4. Suggest: "This is a significant architectural change. Run document manually to create extended architecture documentation?"
```

---

## Tips for Effective Decision Logging

**Capture WHY, not just WHAT**:
- Good `rationale`: "Co-location with components reduces context switching and automatic revalidation eliminates a class of bugs"
- Bad `rationale`: "Use Server Actions"

**Document alternatives**:
- Shows you considered options
- Helps future developers understand trade-offs
- Prevents rehashing old debates

**Note implications**:
- What does this require?
- What does this constrain?
- What changes because of this?

**Link superseded decisions**:
- Maintains decision history
- Shows evolution of thinking
- Prevents confusion about contradictions

**Keep it concise**:
- Decision graph, not essay
- 3-5 implications max
- 2-3 alternatives max

**Update graph nodes and edges**:
- When a decision introduces new components, add nodes
- When a decision changes communication patterns, update edges
- Keep the graph accurate for visualization

---

**Remember**: This skill produces a structured architecture graph with decision history. The JSON format enables dashboard visualization (React Flow for graph, cards for decisions). For detailed architecture docs, use `document manually`.
