# Persona Development Reference

Extended guidance for creating effective user personas.

## Table of Contents

- Creating research-based personas
- B2C vs B2B persona differences
- Persona validation methods
- Common persona antipatterns
- Using personas in product development

## Creating Research-Based Personas

### Data Sources (Ranked by Reliability)

**Primary Research (Most Reliable):**
1. **User Interviews** (1-on-1, 30-60 min)
   - Sample size: 5-10 per segment
   - Mix of current users, churned users, prospects
   - Open-ended questions about goals, pains, workflows

2. **Contextual Inquiry** (Shadowing)
   - Observe users in their natural environment
   - Understand actual behavior vs. reported behavior
   - Identify unstated needs and workarounds

3. **Surveys** (Quantitative validation)
   - Sample size: 100+ respondents
   - Validate hypotheses from interviews
   - Identify segment sizes and characteristics

**Secondary Research:**
4. **Analytics Data**
   - User behavior patterns
   - Feature usage statistics
   - Conversion funnels

5. **Support Tickets**
   - Common problems and pain points
   - Language users use to describe issues

6. **Sales Call Recordings**
   - Questions prospects ask
   - Objections they raise
   - Decision criteria they mention

**Tertiary Research (Use Cautiously):**
7. **Competitor Reviews**
   - What users like/dislike about alternatives
   - Unmet needs in the market

8. **Industry Reports**
   - Market trends and demographics
   - Validate against primary research

### Interview Guide Template

**Introduction (5 min):**
- Thank them for their time
- Explain purpose: Understanding their workflow, not selling
- Get permission to record
- Assure confidentiality

**Background (10 min):**
- Tell me about your role
- What's a typical day like?
- What tools do you use regularly?
- How long have you been in this role?

**Goals & Motivations (15 min):**
- What are you trying to achieve in your role?
- What does success look like for you?
- What metrics are you measured on?
- What motivates you?

**Pain Points & Frustrations (15 min):**
- What's the most frustrating part of your job?
- What takes up too much time?
- What tools or processes don't work well?
- If you could wave a magic wand, what would you change?

**Current Solutions (10 min):**
- How do you currently solve [problem]?
- What tools do you use?
- What workarounds have you created?
- What have you tried that didn't work?

**Decision Making (5 min):**
- How do you evaluate new tools/solutions?
- Who else is involved in purchasing decisions?
- What would make you switch from your current solution?

**Wrap-up:**
- Is there anything else I should have asked?
- Can I follow up if I have more questions?

### Synthesis Process

**Step 1: Affinity Mapping**
- Write each insight on a sticky note
- Group similar insights together
- Look for patterns across interviews

**Step 2: Identify Segments**
- What distinct groups emerge?
- What differentiates them?
- Are segments meaningful and actionable?

**Step 3: Create Proto-Personas**
- Draft personas based on patterns
- Include representative quotes
- Highlight segment-specific needs

**Step 4: Validate**
- Show personas to actual users
- Ask: "Does this sound like you?"
- Refine based on feedback

## B2C vs B2B Persona Differences

### B2C Personas

**Focus Areas:**
- Individual goals and motivations
- Personal pain points
- Lifestyle and values
- Emotional drivers
- Purchase decision is often solo

**Example Factors:**
- Age, gender, location
- Income, education
- Hobbies, interests
- Social media behavior
- Shopping preferences
- Brand affinities

**Use Cases:**
- Consumer apps
- E-commerce
- Entertainment
- Personal productivity
- Health & fitness

### B2B Personas

**Focus Areas:**
- Professional role and responsibilities
- Company goals and metrics
- Budget and procurement process
- Multiple stakeholders involved
- Longer sales cycles

**Example Factors:**
- Job title, seniority
- Company size, industry
- Department, team structure
- KPIs and success metrics
- Budget authority
- Technical requirements
- Compliance needs

**Decision-Making Unit:**
- **Champion:** Advocates for solution internally
- **Economic Buyer:** Controls budget
- **Technical Buyer:** Evaluates technical fit
- **End User:** Actually uses the product
- **Blocker:** Can veto the decision

**Use Cases:**
- SaaS tools
- Enterprise software
- B2B services
- Developer tools
- Business intelligence

### Hybrid: B2B2C Personas

**Marketplace/Platform Models:**
- Create personas for BOTH sides
  - Supply side (e.g., drivers, hosts, sellers)
  - Demand side (e.g., riders, guests, buyers)
- Understand dynamics between sides
- Balance needs of both groups

**Example: Rideshare**
- **Rider Persona:** Busy professional, values convenience
- **Driver Persona:** Part-time earner, values flexibility
- Platform must serve both

## Persona Validation Methods

### Quantitative Validation

**Segment Size:**
- Use survey data to estimate % of market
- Validate that segment is large enough to matter
- Example: "Technical Product Managers represent 15% of our target market"

**Behavioral Validation:**
- Use analytics to confirm behavior patterns
- Example: "Power users log in 5x/week (confirmed by data)"

### Qualitative Validation

