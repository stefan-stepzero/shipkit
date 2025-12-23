---
name: prod-constitution-builder
description: "Create product constitution defining scope, trade-offs, and quality standards for your project type. Use after strategic thinking or when user says 'set product principles', 'define project scope', 'create constitution'."
agent: prod-product-manager
---

# Product Constitution Builder

## Agent Persona

**Load:** `.claude/agents/prod-product-manager-agent.md`

Adopt: Product-focused, understands trade-offs, balances speed vs quality based on project stage.

## Purpose

Create a **product constitution** that defines scope boundaries, quality standards, and decision-making principles based on your project type.

**Critical:** This constitution guides ALL downstream product work (personas, JTBD, user stories, brand) by establishing what's in/out of scope and quality expectations.

## When to Trigger

User says:
- "Set product principles"
- "Define project scope"
- "Create product constitution"
- "What should we prioritize?"
- After completing `/prod-strategic-thinking`

Or explicitly:
- `/prod-constitution-builder`

## Prerequisites

**Recommended:**
- Strategic thinking complete (`.shipkit/skills/prod-strategic-thinking/outputs/business-canvas.md`)
  - Helps inform constitution choices
  - Not required (can create constitution standalone)

## Process

**Important:** Use your natural language understanding and judgment to determine the right maturity and business model flags. The script requires explicit flags - you decide them based on conversation, not keyword matching.

### Step 1: Choose Project Type

Present the user with **6 project type options:**

**1. B2B SaaS Greenfield**
- Building new enterprise product from scratch
- Focus: Enterprise features, compliance, scalability
- Quality: High (long sales cycles, feature depth matters)

**2. B2C SaaS Greenfield**
- Building new consumer product from scratch
- Focus: User experience, growth, simplicity
- Quality: Medium-High (fast iteration, user feedback loops)

**3. Experimental**
- Testing new technology or ideas
- Focus: Learning over shipping, document findings
- Quality: Low-Medium code, HIGH documentation

**4. Side Project MVP**
- 1-4 week minimal viable product
- Focus: Ship something real but basic
- Quality: Medium (balance speed and quality)

**5. Side Project POC**
- Days to 1 week proof of concept
- Focus: Validate idea as fast as possible
- Quality: Low (just prove it works)

**6. Existing Project**
- Adding Shipkit to established codebase
- Focus: Document current state, guide future work
- Quality: Match or exceed existing baseline

**Ask user:** "Which project type best describes what you're building?"

---

### Step 2: Determine Maturity and Business Model

Based on the user's project type choice, determine **two dimensions**:

**Maturity:** (timeline and quality expectations)
- `poc` - Days to 1 week, throwaway validation code
- `mvp` - 1-4 weeks, basic but real product
- `v1` - Months, professional quality product
- `established` - Existing mature codebase

**Business Model:** (target audience)
- `side-project` - Personal/hobby project
- `b2c` - Consumer product
- `b2b` - Enterprise product
- `marketplace` - Two-sided market

**Mapping from project types:**
- B2B SaaS Greenfield → `--maturity v1 --business-model b2b`
- B2C SaaS Greenfield → `--maturity v1 --business-model b2c`
- Experimental → `--maturity poc --business-model side-project`
- Side Project MVP → `--maturity mvp --business-model side-project`
- Side Project POC → `--maturity poc --business-model side-project`
- Existing Project → `--maturity established --business-model [b2c|b2b|side-project]`

---

### Step 3: Run Initialization Script

**CRITICAL:** Use your judgment to determine the correct flags based on the conversation with the user. The script requires explicit flags.

```bash
.shipkit/skills/prod-constitution-builder/scripts/build-constitution.sh \
  --maturity [poc|mvp|v1|established] \
  --business-model [side-project|b2c|b2b|marketplace]
```

**Example:**
```bash
# User building a weekend project to validate idea
.shipkit/skills/prod-constitution-builder/scripts/build-constitution.sh \
  --maturity poc --business-model side-project

# User building enterprise SaaS from scratch
.shipkit/skills/prod-constitution-builder/scripts/build-constitution.sh \
  --maturity v1 --business-model b2b
```

**Script will:**
1. Select appropriate template based on maturity + business model
2. Create `.shipkit/skills/prod-constitution-builder/outputs/product-constitution.md`
3. Report which template was used

