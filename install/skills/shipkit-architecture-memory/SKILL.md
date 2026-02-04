---
name: shipkit-architecture-memory
description: "Use when making or documenting an architectural decision, technology choice, or design pattern. Triggers: 'log decision', 'why did we choose', 'architecture choice'."
argument-hint: "<decision to log>"
---

# shipkit-architecture-memory - Architectural Decision Logger

**Purpose**: Maintain append-only log of architectural decisions with full context (rationale, alternatives, implications, superseded decisions) to preserve decision history and prevent contradictory choices.

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
- Stack defined: `.shipkit/stack.md` (to ensure consistency)
- Architecture log exists: `.shipkit/architecture.md` (to check contradictions)

**Can run standalone**: Yes - creates architecture.md if it doesn't exist

---

## Process

### Step 1: Read Existing Context

**Before asking questions, read existing decisions**:

```bash
# Check if architecture log exists
.shipkit/architecture.md

# Check stack for consistency
.shipkit/stack.md
```

**Why read first**:
- Detect contradictions with existing decisions
- Understand established patterns
- Don't re-ask what's already documented

**If files don't exist**: Continue to questions (will create architecture.md)

---

### Step 2: Capture Decision Context

**Ask user 2-3 questions to capture decision fully**:

**Question 1: What was decided?**
- "What architectural decision did you make?"
- If clear from conversation → Skip this question
- Example: User said "Let's use Server Actions" → Already clear

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

**Token budget**: Keep questions focused, don't over-interrogate

---

### Step 3: Check for Contradictions

**Before appending, check existing architecture.md for conflicts**:

**Contradiction detection logic**:
```
IF architecture.md exists:
  1. Read all existing decisions
  2. Check if new decision contradicts any existing decision
  3. Look for:
     - Same problem, different solution
     - Incompatible patterns
     - Technology conflicts
     - Approach reversals

IF contradiction found:
  → Ask user: "This contradicts [Decision from YYYY-MM-DD]. Supersede it?"
  → If YES: Note what's superseded in new entry
  → If NO: Ask for clarification

IF no contradiction:
  → Proceed to append
```

**Example contradiction**:
```
Existing: "Use API routes for all data fetching"
New: "Use Server Actions for mutations"
→ NOT a contradiction (different use cases)

Existing: "Use REST API for backend"
New: "Use GraphQL for all APIs"
→ IS a contradiction
→ Ask: "This contradicts REST decision from 2025-01-10. Supersede it?"
```

---

### Step 4: Format Decision Entry

**Entry format template**:

```markdown
## [YYYY-MM-DD] [Decision Title]

**Status**: Current | Superseded | Deprecated

**Decision**: [What was decided - 1 clear sentence]

**Reason**: [Why this was chosen - rationale and problem it solves]

**Alternatives considered**:
- [Alternative 1]: [Why not chosen]
- [Alternative 2]: [Why not chosen]

**Implications**:
- [Implication 1]
- [Implication 2]
- [Implication 3]

**Supersedes**: [Decision from YYYY-MM-DD] OR "None"

---
```

**Status values**:
- **Current**: Active decision, still applies
- **Superseded**: Replaced by a newer decision (link in superseding entry)
- **Deprecated**: No longer recommended, may still exist in codebase but should be migrated

**Rules**:
- Timestamp is date only (YYYY-MM-DD), not full timestamp
- Status tracks decision lifecycle (new entries start as "Current")
- Title is concise (5-10 words)
- Decision statement is ONE clear sentence
- Reason captures WHY, not just WHAT
- Alternatives show what was considered
- Implications capture requirements/constraints
- Supersedes links to replaced decisions

**When a decision is superseded**:
1. Create new decision entry with Status: Current
2. Edit the old decision entry to change Status: Current → Status: Superseded
3. This is the ONE exception to append-only - status updates are allowed

---

### Step 5: Append to Architecture Log

**Use Write tool to append entry**:

**Location**: `.shipkit/architecture.md`

**Process**:
1. Read existing architecture.md (if exists)
2. Append new entry to end
3. Write full file back

**File structure** (if creating new):
```markdown
# Architectural Decisions

This file logs all architectural decisions made during development. Each entry captures the decision, rationale, alternatives considered, and implications.

**Format**: Append-only (never edit existing decisions)

**Contradiction handling**: New decisions that contradict old ones note what they supersede

---

[Decision entries appended here]
```

**Append-only rule**: NEVER edit existing decisions. Only append new ones.

---

### Step 6: Check Stack Consistency

**After appending, verify consistency with stack.md**:

