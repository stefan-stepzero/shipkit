# Interaction Design Examples

Concrete examples of user journeys and interaction patterns for different product types.

---

## Example 1: B2B SaaS - Team Collaboration Tool

**Product:** ProjectSync (fictional team project management tool)
**Persona:** Sarah, Engineering Manager at Series B startup
**Job to Be Done:** Keep remote team aligned across timezones without constant meetings
**Stage:** MVP

### Journey: Sarah's First Week

#### Stage 1: Awareness (Day 0)

**Context:**
- Sarah's team scattered across 3 timezones
- Spending 2+ hours daily catching up on Slack, email, GitHub
- Colleague recommends ProjectSync: "Saves me an hour daily"

**Touchpoints:**
1. Google search: "async team alignment tools"
2. Lands on comparison article mentioning ProjectSync
3. Visits homepage

**User Questions:**
- "Is this just another Slack clone?"
- "Will my team actually use it?"
- "How long to set up?"

**Design Focus:**
- Homepage shows 3-minute demo video (not 20-minute walkthrough)
- Social proof: "Used by 500+ engineering teams"
- Clear differentiation: "Async-first, not chat-first"

---

#### Stage 2: First Use (Day 0, 5 minutes after signup)

**Onboarding Flow:**

**Screen 1: Sign up**
- Google SSO (1 click, no form)
- Detects company domain → "Invite team later or start solo?"
- Sarah chooses "Start solo" (explore first)

**Screen 2: Create first project**
- Pre-filled with example: "Q1 Product Launch"
- Template buttons: "Engineering", "Marketing", "General"
- Sarah clicks "Engineering" → project populated with sample tasks

**Screen 3: "Aha!" moment (90 seconds in)**
- Sample project shows: Daily standup (async), Sprint board, Decisions log
- Simulated team updates: "Alex: Deployed fix for login bug ✓"
- Sarah realizes: "This is what our scattered Slack threads should look like"

**Time to value: 90 seconds**
**Success metric: User creates their first real project**

---

#### Stage 3: Regular Use (Week 1)

**Core Flow: Daily Standup (Async)**

```
8:00 AM - Sarah opens ProjectSync
├─ Sees: "3 updates from yesterday" badge
├─ Clicks: Opens standup thread
│  ├─ Alex: "Finished auth refactor. PR ready for review."
│  ├─ Maria: "Blocked on API keys from DevOps"
│  ├─ Jordan: "Working on mobile responsive fixes"
│
├─ Sarah adds her update (3 minutes)
│  ├─ Template auto-loads: "Yesterday / Today / Blockers"
│  ├─ Mentions @DevOps for Maria's blocker
│  ├─ Clicks "Post update" → appears in thread
│
└─ Sarah reviews team updates (5 minutes)
   ├─ Clicks thumbs up on Alex's PR
   ├─ Adds comment on Maria's blocker
   └─ Marks standup as "Reviewed" → badge clears
```

**Total time: 8 minutes (vs. 30-minute meeting)**

**Habit Formation:**
- **Trigger:** Coffee in hand, start of workday
- **Action:** Check team updates (easy, 8 min)
- **Reward:** Feel aligned without meeting, help unblock Maria
- **Investment:** Posted own update (tomorrow expects responses)

---

#### Stage 4: Power Use (Week 2)

**Advanced Features Sarah Discovers:**

**Feature 1: Digest Email**
- Setting: Daily digest at 8 AM
- Email shows: Team updates since last check
- Sarah reads on phone during commute
- Clicks through to comment on urgent items

**Feature 2: Decision Log**
- Sarah documents: "Use PostgreSQL not MySQL"
- Links to Slack discussion and alternatives doc
- Team can reference later (no more "why did we decide this?")

**Feature 3: Keyboard Shortcuts**
- Sarah learns: `c` = create update, `/` = search, `g d` = go to decisions
- Saves 30 seconds per action (adds up!)

---

## Example 2: B2C Mobile App - Fitness Tracker

**Product:** FitPath (fictional fitness app)
**Persona:** Maria, 32, busy parent trying to stay healthy
**Job to Be Done:** Stay consistent with workouts despite chaotic schedule
**Stage:** POC

### Journey: Maria's First Month

#### Stage 1: Download & First Open (Day 0)

**Context:**
- New Year's resolution: Get fit
- Downloaded 3 fitness apps to try
- Has 5 minutes before kids wake up

**First Launch Flow:**

**Screen 1: Welcome**
- Simple: "Get fit in 10 minutes a day"
- Big button: "Start Free Trial"
- Skip option: "Just exploring"

**Screen 2: Quick Setup (60 seconds)**
- "What's your goal?" → Buttons: Lose weight / Build muscle / Stay active
- "How much time?" → Buttons: 10 min / 20 min / 30+ min
- "Experience level?" → Buttons: Beginner / Intermediate / Advanced
- Maria selects: Stay active / 10 min / Beginner

