---
name: prod-discussion
description: "Use when facing product decisions, trade-offs, or 'should we' questions. Facilitates structured decision-making through option exploration and trade-off analysis. Conversational skill that creates no artifacts - purely guidance-focused."
---

# Product Discussion

**Facilitates product decisions through trade-off analysis and structured option exploration.**

---

## What This Skill Does

This is a **conversational skill** that Claude invokes when you:
- Ask product questions ("Should we build X?")
- Challenge decisions ("Why are we doing Y?")
- Posture ideas ("I think we should Z")
- Face trade-offs ("We can't have both A and B")

**Claude will:**
1. **Clarify** the real question behind your ask
2. **Reframe** in trade-off language (what we optimize for vs what we give up)
3. **Present options** with pros/cons colored by best practices
4. **Recommend** based on context (stage, goals, constraints)

**This is NOT a template-based skill.** No artifacts are created—it's purely conversational guidance.

---

## When Claude Should Invoke This

### Automatically Trigger When User:

**Asks "should we" questions:**
- "Should we add feature X?"
- "Should we pivot?"
- "Should we change pricing?"

**Requests recommendations:**
- "How should we price this?"
- "What's the best approach for Y?"
- "Which option is better?"

**Challenges or questions decisions:**
- "Why are we building X?"
- "This doesn't make sense because..."
- "What if we did Z instead?"

**Faces explicit trade-offs:**
- "We can't afford both X and Y"
- "Do we optimize for speed or quality?"
- "Should we go broad or deep?"

**Expresses uncertainty:**
- "I'm not sure if..."
- "What do you think about..."
- "Help me decide..."

---

## How to Use This Skill

### Step 1: Read References

Read all files in the skill's references directory:
```bash
.shipkit/skills/prod-discussion/references/
```

**If >2 files exist:** Ask the user which files are most relevant for this task.

This includes built-in guidance (reference.md, examples.md) and any user-added files (PDFs, research, notes).

---

### Step 2: Clarify the Real Question

**Don't take surface questions at face value.** Dig deeper.

**User says:** "Should we add dark mode?"

**Claude should ask:**
- "What's driving this request? Are users asking for it?"
- "Are competitors offering it?"
- "Is this about accessibility, aesthetics, or competitive parity?"
- "What problem does dark mode solve?"

**Clarifying questions to ask:**
1. **What's the underlying concern?** (Why are we discussing this?)
2. **What stage are we at?** (POC, MVP, Established)
3. **What are we optimizing for?** (Users, revenue, speed, quality)
4. **What's the constraint?** (Time, money, engineering capacity)

### Step 3: Reframe as Trade-Off

**Every decision involves trade-offs.** Make them explicit.

**Generic question → Trade-off framing:**
- "Should we build X?" → "Investment in X vs investment in Y, and what we give up"
- "How do we price?" → "More users at low price vs more revenue per user at high price"
- "Build or buy?" → "Control + customization vs Speed + focus"

**The trade-off template:**
```
"This decision is fundamentally about:
- **What we gain:** [Benefit A]
- **What we give up:** [Cost/Opportunity cost]
- **Alternative:** [Other ways to achieve similar outcome]
```

### Step 4: Present Options with Pros/Cons

**Always present 2-4 options, not just one.**

**Structure:**
```
**Option A: [Name]**
**Pros:**
- [Benefit 1]
- [Benefit 2]
**Cons:**
- [Trade-off 1]
- [Trade-off 2]
**Effort:** [S/M/L/XL]
**Impact:** [Low/Medium/High]
**Best for:** [When this option makes sense]

**Option B: [Alternative]**
[Same structure]

**Option C: [Another alternative or "Don't do it"]**
[Same structure]
```

**Color with best practices from references:**
- Reference SKILL frameworks from prod skills
- Cite industry benchmarks
- Note common patterns
- Warn about anti-patterns

### Step 5: Provide Context-Specific Recommendation

**Base recommendation on:**
1. **Stage:** POC focuses on learning, MVP on PMF, Established on growth
2. **Goals:** What are they optimizing for?
3. **Constraints:** Time, budget, team size
4. **Data:** What metrics/signals support the decision?

**Recommendation template:**
```
**My recommendation: [Option X]**

**Rationale:**
1. [Why this aligns with their stage]
2. [Why this matches their goals]
3. [What this enables next]

**What to measure:**
- [Metric to track if this was right decision]

**When to revisit:**
- [Conditions that would change recommendation]
```

---

## Decision Frameworks to Apply

### From references/reference.md:

**1. Impact vs Effort Matrix**
- High impact, low effort → Do now
- High impact, high effort → Plan carefully
- Low impact, low effort → Do if time
- Low impact, high effort → Don't do

**2. Reversibility Test**
- **Type 1 (one-way door):** Hard to reverse → Go slow, gather data
- **Type 2 (two-way door):** Easy to reverse → Go fast, experiment

**3. Opportunity Cost**
- "If we do X, what are we NOT doing?"
- Every yes is a no to something else

**4. First Principles**
- Strip away assumptions, reason from fundamentals
- Challenge industry norms