```
IF decision involves technology choice:
  → Check if it's documented in stack.md
  → If NO: Suggest "Should I update stack.md to reflect this?"
  → If YES: Verify it aligns

IF inconsistency found:
  → Warn user: "This conflicts with stack.md which says [X]"
```

**Example**:
```
Decision: "Use Prisma for database access"
Stack.md says: "Database: PostgreSQL with Drizzle ORM"
→ Warn: "This conflicts with stack.md (Drizzle ORM). Update stack.md?"
```

---

### Step 7: Suggest Documentation (if needed)

**For complex decisions, offer extended documentation**:

```
IF decision is complex (multiple implications, significant architectural change):
  → Suggest: "document manually to create extended architecture docs"

IF decision is simple (single pattern choice):
  → Just log and continue
```

**Complexity indicators**:
- More than 3 implications
- Affects multiple systems
- Changes foundational pattern
- Requires team alignment

---

### Step 8: Suggest Next Step

---

## Completion Checklist

Copy and track:
- [ ] Identified the decision context
- [ ] Documented rationale and alternatives considered
- [ ] Appended to `.shipkit/architecture.md`

---

## What Makes This "Lite"

**Included**:
- ✅ Append-only decision log
- ✅ Captures rationale and alternatives
- ✅ Contradiction detection
- ✅ Links to superseded decisions
- ✅ Stack consistency checking

**Not included** (vs full architecture-memory):
- ❌ Architecture diagram generation
- ❌ Dependency graph visualization
- ❌ Multi-repository decision tracking
- ❌ Team vote/approval workflows
- ❌ Decision impact analysis across codebase
- ❌ ADR (Architecture Decision Record) templates with status lifecycle

**Philosophy**: Lightweight decision log to maintain context, not comprehensive architecture documentation system.

---

## Integration with Other Skills

**Before shipkit-architecture-memory**:
- `/shipkit-spec` - Makes approach decisions worth logging
- `/shipkit-plan` - Establishes patterns worth documenting
- `/shipkit-project-context` - Generates stack.md for consistency checking

**After shipkit-architecture-memory**:
- `/shipkit-plan` - Create implementation plan using logged decisions
- `implement (no skill needed)` - Code following logged patterns
- `document manually` - Create extended architecture docs (optional)

---

## Context Files This Skill Reads

**Primary**:
- `.shipkit/architecture.md` - Existing decisions (to check contradictions)

**Secondary**:
- `.shipkit/stack.md` - Tech stack (to verify consistency)

---

## Context Files This Skill Writes

**Write Strategy: APPEND**

**Appends to**:
- `.shipkit/architecture.md` - Architectural decisions log
  - **Strategy**: APPEND (never overwrite or archive)
  - **Rationale**: Complete history required for contradiction detection, supersession tracking, and decision evolution narrative
  - **Process**: Read existing file → Append new entry to end → Write full file back
  - **File size**: Not a concern (decisions are infrequent, ~15 lines each)

**Never modifies**:
- Stack, specs, plans (read-only)

---

## Lazy Loading Behavior

**This skill loads minimal context**:

1. User invokes `/shipkit-architecture-memory`
2. Claude reads this SKILL.md
3. Claude reads `.shipkit/architecture.md` (if exists) - ~500-1000 tokens
4. Claude reads `.shipkit/stack.md` (if exists) - ~200 tokens
5. Claude asks 2-3 questions
6. Claude appends decision
7. Total context: ~1000-2000 tokens (very lightweight)

**Not loaded unless needed**:
- Specs, plans, implementations
- User tasks, session logs
- Other context files

---

## Contradiction Detection Examples

### Example 1: No Contradiction
```
Existing: "Use Next.js App Router for routing"
New: "Use Server Actions for form submissions"
→ No conflict (Server Actions work with App Router)
→ Append directly
```

### Example 2: Clear Contradiction
```
Existing: "Use MongoDB for database"
New: "Use PostgreSQL with Prisma"
→ Clear conflict (different databases)
→ Ask: "This contradicts MongoDB decision from 2025-01-12. Supersede it?"
```

### Example 3: Partial Contradiction
```
Existing: "Use REST API for all endpoints"
New: "Use tRPC for admin endpoints"
→ Partial conflict (different approach for subset)
→ Ask: "This modifies REST decision from 2025-01-15. Is this an exception or full replacement?"
```

### Example 4: Enhancement, Not Contradiction
```
Existing: "Use TypeScript for type safety"
New: "Use Zod for runtime validation"
→ No conflict (complementary)
→ Append directly
```

---

## Decision Entry Examples