**Screen 3: First Workout Starts Immediately**
- No account creation (yet!)
- No payment (yet!)
- Video plays: 10-minute beginner yoga
- Maria completes it → Feels accomplished

**Screen 4: Post-Workout**
- "Great job! 🎉 How did that feel?"
- Buttons: Too easy / Just right / Too hard
- "Create account to track progress?" → Now she's motivated to sign up

**Time to value: 2 minutes (started workout)**
**Conversion moment: After first workout (dopamine high)**

---

#### Stage 2: Habit Formation (Week 1-2)

**Daily Pattern:**

**Morning Trigger:**
- Push notification: "☀️ Ready for today's 10-min workout?"
- Timing: 6:00 AM (user-selected)

**Workout Flow:**
```
Maria opens app
├─ Today's workout ready to start (no browsing needed)
├─ Taps "Start" → Video begins
├─ 10-minute workout
├─ Completion screen: "Day 4 streak! 🔥"
└─ Calendar marks day complete (visual progress)
```

**Streak Mechanic:**
- Shows consecutive days
- "Don't break your streak!" (gentle pressure)
- Misses a day → "Restart your streak today!"

**Social Proof:**
- After Day 7 → "Join 10,000 people who completed Week 1"

---

#### Stage 3: Expansion (Week 3-4)

**New Feature Discovery:**

**Contextual Prompt:**
- After Day 14 → "Workouts feeling too easy?"
- Offer: "Try intermediate level"
- Maria accepts → Gradually harder workouts

**Social Feature:**
- "Invite a friend, both get bonus week free"
- Maria invites sister → Social accountability

**Premium Upsell:**
- Shown after Day 21 (habit formed)
- "Unlock 100+ workouts, nutrition plans, personal coaching"
- Timing: When she's most engaged

---

## Example 3: E-Commerce - Online Furniture Store

**Product:** HomeCraft (fictional furniture retailer)
**Persona:** Kevin, 28, furnishing first apartment
**Job to Be Done:** Find furniture that fits space and budget without making expensive mistakes
**Stage:** Established

### Journey: Kevin Buys a Sofa

#### Stage 1: Discovery (Day 0)

**Context:**
- Empty living room (just moved in)
- Budget: $500-800 for sofa
- Measuring space on phone: 7 feet wide

**Entry Point: Google search "modern sofa under $800"**

**Landing Page:**
- Sees: "Modern sofas starting at $449"
- Filter shows: 24 sofas in budget
- Sorts by: "Most popular"

**Product Card Design:**
- Photo showing sofa in real room (not white background)
- Price: $679
- Dimensions: 82" W × 35" D × 32" H (Kevin checks: fits!)
- Rating: 4.5 stars (247 reviews)
- Badge: "Free shipping"

---

#### Stage 2: Product Page (Day 0, 5 minutes later)

**What Kevin Sees:**

**Hero Section:**
- 6 photos: Different angles, close-ups, lifestyle shots
- "View in your space" AR button (mobile)
- Kevin tries AR → Sees sofa in his living room via camera

**Key Info (Above Fold):**
- Price: $679
- Color options: 5 swatches (Navy selected)
- "In stock - Ships in 3-5 days"
- "30-day returns"

**Decision Support:**