---

### Step 4: Customize Constitution

Read the template loaded by the script, then customize it through conversation with the user:

#### For Greenfield Projects (B2B/B2C):

**Refine FORBIDDEN section:**
- Ask: "Are there specific features you want to explicitly rule out?"
- Example: "Should we forbid multi-tenancy for now?"

**Refine REQUIRED section:**
- Ask: "What are non-negotiable requirements?"
- Example: "Must support SSO? Must be GDPR compliant?"

**Refine ALLOWED section:**
- Ask: "What shortcuts are acceptable given your timeline?"
- Example: "Can we skip responsive design in V1?"

**Set Decision Framework:**
- Ask: "What's your primary constraint? Speed, quality, or features?"
- Adjust decision framework accordingly

#### For Experimental Projects:

**Define Clear Hypothesis:**
- Ask: "What specific question are you trying to answer?"
- Example: "Can WebAssembly handle real-time collaboration?"

**Set Success Criteria:**
- Ask: "How will you know if the experiment succeeded?"
- Example: "If latency < 50ms with 10 concurrent users"

**Time-box:**
- Ask: "How long are you willing to explore this?"
- Example: "2 weeks maximum"

#### For POC/MVP Projects:

**Define ONE Core Feature:**
- Ask: "What's the single most important thing this must do?"
- Example: "User can send a message and get AI response"

**Validation Criteria:**
- Ask: "How will you validate this is worth building?"
- Example: "5 people try it and 3 say they'd pay"

#### For Existing Projects:

**Document Current State:**
- Ask: "What tech stack is currently in use?"
- Ask: "What patterns already exist in the codebase?"
- Ask: "What's untouchable vs changeable?"

**Set Integration Strategy:**
- Ask: "Are we using Shipkit for all new features or gradually?"
- Ask: "What's the team's current workflow we must respect?"

---

### Step 5: Fill Template Placeholders

Replace these placeholders in the constitution:

- `[Date]` → Current date
- `[List...]` → Specific technologies/patterns/constraints
- `[e.g., ...]` → Actual examples from user's project
- Any bracketed questions → User's answers

**Write completed constitution to:**
```
.shipkit/skills/prod-constitution-builder/outputs/product-constitution.md
```

---

### Step 6: Validate with User

Read back the key sections:
- Prime Directive
- Top 3 FORBIDDEN items
- Top 3 REQUIRED items
- Primary decision framework

Ask: "Does this accurately capture your project's principles?"

If NO → Iterate on specific sections
If YES → Constitution complete!

---

## Outputs

**Primary:**
```
.shipkit/skills/prod-constitution-builder/outputs/product-constitution.md
```

**Format:** Markdown document with clear sections (FORBIDDEN, REQUIRED, ALLOWED, Decision Framework, Success Criteria)

---

## Next Steps After Constitution Complete

**Immediately:**
```bash
/prod-personas
```
- Personas shaped by project type (POC = 1 persona, Enterprise = 3-5 personas)

**Then continue product discovery pipeline:**
```bash
/prod-jobs-to-be-done
/prod-market-analysis
/prod-brand-guidelines
...
```

**Note:** All downstream product skills should reference this constitution to maintain consistency.

---

## Integration with Other Skills

**Called after:**
- `/prod-strategic-thinking` (recommended but optional)

**Informs:**
- `/prod-personas` - How many personas based on project type
- `/prod-jobs-to-be-done` - Depth of JTBD analysis based on scope
- `/prod-user-stories` - Acceptance criteria rigor based on quality standards
- `/prod-brand-guidelines` - Polish level based on project type
- `/dev-constitution` - Technical constitution builds on product constitution

**Example integration:**
- POC constitution → 1 persona, shallow JTBD, minimal brand guidelines
- B2B Greenfield → 3-5 personas, deep JTBD, comprehensive brand guidelines

---

## Constitution Lifespan

**When to update constitution:**
- Project transitions (POC → MVP → Production)
- Scope changes significantly
- Team size changes (solo → team)
- Quality standards evolve

**How to update:**
```bash
# Must still provide maturity and business-model flags
.shipkit/skills/prod-constitution-builder/scripts/build-constitution.sh \
  --maturity [current-or-new-value] \
  --business-model [current-or-new-value] \
  --update
```