### Example 1: Simple Pattern Choice
```markdown
## [2025-01-15] Server Actions for Mutations

**Status**: Current

**Decision**: Use Server Actions instead of API routes for all data mutations

**Reason**: Co-location with components, automatic revalidation, simpler error handling

**Alternatives considered**:
- API routes: More boilerplate, separate files, manual revalidation
- tRPC: Additional dependency, steeper learning curve

**Implications**:
- Requires Next.js 14+
- Server components by default
- Simpler form handling with useFormState
- Cannot use from client-side JavaScript outside React components

**Supersedes**: None
```

### Example 2: Technology Change (with Supersession)
```markdown
## [2025-01-10] Use Prisma for Database Access

**Status**: Superseded

**Decision**: Use Prisma ORM for all database access
...

---

## [2025-01-20] Switch to Drizzle ORM

**Status**: Current

**Decision**: Replace Prisma with Drizzle ORM for database access

**Reason**: Better TypeScript inference, lighter runtime, SQL-first approach matches team preference

**Alternatives considered**:
- Keep Prisma: Good docs but migrations too magical, type inference issues
- Raw SQL: Too verbose, no type safety

**Implications**:
- Migration from Prisma schema to Drizzle schema required
- All existing database queries need rewrite
- Smaller bundle size
- Better control over generated SQL

**Supersedes**: [2025-01-10] Use Prisma for Database Access
```

### Example 3: Architectural Pattern
```markdown
## [2025-01-25] Component Composition Over Prop Drilling

**Status**: Current

**Decision**: Use component composition pattern instead of prop drilling for deeply nested component trees

**Reason**: Reduce coupling, improve reusability, avoid prop drilling through 3+ levels

**Alternatives considered**:
- Context API: Overkill for non-global state
- Prop drilling: Becomes unmaintainable past 3 levels
- State management library: Too heavy for POC

**Implications**:
- Components accept children as props
- Wrapper components handle data fetching
- Leaf components receive data directly
- May need to restructure existing deeply nested components

**Supersedes**: None
```

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
- [ ] Entry appended to architecture.md
- [ ] Includes decision statement
- [ ] Includes rationale (WHY)
- [ ] Includes alternatives considered
- [ ] Includes implications
- [ ] Notes what it supersedes (if applicable)
- [ ] No contradictions with existing decisions (or user confirmed supersession)
- [ ] Consistency with stack.md verified
<!-- /SECTION:success-criteria -->
---

## Common Scenarios

### Scenario 1: User Makes Decision During Planning

```
User: "Let's use Server Actions for all mutations"

Claude (shipkit-architecture-memory):
1. Read .shipkit/architecture.md (check contradictions)
2. Read .shipkit/stack.md (verify Next.js version)
3. Decision is clear from statement → Skip "What was decided?" question
4. Ask: "Why Server Actions over API routes?"
5. User: "Co-location and simpler error handling"
6. Ask: "What are the implications?"
7. User: "Requires Next.js 14+"
8. Check for contradictions → None found
9. Append to architecture.md
10. "✓ Decision logged. Run /shipkit-plan to create implementation plan?"
```

### Scenario 2: Decision Contradicts Existing Choice

```
User: "Actually, let's use GraphQL instead"

Claude (shipkit-architecture-memory):
1. Read .shipkit/architecture.md
2. Find existing: "Use REST API for all endpoints"
3. Detect contradiction
4. Ask: "This contradicts REST decision from 2025-01-12. Supersede it?"
5. User: "Yes"
6. Ask: "Why GraphQL over REST?"
7. User: "Better for our complex data relationships"
8. Append decision with "Supersedes: [2025-01-12] REST API"
9. "✓ Decision logged and supersedes REST decision"
```

### Scenario 3: Complex Decision Needs Extended Docs

```
User: "We're using microservices with event-driven architecture"

Claude (shipkit-architecture-memory):
1. Ask clarifying questions
2. Append decision to architecture.md
3. Detect complexity (multiple implications, affects multiple systems)
4. Suggest: "This is a significant architectural change. Run document manually to create extended architecture documentation?"
```

---

## Tips for Effective Decision Logging

**Capture WHY, not just WHAT**:
- ✅ "Use Server Actions for co-location and simpler error handling"
- ❌ "Use Server Actions"

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
- Decision log, not essay
- 3-5 implications max
- 2-3 alternatives max

**When to upgrade to full /architecture-memory**:
- Multi-team coordination needed
- Decision approval workflows required
- Architecture diagrams needed
- Cross-repository decision tracking
- Formal ADR process required

---

**Remember**: This is a decision log, not comprehensive architecture documentation. Log decisions as they're made to maintain context. For detailed architecture docs, use `document manually`.