**5. Stage-Appropriate Thinking**
- **POC:** Speed > Quality, Learning > Building
- **MVP:** Core value > Edge cases, PMF > Revenue
- **Established:** Quality + Scale, Competitive moat

---

## Common Trade-Off Patterns

### 1. Speed vs Quality
- **Optimize for speed:** POC, competitive pressure, testing hypothesis
- **Optimize for quality:** Established product, high-stakes, reputation critical

### 2. Simplicity vs Flexibility
- **Optimize for simplicity:** Non-technical users, MVP, onboarding friction
- **Optimize for flexibility:** Power users, established, customization matters

### 3. Broad vs Deep
- **Broad (horizontal):** Large market, network effects, volume business
- **Deep (vertical):** Niche pain, high willingness to pay, deep integration

### 4. Build vs Buy
- **Build:** Core differentiator, unique requirements, long-term lower cost
- **Buy:** Commodity feature, fast time-to-market, focus on core

### 5. Self-Serve vs High-Touch
- **Self-serve:** Low price, simple product, SMB/consumer
- **High-touch:** High price, complex product, enterprise

---

## Integration with Other Prod Skills

**Reference these when relevant:**

**From prod-strategic-thinking:**
- What's the value proposition?
- Is this aligned with our differentiation?

**From prod-personas:**
- Which persona needs this?
- Does this serve our core user or edge case?

**From prod-market-analysis:**
- Is this table stakes or differentiator?
- What do competitors do?

**From prod-brand-guidelines:**
- Does this align with our brand personality?
- Is this true to our voice and values?

**From prod-interaction-design:**
- Does this fit the user journey?
- Where's the friction?

**From prod-user-stories:**
- What user value does this deliver?
- Is this must-have or nice-to-have (MoSCoW)?

**From prod-assumptions-and-risks:**
- What assumptions underpin this decision?
- What's the risk if we're wrong?

**From prod-success-metrics:**
- How will we measure if this was the right decision?
- What's the leading indicator?

---

## Examples from references/examples.md

**See examples.md for full walkthroughs of:**
1. Feature request discussion ("Should we add a mobile app?")
2. Pricing strategy discussion ("How should we price this?")
3. Build vs buy discussion ("Build auth or use Auth0?")
4. Scope reduction discussion ("Cut features to hit deadline?")
5. Competitive response discussion ("Competitor launched X, build it too?")

**Each example shows:**
- How to clarify the real question
- How to reframe as trade-off
- Multiple options with pros/cons
- Context-specific recommendation

---

## Anti-Patterns to Avoid

❌ **Jumping to solutions without clarifying:**
- User: "Should we add feature X?"
- Claude: "Yes, here's how to build it" (NO!)
- Claude: "Help me understand why feature X matters..." (YES!)

❌ **Giving one-size-fits-all answers:**
- "Best practice is to use freemium pricing" (NO!)
- "It depends on your stage, market, value prop..." (YES!)

❌ **Ignoring trade-offs:**
- "You should do both X and Y!" (Usually impossible)
- "X or Y? Here's the trade-off..." (Honest)

❌ **Recommending without context:**
- "Build feature X" (Why? Based on what?)
- "I'd recommend X because [stage/goals/constraints]" (Justified)

❌ **Being prescriptive instead of exploratory:**
- "You must do X" (Closes discussion)
- "Here are 3 options. What resonates?" (Opens discussion)

---

## Success Criteria

**You've used this skill well when:**

✅ **The user has clarity:**
- Understands the real question (not just surface ask)
- Sees the trade-offs explicitly
- Knows what they're optimizing for

✅ **Multiple options are presented:**
- Not just "do this" but "here are 3 paths"
- Pros/cons are honest and balanced
- Effort and impact are estimated

✅ **Context matters:**
- Recommendation changes based on stage/goals
- Best practices are applied, not blindly followed
- User's specific situation guides the answer

✅ **User can decide:**
- Has enough information to choose
- Understands implications of each option
- Knows how to measure if decision was right

---

## Tips for Facilitating Product Discussions

1. **Ask before telling:** Clarify context before recommending
2. **Present options:** Rarely is there only one right answer
3. **Make trade-offs explicit:** Surface what's gained and given up
4. **Reference best practices:** But adapt to context
5. **Recommend, don't dictate:** User makes final call
6. **Help them measure:** Define success criteria
7. **Stay stage-appropriate:** POC ≠ MVP ≠ Established

---

## When NOT to Use This Skill

**Don't invoke for:**
- Simple factual questions ("What's a persona?")
- Technical how-to ("How do I implement auth?")
- Requests for specific skills ("/prod-personas")
- Questions outside product domain (legal, HR, etc.)

**This skill is for:**
- Product strategy questions
- Feature prioritization discussions
- Trade-off analysis
- Decision-making under uncertainty

---

## Quick Reference

**User asks → Claude should:**
1. **Clarify:** What's the real question? What's the context?
2. **Reframe:** What trade-off is this really about?
3. **Present:** 2-4 options with honest pros/cons
4. **Recommend:** Based on stage, goals, constraints
5. **Help measure:** What metrics validate the decision?

**Remember:** This is conversational facilitation, not artifact creation. The value is in helping the user think through trade-offs and make informed decisions.
