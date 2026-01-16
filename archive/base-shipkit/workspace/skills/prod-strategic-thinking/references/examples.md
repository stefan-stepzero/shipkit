# Strategic Thinking Examples

Concrete examples of completed business canvases for different business models and stages.

---

## Example 1: B2C SaaS (MVP Stage)

### Product: "FocusTime" - Deep Work Timer for Remote Workers

**Context:**
- Product Status: Brand new
- Development Phase: MVP
- Business Model: B2C SaaS

---

#### Section 1: Core Value Proposition

**The Problem:**
Remote workers struggle to maintain focus with constant Slack/email interruptions. Average knowledge worker is interrupted every 3 minutes, destroying deep work.

**For whom specifically:**
Remote software engineers, designers, writers who need uninterrupted focus time for creative/complex work.

**Why is this problem worth solving now:**
Remote work explosion (2020-2025) created always-on culture. Studies show it takes 23 minutes to regain focus after interruption. This kills productivity and causes burnout.

**How painful is this problem:**
- Frequency: Every workday, multiple times
- Impact: 2-3 hours lost productivity daily = $50-100/day for high-earners
- Current alternatives: Manual DND mode (forget to turn off), Pomodoro apps (don't integrate with communication tools)

**What makes your solution different:**
Auto-integrates with Slack/email/calendar to create protected focus blocks. AI learns your optimal focus times. Team-aware (colleagues see you're in focus mode).

**Why you:**
Founded by ex-Google engineer who researched attention/productivity. Deep expertise in calendar/communication APIs.

**The "Aha!" moment:**
Realized people don't lack willpower - they lack systems that protect their attention.

---

#### Section 2: Target Market & Customers

**Primary Customer:**
Remote knowledge workers at tech companies, age 25-45, earning $80K+, value productivity and work-life balance.

**Where are they today:**
- Digital: r/productivity, Hacker News, Product Hunt, productivity YouTubers
- Professional: Tech companies with remote-first policies
- Geographic: North America, Europe (English-speaking initially)

**Market Size:**
- TAM: 50M remote knowledge workers globally
- SAM: 10M in English-speaking countries using Slack
- SOM Year 1: 10K users (0.1% of SAM)

**Market Growth:**
Growing 20% YoY as remote work becomes permanent.

**Primary Segment:**
Individual contributors at tech companies (engineers, designers, PMs) who use Slack daily and value deep work.

**Out of Scope:**
- Non-remote workers (different problem)
- Industries without Slack (insurance, healthcare, government)
- Managers (different workflow, more meeting-heavy)

---

#### Section 3: Success Criteria

**North Star Metric:**
Hours of protected deep work per user per week

**Why this metric:**
Directly measures value delivered (more focus time) and predicts retention (users who get >5 hours/week stay).

**MVP Success:**
- [ ] 1,000 signups in first month
- [ ] 40% activate (create first focus session)
- [ ] 20% weekly active users
- [ ] Average 3+ focus sessions per active user per week
- [ ] Net Promoter Score > 40

**Leading Indicators:**
- Focus sessions started (predicts engagement)
- Slack integration connected (predicts activation)
- First week retention (predicts long-term retention)

**Lagging Indicators:**
- Monthly recurring revenue
- Customer lifetime value
- Churn rate

**Measurement:**
- Tool: Mixpanel for product analytics
- Frequency: Daily dashboard review, weekly deep dive
- Owner: Founder (for now)

---

#### Section 4: Business Model

**Revenue Model:**
Freemium SaaS subscription

**Pricing:**
- Free: 5 focus sessions/month
- Pro: $8/month - unlimited sessions, analytics, Slack+calendar integration
- Team: $6/user/month - shared team calendar, focus mode visibility

**Reasoning:**
Price point based on competitor analysis (Freedom app: $7/mo, RescueTime: $12/mo). Positioning between them. Low enough for individual purchase, high enough for sustainable unit economics.

**LTV:**
- Estimated LTV: $192 (2 years * $8/month)
- Assumption: 70% annual retention, users stay 2 years average

**Cost Structure:**
- Fixed: $500/month (hosting, tools, domain)
- Variable: $0.50/user/month (infrastructure)
- CAC: $20 (organic + content marketing)

**Unit Economics:**
- LTV:CAC = 9.6:1 ✓ (healthy)
- Gross margin: 94% ($8 revenue - $0.50 COGS)
- Payback period: 2.5 months

**Path to Profitability:**
Break even at 100 paying customers ($800 MRR covers fixed costs). Target: Month 6.

**Critical Assumptions:**
- 20% free-to-paid conversion (validate: industry standard 2-5%, we need better)
- $20 CAC via content marketing (validate: run content experiments)
- 70% annual retention (validate: cohort analysis after 3 months)

---

## Example 2: B2B SaaS (Adding Feature to Existing Product)

### Product: "CodeReview AI" - Adding Auto-Code-Review Feature

**Context:**
- Product Status: Adding to existing product
- Development Phase: Established product (5K users, $500K ARR)
- Business Model: B2B SaaS

---

#### Section 1: Core Value Proposition

**The Problem:**
Engineering teams spend 20-30% of time on code reviews. Reviews are slow (2-3 day lag), inconsistent (style varies by reviewer), and burn out senior engineers.

**For whom:**
Engineering teams at fast-growing tech companies (50-500 person engineering orgs) who use GitHub/GitLab.

**Why now:**
AI (GPT-4) can now detect bugs, style issues, security vulnerabilities with 85%+ accuracy. Teams are drowning in PRs as codebases grow.

**What makes this different:**
Integrates with existing CodeReview product (already has GitHub integration, team context). AI suggestions learn from your team's past reviews. Human reviewers focus on architecture, not style.

**Why you:**
We already serve 5K engineering teams. Have integration infrastructure. AI augments existing workflow vs. new tool.

---

#### Section 2: Target Market & Customers

**Existing Persona Alignment:**
✓ Serves existing "Engineering Manager" persona
✓ Also appeals to "Senior Engineer" persona (reduces review burden)

**Primary Segment:**
Existing customers with >20 engineers, >100 PRs/week, GitHub Enterprise.

**Market:**
- TAM: Our existing 5K customers (upsell opportunity)
- Target: 500 customers upgrade to AI tier (10% conversion)

---

#### Section 3: Success Criteria

**Feature Success:**
- [ ] 500 customers upgrade to AI tier ($50/month add-on)
- [ ] AI review adoption: 80% of PRs get AI review
- [ ] Time savings: 30% reduction in manual review time
- [ ] Quality: <5% false positive rate on AI suggestions

**Leading Indicators:**
- AI tier trial starts
- First AI review run
- Developer accepts AI suggestion

---

#### Section 4: Business Model

**Status:** Complete (reference existing)

**Revenue Impact:**
- Add-on: $50/month per team (5-50 engineers)
- Target: 500 customers * $50 = $25K MRR ($300K ARR)
- Increases overall ARR by 60%

**Cost:**
- AI API costs: $10/team/month (OpenAI)
- Gross margin: 80% ($50 - $10)

**Existing Business Model:**
(Reference `.shipkit/skills/prod-strategic-thinking/outputs/business-canvas.md` for full model)

---

## Example 3: Side Project / Indie Hacker (POC Stage)

### Product: "LocalSEO" - SEO Tool for Local Businesses

**Context:**
- Product Status: Brand new
- Development Phase: Proof of Concept
- Business Model: Side project (solo founder)

---

#### Section 1: Core Value Proposition (Lite)

**The Problem:**
Local businesses (restaurants, plumbers, dentists) lose customers to competitors because they don't show up in Google Maps. They know they need SEO but don't understand it.

**For Whom:**
Small local business owners (1-10 employees) in competitive markets.

**Solution:**
Dead-simple tool: enter your business, get a checklist of 10 things to fix to rank better. No jargon, just "do this, then that."

**Why Now:**
Google Business Profile changes made local SEO easier to impact (2023-2024). Opportunity for non-technical tool.

---

#### Section 2: Target Customer (Lite)

**Primary:**
Restaurant/cafe owners in mid-size cities (100K-500K population), age 35-55, not tech-savvy.

**Where to Find:**
Local business Facebook groups, Nextdoor, local chamber of commerce, restaurant industry forums.

---

#### Section 3: Success Criteria (Lite)

**POC Success = Validation:**
- [ ] 10 local business owners confirm they have this problem
- [ ] 7/10 say they'd pay $20/month for simple solution
- [ ] Build basic version in 2 weekends
- [ ] 3 businesses try it and see ranking improvement in 30 days

**Key Metric:**
Number of businesses that see Google Maps ranking improvement.

---

#### Section 4: Business Model (Deferred)

**Status:** Deferred - validate problem first

**Rough Plan:**
- $20-30/month subscription
- Target: 100 customers = $2K-3K MRR
- Goal: Profitable side income, not full-time business

---

## Anti-Example: What NOT to Do

### ❌ Bad Strategy: "TaskMaster Pro"

**The Problem:**
People need to manage tasks.

**For Whom:**
Everyone.

**Solution:**
A task manager app.

**Why This is Bad:**
- Problem too vague (what specific pain?)
- Target too broad (everyone = no one)
- No differentiation (1000+ task apps exist)
- No unfair advantage
- No reason to believe you can win

### ✅ Good Version: "TaskMaster for ADHD Adults"

**The Problem:**
Adults with ADHD struggle with traditional task managers - too much friction to add tasks, easy to forget to check, overwhelming lists cause paralysis.

**For Whom:**
Diagnosed ADHD adults (25-45) who've tried Todoist/Things and stopped using them.

**Solution:**
Voice-first task capture (no typing friction), AI automatically prioritizes to top 3 tasks (reduces overwhelm), gentle nudges throughout day (addresses forgetting).

**Why You Can Win:**
Founder has ADHD, deeply understands the problem. Spent 2 years researching ADHD task management. Partnering with ADHD coaches for distribution.

**Unfair Advantage:**
Deep user research (100+ interviews with ADHD adults), partnerships with ADHD community influencers.

---

Use these examples as templates when completing your own business canvas. Notice how specific, focused strategies are more actionable than vague, broad ones.
