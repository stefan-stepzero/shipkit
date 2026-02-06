# Claude Thinking Partner — Concept Notes

**Status:** Concept / Future development
**Form factor:** Skill initially, but evaluate whether MCP plugin is better fit (plugin could be reusable across projects, not Shipkit-specific)

---

## Core Idea

A discussion-mode skill that restricts tool access to force genuine dialogue rather than execution. Claude becomes a thinking partner, not a doer.

## Key Design Principles

### 1. Tool Restriction as Interaction Design
- No Edit, Write, Bash — removes the escape hatch into "let me just build it"
- Forces Claude to stay in the problem space with the human
- The restriction IS the feature

### 2. Cognitive Outsourcing Frameworks
Generalised cognitive scaffolding Claude can apply:
- Decision matrices, weighted criteria
- First principles decomposition
- Pre-mortems, consequence mapping
- Devil's advocate / reality testing
- Blind spot detection
- Option evaluation with factors, weightings, rubrics

These aren't rigid templates — they're lenses applied based on what the discussion needs.

### 3. Semantic Exit Criteria
- On entry, Claude scopes the discussion and proposes exit criteria
- Criteria are semantic, not mechanical ("user has articulated a clear preference with stated reasoning" not "asked 5 questions")
- Discussion holds open until criteria are satisfied
- Claude tracks which criteria are met vs still open
- User can override with a stopbook/circuit-breaker, but default pressure is toward completeness
- Exit criteria force the HUMAN to do the thinking — Claude can't resolve them alone

### 4. Unknown Unknown Detection
- Claude simultaneously tracks what's been said AND infers what hasn't
- Detects knowledge gaps, unexamined assumptions, missing factors
- Probes gently: "have you thought about how X interacts with Y?"
- Can add implicit exit criteria when it detects prerequisite questions the user hasn't considered
- Models what a great senior colleague does — notices what you're skipping over

### 5. User-Specific Discussion Preferences
- Some people want Socratic questioning ("What would happen if...?")
- Others want direct assessment ("Option B is stronger because...")
- Preferences captured and applied per user

## Flow

1. **Entry** — User invokes with a topic
2. **Scoping** — Claude proposes exit criteria (including implicit ones from gap detection)
3. **Discussion** — Back and forth, cognitive frameworks applied as needed
4. **Tracking** — Ongoing awareness of resolved vs open criteria
5. **Exit** — Only when criteria satisfied → produce artifact or hand off to implementation

## Output
- The discussion itself is the primary artifact
- Optionally produces: decision document, weighted scorecard, "what we concluded and why" summary
- Persistent output could go to `.shipkit/` for session memory

## Commercialisation Strategy

**Phase 1: Validate in Shipkit**
- Build as `shipkit-thinking-partner` skill
- Test with real usage, iterate on the mechanics
- Refine cognitive frameworks, exit criteria logic, gap detection

**Phase 2: Extract as standalone product**
- If proven valuable, package as independent MCP plugin or standalone tool
- Not tied to Shipkit — works with any Claude Code setup (or broader)
- Monetisable: this solves a universal problem, not a dev-tooling niche one
- Target: anyone using AI as a thinking partner (product managers, founders, strategists, not just devs)

**Why this order:** Shipkit gives a controlled environment to validate. No point packaging something that doesn't work. But the concept itself is domain-agnostic — the TAM is much bigger than developer tooling.

## Use Cases
- "Which of these 3 approaches should we take?"
- "What am I not seeing here?"
- "Help me think through the implications of X"
- "Is this actually a good idea or am I just excited?"
- Architecture decisions, technology choices, product direction
- Any decision that benefits from structured thinking before action
