# Product Discussion Examples

Practical examples of clarifying questions, analyzing trade-offs, and facilitating product decisions.

---

## Example 1: Feature Request Discussion

**User asks:** "Should we add a mobile app?"

### Step 1: Clarify the Real Question

**Claude:** "Let me help unpack this. When you ask about a mobile app, I want to understand the underlying concern. Are you asking because:
- Users are requesting mobile access?
- Competitors have mobile apps?
- You're seeing drop-off on mobile web?
- You believe mobile-first is the future?

What's driving this question?"

**User:** "We're getting requests from users who want to use the product on the go."

### Step 2: Reframe as Trade-Off

**Claude:** "Got it. So the core question is: **How do we serve users who need mobile access, and what are we willing to invest/sacrifice?**

This is fundamentally a trade-off between:
- **Investment:** Native app development (iOS + Android) is 3-6 months of engineering
- **Alternatives:** Could we serve mobile users differently?
- **Opportunity cost:** What else could we build with that time?

Let me present some options with pros/cons."

### Step 3: Present Options

**Option A: Build Native Mobile Apps (iOS + Android)**

**Pros:**
- Best user experience (native performance, offline support)
- Push notifications, camera access, full device integration
- Competitive parity (if competitors have apps)
- App store presence (discovery channel)

**Cons:**
- **High cost:** 3-6 months dev time (2-3 engineers)
- **Ongoing maintenance:** 2 codebases to maintain forever
- **Delayed ROI:** Long time before value delivered
- **Platform risk:** Subject to app store rules, review delays

**Effort:** XL (3-6 months)
**Impact:** High (if mobile usage is significant)

---

**Option B: Progressive Web App (PWA)**

**Pros:**
- **Faster:** 1-2 months vs 3-6
- **One codebase:** Maintain web app, add PWA features
- **Works everywhere:** iOS, Android, desktop
- **No app store friction:** Install from web

**Cons:**
- Limited access to device features (vs native)
- Less discoverable (no app store listing)
- iOS support weaker than Android
- "Not a real app" perception for some users

**Effort:** M (1-2 months)
**Impact:** Medium-High (80% of native benefits at 30% of cost)

---

**Option C: Responsive Mobile Web (Optimize Existing)**

**Pros:**
- **Fastest:** 2-4 weeks
- **No new platform:** Improve what we have
- **Works immediately:** No install required
- **Lowest maintenance:** One codebase

**Cons:**
- No offline support
- No push notifications (limited on web)
- No app store presence
- Browser chrome takes screen space

**Effort:** S (2-4 weeks)
**Impact:** Medium (solves 60% of mobile need quickly)

---

**Option D: Don't Build Mobile, Focus on Desktop**

**Pros:**
- **Zero cost:** No mobile development
- **Full focus on core:** Improve desktop experience
- **Avoid complexity:** Don't dilute engineering resources

**Cons:**
- Lose mobile users (if significant)
- Competitive disadvantage (if competitors have mobile)
- Miss mobile-first trend

**Effort:** None
**Impact:** Depends on % of users needing mobile

---

### Step 4: Context-Specific Recommendation

**What I'd recommend depends on:**

1. **How many users are requesting this?**
   - 5% of users → Mobile web optimization (Option C)
   - 20%+ of users → PWA (Option B)
   - 50%+ and mobile-critical use case → Native (Option A)

2. **What's your product stage?**
   - **POC/MVP:** Option C or D (focus on core, defer mobile)
   - **Established + growing mobile segment:** Option B or A

3. **What's the use case on mobile?**
   - **Quick checks, notifications:** PWA sufficient (Option B)
   - **Heavy usage, offline needed:** Native required (Option A)
   - **Occasional access:** Mobile web fine (Option C)

4. **Engineering capacity?**
   - **Stretched thin:** Option C (quick win)
   - **Can dedicate 1-2 engineers for 1-2 months:** Option B
   - **Can dedicate 2-3 engineers for 6+ months:** Option A

**My recommendation:** Start with **Option C (Mobile Web Optimization)** as a 2-week sprint. Measure mobile usage and satisfaction. If metrics show strong mobile need and you have capacity, graduate to **Option B (PWA)** next quarter. Reserve **Option A (Native)** for when mobile is >50% of usage or a critical differentiator.

