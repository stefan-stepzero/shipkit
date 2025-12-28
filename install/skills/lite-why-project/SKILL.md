---
name: lite-why-project
description: Define project vision in one page. Captures who it's for, why it exists, current state, future vision, and how you're getting there. Auto-loads at session start for strategic context.
---

# lite-why-project - Project Vision & Strategy

**Purpose**: Create a one-page strategic overview that answers: Who is this for? Why does it exist? Where are we? Where are we going? How are we getting there?

**What it does**: Asks 5 core questions, generates `.shipkit-lite/why.md`, provides strategic context for all future sessions.

---

## When to Invoke

**User triggers**:
- "Define the project vision"
- "Why are we building this?"
- "What's this project about?"
- "Create project overview"
- "Set the strategic direction"

**Auto-suggested**:
- Session start if `why.md` doesn't exist (via lite-session-start.py)

**Use cases**:
- Starting a new project (first skill after lite-project-context)
- Onboarding team members (share why.md)
- Before major architectural decisions (check alignment with vision)
- When project direction shifts (update the vision)

---

## Prerequisites

**None** - This can be the first skill you run (even before lite-project-context)

**Recommended order:**
1. `/lite-why-project` - Define strategic vision
2. `/lite-project-context` - Scan technical stack
3. Start building

---

## Process

### Step 1: Check if why.md Already Exists

**Before starting, check:**

```
If .shipkit-lite/why.md exists:
  → Ask user: "A project vision already exists. Would you like to:"
     1. View current vision
     2. Update vision (will overwrite)
     3. Cancel

  If user chooses "View":
    → Read and display why.md
    → Done

  If user chooses "Update":
    → Read old why.md (for context)
    → Proceed to Step 2 (show old answers as defaults)

  If user chooses "Cancel":
    → Exit

If .shipkit-lite/why.md does NOT exist:
  → Proceed directly to Step 2
```

---

### Step 2: Ask the 5 Core Questions

**Ask questions ONE AT A TIME** - Wait for user answer before asking next.

**Tone**: Conversational, helpful, not interrogative.

---

#### Question 1: Who Is This For?

**Ask:**
```
Let's define your project vision. This will help me make better suggestions aligned with your goals.

Question 1 of 5: Who is this project for?

Think: target users, audience, or stakeholders.

Examples:
  • "Solo developers building side projects"
  • "Small teams at early-stage startups"
  • "Enterprise customers needing compliance tools"
  • "Myself - learning new framework"

Your answer:
```

**Capture**: 1-3 sentences max

**If updating (old answer exists):**
```
Current answer: "{old answer}"

Has this changed? (Enter new answer, or press Enter to keep current)
```

---

#### Question 2: Why Does This Exist?

**Ask:**
```
Question 2 of 5: Why does this project exist?

Think: What problem are you solving? What value does it provide?

Examples:
  • "Developers waste time re-explaining context to AI every session"
  • "No good tool for tracking architecture decisions in small projects"
  • "Need to automate our manual deployment process"
  • "Learning React by building something real"

Your answer:
```

**Capture**: 1-3 sentences max

**If updating (old answer exists):**
```
Current answer: "{old answer}"

Has this changed?
```

---

#### Question 3: Where Are We Now?

**Ask:**
```
Question 3 of 5: Where are we now?

Think: Current state - POC? MVP? Beta? Production? Just starting?

Examples:
  • "Early POC - proving the concept works"
  • "MVP with core features, testing with 10 users"
  • "Production app, adding new features"
  • "Just started - have idea, no code yet"

Your answer:
```

**Capture**: 1-2 sentences max

**If updating (old answer exists):**
```
Current answer: "{old answer}"

Has this changed?
```

---

#### Question 4: Where Do We Need To Be?

**Ask:**
```
Question 4 of 5: Where do we need to be?

Think: Vision, success state, what "done" looks like (even if far away)

Examples:
  • "Stable product used by 100+ developers daily"
  • "Launched and making $1k/month MRR"
  • "Feature complete, ready to hand off to team"
  • "Personal tool I use every day, well-documented"

Your answer:
```

**Capture**: 1-3 sentences max

**If updating (old answer exists):**
```
Current answer: "{old answer}"

Has this changed?
```

---

#### Question 5: How Are We Getting There?