**Quote Matching:**
- Include verbatim quotes from interviews
- If personas resonate, users should say "That's exactly what I think!"

**Scenario Testing:**
- Present scenarios to users
- Ask: "Would [Persona] do this?"
- Refine based on feedback

### Ongoing Validation

**Update Cadence:**
- Review quarterly: Check if assumptions still hold
- Update annually: Refresh with new research
- Major updates: When launching new features or entering new markets

**Signals to Update:**
- Product changes significantly
- Market shifts (new competitors, technology changes)
- User feedback suggests personas are outdated
- Analytics show behavior changes

## Common Persona Antipatterns

### 1. Fictional Personas (No Data)

**Bad:**
```markdown
## Sarah - Tech-Savvy Millennial

Sarah is 28, loves avocado toast, and uses Instagram daily...
```

**Problem:** Based on stereotypes, not research

**Good:**
```markdown
## Sarah - Technical Product Manager (Based on 12 interviews)

**Demographics:** 28-35 years old, based on interview sample
**Quote:** "I need tools that integrate with our existing stack, not another login to manage"
**Data source:** 12 interviews + 150 survey responses
```

### 2. Too Many Personas

**Bad:** Creating 15 different personas

**Problem:**
- Impossible to serve all effectively
- Dilutes focus
- Creates analysis paralysis

**Good:** 3-5 personas maximum
- **Primary:** 60-70% of users
- **Secondary:** 20-30% of users
- **Tertiary:** 5-10% of users (edge cases)

### 3. Demographic-Only Personas

**Bad:**
```markdown
## Persona 1
- Age: 25-34
- Gender: Female
- Income: $50-75K
```

**Problem:** Demographics don't predict behavior

**Good:** Focus on goals, pains, and behaviors
```markdown
## Performance-Driven Product Manager
- **Goal:** Ship features faster without sacrificing quality
- **Pain:** Too much time in status meetings
- **Behavior:** Uses keyboard shortcuts, automates repetitive tasks
```

### 4. Everyone Persona

**Bad:**
```markdown
Our persona is "anyone who needs productivity tools"
```

**Problem:** Too broad, can't make specific design decisions

**Good:**
```markdown
**Freelance Creative Professional:**
- Juggles multiple clients
- Needs to track time for billing
- Works across design, writing, consulting
```

### 5. Static Personas (Never Updated)

**Bad:** Created in 2020, never revisited

**Problem:**
- Markets change
- Products evolve
- User needs shift

**Good:**
- Quarterly review
- Annual refresh
- Update based on new research

## Using Personas in Product Development

### Feature Prioritization

**Ask:**
- Which persona needs this most?
- How does this align with their goals?
- Does this solve a significant pain point?

**Example Decision:**
```
Feature: Advanced keyboard shortcuts
Primary Persona: Power User (Yes, critical pain point)
Secondary Persona: Casual User (No, would confuse them)
Decision: Build, but make it opt-in/discoverable, not default
```

### Design Decisions

**Example: Navigation Structure**
```
Persona: Time-Constrained Manager
- Needs: Quick access to most common tasks
- Pain: Buried features, too many clicks

Design Implication:
- Prioritize top 5 actions in main navigation
- Move advanced features to settings
- Add search for power users
```

### Messaging & Marketing

**Persona-Specific Messaging:**
```
Persona: Budget-Conscious Startup Founder
Message: "Start free, pay only when you scale. No surprises."

Persona: Enterprise Security Officer
Message: "SOC 2 Type II certified. GDPR compliant. On-premise deployment available."
```

### Feature Spec References

When writing specs, reference personas:

```markdown
## Target Users

**Primary:** Performance-Driven Product Manager persona
- This feature solves their "too much time in meetings" pain
- Aligns with their "ship faster" goal

**Secondary:** Engineering Lead persona
- Provides visibility they need for team coordination
```

## Persona Documentation Standards

### Minimum Viable Persona

**Must include:**
- Name and title/role
- Primary goal
- Biggest pain point
- Current behavior/workflow
- Decision criteria

**Can skip (until you have data):**
- Exact age, demographics (unless relevant)
- Hobbies, lifestyle (unless relevant for B2C)
- Hypothetical scenarios

### Rich Persona

**Add when you have data:**
- Multiple goals (ranked)
- Multiple pain points (with severity)
- Technology usage patterns
- Buying process and timeline
- Empathy map
- Day-in-the-life scenario
- Direct quotes from research

## Resources

**Books:**
- "The User Is Drunk" - Richard Littauer
- "Lean Customer Development" - Cindy Alvarez
- "The Mom Test" - Rob Fitzpatrick

**Tools:**
- Xtensio (persona templates)
- Miro (empathy mapping)
- Dovetail (research synthesis)
- Airtable (persona database)

**Internal:**
- Template: `templates/persona-template.md`
- Empathy map: `templates/empathy-map-template.md`
- Examples: `examples.md`

---

Use this reference when developing personas to ensure they're research-based, actionable, and focused on behaviors over demographics.