**This approach:**
- Tests the assumption quickly (is mobile really needed?)
- Delivers value fast (2 weeks vs 6 months)
- Preserves optionality (can still go native later)
- Minimizes opportunity cost (doesn't block other features)

---

## Example 2: Pricing Strategy Discussion

**User asks:** "How should we price this?"

### Step 1: Clarify Context

**Claude:** "Pricing is one of the highest-leverage decisions you'll make. To give you a good recommendation, I need to understand:
- **Who are you targeting?** (SMBs, enterprise, consumers?)
- **What's your cost to serve?** (CAC, infrastructure, support)
- **What value are you delivering?** (time saved, revenue generated, pain avoided)
- **What do competitors charge?** (pricing anchors in market)
- **What's your goal?** (maximize users, maximize revenue, maximize learning)

Also, what stage are you at?"

**User:** "We're MVP stage, B2B SaaS, targeting small teams (5-20 people). Competitors range from $5-$50/user/month. We save teams about 5 hours/week."

### Step 2: Reframe as Trade-Off

**Claude:** "Perfect. So the core trade-off is:

**Low price** = More users, easier to acquire, larger market
**High price** = Higher revenue per customer, but harder to acquire

At MVP stage, the primary goal is **proving product-market fit**, not maximizing revenue. But you still need to validate willingness to pay.

Let me present pricing models with trade-offs."

### Step 3: Present Options

**Option A: Free Trial → $99/month Flat (Team Plan)**

**Pros:**
- Simple (one price, easy to understand)
- High enough to filter serious customers
- Predictable revenue per customer
- 14-day trial lowers barrier

**Cons:**
- Might be too expensive for small teams (2-3 people)
- Leaves money on table with larger teams (15-20 people)
- No upsell path

**Best for:** Testing if teams value product enough to pay ~$100/mo

---

**Option B: Freemium (Free for 3 users, $10/user/month after)**

**Pros:**
- **Low friction:** Free tier gets users in the door
- **Viral:** Teams invite others, naturally expand
- **Fair pricing:** Pay for what you use
- **Upsell path:** Free → Paid is clear

**Cons:**
- **Low conversion:** Freemium typically 2-5% convert
- **Support costs:** Free users consume support
- **Perceived as "cheap":** Harder to go upmarket later

**Best for:** Maximizing user count, building network effects

---

**Option C: 30-Day Free Trial → $15/user/month**

**Pros:**
- **Higher conversion than freemium:** 15-25% typical
- **Qualified users only:** Trial shows intent
- **Per-user pricing:** Scales with team size
- **Industry standard:** Familiar model

**Cons:**
- Pressure to activate in 30 days
- Some teams lost at trial end (didn't get value yet)
- Monthly churn possible (not annual commitment)

**Best for:** Balancing acquisition and revenue

---

**Option D: Annual Only, $1200/year (5-seat minimum)**

**Pros:**
- **Cash upfront:** Helps runway
- **Lower churn:** Annual commitment
- **Higher LTV:** More revenue per customer
- **Signals seriousness:** Filters out tire-kickers

**Cons:**
- **High barrier:** $1200 is big commitment
- **Slower sales cycle:** Requires budget approval
- **Fewer trials:** Can't "try before buy" easily

**Best for:** Established product with proven value, enterprise focus

---

### Step 4: Recommendation Based on Goals

**At MVP stage, I'd recommend Option C: 30-day free trial → $15/user/month**

**Rationale:**
1. **Balances learning and revenue:**
   - You get paid (validates willingness to pay)
   - Trial lets users experience value first
   - Per-user pricing is fair and scalable

2. **Competitive positioning:**
   - $15/user is mid-market (not cheapest, not most expensive)
   - Leaves room to add premium features later

3. **Aligns with your value prop:**
   - 5 hours saved/week × team size = clear ROI
   - At $15/user, a 5-person team pays $75/mo to save 25 team-hours
   - ROI is obvious ($75 for 25 hours = $3/hour saved)

4. **Flexibility:**
   - Can add annual discount later (e.g., pay yearly, get 2 months free)
   - Can add enterprise tier (custom pricing, premium support)
   - Can adjust per-user price based on data

**What to measure:**
- **Trial → Paid conversion rate:** Target 15-25%
- **If conversion too low (<10%):** Price might be too high, or onboarding failing
- **If conversion high (>30%):** You might be underpriced
- **Churn in first 3 months:** If >10%/mo, product-market fit issue

**Iterate:** After 50 customers, revisit pricing. You'll have real data on CAC, LTV, churn to optimize.

---

## Example 3: Build vs Buy Discussion

**User asks:** "Should we build our own authentication system or use Auth0?"

### Step 1: Clarify Stakes

**Claude:** "Authentication is a classic build-vs-buy decision. Let me understand the context:
- **Security requirements?** (compliance, multi-factor, etc.)
- **User experience needs?** (social login, SSO, passwordless?)
- **Team experience?** (Have you built auth before?)
- **Timeline pressure?** (Need this in 1 week or 3 months?)

Also, is authentication a core differentiator for your product, or is it table stakes?"

**User:** "We need basic email/password, social login (Google, GitHub), and maybe SSO for enterprise later. Timeline is flexible, but sooner is better. Auth isn't our differentiator—our core product is the value."

### Step 2: Reframe as Trade-Off

**Claude:** "Perfect. This is a classic trade-off:

**Build:** Full control, no recurring cost, custom UX
**Buy:** Fast, proven, maintained by experts, recurring cost

Since auth isn't your differentiator, this leans toward **buy**. But let me show the full trade-off."

### Step 3: Present Options

**Option A: Build Custom Auth**

**Pros:**
- **Full control:** Exactly the UX you want
- **No vendor lock-in:** You own the code
- **No recurring cost:** Just infrastructure
- **Learning:** Team gains auth expertise

**Cons:**
- **Time:** 2-4 weeks for basic, 2-3 months for enterprise-grade
- **Security risk:** Easy to mess up (password storage, session management, CSRF, etc.)
- **Ongoing maintenance:** Security patches, new features, support
- **Compliance burden:** GDPR, SOC 2 audits fall on you

**Effort:** M-L (2-4 weeks for MVP, ongoing maintenance)
**Risk:** High (security vulnerabilities)

---

**Option B: Use Auth0 (or similar: Clerk, Supabase Auth, AWS Cognito)**

**Pros:**
- **Fast:** Integrate in 1-2 days
- **Proven:** Handles millions of users, battle-tested
- **Security:** Experts manage it, automatic patches
- **Features included:** MFA, social login, SSO, passwordless
- **Compliance:** SOC 2, GDPR handled by vendor

**Cons:**
- **Recurring cost:** ~$250-$1500/mo (scales with users)
- **Vendor lock-in:** Switching later is painful
- **Less control:** UX constrained by vendor
- **Dependency:** If vendor goes down, you're down

**Effort:** S (1-2 days integration)
**Risk:** Low (security), Medium (vendor dependency)

---

**Option C: Open Source Auth (e.g., Keycloak, Ory)**

**Pros:**
- **No licensing cost:** Free software
- **More control than SaaS:** Self-hosted
- **Feature-rich:** Enterprise features included
- **Community support:** Mature projects

**Cons:**
- **Setup complexity:** Harder than Auth0
- **Maintenance burden:** You manage infrastructure, updates
- **Limited support:** Community forums, not dedicated support
- **Overkill for MVP:** Enterprise features you don't need yet

**Effort:** M (1 week setup, ongoing ops)
**Risk:** Medium (operational complexity)

---

### Step 4: Recommendation

**For your situation, I'd recommend Option B: Auth0 (or Clerk/Supabase if cost-sensitive)**

**Rationale:**
1. **Auth isn't your differentiator:** Don't build what you can buy
2. **Security matters:** One mistake (password leak) could kill the business
3. **Speed to market:** 1-2 days vs 2-4 weeks
4. **Focus:** Your team should build your core product, not auth

**Cost-benefit:**
- **Auth0:** ~$250/mo for <1000 users, $1500/mo for 10k users
- **Building it:** 2-4 weeks × $5k/week (loaded engineer cost) = $10-20k upfront, plus ongoing maintenance
- **Payback:** Auth0 pays for itself if it saves >1 month of engineering time

**When to reconsider:**
- **If you hit 50k+ users:** Economics shift, custom might be cheaper long-term
- **If auth becomes a differentiator:** (e.g., you add unique auth UX)
- **If vendor pricing becomes painful:** (but by then you have revenue to hire auth engineers)

**Start with Auth0, revisit when you have scale or specific needs.**

---

## Example 4: Scope Reduction Discussion

**User says:** "We're behind schedule. Should we cut features to make the deadline?"

### Step 1: Clarify the Stakes

**Claude:** "Sounds like you're facing a classic trade-off: **Ship on time with less** vs **Ship late with more**. Before we decide, let me understand:
- **Why is the deadline important?** (Launch event? Investor demo? Competitive pressure?)
- **How far behind are you?** (1 week or 2 months?)
- **What features are in scope?** (Must-haves vs nice-to-haves?)
- **What's the risk of slipping?** (Lost opportunity, team morale, credibility?)

Also, is this POC, MVP, or established product?"

**User:** "It's our MVP. We're 3 weeks behind. The deadline is soft (no external commitment), but team morale is suffering from the slip. We have 10 features planned; realistically need 8 to be viable."

### Step 2: Reframe as Trade-Off

**Claude:** "Got it. So the real trade-off is:

**Ship with 8 features now** = Team momentum, faster learning, but missing 2 features
**Ship with all 10 features later** = Complete vision, but 3 more weeks, risk morale/focus

At MVP stage, **shipping and learning** usually beats **perfection**. Let me present options."

### Step 3: Present Options

**Option A: Cut to Core 8, Ship Now**

**Pros:**
- **Momentum:** Team feels progress, morale boost
- **Faster learning:** Get user feedback 3 weeks sooner
- **Focus:** Forces prioritization (what's truly essential?)
- **Avoid scope creep:** Deadline prevents feature bloat

**Cons:**
- Might miss features users expect
- Need to communicate cuts to stakeholders
- Could look "unfinished"

**Recommendation:** Identify 8 must-haves using MoSCoW (Must/Should/Could/Won't)

---

**Option B: Ship All 10, Accept 3-Week Delay**

**Pros:**
- **Complete vision:** Product feels finished
- **No compromises:** All features users might need
- **Avoid rework:** Don't have to add features later

**Cons:**
- **Delayed feedback:** 3 more weeks without user validation
- **Morale risk:** Team already frustrated by slip
- **Opportunity cost:** 3 weeks could be spent on iteration based on real feedback

**When this makes sense:** If missing features would seriously hurt first impression or make product unusable

---

**Option C: Phased Release (8 now, 2 next sprint)**

**Pros:**
- **Best of both:** Ship fast AND deliver all features
- **Learning loop:** Iterate on first 8 based on feedback before adding final 2
- **Manage expectations:** Communicate roadmap to users
- **Sustainable pace:** Doesn't burn out team

**Cons:**
- Need to communicate "more coming soon"
- Some users might want those 2 features immediately

**When this makes sense:** If 8 features deliver core value and 2 are enhancements

---

### Step 4: Recommendation

**I'd recommend Option C: Phased Release (8 now, 2 in Sprint +1)**

**Rationale:**
1. **Morale:** Shipping NOW addresses team frustration
2. **Learning:** Get feedback on core 8, validate before building final 2
3. **Flexibility:** What if user feedback says "we don't need feature 9, but we DO need feature X"?
4. **Sustainable:** Avoids crunch, sets pattern for future releases

**How to decide which 8:**
**Must-Have criteria (all must be true):**
- User cannot achieve core job-to-be-done without it
- No reasonable workaround exists
- Removing it makes product fundamentally unusable

**Run this test:**
"If we shipped without feature X, would users be able to [accomplish core job]?"
- If yes → Nice-to-have (defer)
- If no → Must-have (keep)

**Communication:**
- **Internal:** "We're shipping phase 1 with the 8 essential features. Phase 2 follows in 2 weeks."
- **External (if relevant):** "Our MVP includes [8 features]. We're actively developing [2 more features] based on your feedback."

**Next steps:**
1. Identify the 8 must-haves (can be done in 1-hour team meeting)
2. Ship the 8
3. Gather user feedback for 1-2 weeks
4. Re-prioritize final 2 features based on real data
5. Ship phase 2

**This turns a schedule slip into a learning opportunity.**

---

## Example 5: Competitive Response Discussion

**User asks:** "Our competitor just launched feature X. Should we build it too?"

### Step 1: Clarify the Threat

**Claude:** "Competitor moves can feel urgent, but let's think strategically before reacting. Help me understand:
- **Is this feature their differentiator, or table stakes?**
- **Are we losing customers because we lack it?**
- **Does it align with our strategy?**
- **What's our unique advantage—are we defending it or abandoning it to chase them?**

Also, what's the competitive dynamic? Are they ahead, behind, or neck-and-neck?"

**User:** "They're ahead in market share. This feature is getting press. We haven't lost customers yet, but I'm worried we will."

### Step 2: Reframe as Trade-Off

**Claude:** "Got it. So the trade-off is:

**Build feature X (defensive)** = Competitive parity, but we're playing their game
**Build our differentiator (offensive)** = Widen our unique advantage, but accept gap in feature X

This is a classic strategic choice: **React vs Lead**. Let me present options."

### Step 3: Present Options

**Option A: Build Feature X (Competitive Parity)**

**Pros:**
- Avoid losing customers over this specific gap
- Press mentions might help (if feature is buzzworthy)
- Signals "we're keeping up"

**Cons:**
- **Reactive:** We're following, not leading
- **Opportunity cost:** Time not spent on our differentiator
- **Arms race:** They'll launch the next thing, are we going to chase forever?

**When to choose:** If feature X is table stakes (users expect it) and we're bleeding customers without it

---

**Option B: Double Down on Our Differentiator**

**Pros:**
- **Strategic:** Play to our strengths
- **Differentiation:** Widen the gap on what makes us unique
- **Brand:** Signals confidence, vision, independence

**Cons:**
- Risk losing customers who want feature X
- Competitor might pull ahead on their differentiator AND have our feature

**When to choose:** If our differentiator is strong and feature X is not table stakes

---

**Option C: Hybrid Approach (80% Solution Fast)**

**Pros:**
- **Pragmatic:** Address the gap without full investment
- **Speed:** Ship in 1-2 weeks instead of 1-2 months
- **Focus:** Reserve most resources for differentiator

**Cons:**
- 80% solution might not be enough
- Could feel half-baked

**When to choose:** If feature X matters but isn't critical

---

### Step 4: Recommendation (Strategic Lens)

**Questions to answer:**

1. **Is feature X table stakes or differentiator?**
   - **Table stakes:** (e.g., "login with Google") → Build it (users expect it)
   - **Differentiator:** (e.g., their unique algorithm) → Focus on ours instead

2. **Are we losing customers?**
   - **Yes, measurably:** Build feature X (Option A)
   - **No, just worried:** Don't react emotionally (Option B)

3. **How strong is our differentiator?**
   - **Very strong:** Double down (Option B)
   - **Weak:** Need to catch up (Option A)

**My recommendation (based on "ahead in market share, no customer losses yet"):**

**Option B: Double down on our differentiator**

**Rationale:**
- No evidence of customer loss = no fire to fight
- They're ahead, so chasing them keeps us behind
- Your best chance is to differentiate on something they CAN'T copy easily

**What to do instead:**
1. **Monitor:** Track if feature X causes churn (set up alert)
2. **Communicate:** Proactively tell customers why you're NOT building it (focus on your strength)
3. **Differentiate:** Make your unique value so strong that feature X doesn't matter
4. **Revisit:** If you start losing customers, re-evaluate

**Example messaging:**
"Our competitor launched feature X. We've chosen to focus on [your differentiator] because our customers tell us that's what matters most. If feature X becomes critical to you, let us know—we're listening."

**This positions you as confident and strategic, not reactive.**

---

## Discussion Facilitation Tips

### Pattern: User Asks Vague Question

**Example:** "What should we do about churn?"

**Don't:** Jump to solutions ("Add a retention campaign!")

**Do:** Clarify first
- "What's your current churn rate?"
- "Which segment is churning most?"
- "Why are they leaving? (surveys, exit interviews?)"
- "What's an acceptable churn rate for your business?"

**Then:** Present options based on root cause

---

### Pattern: User Has Strong Opinion

**Example:** "We NEED to build a mobile app!"

**Don't:** Argue directly ("No, that's wrong")

**Do:** Validate, then explore
- "I hear that mobile is important to you. Help me understand why."
- "What problem would mobile solve that we can't solve another way?"
- "If we DON'T build mobile, what's the risk?"

**Then:** Present alternatives with trade-offs

---

### Pattern: User Wants "Best Practice"

**Example:** "What's the best pricing model?"

**Don't:** Give one-size-fits-all answer

**Do:** "It depends on your context. Let me ask..."
- Stage (POC/MVP/Established)
- Target customer (B2B/B2C, SMB/Enterprise)
- Value prop (time saved, revenue generated, etc.)
- Competitive context

**Then:** "Based on X, Y, Z, here are the options..."

---

## Key Takeaways

1. **Clarify before solving:** Most questions hide deeper questions
2. **Frame as trade-offs:** Every decision sacrifices something
3. **Present options:** Rarely is there only one path
4. **Context matters:** POC ≠ MVP ≠ Established
5. **Avoid dogma:** "Best practices" depend on your situation
6. **Measure, don't guess:** Data > opinions
7. **Preserve optionality:** Reversible decisions move fast, irreversible decisions move slow