**Ask:**
```
Question 5 of 5: How are we getting there?

Think: Approach, methodology, constraints, priorities

Examples:
  • "Ship fast, iterate based on feedback, keep it simple"
  • "TDD approach, deploy weekly, focus on reliability"
  • "Learn by doing, document as I build, no deadlines"
  • "Agile sprints, user testing every 2 weeks"

Your answer:
```

**Capture**: 1-3 sentences max

**If updating (old answer exists):**
```
Current answer: "{old answer}"

Has this changed?
```

---

### Step 3: Ask About Constraints & Priorities (Optional)

**After the 5 core questions, ask:**

```
Optional: Do you have specific constraints or priorities to note?

Examples:
  • Constraints: "Solo developer, limited time (5hrs/week)", "Must use Python"
  • Priorities: "Speed over perfection", "UX is #1 priority"

Enter constraints/priorities (or press Enter to skip):
```

**If user provides content:**
- Capture it
- Include in why.md

**If user skips:**
- Omit this section from why.md

---

### Step 4: Generate why.md

**Use Write tool to create:**

**Location**: `.shipkit-lite/why.md`

**Template:**

```markdown
# Why This Project

**Created**: {First creation date - preserve if updating}
**Last Updated**: {Current date}

---

## Who Is This For?

{Answer to Question 1}

---

## Why Does This Exist?

{Answer to Question 2}

---

## Where Are We Now?

{Answer to Question 3}

---

## Where Do We Need To Be?

{Answer to Question 4}

---

## How Are We Getting There?

{Answer to Question 5}

{IF CONSTRAINTS/PRIORITIES PROVIDED:}
---

## Constraints & Priorities

{User-provided constraints/priorities formatted as bullets or paragraphs}
{END IF}
```

**Date handling:**
- **First time**: Set both Created and Last Updated to current date
- **Updating**: Keep original Created date, update Last Updated to current date

**Example output:**

```markdown
# Why This Project

**Created**: 2025-12-28
**Last Updated**: 2025-12-28

---

## Who Is This For?

Solo developers building side projects who need structure without complexity.

---

## Why Does This Exist?

Claude forgets context between sessions. Developers waste time re-explaining their stack, decisions, and goals every time. This solves that.

---

## Where Are We Now?

Early MVP with 17 core lite skills. Being tested by a handful of developers on POCs and side projects.

---

## Where Do We Need To Be?

Stable Lite edition with 20 skills used by 100+ developers. Full edition ready for teams working on complex projects.

---

## How Are We Getting There?

Prompt-driven skills (no bash complexity). Iterate quickly based on user feedback. Keep Lite simple and fast, Full comprehensive and powerful.

---

## Constraints & Priorities

**Constraints:**
- Solo maintainer, limited time
- Must work on Windows/Mac/Linux

**Priorities:**
1. Speed of execution (ship fast)
2. User experience (make it obvious)
3. Documentation (make it learnable)
```

---

### Step 5: Confirm to User

**After creating why.md:**

```
✅ Project vision defined

📁 Location: .shipkit-lite/why.md

📋 Summary:
  • Who: {Brief snippet from answer 1}
  • Why: {Brief snippet from answer 2}
  • Current: {Brief snippet from answer 3}

💡 This will auto-load at every session start to give me strategic context.
```

---

## Workspace Structure

**This skill creates:**

```
.shipkit-lite/
  why.md              # One-page strategic vision
```

**Auto-loaded at session start by `lite-session-start.py`**

---

## What Makes This "Lite"

**Included**:
- ✅ One page (not dozens)
- ✅ 5 core questions (not 50)
- ✅ 2-5 minutes to complete (not hours)
- ✅ High-level strategic context
- ✅ Auto-loads at session start
- ✅ Easy to update (overwrite entire file)

**Not included** (vs full ShipKit prod-* skills):
- ❌ Detailed personas (prod-personas)
- ❌ Jobs-to-be-done analysis (prod-jobs-to-be-done)
- ❌ Market analysis (prod-market-analysis)
- ❌ Brand guidelines (prod-brand-guidelines)
- ❌ Interaction design (prod-interaction-design)
- ❌ User stories with ACs (prod-user-stories)

**Philosophy**: Answer "why" in 5 minutes, not 5 hours. Provide enough strategic context for Claude to make aligned suggestions, without the ceremony of full product discovery.

---