**Reviews Section:**
- Filter: "People with small spaces" (Kevin's concern)
- Top review: "Perfect for my 600 sq ft apartment" (photos)
- Con mentions: "Firm cushions" (appears 12 times)
- Kevin thinks: "I like firm, that's good"

**Q&A Section:**
- "Will this fit through a 32" door?" → Answer: "Yes, legs detach"
- Kevin didn't even think of this → Avoided future problem

**Comparison Table:**
- Similar sofas side-by-side
- This one: Higher rated, better price, similar quality

---

#### Stage 3: Checkout (Day 0, 15 minutes later)

**Cart Page:**
- Sofa: $679
- Suggested: "Complete the look - Coffee table $199"
- Kevin adds coffee table (smart upsell, needs one anyway)

**Checkout Flow (4 steps):**

**Step 1: Shipping**
- Address autofilled from Google account
- Delivery date: "Arriving April 15-18"
- Option: "Add assembly service +$79" → Kevin declines

**Step 2: Payment**
- Saved card (one click)
- Option: "Pay over 4 months, $0 interest" (Affirm)
- Kevin chooses monthly payments

**Step 3: Review**
- Summary with photos
- Total: $878 (sofa + table)
- Payments: $219.50/month × 4

**Step 4: Confirmation**
- "Order placed! 🎉"
- Track delivery link
- "We'll email when it ships"

**Total time: 20 minutes from search to purchase**

---

#### Stage 4: Post-Purchase (Days 1-14)

**Email Journey:**

**Day 1:** Order confirmation with itemized receipt
**Day 3:** "Your order has shipped! Track here"
**Day 7:** Delivery reminder "Arriving in 2 days"
**Day 9:** Delivery day "It's here!"
**Day 10:** "How's your new sofa?" → Review request

**Kevin's Experience:**
- Sofa arrives on time
- Assembly easier than expected (clear instructions)
- Looks exactly like photos
- Firm cushions as reviews mentioned (happy about it)

**Day 14:** Leaves 5-star review with photo
- Review asks: "Would you recommend to a friend?"
- Kevin: "Yes" → Gets referral link "$50 off for you and friend"

---

## Example 4: Developer Tool - API Monitoring SaaS

**Product:** AlertFlow (fictional API monitoring)
**Persona:** Dev team lead at startup
**Job to Be Done:** Know immediately when API goes down, not from angry customers
**Stage:** MVP

### Journey: Critical Incident Response

#### Stage 1: Setup (Day 0, 3 minutes)

**Super Fast Onboarding:**

**Screen 1:**
- "Monitor your first API in 60 seconds"
- Input: API endpoint URL
- Input: Expected status code (defaults to 200)
- Button: "Start Monitoring"

**Screen 2:**
- "Pinging every 60 seconds from 3 locations"
- Real-time: "✓ US-East: 45ms" "✓ EU-West: 120ms" "✓ Asia: 230ms"
- "Where should we alert you?" → Slack integration (OAuth, 2 clicks)

**Time to value: 3 minutes (API being monitored)**

---

#### Stage 2: First Alert (Day 7, 2:47 AM)

**Alert Notification:**

**Slack Message:**
```
🚨 AlertFlow: api.startup.com is DOWN

Status: 500 Internal Server Error
Location: US-East
Duration: 30 seconds
Incident page: https://app.alertflow.io/inc/abc123
```

**Developer Opens Incident Page:**

**What They See:**
- Timeline graph: When it started (2:47 AM)
- Error details: Full response, headers, timing
- Recent changes: "Deploy #234 at 2:45 AM" (ah-ha!)
- Quick actions: "Rollback deploy" button

**Resolution:**
- Developer rolls back deploy
- 2:50 AM: API back up
- AlertFlow detects: "✅ api.startup.com is UP"
- Slack: "Resolved after 3 minutes"

**Post-Incident:**
- Email summary sent to team
- "What caused this?" → Developer adds note: "Bad migration"
- Incident auto-closed, saved in history

**Value Delivered:**
- Detected issue in 30 seconds (vs. waiting for customer complaints)
- Provided context to diagnose (recent deploy)
- Total downtime: 3 minutes (vs. potential hours)

---

## Pattern Library: Common Interaction Solutions

### Pattern: Empty State

**Bad Example:**
```
[Empty table]
No data available.
```

**Good Example:**
```
[Illustration of empty inbox]
📬 No messages yet

Your team updates will appear here once you create your first project.

[Button: Create Project]
```

**Why Better:**
- Explains why it's empty
- Guides next action
- Friendly, not cold

---

### Pattern: Error Messages

**Bad Example:**
```
❌ Error: Invalid input
```

**Good Example:**
```
Email address should include @ symbol
Try: yourname@example.com
```

**Why Better:**
- Specific about what's wrong
- Shows example of correct format
- Helpful, not frustrating

---

### Pattern: Loading State

**Bad Example:**
```
[Spinner]
Loading...
```

**Good Example:**
```
[Progress bar: 60%]
Loading your projects...
Hang tight, we're fetching 2,847 tasks

[Still loading after 5 seconds?]
This is taking longer than usual. Your connection might be slow.
```

**Why Better:**
- Shows progress
- Sets expectations
- Explains delays

---

### Pattern: Confirmation Dialog

**Bad Example:**
```
Are you sure?
[Yes] [No]
```

**Good Example:**
```
Delete "Q4 Marketing Campaign"?

This will permanently delete:
- 47 tasks
- 12 comments
- 3 file attachments

This cannot be undone.

[Cancel] [Delete Project]
```

**Why Better:**
- Specific about what's being deleted
- Shows impact (47 tasks!)
- Clear consequences
- Button text matches action

---

## Design Decision Examples

### Decision: When to Use Modal vs. Inline Editing

**Use Modal When:**
- Action requires focus (writing long content)
- Multiple steps (wizard)
- Destructive action (needs confirmation)
- **Example:** Compose email, delete account

**Use Inline When:**
- Quick edit (changing name)
- Preserves context
- Frequent action
- **Example:** Editing task name, toggling setting

---

### Decision: When to Auto-Save vs. Manual Save

**Auto-Save When:**
- Content creation (writing, design)
- Long sessions (user might forget)
- Low risk of unwanted changes
- **Example:** Google Docs, Notion

**Manual Save When:**
- Deliberate commits (code, config)
- Users need to review before saving
- Versioning matters
- **Example:** Settings page, form submissions

---

These examples show real-world applications of interaction design principles. Use them as inspiration, adapt to your specific context!