**Note:** Changing constitution mid-project should be intentional and communicated to team.

---

## Template Details

### B2B SaaS Greenfield
**Best for:** Enterprise products, long sales cycles
**Emphasizes:** Compliance, scalability, feature depth
**Timelines:** Months to years
**Quality bar:** High

### B2C SaaS Greenfield
**Best for:** Consumer apps, growth products
**Emphasizes:** UX, virality, simplicity
**Timelines:** Weeks to months
**Quality bar:** Medium-High

### Experimental
**Best for:** Technology exploration, research
**Emphasizes:** Learning, documentation, failing fast
**Timelines:** Time-boxed (days to weeks)
**Quality bar:** Code low, docs high

### Side Project MVP
**Best for:** Nights/weekends, 1-4 week builds
**Emphasizes:** Ship something real, balance speed & quality
**Timelines:** 1-4 weeks
**Quality bar:** Medium

### Side Project POC
**Best for:** Idea validation, throwaway code
**Emphasizes:** Speed above all, prove concept
**Timelines:** Days to 1 week
**Quality bar:** Low (code is disposable)

### Existing Project
**Best for:** Adding Shipkit to established codebases
**Emphasizes:** Document current state, respect existing patterns
**Timelines:** Ongoing integration
**Quality bar:** Match or exceed baseline

---

## Decision Framework Examples

**POC Decision Framework:**
- Question: "Does this help me validate faster?"
- YES → Do it | NO → Don't do it

**B2B Greenfield Decision Framework:**
- Question: "Does this meet enterprise requirements?"
- YES → Required | NO → Check if blocking or nice-to-have

**Experimental Decision Framework:**
- Question: "Does this help me learn faster?"
- YES → Do it | NO → Don't do it
- Secondary: "Am I documenting learnings?"

---

## Common Patterns

**Transitioning between types:**

```
POC → MVP → B2C Greenfield → Production
├─ Validated idea (POC complete)
├─ Ship basic version (MVP complete)
├─ Professional quality (B2C Greenfield)
└─ Established product (update constitution to Existing Project)
```

**Starting points:**
- New idea → Start with POC
- Clear problem → Start with MVP
- Funded startup → Start with Greenfield (B2B or B2C)
- Existing codebase → Start with Existing Project
- Research question → Start with Experimental

---

## Constraints

**DO:**
- ✅ Choose template that matches actual project reality
- ✅ Be honest about constraints (time, quality, resources)
- ✅ Update constitution when project transitions
- ✅ Reference constitution in downstream product skills
- ✅ Keep constitution concise (<2 pages)

**DON'T:**
- ❌ Choose aspirational type (POC isn't "B2B Greenfield done quickly")
- ❌ Mix principles from multiple types (creates confusion)
- ❌ Skip constitution for "simple" projects (even POCs benefit)
- ❌ Update constitution casually (should be intentional decision)

---

## Red Flags

**Stop and reconsider if:**
- User wants POC quality but B2B timelines (pick one)
- Constitution has conflicting principles (e.g., "ship fast" + "perfect quality")
- FORBIDDEN list is empty (no boundaries = no focus)
- REQUIRED list has >10 items (too many must-haves)
- User can't articulate primary constraint (speed/quality/features)

---

## Quick Reference

| Project Type | Timeline | Quality | Output Use |
|--------------|----------|---------|------------|
| B2B Greenfield | Months | High | Enterprise product |
| B2C Greenfield | Weeks-Months | Med-High | Consumer product |
| Experimental | Time-boxed | Code: Low, Docs: High | Learning |
| Side MVP | 1-4 weeks | Medium | Real but basic |
| Side POC | Days-1 week | Low | Throwaway validation |
| Existing | Ongoing | Match baseline | Integration |

---

## Success Criteria

A good product constitution:
1. ✅ Clearly states project type
2. ✅ Defines what's FORBIDDEN (out of scope)
3. ✅ Defines what's REQUIRED (must-haves)
4. ✅ Provides decision framework for trade-offs
5. ✅ Sets realistic quality expectations
6. ✅ Is referenced by downstream product skills
7. ✅ Team agrees it reflects reality

---

**This skill establishes the foundation for all product work. Get this right, everything else flows from it.**