## Difference from Full ShipKit

| Aspect | Full ShipKit (prod-*) | lite-why-project |
|--------|----------------------|------------------|
| **Time to complete** | 2-4 hours (10 skills) | 2-5 minutes (5 questions) |
| **Detail level** | Comprehensive product discovery | High-level strategic overview |
| **Output files** | 10+ files (personas, JTBD, market, brand, stories, etc.) | 1 file (why.md) |
| **When to use** | Greenfield products needing validation | POCs, MVPs, side projects |
| **Update frequency** | Rarely (major pivots only) | Anytime vision evolves |
| **Session loading** | Not auto-loaded (too large) | Auto-loads (~150 tokens) |

**Use lite-why-project for:**
- Side projects
- POCs and experiments
- MVPs and early products
- Learning projects
- Internal tools
- When you just need alignment, not validation

**Use full ShipKit prod-* skills for:**
- Startups raising funding
- Products needing market validation
- B2B SaaS with complex user types
- When you need detailed product artifacts
- Enterprise products

---

## Integration with Other Skills

**Before lite-why-project**:
- Nothing (can be first skill)

**After lite-why-project**:
- `/lite-project-context` - Scan technical stack
- `/lite-architecture-memory` - Log decisions aligned with vision
- `/lite-spec` - Create feature specs aligned with vision
- Any other skill - Claude now has strategic context

**When to use**:
- **New project**: Run this first (before even scanning stack)
- **Mid-project**: When you realize Claude doesn't understand your goals
- **Team onboarding**: Share why.md to align everyone
- **Vision shift**: When direction changes, update the vision

**How other skills use this**:
```
User: "Should we add OAuth or keep simple email auth?"

Claude (WITH why.md loaded):
"Given this is for solo developers (from why.md) with priority
 'ship fast' (from why.md), simple email auth aligns better.
 OAuth adds complexity that doesn't serve your vision of speed."

Claude (WITHOUT why.md):
"Both are valid. OAuth is more flexible but complex.
 Email auth is simpler but less feature-rich. What do you prefer?"
```

---

## Context Files This Skill Reads

**On update (if why.md exists)**:
- `.shipkit-lite/why.md` - Read old answers as defaults

**Never reads other files** - This is the starting point

---

## Context Files This Skill Writes

**Creates/Updates**:
- `.shipkit-lite/why.md` - OVERWRITE AND REPLACE
  - **Write Strategy**: OVERWRITE AND REPLACE
  - **Behavior**: Entire file regenerated when vision changes
  - **Why**: Represents current state, not history (like stack.md)
  - **Created date**: Preserved from original when updating
  - **Updated date**: Changed to current date

**Never modifies other files**

---

## Session Start Behavior

**lite-session-start.py will auto-load why.md:**

```python
# If why.md exists
why_file = project_root / '.shipkit-lite' / 'why.md'
if why_file.exists():
    print("# Project Vision (cached)")
    print()
    print(why_file.read_text(encoding='utf-8'))
    print()
    print("---")
    print()
```

**Result**: Claude starts every session knowing:
- Who the project is for
- Why it exists
- Current state
- Future vision
- Approach and priorities

**Token cost**: ~150 tokens (one-page document)

**Benefit**: Better suggestions aligned with strategic goals

---

## Success Criteria

Vision is defined when:
- [ ] User answered all 5 core questions
- [ ] Answers are high-level (1-3 sentences each)
- [ ] why.md created in `.shipkit-lite/`
- [ ] File follows template structure
- [ ] Dates are correct (Created preserved if updating)
- [ ] User knows vision will auto-load at session start
- [ ] Constraints/priorities included (if provided)

---

## Common Scenarios

### Scenario 1: Brand New Project

```
User: "Define the project vision"

Claude:
1. Check: why.md doesn't exist
2. Ask Question 1: "Who is this for?"
3. User: "Solo developers learning React"
4. Ask Question 2: "Why does this exist?"
5. User: "I need a real project to learn React hooks and state management"
6. Ask Question 3: "Where are we now?"
7. User: "Just started, have basic setup"
8. Ask Question 4: "Where do we need to be?"
9. User: "Working app I can show in portfolio, well-documented code I can reference later"
10. Ask Question 5: "How are we getting there?"
11. User: "Build feature by feature, document each pattern as I learn it"
12. Ask: Constraints/priorities?
13. User: "Priority: learning over shipping fast"
14. Write: why.md with all answers
15. Confirm: "Vision defined. Will auto-load at session start."
```

### Scenario 2: Updating Existing Vision

```
User: "Update the project vision"

Claude:
1. Check: why.md exists
2. Ask: "Vision exists. View, Update, or Cancel?"
3. User: "Update"
4. Read: old why.md
5. Ask Question 1: "Who is this for?"
   Show: "Current: Solo developers learning React"
   Ask: "Has this changed?"
6. User: "Now for small dev teams at startups"
7. Ask Questions 2-5 (showing old answers, asking for changes)
8. User updates answers 1 and 4, keeps others
9. Ask: Constraints/priorities?
10. User keeps old constraints
11. Write: why.md (preserve Created date, update Last Updated)
12. Confirm: Updated vision shown
```

### Scenario 3: Mid-Session Suggestion

```
[Session starts]
lite-session-start.py: "📝 No project vision found. Run /lite-why-project to define who/why/where"

User: "Scan my project"
Claude: Runs /lite-project-context

User: "Should I use TypeScript or JavaScript?"
Claude: "Before I recommend, would you like to run /lite-why-project?
         Knowing your goals (learning vs shipping, team size, priorities)
         will help me give you a better answer."

User: "/lite-why-project"
Claude: [Runs through 5 questions]
Claude: "Now that I know this is a learning project with priority on
         understanding fundamentals, I'd recommend starting with JavaScript.
         Once you're comfortable, add TypeScript to learn type systems."
```

---

## Tips for Effective Vision Definition

**Keep it concise**:
- 1-3 sentences per question
- High-level, not detailed
- Strategic, not tactical

**Be honest**:
- "Learning project" is valid
- "Just for me" is valid
- "No deadline" is valid

**Think about Claude's decisions**:
- Your answers will influence every suggestion Claude makes
- Example: "Priority: speed" → Claude suggests simpler solutions
- Example: "Priority: learning" → Claude suggests educational approaches

**Update when things change**:
- Pivot from solo to team? Update.
- Shift from POC to production? Update.
- Changed priorities? Update.

**Share with team**:
- why.md is onboarding documentation
- Gets everyone aligned on vision
- Reference it in discussions

---

## When NOT to Use This Skill

**Skip lite-why-project if:**
- You're doing a 10-minute code spike (too small)
- You're modifying someone else's codebase (not your vision to define)
- You're following strict requirements (vision already defined elsewhere)

**Use full ShipKit prod-* skills if:**
- Raising funding (need comprehensive business case)
- Validating market (need market analysis)
- Complex product (need detailed personas, JTBD)
- B2B SaaS (need multiple user types mapped)

---

## Example Output

**File**: `.shipkit-lite/why.md`

```markdown
# Why This Project

**Created**: 2025-12-28
**Last Updated**: 2025-12-28

---

## Who Is This For?

Solo developers building side projects who want structure without complexity. People who have good ideas but get lost in implementation without a framework.

---

## Why Does This Exist?

Claude Code is powerful but forgets everything between sessions. Developers waste 10-15 minutes every session re-explaining their stack, architecture decisions, and project goals. This framework gives Claude persistent memory.

---

## Where Are We Now?

Early MVP with 18 lite skills. Being tested by a handful of developers on POCs and side projects. Core patterns proven, ready to expand.

---

## Where Do We Need To Be?

Stable Lite edition with 20 skills, used by 100+ developers daily. Full edition ready for teams working on complex greenfield products. Solid documentation so anyone can install and use it.

---

## How Are We Getting There?

Ship quickly, iterate based on user feedback. Keep Lite simple (prompt-driven, no bash complexity). Make Full comprehensive (full product discovery + dev workflow). Document everything as we build.

---

## Constraints & Priorities

**Constraints:**
- Solo maintainer with limited time (~10 hours/week)
- Must work cross-platform (Windows/Mac/Linux)
- No external dependencies (just Claude Code + Python)

**Priorities:**
1. Speed of execution (ship fast, iterate)
2. Developer experience (make it obvious)
3. Documentation (make it learnable)
```

---

**Remember**: This is strategic context, not requirements. Keep it high-level. Answer "why" not "how". Think vision, not spec. Claude will use this to make better decisions aligned with your goals.
